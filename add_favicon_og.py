#!/usr/bin/env python3
"""
add_favicon_og.py
Adds favicon and OG image tags to all HTML pages.
"""

import re, glob

FAVICON_TAGS = '''  <link rel="icon" type="image/png" href="/favicon.png">
  <link rel="shortcut icon" href="/favicon.png">
  <meta property="og:image" content="https://carinsuranceimmigrants.us/og-image.jpg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:type" content="image/jpeg">
  <meta name="twitter:image" content="https://carinsuranceimmigrants.us/og-image.jpg">
  <meta name="twitter:card" content="summary_large_image">'''

files = [f for f in glob.glob('**/*.html', recursive=True) if not f.startswith('.')]
print(f"Processing {len(files)} files...")
updated = 0

for filepath in files:
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        original = content

        # Remove old favicon/og tags if any
        content = re.sub(r'<link[^>]*favicon[^>]*>', '', content)
        content = re.sub(r'<meta[^>]*og:image[^>]*>', '', content)
        content = re.sub(r'<meta[^>]*twitter:image[^>]*>', '', content)
        content = re.sub(r'<meta[^>]*twitter:card[^>]*>', '', content)

        # Add new ones
        content = content.replace('</head>', FAVICON_TAGS + '\n</head>', 1)

        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            updated += 1
    except Exception as e:
        print(f"  Error {filepath}: {e}")

print(f"Updated {updated} files.")
