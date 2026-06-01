#!/usr/bin/env python3
"""
sarah_v3.py
- Opens automatically (no button)
- Short greeting, no immigration talk
- Asks name first in chat, then shows car form
- Removes top nav lang pills
- Minimal friction
"""

import re, glob

LANG_CONFIG = {
    'en': {
        'name': 'Sarah',
        'title': 'Car Insurance Specialist',
        'greeting': 'Hi, I am Sarah. I can help you find car insurance — no matter your situation. What is your full name?',
        'name_q': 'What is your full name?',
        'phone_q': 'And your phone number?',
        'car_title': 'Tell me about your vehicle',
        'placeholder': 'Type here...',
        'submit': 'Find My Insurance',
        'privacy': 'Your information is never shared with any government agency.',
        'system': 'You are Sarah, a car insurance specialist. Help the user get car insurance. Be brief and friendly. No more than 2 sentences per reply. Collect name, phone, then show vehicle form. Never mention ICE or immigration enforcement.',
    },
    'es': {
        'name': 'Sarah',
        'title': 'Especialista en Seguros',
        'greeting': 'Hola, soy Sarah. Le ayudo a encontrar seguro de auto — sin importar su situacion. Cual es su nombre completo?',
        'name_q': 'Cual es su nombre completo?',
        'phone_q': 'Y su numero de telefono?',
        'car_title': 'Cuenteme sobre su vehiculo',
        'placeholder': 'Escriba aqui...',
        'submit': 'Encontrar Mi Seguro',
        'privacy': 'Su informacion nunca se comparte con ninguna agencia gubernamental.',
        'system': 'Eres Sarah, especialista en seguros de auto. Ayuda al usuario. Maximo 2 oraciones por respuesta. Recopila nombre, telefono, luego muestra formulario del vehiculo.',
    },
    'zh': {
        'name': 'Sarah',
        'title': '汽车保险专家',
        'greeting': '您好，我是Sarah。无论您的情况如何，我都可以帮您找到汽车保险。请问您的全名是什么？',
        'name_q': '请问您的全名？',
        'phone_q': '您的电话号码？',
        'car_title': '告诉我您的车辆信息',
        'placeholder': '在此输入...',
        'submit': '找到我的保险',
        'privacy': '您的信息绝不会与任何政府机构共享。',
        'system': '你是Sarah，汽车保险专家。帮助用户。每次回复不超过2句话。收集姓名、电话，然后显示车辆表单。',
    },
    'ar': {
        'name': 'سارة',
        'title': 'متخصصة تامين السيارات',
        'greeting': 'مرحبا، انا سارة. يمكنني مساعدتك في ايجاد تامين سيارة — بغض النظر عن وضعك. ما اسمك الكامل؟',
        'name_q': 'ما اسمك الكامل؟',
        'phone_q': 'ورقم هاتفك؟',
        'car_title': 'اخبرني عن سيارتك',
        'placeholder': 'اكتب هنا...',
        'submit': 'ابحث عن تاميني',
        'privacy': 'معلوماتك لن تشارك مع اي جهة حكومية.',
        'system': 'انت سارة، متخصصة تامين سيارات. ساعد المستخدم. جملتان كحد اقصى. اجمع الاسم والهاتف ثم اعرض نموذج السيارة.',
    },
    'pt': {
        'name': 'Sarah',
        'title': 'Especialista em Seguros',
        'greeting': 'Ola, sou a Sarah. Posso ajuda-lo a encontrar seguro de carro — independentemente da sua situacao. Qual e o seu nome completo?',
        'name_q': 'Qual e o seu nome completo?',
        'phone_q': 'E o seu numero de telefone?',
        'car_title': 'Fale sobre o seu veiculo',
        'placeholder': 'Digite aqui...',
        'submit': 'Encontrar Meu Seguro',
        'privacy': 'Suas informacoes nunca sao compartilhadas com nenhuma agencia governamental.',
        'system': 'Voce e Sarah, especialista em seguros de auto. Ajude o usuario. Maximo 2 frases por resposta.',
    },
    'ru': {
        'name': 'Сара',
        'title': 'Специалист по страхованию',
        'greeting': 'Здравствуйте, я Сара. Я помогу вам найти автостраховку — независимо от вашей ситуации. Как вас зовут?',
        'name_q': 'Как вас зовут?',
        'phone_q': 'Ваш номер телефона?',
        'car_title': 'Расскажите о вашем автомобиле',
        'placeholder': 'Введите здесь...',
        'submit': 'Найти страховку',
        'privacy': 'Ваши данные никогда не передаются государственным органам.',
        'system': 'Вы Сара, специалист по автострахованию. Помогите пользователю. Максимум 2 предложения.',
    },
    'pl': {
        'name': 'Sarah',
        'title': 'Specjalista ds. ubezpieczen',
        'greeting': 'Czesc, jestem Sarah. Moge pomoc ci znalezc ubezpieczenie samochodu — bez wzgledu na twoja sytuacje. Jak masz na imie?',
        'name_q': 'Jak masz na imie?',
        'phone_q': 'Twoj numer telefonu?',
        'car_title': 'Opowiedz mi o swoim samochodzie',
        'placeholder': 'Wpisz tutaj...',
        'submit': 'Znajdz moje ubezpieczenie',
        'privacy': 'Twoje dane nigdy nie sa udostepniane zadnej agencji rzadowej.',
        'system': 'Jestes Sarah, specjalista ds. ubezpieczen samochodowych. Pomoz uzytkownikowi. Maksymalnie 2 zdania.',
    },
}

for lang in ['vi', 'tl', 'ko']:
    LANG_CONFIG[lang] = LANG_CONFIG['en'].copy()

US_STATES = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming']
CAR_MAKES = ['Acura','Audi','BMW','Buick','Cadillac','Chevrolet','Chrysler','Dodge','Ford','GMC','Honda','Hyundai','Infiniti','Jeep','Kia','Lexus','Lincoln','Mazda','Mercedes-Benz','Mitsubishi','Nissan','Ram','Subaru','Tesla','Toyota','Volkswagen','Volvo','Other']

def get_lang(filepath):
    parts = filepath.replace('\\','/').split('/')
    for p in parts:
        if p in LANG_CONFIG and p != 'en':
            return p
    return 'en'

def build_sarah(lang_code):
    cfg = LANG_CONFIG.get(lang_code, LANG_CONFIG['en'])
    is_rtl = lang_code == 'ar'
    dir_attr = 'rtl' if is_rtl else 'ltr'
    
    state_opts = ''.join(f'<option value="{s}">{s}</option>' for s in US_STATES)
    make_opts = ''.join(f'<option value="{m}">{m}</option>' for m in CAR_MAKES)
    years = list(range(2026, 1989, -1))
    year_opts = ''.join(f'<option value="{y}">{y}</option>' for y in years)
    license_opts = '<option value="">License type</option><option>US License</option><option>Foreign License</option><option>Mexican License</option><option>International License</option><option>No License</option>'
    
    sys_escaped = cfg['system'].replace('"',"'")
    
    return f'''
<!-- Sarah V3 -->
<style>
#sarah-wrap {{
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9999;
  width: 340px;
  max-width: calc(100vw - 32px);
  font-family: system-ui, -apple-system, sans-serif;
  direction: {dir_attr};
}}
#sarah-panel {{
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 8px 40px rgba(0,0,0,0.2);
  overflow: hidden;
  animation: sarahSlide 0.3s ease;
}}
@keyframes sarahSlide {{
  from {{ opacity:0; transform: translateY(20px); }}
  to {{ opacity:1; transform: translateY(0); }}
}}
.sarah-hdr {{
  background: linear-gradient(135deg, #0f2944, #1a4a7a);
  padding: 14px 18px;
  display: flex;
  align-items: center;
  gap: 12px;
}}
.sarah-msgs {{
  background: #f8fafc;
  padding: 14px;
  min-height: 70px;
  max-height: 180px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}}
.sarah-bot-msg {{
  background: #fff;
  border-radius: 12px 12px 12px 4px;
  padding: 10px 14px;
  font-size: 0.88rem;
  color: #374151;
  box-shadow: 0 1px 3px rgba(0,0,0,0.08);
  max-width: 92%;
  line-height: 1.5;
}}
.sarah-user-msg {{
  background: #0f2944;
  color: #fff;
  border-radius: 12px 12px 4px 12px;
  padding: 9px 13px;
  font-size: 0.88rem;
  max-width: 85%;
  align-self: flex-end;
  margin-left: auto;
  line-height: 1.5;
}}
.sarah-input-row {{
  padding: 10px 12px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 8px;
}}
.sarah-input-row input {{
  flex: 1;
  border: 1px solid #d1d5db;
  border-radius: 8px;
  padding: 9px 12px;
  font-size: 0.88rem;
  outline: none;
}}
.sarah-input-row button {{
  background: #f59e0b;
  color: #fff;
  border: none;
  border-radius: 8px;
  padding: 9px 16px;
  font-weight: 700;
  cursor: pointer;
  font-size: 0.9rem;
}}
.sarah-form {{
  padding: 12px 14px;
  border-top: 1px solid #e5e7eb;
}}
.sarah-form-title {{
  font-weight: 700;
  color: #0f2944;
  font-size: 0.88rem;
  margin-bottom: 10px;
}}
.sarah-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 7px;
  margin-bottom: 7px;
}}
.sarah-grid select, .sarah-grid input {{
  border: 1px solid #d1d5db;
  border-radius: 7px;
  padding: 8px 9px;
  font-size: 0.82rem;
  background: #fff;
  width: 100%;
  color: #374151;
}}
.sarah-submit {{
  width: 100%;
  background: linear-gradient(135deg, #16a34a, #15803d);
  color: #fff;
  border: none;
  border-radius: 9px;
  padding: 11px;
  font-size: 0.9rem;
  font-weight: 700;
  cursor: pointer;
  margin-top: 8px;
}}
.sarah-privacy {{
  font-size: 0.72rem;
  color: #9ca3af;
  text-align: center;
  margin-top: 6px;
}}
#sarah-minimize {{
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 9999;
  background: linear-gradient(135deg, #0f2944, #1a4a7a);
  color: #fff;
  border: none;
  border-radius: 30px;
  padding: 12px 20px;
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 16px rgba(0,0,0,0.2);
  display: none;
}}
</style>

<div id="sarah-wrap">
  <div id="sarah-panel">
    <div class="sarah-hdr">
      <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=80&h=80&fit=crop&crop=face"
           alt="Sarah" style="width:44px;height:44px;border-radius:50%;object-fit:cover;border:2px solid rgba(255,255,255,0.3);flex-shrink:0"
           onerror="this.style.display='none'">
      <div style="flex:1">
        <div style="color:#fff;font-weight:700;font-size:0.95rem">{cfg["name"]}</div>
        <div style="color:rgba(255,255,255,0.7);font-size:0.75rem">{cfg["title"]}</div>
        <div style="display:flex;align-items:center;gap:5px;margin-top:2px">
          <div style="width:6px;height:6px;background:#22c55e;border-radius:50%"></div>
          <span style="color:rgba(255,255,255,0.65);font-size:0.7rem">Online</span>
        </div>
      </div>
      <button onclick="sarahClose()" style="background:none;border:none;color:rgba(255,255,255,0.6);font-size:1.2rem;cursor:pointer;padding:2px 6px">—</button>
    </div>

    <div class="sarah-msgs" id="sarah-msgs">
      <div class="sarah-bot-msg">{cfg["greeting"]}</div>
    </div>

    <!-- Text input (shown first) -->
    <div class="sarah-input-row" id="sarah-text-row">
      <input id="sarah-input" type="text" placeholder="{cfg["placeholder"]}"
        onkeydown="if(event.key==='Enter')sarahSend()">
      <button onclick="sarahSend()">&#8594;</button>
    </div>

    <!-- Car form (shown after name + phone collected) -->
    <div class="sarah-form" id="sarah-car-form" style="display:none">
      <div class="sarah-form-title">{cfg["car_title"]}</div>
      <div class="sarah-grid">
        <select id="s-year"><option value="">Year</option>{year_opts}</select>
        <select id="s-make"><option value="">Make</option>{make_opts}</select>
      </div>
      <div class="sarah-grid">
        <input id="s-model" type="text" placeholder="Model">
        <select id="s-state"><option value="">State</option>{state_opts}</select>
      </div>
      <div class="sarah-grid">
        <select id="s-license">{license_opts}</select>
        <div></div>
      </div>
      <button class="sarah-submit" onclick="sarahFormSubmit()">{cfg["submit"]}</button>
      <div class="sarah-privacy">{cfg["privacy"]}</div>
    </div>
  </div>
</div>

<button id="sarah-minimize" onclick="sarahOpen()">Chat with {cfg["name"]} &rarr;</button>

<script>
var SARAH_SYS = "{sys_escaped}";
var sarahHistory = [];
var sarahStep = 0; // 0=name, 1=phone, 2=car form, 3=chat
var sarahName = '';
var sarahPhone = '';

function sarahClose() {{
  document.getElementById('sarah-wrap').style.display = 'none';
  document.getElementById('sarah-minimize').style.display = 'block';
}}
function sarahOpen() {{
  document.getElementById('sarah-wrap').style.display = 'block';
  document.getElementById('sarah-minimize').style.display = 'none';
}}

function addBot(text) {{
  var msgs = document.getElementById('sarah-msgs');
  var d = document.createElement('div');
  d.className = 'sarah-bot-msg';
  d.textContent = text;
  msgs.appendChild(d);
  msgs.scrollTop = msgs.scrollHeight;
}}

function addUser(text) {{
  var msgs = document.getElementById('sarah-msgs');
  var d = document.createElement('div');
  d.className = 'sarah-user-msg';
  d.textContent = text;
  msgs.appendChild(d);
  msgs.scrollTop = msgs.scrollHeight;
}}

function sarahSend() {{
  var input = document.getElementById('sarah-input');
  var val = input.value.trim();
  if (!val) return;
  input.value = '';
  addUser(val);

  if (sarahStep === 0) {{
    sarahName = val;
    sarahStep = 1;
    setTimeout(() => addBot('{cfg["phone_q"]}'), 300);
  }} else if (sarahStep === 1) {{
    sarahPhone = val;
    sarahStep = 2;
    setTimeout(() => {{
      addBot('Got it. Now tell me about your vehicle.');
      document.getElementById('sarah-text-row').style.display = 'none';
      document.getElementById('sarah-car-form').style.display = 'block';
    }}, 300);
  }} else {{
    sarahHistory.push({{role:'user', content:val}});
    sarahAI(val);
  }}
}}

async function sarahAI(msg) {{
  var typing = document.createElement('div');
  typing.className = 'sarah-bot-msg';
  typing.id = 'sarah-typing';
  typing.textContent = '...';
  typing.style.color = '#9ca3af';
  document.getElementById('sarah-msgs').appendChild(typing);
  document.getElementById('sarah-msgs').scrollTop = 9999;
  try {{
    var res = await fetch('https://api.anthropic.com/v1/messages', {{
      method: 'POST',
      headers: {{'Content-Type':'application/json'}},
      body: JSON.stringify({{
        model: 'claude-haiku-4-5-20251001',
        max_tokens: 150,
        system: SARAH_SYS,
        messages: sarahHistory
      }})
    }});
    var data = await res.json();
    var reply = data.content && data.content[0] ? data.content[0].text : 'Please try again.';
    var t = document.getElementById('sarah-typing');
    if(t) t.remove();
    addBot(reply);
    sarahHistory.push({{role:'assistant',content:reply}});
  }} catch(e) {{
    var t = document.getElementById('sarah-typing');
    if(t) t.remove();
    addBot('Please try again.');
  }}
}}

async function sarahFormSubmit() {{
  var year = document.getElementById('s-year').value;
  var make = document.getElementById('s-make').value;
  var model = document.getElementById('s-model').value;
  var state = document.getElementById('s-state').value;
  var license = document.getElementById('s-license').value;
  if (!year || !make || !state) {{
    alert('Please select year, make and state.');
    return;
  }}
  var lead = {{name:sarahName, phone:sarahPhone, year, make, model, state, license, url:window.location.href, time:new Date().toISOString()}};
  console.log('LEAD CAPTURED:', JSON.stringify(lead));
  
  document.getElementById('sarah-car-form').style.display = 'none';
  document.getElementById('sarah-text-row').style.display = 'flex';
  sarahStep = 3;
  
  var summary = sarahName + ', ' + year + ' ' + make + ' ' + (model||'') + ' in ' + state + ', ' + (license||'');
  sarahHistory.push({{role:'user', content:'My details: ' + summary}});
  addUser(year + ' ' + make + ' — ' + state);
  
  await sarahAI('User submitted: ' + summary + '. Confirm you received it and let them know a specialist will be in touch.');
}}
</script>'''


def fix_nav_pills(content):
    """Remove top nav language pills — keep only the ones in the hero."""
    # Remove lang-switcher from header
    content = re.sub(
        r'<div class="lang-switcher">.*?</div>',
        '',
        content,
        flags=re.DOTALL
    )
    return content


files = [f for f in glob.glob('**/*.html', recursive=True) if not f.startswith('.')]
print(f"Processing {len(files)} files...")
updated = 0

for filepath in files:
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original = content
        
        # Remove old Sarah
        content = re.sub(r'<!-- Sarah.*?</script>\s*', '', content, flags=re.DOTALL)
        content = re.sub(r'<!-- Sarah Widget.*?</script>\s*', '', content, flags=re.DOTALL)
        content = re.sub(r'<!-- Sarah V[0-9].*?</script>\s*', '', content, flags=re.DOTALL)
        content = re.sub(r'<style>\s*#sarah-wrap.*?</style>\s*', '', content, flags=re.DOTALL)
        
        # Remove top nav lang switcher
        content = fix_nav_pills(content)
        
        # Add new Sarah
        lang = get_lang(filepath)
        content = content.replace('</body>', build_sarah(lang) + '\n</body>')
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            updated += 1
    except Exception as e:
        print(f"  Error {filepath}: {e}")

print(f"Updated {updated} files.")
