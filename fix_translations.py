#!/usr/bin/env python3
"""
fix_translations.py
Fixes over-aggressive translations on inner pages.
Reverts "Prawo Jazdy" back to "License" in English sentences.
Only keeps translations in specific UI elements.
"""

import re, glob

# These are the ONLY strings we should translate on inner pages
# Full sentence replacements are too risky - revert them

REVERT_POLISH = {
    "Driver's Prawo Jazdy": "Driver's License",
    "Foreign Prawo Jazdy": "Foreign License", 
    "Prawo Jazdy Without SSN": "License Without SSN",
    "Foreign Driver's Prawo Jazdy": "Foreign Driver's License",
    "Prawo Jazdy Valid": "License Valid",
    "Car Insurance With a Foreign Driver's Prawo Jazdy": "Car Insurance With a Foreign Driver's License",
    "States That Issue Driver's Prawo Jazdys": "States That Issue Driver's Licenses",
    "How Long Is a Foreign Driver's Prawo Jazdy": "How Long Is a Foreign Driver's License",
    "Driver's Prawo Jazdy for Immigrants": "Driver's License for Immigrants",
    "Prawo Jazdy for Immigrants": "License for Immigrants",
    "get a Prawo Jazdy": "get a License",
    "your Prawo Jazdy": "your License",
    "a Prawo Jazdy": "a License",
    "the Prawo Jazdy": "the License",
    "my Prawo Jazdy": "my License",
    "US Prawo Jazdy": "US License",
}

REVERT_SPANISH = {
    "Driver's Licencia": "Driver's License",
    "Foreign Licencia": "Foreign License", 
    "a Licencia": "a License",
    "the Licencia": "the License",
    "your Licencia": "your License",
    "US Licencia": "US License",
}

REVERT_CHINESE = {
    "Driver's 驾照": "Driver's License",
    "Foreign 驾照": "Foreign License",
}

# Only fix inner pages (not homepages)
lang_reverts = {
    'pl': REVERT_POLISH,
    'es': REVERT_SPANISH,
    'zh': REVERT_CHINESE,
}

fixed = 0
for lang, reverts in lang_reverts.items():
    # Get all non-homepage files for this language
    files = glob.glob(f'{lang}/**/*.html', recursive=True)
    files = [f for f in files if f != f'{lang}/index.html']
    
    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            original = content
            
            for wrong, correct in reverts.items():
                content = content.replace(wrong, correct)
            
            if content != original:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                fixed += 1
        except Exception as e:
            print(f"  Error {filepath}: {e}")

print(f"Reverted over-aggressive translations in {fixed} files.")
