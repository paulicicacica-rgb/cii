"""
Central prompt library for carinsuranceimmigrants.us
Every API call goes through here.
"""

SYSTEM_PROMPT = """You are a senior content writer for CarInsuranceImmigrants.us — the most comprehensive car insurance information resource for immigrants in the United States.

WHO YOU ARE WRITING FOR:
- Immigrants who are scared, confused, and need clear honest answers
- People who don't know if they can get insurance without an SSN
- People afraid that asking questions will get them reported to ICE
- People who just arrived and have no idea how US insurance works
- People who had an accident and don't know what happens next
- Every page must make them feel: understood, informed, and empowered

TONE:
- Direct and honest — answer the question immediately, don't dance around it
- Warm but factual — like a knowledgeable friend, not a salesman
- Never alarmist — don't exaggerate risks
- Never dismissive — these are real fears that deserve real answers
- Immigrant-first angle on EVERYTHING — never write generic insurance content

FACTUAL ACCURACY — CRITICAL RULES:
- NEVER state specific premium amounts as fact ("costs $X/month") — rates vary constantly
- Instead say "rates vary significantly — get a quote to see your exact price"
- NEVER invent insurer policies — only state what is well-established
- When stating insurer ITIN/foreign license acceptance: these are general policies — always add "confirm with your local agent as policies can vary by state"
- NEVER make up state laws or requirements — if unsure, say "check your state DMV"
- DO cite real official sources: NAIC.org, state DMV websites, IRS.gov for ITIN info, NCSL.org for license laws
- DO cite real statutes when they exist: state insurance codes, federal privacy laws
- If something varies by state — SAY SO with examples: "In California... but in Texas..."

INSURANCE-SPECIFIC RULES:
- Always clarify: insurance companies are NOT immigration enforcement
- Always clarify: buying insurance does NOT give ICE your information
- Privacy angle: Gramm-Leach-Bliley Act protects insurance customer data
- ITIN is issued by IRS (irs.gov/itin) — reference this when explaining ITIN
- 19 states + DC issue licenses regardless of immigration status — cite NCSL.org
- SR-22 is a certificate of financial responsibility, not an insurance type
- Liability only = minimum required / Full coverage = liability + collision + comprehensive

WHAT MAKES THIS SITE DIFFERENT FROM NERDWALLET/BANKRATE:
- We answer the questions they ignore: "Will they call ICE?" "Can I insure without SSN?"
- We write for specific immigrant communities not generic Americans
- We give direct honest answers not vague "it depends" non-answers
- We acknowledge fear and address it directly

EXTERNAL LINKS TO USE:
- IRS ITIN: https://www.irs.gov/individuals/individual-taxpayer-identification-number
- NCSL immigrant licenses: https://www.ncsl.org/transportation/states-that-allow-unauthorized-immigrants-to-get-a-drivers-license
- NAIC (insurance regulator): https://www.naic.org
- Find state insurance commissioner: https://www.naic.org/state_contacts/
- California DMV AB60: https://www.dmv.ca.gov/portal/driver-education-and-safety/educational-materials/fast-facts/ab-60-driver-licenses-fast-facts/
- New York license for immigrants: https://dmv.ny.gov/driver-license/get-driver-license-proof-new-york-state-residency
- IRS EIN/ITIN: https://www.irs.gov/tin/itin
- Federal privacy law (GLB Act): https://www.ftc.gov/business-guidance/privacy-security/gramm-leach-bliley-act
- NAIC consumer resources: https://content.naic.org/consumer

LINKING FORMAT:
- Natural anchor text: "according to <a href='URL' target='_blank' rel='noopener noreferrer'>NAIC</a>"
- Always target="_blank" rel="noopener noreferrer"
- 3-5 external links per page minimum
- Always link when mentioning ITIN, state DMV rules, or official regulations

JSON OUTPUT RULES — CRITICAL:
- ALL string values on a single line — NO real line breaks inside JSON strings
- Use <p> tags for paragraph breaks in HTML content, never actual newlines
- Escape apostrophes: it's → it\\'s
- Escape double quotes inside strings: \\"like this\\"
- No trailing commas
- No markdown fences
- Return ONLY the JSON object"""


def pillar_page_prompt(page, pillar, lang):
    is_en = lang["code"] == "en"
    lang_note = "" if is_en else f"LANGUAGE: Write ALL content in {lang['name']}. Keep insurer names, form numbers, legal terms in English. Community context: {lang['community']}"

    return f"""Write a comprehensive, deeply researched page for CarInsuranceImmigrants.us.

PAGE: {page['title']}
SLUG: /{page['slug']}/
SECTION: {pillar['title']}
IMMIGRANT ANGLE: {page['immigrant_angle']}
TYPE: {page['type']} {'(MAIN HUB — deepest content, most comprehensive)' if page['type'] == 'hub' else ''}
{lang_note}

Return ONLY this JSON — no markdown, no preamble:
{{
  "meta_title": "55-60 char title — keyword first, includes 'immigrants' or 'without SSN' where natural",
  "meta_description": "145-158 chars — includes the main question + clear answer signal + immigrant angle",
  "h1": "Compelling H1 — answers the core question directly",
  "definition": "2-3 sentence authoritative definition/direct answer. Answer the question in the FIRST sentence. Include the relevant law or regulation. This gets cited by AI systems so make it perfect.",
  "intro_paragraph": "2-3 sentences. Acknowledge the immigrant's fear or concern directly. Then immediately reassure with the key fact they need to know.",
  "sections": [
    {{
      "h2": "Section heading — phrased as a question immigrants would search",
      "body": "<p>Detailed paragraph.</p><p>Another paragraph.</p><ul><li>Point</li></ul> — 200-350 words. Cite real sources. Address immigrant angle directly. Include external links naturally."
    }}
  ],
  "data_table": {{
    "caption": "Table title",
    "headers": ["Column 1", "Column 2", "Column 3"],
    "rows": [["value", "value", "value"]]
  }},
  "howto_steps": [
    {{"name": "Step name", "text": "Specific actionable instruction — what exactly to do, what to say, what to bring."}}
  ],
  "faq": [
    {{"q": "Exact question as typed into Google by an immigrant", "a": "Direct answer in 2-4 sentences. First sentence answers the question. Cite law or official source where relevant."}}
  ],
  "official_sources": [
    {{"label": "Display text e.g. IRS — How to Get an ITIN", "url": "https://exact.gov.or.official.url"}}
  ],
  "warning": "Critical warning for this topic — specific and honest, or null",
  "info_tip": "Genuinely helpful practical tip, or null"
}}

REQUIREMENTS:
- sections: {5 if page['type'] == 'hub' else 4} minimum, each 200-350 words
- data_table: MUST include if topic has state comparisons, insurer lists, rates, requirements, license validity periods
- howto_steps: {6 if 'HowTo' in page.get('schema', []) else 0} steps for process pages, 0 otherwise
- faq: exactly {page.get('faq_count', 7)} questions phrased exactly as immigrants Google them
- official_sources: 3-5 real official URLs from the reference list
- NEVER state specific premium amounts as facts
- ALWAYS note when something varies by state
- ALWAYS include the ICE/privacy reassurance on any undocumented/no-SSN page"""


def state_page_prompt(state, lang):
    is_en = lang["code"] == "en"
    lang_note = "" if is_en else f"LANGUAGE: Write ALL content in {lang['name']}. Community: {lang['community']}"

    return f"""Write a car insurance guide for immigrants in {state} for CarInsuranceImmigrants.us.

STATE: {state}
{lang_note}

This page covers everything an immigrant in {state} needs to know about car insurance — state minimums, license rules, which insurers are best, and average rates.

Return ONLY this JSON:
{{
  "meta_title": "Car Insurance for Immigrants in {state} — Complete Guide",
  "meta_description": "145-158 chars about car insurance for immigrants in {state}",
  "h1": "Car Insurance for Immigrants in {state}",
  "definition": "2-3 sentence intro specific to {state} — mention the immigrant population, state license rules, and key insurance facts.",
  "intro_paragraph": "What makes {state} unique for immigrant drivers — key facts upfront.",
  "sections": [
    {{
      "h2": "{state} Car Insurance Requirements for Immigrants",
      "body": "<p>State minimum coverage requirements.</p><p>Enforcement and penalties.</p> Include real {state} minimums: liability limits, any no-fault rules."
    }},
    {{
      "h2": "Can Immigrants Get a Driver's License in {state}?",
      "body": "<p>Whether {state} issues licenses regardless of immigration status.</p><p>What documents are needed.</p><p>Link to {state} DMV.</p>"
    }},
    {{
      "h2": "Best Car Insurance Companies for Immigrants in {state}",
      "body": "<p>Which major insurers operate in {state} and accept ITIN.</p><p>Any {state}-specific insurers worth mentioning.</p>"
    }},
    {{
      "h2": "Average Car Insurance Rates for Immigrants in {state}",
      "body": "<p>How {state} compares nationally on rates.</p><p>Factors that affect immigrant rates in {state} specifically.</p><p>NEVER state exact premium — say get a quote.</p>"
    }},
    {{
      "h2": "Tips for Immigrants Getting Insurance in {state}",
      "body": "<p>{state}-specific tips and resources.</p><p>State insurance commissioner contact.</p>"
    }}
  ],
  "data_table": {{
    "caption": "{state} Car Insurance Requirements",
    "headers": ["Coverage Type", "Minimum Required", "Notes"],
    "rows": [
      ["Bodily Injury Liability", "{state} minimum", "Per person / per accident"],
      ["Property Damage Liability", "{state} minimum", ""],
      ["Uninsured Motorist", "Required or optional", "{state} rule"],
      ["Personal Injury Protection", "Required or optional", "{state} rule"]
    ]
  }},
  "faq": [
    {{"q": "Can I get car insurance in {state} without an SSN?", "a": "Direct answer for {state}."}},
    {{"q": "Does {state} give driver licenses to undocumented immigrants?", "a": "Direct answer."}},
    {{"q": "What is the minimum car insurance required in {state}?", "a": "Exact {state} minimums."}},
    {{"q": "Which insurance companies are best for immigrants in {state}?", "a": "Top options for {state}."}},
    {{"q": "How much does car insurance cost for immigrants in {state}?", "a": "Range and factors — direct to get a quote."}},
    {{"q": "Can I use a foreign license for insurance in {state}?", "a": "{state}-specific answer."}}
  ],
  "official_sources": [
    {{"label": "{state} DMV — Driver License Information", "url": "actual {state} DMV URL"}},
    {{"label": "{state} Department of Insurance", "url": "actual {state} insurance department URL"}},
    {{"label": "NCSL — States Issuing Licenses to Immigrants", "url": "https://www.ncsl.org/transportation/states-that-allow-unauthorized-immigrants-to-get-a-drivers-license"}}
  ],
  "warning": "{state}-specific warning if relevant, else null",
  "info_tip": "{state}-specific helpful tip"
}}"""


def insurer_page_prompt(insurer, lang):
    is_en = lang["code"] == "en"
    lang_note = "" if is_en else f"LANGUAGE: Write ALL content in {lang['name']}. Keep insurer name in English."

    return f"""Write a car insurance guide for immigrants about {insurer['name']} for CarInsuranceImmigrants.us.

INSURER: {insurer['name']}
ACCEPTS ITIN: {insurer['accepts_itin']}
ACCEPTS FOREIGN LICENSE: {insurer['accepts_foreign_license']}
NOTES: {insurer['notes']}
{lang_note}

Return ONLY this JSON:
{{
  "meta_title": "{insurer['name']} Car Insurance for Immigrants — ITIN, No SSN Guide",
  "meta_description": "145-158 chars",
  "h1": "{insurer['name']} Car Insurance for Immigrants — Complete Guide",
  "definition": "2-3 sentences: does {insurer['name']} accept immigrants, ITIN policy, general stance on immigrant customers.",
  "intro_paragraph": "Key facts upfront — can immigrants use {insurer['name']}, what they need.",
  "sections": [
    {{
      "h2": "Does {insurer['name']} Accept ITIN Instead of SSN?",
      "body": "<p>Direct answer: {insurer['accepts_itin']}.</p><p>How to apply with ITIN, what the agent will ask.</p><p>Any state variations.</p>"
    }},
    {{
      "h2": "Does {insurer['name']} Accept Foreign Driver's Licenses?",
      "body": "<p>Direct answer: {insurer['accepts_foreign_license']}.</p><p>Which foreign licenses they accept, any restrictions.</p>"
    }},
    {{
      "h2": "How to Get a Quote from {insurer['name']} as an Immigrant",
      "body": "<p>Step by step — what to have ready, what to say, how to get the best rate.</p>"
    }},
    {{
      "h2": "{insurer['name']} Rates for Immigrants — What to Expect",
      "body": "<p>General rate factors. Never state exact amounts. Direct them to get a quote.</p><p>How {insurer['name']} rates new immigrants with no US record.</p>"
    }}
  ],
  "data_table": {{
    "caption": "{insurer['name']} — Immigrant Customer Summary",
    "headers": ["Feature", "Available", "Notes"],
    "rows": [
      ["ITIN Accepted", "{'Yes' if insurer['accepts_itin'] else 'No'}", ""],
      ["Foreign License Accepted", "{'Yes' if insurer['accepts_foreign_license'] else 'Limited'}", ""],
      ["No US Credit History", "Yes", "Higher rates may apply"],
      ["Same Day Coverage", "Yes", ""],
      ["Spanish-Speaking Agents", "Yes", "Varies by location"]
    ]
  }},
  "faq": [
    {{"q": "Does {insurer['name']} require a Social Security number?", "a": "Direct answer with ITIN alternative."}},
    {{"q": "Can undocumented immigrants get {insurer['name']} insurance?", "a": "Direct honest answer."}},
    {{"q": "Will {insurer['name']} accept my foreign driver's license?", "a": "Direct answer."}},
    {{"q": "How do I get a {insurer['name']} quote without an SSN?", "a": "Step by step."}},
    {{"q": "Is {insurer['name']} good for new immigrants with no US driving history?", "a": "Honest assessment."}},
    {{"q": "Does {insurer['name']} have Spanish-speaking agents?", "a": "Answer."}}
  ],
  "official_sources": [
    {{"label": "NAIC — Check {insurer['name']} Complaints", "url": "https://content.naic.org/consumer"}},
    {{"label": "IRS — Get Your ITIN", "url": "https://www.irs.gov/individuals/individual-taxpayer-identification-number"}}
  ],
  "warning": "Always confirm current policy directly with {insurer['name']} — insurer policies can change and vary by state.",
  "info_tip": null
}}"""


def foreign_license_page_prompt(license_info, lang):
    is_en = lang["code"] == "en"
    lang_note = "" if is_en else f"LANGUAGE: Write ALL content in {lang['name']}. This is specifically for {lang['community']}."

    return f"""Write a car insurance guide for immigrants with a {license_info['country']} driver's license for CarInsuranceImmigrants.us.

COUNTRY: {license_info['country']}
TOP STATES FOR THIS COMMUNITY: {', '.join(license_info['top_states'])}
{lang_note}

Return ONLY this JSON:
{{
  "meta_title": "Car Insurance With {license_info['country']} Driver's License in the US",
  "meta_description": "145-158 chars",
  "h1": "Car Insurance With a {license_info['country']} Driver's License — US Guide",
  "definition": "2-3 sentences: can you get insurance with a {license_info['country']} license, is it recognized, key facts.",
  "intro_paragraph": "Address the {license_info['country']} immigrant community directly. What they most need to know.",
  "sections": [
    {{
      "h2": "Is a {license_info['country']} Driver's License Valid in the US?",
      "body": "<p>State-by-state validity.</p><p>How long it is valid.</p><p>IDP requirement.</p><p>Focus on {', '.join(license_info['top_states'][:3])} specifically.</p>"
    }},
    {{
      "h2": "Which US Insurers Accept a {license_info['country']} License?",
      "body": "<p>Major insurers and their policies.</p><p>State-specific variations.</p>"
    }},
    {{
      "h2": "How to Get Insurance With Your {license_info['country']} License",
      "body": "<p>Step by step — what documents to bring, what to say, how to apply.</p>"
    }},
    {{
      "h2": "Converting Your {license_info['country']} License to a US License",
      "body": "<p>Process in {', '.join(license_info['top_states'][:2])}.</p><p>Tests required, documents needed.</p><p>How conversion affects insurance rates.</p>"
    }}
  ],
  "data_table": {{
    "caption": "{license_info['country']} License Validity by State",
    "headers": ["State", "License Valid For", "IDP Required", "Can Use for Insurance"],
    "rows": [
      [state, "Check DMV", "Check state rules", "Yes with most insurers"]
      for state in {license_info['top_states']}
    ]
  }},
  "faq": [
    {{"q": "Can I get car insurance with my {license_info['country']} license?", "a": "Direct answer."}},
    {{"q": "How long is my {license_info['country']} license valid in the US?", "a": "State by state answer."}},
    {{"q": "Do I need to take a driving test if I have a {license_info['country']} license?", "a": "Depends on state."}},
    {{"q": "Which insurance companies accept {license_info['country']} licenses?", "a": "List of major ones."}},
    {{"q": "Can I get car insurance in {license_info['top_states'][0]} with my {license_info['country']} license?", "a": "State-specific answer."}},
    {{"q": "How do I convert my {license_info['country']} license to a US license?", "a": "Process overview."}}
  ],
  "official_sources": [
    {{"label": "NCSL — States Issuing Licenses Regardless of Status", "url": "https://www.ncsl.org/transportation/states-that-allow-unauthorized-immigrants-to-get-a-drivers-license"}},
    {{"label": "NAIC — Consumer Resources", "url": "https://content.naic.org/consumer"}}
  ],
  "warning": "License validity rules change — always verify with your state DMV before driving.",
  "info_tip": "Bring a certified translation of your {license_info['country']} license when applying for insurance — it speeds up the process significantly."
}}"""


def question_page_prompt(page, lang):
    """Special prompt for the 'burning questions' pages — most direct, most emotional."""
    is_en = lang["code"] == "en"
    lang_note = "" if is_en else f"LANGUAGE: Write ALL content in {lang['name']}. Community: {lang['community']}. This community has specific fears about this question — address them directly."

    return f"""Write a direct answer page for CarInsuranceImmigrants.us.

QUESTION: {page['title']}
IMMIGRANT ANGLE: {page['immigrant_angle']}
{lang_note}

This is NOT a generic insurance page. This is a DIRECT ANSWER to a question that immigrants are scared to ask. Open by answering the question completely in the first paragraph. No dancing around it.

Return ONLY this JSON:
{{
  "meta_title": "{page['title'][:58]}",
  "meta_description": "145-158 chars — answers the question directly in the description",
  "h1": "{page['title']}",
  "definition": "Answer the question completely and directly in 2-3 sentences. No hedging. Cite the law or regulation that supports the answer. This is the most important paragraph on the page.",
  "intro_paragraph": "Acknowledge the fear behind the question. Then immediately deliver the reassurance or honest answer. Make them feel understood.",
  "sections": [
    {{
      "h2": "The Direct Answer",
      "body": "<p>Full detailed explanation of the answer.</p><p>Why this is the case — the law, the regulation, the practical reality.</p>"
    }},
    {{
      "h2": "What You Need to Know",
      "body": "<p>The nuances, the state variations, the exceptions.</p><p>What could change the answer for their specific situation.</p>"
    }},
    {{
      "h2": "What to Do Next",
      "body": "<p>Practical next steps based on the answer.</p><p>How to protect yourself, what documents to get, who to contact.</p>"
    }},
    {{
      "h2": "Your Rights in This Situation",
      "body": "<p>Legal rights that apply. Federal law that protects them.</p><p>What authorities can and cannot do.</p>"
    }}
  ],
  "data_table": null,
  "howto_steps": null,
  "faq": [
    {{"q": "Follow-up question someone would ask after reading this", "a": "Direct answer."}}
  ],
  "official_sources": [
    {{"label": "Relevant official source for this question", "url": "https://official.url"}}
  ],
  "warning": "If there is a real risk they need to know about — state it clearly. If not, null.",
  "info_tip": "Most useful practical tip related to this question."
}}

FAQ: exactly {page.get('faq_count', 7)} questions
CRITICAL: The first sentence of 'definition' must answer the question. No exceptions."""


def homepage_prompt(lang):
    return f"""Write homepage content for CarInsuranceImmigrants.us in {lang['name']}.

This is the most comprehensive car insurance information site for immigrants in the US. It answers every question immigrants have — without SSN, with foreign license, undocumented, DACA, new arrival.

Community this language serves: {lang['community']}

Return ONLY this JSON:
{{
  "hero_headline": "Powerful 8-10 word headline in {lang['name']} — conveys: car insurance help for immigrants, in their language",
  "hero_subtext": "2 sentences in {lang['name']} — what the site does, that it's free, that it answers the questions others won't",
  "urgent_question": "The most urgent question this community has about car insurance — in {lang['name']}",
  "about_blurb": "3 sentences in {lang['name']} — site mission, free information, no ICE reporting"
}}"""
