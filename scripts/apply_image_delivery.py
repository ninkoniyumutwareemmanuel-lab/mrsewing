#!/usr/bin/env python3
"""Apply generated responsive candidates without changing source URLs or alt text.
Run optimize_images.py once before this script, then build_homepage.py.
"""
import html
import json
from pathlib import Path
import re
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'_data/image-delivery.json').read_text())
def attributes(name):
    entry=DATA[name]
    candidates={v['width']:v['src'] for v in entry['variants']}
    candidates.setdefault(entry['width'],quote(name))
    srcset=', '.join(f'{src} {width}w' for width,src in sorted(candidates.items()))
    sizes='180px' if name.startswith('MR LOGO') else '(max-width: 700px) 100vw, 50vw'
    return f'width="{entry["width"]}" height="{entry["height"]}" decoding="async" srcset="{srcset}" sizes="{sizes}"'
for path in [*ROOT.glob('*.html'), ROOT/'_templates/homepage.html']:
    if path.name=='index.html': continue
    source=path.read_text()
    first=True
    def update(match):
        global first
        tag=match[0]
        src=re.search(r'\bsrc="([^"]*)"',tag)
        if not src or html.unescape(src[1]) not in DATA: return tag
        name=html.unescape(src[1])
        tag=re.sub(r'\s+(?:width|height|decoding|srcset|sizes)="[^"]*"','',tag)
        tag=tag[:-1]+' '+attributes(name)+'>'
        if not first and 'loading=' not in tag and not name.startswith('MR LOGO'):
            tag=tag[:-1]+' loading="lazy">'
        if not name.startswith('MR LOGO'): first=False
        return tag
    source=re.sub(r'<img\b[^>]*>',update,source)
    # Dynamic galleries need attributes at creation, before the browser picks a source.
    dynamic={'mensuits.html':'photo.file','womensuits.html':'photo.file','suits.html':'imgFile','reviews.html':'encodeURI(item.file)'}
    if path.name in dynamic:
        expression=dynamic[path.name]
        lookup='item.file' if path.name=='reviews.html' else expression
        source=source.replace(f'<img src="${{{expression}}}"',f'<img ${{imageDelivery[{lookup}] || \'\'}} src="${{{expression}}}"')
        source=re.sub(r'    const imageDelivery = [^\n]*;\n', '', source)
        referenced=[name for name in DATA if repr(name) in source or '"'+name+'"' in source]
        mapping={name:attributes(name) for name in referenced}
        source=source.replace('<script>\n\n', '<script>\n', 1)
        source=source.replace('<script>', '<script>\n    const imageDelivery = '+json.dumps(mapping,separators=(',',':'))+';\n',1)
    source=re.sub(r'<video\b(?![^>]*\bpreload=)', '<video preload="none"',source)
    source=source.replace('href="/MR%20LOGO.jpeg" type="image/jpeg"', 'href="/assets/images/logo-icon.png" type="image/png"').replace('href="/MR%20LOGO.jpeg"', 'href="/assets/images/logo-icon.png"')
    if source!=path.read_text():path.write_text(source)
# CSS background uses the full-resolution derivative, preserving the existing crop.
hero=DATA['The Executive Line.jpeg']
full=next((v['src'] for v in hero['variants'] if v['width']==hero['width']),None)
if full:
    path=ROOT/'hero.html';path.write_text(path.read_text().replace("url('The Executive Line.jpeg')",f"url('{full}')"))
    path=ROOT/'_templates/homepage.html';path.write_text(path.read_text().replace('href="The%20Executive%20Line.jpeg"',f'href="{full}"'))
print('Updated authored image delivery; run scripts/build_homepage.py next.')
