#!/usr/bin/env python3
"""
fix_sidebar.py
Removes eSolicitors leftover links from all built HTML pages.
Run in repo root: python3 fix_sidebar.py
"""

import re, os, glob

REMOVE_PATTERNS = [
    r'<a href="/[^"]*immigration-law/?"[^>]*>🛂 Immigration</a>',
    r'<a href="/[^"]*rights/?"[^>]*>✊ Rights</a>',
    r'<a href="/[^"]*workers-rights/?"[^>]*>👷 Workers</a>',
    r'<a href="/[^"]*criminal-law/?"[^>]*>⚖️ Criminal</a>',
    r'<a href="/[^"]*family-law/?"[^>]*>👨‍👩‍👧 Family</a>',
    r'<a href="/[^"]*personal-injury/?"[^>]*>🏥 Injury</a>',
    r'<li><a href="/[^"]*immigration-law/?"[^>]*>Immigration Law</a></li>',
    r'<li><a href="/[^"]*criminal-law/?"[^>]*>Criminal Law</a></li>',
    r'<li><a href="/[^"]*personal-injury/?"[^>]*>Personal Injury</a></li>',
    r'<li><a href="/[^"]*workers-rights/?"[^>]*>Workers. Rights</a></li>',
    r'<li><a href="/[^"]*family-law/?"[^>]*>Family Law</a></li>',
    r'<li><a href="/[^"]*property/?"[^>]*>Property.*?Housing</a></li>',
    r'<li><a href="/[^"]*wills-and-estates/?"[^>]*>Wills.*?Estates</a></li>',
    r'<li><a href="/[^"]*debt-law/?"[^>]*>Debt Law</a></li>',
    r'<li><a href="/[^"]*business-law/?"[^>]*>Business Law</a></li>',
    r'<li><a href="/[^"]*rights/?"[^>]*>Know Your Rights</a></li>',
    r'<li><a href="/[^"]*ice-at-door/?"[^>]*>ICE at Your Door</a></li>',
    r'<li><a href="/[^"]*deportation/defense/?"[^>]*>Deportation Defense</a></li>',
    r'<li><a href="/[^"]*immigration-law/asylum/?"[^>]*>Asylum Guide</a></li>',
    r'<li><a href="/[^"]*immigration-law/daca/?"[^>]*>DACA Information</a></li>',
    r'<li><a href="/[^"]*undocumented-worker-rights/?"[^>]*>Undocumented Worker Rights</a></li>',
    r'<h4>Key Topics</h4>\s*<ul>\s*</ul>',
    r'<div class="footer-col">\s*<h4>Key Topics</h4>\s*<ul>\s*</ul>\s*</div>',
    r'<h4>Key Topics</h4>',
]

def fix_file(fp):
    with open(fp, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    original = content
    for p in REMOVE_PATTERNS:
        content = re.sub(p, '', content, flags=re.DOTALL)
    content = re.sub(r'\n{3,}', '\n\n', content)
    if content != original:
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

files = [f for f in glob.glob('**/*.html', recursive=True) if not f.startswith('.')]
print(f"Processing {len(files)} HTML files...")
fixed = sum(1 for f in files if fix_file(f))
print(f"Fixed {fixed} files. Commit and push.")
