#!/usr/bin/env python3
"""
CarInsuranceImmigrants.us — Master Site Builder
Uses split API calls (meta + sections + table + faq separately)
to avoid JSON parse errors on large responses.
"""

import os, json, re, time, datetime, argparse, anthropic, xml.etree.ElementTree as ET
from pathlib import Path
from prompts import (SYSTEM_PROMPT, meta_prompt, sections_prompt, table_prompt,
                     howto_prompt, faq_prompt, state_meta_prompt, state_sections_prompt,
                     state_table_prompt, state_faq_prompt, homepage_prompt)

client     = anthropic.Anthropic()
MODEL      = "claude-haiku-4-5-20251001"
OUTPUT_DIR = Path(".")

with open("config.json") as f:
    CONFIG = json.load(f)
with open("template.html") as f:
    TEMPLATE = f.read()

SITE      = CONFIG["site"]
LANGUAGES = CONFIG["languages"]
PILLARS   = CONFIG["pillars"]
YEAR      = datetime.date.today().year
LAST_REV  = datetime.date.today().strftime("%B %Y")
LOCALE_MAP = {"en":"en_US","es":"es_US","zh":"zh_CN","ar":"ar_SA","pt":"pt_BR",
              "vi":"vi_VN","tl":"tl_PH","ko":"ko_KR","ru":"ru_RU","pl":"pl_PL"}

ALL_PAGES = {}
for pillar in PILLARS:
    for page in pillar["pages"]:
        ALL_PAGES[page["slug"]] = {"title":page["title"],"icon":pillar.get("icon","📄"),"desc":page.get("immigrant_angle","")[:80]}

# ─── SITEMAP ──────────────────────────────────────────────────────────────────
SITEMAP_FILE = OUTPUT_DIR / "sitemap.xml"

def load_sitemap():
    urls = {}
    if SITEMAP_FILE.exists():
        try:
            tree = ET.parse(str(SITEMAP_FILE))
            ns = "http://www.sitemaps.org/schemas/sitemap/0.9"
            for u in tree.getroot():
                loc = u.find(f"{{{ns}}}loc")
                pri = u.find(f"{{{ns}}}priority")
                if loc is not None:
                    urls[loc.text] = {"priority": pri.text if pri is not None else "0.8", "lastmod": datetime.date.today().isoformat()}
        except: pass
    return urls

sitemap_urls = load_sitemap()

def add_sitemap(url, priority="0.8"):
    sitemap_urls[url] = {"priority": priority, "lastmod": datetime.date.today().isoformat()}

def write_sitemap():
    root = ET.Element("urlset")
    root.set("xmlns","http://www.sitemaps.org/schemas/sitemap/0.9")
    for loc, d in sorted(sitemap_urls.items()):
        u = ET.SubElement(root,"url")
        ET.SubElement(u,"loc").text      = loc
        ET.SubElement(u,"lastmod").text  = d["lastmod"]
        ET.SubElement(u,"priority").text = d["priority"]
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ")
    tree.write(str(SITEMAP_FILE), encoding="unicode", xml_declaration=True)
    print(f"\n✅ sitemap.xml — {len(sitemap_urls)} URLs")

# ─── HELPERS ──────────────────────────────────────────────────────────────────
def lp(lang): return lang["prefix"] + "/" if lang["prefix"] else ""

def page_url(slug, lang):
    p = lp(lang)
    return f"{SITE['domain']}/{p}{slug}/" if slug else (f"{SITE['domain']}/{p}" if p else f"{SITE['domain']}/")

def write_file(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"  ✅ {path}")

def clean_json(raw: str) -> str:
    raw = re.sub(r'^```(?:json)?\s*','',raw,flags=re.MULTILINE)
    raw = re.sub(r'\s*```\s*$','',raw,flags=re.MULTILINE)
    raw = raw.strip()
    # Remove Arabic/Persian commas that break JSON
    raw = raw.replace('\u060c', ',').replace('،', ',')
    # Remove RTL/LTR marks
    raw = raw.replace('\u200f', '').replace('\u200e', '')
    s,e = raw.find('{'), raw.rfind('}')
    return raw[s:e+1] if s!=-1 and e!=-1 else raw

def call_claude(prompt: str, max_tokens=2000, retries=3) -> dict:
    """Small focused API calls — max 2000 tokens keeps JSON clean."""
    messages = [{"role":"user","content":prompt}]
    last_raw = ""
    for attempt in range(retries):
        try:
            resp = client.messages.create(
                model=MODEL, max_tokens=max_tokens,
                system=SYSTEM_PROMPT, messages=messages
            )
            last_raw = resp.content[0].text.strip()
            return json.loads(clean_json(last_raw))
        except json.JSONDecodeError as e:
            print("    WARNING JSON attempt "+str(attempt+1)+": "+str(e)[:60])
            if attempt < retries-1:
                messages.append({"role":"assistant","content":last_raw})
                messages.append({"role":"user","content":"JSON error: "+str(e)[:100]+". Return ONLY valid JSON. No apostrophes. No line breaks in strings. No trailing commas."})
                time.sleep(2)
            else:
                raise
        except Exception as e:
            print("    WARNING API attempt "+str(attempt+1)+": "+str(e)[:60])
            if attempt < retries-1: time.sleep(5)
            else: raise

def build_hreflang(slug):
    tags = "\n  ".join(f'<link rel="alternate" hreflang="{l["hreflang"]}" href="{page_url(slug,l)}">' for l in LANGUAGES)
    return tags + f'\n  <link rel="alternate" hreflang="x-default" href="{page_url(slug,LANGUAGES[0])}">'

def build_lang_switcher(slug, current_lang):
    return "\n      ".join(
        f'<a href="{page_url(slug,l)}" class="{"active" if l["code"]==current_lang["code"] else ""}">{l["name"]}</a>'
        for l in LANGUAGES)

def build_breadcrumb(crumbs):
    li = "".join(f'<li><a href="{u}">{t}</a></li>' if u else f'<li>{t}</li>' for t,u in crumbs)
    schema = {"@context":"https://schema.org","@type":"BreadcrumbList",
              "itemListElement":[{"@type":"ListItem","position":i+1,"name":t,**({"item":u} if u else {})} for i,(t,u) in enumerate(crumbs)]}
    return f'<div class="breadcrumb-bar"><ol>{li}</ol></div>', schema

def build_sidebar(prefix):
    links = "".join(f'<li><a href="/{prefix}{p["slug"]}/">{p["icon"]} {p["title"]}</a></li>' for p in PILLARS)
    return f'''<aside class="sidebar">
  <div class="sidebar-card"><h3>Topics</h3><ul class="practice-area-list">{links}</ul></div>
  <div class="sidebar-card disclaimer-card">
    <h3>Important</h3>
    <p>General information only. Insurance policies and state laws change frequently. Always verify directly with insurers and your state DMV.</p>
    <p style="margin-top:8px"><a href="/legal/disclaimer/" style="color:#b45309">Full disclaimer</a></p>
  </div>
</aside>'''

def build_schema(slug, lang, meta_title, meta_desc, faq_pairs, howto_steps, bc_schema):
    schemas = [{"@context":"https://schema.org","@type":"Article","headline":meta_title,"description":meta_desc,
                "url":page_url(slug,lang),"inLanguage":lang["hreflang"],
                "dateModified":datetime.date.today().isoformat(),"datePublished":"2025-06-01",
                "author":{"@type":"Organization","name":"CarInsuranceImmigrants.us Editorial Team"},
                "publisher":{"@type":"Organization","name":"Car Insurance Immigrants","url":SITE["domain"]}}]
    if faq_pairs:
        schemas.append({"@context":"https://schema.org","@type":"FAQPage",
            "mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq_pairs]})
    if howto_steps:
        schemas.append({"@context":"https://schema.org","@type":"HowTo","name":meta_title,
            "step":[{"@type":"HowToStep","position":i+1,"name":s["name"],"text":s["text"]} for i,s in enumerate(howto_steps)]})
    schemas.append(bc_schema)
    return json.dumps(schemas, ensure_ascii=False, indent=2)

def assemble_html(meta_title, meta_desc, canonical, lang, slug, bc_html, page_content, schema_json):
    prefix = lp(lang)
    html = TEMPLATE
    for k,v in {
        "{{META_TITLE}}":meta_title,"{{META_DESCRIPTION}}":meta_desc,
        "{{CANONICAL_URL}}":canonical,"{{LANG_CODE}}":lang["code"],
        "{{DIR}}":lang["dir"],"{{OG_LOCALE}}":LOCALE_MAP.get(lang["code"],"en_US"),
        "{{HREFLANG_TAGS}}":build_hreflang(slug),"{{LANG_SWITCHER}}":build_lang_switcher(slug,lang),
        "{{LANG_PREFIX}}":prefix,"{{BREADCRUMB_HTML}}":bc_html,
        "{{PAGE_CONTENT}}":page_content,"{{SCHEMA_JSON}}":schema_json,
        "{{YEAR}}":str(YEAR),"{{LAST_REVIEWED}}":LAST_REV
    }.items():
        html = html.replace(k,v)
    return html

# ─── PAGE BUILDER — SPLIT CALLS ───────────────────────────────────────────────
def build_page_content(page, pillar, lang):
    """Build a page using 4 small API calls instead of 1 giant one."""
    title   = page["title"]
    slug    = page["slug"]
    angle   = page["immigrant_angle"]
    ptype   = page["type"]
    lname   = lang["name"]
    lcomm   = lang.get("community","")
    has_howto = "HowTo" in page.get("schema",[])

    # Call 1 — meta (small, fast, clean)
    meta = call_claude(meta_prompt(title, slug, angle, lname, lcomm), max_tokens=600)

    # Call 2 — sections
    secs = call_claude(sections_prompt(title, slug, angle, ptype, lname, lcomm), max_tokens=1800)

    # Call 3 — table + steps (combined, both small)
    tbl  = call_claude(table_prompt(title, slug, angle, lname), max_tokens=600)
    steps = call_claude(howto_prompt(title, slug, lname), max_tokens=600) if has_howto else {"has_steps": False}

    # Call 4 — FAQ
    faqs = call_claude(faq_prompt(title, slug, angle, page.get("faq_count",7), lname, lcomm), max_tokens=1200)

    return meta, secs, tbl, steps, faqs


def render_page(slug, meta, secs, tbl, steps, faqs, lang, pillar, breadcrumbs):
    prefix = lp(lang)
    bc_html, bc_schema = build_breadcrumb(breadcrumbs)
    faq_pairs  = [(f["q"],f["a"]) for f in faqs.get("faq",[])]
    howto_list = steps.get("steps") if steps.get("has_steps") else None

    schema_json = build_schema(slug, lang, meta["meta_title"], meta["meta_description"],
                               faq_pairs, howto_list, bc_schema)

    # Data table
    table_html = ""
    if tbl.get("has_table") and tbl.get("headers") and tbl.get("rows"):
        cap  = f"<caption style='caption-side:top;font-weight:700;padding:10px 16px;background:#f4f7fb;text-align:left'>{tbl.get('caption','')}</caption>"
        rows = "".join("<tr>"+"".join(f"<td>{c}</td>" for c in row)+"</tr>" for row in tbl["rows"])
        table_html = f'<div class="data-table-wrap"><table>{cap}<thead><tr>{"".join(f"<th>{h}</th>" for h in tbl["headers"])}</tr></thead><tbody>{rows}</tbody></table></div>'

    # Steps
    steps_html = ""
    if howto_list:
        lis = "".join(f'<li><div class="step-num">{i+1}</div><div class="step-content"><h4>{s["name"]}</h4><p>{s["text"]}</p></div></li>' for i,s in enumerate(howto_list))
        steps_html = f'<h2>Step-by-Step Guide</h2><ul class="steps-list">{lis}</ul>'

    # Sections
    sections_html = "".join(f'<h2>{s["h2"]}</h2>{s["body"]}' for s in secs.get("sections",[]))

    # Sources
    sources_html = ""
    sources = faqs.get("sources",[])
    if sources:
        links = "".join(f'<li><a href="{s["url"]}" target="_blank" rel="noopener noreferrer">↗ {s["label"]}</a></li>' for s in sources if s.get("url"))
        if links: sources_html = f'<div class="official-sources"><h3>📋 Official Sources</h3><ul>{links}</ul></div>'

    # FAQ
    faq_html = ""
    if faq_pairs:
        items = "".join(f'<div class="faq-item"><button class="faq-q">{q}<span class="chevron">▾</span></button><div class="faq-a"><p>{a}</p></div></div>' for q,a in faq_pairs)
        faq_html = f'<div class="faq-section"><h2>Frequently Asked Questions</h2>{items}</div>'

    # Warning / tip
    warning_html = f'<div class="warning-box"><strong>Important:</strong> {secs["warning"]}</div>' if secs.get("warning") else ""
    info_html    = f'<div class="info-box">💡 {secs["info_tip"]}</div>' if secs.get("info_tip") else ""

    # Related
    related_html = ""
    page_obj = next((pg for p in PILLARS for pg in p["pages"] if pg["slug"]==slug), None)
    if page_obj and page_obj.get("related"):
        cards = [f'<a href="/{prefix}{r}/" class="related-card"><div class="icon">{ALL_PAGES.get(r,{}).get("icon","📄")}</div><div class="title">{ALL_PAGES.get(r,{}).get("title","")}</div><div class="desc">{ALL_PAGES.get(r,{}).get("desc","")}</div></a>'
                 for r in page_obj["related"][:5] if ALL_PAGES.get(r)]
        if cards: related_html = f'<div class="related-section"><h2>Related Topics</h2><div class="related-grid">{"".join(cards)}</div></div>'

    icon    = next((p["icon"] for p in PILLARS for pg in p["pages"] if pg["slug"]==slug), "🚗")
    section = next((p["title"] for p in PILLARS for pg in p["pages"] if pg["slug"]==slug), "Car Insurance")

    page_content = f'''<div class="hero">
  <div style="max-width:1200px;margin:0 auto;text-align:center">
    <span class="last-reviewed">✅ Last reviewed: {LAST_REV}</span>
    <h1>{meta["h1"]}</h1>
    <p class="subtitle">{meta.get("intro","")}</p>
    <div class="badges">
      <span class="badge">🇺🇸 All 50 States</span>
      <span class="badge">All Immigration Statuses</span>
      <span class="badge">{icon} {section}</span>
    </div>
  </div>
</div>
<div class="page-container">
  <main>
    <div class="definition-box"><strong>Quick Answer: </strong>{meta["definition"]}</div>
    {warning_html}{info_html}
    {sections_html}
    {table_html}{steps_html}
    {sources_html}
    {faq_html}
    {related_html}
  </main>
  {build_sidebar(prefix)}
</div>'''

    return assemble_html(meta["meta_title"], meta["meta_description"],
                         page_url(slug,lang), lang, slug, bc_html, page_content, schema_json)


def build_pillar_page(page, pillar, lang):
    slug  = page["slug"]
    prefix = lp(lang)
    parts  = slug.split("/")
    crumbs = [("Home", f"/{prefix}" if prefix else "/")]
    if slug != pillar["slug"]:
        crumbs.append((pillar["title"], f"/{prefix}{pillar['slug']}/"))
    if len(parts) >= 3:
        inter = ALL_PAGES.get("/".join(parts[:2]),{})
        if inter: crumbs.append((inter["title"], f"/{prefix}{'/'.join(parts[:2])}/"))
    crumbs.append((page["title"], None))

    meta, secs, tbl, steps, faqs = build_page_content(page, pillar, lang)
    return render_page(slug, meta, secs, tbl, steps, faqs, lang, pillar, crumbs)


def build_state_page(state, lang):
    slug    = f"states/{state.lower().replace(' ','-')}"
    prefix  = lp(lang)
    lname   = lang["name"]
    crumbs  = [("Home", f"/{prefix}" if prefix else "/"), ("By State", f"/{prefix}states/"), (state, None)]
    states_pillar = next(p for p in PILLARS if p["id"]=="states")

    meta   = call_claude(state_meta_prompt(state, lname), max_tokens=600)
    secs   = call_claude(state_sections_prompt(state, lname), max_tokens=1500)
    tbl_d  = call_claude(state_table_prompt(state), max_tokens=600)
    faqs   = call_claude(state_faq_prompt(state, lname), max_tokens=1000)
    tbl    = {"has_table": True, **tbl_d} if tbl_d.get("headers") else {"has_table": False}
    steps  = {"has_steps": False}

    return render_page(slug, meta, secs, tbl, steps, faqs, lang, states_pillar, crumbs), slug


def build_homepage(lang):
    prefix  = lp(lang)
    content = call_claude(homepage_prompt(lang), max_tokens=600)

    lang_btns = "".join(
        f'<a href="/{l["prefix"]}/" class="lang-btn">{l["name"]}</a>' if l["prefix"]
        else '<a href="/" class="lang-btn">English</a>'
        for l in LANGUAGES)

    cards = "".join(f'<a href="/{prefix}{p["slug"]}/" class="hub-card"><div class="card-icon">{p["icon"]}</div><h3>{p["title"]}</h3><p>{p["description"]}</p></a>' for p in PILLARS)

    top_q = [
        ("questions/can-undocumented-get-car-insurance","Can I get insurance if undocumented?"),
        ("questions/will-insurance-company-call-ice","Will they call ICE?"),
        ("questions/what-is-itin-car-insurance","Can I use ITIN instead of SSN?"),
        ("questions/mexican-license-texas","Can I use my foreign license?"),
        ("getting-insured/same-day","Can I get insured same day?"),
    ]
    q_links = "".join(f'<a href="/{prefix}{s}/" style="display:block;color:#f59e0b;margin-bottom:8px;font-size:0.95rem">→ {t}</a>' for s,t in top_q)

    schema = json.dumps([
        {"@context":"https://schema.org","@type":"Organization","name":"Car Insurance Immigrants","url":SITE["domain"],"description":SITE["description"]},
        {"@context":"https://schema.org","@type":"WebSite","name":"Car Insurance Immigrants","url":SITE["domain"]}
    ], ensure_ascii=False, indent=2)

    page_content = f'''<div class="home-hero">
  <div style="max-width:900px;margin:0 auto">
    <h1>{content.get("hero_headline","Car Insurance for Immigrants — Every Question Answered")}</h1>
    <p>{content.get("hero_subtext","Free car insurance information for immigrants in all 50 states.")}</p>
    <div class="lang-bar">{lang_btns}</div>
  </div>
  <div class="stats-bar">
    <div class="stat"><div class="num">53M+</div><div class="label">Immigrants in the US</div></div>
    <div class="stat"><div class="num">10</div><div class="label">Languages</div></div>
    <div class="stat"><div class="num">50</div><div class="label">States Covered</div></div>
    <div class="stat"><div class="num">2,000+</div><div class="label">Information Pages</div></div>
  </div>
</div>
<div style="max-width:1200px;margin:40px auto;padding:0 24px">
  <div style="background:#fff0f0;border:2px solid #e85d26;border-radius:8px;padding:20px 24px;margin-bottom:40px;display:flex;gap:16px;align-items:flex-start">
    <span style="font-size:2rem;flex-shrink:0">❓</span>
    <div>
      <strong style="color:#c0392b;font-size:1.05rem">{content.get("urgent_question","Common Questions We Answer")}</strong>
      <div style="margin-top:8px">{q_links}</div>
    </div>
  </div>
  <h2 style="font-size:1.8rem;color:#1a3a5c;margin-bottom:8px;border:none">Everything You Need to Know</h2>
  <p style="color:#5a6a7a;margin-bottom:24px">Car insurance answers for immigrants — the questions others will not answer, in your language.</p>
  <div class="hub-grid">{cards}</div>
  <div style="background:#eef4ff;border-radius:12px;padding:32px;margin:40px 0">
    <h2 style="border:none;margin-top:0;color:#1a3a5c">About This Site</h2>
    <p>{content.get("about_blurb","CarInsuranceImmigrants.us provides free car insurance information for immigrants across the United States.")}</p>
    <p style="margin-top:12px"><a href="/about/">About us</a> · <a href="/legal/disclaimer/">Disclaimer</a> · <a href="/states/">All 50 states</a></p>
  </div>
</div>'''

    html = TEMPLATE
    for k,v in {
        "{{META_TITLE}}":"Car Insurance for Immigrants in the US | CarInsuranceImmigrants.us",
        "{{META_DESCRIPTION}}":"Free car insurance info for immigrants. No SSN? Foreign license? Undocumented? Every question answered in 10 languages.",
        "{{CANONICAL_URL}}":page_url("",lang),"{{LANG_CODE}}":lang["code"],"{{DIR}}":lang["dir"],
        "{{OG_LOCALE}}":LOCALE_MAP.get(lang["code"],"en_US"),
        "{{HREFLANG_TAGS}}":build_hreflang(""),"{{LANG_SWITCHER}}":build_lang_switcher("",lang),
        "{{LANG_PREFIX}}":prefix,"{{BREADCRUMB_HTML}}":"",
        "{{PAGE_CONTENT}}":page_content,"{{SCHEMA_JSON}}":schema,
        "{{YEAR}}":str(YEAR),"{{LAST_REVIEWED}}":LAST_REV
    }.items():
        html = html.replace(k,v)
    return html


def build_static_pages():
    pages = {
        "about/index.html":("About CarInsuranceImmigrants.us","Free car insurance info for immigrants in the US — no SSN needed to read. Every question in 10 languages.",
            f'<div class="page-container full-width"><main><span class="last-reviewed">Last reviewed: {LAST_REV}</span><h1 style="color:#1a3a5c;font-size:2rem;margin:16px 0">About CarInsuranceImmigrants.us</h1><p>The most comprehensive car insurance resource for immigrants in the US. We answer the questions mainstream sites ignore.</p><h2>Our Mission</h2><p>Over 53 million immigrants in the US need car insurance. Many are afraid to ask basic questions. We give honest, accurate answers in their language.</p><h2>What We Cover</h2><p>Getting insured without SSN · By immigration status · Common questions · Foreign license insurance · After accidents · Coverage explained · All 50 states · Saving money</p><h2>Notice</h2><p>Information resource only. Not an insurance company or broker. Always verify with insurers and your state DMV.</p></main></div>'),
        "legal/disclaimer/index.html":("Disclaimer | CarInsuranceImmigrants.us","General information only. Insurance rates, policies, and state laws change. Always verify directly with insurers.",
            f'<div class="page-container full-width"><main><div class="warning-box"><strong>Read before using this site.</strong></div><h1 style="color:#1a3a5c;font-size:2rem;margin:16px 0">Disclaimer</h1><h2>General Information Only</h2><p>This site provides general educational information. We are not an insurance company, broker, or agent.</p><h2>Information Changes</h2><p>Insurance rates, insurer policies, state laws, and license requirements change frequently. Always verify current information directly with insurance companies and your state DMV.</p><h2>Not Affiliated With Any Insurer</h2><p>We are independent. Not affiliated with, endorsed by, or paid by any insurance company.</p><h2>Privacy</h2><p>Reading this site does not give any insurance company or government agency your information. See our <a href="/legal/privacy/">privacy policy</a>.</p></main></div>'),
        "legal/privacy/index.html":("Privacy Policy | CarInsuranceImmigrants.us","We collect minimal anonymous data and never share with insurance companies or government agencies including ICE.",
            f'<div class="page-container full-width"><main><h1 style="color:#1a3a5c;font-size:2rem;margin-bottom:16px">Privacy Policy</h1><p><em>Last updated: {LAST_REV}</em></p><h2>We Understand Your Privacy Concerns</h2><p>Reading this website does not give any insurance company, government agency, or ICE your personal information.</p><h2>What We Collect</h2><p>Only anonymous analytics (pages visited, browser type, approximate country). No names, addresses, immigration status, or identifying information.</p><h2>We Never Share With</h2><ul><li>Insurance companies</li><li>Government agencies</li><li>ICE or immigration enforcement</li><li>Any third party for commercial purposes</li></ul><h2>Cookies</h2><p>Minimal cookies for analytics and language preferences only. No advertising cookies.</p></main></div>'),
        "legal/terms/index.html":("Terms of Use | CarInsuranceImmigrants.us","Terms of use for this free car insurance information resource for immigrants.",
            f'<div class="page-container full-width"><main><h1 style="color:#1a3a5c;font-size:2rem;margin-bottom:16px">Terms of Use</h1><p><em>Last updated: {LAST_REV}</em></p><h2>Acceptance</h2><p>By using this site you agree to these terms.</p><h2>Permitted Use</h2><p>Personal non-commercial use. You may share links and quote brief passages with attribution.</p><h2>No Warranties</h2><p>Site provided as-is. Information may not be current. Verify before acting.</p></main></div>'),
        "contact/index.html":("Contact | CarInsuranceImmigrants.us","Contact us to report errors or give feedback. We are an information site, not an insurance company.",
            f'<div class="page-container full-width"><main><h1 style="color:#1a3a5c;font-size:2rem;margin-bottom:16px">Contact Us</h1><div class="info-box">We are an information website, not an insurance company. We cannot get you a quote or sell insurance.</div><h2>Report an Error</h2><p>Email <strong>info@carinsuranceimmigrants.us</strong> with the page URL and the correction.</p><h2>Need Insurance?</h2><p>Our <a href="/getting-insured/">getting insured guide</a> and <a href="/save-money/compare-quotes/">comparison guide</a> can help.</p></main></div>'),
    }
    for filename, (title, desc, body) in pages.items():
        slug_from_file = filename.replace("/index.html","")
        bc = f'<div class="breadcrumb-bar"><ol><li><a href="/">Home</a></li><li>{title.split("|")[0].strip()}</li></ol></div>'
        schema = json.dumps([{"@context":"https://schema.org","@type":"WebPage","name":title,"description":desc}], indent=2)
        html = TEMPLATE
        for k,v in {
            "{{META_TITLE}}":title,"{{META_DESCRIPTION}}":desc,
            "{{CANONICAL_URL}}":f"{SITE['domain']}/{slug_from_file}/",
            "{{LANG_CODE}}":"en","{{DIR}}":"ltr","{{OG_LOCALE}}":"en_US",
            "{{HREFLANG_TAGS}}":"","{{LANG_SWITCHER}}":"","{{LANG_PREFIX}}":"",
            "{{BREADCRUMB_HTML}}":bc,"{{PAGE_CONTENT}}":body,"{{SCHEMA_JSON}}":schema,
            "{{YEAR}}":str(YEAR),"{{LAST_REVIEWED}}":LAST_REV
        }.items():
            html = html.replace(k,v)
        write_file(OUTPUT_DIR/filename, html)
        add_sitemap(f"{SITE['domain']}/{slug_from_file}/","0.6")

def write_robots():
    write_file(OUTPUT_DIR/"robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE['domain']}/sitemap.xml\n")

def write_vercel():
    cfg = {"cleanUrls":True,"trailingSlash":True,
           "headers":[{"source":"/(.*)","headers":[{"key":"X-Content-Type-Options","value":"nosniff"},{"key":"Cache-Control","value":"public, max-age=86400, stale-while-revalidate=604800"}]}],
           "routes":[{"src":f"/{f}","dest":"/404"} for f in ["build\\.py","config\\.json","template\\.html","prompts\\.py","README\\.md"]]}
    write_file(OUTPUT_DIR/"vercel.json", json.dumps(cfg,indent=2))

# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--section", default="foundation")
    parser.add_argument("--lang", default="en")
    args = parser.parse_args()

    section = args.section
    target_langs = LANGUAGES if args.lang=="all" else [l for l in LANGUAGES if l["code"] in args.lang.split(",")]

    print(f"\n🚗 CarInsuranceImmigrants.us — [{section}] {[l['code'] for l in target_langs]}\n")
    total = 0
    errors = []

    if section in ("foundation","all"):
        print("📄 Static pages...")
        build_static_pages()
        write_robots()
        write_vercel()
        print("\n🏠 Homepages...")
        for lang in target_langs:
            try:
                prefix = lp(lang)
                path = OUTPUT_DIR/prefix/"index.html" if prefix else OUTPUT_DIR/"index.html"
                write_file(path, build_homepage(lang))
                add_sitemap(page_url("",lang),"1.0")
                total += 1
            except Exception as e:
                errors.append(f"Homepage [{lang['code']}]: {e}")
                print(f"  ❌ {e}")

    for pillar in PILLARS:
        if section not in ("all", pillar["id"]):
            continue
        print(f"\n📚 {pillar['title']}")
        for lang in target_langs:
            print(f"  [{lang['code']}]")
            for page in pillar["pages"]:
                print(f"    → {page['slug']}")
                try:
                    html = build_pillar_page(page, pillar, lang)
                    prefix = lp(lang)
                    path = OUTPUT_DIR/prefix/page["slug"]/"index.html" if prefix else OUTPUT_DIR/page["slug"]/"index.html"
                    write_file(path, html)
                    add_sitemap(page_url(page["slug"],lang), str(page.get("priority",0.8)))
                    total += 1
                    time.sleep(0.3)
                except Exception as e:
                    err = f"[{lang['code']}] {page['slug']}: {e}"
                    errors.append(err)
                    print(f"    ❌ {err}")
                    time.sleep(1)

    if section in ("states-top","states-all","all"):
        states = CONFIG["all_states"] if section in ("states-all","all") else CONFIG["top_states"]
        print(f"\n📍 States ({len(states)})...")
        for lang in target_langs:
            for state in states:
                print(f"  [{lang['code']}] {state}")
                try:
                    html, slug = build_state_page(state, lang)
                    prefix = lp(lang)
                    path = OUTPUT_DIR/prefix/slug/"index.html" if prefix else OUTPUT_DIR/slug/"index.html"
                    write_file(path, html)
                    add_sitemap(page_url(slug,lang),"0.8")
                    total += 1
                    time.sleep(0.3)
                except Exception as e:
                    errors.append(f"State [{lang['code']}] {state}: {e}")
                    print(f"  ❌ {e}")
                    time.sleep(1)

    write_sitemap()
    print(f"\n{'='*50}")
    print(f"✅ [{section}] — {total} pages, {len(errors)} errors")
    if errors:
        for e in errors: print(f"  • {e}")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    main()
