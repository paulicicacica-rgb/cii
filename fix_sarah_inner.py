#!/usr/bin/env python3
"""
fix_sarah_inner.py
Makes Sarah on inner pages:
- Bigger panel (400px wide)
- Auto-opens after 3 seconds
- Larger message area
"""

import re, glob

files = [f for f in glob.glob('**/*.html', recursive=True) 
         if not f.startswith('.') and f not in [
             'index.html','es/index.html','zh/index.html','ar/index.html',
             'pt/index.html','ru/index.html','pl/index.html','vi/index.html',
             'tl/index.html','ko/index.html'
         ]]

print(f"Processing {len(files)} inner pages...")
updated = 0

for filepath in files:
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        original = content

        # Make Sarah panel wider
        content = content.replace('width: 340px', 'width: 380px')
        content = content.replace('width:340px', 'width:380px')
        
        # Make message area taller
        content = content.replace('max-height:200px', 'max-height:260px')
        content = content.replace('max-height: 200px', 'max-height: 260px')

        # Auto-open after 3 seconds
        if 'sarahOpen=false' in content and 'setTimeout' not in content:
            content = content.replace(
                'var sarahOpen=false',
                'var sarahOpen=false;\nsetTimeout(function(){if(!sarahOpen){toggleSarah();}}, 3000);'
            )

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            updated += 1
    except Exception as e:
        print(f"  Error {filepath}: {e}")

print(f"Updated {updated} inner pages.")
