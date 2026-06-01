#!/usr/bin/env python3
"""
fix_homepage_cii.py
Fixes carinsuranceimmigrants.us:
1. Removes duplicate lang pills from hero
2. Better looking lang pills
3. Replaces "CarInsuranceImmigrants.us" with "We"
4. Fixes dead footer links
5. Fixes footer disclaimer
6. Installs Sarah on all pages — in the correct language
"""

import re, glob

LANG_CONFIG = {
    'en': {'name': 'Sarah', 'greeting': "Hi! I'm Sarah 👋 I help immigrants find car insurance — no SSN required, no ICE reporting, completely free. What's your question?", 'placeholder': 'Ask me anything...', 'system': 'You are Sarah, a friendly car insurance assistant for CarInsuranceImmigrants.us. Help immigrants in the US find car insurance regardless of their status. Key facts: You do NOT need SSN. Insurance companies do NOT report to ICE. ITIN works for many insurers. Undocumented immigrants CAN get insurance. Be warm, direct, reassuring. Answer in 2-3 sentences max. If they want help, ask for name and phone number.'},
    'es': {'name': 'Sarah', 'greeting': "¡Hola! Soy Sarah 👋 Ayudo a inmigrantes a encontrar seguro de auto — sin SSN, sin reporte a ICE, completamente gratis. ¿Cuál es tu pregunta?", 'placeholder': 'Hazme una pregunta...', 'system': 'Eres Sarah, asistente de seguros de auto para CarInsuranceImmigrants.us. Ayuda a inmigrantes en EEUU a obtener seguro sin importar su estatus. Hechos clave: NO necesitas SSN. Las aseguradoras NO reportan a ICE. El ITIN funciona. Los indocumentados SÍ pueden obtener seguro. Sé cálida, directa y tranquilizadora. Responde en 2-3 oraciones. Si quieren ayuda, pide nombre y teléfono.'},
    'zh': {'name': 'Sarah', 'greeting': "你好！我是Sarah 👋 我帮助移民找到汽车保险——不需要SSN，不向ICE举报，完全免费。您有什么问题？", 'placeholder': '请问我任何问题...', 'system': '你是Sarah，CarInsuranceImmigrants.us的汽车保险助理。帮助美国移民获得汽车保险，不论其身份。关键事实：不需要SSN。保险公司不向ICE举报。ITIN适用于许多保险公司。无证移民可以获得保险。要热情、直接、令人安心。回答2-3句话。如果他们需要帮助，请询问姓名和电话号码。'},
    'ar': {'name': 'سارة', 'greeting': "مرحباً! أنا سارة 👋 أساعد المهاجرين في إيجاد تأمين السيارات — بدون SSN، بدون إبلاغ ICE، مجاناً تماماً. ما سؤالك؟", 'placeholder': 'اسألني أي شيء...', 'system': 'أنت سارة، مساعدة تأمين السيارات في CarInsuranceImmigrants.us. ساعد المهاجرين في الحصول على تأمين بغض النظر عن وضعهم. حقائق مهمة: لا تحتاج SSN. شركات التأمين لا تبلغ ICE. ITIN يعمل مع كثير من الشركات. المهاجرون غير الموثقين يمكنهم الحصول على تأمين. كوني دافئة ومباشرة ومطمئنة. أجيبي في 2-3 جمل.'},
    'pt': {'name': 'Sarah', 'greeting': "Olá! Sou a Sarah 👋 Ajudo imigrantes a encontrar seguro de carro — sem SSN, sem denúncia ao ICE, completamente grátis. Qual é a sua pergunta?", 'placeholder': 'Pergunte-me qualquer coisa...', 'system': 'Você é Sarah, assistente de seguro de carro da CarInsuranceImmigrants.us. Ajude imigrantes nos EUA a obter seguro independente do status. Fatos importantes: Não precisa de SSN. Seguradoras NÃO reportam ao ICE. ITIN funciona. Imigrantes sem documentos PODEM obter seguro. Seja calorosa, direta e tranquilizadora. Responda em 2-3 frases.'},
    'vi': {'name': 'Sarah', 'greeting': "Xin chào! Tôi là Sarah 👋 Tôi giúp người nhập cư tìm bảo hiểm xe hơi — không cần SSN, không báo cáo với ICE, hoàn toàn miễn phí. Câu hỏi của bạn là gì?", 'placeholder': 'Hỏi tôi bất cứ điều gì...', 'system': 'Bạn là Sarah, trợ lý bảo hiểm xe hơi cho CarInsuranceImmigrants.us. Giúp người nhập cư tại Mỹ có được bảo hiểm bất kể tình trạng của họ. Sự thật quan trọng: Không cần SSN. Công ty bảo hiểm KHÔNG báo cáo với ICE. ITIN hoạt động với nhiều công ty. Người nhập cư không có giấy tờ CÓ THỂ mua bảo hiểm. Hãy thân thiện, thẳng thắn và trấn an. Trả lời 2-3 câu.'},
    'tl': {'name': 'Sarah', 'greeting': "Kumusta! Ako si Sarah 👋 Tinutulungan ko ang mga imigrante na mahanap ang insurance sa kotse — walang SSN, walang report sa ICE, libre. Ano ang iyong tanong?", 'placeholder': 'Tanungin mo ako ng kahit ano...', 'system': 'Ikaw si Sarah, car insurance assistant para sa CarInsuranceImmigrants.us. Tulungan ang mga imigrante sa US na makakuha ng insurance kahit anong katayuan. Mahahalagang katotohanan: Hindi kailangan ng SSN. Hindi nag-rerepor ang mga kompanya ng insurance sa ICE. Gumagana ang ITIN. Pwedeng makakuha ng insurance ang mga undocumented. Maging mainit, tapat at nakakapanatag. Sagutin sa 2-3 pangungusap.'},
    'ko': {'name': 'Sarah', 'greeting': "안녕하세요! 저는 Sarah예요 👋 이민자들이 자동차 보험을 찾도록 도와드립니다 — SSN 없어도 되고, ICE에 신고하지 않으며, 완전 무료예요. 질문이 있으세요?", 'placeholder': '무엇이든 물어보세요...', 'system': '당신은 Sarah로 CarInsuranceImmigrants.us의 자동차 보험 도우미입니다. 체류 신분에 관계없이 미국 이민자들이 자동차 보험을 받을 수 있도록 도와주세요. 핵심 사실: SSN 불필요. 보험회사는 ICE에 신고하지 않음. ITIN 가능. 서류 미비자도 보험 가입 가능. 따뜻하고 직접적이며 안심시켜주세요. 2-3문장으로 답하세요.'},
    'ru': {'name': 'Сара', 'greeting': "Привет! Я Сара 👋 Помогаю иммигрантам найти автострахование — без SSN, без сообщения в ICE, совершенно бесплатно. Какой у вас вопрос?", 'placeholder': 'Спросите меня о чём угодно...', 'system': 'Вы Сара, помощник по автострахованию для CarInsuranceImmigrants.us. Помогайте иммигрантам в США получить страховку независимо от их статуса. Ключевые факты: SSN не нужен. Страховые компании НЕ сообщают в ICE. ITIN работает. Нелегальные иммигранты МОГУТ получить страховку. Будьте тёплой, прямой и успокаивающей. Отвечайте 2-3 предложениями.'},
    'pl': {'name': 'Sarah', 'greeting': "Cześć! Jestem Sarah 👋 Pomagam imigrantom znaleźć ubezpieczenie samochodu — bez SSN, bez zgłaszania do ICE, całkowicie bezpłatnie. Jakie masz pytanie?", 'placeholder': 'Zapytaj mnie o cokolwiek...', 'system': 'Jesteś Sarah, asystentką ubezpieczeń samochodowych dla CarInsuranceImmigrants.us. Pomagaj imigrantom w USA uzyskać ubezpieczenie niezależnie od statusu. Kluczowe fakty: Nie potrzebujesz SSN. Firmy ubezpieczeniowe NIE zgłaszają do ICE. ITIN działa. Nielegalni imigranci MOGĄ uzyskać ubezpieczenie. Bądź ciepła, bezpośrednia i uspokajająca. Odpowiadaj w 2-3 zdaniach.'},
}

def get_lang_from_path(filepath):
    """Get language code from file path."""
    parts = filepath.replace('\\', '/').split('/')
    lang_codes = list(LANG_CONFIG.keys())
    for part in parts:
        if part in lang_codes and part != 'en':
            return part
    return 'en'

def build_sarah(lang_code):
    """Build Sarah widget for specific language."""
    cfg = LANG_CONFIG.get(lang_code, LANG_CONFIG['en'])
    is_rtl = lang_code == 'ar'
    
    return f'''
<!-- Sarah AI Widget -->
<div id="sarah-widget" style="position:fixed;bottom:24px;right:24px;z-index:9999;font-family:system-ui,sans-serif">
  <div id="sarah-bubble" style="display:none;background:#fff;border-radius:16px;box-shadow:0 8px 32px rgba(0,0,0,0.18);width:340px;max-height:500px;flex-direction:column;overflow:hidden;direction:{"rtl" if is_rtl else "ltr"}">
    <div style="background:linear-gradient(135deg,#0f2944,#1a4a7a);padding:16px 20px;display:flex;align-items:center;gap:12px">
      <div style="width:40px;height:40px;background:#f59e0b;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:1.3rem">🤖</div>
      <div>
        <div style="color:#fff;font-weight:700;font-size:1rem">{cfg["name"]}</div>
        <div style="color:rgba(255,255,255,0.7);font-size:0.8rem">CarInsuranceImmigrants.us</div>
      </div>
      <button onclick="toggleSarah()" style="margin-left:auto;background:none;border:none;color:#fff;font-size:1.4rem;cursor:pointer;padding:4px">×</button>
    </div>
    <div id="sarah-messages" style="flex:1;overflow-y:auto;padding:16px;display:flex;flex-direction:column;gap:12px;min-height:200px;max-height:280px">
      <div style="background:#f0f4f8;border-radius:12px 12px 12px 4px;padding:12px 14px;font-size:0.9rem;max-width:88%">{cfg["greeting"]}</div>
    </div>
    <div style="padding:12px;border-top:1px solid #e5e7eb;display:flex;gap:8px">
      <input id="sarah-input" type="text" placeholder="{cfg["placeholder"]}"
        style="flex:1;border:1px solid #d1d5db;border-radius:8px;padding:10px 14px;font-size:0.9rem;outline:none;direction:{"rtl" if is_rtl else "ltr"}"
        onkeydown="if(event.key==='Enter')sendSarah()">
      <button onclick="sendSarah()"
        style="background:#f59e0b;color:#fff;border:none;border-radius:8px;padding:10px 16px;font-weight:700;cursor:pointer;font-size:0.9rem">→</button>
    </div>
  </div>
  <button onclick="toggleSarah()" id="sarah-btn"
    style="width:60px;height:60px;background:linear-gradient(135deg,#f59e0b,#e07c00);border:none;border-radius:50%;box-shadow:0 4px 16px rgba(245,158,11,0.5);cursor:pointer;font-size:1.6rem;display:flex;align-items:center;justify-content:center;transition:transform 0.2s"
    onmouseover="this.style.transform=\'scale(1.1)\'" onmouseout="this.style.transform=\'scale(1)\'">💬</button>
</div>
<script>
var sarahOpen=false,sarahHistory=[];
var SARAH_SYSTEM="{cfg["system"].replace(chr(34), chr(39))}";
function toggleSarah(){{
  sarahOpen=!sarahOpen;
  var b=document.getElementById("sarah-bubble");
  b.style.display=sarahOpen?"flex":"none";
  if(sarahOpen)document.getElementById("sarah-input").focus();
}}
function addMsg(text,role){{
  var msgs=document.getElementById("sarah-messages");
  var div=document.createElement("div");
  div.style.cssText=role==="user"
    ?"background:#f59e0b;color:#fff;border-radius:12px 12px 4px 12px;padding:10px 14px;font-size:0.9rem;max-width:85%;align-self:flex-end;margin-left:auto"
    :"background:#f0f4f8;border-radius:12px 12px 12px 4px;padding:12px 14px;font-size:0.9rem;max-width:88%";
  div.textContent=text;
  msgs.appendChild(div);
  msgs.scrollTop=msgs.scrollHeight;
}}
async function sendSarah(){{
  var input=document.getElementById("sarah-input");
  var msg=input.value.trim();
  if(!msg)return;
  input.value="";
  addMsg(msg,"user");
  sarahHistory.push({{role:"user",content:msg}});
  var typing=document.createElement("div");
  typing.id="sarah-typing";
  typing.style.cssText="background:#f0f4f8;border-radius:12px;padding:10px 14px;font-size:0.85rem;color:#999;max-width:85%";
  typing.textContent="...";
  document.getElementById("sarah-messages").appendChild(typing);
  try{{
    var res=await fetch("https://api.anthropic.com/v1/messages",{{
      method:"POST",
      headers:{{"Content-Type":"application/json"}},
      body:JSON.stringify({{
        model:"claude-haiku-4-5-20251001",
        max_tokens:300,
        system:SARAH_SYSTEM,
        messages:sarahHistory
      }})
    }});
    var data=await res.json();
    var reply=data.content&&data.content[0]?data.content[0].text:"Sorry, try again.";
    var t=document.getElementById("sarah-typing");
    if(t)t.remove();
    addMsg(reply,"bot");
    sarahHistory.push({{role:"assistant",content:reply}});
  }}catch(e){{
    var t=document.getElementById("sarah-typing");
    if(t)t.remove();
    addMsg("Connection error. Please try again.","bot");
  }}
}}
</script>'''

def fix_homepage(content):
    content = content.replace(
        'CarInsuranceImmigrants.us answers every car insurance question immigrants have',
        'We answer every car insurance question immigrants have'
    )
    content = re.sub(r'<div class="lang-bar">.*?</div>', '', content, flags=re.DOTALL)
    content = content.replace('<li><a href="/foreign-license/">Foreign License</a></li>',
        '<li><a href="/foreign-license/mexican/">Foreign License</a></li>')
    content = content.replace('<li><a href="/save-money/">Save Money</a></li>',
        '<li><a href="/coverage/">Coverage Explained</a></li>')
    content = content.replace('<li><a href="/states/">All 50 States</a></li>',
        '<li><a href="/questions/">All Questions</a></li>')
    content = content.replace('<li><a href="/about/how-we-research/">How We Research</a></li>', '')
    content = content.replace('<li><a href="/resources/state-legal-aid/">Free Legal Aid</a></li>', '')
    content = content.replace(
        'The information on Car Insurance Immigrants is provided for general educational purposes only. It does not constitute legal advice and does not create an attorney-client relationship. Immigration law and other areas of law are complex, change frequently, and vary by individual circumstances and state. Do not act or refrain from acting based solely on information found on this website without first seeking qualified legal advice from a licensed attorney. If you need legal assistance, please consult a qualified attorney or contact a free legal aid organization.',
        'The information on CarInsuranceImmigrants.us is for general educational purposes only. We are not an insurance company, broker, or agent. Insurance rates, policies, and state laws change frequently — always verify directly with insurers and your state DMV.'
    )
    return content

files = [f for f in glob.glob('**/*.html', recursive=True) if not f.startswith('.')]
print(f"Processing {len(files)} HTML files...")
sarah_added = fixed = 0

for filepath in files:
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            original = f.read()
        modified = original
        lang = get_lang_from_path(filepath)
        if 'sarah-widget' not in modified:
            modified = modified.replace('</body>', build_sarah(lang) + '\n</body>')
            sarah_added += 1
        if filepath == 'index.html':
            modified = fix_homepage(modified)
            fixed += 1
            print(f"  ✅ Homepage fixed")
        if modified != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(modified)
    except Exception as e:
        print(f"  ❌ {filepath}: {e}")

print(f"\n{'='*50}")
print(f"Sarah added: {sarah_added} pages")
print(f"Homepage fixed: {fixed}")
print("Done. Commit and push.")
