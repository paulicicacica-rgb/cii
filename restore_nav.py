#!/usr/bin/env python3
"""
restore_nav.py
Restores correct car insurance nav and footer links to all HTML pages.
Replaces the empty footer left by the broken fix_sidebar.py script.
"""

import re, glob

OLD_FOOTER_COL1 = '''      <div class="footer-col">
        <h4>Practice Areas</h4>
        <ul>
          
          
          
          
          
        </ul>
      </div>'''

OLD_FOOTER_COL2 = '''      <div class="footer-col">
        <ul style="margin-top:22px">
          
          
          
          
          
        </ul>
      </div>'''

OLD_FOOTER_COL3_EMPTY = '''      <div class="footer-col">
        
      </div>'''

def get_lang_prefix(filepath):
    """Extract language prefix from file path."""
    parts = filepath.replace('\\', '/').split('/')
    known_langs = ['es','zh','ar','pt','vi','tl','ko','ru','pl']
    for part in parts:
        if part in known_langs:
            return part + '/'
    return ''

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    original = content
    prefix = get_lang_prefix(filepath)
    
    # Fix nav - restore car insurance nav links
    old_nav = '<nav>\n      \n      \n      \n      \n      \n      \n    </nav>'
    new_nav = f'''<nav>
      <a href="/{prefix}getting-insured/">🚗 Get Insured</a>
      <a href="/{prefix}questions/">❓ Questions</a>
      <a href="/{prefix}by-status/">📋 By Status</a>
      <a href="/{prefix}after-accident/">🚨 Accidents</a>
      <a href="/{prefix}states/">📍 By State</a>
      <a href="/{prefix}license/">🪪 License</a>
    </nav>'''
    content = content.replace(old_nav, new_nav)

    # Fix footer col 1
    new_col1 = f'''      <div class="footer-col">
        <h4>Get Insured</h4>
        <ul>
          <li><a href="/{prefix}getting-insured/">Getting Insured</a></li>
          <li><a href="/{prefix}getting-insured/no-ssn/">No SSN Required</a></li>
          <li><a href="/{prefix}getting-insured/itin/">Use Your ITIN</a></li>
          <li><a href="/{prefix}getting-insured/foreign-license/">Foreign License</a></li>
          <li><a href="/{prefix}getting-insured/undocumented/">Undocumented</a></li>
        </ul>
      </div>'''
    
    # Fix footer col 2
    new_col2 = f'''      <div class="footer-col">
        <ul style="margin-top:22px">
          <li><a href="/{prefix}by-status/">By Immigration Status</a></li>
          <li><a href="/{prefix}foreign-license/">Foreign License</a></li>
          <li><a href="/{prefix}after-accident/">After an Accident</a></li>
          <li><a href="/{prefix}coverage/">Coverage Explained</a></li>
          <li><a href="/{prefix}save-money/">Save Money</a></li>
        </ul>
      </div>'''

    # Fix footer col 3
    new_col3 = f'''      <div class="footer-col">
        <h4>Top Questions</h4>
        <ul>
          <li><a href="/{prefix}questions/can-undocumented-get-car-insurance/">Undocumented Insurance</a></li>
          <li><a href="/{prefix}questions/will-insurance-company-call-ice/">Will They Call ICE?</a></li>
          <li><a href="/{prefix}questions/what-is-itin-car-insurance/">ITIN Insurance Guide</a></li>
          <li><a href="/{prefix}questions/does-geico-require-ssn/">GEICO Without SSN</a></li>
          <li><a href="/{prefix}states/">All 50 States</a></li>
        </ul>
      </div>'''

    # Apply footer fixes using regex to catch variations
    content = re.sub(
        r'<div class="footer-col">\s*<h4>Practice Areas</h4>\s*<ul>[\s]*</ul>\s*</div>',
        new_col1, content, flags=re.DOTALL)
    
    content = re.sub(
        r'<div class="footer-col">\s*<ul style="margin-top:22px">[\s]*</ul>\s*</div>',
        new_col2, content, flags=re.DOTALL)

    content = re.sub(
        r'<div class="footer-col">\s*\n\s*</div>',
        new_col3, content, flags=re.DOTALL)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

files = [f for f in glob.glob('**/*.html', recursive=True) if not f.startswith('.')]
print(f"Processing {len(files)} HTML files...")
fixed = 0
for f in files:
    try:
        if fix_file(f):
            fixed += 1
    except Exception as e:
        print(f"Error {f}: {e}")

print(f"Fixed {fixed} files. Commit and push.")
