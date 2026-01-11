#!/usr/bin/env python3
import os
import re
import argparse
from datetime import datetime

EXTS = {'.htm', '.html', '.php', '.xml'}

def backup_path(path):
    ts = datetime.now().strftime('%Y%m%d%H%M%S')
    return path + '.bak.' + ts

LOGO_SNIPPET = '\n<div id="site-logo"><a href="https://killasnus.store/"><img src="/images/killa-snus-logo.png" alt="Killa Snus" /></a></div>\n'

OG_TEMPLATE = ('\n<meta property="og:title" content="{title}" />\n'
               '<meta property="og:description" content="{desc}" />\n'
               '<meta property="og:url" content="{url}" />\n'
               '<meta property="og:image" content="{image}" />\n')

META_DESC_TEMPLATE = '<meta name="description" content="{desc}" />\n'

REPLACEMENTS = [
    (re.compile(re.escape('https://pussit.com'), re.IGNORECASE), 'https://killasnus.store'),
    (re.compile(re.escape('http://pussit.com'), re.IGNORECASE), 'https://killasnus.store'),
    (re.compile(re.escape('pussit.com'), re.IGNORECASE), 'killasnus.store'),
]

SITE_NAME_PATTERNS = [
    (re.compile(r'\bPussit\b'), 'Killa Snus'),
    (re.compile(r'\bpussit\b'), 'killa snus'),
]


def process_file(path, dry_run=False):
    changed = False
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        text = f.read()

    original = text

    # Basic replacements for domain
    for pat, repl in REPLACEMENTS:
        text, n = pat.subn(repl, text)
        if n:
            changed = True

    # Replace site name patterns
    for pat, repl in SITE_NAME_PATTERNS:
        text, n = pat.subn(repl, text)
        if n:
            changed = True

    # Insert logo snippet once
    if 'killa-snus-logo.png' not in text:
        # Try to insert inside <header> if present
        m = re.search(r'(<header[^>]*>)', text, flags=re.IGNORECASE)
        if m:
            insert_at = m.end()
            text = text[:insert_at] + LOGO_SNIPPET + text[insert_at:]
            changed = True
        else:
            m2 = re.search(r'(<body[^>]*>)', text, flags=re.IGNORECASE)
            if m2:
                insert_at = m2.end()
                text = text[:insert_at] + LOGO_SNIPPET + text[insert_at:]
                changed = True

    # Ensure meta description exists in <head>
    head_match = re.search(r'<head[^>]*>(.*?)</head>', text, flags=re.IGNORECASE | re.DOTALL)
    if head_match:
        head = head_match.group(1)
        if 'name="description"' not in head and 'name=\'description\'' not in head:
            # derive simple description from title or fallback
            title_match = re.search(r'<title>([^<]+)</title>', head, flags=re.IGNORECASE)
            if title_match:
                desc = title_match.group(1).strip() + ' — Killa Snus'
            else:
                desc = 'Killa Snus — quality snus and information.'
            new_meta = META_DESC_TEMPLATE.format(desc=desc)
            # insert after <title> if exists, otherwise after <head>
            if title_match:
                title_end = head_match.start(1) + title_match.end()
                absolute_insert = title_end
                text = text[:absolute_insert] + '\n' + new_meta + text[absolute_insert:]
            else:
                # insert right after <head ...>
                hm = re.search(r'(<head[^>]*>)', text, flags=re.IGNORECASE)
                if hm:
                    pos = hm.end()
                    text = text[:pos] + '\n' + new_meta + text[pos:]
            changed = True

    # Add basic Open Graph tags if missing
    head = re.search(r'<head[^>]*>(.*?)</head>', text, flags=re.IGNORECASE | re.DOTALL)
    if head:
        head_text = head.group(1)
        if 'property="og:title"' not in head_text:
            # derive title/desc/url/image
            title = ''
            tm = re.search(r'<title>([^<]+)</title>', head_text, flags=re.IGNORECASE)
            if tm:
                title = tm.group(1).strip()
            desc = ''
            dm = re.search(r'<meta[^>]+name=["\']description["\'][^>]*content=["\']([^"']+)["\']', head_text, flags=re.IGNORECASE)
            if dm:
                desc = dm.group(1).strip()
            url = ''
            cm = re.search(r'<link[^>]+rel=["\']canonical["\'][^>]*href=["\']([^"']+)["\']', head_text, flags=re.IGNORECASE)
            if cm:
                url = cm.group(1).strip()
            image = '/images/killa-snus-logo.png'
            ogs = OG_TEMPLATE.format(title=title or 'Killa Snus', desc=desc or 'Killa Snus', url=url or 'https://killasnus.store', image=image)
            # insert before </head>
            text = text.replace('</head>', ogs + '\n</head>')
            changed = True

    if changed:
        if not dry_run:
            bak = backup_path(path)
            with open(bak, 'w', encoding='utf-8', errors='ignore') as bf:
                bf.write(original)
            with open(path, 'w', encoding='utf-8', errors='ignore') as f:
                f.write(text)
        return True
    return False


def main(root, dry_run=False):
    total_files = 0
    changed_files = 0
    for dirpath, dirnames, filenames in os.walk(root):
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext in EXTS:
                total_files += 1
                path = os.path.join(dirpath, fn)
                try:
                    if process_file(path, dry_run=dry_run):
                        changed_files += 1
                        print('Modified:', path)
                except Exception as e:
                    print('Error processing', path, e)
    print('\nScan complete. Files scanned:', total_files, 'Modified:', changed_files)

if __name__ == '__main__':
    p = argparse.ArgumentParser(description='Replace site domain/name and add logo/meta tags across site files (backups created).')
    p.add_argument('--root', default='.', help='Root folder to process')
    p.add_argument('--dry-run', action='store_true', help='Do not write changes, only report')
    args = p.parse_args()
    main(args.root, dry_run=args.dry_run)
