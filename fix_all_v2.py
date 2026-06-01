#!/usr/bin/env python3
"""
fix_all_v2.py — One script to fix everything:
1. Hero text on English homepage — professional tone
2. Sarah on ALL pages — open by default, bigger, not a bubble
3. Lang pills on homepage — restored clean
4. Remove nav lang-switcher from all pages
"""

import re, glob

# ─── 1. PROFESSIONAL HERO TEXT ────────────────────────────────────────────────
NEW_HERO_TEXT = "Car insurance information for everyone — in your language, at no cost. We cover every question about getting covered without an SSN, with a foreign license, or as a new arrival. Clear answers, no judgment."

# ─── 2. LANG PILLS CSS + HTML ─────────────────────────────────────────────────
LANG_CSS = '''<style>
.lang-grid{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:24px auto 0;max-width:500px;padding:0 16px}
.lang-pill{background:rgba(255,255,255,0.12);border:1.5px solid rgba(255,255,255,0.3);color:#fff;padding:8px 16px;border-radius:24px;font-size:0.85rem;font-weight:500;text-decoration:none;transition:all 0.2s;white-space:nowrap;display:inline-block}
.lang-pill:hover,.lang-pill.active{background:rgba(255,255,255,0.25);border-color:rgba(255,255,255,0.7);color:#fff;text-decoration:none}
</style>'''

LANG_PILLS_EN = '''<div class="lang-grid">
  <a href="/" class="lang-pill active">English</a>
  <a href="/es/" class="lang-pill">Español</a>
  <a href="/zh/" class="lang-pill">中文</a>
  <a href="/ar/" class="lang-pill">العربية</a>
  <a href="/pt/" class="lang-pill">Português</a>
  <a href="/vi/" class="lang-pill">Tiếng Việt</a>
  <a href="/tl/" class="lang-pill">Filipino</a>
  <a href="/ko/" class="lang-pill">한국어</a>
  <a href="/ru/" class="lang-pill">Русский</a>
  <a href="/pl/" class="lang-pill">Polski</a>
</div>'''

# ─── 3. SARAH WIDGET ──────────────────────────────────────────────────────────
def build_sarah(lang_code='en', auto_open=False):
    greetings = {
        'en': "Hi, I am Sarah. I can help you find car insurance — no matter your situation. What is your full name?",
        'es': "Hola, soy Sarah. Puedo ayudarle a encontrar seguro de auto. Cual es su nombre completo?",
        'zh': "您好，我是Sarah。我可以帮您找到汽车保险。请问您的全名是什么？",
        'ar': "مرحبا، انا سارة. يمكنني مساعدتك في ايجاد تامين سيارة. ما اسمك الكامل؟",
        'pt': "Ola, sou Sarah. Posso ajuda-lo a encontrar seguro de carro. Qual e o seu nome completo?",
        'ru': "Здравствуйте, я Сара. Я помогу найти автостраховку. Как вас зовут?",
        'pl': "Czesc, jestem Sarah. Moge pomoc znalezc ubezpieczenie. Jak masz na imie?",
        'vi': "Xin chao, toi la Sarah. Toi co the giup ban tim bao hiem xe hoi. Ten day du cua ban la gi?",
        'tl': "Kumusta, ako si Sarah. Matutulungan kita mahanap ng car insurance. Ano ang iyong buong pangalan?",
        'ko': "안녕하세요, 저는 Sarah예요. 자동차 보험 찾는 걸 도와드릴게요. 성함이 어떻게 되세요?",
    }
    systems = {
        'en': 'You are Sarah, a car insurance specialist at CarInsuranceImmigrants.us. Help immigrants get car insurance. Max 2 sentences. Professional and warm.',
        'es': 'Eres Sarah, especialista en seguros de auto. Responde en espanol. Maximo 2 oraciones.',
        'zh': '你是Sarah，汽车保险专家。用中文回答。最多2句话。',
        'ar': 'انت سارة، متخصصة تامين سيارات. اجيبي بالعربية. جملتان كحد اقصى.',
        'pt': 'Voce e Sarah, especialista em seguros. Responda em portugues. Maximo 2 frases.',
        'ru': 'Вы Сара, специалист по автострахованию. Отвечайте по-русски. Максимум 2 предложения.',
        'pl': 'Jestes Sarah, specjalista ds. ubezpieczen. Odpowiadaj po polsku. Maksymalnie 2 zdania.',
        'vi': 'Ban la Sarah, chuyen gia bao hiem xe hoi. Tra loi bang tieng Viet. Toi da 2 cau.',
        'tl': 'Ikaw si Sarah, car insurance specialist. Sumagot sa Filipino. 2 pangungusap lang.',
        'ko': '당신은 Sarah, 자동차 보험 전문가입니다. 한국어로 답하세요. 최대 2문장.',
    }
    greeting = greetings.get(lang_code, greetings['en'])
    system = systems.get(lang_code, systems['en'])
    sys_esc = system.replace('"', "'")
    
    # Auto-open JS
    auto_js = 'setTimeout(function(){if(!sarahOpen)toggleSarah();},2500);' if auto_open else ''
    
    return f'''
<!-- Sarah Widget -->
<div id="sarah-wrap" style="position:fixed;bottom:24px;right:24px;z-index:9999;width:380px;max-width:calc(100vw - 32px);font-family:system-ui,-apple-system,sans-serif">
  <div id="sarah-panel" style="background:#fff;border-radius:16px;box-shadow:0 8px 40px rgba(0,0,0,0.2);overflow:hidden">
    <div style="background:linear-gradient(135deg,#0f2944,#1a4a7a);padding:14px 18px;display:flex;align-items:center;gap:12px">
      <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=80&h=80&fit=crop&crop=face" alt="Sarah" style="width:42px;height:42px;border-radius:50%;object-fit:cover;border:2px solid rgba(245,158,11,0.5);flex-shrink:0" onerror="this.style.display=\'none\'">
      <div style="flex:1">
        <div style="color:#fff;font-weight:700;font-size:0.95rem">Sarah</div>
        <div style="color:rgba(255,255,255,0.65);font-size:0.75rem">Car Insurance Specialist</div>
      </div>
      <div style="display:flex;align-items:center;gap:5px;margin-right:8px">
        <div style="width:7px;height:7px;background:#22c55e;border-radius:50%"></div>
        <span style="color:rgba(255,255,255,0.65);font-size:0.72rem">Online</span>
      </div>
      <button onclick="toggleSarah()" style="background:none;border:none;color:rgba(255,255,255,0.6);font-size:1.2rem;cursor:pointer;padding:2px 6px">—</button>
    </div>
    <div id="sarah-msgs" style="background:#f8fafc;padding:14px;min-height:100px;max-height:260px;overflow-y:auto;display:flex;flex-direction:column;gap:10px">
      <div style="background:#fff;border-radius:12px 12px 12px 4px;padding:11px 14px;font-size:0.88rem;color:#374151;box-shadow:0 1px 3px rgba(0,0,0,0.07);max-width:92%;line-height:1.55">{greeting}</div>
    </div>
    <div id="sarah-step1" style="padding:12px 14px;border-top:1px solid #e5e7eb">
      <div style="display:flex;gap:8px">
        <input id="sarah-input" type="text" placeholder="Type here..." style="flex:1;border:1px solid #d1d5db;border-radius:8px;padding:10px 13px;font-size:0.88rem;outline:none" onkeydown="if(event.key===\'Enter\')sarahSend()">
        <button onclick="sarahSend()" style="background:#f59e0b;color:#fff;border:none;border-radius:8px;padding:10px 18px;font-weight:700;cursor:pointer">&#8594;</button>
      </div>
      <div style="text-align:center;font-size:0.72rem;color:#9ca3af;margin-top:5px">Free · Confidential · No SSN required</div>
    </div>
    <div id="sarah-step2" style="display:none;padding:14px;border-top:1px solid #e5e7eb">
      <div style="font-weight:700;color:#0f2944;font-size:0.88rem;margin-bottom:10px">Tell me about your vehicle</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-bottom:7px">
        <select id="s-year" style="border:1px solid #d1d5db;border-radius:7px;padding:8px 9px;font-size:0.82rem;background:#fff;width:100%"><option value="">Year</option><option>2026</option><option>2025</option><option>2024</option><option>2023</option><option>2022</option><option>2021</option><option>2020</option><option>2019</option><option>2018</option><option>2017</option><option>2016</option><option>2015</option><option>2014</option><option>2013</option><option>2012</option><option>2011</option><option>2010</option><option>2009</option><option>2008</option><option>2007</option><option>2006</option><option>2005</option><option>2004</option><option>2003</option><option>2002</option><option>2001</option><option>2000</option><option>1999</option><option>1998</option><option>1997</option><option>1995</option></select>
        <select id="s-make" style="border:1px solid #d1d5db;border-radius:7px;padding:8px 9px;font-size:0.82rem;background:#fff;width:100%"><option value="">Make</option><option>Chevrolet</option><option>Ford</option><option>Honda</option><option>Toyota</option><option>Nissan</option><option>Hyundai</option><option>Kia</option><option>Jeep</option><option>Dodge</option><option>Ram</option><option>GMC</option><option>Subaru</option><option>Mazda</option><option>Volkswagen</option><option>BMW</option><option>Mercedes-Benz</option><option>Audi</option><option>Lexus</option><option>Tesla</option><option>Other</option></select>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-bottom:7px">
        <input id="s-model" type="text" placeholder="Model" style="border:1px solid #d1d5db;border-radius:7px;padding:8px 9px;font-size:0.82rem">
        <select id="s-state" style="border:1px solid #d1d5db;border-radius:7px;padding:8px 9px;font-size:0.82rem;background:#fff;width:100%"><option value="">State</option><option>California</option><option>Texas</option><option>Florida</option><option>New York</option><option>Illinois</option><option>Pennsylvania</option><option>Ohio</option><option>Georgia</option><option>North Carolina</option><option>Michigan</option><option>New Jersey</option><option>Virginia</option><option>Washington</option><option>Arizona</option><option>Massachusetts</option><option>Tennessee</option><option>Indiana</option><option>Missouri</option><option>Maryland</option><option>Wisconsin</option><option>Colorado</option><option>Minnesota</option><option>South Carolina</option><option>Alabama</option><option>Louisiana</option><option>Kentucky</option><option>Oregon</option><option>Oklahoma</option><option>Connecticut</option><option>Utah</option><option>Nevada</option><option>Arkansas</option><option>Mississippi</option><option>Kansas</option><option>New Mexico</option><option>Nebraska</option><option>West Virginia</option><option>Idaho</option><option>Hawaii</option><option>New Hampshire</option><option>Maine</option><option>Montana</option><option>Rhode Island</option><option>Delaware</option><option>South Dakota</option><option>North Dakota</option><option>Alaska</option><option>Vermont</option><option>Wyoming</option><option>Other</option></select>
      </div>
      <select id="s-license" style="border:1px solid #d1d5db;border-radius:7px;padding:8px 9px;font-size:0.82rem;background:#fff;width:100%;margin-bottom:10px"><option value="">License type</option><option>US License</option><option>Foreign License</option><option>Mexican License</option><option>International License</option><option>No License</option></select>
      <button onclick="sarahSubmit()" style="width:100%;background:linear-gradient(135deg,#16a34a,#15803d);color:#fff;border:none;border-radius:9px;padding:12px;font-size:0.92rem;font-weight:700;cursor:pointer">Find My Insurance</button>
      <div style="text-align:center;font-size:0.72rem;color:#9ca3af;margin-top:6px">Your information is never shared with any government agency</div>
    </div>
    <div id="sarah-step3" style="display:none;padding:12px 14px;border-top:1px solid #e5e7eb">
      <div style="display:flex;gap:8px">
        <input id="sarah-chat" type="text" placeholder="Ask a question..." style="flex:1;border:1px solid #d1d5db;border-radius:8px;padding:10px 13px;font-size:0.88rem;outline:none" onkeydown="if(event.key===\'Enter\')sarahChat()">
        <button onclick="sarahChat()" style="background:#0f2944;color:#fff;border:none;border-radius:8px;padding:10px 16px;font-weight:700;cursor:pointer">&#8594;</button>
      </div>
    </div>
  </div>
  <button id="sarah-min-btn" onclick="toggleSarah()" style="display:none;background:linear-gradient(135deg,#0f2944,#1a4a7a);color:#fff;border:none;border-radius:30px;padding:12px 20px;font-size:0.88rem;font-weight:600;cursor:pointer;box-shadow:0 4px 16px rgba(0,0,0,0.2);width:100%;margin-top:8px">Chat with Sarah &rarr;</button>
</div>
<script>
var sarahOpen=true,sarahStep=0,sarahName='',sarahPhone='',sarahHist=[];
var SSYS="{sys_esc} Page: "+document.title+". URL: "+window.location.pathname;
{auto_js}
function toggleSarah(){{sarahOpen=!sarahOpen;document.getElementById('sarah-panel').style.display=sarahOpen?'block':'none';document.getElementById('sarah-min-btn').style.display=sarahOpen?'none':'block';}}
function sarahAddBot(t){{var m=document.getElementById('sarah-msgs');var d=document.createElement('div');d.style.cssText='background:#fff;border-radius:12px 12px 12px 4px;padding:11px 14px;font-size:0.88rem;color:#374151;box-shadow:0 1px 3px rgba(0,0,0,0.07);max-width:92%;line-height:1.55';d.textContent=t;m.appendChild(d);m.scrollTop=m.scrollHeight;}}
function sarahAddUser(t){{var m=document.getElementById('sarah-msgs');var d=document.createElement('div');d.style.cssText='background:#0f2944;color:#fff;border-radius:12px 12px 4px 12px;padding:10px 13px;font-size:0.88rem;max-width:85%;align-self:flex-end;margin-left:auto;line-height:1.5';d.textContent=t;m.appendChild(d);m.scrollTop=m.scrollHeight;}}
function sarahSend(){{var i=document.getElementById('sarah-input');var v=i.value.trim();if(!v)return;i.value='';sarahAddUser(v);if(sarahStep===0){{sarahName=v;sarahStep=1;setTimeout(()=>sarahAddBot('And your phone number?'),300);}}else if(sarahStep===1){{sarahPhone=v;sarahStep=2;setTimeout(()=>{{sarahAddBot('Got it. Now tell me about your vehicle.');document.getElementById('sarah-step1').style.display='none';document.getElementById('sarah-step2').style.display='block';}},300);}}}};
async function sarahSubmit(){{var year=document.getElementById('s-year').value;var make=document.getElementById('s-make').value;var state=document.getElementById('s-state').value;var model=document.getElementById('s-model').value;var license=document.getElementById('s-license').value;if(!year||!make||!state){{alert('Please select year, make and state.');return;}}var lead={{name:sarahName,phone:sarahPhone,year,make,model,state,license,url:window.location.href,time:new Date().toISOString()}};console.log('LEAD:',JSON.stringify(lead));document.getElementById('sarah-step2').style.display='none';document.getElementById('sarah-step3').style.display='block';sarahStep=3;sarahAddUser(year+' '+make+' — '+state);sarahHist.push({{role:'user',content:'Details: '+sarahName+', '+sarahPhone+', '+year+' '+make+' '+model+', '+state+', '+license}});setTimeout(async()=>{{try{{var r=await fetch('https://api.anthropic.com/v1/messages',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{model:'claude-haiku-4-5-20251001',max_tokens:150,system:SSYS,messages:sarahHist}})}});var d=await r.json();var rep=d.content&&d.content[0]?d.content[0].text:'Thank you. A specialist will contact you shortly.';sarahAddBot(rep);sarahHist.push({{role:'assistant',content:rep}})}}catch(e){{sarahAddBot('Thank you '+sarahName+'. A specialist will contact you at '+sarahPhone+' shortly.');}}}},400);}}
async function sarahChat(){{var i=document.getElementById('sarah-chat');var msg=i.value.trim();if(!msg)return;i.value='';sarahAddUser(msg);sarahHist.push({{role:'user',content:msg}});try{{var r=await fetch('https://api.anthropic.com/v1/messages',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{model:'claude-haiku-4-5-20251001',max_tokens:150,system:SSYS,messages:sarahHist}})}});var d=await r.json();var rep=d.content&&d.content[0]?d.content[0].text:'Please try again.';sarahAddBot(rep);sarahHist.push({{role:'assistant',content:rep}})}}catch(e){{sarahAddBot('Please try again.');}}}}
</script>'''


def get_lang(filepath):
    parts = filepath.replace('\\','/').split('/')
    langs = ['es','zh','ar','pt','vi','tl','ko','ru','pl']
    for p in parts:
        if p in langs:
            return p
    return 'en'


def is_homepage(filepath):
    fp = filepath.replace('\\','/')
    homepages = ['index.html','es/index.html','zh/index.html','ar/index.html',
                 'pt/index.html','vi/index.html','tl/index.html','ko/index.html',
                 'ru/index.html','pl/index.html']
    return fp in homepages


# ─── PROCESS ALL FILES ────────────────────────────────────────────────────────
files = [f for f in glob.glob('**/*.html', recursive=True) if not f.startswith('.')]
print(f"Processing {len(files)} files...")

hero_fixed = 0
sarah_added = 0
nav_fixed = 0
pills_fixed = 0

for filepath in files:
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        original = content
        lang = get_lang(filepath)
        homepage = is_homepage(filepath)

        # 1. Fix hero text on English homepage
        if filepath == 'index.html':
            old_texts = [
                "We answer every car insurance question immigrants have — including the ones other sites won't touch, like getting covered without an SSN, with a foreign license, or without legal status. Everything here is free, in plain language, and written specifically for people navigating the US insurance system for the first time.",
                "CarInsuranceImmigrants.us answers every car insurance question immigrants have — including the ones other sites won't touch",
            ]
            for old in old_texts:
                if old in content:
                    content = content.replace(old, NEW_HERO_TEXT)
                    hero_fixed += 1
                    break

        # 2. Remove ALL old Sarah widgets
        content = re.sub(r'<!-- Sarah.*?</script>\s*', '', content, flags=re.DOTALL)
        content = re.sub(r'<!-- Sarah V\d.*?</script>\s*', '', content, flags=re.DOTALL)
        content = re.sub(r'<!-- Sarah Widget.*?</script>\s*', '', content, flags=re.DOTALL)
        content = re.sub(r'<div id="sarah-wrap".*?</script>\s*', '', content, flags=re.DOTALL)
        content = re.sub(r'<button id="sarah-minimize".*?</button>', '', content, flags=re.DOTALL)

        # 3. Remove nav lang-switcher
        content = re.sub(r'<div class="lang-switcher">.*?</div>', '', content, flags=re.DOTALL)
        nav_fixed += 1

        # 4. Add lang CSS to head if homepage
        if homepage and '.lang-pill' not in content:
            content = content.replace('</head>', LANG_CSS + '\n</head>', 1)

        # 5. Fix English homepage lang pills
        if filepath == 'index.html':
            # Remove any duplicate pills
            content = re.sub(r'<div class="lang-grid">.*?</div>', '', content, flags=re.DOTALL)
            content = re.sub(r'<div class="lang-bar">.*?</div>', '', content, flags=re.DOTALL)
            # Add pills before stats-bar or before Sarah section
            if 'stats-bar' in content:
                content = re.sub(r'(<div class="stats-bar">)', LANG_PILLS_EN + '\n\\1', content, count=1)
                # Remove stats-bar
                content = re.sub(r'<div class="stats-bar">.*?</div>', '', content, flags=re.DOTALL, count=1)
            pills_fixed += 1

        # 6. Add Sarah — open by default on all pages
        # On homepages: don't add floating Sarah (has hardcoded one)
        # On inner pages: add floating Sarah, auto-opens after 2.5s
        if not homepage:
            sarah = build_sarah(lang, auto_open=True)
            content = content.replace('</body>', sarah + '\n</body>', 1)
            sarah_added += 1

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)

    except Exception as e:
        print(f"  Error {filepath}: {e}")

print(f"\n{'='*50}")
print(f"Hero text fixed:  {hero_fixed}")
print(f"Nav cleaned:      {nav_fixed}")
print(f"Sarah added:      {sarah_added} inner pages")
print(f"Pills fixed:      {pills_fixed}")
print(f"{'='*50}")
