#!/usr/bin/env python3
"""
sarah_page_aware.py
Makes Sarah aware of page context by injecting
page title + URL + language into every API call.
Works for both floating and hardcoded Sarah.
"""

import re, glob

# The key change — in the fetch call, build system dynamically
OLD_FETCH = '''body: JSON.stringify({model:'claude-haiku-4-5-20251001',max_tokens:150,system:S3SYS,messages:s3Hist})'''
NEW_FETCH = '''body: JSON.stringify({model:'claude-haiku-4-5-20251001',max_tokens:150,system:S3SYS+' Page: '+document.title+'. URL: '+window.location.pathname,messages:s3Hist})'''

OLD_FETCH2 = '''body: JSON.stringify({model:'claude-haiku-4-5-20251001',max_tokens:200,system:SARAH_SYS,messages:sarahHistory})'''
NEW_FETCH2 = '''body: JSON.stringify({model:'claude-haiku-4-5-20251001',max_tokens:200,system:SARAH_SYS+' Page: '+document.title+'. URL: '+window.location.pathname,messages:sarahHistory})'''

OLD_FETCH3 = '''body: JSON.stringify({model:'claude-haiku-4-5-20251001',max_tokens:300,system:SARAH_SYS,messages:sarahHistory})'''
NEW_FETCH3 = '''body: JSON.stringify({model:'claude-haiku-4-5-20251001',max_tokens:300,system:SARAH_SYS+' Page: '+document.title+'. URL: '+window.location.pathname,messages:sarahHistory})'''

files = [f for f in glob.glob('**/*.html', recursive=True) if not f.startswith('.')]
print(f"Processing {len(files)} files...")
updated = 0

for filepath in files:
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original = content
        content = content.replace(OLD_FETCH, NEW_FETCH)
        content = content.replace(OLD_FETCH2, NEW_FETCH2)
        content = content.replace(OLD_FETCH3, NEW_FETCH3)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            updated += 1
    except Exception as e:
        print(f"  Error {filepath}: {e}")

print(f"Updated {updated} files with page context.")
