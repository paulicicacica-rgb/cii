#!/usr/bin/env python3
"""
fix_homepage_v3.py
- Fixes double language pills on all homepages
- Sarah speaks correct language per homepage
- Removes injected English Sarah from non-English homepages
- Only injects correct language Sarah on each homepage
"""

import re, glob

LANGS = {
    'en': {
        'greeting': 'Hi, I am Sarah. I can help you find car insurance — no matter your situation. What is your full name?',
        'phone_q': 'And your phone number?',
        'car_title': 'Now tell me about your vehicle',
        'placeholder': 'Type here...',
        'submit': 'Find My Insurance',
        'privacy': 'Your information is never shared with any government agency.',
        'cta_label': 'GET STARTED',
        'cta_h2': 'Tell Sarah about your situation.<br>She will find you the right coverage.',
        'cta_sub': 'Free · No obligation · No SSN required',
        'specialist': 'Car Insurance Specialist',
        'got_it': 'Got it. Now tell me about your vehicle.',
        'thank_you': 'Thank you. A specialist will contact you shortly. Do you have any questions?',
        'system': 'You are Sarah, a car insurance specialist. Help users get car insurance. Max 2 sentences per reply.',
        'prefix': '',
    },
    'es': {
        'greeting': 'Hola, soy Sarah. Puedo ayudarle a encontrar seguro de auto — sin importar su situacion. Cual es su nombre completo?',
        'phone_q': 'Y su numero de telefono?',
        'car_title': 'Ahora cuenteme sobre su vehiculo',
        'placeholder': 'Escriba aqui...',
        'submit': 'Encontrar Mi Seguro',
        'privacy': 'Su informacion nunca se comparte con ninguna agencia gubernamental.',
        'cta_label': 'COMENZAR',
        'cta_h2': 'Cuentele a Sarah su situacion.<br>Ella encontrara la cobertura correcta.',
        'cta_sub': 'Gratis · Sin compromiso · Sin SSN requerido',
        'specialist': 'Especialista en Seguros',
        'got_it': 'Entendido. Ahora cuenteme sobre su vehiculo.',
        'thank_you': 'Gracias. Un especialista le contactara pronto. Tiene alguna pregunta?',
        'system': 'Eres Sarah, especialista en seguros de auto. Ayuda en espanol. Maximo 2 oraciones.',
        'prefix': 'es/',
    },
    'zh': {
        'greeting': '您好，我是Sarah。无论您的情况如何，我都可以帮您找到汽车保险。请问您的全名是什么？',
        'phone_q': '您的电话号码？',
        'car_title': '告诉我您的车辆信息',
        'placeholder': '在此输入...',
        'submit': '找到我的保险',
        'privacy': '您的信息绝不会与任何政府机构共享。',
        'cta_label': '开始',
        'cta_h2': '告诉Sarah您的情况。<br>她会为您找到合适的保险。',
        'cta_sub': '免费 · 无义务 · 不需要SSN',
        'specialist': '汽车保险专家',
        'got_it': '好的。现在告诉我您的车辆信息。',
        'thank_you': '谢谢。专家将很快与您联系。您有什么问题吗？',
        'system': '你是Sarah，汽车保险专家。用中文回答。最多2句话。',
        'prefix': 'zh/',
    },
    'ar': {
        'greeting': 'مرحبا، انا سارة. يمكنني مساعدتك في ايجاد تامين سيارة — بغض النظر عن وضعك. ما اسمك الكامل؟',
        'phone_q': 'ورقم هاتفك؟',
        'car_title': 'الان اخبرني عن سيارتك',
        'placeholder': 'اكتب هنا...',
        'submit': 'ابحث عن تاميني',
        'privacy': 'معلوماتك لن تشارك مع اي جهة حكومية.',
        'cta_label': 'ابدا',
        'cta_h2': 'اخبر سارة عن وضعك.<br>ستجد لك التغطية المناسبة.',
        'cta_sub': 'مجاني · بدون التزام · بدون SSN',
        'specialist': 'متخصصة تامين السيارات',
        'got_it': 'حسنا. الان اخبرني عن سيارتك.',
        'thank_you': 'شكرا. سيتواصل معك متخصص قريبا. هل لديك اي اسئلة؟',
        'system': 'انت سارة، متخصصة تامين سيارات. اجيبي بالعربية. جملتان كحد اقصى.',
        'prefix': 'ar/',
    },
    'pt': {
        'greeting': 'Ola, sou a Sarah. Posso ajuda-lo a encontrar seguro de carro — independente da sua situacao. Qual e o seu nome completo?',
        'phone_q': 'E o seu numero de telefone?',
        'car_title': 'Agora fale sobre o seu veiculo',
        'placeholder': 'Digite aqui...',
        'submit': 'Encontrar Meu Seguro',
        'privacy': 'Suas informacoes nunca sao compartilhadas com nenhuma agencia governamental.',
        'cta_label': 'COMECAR',
        'cta_h2': 'Conte a Sarah sua situacao.<br>Ela encontrara a cobertura certa.',
        'cta_sub': 'Gratis · Sem compromisso · Sem SSN',
        'specialist': 'Especialista em Seguros',
        'got_it': 'Entendido. Agora fale sobre o seu veiculo.',
        'thank_you': 'Obrigado. Um especialista entrara em contato em breve.',
        'system': 'Voce e Sarah, especialista em seguros de auto. Responda em portugues. Maximo 2 frases.',
        'prefix': 'pt/',
    },
    'ru': {
        'greeting': 'Здравствуйте, я Сара. Я помогу вам найти автостраховку — независимо от вашей ситуации. Как вас зовут?',
        'phone_q': 'Ваш номер телефона?',
        'car_title': 'Теперь расскажите о вашем автомобиле',
        'placeholder': 'Введите здесь...',
        'submit': 'Найти страховку',
        'privacy': 'Ваши данные никогда не передаются государственным органам.',
        'cta_label': 'НАЧАТЬ',
        'cta_h2': 'Расскажите Саре о вашей ситуации.<br>Она найдет подходящее покрытие.',
        'cta_sub': 'Бесплатно · Без обязательств · Без SSN',
        'specialist': 'Специалист по страхованию',
        'got_it': 'Понятно. Теперь расскажите об автомобиле.',
        'thank_you': 'Спасибо. Специалист свяжется с вами.',
        'system': 'Вы Сара, специалист по автострахованию. Отвечайте по-русски. Максимум 2 предложения.',
        'prefix': 'ru/',
    },
    'pl': {
        'greeting': 'Czesc, jestem Sarah. Moge pomoc ci znalezc ubezpieczenie samochodu — bez wzgledu na twoja sytuacje. Jak masz na imie?',
        'phone_q': 'Twoj numer telefonu?',
        'car_title': 'Teraz opowiedz o swoim samochodzie',
        'placeholder': 'Wpisz tutaj...',
        'submit': 'Znajdz moje ubezpieczenie',
        'privacy': 'Twoje dane nigdy nie sa udostepniane zadnej agencji rzadowej.',
        'cta_label': 'ZACZNIJ',
        'cta_h2': 'Opowiedz Sarah o swojej sytuacji.<br>Ona znajdzie odpowiednie ubezpieczenie.',
        'cta_sub': 'Bezplatnie · Bez zobowiazan · Bez SSN',
        'specialist': 'Specjalista ds. ubezpieczen',
        'got_it': 'Rozumiem. Teraz opowiedz o swoim samochodzie.',
        'thank_you': 'Dziekuje. Specjalista skontaktuje sie wkrotce.',
        'system': 'Jestes Sarah, specjalista ds. ubezpieczen samochodowych. Odpowiadaj po polsku. Maksymalnie 2 zdania.',
        'prefix': 'pl/',
    },
}

# Fallback for vi, tl, ko
for lang in ['vi', 'tl', 'ko']:
    LANGS[lang] = LANGS['en'].copy()
    LANGS[lang]['prefix'] = f'{lang}/'

LANG_PILLS_TEMPLATE = '''<div class="lang-grid">
  <a href="/" class="lang-pill{en_active}">English</a>
  <a href="/es/" class="lang-pill{es_active}">Español</a>
  <a href="/zh/" class="lang-pill{zh_active}">中文</a>
  <a href="/ar/" class="lang-pill{ar_active}">العربية</a>
  <a href="/pt/" class="lang-pill{pt_active}">Português</a>
  <a href="/vi/" class="lang-pill{vi_active}">Tiếng Việt</a>
  <a href="/tl/" class="lang-pill{tl_active}">Filipino</a>
  <a href="/ko/" class="lang-pill{ko_active}">한국어</a>
  <a href="/ru/" class="lang-pill{ru_active}">Русский</a>
  <a href="/pl/" class="lang-pill{pl_active}">Polski</a>
</div>'''

LANG_CSS = '''<style>
.lang-grid{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:24px auto 0;max-width:480px}
.lang-pill{background:rgba(255,255,255,0.12);border:1.5px solid rgba(255,255,255,0.3);color:#fff;padding:8px 16px;border-radius:24px;font-size:0.85rem;font-weight:500;text-decoration:none;transition:all 0.2s;white-space:nowrap}
.lang-pill:hover,.lang-pill.active{background:rgba(255,255,255,0.25);border-color:rgba(255,255,255,0.7);color:#fff;text-decoration:none}
</style>'''

def build_lang_pills(active_lang):
    active = {l: ' active' if l == active_lang else '' for l in LANGS}
    return LANG_PILLS_TEMPLATE.format(**{f'{l}_active': v for l, v in active.items()})

def build_sarah_section(lang_code):
    cfg = LANGS.get(lang_code, LANGS['en'])
    sys_escaped = cfg['system'].replace('"', "'")
    prefix = cfg['prefix']
    
    return f'''
<!-- Sarah Hardcoded Section -->
<div style="background:#f7f9fc;padding:60px 24px 80px;text-align:center">
  <div style="max-width:480px;margin:0 auto">
    <p style="color:#f59e0b;font-size:0.78rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:12px">{cfg["cta_label"]}</p>
    <h2 style="font-size:clamp(1.5rem,4vw,2rem);font-weight:800;color:#0f2944;line-height:1.3;margin-bottom:10px">{cfg["cta_h2"]}</h2>
    <p style="color:#6b7280;font-size:0.9rem;margin-bottom:28px">{cfg["cta_sub"]}</p>

    <div style="background:#fff;border-radius:16px;box-shadow:0 8px 40px rgba(0,0,0,0.12);overflow:hidden;text-align:left">
      <div style="background:linear-gradient(135deg,#0f2944,#1a4a7a);padding:14px 18px;display:flex;align-items:center;gap:12px">
        <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=80&h=80&fit=crop&crop=face" alt="Sarah" style="width:42px;height:42px;border-radius:50%;object-fit:cover;border:2px solid rgba(245,158,11,0.6);flex-shrink:0" onerror="this.style.display=\'none\'">
        <div style="flex:1">
          <div style="color:#fff;font-weight:700;font-size:0.95rem">Sarah</div>
          <div style="color:rgba(255,255,255,0.65);font-size:0.75rem">{cfg["specialist"]}</div>
        </div>
        <div style="display:flex;align-items:center;gap:5px">
          <div style="width:7px;height:7px;background:#22c55e;border-radius:50%"></div>
          <span style="color:rgba(255,255,255,0.65);font-size:0.75rem">Online</span>
        </div>
      </div>

      <div id="s3-msgs" style="background:#f8fafc;padding:16px;min-height:80px;max-height:220px;overflow-y:auto;display:flex;flex-direction:column;gap:10px">
        <div style="background:#fff;border-radius:12px 12px 12px 4px;padding:11px 14px;font-size:0.88rem;color:#374151;box-shadow:0 1px 3px rgba(0,0,0,0.07);max-width:88%;line-height:1.55">{cfg["greeting"]}</div>
      </div>

      <div id="s3-step1" style="padding:12px 14px;border-top:1px solid #e5e7eb">
        <div style="display:flex;gap:8px">
          <input id="s3-input" type="text" placeholder="{cfg["placeholder"]}" style="flex:1;border:1px solid #d1d5db;border-radius:8px;padding:10px 13px;font-size:0.88rem;outline:none" onkeydown="if(event.key===\'Enter\')s3Send()">
          <button onclick="s3Send()" style="background:#f59e0b;color:#fff;border:none;border-radius:8px;padding:10px 18px;font-weight:700;cursor:pointer;font-size:0.9rem">&#8594;</button>
        </div>
        <div style="text-align:center;font-size:0.72rem;color:#9ca3af;margin-top:6px">Free · No obligation · No SSN required</div>
      </div>

      <div id="s3-step2" style="display:none;padding:14px;border-top:1px solid #e5e7eb">
        <div style="font-weight:700;color:#0f2944;font-size:0.88rem;margin-bottom:10px">{cfg["car_title"]}</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-bottom:7px">
          <select id="s3-year" style="border:1px solid #d1d5db;border-radius:7px;padding:8px 9px;font-size:0.82rem;background:#fff;width:100%">
            <option value="">Year</option>
            {"".join(f"<option>{y}</option>" for y in range(2026,1989,-1))}
          </select>
          <select id="s3-make" style="border:1px solid #d1d5db;border-radius:7px;padding:8px 9px;font-size:0.82rem;background:#fff;width:100%">
            <option value="">Make</option>
            <option>Chevrolet</option><option>Ford</option><option>Honda</option><option>Toyota</option><option>Nissan</option><option>Hyundai</option><option>Kia</option><option>Jeep</option><option>Dodge</option><option>Ram</option><option>GMC</option><option>Subaru</option><option>Mazda</option><option>Volkswagen</option><option>BMW</option><option>Mercedes-Benz</option><option>Audi</option><option>Lexus</option><option>Tesla</option><option>Other</option>
          </select>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-bottom:7px">
          <input id="s3-model" type="text" placeholder="Model" style="border:1px solid #d1d5db;border-radius:7px;padding:8px 9px;font-size:0.82rem">
          <select id="s3-state" style="border:1px solid #d1d5db;border-radius:7px;padding:8px 9px;font-size:0.82rem;background:#fff;width:100%">
            <option value="">State</option>
            <option>California</option><option>Texas</option><option>Florida</option><option>New York</option><option>Illinois</option><option>Pennsylvania</option><option>Ohio</option><option>Georgia</option><option>North Carolina</option><option>Michigan</option><option>New Jersey</option><option>Virginia</option><option>Washington</option><option>Arizona</option><option>Massachusetts</option><option>Tennessee</option><option>Indiana</option><option>Missouri</option><option>Maryland</option><option>Wisconsin</option><option>Colorado</option><option>Minnesota</option><option>South Carolina</option><option>Alabama</option><option>Louisiana</option><option>Kentucky</option><option>Oregon</option><option>Oklahoma</option><option>Connecticut</option><option>Utah</option><option>Nevada</option><option>Arkansas</option><option>Mississippi</option><option>Kansas</option><option>New Mexico</option><option>Nebraska</option><option>West Virginia</option><option>Idaho</option><option>Hawaii</option><option>New Hampshire</option><option>Maine</option><option>Montana</option><option>Rhode Island</option><option>Delaware</option><option>South Dakota</option><option>North Dakota</option><option>Alaska</option><option>Vermont</option><option>Wyoming</option><option>Other</option>
          </select>
        </div>
        <select id="s3-license" style="border:1px solid #d1d5db;border-radius:7px;padding:8px 9px;font-size:0.82rem;background:#fff;width:100%;margin-bottom:10px">
          <option value="">License type</option><option>US License</option><option>Foreign License</option><option>Mexican License</option><option>International License</option><option>No License</option>
        </select>
        <button onclick="s3Submit()" style="width:100%;background:linear-gradient(135deg,#16a34a,#15803d);color:#fff;border:none;border-radius:9px;padding:12px;font-size:0.92rem;font-weight:700;cursor:pointer">{cfg["submit"]}</button>
        <div style="text-align:center;font-size:0.72rem;color:#9ca3af;margin-top:7px">{cfg["privacy"]}</div>
      </div>

      <div id="s3-step3" style="display:none;padding:12px 14px;border-top:1px solid #e5e7eb">
        <div style="display:flex;gap:8px">
          <input id="s3-chat" type="text" placeholder="{cfg["placeholder"]}" style="flex:1;border:1px solid #d1d5db;border-radius:8px;padding:10px 13px;font-size:0.88rem;outline:none" onkeydown="if(event.key===\'Enter\')s3Chat()">
          <button onclick="s3Chat()" style="background:#0f2944;color:#fff;border:none;border-radius:8px;padding:10px 16px;font-weight:700;cursor:pointer">&#8594;</button>
        </div>
      </div>
    </div>
  </div>
</div>
<script>
var s3Step=0,s3Name='',s3Phone='',s3Hist=[];
var S3SYS="{sys_escaped}";
function s3AddBot(t){{var m=document.getElementById('s3-msgs');var d=document.createElement('div');d.style.cssText='background:#fff;border-radius:12px 12px 12px 4px;padding:11px 14px;font-size:0.88rem;color:#374151;box-shadow:0 1px 3px rgba(0,0,0,0.07);max-width:88%;line-height:1.55';d.textContent=t;m.appendChild(d);m.scrollTop=m.scrollHeight;}}
function s3AddUser(t){{var m=document.getElementById('s3-msgs');var d=document.createElement('div');d.style.cssText='background:#0f2944;color:#fff;border-radius:12px 12px 4px 12px;padding:10px 13px;font-size:0.88rem;max-width:85%;align-self:flex-end;margin-left:auto;line-height:1.5';d.textContent=t;m.appendChild(d);m.scrollTop=m.scrollHeight;}}
function s3Send(){{var i=document.getElementById('s3-input');var v=i.value.trim();if(!v)return;i.value='';s3AddUser(v);if(s3Step===0){{s3Name=v;s3Step=1;setTimeout(()=>s3AddBot('{cfg["phone_q"]}'),300);}}else if(s3Step===1){{s3Phone=v;s3Step=2;setTimeout(()=>{{s3AddBot('{cfg["got_it"]}');document.getElementById('s3-step1').style.display='none';document.getElementById('s3-step2').style.display='block';}},300);}}}};
async function s3Submit(){{var year=document.getElementById('s3-year').value;var make=document.getElementById('s3-make').value;var state=document.getElementById('s3-state').value;var model=document.getElementById('s3-model').value;var license=document.getElementById('s3-license').value;if(!year||!make||!state){{alert('Please select year, make and state.');return;}}var lead={{name:s3Name,phone:s3Phone,year,make,model,state,license,url:window.location.href,time:new Date().toISOString()}};console.log('LEAD:',JSON.stringify(lead));document.getElementById('s3-step2').style.display='none';document.getElementById('s3-step3').style.display='block';s3Step=3;s3AddUser(year+' '+make+' — '+state);setTimeout(()=>s3AddBot('{cfg["thank_you"]}'),400);}}
async function s3Chat(){{var i=document.getElementById('s3-chat');var msg=i.value.trim();if(!msg)return;i.value='';s3AddUser(msg);s3Hist.push({{role:'user',content:msg}});try{{var r=await fetch('https://api.anthropic.com/v1/messages',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{model:'claude-haiku-4-5-20251001',max_tokens:150,system:S3SYS,messages:s3Hist}})}});var d=await r.json();var rep=d.content&&d.content[0]?d.content[0].text:'Please try again.';s3AddBot(rep);s3Hist.push({{role:'assistant',content:rep}});}}catch(e){{s3AddBot('Please try again.');}}}}
</script>'''


def get_lang_from_path(filepath):
    parts = filepath.replace('\\', '/').split('/')
    for p in parts:
        if p in LANGS and p != 'en':
            return p
    return 'en'


def fix_homepage(filepath, lang_code):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    original = content

    # 1. Remove ALL existing lang pills (both sets)
    content = re.sub(r'<div class="lang-bar">.*?</div>', '', content, flags=re.DOTALL)
    content = re.sub(r'<div class="lang-grid">.*?</div>', '', content, flags=re.DOTALL)

    # 2. Remove ALL existing Sarah hardcoded sections
    content = re.sub(r'<!-- Sarah Hardcoded Section -->.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<!-- Hardcoded Sarah -->.*?</script>', '', content, flags=re.DOTALL)

    # 3. Add lang CSS if not present
    if '.lang-pill' not in content:
        content = content.replace('</head>', LANG_CSS + '\n</head>', 1)

    # 4. Add clean lang pills in the hero (after the paragraph, before stats-bar or end of hero)
    pills = build_lang_pills(lang_code)
    # Insert pills before stats-bar
    content = re.sub(
        r'(<div class="stats-bar">)',
        pills + '\n\\1',
        content,
        count=1
    )

    # 5. Remove stats-bar (replace with nothing — lang pills are enough)
    content = re.sub(
        r'<div class="stats-bar">.*?</div>',
        '',
        content,
        flags=re.DOTALL,
        count=1
    )

    # 6. Inject correct language Sarah after hero
    sarah = build_sarah_section(lang_code)
    content = re.sub(
        r'(<div style="max-width:1200px;margin:40px auto)',
        sarah + '\n\\1',
        content,
        count=1
    )

    return content


# Process all homepage files
homepage_map = {
    'index.html': 'en',
    'es/index.html': 'es',
    'zh/index.html': 'zh',
    'ar/index.html': 'ar',
    'pt/index.html': 'pt',
    'ru/index.html': 'ru',
    'pl/index.html': 'pl',
    'vi/index.html': 'vi',
    'tl/index.html': 'tl',
    'ko/index.html': 'ko',
}

fixed = 0
for filepath, lang in homepage_map.items():
    try:
        content = fix_homepage(filepath, lang)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed += 1
        print(f"  Fixed [{lang}]: {filepath}")
    except FileNotFoundError:
        print(f"  Skipped (not found): {filepath}")
    except Exception as e:
        print(f"  Error {filepath}: {e}")

print(f"\nFixed {fixed} homepage files.")
