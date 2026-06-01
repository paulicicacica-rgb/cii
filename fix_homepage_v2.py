#!/usr/bin/env python3
"""
fix_homepage_v2.py
- Sarah hardcoded into homepage (not floating)
- Language buttons restored, clean grid layout
- Floating Sarah removed from homepage only
- CTA section below hero
"""

import re, glob

LANG_BUTTONS = '''<div class="lang-grid">
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

LANG_CSS = '''
<style>
.lang-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  justify-content: center;
  margin: 28px auto 0;
  max-width: 500px;
}
.lang-pill {
  background: rgba(255,255,255,0.12);
  border: 1.5px solid rgba(255,255,255,0.35);
  color: #fff;
  padding: 8px 16px;
  border-radius: 24px;
  font-size: 0.85rem;
  font-weight: 500;
  text-decoration: none;
  transition: all 0.2s;
  white-space: nowrap;
}
.lang-pill:hover, .lang-pill.active {
  background: rgba(255,255,255,0.25);
  border-color: rgba(255,255,255,0.7);
  color: #fff;
  text-decoration: none;
}
</style>'''

HERO_SARAH = '''
<!-- Hardcoded Sarah -->
<div style="background:#f7f9fc;padding:60px 24px 80px;text-align:center">
  <div style="max-width:480px;margin:0 auto">
    
    <p style="color:#f59e0b;font-size:0.8rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;margin-bottom:12px">GET STARTED</p>
    <h2 style="font-size:clamp(1.6rem,4vw,2.2rem);font-weight:800;color:#0f2944;line-height:1.25;margin-bottom:12px">
      Tell Sarah about your situation.<br>She will find you the right coverage.
    </h2>
    <p style="color:#6b7280;font-size:0.95rem;margin-bottom:32px">Free · No obligation · No SSN required</p>

    <!-- Sarah chat hardcoded -->
    <div id="sarah-inline" style="background:#fff;border-radius:16px;box-shadow:0 8px 40px rgba(0,0,0,0.12);overflow:hidden;text-align:left">
      
      <!-- Header -->
      <div style="background:linear-gradient(135deg,#0f2944,#1a4a7a);padding:14px 18px;display:flex;align-items:center;gap:12px">
        <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=80&h=80&fit=crop&crop=face"
             alt="Sarah" style="width:42px;height:42px;border-radius:50%;object-fit:cover;border:2px solid rgba(245,158,11,0.6);flex-shrink:0"
             onerror="this.style.display=\'none\'">
        <div style="flex:1">
          <div style="color:#fff;font-weight:700;font-size:0.95rem">Sarah</div>
          <div style="color:rgba(255,255,255,0.65);font-size:0.75rem">Car Insurance Specialist</div>
        </div>
        <div style="display:flex;align-items:center;gap:5px">
          <div style="width:7px;height:7px;background:#22c55e;border-radius:50%"></div>
          <span style="color:rgba(255,255,255,0.65);font-size:0.75rem">Online</span>
        </div>
      </div>

      <!-- Messages -->
      <div id="inline-msgs" style="background:#f8fafc;padding:16px;min-height:80px;max-height:220px;overflow-y:auto;display:flex;flex-direction:column;gap:10px">
        <div style="background:#fff;border-radius:12px 12px 12px 4px;padding:11px 14px;font-size:0.88rem;color:#374151;box-shadow:0 1px 3px rgba(0,0,0,0.07);max-width:88%;line-height:1.55">
          Hi, I am Sarah. I can help you find car insurance — no matter your situation. What is your full name?
        </div>
      </div>

      <!-- Step 1: name input -->
      <div id="inline-step1" style="padding:12px 14px;border-top:1px solid #e5e7eb">
        <div style="display:flex;gap:8px">
          <input id="inline-input" type="text" placeholder="Type here..."
            style="flex:1;border:1px solid #d1d5db;border-radius:8px;padding:10px 13px;font-size:0.88rem;outline:none"
            onkeydown="if(event.key===\'Enter\')inlineSend()">
          <button onclick="inlineSend()"
            style="background:#f59e0b;color:#fff;border:none;border-radius:8px;padding:10px 18px;font-weight:700;cursor:pointer;font-size:0.9rem">&#8594;</button>
        </div>
        <div style="text-align:center;font-size:0.72rem;color:#9ca3af;margin-top:6px">Confidential · Free · No obligation</div>
      </div>

      <!-- Step 2: car form (hidden) -->
      <div id="inline-step2" style="display:none;padding:14px;border-top:1px solid #e5e7eb">
        <div style="font-weight:700;color:#0f2944;font-size:0.88rem;margin-bottom:10px">Now tell me about your vehicle</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-bottom:7px">
          <select id="i-year" style="border:1px solid #d1d5db;border-radius:7px;padding:8px 9px;font-size:0.82rem;background:#fff;width:100%">
            <option value="">Year</option>
            <option>2026</option><option>2025</option><option>2024</option><option>2023</option><option>2022</option>
            <option>2021</option><option>2020</option><option>2019</option><option>2018</option><option>2017</option>
            <option>2016</option><option>2015</option><option>2014</option><option>2013</option><option>2012</option>
            <option>2011</option><option>2010</option><option>2009</option><option>2008</option><option>2007</option>
            <option>2006</option><option>2005</option><option>2004</option><option>2003</option><option>2002</option>
            <option>2001</option><option>2000</option><option>1999</option><option>1998</option><option>1997</option>
            <option>1995</option><option>1994</option><option>1993</option><option>1992</option><option>1991</option><option>1990</option>
          </select>
          <select id="i-make" style="border:1px solid #d1d5db;border-radius:7px;padding:8px 9px;font-size:0.82rem;background:#fff;width:100%">
            <option value="">Make</option>
            <option>Chevrolet</option><option>Ford</option><option>Honda</option><option>Toyota</option>
            <option>Nissan</option><option>Hyundai</option><option>Kia</option><option>Jeep</option>
            <option>Dodge</option><option>Ram</option><option>GMC</option><option>Subaru</option>
            <option>Mazda</option><option>Volkswagen</option><option>BMW</option><option>Mercedes-Benz</option>
            <option>Audi</option><option>Lexus</option><option>Tesla</option><option>Other</option>
          </select>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-bottom:7px">
          <input id="i-model" type="text" placeholder="Model (e.g. Civic)"
            style="border:1px solid #d1d5db;border-radius:7px;padding:8px 9px;font-size:0.82rem">
          <select id="i-state" style="border:1px solid #d1d5db;border-radius:7px;padding:8px 9px;font-size:0.82rem;background:#fff;width:100%">
            <option value="">State</option>
            <option>California</option><option>Texas</option><option>Florida</option><option>New York</option>
            <option>Illinois</option><option>Pennsylvania</option><option>Ohio</option><option>Georgia</option>
            <option>North Carolina</option><option>Michigan</option><option>New Jersey</option><option>Virginia</option>
            <option>Washington</option><option>Arizona</option><option>Massachusetts</option><option>Tennessee</option>
            <option>Indiana</option><option>Missouri</option><option>Maryland</option><option>Wisconsin</option>
            <option>Colorado</option><option>Minnesota</option><option>South Carolina</option><option>Alabama</option>
            <option>Louisiana</option><option>Kentucky</option><option>Oregon</option><option>Oklahoma</option>
            <option>Connecticut</option><option>Utah</option><option>Nevada</option><option>Arkansas</option>
            <option>Mississippi</option><option>Kansas</option><option>New Mexico</option><option>Nebraska</option>
            <option>West Virginia</option><option>Idaho</option><option>Hawaii</option><option>New Hampshire</option>
            <option>Maine</option><option>Montana</option><option>Rhode Island</option><option>Delaware</option>
            <option>South Dakota</option><option>North Dakota</option><option>Alaska</option><option>Vermont</option>
            <option>Wyoming</option><option>Other</option>
          </select>
        </div>
        <select id="i-license" style="border:1px solid #d1d5db;border-radius:7px;padding:8px 9px;font-size:0.82rem;background:#fff;width:100%;margin-bottom:10px">
          <option value="">License type</option>
          <option>US License</option>
          <option>Foreign License</option>
          <option>Mexican License (Matricula)</option>
          <option>International License</option>
          <option>No License</option>
        </select>
        <button onclick="inlineSubmit()"
          style="width:100%;background:linear-gradient(135deg,#16a34a,#15803d);color:#fff;border:none;border-radius:9px;padding:12px;font-size:0.92rem;font-weight:700;cursor:pointer">
          Find My Insurance
        </button>
        <div style="text-align:center;font-size:0.72rem;color:#9ca3af;margin-top:7px">Your information is never shared with any government agency</div>
      </div>

      <!-- Step 3: chat (hidden) -->
      <div id="inline-step3" style="display:none;padding:12px 14px;border-top:1px solid #e5e7eb">
        <div style="display:flex;gap:8px">
          <input id="inline-chat" type="text" placeholder="Ask a question..."
            style="flex:1;border:1px solid #d1d5db;border-radius:8px;padding:10px 13px;font-size:0.88rem;outline:none"
            onkeydown="if(event.key===\'Enter\')inlineChat()">
          <button onclick="inlineChat()"
            style="background:#0f2944;color:#fff;border:none;border-radius:8px;padding:10px 16px;font-weight:700;cursor:pointer">&#8594;</button>
        </div>
      </div>

    </div>
  </div>
</div>

<script>
var inlineStep = 0;
var inlineName = '';
var inlinePhone = '';
var inlineHistory = [];
var INLINE_SYS = "You are Sarah, a car insurance specialist. Help users get car insurance. Be brief — max 2 sentences. Never mention ICE or immigration enforcement.";

function inlineAddBot(text) {
  var msgs = document.getElementById('inline-msgs');
  var d = document.createElement('div');
  d.style.cssText = 'background:#fff;border-radius:12px 12px 12px 4px;padding:11px 14px;font-size:0.88rem;color:#374151;box-shadow:0 1px 3px rgba(0,0,0,0.07);max-width:88%;line-height:1.55';
  d.textContent = text;
  msgs.appendChild(d);
  msgs.scrollTop = msgs.scrollHeight;
}

function inlineAddUser(text) {
  var msgs = document.getElementById('inline-msgs');
  var d = document.createElement('div');
  d.style.cssText = 'background:#0f2944;color:#fff;border-radius:12px 12px 4px 12px;padding:10px 13px;font-size:0.88rem;max-width:85%;align-self:flex-end;margin-left:auto;line-height:1.5';
  d.textContent = text;
  msgs.appendChild(d);
  msgs.scrollTop = msgs.scrollHeight;
}

function inlineSend() {
  var input = document.getElementById('inline-input');
  var val = input.value.trim();
  if (!val) return;
  input.value = '';
  inlineAddUser(val);
  if (inlineStep === 0) {
    inlineName = val;
    inlineStep = 1;
    setTimeout(() => inlineAddBot('And your phone number, ' + inlineName + '?'), 300);
  } else if (inlineStep === 1) {
    inlinePhone = val;
    inlineStep = 2;
    setTimeout(() => {
      inlineAddBot('Got it. Now tell me about your vehicle.');
      document.getElementById('inline-step1').style.display = 'none';
      document.getElementById('inline-step2').style.display = 'block';
    }, 300);
  }
}

async function inlineSubmit() {
  var year = document.getElementById('i-year').value;
  var make = document.getElementById('i-make').value;
  var state = document.getElementById('i-state').value;
  var model = document.getElementById('i-model').value;
  var license = document.getElementById('i-license').value;
  if (!year || !make || !state) { alert('Please select year, make and state.'); return; }
  
  var lead = {name:inlineName, phone:inlinePhone, year, make, model, state, license, url:window.location.href, time:new Date().toISOString()};
  console.log('LEAD:', JSON.stringify(lead));
  
  document.getElementById('inline-step2').style.display = 'none';
  document.getElementById('inline-step3').style.display = 'block';
  inlineStep = 3;
  inlineAddUser(year + ' ' + make + ' — ' + state);
  inlineHistory.push({role:'user', content:'Details: ' + inlineName + ', ' + inlinePhone + ', ' + year + ' ' + make + ' ' + model + ', ' + state + ', ' + license});
  
  setTimeout(async () => {
    inlineAddBot('Thank you ' + inlineName + '. A specialist will contact you at ' + inlinePhone + ' shortly. Do you have any questions in the meantime?');
  }, 400);
}

async function inlineChat() {
  var input = document.getElementById('inline-chat');
  var msg = input.value.trim();
  if (!msg) return;
  input.value = '';
  inlineAddUser(msg);
  inlineHistory.push({role:'user', content:msg});
  try {
    var res = await fetch('https://api.anthropic.com/v1/messages', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({model:'claude-haiku-4-5-20251001',max_tokens:150,system:INLINE_SYS,messages:inlineHistory})
    });
    var data = await res.json();
    var reply = data.content && data.content[0] ? data.content[0].text : 'Please try again.';
    inlineAddBot(reply);
    inlineHistory.push({role:'assistant', content:reply});
  } catch(e) { inlineAddBot('Please try again.'); }
}
</script>'''


def fix_homepage(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content

    # 1. Remove the floating Sarah from homepage only
    content = re.sub(r'<!-- Sarah V3 -->.*?</script>\s*', '', content, flags=re.DOTALL)
    content = re.sub(r'<style>\s*#sarah-wrap.*?</style>\s*', '', content, flags=re.DOTALL)
    content = re.sub(r'<div id="sarah-wrap".*?</script>\s*', '', content, flags=re.DOTALL)
    content = re.sub(r'<button id="sarah-minimize".*?</button>', '', content, flags=re.DOTALL)

    # 2. Add lang CSS to head
    content = content.replace('</head>', LANG_CSS + '\n</head>')

    # 3. Replace the stats-bar div + everything after it in hero with lang buttons
    # Find the stats bar and replace with lang buttons
    content = re.sub(
        r'<div class="stats-bar">.*?</div>\s*</div>\s*</div>',
        LANG_BUTTONS + '\n  </div>\n</div>',
        content,
        flags=re.DOTALL,
        count=1
    )

    # 4. Inject hardcoded Sarah after the hero section
    content = re.sub(
        r'(<div style="max-width:1200px;margin:40px auto)',
        HERO_SARAH + '\n\\1',
        content,
        count=1
    )

    return content


# Only fix the homepage index.html files
homepage_files = ['index.html'] + [f'es/index.html', 'zh/index.html', 'ar/index.html', 
                                     'pt/index.html', 'vi/index.html', 'tl/index.html',
                                     'ko/index.html', 'ru/index.html', 'pl/index.html']

fixed = 0
for filepath in homepage_files:
    try:
        content = fix_homepage(filepath)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        fixed += 1
        print(f"  Fixed: {filepath}")
    except FileNotFoundError:
        pass
    except Exception as e:
        print(f"  Error {filepath}: {e}")

print(f"\nFixed {fixed} homepage files.")
