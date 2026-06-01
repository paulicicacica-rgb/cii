#!/usr/bin/env python3
"""
FINAL_FIX.py — The last fix script.
Fixes exactly what's broken based on repo audit:
1. Add lang pills HTML to English homepage (CSS exists, HTML missing)
2. Add hardcoded Sarah to all language homepages
3. Sarah on inner pages - make panel visible by default
4. Remove lang-switcher HTML from all pages (CSS stays, HTML nav removed)
"""

import re, glob

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

LANG_PILLS = {
    'es': LANG_PILLS_EN.replace('class="lang-pill active">English', 'class="lang-pill">English').replace('class="lang-pill">Español', 'class="lang-pill active">Español'),
    'zh': LANG_PILLS_EN.replace('class="lang-pill active">English', 'class="lang-pill">English').replace('class="lang-pill">中文', 'class="lang-pill active">中文'),
    'ar': LANG_PILLS_EN.replace('class="lang-pill active">English', 'class="lang-pill">English').replace('class="lang-pill">العربية', 'class="lang-pill active">العربية'),
    'pt': LANG_PILLS_EN.replace('class="lang-pill active">English', 'class="lang-pill">English').replace('class="lang-pill">Português', 'class="lang-pill active">Português'),
    'vi': LANG_PILLS_EN.replace('class="lang-pill active">English', 'class="lang-pill">English').replace('class="lang-pill">Tiếng Việt', 'class="lang-pill active">Tiếng Việt'),
    'tl': LANG_PILLS_EN.replace('class="lang-pill active">English', 'class="lang-pill">English').replace('class="lang-pill">Filipino', 'class="lang-pill active">Filipino'),
    'ko': LANG_PILLS_EN.replace('class="lang-pill active">English', 'class="lang-pill">English').replace('class="lang-pill">한국어', 'class="lang-pill active">한국어'),
    'ru': LANG_PILLS_EN.replace('class="lang-pill active">English', 'class="lang-pill">English').replace('class="lang-pill">Русский', 'class="lang-pill active">Русский'),
    'pl': LANG_PILLS_EN.replace('class="lang-pill active">English', 'class="lang-pill">English').replace('class="lang-pill">Polski', 'class="lang-pill active">Polski'),
}

SARAH_LANGS = {
    'en': {'greeting': 'Hi, I am Sarah. I can help you find car insurance — no matter your situation. What is your full name?', 'phone': 'And your phone number?', 'gotit': 'Got it. Now tell me about your vehicle.', 'submit': 'Find My Insurance', 'privacy': 'Your information is never shared with any government agency.', 'cta': 'GET STARTED', 'h2': 'Tell Sarah about your situation.<br>She will find you the right coverage.', 'sub': 'Free · No obligation · No SSN required', 'specialist': 'Car Insurance Specialist', 'thanks': 'Thank you. A specialist will contact you shortly.', 'sys': 'You are Sarah, a professional car insurance specialist. Help the user get car insurance. Max 2 sentences. Never mention ICE.'},
    'es': {'greeting': 'Hola, soy Sarah. Puedo ayudarle a encontrar seguro de auto. Cual es su nombre completo?', 'phone': 'Y su numero de telefono?', 'gotit': 'Entendido. Ahora cuenteme sobre su vehiculo.', 'submit': 'Encontrar Mi Seguro', 'privacy': 'Su informacion nunca se comparte con ninguna agencia gubernamental.', 'cta': 'COMENZAR', 'h2': 'Cuentele a Sarah su situacion.<br>Ella encontrara la cobertura correcta.', 'sub': 'Gratis · Sin compromiso · Sin SSN', 'specialist': 'Especialista en Seguros', 'thanks': 'Gracias. Un especialista le contactara pronto.', 'sys': 'Eres Sarah, especialista en seguros de auto. Responde en espanol. Maximo 2 oraciones.'},
    'zh': {'greeting': '您好，我是Sarah。我可以帮您找到汽车保险。请问您的全名是什么？', 'phone': '您的电话号码？', 'gotit': '好的。现在告诉我您的车辆信息。', 'submit': '找到我的保险', 'privacy': '您的信息绝不会与任何政府机构共享。', 'cta': '开始', 'h2': '告诉Sarah您的情况。<br>她会为您找到合适的保险。', 'sub': '免费 · 无义务 · 不需要SSN', 'specialist': '汽车保险专家', 'thanks': '谢谢。专家将很快与您联系。', 'sys': '你是Sarah，汽车保险专家。用中文回答。最多2句话。'},
    'ar': {'greeting': 'مرحبا، انا سارة. يمكنني مساعدتك. ما اسمك الكامل؟', 'phone': 'ورقم هاتفك؟', 'gotit': 'حسنا. اخبرني عن سيارتك.', 'submit': 'ابحث عن تاميني', 'privacy': 'معلوماتك لن تشارك مع اي جهة حكومية.', 'cta': 'ابدا', 'h2': 'اخبر سارة عن وضعك.<br>ستجد لك التغطية المناسبة.', 'sub': 'مجاني · بدون التزام · بدون SSN', 'specialist': 'متخصصة تامين', 'thanks': 'شكرا. سيتواصل معك متخصص قريبا.', 'sys': 'انت سارة، متخصصة تامين سيارات. اجيبي بالعربية. جملتان.'},
    'pt': {'greeting': 'Ola, sou Sarah. Posso ajuda-lo a encontrar seguro. Qual e o seu nome?', 'phone': 'E o seu telefone?', 'gotit': 'Entendido. Fale sobre o seu veiculo.', 'submit': 'Encontrar Meu Seguro', 'privacy': 'Seus dados nunca sao compartilhados com nenhuma agencia.', 'cta': 'COMECAR', 'h2': 'Conte a Sarah sua situacao.<br>Ela encontrara a cobertura certa.', 'sub': 'Gratis · Sem compromisso · Sem SSN', 'specialist': 'Especialista em Seguros', 'thanks': 'Obrigado. Um especialista entrara em contato.', 'sys': 'Voce e Sarah, especialista em seguros. Responda em portugues. Maximo 2 frases.'},
    'ru': {'greeting': 'Здравствуйте, я Сара. Помогу найти автостраховку. Как вас зовут?', 'phone': 'Ваш номер телефона?', 'gotit': 'Понятно. Расскажите об автомобиле.', 'submit': 'Найти страховку', 'privacy': 'Ваши данные никогда не передаются государственным органам.', 'cta': 'НАЧАТЬ', 'h2': 'Расскажите Саре о вашей ситуации.<br>Она найдет подходящее покрытие.', 'sub': 'Бесплатно · Без обязательств · Без SSN', 'specialist': 'Специалист по страхованию', 'thanks': 'Спасибо. Специалист свяжется с вами.', 'sys': 'Вы Сара, специалист по автострахованию. Отвечайте по-русски. 2 предложения.'},
    'pl': {'greeting': 'Czesc, jestem Sarah. Moge pomoc znalezc ubezpieczenie. Jak masz na imie?', 'phone': 'Twoj numer telefonu?', 'gotit': 'Rozumiem. Opowiedz o samochodzie.', 'submit': 'Znajdz ubezpieczenie', 'privacy': 'Twoje dane nigdy nie sa udostepniane zadnej agencji.', 'cta': 'ZACZNIJ', 'h2': 'Opowiedz Sarah o swojej sytuacji.<br>Ona znajdzie odpowiednie ubezpieczenie.', 'sub': 'Bezplatnie · Bez zobowiazan · Bez SSN', 'specialist': 'Specjalista ds. ubezpieczen', 'thanks': 'Dziekuje. Specjalista skontaktuje sie wkrotce.', 'sys': 'Jestes Sarah, specjalista ubezpieczen. Odpowiadaj po polsku. 2 zdania.'},
}
for lang in ['vi','tl','ko']:
    SARAH_LANGS[lang] = SARAH_LANGS['en'].copy()

YEAR_OPTS = ''.join(f'<option>{y}</option>' for y in range(2026,1989,-1))
STATE_OPTS = '<option value="">State</option><option>California</option><option>Texas</option><option>Florida</option><option>New York</option><option>Illinois</option><option>Pennsylvania</option><option>Ohio</option><option>Georgia</option><option>North Carolina</option><option>Michigan</option><option>New Jersey</option><option>Virginia</option><option>Washington</option><option>Arizona</option><option>Massachusetts</option><option>Tennessee</option><option>Indiana</option><option>Missouri</option><option>Maryland</option><option>Wisconsin</option><option>Colorado</option><option>Minnesota</option><option>South Carolina</option><option>Alabama</option><option>Louisiana</option><option>Kentucky</option><option>Oregon</option><option>Oklahoma</option><option>Connecticut</option><option>Utah</option><option>Nevada</option><option>Arkansas</option><option>Mississippi</option><option>Kansas</option><option>New Mexico</option><option>Nebraska</option><option>West Virginia</option><option>Idaho</option><option>Hawaii</option><option>New Hampshire</option><option>Maine</option><option>Montana</option><option>Rhode Island</option><option>Delaware</option><option>South Dakota</option><option>North Dakota</option><option>Alaska</option><option>Vermont</option><option>Wyoming</option><option>Other</option>'

def build_inline_sarah(lang):
    c = SARAH_LANGS.get(lang, SARAH_LANGS['en'])
    sys_esc = c['sys'].replace('"',"'")
    return f'''<div style="background:#f7f9fc;padding:60px 24px 80px;text-align:center">
  <div style="max-width:480px;margin:0 auto">
    <p style="color:#f59e0b;font-size:0.78rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:12px">{c["cta"]}</p>
    <h2 style="font-size:clamp(1.5rem,4vw,2rem);font-weight:800;color:#0f2944;line-height:1.3;margin-bottom:10px">{c["h2"]}</h2>
    <p style="color:#6b7280;font-size:0.9rem;margin-bottom:28px">{c["sub"]}</p>
    <div style="background:#fff;border-radius:16px;box-shadow:0 8px 40px rgba(0,0,0,0.12);overflow:hidden;text-align:left">
      <div style="background:linear-gradient(135deg,#0f2944,#1a4a7a);padding:14px 18px;display:flex;align-items:center;gap:12px">
        <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=80&h=80&fit=crop&crop=face" alt="Sarah" style="width:42px;height:42px;border-radius:50%;object-fit:cover;border:2px solid rgba(245,158,11,0.5);flex-shrink:0" onerror="this.style.display=\'none\'">
        <div style="flex:1"><div style="color:#fff;font-weight:700;font-size:0.95rem">Sarah</div><div style="color:rgba(255,255,255,0.65);font-size:0.75rem">{c["specialist"]}</div></div>
        <div style="display:flex;align-items:center;gap:5px"><div style="width:7px;height:7px;background:#22c55e;border-radius:50%"></div><span style="color:rgba(255,255,255,0.65);font-size:0.72rem">Online</span></div>
      </div>
      <div id="hp-msgs" style="background:#f8fafc;padding:16px;min-height:80px;max-height:260px;overflow-y:auto;display:flex;flex-direction:column;gap:10px">
        <div style="background:#fff;border-radius:12px 12px 12px 4px;padding:11px 14px;font-size:0.88rem;color:#374151;box-shadow:0 1px 3px rgba(0,0,0,0.07);max-width:92%;line-height:1.55">{c["greeting"]}</div>
      </div>
      <div id="hp-s1" style="padding:12px 14px;border-top:1px solid #e5e7eb">
        <div style="display:flex;gap:8px">
          <input id="hp-in" type="text" placeholder="Type here..." style="flex:1;border:1px solid #d1d5db;border-radius:8px;padding:10px 13px;font-size:0.88rem;outline:none" onkeydown="if(event.key===\'Enter\')hpSend()">
          <button onclick="hpSend()" style="background:#f59e0b;color:#fff;border:none;border-radius:8px;padding:10px 18px;font-weight:700;cursor:pointer">&#8594;</button>
        </div>
        <div style="text-align:center;font-size:0.72rem;color:#9ca3af;margin-top:5px">Free · Confidential · No SSN required</div>
      </div>
      <div id="hp-s2" style="display:none;padding:14px;border-top:1px solid #e5e7eb">
        <div style="font-weight:700;color:#0f2944;font-size:0.88rem;margin-bottom:10px">Tell me about your vehicle</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-bottom:7px">
          <select id="hp-yr" style="border:1px solid #d1d5db;border-radius:7px;padding:8px 9px;font-size:0.82rem;background:#fff;width:100%"><option value="">Year</option>{YEAR_OPTS}</select>
          <select id="hp-mk" style="border:1px solid #d1d5db;border-radius:7px;padding:8px 9px;font-size:0.82rem;background:#fff;width:100%"><option value="">Make</option><option>Chevrolet</option><option>Ford</option><option>Honda</option><option>Toyota</option><option>Nissan</option><option>Hyundai</option><option>Kia</option><option>Jeep</option><option>Dodge</option><option>Ram</option><option>GMC</option><option>Subaru</option><option>Mazda</option><option>Volkswagen</option><option>BMW</option><option>Mercedes-Benz</option><option>Audi</option><option>Lexus</option><option>Tesla</option><option>Other</option></select>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-bottom:7px">
          <input id="hp-mo" type="text" placeholder="Model" style="border:1px solid #d1d5db;border-radius:7px;padding:8px 9px;font-size:0.82rem">
          <select id="hp-st" style="border:1px solid #d1d5db;border-radius:7px;padding:8px 9px;font-size:0.82rem;background:#fff;width:100%">{STATE_OPTS}</select>
        </div>
        <select id="hp-li" style="border:1px solid #d1d5db;border-radius:7px;padding:8px 9px;font-size:0.82rem;background:#fff;width:100%;margin-bottom:10px"><option value="">License type</option><option>US License</option><option>Foreign License</option><option>Mexican License</option><option>International License</option><option>No License</option></select>
        <button onclick="hpSubmit()" style="width:100%;background:linear-gradient(135deg,#16a34a,#15803d);color:#fff;border:none;border-radius:9px;padding:12px;font-size:0.92rem;font-weight:700;cursor:pointer">{c["submit"]}</button>
        <div style="text-align:center;font-size:0.72rem;color:#9ca3af;margin-top:7px">{c["privacy"]}</div>
      </div>
      <div id="hp-s3" style="display:none;padding:12px 14px;border-top:1px solid #e5e7eb">
        <div style="display:flex;gap:8px">
          <input id="hp-ch" type="text" placeholder="Ask a question..." style="flex:1;border:1px solid #d1d5db;border-radius:8px;padding:10px 13px;font-size:0.88rem;outline:none" onkeydown="if(event.key===\'Enter\')hpChat()">
          <button onclick="hpChat()" style="background:#0f2944;color:#fff;border:none;border-radius:8px;padding:10px 16px;font-weight:700;cursor:pointer">&#8594;</button>
        </div>
      </div>
    </div>
  </div>
</div>
<script>
var hpStep=0,hpName='',hpPhone='',hpHist=[];
var HPSYS="{sys_esc}";
function hpAddBot(t){{var m=document.getElementById('hp-msgs');var d=document.createElement('div');d.style.cssText='background:#fff;border-radius:12px 12px 12px 4px;padding:11px 14px;font-size:0.88rem;color:#374151;box-shadow:0 1px 3px rgba(0,0,0,0.07);max-width:92%;line-height:1.55';d.textContent=t;m.appendChild(d);m.scrollTop=m.scrollHeight;}}
function hpAddUser(t){{var m=document.getElementById('hp-msgs');var d=document.createElement('div');d.style.cssText='background:#0f2944;color:#fff;border-radius:12px 12px 4px 12px;padding:10px 13px;font-size:0.88rem;max-width:85%;align-self:flex-end;margin-left:auto;line-height:1.5';d.textContent=t;m.appendChild(d);m.scrollTop=m.scrollHeight;}}
function hpSend(){{var i=document.getElementById('hp-in');var v=i.value.trim();if(!v)return;i.value='';hpAddUser(v);if(hpStep===0){{hpName=v;hpStep=1;setTimeout(()=>hpAddBot('{c["phone"]}'),300);}}else if(hpStep===1){{hpPhone=v;hpStep=2;setTimeout(()=>{{hpAddBot('{c["gotit"]}');document.getElementById('hp-s1').style.display='none';document.getElementById('hp-s2').style.display='block';}},300);}}}};
async function hpSubmit(){{var yr=document.getElementById('hp-yr').value;var mk=document.getElementById('hp-mk').value;var st=document.getElementById('hp-st').value;var mo=document.getElementById('hp-mo').value;var li=document.getElementById('hp-li').value;if(!yr||!mk||!st){{alert('Please select year, make and state.');return;}}var lead={{name:hpName,phone:hpPhone,year:yr,make:mk,model:mo,state:st,license:li,url:window.location.href,time:new Date().toISOString()}};console.log('LEAD:',JSON.stringify(lead));document.getElementById('hp-s2').style.display='none';document.getElementById('hp-s3').style.display='block';hpStep=3;hpAddUser(yr+' '+mk+' — '+st);hpHist.push({{role:'user',content:'Details: '+hpName+', '+hpPhone+', '+yr+' '+mk+' '+mo+', '+st+', '+li}});setTimeout(async()=>{{try{{var r=await fetch('https://api.anthropic.com/v1/messages',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{model:'claude-haiku-4-5-20251001',max_tokens:150,system:HPSYS,messages:hpHist}})}});var d=await r.json();var rep=d.content&&d.content[0]?d.content[0].text:'{c["thanks"]}';hpAddBot(rep);hpHist.push({{role:'assistant',content:rep}})}}catch(e){{hpAddBot('{c["thanks"]}');}}}},400);}}
async function hpChat(){{var i=document.getElementById('hp-ch');var msg=i.value.trim();if(!msg)return;i.value='';hpAddUser(msg);hpHist.push({{role:'user',content:msg}});try{{var r=await fetch('https://api.anthropic.com/v1/messages',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{model:'claude-haiku-4-5-20251001',max_tokens:150,system:HPSYS,messages:hpHist}})}});var d=await r.json();var rep=d.content&&d.content[0]?d.content[0].text:'Please try again.';hpAddBot(rep);hpHist.push({{role:'assistant',content:rep}})}}catch(e){{hpAddBot('Please try again.');}}}}
</script>'''


def build_floating_sarah(lang):
    c = SARAH_LANGS.get(lang, SARAH_LANGS['en'])
    sys_esc = (c['sys'] + ' Page: "+document.title+". URL: "+window.location.pathname+"').replace('"',"'")
    return f'''<!-- Sarah Float -->
<div id="sw" style="position:fixed;bottom:24px;right:24px;z-index:9999;width:360px;max-width:calc(100vw - 32px);font-family:system-ui,sans-serif">
  <div id="sp" style="background:#fff;border-radius:16px;box-shadow:0 8px 40px rgba(0,0,0,0.2);overflow:hidden">
    <div style="background:linear-gradient(135deg,#0f2944,#1a4a7a);padding:12px 16px;display:flex;align-items:center;gap:10px">
      <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=80&h=80&fit=crop&crop=face" alt="Sarah" style="width:38px;height:38px;border-radius:50%;object-fit:cover;border:2px solid rgba(245,158,11,0.5);flex-shrink:0" onerror="this.style.display=\'none\'">
      <div style="flex:1"><div style="color:#fff;font-weight:700;font-size:0.9rem">Sarah</div><div style="color:rgba(255,255,255,0.65);font-size:0.72rem">{c["specialist"]}</div></div>
      <div style="display:flex;align-items:center;gap:4px;margin-right:6px"><div style="width:6px;height:6px;background:#22c55e;border-radius:50%"></div><span style="color:rgba(255,255,255,0.6);font-size:0.7rem">Online</span></div>
      <button onclick="swToggle()" style="background:none;border:none;color:rgba(255,255,255,0.6);font-size:1.1rem;cursor:pointer;padding:2px 4px">—</button>
    </div>
    <div id="sm" style="background:#f8fafc;padding:12px;min-height:80px;max-height:220px;overflow-y:auto;display:flex;flex-direction:column;gap:8px">
      <div style="background:#fff;border-radius:10px 10px 10px 3px;padding:10px 12px;font-size:0.86rem;color:#374151;box-shadow:0 1px 3px rgba(0,0,0,0.07);max-width:92%;line-height:1.5">{c["greeting"]}</div>
    </div>
    <div id="sw-s1" style="padding:10px 12px;border-top:1px solid #e5e7eb">
      <div style="display:flex;gap:7px">
        <input id="sw-in" type="text" placeholder="Type here..." style="flex:1;border:1px solid #d1d5db;border-radius:7px;padding:9px 11px;font-size:0.85rem;outline:none" onkeydown="if(event.key===\'Enter\')swSend()">
        <button onclick="swSend()" style="background:#f59e0b;color:#fff;border:none;border-radius:7px;padding:9px 14px;font-weight:700;cursor:pointer">&#8594;</button>
      </div>
    </div>
    <div id="sw-s2" style="display:none;padding:12px;border-top:1px solid #e5e7eb">
      <div style="font-weight:700;color:#0f2944;font-size:0.84rem;margin-bottom:8px">Tell me about your vehicle</div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:6px">
        <select id="sw-yr" style="border:1px solid #d1d5db;border-radius:6px;padding:7px 8px;font-size:0.8rem;background:#fff;width:100%"><option value="">Year</option>{YEAR_OPTS}</select>
        <select id="sw-mk" style="border:1px solid #d1d5db;border-radius:6px;padding:7px 8px;font-size:0.8rem;background:#fff;width:100%"><option value="">Make</option><option>Chevrolet</option><option>Ford</option><option>Honda</option><option>Toyota</option><option>Nissan</option><option>Hyundai</option><option>Kia</option><option>Jeep</option><option>Dodge</option><option>Ram</option><option>GMC</option><option>Subaru</option><option>Mazda</option><option>Volkswagen</option><option>BMW</option><option>Mercedes-Benz</option><option>Audi</option><option>Lexus</option><option>Tesla</option><option>Other</option></select>
      </div>
      <div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:6px">
        <input id="sw-mo" type="text" placeholder="Model" style="border:1px solid #d1d5db;border-radius:6px;padding:7px 8px;font-size:0.8rem">
        <select id="sw-st" style="border:1px solid #d1d5db;border-radius:6px;padding:7px 8px;font-size:0.8rem;background:#fff;width:100%">{STATE_OPTS}</select>
      </div>
      <select id="sw-li" style="border:1px solid #d1d5db;border-radius:6px;padding:7px 8px;font-size:0.8rem;background:#fff;width:100%;margin-bottom:8px"><option value="">License type</option><option>US License</option><option>Foreign License</option><option>Mexican License</option><option>International License</option><option>No License</option></select>
      <button onclick="swSubmit()" style="width:100%;background:linear-gradient(135deg,#16a34a,#15803d);color:#fff;border:none;border-radius:8px;padding:10px;font-size:0.88rem;font-weight:700;cursor:pointer">{c["submit"]}</button>
      <div style="text-align:center;font-size:0.7rem;color:#9ca3af;margin-top:5px">{c["privacy"]}</div>
    </div>
    <div id="sw-s3" style="display:none;padding:10px 12px;border-top:1px solid #e5e7eb">
      <div style="display:flex;gap:7px">
        <input id="sw-ch" type="text" placeholder="Ask a question..." style="flex:1;border:1px solid #d1d5db;border-radius:7px;padding:9px 11px;font-size:0.85rem;outline:none" onkeydown="if(event.key===\'Enter\')swChat()">
        <button onclick="swChat()" style="background:#0f2944;color:#fff;border:none;border-radius:7px;padding:9px 13px;font-weight:700;cursor:pointer">&#8594;</button>
      </div>
    </div>
  </div>
  <button id="sw-btn" onclick="swToggle()" style="display:none;background:linear-gradient(135deg,#f59e0b,#d97706);color:#fff;border:none;border-radius:50px;padding:12px 20px;font-size:0.88rem;font-weight:700;cursor:pointer;box-shadow:0 4px 16px rgba(245,158,11,0.4);width:100%;margin-top:8px">Chat with Sarah &rarr;</button>
</div>
<script>
var swOpen=true,swStep=0,swName='',swPhone='',swHist=[];
var SWSYS="{sys_esc}";
function swToggle(){{swOpen=!swOpen;document.getElementById('sp').style.display=swOpen?'block':'none';document.getElementById('sw-btn').style.display=swOpen?'none':'block';}}
function swAddBot(t){{var m=document.getElementById('sm');var d=document.createElement('div');d.style.cssText='background:#fff;border-radius:10px 10px 10px 3px;padding:10px 12px;font-size:0.86rem;color:#374151;box-shadow:0 1px 3px rgba(0,0,0,0.07);max-width:92%;line-height:1.5';d.textContent=t;m.appendChild(d);m.scrollTop=m.scrollHeight;}}
function swAddUser(t){{var m=document.getElementById('sm');var d=document.createElement('div');d.style.cssText='background:#0f2944;color:#fff;border-radius:10px 10px 3px 10px;padding:9px 12px;font-size:0.86rem;max-width:85%;align-self:flex-end;margin-left:auto;line-height:1.5';d.textContent=t;m.appendChild(d);m.scrollTop=m.scrollHeight;}}
function swSend(){{var i=document.getElementById('sw-in');var v=i.value.trim();if(!v)return;i.value='';swAddUser(v);if(swStep===0){{swName=v;swStep=1;setTimeout(()=>swAddBot('{c["phone"]}'),300);}}else if(swStep===1){{swPhone=v;swStep=2;setTimeout(()=>{{swAddBot('{c["gotit"]}');document.getElementById('sw-s1').style.display='none';document.getElementById('sw-s2').style.display='block';}},300);}}}};
async function swSubmit(){{var yr=document.getElementById('sw-yr').value;var mk=document.getElementById('sw-mk').value;var st=document.getElementById('sw-st').value;var mo=document.getElementById('sw-mo').value;var li=document.getElementById('sw-li').value;if(!yr||!mk||!st){{alert('Please select year, make and state.');return;}}var lead={{name:swName,phone:swPhone,year:yr,make:mk,model:mo,state:st,license:li,url:window.location.href,time:new Date().toISOString()}};console.log('LEAD:',JSON.stringify(lead));document.getElementById('sw-s2').style.display='none';document.getElementById('sw-s3').style.display='block';swStep=3;swAddUser(yr+' '+mk+' — '+st);swHist.push({{role:'user',content:'Details: '+swName+', '+swPhone+', '+yr+' '+mk+' '+mo+', '+st+', '+li}});setTimeout(async()=>{{try{{var r=await fetch('https://api.anthropic.com/v1/messages',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{model:'claude-haiku-4-5-20251001',max_tokens:150,system:SWSYS,messages:swHist}})}});var d=await r.json();var rep=d.content&&d.content[0]?d.content[0].text:'{c["thanks"]}';swAddBot(rep);swHist.push({{role:'assistant',content:rep}})}}catch(e){{swAddBot('{c["thanks"]}');}}}},400);}}
async function swChat(){{var i=document.getElementById('sw-ch');var msg=i.value.trim();if(!msg)return;i.value='';swAddUser(msg);swHist.push({{role:'user',content:msg}});try{{var r=await fetch('https://api.anthropic.com/v1/messages',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{model:'claude-haiku-4-5-20251001',max_tokens:150,system:SWSYS,messages:swHist}})}});var d=await r.json();var rep=d.content&&d.content[0]?d.content[0].text:'Please try again.';swAddBot(rep);swHist.push({{role:'assistant',content:rep}})}}catch(e){{swAddBot('Please try again.');}}}}
</script>'''


HOMEPAGES = {
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

files = [f for f in glob.glob('**/*.html', recursive=True) if not f.startswith('.')]
print(f"Processing {len(files)} files...")
hp_fixed = nav_fixed = sarah_fixed = pills_fixed = 0

for filepath in files:
    try:
        with open(filepath,'r',encoding='utf-8',errors='ignore') as f:
            content = f.read()
        original = content
        fp = filepath.replace('\\','/')
        lang = HOMEPAGES.get(fp, None)
        if lang is None:
            # Get lang from path for floating sarah
            parts = fp.split('/')
            known = ['es','zh','ar','pt','vi','tl','ko','ru','pl']
            lang = next((p for p in parts if p in known), 'en')

        is_hp = fp in HOMEPAGES

        # 1. Remove ALL old Sarah from every page
        content = re.sub(r'<!-- Sarah.*?</script>\s*', '', content, flags=re.DOTALL)
        content = re.sub(r'<!-- Sarah Float -->.*?</script>\s*', '', content, flags=re.DOTALL)
        content = re.sub(r'<div id="sw".*?</script>\s*', '', content, flags=re.DOTALL)
        content = re.sub(r'<div id="sarah-wrap".*?</script>\s*', '', content, flags=re.DOTALL)
        content = re.sub(r'<button id="sw-btn".*?</button>', '', content, flags=re.DOTALL)
        content = re.sub(r'<button id="sarah-min-btn".*?</button>', '', content, flags=re.DOTALL)
        content = re.sub(r'<div id="sarah-container".*?</script>\s*', '', content, flags=re.DOTALL)

        # 2. Remove nav lang-switcher HTML (not CSS)
        content = re.sub(r'<div class="lang-switcher">\s*<a[^>]*>.*?</div>', '', content, flags=re.DOTALL)
        nav_fixed += 1

        if is_hp:
            hp_lang = HOMEPAGES[fp]
            
            # 3. Remove old lang pills
            content = re.sub(r'<div class="lang-grid">.*?</div>', '', content, flags=re.DOTALL)
            content = re.sub(r'<div class="lang-bar">.*?</div>', '', content, flags=re.DOTALL)

            # 4. Add lang pills in hero — before closing hero div
            pills = LANG_PILLS.get(hp_lang, LANG_PILLS_EN) if hp_lang != 'en' else LANG_PILLS_EN
            # Insert after the hero paragraph
            content = re.sub(
                r'(</p>\s*</div>\s*</div>\s*</div>)',
                lambda m: '\n' + pills + '\n' + m.group(0),
                content, count=1
            )
            pills_fixed += 1

            # 5. Add hardcoded Sarah after hero
            inline = build_inline_sarah(hp_lang)
            content = re.sub(
                r'(<div style="max-width:1200px;margin:40px auto)',
                inline + '\n\\1',
                content, count=1
            )
            hp_fixed += 1

        else:
            # 6. Add floating Sarah to inner pages
            floating = build_floating_sarah(lang)
            content = content.replace('</body>', floating + '\n</body>', 1)
            sarah_fixed += 1

        if content != original:
            with open(filepath,'w',encoding='utf-8') as f:
                f.write(content)

    except Exception as e:
        print(f"  Error {filepath}: {e}")

print(f"\n{'='*50}")
print(f"Homepages fixed:     {hp_fixed}")
print(f"Nav cleaned:         {nav_fixed}")
print(f"Inner Sarah added:   {sarah_fixed}")
print(f"Lang pills fixed:    {pills_fixed}")
print(f"{'='*50}")
