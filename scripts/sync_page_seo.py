#!/usr/bin/env python3
"""Apply reviewed page titles/descriptions without touching canonical or JSON-LD.

Only existing title, description and matching social-title/description fields are
updated. Regenerate index.html afterward; --check is read-only.
"""
import argparse
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
META = re.compile(r'<meta\b[^>]*>', re.I)


def apply(source, data):
    source, count = re.subn(r'<title>.*?</title>', lambda _: '<title>' + escape(data['title'], quote=False) + '</title>', source, flags=re.S | re.I)
    if count != 1:
        raise ValueError('A standalone page needs exactly one title')
    descriptions = 0

    def replace(match):
        nonlocal descriptions
        tag = match[0]
        key = re.search(r'\b(?:name|property)=["\']([^"\']+)["\']', tag, re.I)
        if not key:
            return tag
        key = key[1].lower()
        if key in ('description', 'og:description', 'twitter:description'):
            value = data['description']
            descriptions += key == 'description'
        elif key in ('og:title', 'twitter:title'):
            value = data['title']
        else:
            return tag
        tag, changed = re.subn(r'\bcontent=(["\'])(.*?)\1', lambda _: 'content="' + escape(value, quote=True) + '"', tag, flags=re.S | re.I)
        if changed != 1:
            raise ValueError('SEO meta field needs one content attribute')
        return tag

    source = META.sub(replace, source)
    if descriptions != 1:
        raise ValueError('A standalone page needs exactly one meta description')
    return source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    pages = json.loads((ROOT / '_data/page-seo.json').read_text())
    stale = []
    for name, data in pages.items():
        if name in json.loads((ROOT/'_data/route-aliases.json').read_text()):continue
        path = ROOT / ('_templates/homepage.html' if name == 'index.html' else name)
        old = path.read_text()
        new = apply(old, data)
        if old != new:
            stale.append(name)
            if not args.check:
                path.write_text(new)
    if args.check and stale:
        raise SystemExit('Page metadata is out of date: ' + ', '.join(stale))
    print('PASS: reviewed page metadata is synchronized.' if args.check else f'Updated metadata for {len(stale)} source pages; regenerate index.html next.')


if __name__ == '__main__':
    main()
