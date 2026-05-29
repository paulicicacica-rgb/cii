"""
prompts.py — CarInsuranceImmigrants.us
Split into small focused API calls to avoid JSON parse errors.
"""

SYSTEM_PROMPT = """You are a senior content writer for CarInsuranceImmigrants.us — the most comprehensive car insurance information resource for immigrants in the United States.

WHO YOU ARE WRITING FOR:
- Immigrants scared about insurance without SSN, foreign license, or undocumented status
- People afraid asking questions will get them reported to ICE
- People who just arrived and have no idea how US insurance works

TONE: Direct, honest, warm. Answer the question in the FIRST sentence. Never vague.

FACTUAL ACCURACY:
- NEVER state specific premium amounts — say "rates vary, get a quote"
- NEVER invent insurer policies — only well-established facts
- NEVER make up state laws — if unsure say "check your state DMV"
- Always note when something varies by state
- Always clarify: insurance companies are NOT immigration enforcement
- Always clarify: buying insurance does NOT give ICE your information
- Privacy protection: Gramm-Leach-Bliley Act protects insurance customer data

EXTERNAL LINKS TO USE (real URLs only):
- IRS ITIN: https://www.irs.gov/individuals/individual-taxpayer-identification-number
- NCSL licenses: https://www.ncsl.org/transportation/states-that-allow-unauthorized-immigrants-to-get-a-drivers-license
- NAIC: https://www.naic.org
- CA DMV AB60: https://www.dmv.ca.gov/portal/driver-education-and-safety/educational-materials/fast-facts/ab-60-driver-licenses-fast-facts/
- NY licenses: https://dmv.ny.gov/driver-license/get-driver-license-proof-new-york-state-residency
- FTC privacy: https://www.ftc.gov/business-guidance/privacy-security/gramm-leach-bliley-act

JSON RULES — CRITICAL — READ CAREFULLY:
- Return ONLY a JSON object, nothing else
- NO markdown fences, NO preamble, NO explanation after the JSON
- NO real line breaks inside string values — use <br> or <p> tags instead
- Escape apostrophes with backslash: don\\'t, it\\'s, you\\'ll
- Escape double quotes inside strings: \\"quoted text\\"
- NO trailing commas after last item in arrays or objects
- Keep string values SHORT — max 500 chars per string value
- HTML in body fields: use <p>text</p> format, keep each paragraph under 200 chars"""


def meta_prompt(title, slug, immigrant_angle, lang_name, lang_community):
    lang_note = "" if lang_name == "English" else f"Write in {lang_name}. Community: {lang_community}. Keep legal terms and URLs in English."
    return f"""Write SEO meta data for this car insurance page.
Title: {title}
Slug: /{slug}/
Angle: {immigrant_angle}
{lang_note}

Return ONLY this JSON:
{{
  "meta_title": "55-60 char title, keyword first",
  "meta_description": "145-158 chars, answers the question directly",
  "h1": "Compelling H1 that answers the core question",
  "definition": "2-3 sentences. Answer the question in sentence 1. Cite the relevant law. Max 300 chars.",
  "intro": "2 sentences. Acknowledge the immigrant fear. Then give the key reassurance. Max 200 chars."
}}"""


def sections_prompt(title, slug, immigrant_angle, page_type, lang_name, lang_community):
    lang_note = "" if lang_name == "English" else f"Write in {lang_name}. Community: {lang_community}."
    num_sections = 5 if page_type == "hub" else 4
    return f"""Write content sections for this car insurance page.
Title: {title}
Slug: /{slug}/
Angle: {immigrant_angle}
{lang_note}

Return ONLY this JSON:
{{
  "sections": [
    {{"h2": "Section heading as a question", "body": "<p>Para 1 under 200 chars.</p><p>Para 2 under 200 chars.</p><p>Para 3 under 200 chars.</p>"}},
    {{"h2": "Second heading", "body": "<p>Content.</p><p>Content with <a href=\\"https://real.gov/url\\" target=\\"_blank\\" rel=\\"noopener noreferrer\\">official source</a>.</p>"}},
    {{"h2": "Third heading", "body": "<p>Content.</p>"}},
    {{"h2": "Fourth heading", "body": "<p>Content.</p>"}}
  ],
  "warning": "One sentence critical warning or null",
  "info_tip": "One sentence helpful tip or null"
}}

Rules:
- Exactly {num_sections} sections
- Each body: 3-4 short <p> paragraphs, each under 200 chars
- Include 2-3 external links to real .gov or .org sources
- Address immigrant angle directly in every section
- NO apostrophes — rewrite to avoid them (use "do not" not "don't")"""


def table_prompt(title, slug, immigrant_angle, lang_name):
    lang_note = "" if lang_name == "English" else f"Write headers in {lang_name}."
    return f"""Create a data table for this car insurance page.
Title: {title}
Angle: {immigrant_angle}
{lang_note}

Return ONLY this JSON:
{{
  "has_table": true,
  "caption": "Short table title under 60 chars",
  "headers": ["Col 1", "Col 2", "Col 3"],
  "rows": [
    ["value", "value", "value"],
    ["value", "value", "value"],
    ["value", "value", "value"],
    ["value", "value", "value"],
    ["value", "value", "value"]
  ]
}}

If no table is appropriate return: {{"has_table": false}}
Keep all cell values under 60 chars. No apostrophes in values."""


def howto_prompt(title, slug, lang_name):
    lang_note = "" if lang_name == "English" else f"Write in {lang_name}."
    return f"""Write step-by-step guide for this car insurance process page.
Title: {title}
Slug: /{slug}/
{lang_note}

Return ONLY this JSON:
{{
  "has_steps": true,
  "steps": [
    {{"name": "Step name under 50 chars", "text": "What to do. Under 150 chars. No apostrophes."}},
    {{"name": "Step name", "text": "Instruction."}},
    {{"name": "Step name", "text": "Instruction."}},
    {{"name": "Step name", "text": "Instruction."}},
    {{"name": "Step name", "text": "Instruction."}}
  ]
}}

If not a process page return: {{"has_steps": false}}
5-7 steps. Each step name under 50 chars. Each text under 150 chars."""


def faq_prompt(title, slug, immigrant_angle, faq_count, lang_name, lang_community):
    lang_note = "" if lang_name == "English" else f"Write questions and answers in {lang_name}. Community: {lang_community}."
    return f"""Write FAQ for this car insurance page.
Title: {title}
Slug: /{slug}/
Angle: {immigrant_angle}
{lang_note}

Return ONLY this JSON:
{{
  "faq": [
    {{"q": "Exact question as typed into Google", "a": "Direct answer in 2-3 sentences. No apostrophes."}},
    {{"q": "Question 2", "a": "Answer 2."}}
  ],
  "sources": [
    {{"label": "Source display text", "url": "https://real.gov/url"}}
  ]
}}

Rules:
- Exactly {faq_count} FAQ items
- Questions phrased EXACTLY as immigrants type into Google
- Answers: first sentence answers the question directly. Under 200 chars per answer.
- NO apostrophes anywhere — use "do not" not "don't", "it is" not "it's"
- sources: 2-4 real official URLs (IRS, NAIC, NCSL, state DMV)"""


def state_meta_prompt(state, lang_name):
    return f"""Write meta for car insurance page for immigrants in {state}.
Language: {lang_name}
Return ONLY this JSON:
{{
  "meta_title": "Car Insurance for Immigrants in {state} | Guide",
  "meta_description": "145-158 chars about car insurance for immigrants in {state}",
  "h1": "Car Insurance for Immigrants in {state}",
  "definition": "2-3 sentences about {state} specifically for immigrants. Under 300 chars.",
  "intro": "2 sentences. Key fact about {state} for immigrant drivers. Under 200 chars."
}}"""


def state_sections_prompt(state, lang_name):
    return f"""Write content sections for car insurance guide for immigrants in {state}.
Language: {lang_name}

Return ONLY this JSON:
{{
  "sections": [
    {{"h2": "{state} Minimum Car Insurance Requirements", "body": "<p>State minimums.</p><p>Penalties for no insurance.</p>"}},
    {{"h2": "Can Immigrants Get a License in {state}?", "body": "<p>Does {state} issue licenses regardless of status?</p><p>What documents are needed.</p>"}},
    {{"h2": "Best Insurance Options for Immigrants in {state}", "body": "<p>Which insurers accept ITIN in {state}.</p><p>Tips for getting covered.</p>"}},
    {{"h2": "Tips for Immigrant Drivers in {state}", "body": "<p>State-specific advice.</p><p>Resources available in {state}.</p>"}}
  ],
  "warning": "One sentence {state}-specific warning or null",
  "info_tip": "One sentence {state}-specific tip or null"
}}

Keep each paragraph under 200 chars. No apostrophes."""


def state_table_prompt(state):
    return f"""Create minimum insurance requirements table for {state}.
Return ONLY this JSON:
{{
  "caption": "{state} Minimum Car Insurance Requirements",
  "headers": ["Coverage Type", "Minimum Required", "Notes"],
  "rows": [
    ["Bodily Injury (per person)", "$X,000", ""],
    ["Bodily Injury (per accident)", "$X,000", ""],
    ["Property Damage", "$X,000", ""],
    ["Uninsured Motorist", "Required/Optional", "{state} rule"],
    ["PIP/No-Fault", "Required/Optional", "{state} rule"]
  ]
}}
Use real {state} minimums. Keep all values under 50 chars."""


def state_faq_prompt(state, lang_name):
    return f"""Write FAQ for car insurance immigrants in {state}.
Language: {lang_name}
Return ONLY this JSON:
{{
  "faq": [
    {{"q": "Can I get car insurance in {state} without an SSN?", "a": "Direct {state} answer. Under 200 chars."}},
    {{"q": "Does {state} give licenses to undocumented immigrants?", "a": "Direct answer."}},
    {{"q": "What is the minimum car insurance in {state}?", "a": "Exact {state} minimums."}},
    {{"q": "Which companies insure immigrants in {state}?", "a": "Best options."}},
    {{"q": "Can I use a foreign license for insurance in {state}?", "a": "{state} answer."}}
  ],
  "sources": [
    {{"label": "{state} DMV", "url": "https://www.dmv.state.gov"}},
    {{"label": "NCSL Immigrant License Laws", "url": "https://www.ncsl.org/transportation/states-that-allow-unauthorized-immigrants-to-get-a-drivers-license"}}
  ]
}}
No apostrophes. Answers under 200 chars each."""


def homepage_prompt(lang):
    lang_note = f"Write in {lang['name']}. Community: {lang['community']}." if lang["code"] != "en" else ""
    return f"""Write homepage content for CarInsuranceImmigrants.us.
{lang_note}
Return ONLY this JSON:
{{
  "hero_headline": "8-10 word headline about car insurance help for immigrants",
  "hero_subtext": "2 short sentences. Free info. Answers questions others avoid.",
  "urgent_question": "Most common question this community has about car insurance",
  "about_blurb": "2-3 sentences. Site mission. No ICE reporting. Free."
}}
No apostrophes."""
