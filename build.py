#!/usr/bin/env python3
"""
CarInsuranceImmigrants.us — Master Site Builder
Writes HTML directly to repo root. Vercel serves it.

Usage:
  python3 build.py --section=foundation     # static pages + homepages
  python3 build.py --section=getting-insured
  python3 build.py --section=by-status
  python3 build.py --section=questions      # the burning questions pages
  python3 build.py --section=foreign-license
  python3 build.py --section=after-accident
  python3 build.py --section=coverage
  python3 build.py --section=insurers
  python3 build.py --section=license
  python3 build.py --section=states-top     # top 20 states
  python3 build.py --section=states-all     # all 50 states
  python3 build.py --section=save-money
  python3 build.py --section=community      # language-specific pages
  python3 build.py --section=all

  --lang=en (default) | es | zh | ar | pt | vi | tl | ko | ru | pl | all
"""

import os, json, re, time, datetime, argparse, anthropic, xml.etree.ElementTree as ET
from pathlib import Path
from prompts import (SYSTEM_PROMPT, pillar_page_prompt, state_page_prompt,
                     insurer_page_prompt, foreign_license_page_prompt,
                     question_page_prompt, homepage_prompt)

# ─── INIT ─────────────────────────────────────────────────────────────────────
client     = anthropic.Anthropic()
MODEL      = "claude-sonnet-4-6"
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

LOCALE_MAP = {
    "en": "en_US", "es": "es_US", "zh": "zh_CN",
    "ar": "ar_SA", "pt": "pt_BR", "vi": "vi_VN",
    "tl": "tl_PH", "ko": "ko_KR", "ru": "ru_RU", "pl": "pl_PL"
}

# Build page lookup for internal linking
ALL_PAGES = {}
for pillar in PILLARS:
    for page in pillar["pages"]:
        ALL_PAGES[page["slug"]] = {
            "title": page["title"],
            "icon":  pillar.get("icon", "📄"),
            "desc":  page.get("immigrant_angle", "")[:100]
        }

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
                    urls[loc.text] = {"priority": pri.text if pri is not None else "0.8", "changefreq": "monthly", "lastmod": datetime.date.today().isoformat()}
        except: pass
    return urls

sitemap_urls = load_sitemap()

def add_sitemap(url, priority="0.8"):
    sitemap_urls[url] = {"priority": priority, "changefreq": "monthly", "lastmod": datetime.date.today().isoformat()}

def write_sitemap():
    root = ET.Element("urlset")
    root.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    for loc, d in sorted(sitemap_urls.items()):
        u = ET.SubElement(root, "url")
        ET.SubElement(u, "loc").text        = loc
        ET.SubElement(u, "lastmod").text    = d["lastmod"]
        ET.SubElement(u, "changefreq").text = d["changefreq"]
        ET.SubElement(u, "priority").text   = d["priority"]
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
    raw = re.sub(r'^```(?:json)?\s*', '', raw, flags=re.MULTILINE)
    raw = re.sub(r'\s*```\s*$', '', raw, flags=re.MULTILINE)
    raw = raw.strip()
    s, e = raw.find('{'), raw.rfind('}')
    return raw[s:e+1] if s != -1 and e != -1 else raw

def call_claude(prompt: str, max_tokens=5000, retries=3) -> dict:
    messages = [{"role": "user", "content": prompt}]
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
            print("    WARNING JSON error attempt " + str(attempt+1) + ": " + str(e))
            if attempt < retries - 1:
                messages.append({"role": "assistant", "content": last_raw})
                messages.append({"role": "user", "content": "JSON error: " + str(e) + ". Return ONLY corrected JSON. Use <p> tags not newlines. Escape apostrophes. No trailing commas."})
                time.sleep(2)
            else: raise
        except Exception as e:
            print("    WARNING API error attempt " + str(attempt+1) + ": " + str(e))
            if attempt < retries - 1: time.sleep(5)
            else: raise

def build_hreflang(slug):
    return "\n  ".join(
        f'<link rel="alternate" hreflang="{l["hreflang"]}" href="{page_url(slug, l)}">'
        for l in LANGUAGES
    ) + f'\n  <link rel="alternate" hreflang="x-default" href="{page_url(slug, LANGUAGES[0])}">'

def build_lang_switcher(slug, current_lang):
    return "\n      ".join(
        f'<a href="{page_url(slug, l)}" class="{"active" if l["code"] == current_lang["code"] else ""}">{l["name"]}</a>'
        for l in LANGUAGES
    )

def build_breadcrumb(crumbs):
    li = "".join(f'<li><a href="{u}">{t}</a></li>' if u else f'<li>{t}</li>' for t, u in crumbs)
    schema = {"@context": "https://schema.org", "@type": "BreadcrumbList",
              "itemListElement": [{"@type": "ListItem", "position": i+1, "name": t, **({"item": u} if u else {})} for i, (t, u) in enumerate(crumbs)]}
    return f'<div class="breadcrumb-bar"><ol>{li}</ol></div>', schema

def build_sidebar(prefix):
    links = "".join(f'<li><a href="/{prefix}{p["slug"]}/">{p["icon"]} {p["title"]}</a></li>' for p in PILLARS)
    return f'''<aside class="sidebar">
  <div class="sidebar-card">
    <h3>Topics</h3>
    <ul class="practice-area-list">{links}</ul>
  </div>
  <div class="sidebar-card disclaimer-card">
    <h3>⚠️ Important</h3>
    <p>This information is for general educational purposes only. Insurance policies, rates, and state laws change frequently. Always verify current information directly with insurers and your state DMV.</p>
    <p style="margin-top:10px"><a href="/legal/disclaimer/" style="color:#b45309">Full disclaimer →</a></p>
  </div>
</aside>'''

def build_schema(slug, lang, meta_title, meta_desc, faq_pairs, howto_steps, bc_schema):
    schemas = [{
        "@context": "https://schema.org", "@type": "Article",
        "headline": meta_title, "description": meta_desc,
        "url": page_url(slug, lang), "inLanguage": lang["hreflang"],
        "dateModified": datetime.date.today().isoformat(),
        "datePublished": "2025-06-01",
        "author": {"@type": "Organization", "name": "CarInsuranceImmigrants.us Editorial Team"},
        "publisher": {"@type": "Organization", "name": "Car Insurance Immigrants", "url": SITE["domain"]}
    }]
    if faq_pairs:
        schemas.append({"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_pairs]})
    if howto_steps:
        schemas.append({"@context": "https://schema.org", "@type": "HowTo", "name": meta_title,
            "step": [{"@type": "HowToStep", "position": i+1, "name": s["name"], "text": s["text"]} for i, s in enumerate(howto_steps)]})
    schemas.append(bc_schema)
    return json.dumps(schemas, ensure_ascii=False, indent=2)

def assemble_html(meta_title, meta_desc, canonical, lang, slug, bc_html, page_content, schema_json):
    prefix = lp(lang)
    html = TEMPLATE
    for k, v in {
        "{{META_TITLE}}": meta_title, "{{META_DESCRIPTION}}": meta_desc,
        "{{CANONICAL_URL}}": canonical, "{{LANG_CODE}}": lang["code"],
        "{{DIR}}": lang["dir"], "{{OG_LOCALE}}": LOCALE_MAP.get(lang["code"], "en_US"),
        "{{HREFLANG_TAGS}}": build_hreflang(slug), "{{LANG_SWITCHER}}": build_lang_switcher(slug, lang),
        "{{LANG_PREFIX}}": prefix, "{{BREADCRUMB_HTML}}": bc_html,
        "{{PAGE_CONTENT}}": page_content, "{{SCHEMA_JSON}}": schema_json,
        "{{YEAR}}": str(YEAR), "{{LAST_REVIEWED}}": LAST_REV
    }.items():
        html = html.replace(k, v)
    return html

# ─── PAGE BUILDER ─────────────────────────────────────────────────────────────
def render_page(slug, content, lang, pillar, breadcrumbs, prompt_type="pillar"):
    prefix = lp(lang)
    bc_html, bc_schema = build_breadcrumb(breadcrumbs)
    faq_pairs = [(f["q"], f["a"]) for f in content.get("faq", [])]
    howto     = content.get("howto_steps") or []

    schema_json = build_schema(slug, lang, content["meta_title"],
                               content["meta_description"], faq_pairs,
                               howto if howto else None, bc_schema)

    # Data table
    table_html = ""
    dt = content.get("data_table")
    if dt and dt.get("headers") and dt.get("rows"):
        cap  = f"<caption style='caption-side:top;font-weight:700;padding:10px 16px;background:#f4f7fb;text-align:left'>{dt['caption']}</caption>" if dt.get("caption") else ""
        rows = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in dt["rows"])
        table_html = f'<div class="data-table-wrap"><table>{cap}<thead><tr>{"".join(f"<th>{h}</th>" for h in dt["headers"])}</tr></thead><tbody>{rows}</tbody></table></div>'

    # HowTo steps
    steps_html = ""
    if howto:
        lis = "".join(f'<li><div class="step-num">{i+1}</div><div class="step-content"><h4>{s["name"]}</h4><p>{s["text"]}</p></div></li>' for i, s in enumerate(howto))
        steps_html = f'<h2>Step-by-Step Guide</h2><ul class="steps-list">{lis}</ul>'

    # Sections
    sections_html = "".join(f'<h2>{s["h2"]}</h2>{s["body"]}' for s in content.get("sections", []))

    # Official sources
    sources_html = ""
    sources = content.get("official_sources", [])
    if sources:
        links = "".join(f'<li><a href="{s["url"]}" target="_blank" rel="noopener noreferrer">↗ {s["label"]}</a></li>' for s in sources if s.get("url") and s.get("label"))
        if links: sources_html = f'<div class="official-sources"><h3>📋 Official Sources</h3><ul>{links}</ul></div>'

    # FAQ
    faq_html = ""
    if faq_pairs:
        items = "".join(f'<div class="faq-item"><button class="faq-q">{q}<span class="chevron">▾</span></button><div class="faq-a"><p>{a}</p></div></div>' for q, a in faq_pairs)
        faq_html = f'<div class="faq-section"><h2>Frequently Asked Questions</h2>{items}</div>'

    # Warning / tip
    warning_html = f'<div class="warning-box"><strong>⚠️ Important:</strong> {content["warning"]}</div>' if content.get("warning") else ""
    info_html    = f'<div class="info-box">💡 {content["info_tip"]}</div>' if content.get("info_tip") else ""

    # Related
    related_html = ""
    related_slugs = []
    for p in PILLARS:
        for pg in p["pages"]:
            if pg["slug"] == slug:
                related_slugs = pg.get("related", [])
    if related_slugs:
        cards = []
        for rel in related_slugs[:5]:
            info = ALL_PAGES.get(rel, {})
            if info:
                cards.append(f'<a href="/{prefix}{rel}/" class="related-card"><div class="icon">{info["icon"]}</div><div class="title">{info["title"]}</div><div class="desc">{info["desc"]}</div></a>')
        if cards:
            related_html = f'<div class="related-section"><h2>Related Topics</h2><div class="related-grid">{"".join(cards)}</div></div>'

    # Pillar icon
    icon = next((p["icon"] for p in PILLARS for pg in p["pages"] if pg["slug"] == slug), "🚗")
    section_name = next((p["title"] for p in PILLARS for pg in p["pages"] if pg["slug"] == slug), "Car Insurance")

    page_content = f'''<div class="hero">
  <div style="max-width:1200px;margin:0 auto;text-align:center">
    <span class="last-reviewed">✅ Last reviewed: {LAST_REV}</span>
    <h1>{content["h1"]}</h1>
    <p class="subtitle">{content.get("intro_paragraph","")}</p>
    <div class="badges">
      <span class="badge">🇺🇸 All 50 States</span>
      <span class="badge">All Immigration Statuses</span>
      <span class="badge">{icon} {section_name}</span>
    </div>
  </div>
</div>
<div class="page-container">
  <main>
    <div class="definition-box"><strong>Quick Answer: </strong>{content["definition"]}</div>
    {warning_html}
    {info_html}
    {sections_html}
    {table_html}
    {steps_html}
    {sources_html}
    {faq_html}
    {related_html}
  </main>
  {build_sidebar(prefix)}
</div>'''

    return assemble_html(content["meta_title"], content["meta_description"],
                         page_url(slug, lang), lang, slug, bc_html, page_content, schema_json)


def build_pillar_page(page, pillar, lang):
    slug   = page["slug"]
    prefix = lp(lang)
    parts  = slug.split("/")

    crumbs = [("Home", f"/{prefix}" if prefix else "/")]
    if slug != pillar["slug"]:
        crumbs.append((pillar["title"], f"/{prefix}{pillar['slug']}/"))
    if len(parts) >= 3:
        inter_slug = "/".join(parts[:2])
        inter = ALL_PAGES.get(inter_slug, {})
        if inter:
            crumbs.append((inter["title"], f"/{prefix}{inter_slug}/"))
    crumbs.append((page["title"], None))

    # Use question prompt for questions pillar
    if pillar["id"] == "questions":
        prompt = question_page_prompt(page, lang)
    else:
        prompt = pillar_page_prompt(page, pillar, lang)

    content = call_claude(prompt)
    return render_page(slug, content, lang, pillar, crumbs)


def build_state_page(state, lang):
    slug    = f"states/{state.lower().replace(' ', '-')}"
    prefix  = lp(lang)
    crumbs  = [
        ("Home", f"/{prefix}" if prefix else "/"),
        ("By State", f"/{prefix}states/"),
        (f"{state}", None)
    ]
    content = call_claude(state_page_prompt(state, lang))
    states_pillar = next(p for p in PILLARS if p["id"] == "states")
    return render_page(slug, content, lang, states_pillar, crumbs), slug


def build_insurer_page(insurer, lang):
    slug    = f"insurers/{insurer['slug']}"
    prefix  = lp(lang)
    crumbs  = [
        ("Home", f"/{prefix}" if prefix else "/"),
        ("Insurance Companies", f"/{prefix}insurers/"),
        (insurer["name"], None)
    ]
    content = call_claude(insurer_page_prompt(insurer, lang))
    ins_pillar = next(p for p in PILLARS if p["id"] == "insurers")
    return render_page(slug, content, lang, ins_pillar, crumbs), slug


def build_foreign_license_page(license_info, lang):
    slug    = f"foreign-license/{license_info['slug']}"
    prefix  = lp(lang)
    crumbs  = [
        ("Home", f"/{prefix}" if prefix else "/"),
        ("Foreign License Insurance", f"/{prefix}foreign-license/"),
        (f"{license_info['country']} License", None)
    ]
    content = call_claude(foreign_license_page_prompt(license_info, lang))
    fl_pillar = next(p for p in PILLARS if p["id"] == "foreign-license")
    return render_page(slug, content, lang, fl_pillar, crumbs), slug


def build_homepage(lang):
    prefix  = lp(lang)
    content = call_claude(homepage_prompt(lang), max_tokens=800)

    lang_btns = "".join(
        f'<a href="/{l["prefix"]}/" class="lang-btn">{l["name"]}</a>' if l["prefix"]
        else '<a href="/" class="lang-btn">English</a>'
        for l in LANGUAGES
    )

    cards = "".join(f'''<a href="/{prefix}{p['slug']}/" class="hub-card">
  <div class="card-icon">{p["icon"]}</div>
  <h3>{p["title"]}</h3>
  <p>{p["description"]}</p>
</a>''' for p in PILLARS)

    top_questions = [
        ("questions/can-undocumented-get-car-insurance", "Can I get insurance if I'm undocumented?"),
        ("questions/will-insurance-company-call-ice",    "Will they call ICE?"),
        ("questions/what-is-itin-car-insurance",         "Can I use ITIN instead of SSN?"),
        ("questions/mexican-license-texas",              "Can I use my foreign license?"),
        ("getting-insured/same-day",                     "Can I get insured same day?"),
    ]
    q_links = "".join(f'<a href="/{prefix}{s}/" style="display:block;color:#f59e0b;margin-bottom:8px;font-size:0.95rem">→ {t}</a>' for s, t in top_questions)

    schema = json.dumps([
        {"@context": "https://schema.org", "@type": "Organization", "name": "Car Insurance Immigrants", "url": SITE["domain"], "description": SITE["description"]},
        {"@context": "https://schema.org", "@type": "WebSite", "name": "Car Insurance Immigrants", "url": SITE["domain"]}
    ], ensure_ascii=False, indent=2)

    page_content = f'''<div class="home-hero">
  <div style="max-width:900px;margin:0 auto">
    <h1>{content.get("hero_headline", "Car Insurance for Immigrants — Every Question Answered")}</h1>
    <p>{content.get("hero_subtext", "Free car insurance information for immigrants in all 50 states. No SSN required to read.")}</p>
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
      <strong style="color:#c0392b;font-size:1.05rem">{content.get("urgent_question", "Common Questions We Answer")}</strong>
      <div style="margin-top:8px">{q_links}</div>
    </div>
  </div>

  <h2 style="font-size:1.8rem;color:#1a3a5c;margin-bottom:8px;border:none">Everything You Need to Know</h2>
  <p style="color:#5a6a7a;margin-bottom:24px">Car insurance answers for immigrants — the questions others won't answer, in your language.</p>
  <div class="hub-grid">{cards}</div>

  <div style="background:#eef4ff;border-radius:12px;padding:32px;margin:40px 0">
    <h2 style="border:none;margin-top:0;color:#1a3a5c">About This Site</h2>
    <p>{content.get("about_blurb", "CarInsuranceImmigrants.us provides free car insurance information for immigrants across the United States.")}</p>
    <p style="margin-top:12px">
      <a href="/about/">About us</a> &nbsp;·&nbsp;
      <a href="/legal/disclaimer/">Disclaimer</a> &nbsp;·&nbsp;
      <a href="/states/">All 50 states</a> &nbsp;·&nbsp;
      <a href="/insurers/">Insurance companies</a>
    </p>
  </div>
</div>'''

    html = TEMPLATE
    for k, v in {
        "{{META_TITLE}}": "Car Insurance for Immigrants in the US | CarInsuranceImmigrants.us",
        "{{META_DESCRIPTION}}": "Free car insurance information for immigrants. No SSN? Foreign license? Undocumented? We answer every question in 10 languages.",
        "{{CANONICAL_URL}}": page_url("", lang),
        "{{LANG_CODE}}": lang["code"], "{{DIR}}": lang["dir"],
        "{{OG_LOCALE}}": LOCALE_MAP.get(lang["code"], "en_US"),
        "{{HREFLANG_TAGS}}": build_hreflang(""),
        "{{LANG_SWITCHER}}": build_lang_switcher("", lang),
        "{{LANG_PREFIX}}": prefix, "{{BREADCRUMB_HTML}}": "",
        "{{PAGE_CONTENT}}": page_content, "{{SCHEMA_JSON}}": schema,
        "{{YEAR}}": str(YEAR), "{{LAST_REVIEWED}}": LAST_REV
    }.items():
        html = html.replace(k, v)
    return html


def build_static_pages():
    pages = {
        "about/index.html": ("About CarInsuranceImmigrants.us",
            "We provide free car insurance information for immigrants in the US — no SSN required to read. Every question answered in 10 languages.",
            f'''<div class="page-container full-width"><main>
<span class="last-reviewed">✅ Last reviewed: {LAST_REV}</span>
<h1 style="color:#1a3a5c;font-size:2rem;margin:16px 0">About CarInsuranceImmigrants.us</h1>
<p>CarInsuranceImmigrants.us is the most comprehensive car insurance information resource for immigrants in the United States. We answer the questions that mainstream insurance sites ignore — can you get insurance without an SSN, will they call ICE, what happens if you have a foreign license.</p>
<h2>Our Mission</h2>
<p>Over 53 million immigrants live in the United States. Most need car insurance. Many are afraid to ask basic questions because they fear consequences for their immigration status. We exist to give them honest, accurate answers — in their language.</p>
<h2>What We Cover</h2>
<p>Getting insured without SSN · Insurance by immigration status · The burning questions immigrants are afraid to ask · Foreign license insurance by country · After-accident guidance · Coverage explained · Insurance companies compared · All 50 states · How to save money</p>
<h2>Our Editorial Standards</h2>
<p>All content is researched against official sources: NAIC.org, state DMV websites, IRS.gov, and state insurance commissioner data. We cite real sources. We never invent rates or insurer policies. When something varies by state — we say so.</p>
<h2>Important Notice</h2>
<p>CarInsuranceImmigrants.us is an information resource only. We are not an insurance company or broker. We do not sell insurance. Always verify current information directly with insurers and your state DMV before making decisions.</p>
</main></div>'''),

        "legal/disclaimer/index.html": ("Disclaimer | CarInsuranceImmigrants.us",
            "Important disclaimer: CarInsuranceImmigrants.us provides general information only. Insurance rates, policies, and state laws change frequently.",
            f'''<div class="page-container full-width"><main>
<div class="warning-box"><strong>Please read this before using this website.</strong></div>
<h1 style="color:#1a3a5c;font-size:2rem;margin:16px 0">Disclaimer</h1>
<h2>General Information Only</h2>
<p>CarInsuranceImmigrants.us provides general educational information about car insurance for immigrants. This is not insurance advice, and we are not an insurance company, broker, or agent.</p>
<h2>Information Changes Frequently</h2>
<p>Insurance rates, insurer policies, state laws, and license requirements change frequently. Always verify current information directly with insurance companies and your state DMV before making any decision.</p>
<h2>No Guarantee of Accuracy</h2>
<p>While we work hard to keep information accurate and current, we cannot guarantee that all information is up to date. Do not make insurance decisions based solely on this website.</p>
<h2>We Are Not Affiliated With Any Insurer</h2>
<p>CarInsuranceImmigrants.us is an independent information resource. We are not affiliated with, endorsed by, or paid by any insurance company. Any affiliate relationships are disclosed.</p>
<h2>Privacy</h2>
<p>Reading this website does not give any insurance company or government agency your information. We take your privacy seriously. See our <a href="/legal/privacy/">privacy policy</a>.</p>
</main></div>'''),

        "legal/privacy/index.html": ("Privacy Policy | CarInsuranceImmigrants.us",
            "Our privacy policy — we collect minimal anonymous data and never share information with insurance companies or government agencies.",
            f'''<div class="page-container full-width"><main>
<h1 style="color:#1a3a5c;font-size:2rem;margin-bottom:16px">Privacy Policy</h1>
<p><em>Last updated: {LAST_REV}</em></p>
<h2>We Understand Your Privacy Concerns</h2>
<p>Many visitors to this site have concerns about their immigration status. We want to be completely clear: reading this website does not give any insurance company, government agency, or ICE your personal information.</p>
<h2>What We Collect</h2>
<p>We collect only anonymous analytics (pages visited, browser type, approximate country — never personal details). We do not collect names, addresses, immigration status, or any identifying information unless you voluntarily email us.</p>
<h2>We Never Share With:</h2>
<ul><li>Insurance companies</li><li>Government agencies</li><li>ICE or immigration enforcement</li><li>Any third party for commercial purposes</li></ul>
<h2>Cookies</h2>
<p>We use minimal cookies for analytics and language preferences only. No advertising cookies.</p>
</main></div>'''),

        "legal/terms/index.html": ("Terms of Use | CarInsuranceImmigrants.us",
            "Terms of use for CarInsuranceImmigrants.us — a free car insurance information resource for immigrants.",
            f'''<div class="page-container full-width"><main>
<h1 style="color:#1a3a5c;font-size:2rem;margin-bottom:16px">Terms of Use</h1>
<p><em>Last updated: {LAST_REV}</em></p>
<h2>Acceptance</h2><p>By using CarInsuranceImmigrants.us you agree to these terms.</p>
<h2>Permitted Use</h2><p>Personal, non-commercial use. You may share links and quote brief passages with attribution.</p>
<h2>Prohibited</h2><p>Scraping, bulk reproduction, or republishing content without permission. Using the site for unlawful purposes.</p>
<h2>No Warranties</h2><p>Site provided as-is. Information may not be current. Verify all information before acting.</p>
</main></div>'''),

        "contact/index.html": ("Contact | CarInsuranceImmigrants.us",
            "Contact CarInsuranceImmigrants.us — report errors, ask content questions, or give feedback.",
            f'''<div class="page-container full-width"><main>
<h1 style="color:#1a3a5c;font-size:2rem;margin-bottom:16px">Contact Us</h1>
<div class="info-box">💡 We are an information website, not an insurance company. We cannot get you a quote or sell you insurance.</div>
<h2>Report an Error</h2>
<p>If you find outdated or incorrect information, please email <strong>info@carinsuranceimmigrants.us</strong> with the page URL and the correction. We update quickly.</p>
<h2>Content Questions</h2>
<p>For questions about content or suggestions for topics to cover, email info@carinsuranceimmigrants.us.</p>
<h2>Need Insurance?</h2>
<p>We don't sell insurance but our <a href="/insurers/">insurance company guides</a> and <a href="/save-money/compare-quotes/">comparison guide</a> can help you find the right insurer.</p>
</main></div>'''),
    }

    for filename, (title, desc, body) in pages.items():
        slug_from_file = filename.replace("/index.html", "")
        bc = f'<div class="breadcrumb-bar"><ol><li><a href="/">Home</a></li><li>{title.split("|")[0].strip()}</li></ol></div>'
        schema = json.dumps([{"@context": "https://schema.org", "@type": "WebPage", "name": title, "description": desc, "url": f"{SITE['domain']}/{slug_from_file}/"}], indent=2)
        html = TEMPLATE
        for k, v in {
            "{{META_TITLE}}": title, "{{META_DESCRIPTION}}": desc,
            "{{CANONICAL_URL}}": f"{SITE['domain']}/{slug_from_file}/",
            "{{LANG_CODE}}": "en", "{{DIR}}": "ltr", "{{OG_LOCALE}}": "en_US",
            "{{HREFLANG_TAGS}}": "", "{{LANG_SWITCHER}}": "", "{{LANG_PREFIX}}": "",
            "{{BREADCRUMB_HTML}}": bc, "{{PAGE_CONTENT}}": body,
            "{{SCHEMA_JSON}}": schema, "{{YEAR}}": str(YEAR), "{{LAST_REVIEWED}}": LAST_REV
        }.items():
            html = html.replace(k, v)
        write_file(OUTPUT_DIR / filename, html)
        add_sitemap(f"{SITE['domain']}/{slug_from_file}/", "0.6")


def write_robots():
    write_file(OUTPUT_DIR / "robots.txt", f"User-agent: *\nAllow: /\nSitemap: {SITE['domain']}/sitemap.xml\n")

def write_vercel():
    cfg = {"cleanUrls": True, "trailingSlash": True,
           "headers": [{"source": "/(.*)", "headers": [
               {"key": "X-Content-Type-Options", "value": "nosniff"},
               {"key": "Cache-Control", "value": "public, max-age=86400, stale-while-revalidate=604800"}
           ]}],
           "routes": [{"src": f"/{f}", "dest": "/404"} for f in ["build\\.py", "config\\.json", "template\\.html", "prompts\\.py", "README\\.md"]]}
    write_file(OUTPUT_DIR / "vercel.json", json.dumps(cfg, indent=2))

# ─── MAIN ─────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--section", default="foundation")
    parser.add_argument("--lang", default="en")
    args = parser.parse_args()

    section = args.section
    target_langs = LANGUAGES if args.lang == "all" else [l for l in LANGUAGES if l["code"] in args.lang.split(",")]

    print(f"\n🚗 CarInsuranceImmigrants.us — [{section}] [{[l['code'] for l in target_langs]}]\n")

    total = 0
    errors = []

    # Foundation
    if section in ("foundation", "all"):
        print("📄 Static pages...")
        build_static_pages()
        write_robots()
        write_vercel()
        print("\n🏠 Homepages...")
        for lang in target_langs:
            try:
                prefix = lp(lang)
                path = OUTPUT_DIR / prefix / "index.html" if prefix else OUTPUT_DIR / "index.html"
                write_file(path, build_homepage(lang))
                add_sitemap(page_url("", lang), "1.0")
                total += 1
            except Exception as e:
                errors.append(f"Homepage [{lang['code']}]: {e}")
                print(f"  ❌ {e}")

    # Pillar pages
    SECTION_TO_PILLAR = {p["id"]: p["id"] for p in PILLARS}
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
                    path = OUTPUT_DIR / prefix / page["slug"] / "index.html" if prefix else OUTPUT_DIR / page["slug"] / "index.html"
                    write_file(path, html)
                    add_sitemap(page_url(page["slug"], lang), str(page.get("priority", 0.8)))
                    total += 1
                    time.sleep(0.5)
                except Exception as e:
                    err = f"[{lang['code']}] {page['slug']}: {e}"
                    errors.append(err)
                    print(f"    ❌ {err}")
                    time.sleep(1)

    # State pages
    if section in ("states-top", "states-all", "all"):
        states = CONFIG["all_states"] if section in ("states-all", "all") else CONFIG["top_states"]
        print(f"\n📍 State pages ({len(states)} states)...")
        for lang in target_langs:
            for state in states:
                print(f"  [{lang['code']}] {state}")
                try:
                    html, slug = build_state_page(state, lang)
                    prefix = lp(lang)
                    path = OUTPUT_DIR / prefix / slug / "index.html" if prefix else OUTPUT_DIR / slug / "index.html"
                    write_file(path, html)
                    add_sitemap(page_url(slug, lang), "0.8")
                    total += 1
                    time.sleep(0.5)
                except Exception as e:
                    errors.append(f"State [{lang['code']}] {state}: {e}")
                    print(f"  ❌ {e}")
                    time.sleep(1)

    # Foreign license pages
    if section in ("foreign-license-countries", "all"):
        print(f"\n🪪 Foreign license country pages...")
        for lang in target_langs:
            for lic in CONFIG["foreign_licenses"]:
                print(f"  [{lang['code']}] {lic['country']}")
                try:
                    html, slug = build_foreign_license_page(lic, lang)
                    prefix = lp(lang)
                    path = OUTPUT_DIR / prefix / slug / "index.html" if prefix else OUTPUT_DIR / slug / "index.html"
                    write_file(path, html)
                    add_sitemap(page_url(slug, lang), "0.9")
                    total += 1
                    time.sleep(0.5)
                except Exception as e:
                    errors.append(f"License [{lang['code']}] {lic['country']}: {e}")
                    print(f"  ❌ {e}")
                    time.sleep(1)

    # Insurer detail pages
    if section in ("insurer-pages", "all"):
        print(f"\n🏢 Insurer pages...")
        for lang in target_langs:
            for ins in CONFIG["insurers"]:
                print(f"  [{lang['code']}] {ins['name']}")
                try:
                    html, slug = build_insurer_page(ins, lang)
                    prefix = lp(lang)
                    path = OUTPUT_DIR / prefix / slug / "index.html" if prefix else OUTPUT_DIR / slug / "index.html"
                    write_file(path, html)
                    add_sitemap(page_url(slug, lang), "0.9")
                    total += 1
                    time.sleep(0.5)
                except Exception as e:
                    errors.append(f"Insurer [{lang['code']}] {ins['name']}: {e}")
                    print(f"  ❌ {e}")
                    time.sleep(1)

    write_sitemap()

    print(f"\n{'='*60}")
    print(f"✅ [{section}] done — {total} pages built, {len(errors)} errors")
    if errors:
        for e in errors: print(f"  • {e}")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
