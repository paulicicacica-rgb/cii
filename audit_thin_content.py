#!/usr/bin/env python3
"""
Audits HTML pages for thin content (< THIN_THRESHOLD words).

Usage:
  python3 audit_thin_content.py .
  python3 audit_thin_content.py /path/to/repo
  python3 audit_thin_content.py . --threshold 200
  python3 audit_thin_content.py . --lang pl
  python3 audit_thin_content.py . --show-ok

Skips: node_modules, .git, .vercel, dist, __pycache__
"""

import os, re, sys, argparse

THIN_THRESHOLD = 150

SKIP_DIRS  = {'node_modules', '.git', '.vercel', 'dist', '__pycache__'}
SKIP_PATHS = set()
SKIP_PATTERNS = [r'googlea\w+\.html']

LANG_CODES = ['pl', 'ro', 'pt', 'pt-br', 'es', 'ar', 'ru', 'en']

def get_lang(rel_path):
    parts = rel_path.replace('\\', '/').split('/')
    for lang in LANG_CODES:
        if parts[0] == lang:
            return lang
    return 'en'

def should_skip(rel):
    rel = rel.replace('\\', '/')
    if rel in SKIP_PATHS:
        return True
    for pat in SKIP_PATTERNS:
        if re.search(pat, rel):
            return True
    return False

def extract_word_count(html):
    html2 = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
    html2 = re.sub(r'<script[^>]*>.*?</script>', '', html2, flags=re.DOTALL)
    html2 = re.sub(r'<nav[^>]*>.*?</nav>', '', html2, flags=re.DOTALL)
    html2 = re.sub(r'<footer[^>]*>.*?</footer>', '', html2, flags=re.DOTALL)
    html2 = re.sub(r'<div class="breadcrumb"[^>]*>.*?</div>', '', html2, flags=re.DOTALL)
    text  = re.sub(r'<[^>]+>', ' ', html2)
    text  = re.sub(r'\s+', ' ', text).strip()
    return len([w for w in text.split() if len(w) > 1])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('repo_root', nargs='?', default='.')
    parser.add_argument('--threshold', type=int, default=THIN_THRESHOLD,
                        help=f'Word count threshold (default: {THIN_THRESHOLD})')
    parser.add_argument('--lang', type=str, default='',
                        help='Filter by language code (e.g. pl, ro, en)')
    parser.add_argument('--show-ok', action='store_true',
                        help='Also show pages that pass the threshold')
    args = parser.parse_args()

    repo_root  = args.repo_root
    threshold  = args.threshold
    lang_filter = args.lang.strip()

    thin  = []
    ok    = []
    errors = []
    total  = 0

    for root, dirs, files in os.walk(repo_root):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for fname in files:
            if not fname.endswith('.html'):
                continue
            fpath = os.path.join(root, fname)
            rel   = os.path.relpath(fpath, repo_root).replace('\\', '/')
            if should_skip(rel):
                continue
            lang = get_lang(rel)
            if lang_filter and lang != lang_filter:
                continue
            total += 1
            try:
                with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                    html = f.read()
                count = extract_word_count(html)
                if count < threshold:
                    thin.append((count, rel, lang))
                else:
                    ok.append((count, rel, lang))
            except Exception as e:
                errors.append((rel, str(e)))

    # Sort thin pages by word count ascending (worst first)
    thin.sort(key=lambda x: x[0])

    print(f'\n{"="*60}')
    print(f'THIN CONTENT AUDIT — threshold: {threshold} words')
    print(f'Repo: {os.path.abspath(repo_root)}')
    if lang_filter:
        print(f'Language filter: {lang_filter}')
    print(f'{"="*60}')
    print(f'Total pages scanned : {total}')
    print(f'Thin pages (<{threshold}w) : {len(thin)}')
    print(f'OK pages             : {len(ok)}')
    print(f'Errors               : {len(errors)}')
    print(f'{"="*60}\n')

    if thin:
        print(f'THIN PAGES ({len(thin)}):')
        print(f'{"-"*60}')
        # Group by language
        by_lang = {}
        for count, rel, lang in thin:
            by_lang.setdefault(lang, []).append((count, rel))

        for lang in sorted(by_lang.keys()):
            pages = by_lang[lang]
            print(f'\n  [{lang.upper()}] — {len(pages)} thin pages')
            for count, rel in pages:
                bar = '█' * min(count // 10, 20)
                print(f'    {count:4d}w  {bar:<20}  {rel}')

    if args.show_ok and ok:
        ok.sort(key=lambda x: x[0])
        print(f'\nOK PAGES ({len(ok)}):')
        print(f'{"-"*60}')
        for count, rel, lang in ok:
            print(f'  {count:4d}w  [{lang}]  {rel}')

    if errors:
        print(f'\nERRORS ({len(errors)}):')
        for rel, err in errors:
            print(f'  {rel}: {err}')

    print(f'\n{"="*60}')
    print(f'Run fill_thin_pages.py to fix {len(thin)} thin pages.')
    print(f'{"="*60}\n')

    # Exit code 1 if thin pages found (useful for CI)
    sys.exit(1 if thin else 0)

if __name__ == '__main__':
    main()
