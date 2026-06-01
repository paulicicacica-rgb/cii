#!/usr/bin/env python3
"""
fix_nav_final.py
Remove nav lang-switcher from ALL pages (causes double pills)
Keep only the hero lang-grid pills on homepages
"""

import re, glob

files = [f for f in glob.glob('**/*.html', recursive=True) if not f.startswith('.')]
print(f"Processing {len(files)} files...")
fixed = 0

for filepath in files:
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        original = content

        # Remove the lang-switcher div from header nav
        content = re.sub(
            r'<div class="lang-switcher">.*?</div>',
            '',
            content,
            flags=re.DOTALL
        )

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            fixed += 1
    except Exception as e:
        print(f"  Error {filepath}: {e}")

print(f"Removed nav lang-switcher from {fixed} files.")
