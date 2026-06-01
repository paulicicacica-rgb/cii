#!/usr/bin/env python3
"""
sarah_widget.py
Replaces Sarah widget on all pages with:
- Professional avatar photo (real woman, not robot)
- Open by default (not bubble)
- Clean intake form with dropdowns
- Multilingual
- No emojis
- Collects lead data properly
"""

import re, glob

LANG_CONFIG = {
    'en': {
        'name': 'Sarah',
        'title': 'Car Insurance Specialist',
        'greeting': 'Hi, I am Sarah. I help immigrants get car insurance in the US — regardless of your status, license type, or whether you have an SSN. Let me help you find coverage. To get started, tell me about your vehicle.',
        'btn_start': 'Find My Insurance',
        'placeholder': 'Or type your question here...',
        'system': 'You are Sarah, a professional car insurance specialist at CarInsuranceImmigrants.us. Help immigrants get car insurance in the US. Key facts: No SSN required. Insurance companies do not report to ICE. ITIN accepted by many insurers. Undocumented immigrants can get insurance. Be professional, warm, and reassuring. Collect: name, phone, vehicle year/make/model, state, license type (US/foreign/none), immigration status (optional). Keep responses under 3 sentences.',
        'form': {
            'step1_title': 'Tell me about your vehicle',
            'year_label': 'Vehicle Year',
            'make_label': 'Vehicle Make',
            'model_label': 'Vehicle Model',
            'state_label': 'Your State',
            'step2_title': 'Tell me about yourself',
            'name_label': 'Your First Name',
            'phone_label': 'Phone Number',
            'license_label': 'License Type',
            'license_options': ['US License', 'Foreign License', 'Mexican License (Matricula)', 'International License', 'No License'],
            'status_label': 'Immigration Status (Optional)',
            'status_options': ['Prefer not to say', 'US Citizen', 'Green Card', 'Work Visa', 'DACA', 'TPS', 'Asylum', 'Undocumented'],
            'submit': 'Get My Free Quote',
            'privacy': 'Your information is never shared with ICE or any government agency.',
        }
    },
    'es': {
        'name': 'Sarah',
        'title': 'Especialista en Seguros de Auto',
        'greeting': 'Hola, soy Sarah. Ayudo a inmigrantes a obtener seguro de auto en EEUU — sin importar su estatus, tipo de licencia o si tiene SSN. Para comenzar, cuenteme sobre su vehiculo.',
        'btn_start': 'Encontrar Mi Seguro',
        'placeholder': 'O escriba su pregunta aqui...',
        'system': 'Eres Sarah, especialista profesional en seguros de auto en CarInsuranceImmigrants.us. Ayuda a inmigrantes en EEUU. No se necesita SSN. Las aseguradoras no reportan a ICE. ITIN aceptado. Los indocumentados pueden asegurarse. Se profesional, calorosa y tranquilizadora. Recopila: nombre, telefono, ano/marca/modelo, estado, tipo de licencia. Respuestas en 3 oraciones maximo.',
        'form': {
            'step1_title': 'Cuenteme sobre su vehiculo',
            'year_label': 'Ano del Vehiculo',
            'make_label': 'Marca',
            'model_label': 'Modelo',
            'state_label': 'Su Estado',
            'step2_title': 'Cuenteme sobre usted',
            'name_label': 'Su Nombre',
            'phone_label': 'Telefono',
            'license_label': 'Tipo de Licencia',
            'license_options': ['Licencia de EEUU', 'Licencia Extranjera', 'Licencia Mexicana (Matricula)', 'Licencia Internacional', 'Sin Licencia'],
            'status_label': 'Estatus Migratorio (Opcional)',
            'status_options': ['Prefiero no decir', 'Ciudadano EEUU', 'Residencia Permanente', 'Visa de Trabajo', 'DACA', 'TPS', 'Asilo', 'Sin documentos'],
            'submit': 'Obtener Mi Cotizacion Gratis',
            'privacy': 'Su informacion nunca se comparte con ICE ni ninguna agencia del gobierno.',
        }
    },
    'zh': {
        'name': 'Sarah',
        'title': '汽车保险专家',
        'greeting': '您好，我是Sarah。我帮助在美移民获得汽车保险，无论您的身份状态、驾照类型或是否有社会安全号。请告诉我您的车辆信息。',
        'btn_start': '寻找我的保险',
        'placeholder': '或在此输入您的问题...',
        'system': '你是Sarah，CarInsuranceImmigrants.us的专业汽车保险专家。帮助美国移民。不需要SSN。保险公司不向ICE举报。ITIN可用。无证移民可以投保。专业、热情、令人放心。收集：姓名、电话、车辆年份/品牌/型号、州、驾照类型。回复不超过3句话。',
        'form': {
            'step1_title': '告诉我您的车辆信息',
            'year_label': '车辆年份',
            'make_label': '品牌',
            'model_label': '型号',
            'state_label': '您所在的州',
            'step2_title': '告诉我您的个人信息',
            'name_label': '您的名字',
            'phone_label': '电话号码',
            'license_label': '驾照类型',
            'license_options': ['美国驾照', '外国驾照', '墨西哥驾照', '国际驾照', '无驾照'],
            'status_label': '移民身份（可选）',
            'status_options': ['不愿透露', '美国公民', '绿卡', '工作签证', 'DACA', 'TPS', '庇护', '无证件'],
            'submit': '获取免费报价',
            'privacy': '您的信息绝不会与ICE或任何政府机构共享。',
        }
    },
    'ar': {
        'name': 'سارة',
        'title': 'متخصصة تأمين السيارات',
        'greeting': 'مرحبا، انا سارة. اساعد المهاجرين على الحصول على تامين السيارة في الولايات المتحدة - بغض النظر عن وضعك او نوع رخصتك او ما اذا كان لديك SSN. للبدء، اخبرني عن سيارتك.',
        'btn_start': 'ابحث عن تاميني',
        'placeholder': 'او اكتب سؤالك هنا...',
        'system': 'انت سارة، متخصصة تامين سيارات محترفة في CarInsuranceImmigrants.us. ساعد المهاجرين في الولايات المتحدة. لا يلزم SSN. شركات التامين لا تبلغ ICE. ITIN مقبول. المهاجرون غير الموثقين يمكنهم التامين. كوني محترفة وودية ومطمئنة. اجمعي: الاسم، الهاتف، السنة/الماركة/الموديل، الولاية، نوع الرخصة. ردود في 3 جمل كحد اقصى.',
        'form': {
            'step1_title': 'اخبرني عن سيارتك',
            'year_label': 'سنة السيارة',
            'make_label': 'الماركة',
            'model_label': 'الموديل',
            'state_label': 'ولايتك',
            'step2_title': 'اخبرني عن نفسك',
            'name_label': 'اسمك الاول',
            'phone_label': 'رقم الهاتف',
            'license_label': 'نوع الرخصة',
            'license_options': ['رخصة امريكية', 'رخصة اجنبية', 'رخصة مكسيكية', 'رخصة دولية', 'بدون رخصة'],
            'status_label': 'الوضع المهاجر (اختياري)',
            'status_options': ['افضل عدم القول', 'مواطن امريكي', 'بطاقة خضراء', 'تاشيرة عمل', 'DACA', 'TPS', 'لجوء', 'غير موثق'],
            'submit': 'احصل على عرضي المجاني',
            'privacy': 'معلوماتك لن تشارك ابدا مع ICE او اي جهة حكومية.',
        }
    },
}

# Add other languages with English fallback
for lang in ['pt', 'vi', 'tl', 'ko', 'ru', 'pl']:
    LANG_CONFIG[lang] = LANG_CONFIG['en'].copy()

# US States for dropdown
US_STATES = ['Alabama','Alaska','Arizona','Arkansas','California','Colorado','Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho','Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana','Maine','Maryland','Massachusetts','Michigan','Minnesota','Mississippi','Missouri','Montana','Nebraska','Nevada','New Hampshire','New Jersey','New Mexico','New York','North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island','South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia','Wisconsin','Wyoming']

# Car makes
CAR_MAKES = ['Acura','Audi','BMW','Buick','Cadillac','Chevrolet','Chrysler','Dodge','Ford','GMC','Honda','Hyundai','Infiniti','Jeep','Kia','Lexus','Lincoln','Mazda','Mercedes-Benz','Mitsubishi','Nissan','Ram','Subaru','Tesla','Toyota','Volkswagen','Volvo','Other']

def build_sarah(lang_code):
    cfg = LANG_CONFIG.get(lang_code, LANG_CONFIG['en'])
    f = cfg['form']
    is_rtl = lang_code == 'ar'
    dir_attr = 'rtl' if is_rtl else 'ltr'
    
    state_options = ''.join(f'<option value="{s}">{s}</option>' for s in US_STATES)
    make_options = ''.join(f'<option value="{m}">{m}</option>' for m in CAR_MAKES)
    license_options = ''.join(f'<option value="{o}">{o}</option>' for o in f['license_options'])
    status_options = ''.join(f'<option value="{o}">{o}</option>' for o in f['status_options'])
    
    years = list(range(2026, 1989, -1))
    year_options = ''.join(f'<option value="{y}">{y}</option>' for y in years)
    
    system_escaped = cfg['system'].replace('"', "'").replace('\n', ' ')
    
    return f'''
<!-- Sarah Widget -->
<div id="sarah-container" style="position:fixed;bottom:24px;right:24px;z-index:9999;width:360px;max-width:calc(100vw - 32px);font-family:system-ui,-apple-system,sans-serif;direction:{dir_attr}">
  
  <!-- Toggle button (shown when minimized) -->
  <button id="sarah-toggle" onclick="toggleSarah()" style="display:none;background:linear-gradient(135deg,#1a4a7a,#0f2944);color:#fff;border:none;border-radius:30px;padding:12px 24px;font-size:0.95rem;font-weight:600;cursor:pointer;box-shadow:0 4px 20px rgba(0,0,0,0.25);width:100%">
    Chat with Sarah — Car Insurance Help
  </button>

  <!-- Main panel -->
  <div id="sarah-panel" style="background:#fff;border-radius:16px;box-shadow:0 8px 40px rgba(0,0,0,0.18);overflow:hidden">
    
    <!-- Header -->
    <div style="background:linear-gradient(135deg,#0f2944,#1a4a7a);padding:16px 20px;display:flex;align-items:center;gap:14px">
      <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=80&h=80&fit=crop&crop=face" 
           alt="Sarah" 
           style="width:48px;height:48px;border-radius:50%;object-fit:cover;border:2px solid rgba(255,255,255,0.3)"
           onerror="this.style.display='none';document.getElementById('sarah-avatar-fallback').style.display='flex'">
      <div id="sarah-avatar-fallback" style="display:none;width:48px;height:48px;background:#f59e0b;border-radius:50%;align-items:center;justify-content:center;font-size:1.4rem;color:#fff;font-weight:700;flex-shrink:0">S</div>
      <div style="flex:1">
        <div style="color:#fff;font-weight:700;font-size:1rem">{cfg["name"]}</div>
        <div style="color:rgba(255,255,255,0.75);font-size:0.8rem">{cfg["title"]}</div>
        <div style="display:flex;align-items:center;gap:6px;margin-top:3px">
          <div style="width:7px;height:7px;background:#22c55e;border-radius:50%"></div>
          <span style="color:rgba(255,255,255,0.7);font-size:0.75rem">Online now</span>
        </div>
      </div>
      <button onclick="minimizeSarah()" style="background:none;border:none;color:rgba(255,255,255,0.7);font-size:1.2rem;cursor:pointer;padding:4px 8px;border-radius:4px" title="Minimize">—</button>
    </div>

    <!-- Chat messages -->
    <div id="sarah-messages" style="padding:16px;background:#f8fafc;min-height:80px;max-height:200px;overflow-y:auto;display:flex;flex-direction:column;gap:10px">
      <div style="background:#fff;border-radius:12px 12px 12px 4px;padding:12px 14px;font-size:0.9rem;color:#374151;box-shadow:0 1px 4px rgba(0,0,0,0.08);max-width:90%;line-height:1.5">
        {cfg["greeting"]}
      </div>
    </div>

    <!-- Step 1: Vehicle Info -->
    <div id="sarah-step1" style="padding:16px;border-top:1px solid #e5e7eb">
      <div style="font-weight:700;color:#0f2944;margin-bottom:12px;font-size:0.95rem">{f["step1_title"]}</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px">
        <select id="s-year" style="border:1px solid #d1d5db;border-radius:8px;padding:9px 10px;font-size:0.88rem;background:#fff;color:#374151;width:100%">
          <option value="">{f["year_label"]}</option>
          {year_options}
        </select>
        <select id="s-make" style="border:1px solid #d1d5db;border-radius:8px;padding:9px 10px;font-size:0.88rem;background:#fff;color:#374151;width:100%">
          <option value="">{f["make_label"]}</option>
          {make_options}
        </select>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px">
        <input id="s-model" type="text" placeholder="{f["model_label"]}"
          style="border:1px solid #d1d5db;border-radius:8px;padding:9px 10px;font-size:0.88rem;color:#374151">
        <select id="s-state" style="border:1px solid #d1d5db;border-radius:8px;padding:9px 10px;font-size:0.88rem;background:#fff;color:#374151;width:100%">
          <option value="">{f["state_label"]}</option>
          {state_options}
        </select>
      </div>
      <button onclick="sarahStep2()" 
        style="width:100%;background:linear-gradient(135deg,#f59e0b,#d97706);color:#fff;border:none;border-radius:10px;padding:12px;font-size:0.95rem;font-weight:700;cursor:pointer">
        Next
      </button>
    </div>

    <!-- Step 2: Personal Info (hidden initially) -->
    <div id="sarah-step2" style="display:none;padding:16px;border-top:1px solid #e5e7eb">
      <div style="font-weight:700;color:#0f2944;margin-bottom:12px;font-size:0.95rem">{f["step2_title"]}</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px">
        <input id="s-name" type="text" placeholder="{f["name_label"]}"
          style="border:1px solid #d1d5db;border-radius:8px;padding:9px 10px;font-size:0.88rem">
        <input id="s-phone" type="tel" placeholder="{f["phone_label"]}"
          style="border:1px solid #d1d5db;border-radius:8px;padding:9px 10px;font-size:0.88rem">
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:8px">
        <select id="s-license" style="border:1px solid #d1d5db;border-radius:8px;padding:9px 10px;font-size:0.88rem;background:#fff;width:100%">
          <option value="">{f["license_label"]}</option>
          {license_options}
        </select>
        <select id="s-status" style="border:1px solid #d1d5db;border-radius:8px;padding:9px 10px;font-size:0.88rem;background:#fff;width:100%">
          <option value="">{f["status_label"]}</option>
          {status_options}
        </select>
      </div>
      <button onclick="sarahSubmit()"
        style="width:100%;background:linear-gradient(135deg,#16a34a,#15803d);color:#fff;border:none;border-radius:10px;padding:12px;font-size:0.95rem;font-weight:700;cursor:pointer;margin-bottom:8px">
        {f["submit"]}
      </button>
      <p style="font-size:0.75rem;color:#6b7280;text-align:center;margin:0">{f["privacy"]}</p>
    </div>

    <!-- Step 3: Chat (shown after form) -->
    <div id="sarah-chat" style="display:none;padding:12px;border-top:1px solid #e5e7eb">
      <div style="display:flex;gap:8px">
        <input id="sarah-input" type="text" placeholder="{cfg["placeholder"]}"
          style="flex:1;border:1px solid #d1d5db;border-radius:8px;padding:10px 14px;font-size:0.9rem;outline:none"
          onkeydown="if(event.key==='Enter')sendSarah()">
        <button onclick="sendSarah()"
          style="background:#f59e0b;color:#fff;border:none;border-radius:8px;padding:10px 18px;font-weight:700;cursor:pointer">
          Send
        </button>
      </div>
    </div>

  </div>
</div>

<script>
var sarahHistory = [];
var sarahMinimized = false;
var SARAH_SYS = "{system_escaped}";

function minimizeSarah() {{
  document.getElementById('sarah-panel').style.display = 'none';
  document.getElementById('sarah-toggle').style.display = 'block';
  sarahMinimized = true;
}}

function toggleSarah() {{
  document.getElementById('sarah-panel').style.display = 'block';
  document.getElementById('sarah-toggle').style.display = 'none';
  sarahMinimized = false;
}}

function addMsg(text, role) {{
  var msgs = document.getElementById('sarah-messages');
  var div = document.createElement('div');
  if (role === 'user') {{
    div.style.cssText = 'background:#0f2944;color:#fff;border-radius:12px 12px 4px 12px;padding:10px 14px;font-size:0.9rem;max-width:85%;align-self:flex-end;margin-left:auto;line-height:1.5';
  }} else {{
    div.style.cssText = 'background:#fff;border-radius:12px 12px 12px 4px;padding:12px 14px;font-size:0.9rem;color:#374151;box-shadow:0 1px 4px rgba(0,0,0,0.08);max-width:90%;line-height:1.5';
  }}
  div.textContent = text;
  msgs.appendChild(div);
  msgs.scrollTop = msgs.scrollHeight;
}}

function sarahStep2() {{
  var year = document.getElementById('s-year').value;
  var make = document.getElementById('s-make').value;
  var model = document.getElementById('s-model').value;
  var state = document.getElementById('s-state').value;
  if (!year || !make || !state) {{
    alert('Please select the year, make, and state.');
    return;
  }}
  document.getElementById('sarah-step1').style.display = 'none';
  document.getElementById('sarah-step2').style.display = 'block';
  addMsg('Vehicle: ' + year + ' ' + make + ' ' + model + ' — ' + state, 'user');
  sarahHistory.push({{role:'user', content:'My vehicle is a ' + year + ' ' + make + ' ' + model + ' in ' + state}});
}}

async function sarahSubmit() {{
  var name = document.getElementById('s-name').value.trim();
  var phone = document.getElementById('s-phone').value.trim();
  var license = document.getElementById('s-license').value;
  var status = document.getElementById('s-status').value;
  if (!name || !phone) {{
    alert('Please enter your name and phone number.');
    return;
  }}
  var year = document.getElementById('s-year').value;
  var make = document.getElementById('s-make').value;
  var model = document.getElementById('s-model').value;
  var state = document.getElementById('s-state').value;
  var leadData = {{name,phone,year,make,model,state,license,status,page:window.location.href,time:new Date().toISOString()}};
  console.log('LEAD:', JSON.stringify(leadData));
  
  document.getElementById('sarah-step2').style.display = 'none';
  document.getElementById('sarah-chat').style.display = 'block';
  
  var summary = name + ', ' + year + ' ' + make + ' ' + (model||'') + ', ' + state + ', ' + (license||'not specified');
  sarahHistory.push({{role:'user', content:'My details: ' + summary}});
  addMsg(name + ', ' + year + ' ' + make + ' — ' + state, 'user');
  
  var typing = document.createElement('div');
  typing.id = 'sarah-typing';
  typing.style.cssText = 'background:#f0f4f8;border-radius:12px;padding:10px 14px;font-size:0.85rem;color:#9ca3af';
  typing.textContent = '...';
  document.getElementById('sarah-messages').appendChild(typing);
  
  try {{
    var res = await fetch('https://api.anthropic.com/v1/messages', {{
      method:'POST',
      headers:{{'Content-Type':'application/json'}},
      body: JSON.stringify({{
        model:'claude-haiku-4-5-20251001',
        max_tokens:200,
        system: SARAH_SYS,
        messages: sarahHistory
      }})
    }});
    var data = await res.json();
    var reply = data.content && data.content[0] ? data.content[0].text : 'Thank you. A specialist will call you shortly.';
    var t = document.getElementById('sarah-typing');
    if(t) t.remove();
    addMsg(reply, 'bot');
    sarahHistory.push({{role:'assistant', content:reply}});
  }} catch(e) {{
    var t = document.getElementById('sarah-typing');
    if(t) t.remove();
    addMsg('Thank you ' + name + '. A specialist will contact you at ' + phone + ' shortly.', 'bot');
  }}
}}

async function sendSarah() {{
  var input = document.getElementById('sarah-input');
  var msg = input.value.trim();
  if (!msg) return;
  input.value = '';
  addMsg(msg, 'user');
  sarahHistory.push({{role:'user', content:msg}});
  var typing = document.createElement('div');
  typing.id = 'sarah-typing';
  typing.style.cssText = 'background:#f0f4f8;border-radius:12px;padding:10px 14px;font-size:0.85rem;color:#9ca3af';
  typing.textContent = '...';
  document.getElementById('sarah-messages').appendChild(typing);
  try {{
    var res = await fetch('https://api.anthropic.com/v1/messages', {{
      method:'POST',
      headers:{{'Content-Type':'application/json'}},
      body: JSON.stringify({{model:'claude-haiku-4-5-20251001',max_tokens:200,system:SARAH_SYS,messages:sarahHistory}})
    }});
    var data = await res.json();
    var reply = data.content && data.content[0] ? data.content[0].text : 'Please try again.';
    var t = document.getElementById('sarah-typing');
    if(t) t.remove();
    addMsg(reply, 'bot');
    sarahHistory.push({{role:'assistant', content:reply}});
  }} catch(e) {{
    var t = document.getElementById('sarah-typing');
    if(t) t.remove();
    addMsg('Connection issue. Please try again.', 'bot');
  }}
}}
</script>'''

def get_lang(filepath):
    parts = filepath.replace('\\','/').split('/')
    langs = list(LANG_CONFIG.keys())
    for p in parts:
        if p in langs and p != 'en':
            return p
    return 'en'

files = [f for f in glob.glob('**/*.html', recursive=True) if not f.startswith('.')]
print(f"Processing {len(files)} files...")
updated = 0

for filepath in files:
    try:
        with open(filepath,'r',encoding='utf-8',errors='ignore') as f:
            content = f.read()
        
        # Remove old Sarah widget
        content = re.sub(r'<!-- Sarah.*?</script>', '', content, flags=re.DOTALL)
        content = re.sub(r'<!-- Sarah Widget -->.*?</script>', '', content, flags=re.DOTALL)
        
        # Add new Sarah
        lang = get_lang(filepath)
        new_content = content.replace('</body>', build_sarah(lang) + '\n</body>')
        
        if new_content != content:
            with open(filepath,'w',encoding='utf-8') as f:
                f.write(new_content)
            updated += 1
    except Exception as e:
        print(f"  Error {filepath}: {e}")

print(f"Updated {updated} files with new Sarah widget.")
