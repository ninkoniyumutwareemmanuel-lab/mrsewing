#!/usr/bin/env python3
"""R48: preserve technical SEO, approved content and unrelated customer journeys.

This static boundary test supplements the mocked browser/shared-backend tests.
It never establishes a live Cloudflare, Googlebot or provider response.
"""
from pathlib import Path
from html.parser import HTMLParser
import argparse
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = 'c1428b991b809ee0b8b3289086f07d831c4549c7'
OUT = Path('/workspace/review/shared-fabric-journey-2026-11-13')
AFFECTED_HTML = {'guides/fabrics/index.html', 'services/custom-tailoring/fabric/index.html', 'request/index.html'}
# These existing components implement the owner's newly approved shared journey.
ALLOWED_SOURCE = {
    '_templates/design-selections.js', '_templates/selection-session.js',
    '_templates/selected-suit-quote.js', '_templates/selected-suit-quote.css',
    '_templates/design-selections.css', '_templates/customer-site.js',
    '_templates/request-context.js', '_templates/customer-site.css',
    'assets/design-selections.js', 'assets/design-selections.css',
    'assets/customer-site.js', 'assets/request-context.js', 'assets/customer-site.css',
    'functions/_lib/selected-design-handler.js',
    '_data/fabric-reference-catalogue.json', '_data/customer-release.json',
}
TECHNICAL = {'sitemap.xml', 'robots.txt', '_headers', '_redirects', 'CNAME',
             '404.html', '_templates/not-found.html', 'favicon.ico',
             'assets/images/favicon-192.png', 'assets/images/logo-icon.png',
             '_data/favicon-assets.json'}


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def original(path):
    return git('show', BASE + ':' + path)


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.tags, self.schemas, self.title = [], [], ''
        self.current, self.buffer = None, ''
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag == 'title' or (tag == 'script' and attrs.get('type') == 'application/ld+json'):
            self.current, self.buffer = tag, ''

    def handle_data(self, data):
        if self.current:
            self.buffer += data

    def handle_endtag(self, tag):
        if tag == self.current:
            if tag == 'title':
                self.title = self.buffer.strip()
            else:
                self.schemas.append(json.loads(self.buffer))
            self.current = None

    def attrs(self, tag):
        return [a for t, a in self.tags if t == tag]


def seo(source):
    doc = Document(source)
    return {
        'title': doc.title,
        'meta': doc.attrs('meta'),
        'canonical': [a for a in doc.attrs('link') if a.get('rel') == 'canonical'],
        'structuredData': doc.schemas,
        'images': [{k: a.get(k) for k in ['src', 'srcset', 'alt', 'width', 'height']} for a in doc.attrs('img')],
        'stagingGuard': re.findall(r'<script data-staging-indexing>.*?</script>', source, re.S),
    }


def selection_data(source):
    match = re.search(r'<script id="designSelectionData"[^>]*>(.*?)</script>', source, re.S)
    return json.loads(match[1]) if match else None


def normalize(source):
    # Version refreshes cannot change approved markup or customer information.
    source = re.sub(r'(/assets/[^\s"\'<>]+\.(?:js|css))\?v=[^\s"\'<>]+', r'\1', source)
    return re.sub(r'<script id="designSelectionData"[^>]*>.*?</script>', '__SELECTION_DATA__', source, flags=re.S)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def protected(path):
    return path in TECHNICAL or path.startswith(('_data/', '_templates/', 'assets/', 'functions/')) or Path(path).suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp', '.avif', '.gif', '.svg', '.mp4'}


parser = argparse.ArgumentParser()
parser.add_argument('--capture-baseline', action='store_true')
args = parser.parse_args()
paths = git('ls-tree', '-r', '--name-only', BASE).decode().splitlines()
html = [p for p in paths if p.endswith('.html') and not p.startswith('_templates/')]
report = {'baseline': BASE, 'existingHTML': len(html), 'pages': {}, 'protectedCount': 0,
          'technicalSEOUnchanged': True, 'errors': [], 'liveVerification': False}
for path in html:
    before = original(path).decode()
    report['pages'][path] = {'beforeSEO': seo(before), 'beforeSHA256': sha(before.encode())}
    if args.capture_baseline:
        continue
    target = ROOT / path
    if not target.is_file():
        report['errors'].append(path + ': existing HTML removed')
        continue
    after = target.read_text()
    old_seo, new_seo = seo(before), seo(after)
    # Fabric photographs remain in the guide; the simplified preference page
    # intentionally removes its duplicated fabric-card collection.
    if path == 'services/custom-tailoring/fabric/index.html':
        old_seo.pop('images'); new_seo.pop('images')
    if old_seo != new_seo:
        report['errors'].append(path + ': title/meta/canonical/schema/image identity/staging guard changed')
    if path not in AFFECTED_HTML and normalize(before) != normalize(after):
        report['errors'].append(path + ': unrelated HTML changed beyond asset versions/validated shared selection data')
    old, new = selection_data(before), selection_data(after)
    if bool(old) != bool(new):
        report['errors'].append(path + ': selection context inclusion changed')
    if old and new:
        if old.get('designs') != new.get('designs') or old.get('projects') != new.get('projects'):
            report['errors'].append(path + ': design/project identities or photographs changed')
        for ident, row in old.get('fabrics', {}).items():
            if any(new.get('fabrics', {}).get(ident, {}).get(k) != row.get(k) for k in ['id', 'name', 'tier', 'category', 'image']):
                report['errors'].append(path + ': approved fabric identity/tier/photo changed')

for path in paths:
    if not protected(path) or path in ALLOWED_SOURCE:
        continue
    report['protectedCount'] += 1
    if args.capture_baseline:
        continue
    before = original(path)
    target = ROOT / path
    if not target.is_file():
        report['errors'].append(path + ': protected file removed')
        continue
    after = target.read_bytes()
    # This generated module embeds actual Shop HTML; only existing asset-query
    # versions may refresh, with every commercial restriction/markup preserved.
    if path == 'functions/_lib/shop-preview-pages.js':
        if normalize(before.decode()) != normalize(after.decode()):
            report['errors'].append(path + ': embedded Shop behavior/content changed')
    elif before != after:
        report['errors'].append(path + ': protected data/image/template/provider changed')
    if path in TECHNICAL and before != after:
        report['technicalSEOUnchanged'] = False

if not args.capture_baseline:
    before = json.loads(original('_data/fabric-reference-catalogue.json'))
    after = json.loads((ROOT / '_data/fabric-reference-catalogue.json').read_text())
    fields = ['id', 'category', 'name', 'tier', 'image']
    assert [{k: x[k] for k in fields} for x in before['fabrics']] == [{k: x[k] for k in fields} for x in after['fabrics']], 'Approved fabric assignments/photo references changed'
    before = json.loads(original('_data/customer-release.json'))
    after = json.loads((ROOT / '_data/customer-release.json').read_text())
    before['pages'].pop('/guides/fabrics/', None)
    after['pages'].pop('/guides/fabrics/', None)
    assert before == after, 'Unrelated service/payment/policy facts changed in customer-release.json'
    # Colours are illustrative enquiry preferences, never fabric-specific stock.
    palette = json.loads((ROOT / '_data/fabric-colours.json').read_text())
    expected = {
        'black': 'Black', 'white': 'White', 'grey': 'Grey', 'charcoal': 'Charcoal / Dark Grey',
        'beige': 'Beige', 'khaki': 'Khaki', 'tan': 'Tan', 'navy-blue': 'Navy Blue',
        'blue': 'Blue', 'royal-blue': 'Royal Blue', 'sky-blue': 'Sky Blue', 'ocean-blue': 'Ocean Blue',
        'red': 'Red', 'wine-red': 'Wine Red', 'burgundy': 'Burgundy', 'purple': 'Purple',
        'brown': 'Brown', 'chocolate-brown': 'Chocolate Brown', 'green': 'Green',
        'dark-green': 'Dark Green', 'army-green': 'Army Green', 'olive-green': 'Olive Green',
        'other': 'Other Colour / Ask About a Colour',
    }
    actual = {row['id']: row for row in palette['colours']}
    assert len(palette['colours']) == len(expected) == len(actual), 'Duplicate/missing approved colour preferences'
    assert {key: row['name'] for key, row in actual.items()} == expected, 'Approved colour labels changed'
    hexes = [row['hex'] for key, row in actual.items() if key != 'other']
    assert len(set(hexes)) == 22 and all(re.fullmatch(r'#[0-9A-Fa-f]{6}', value) for value in hexes), 'Distinct illustrative HEX swatches required'
    assert actual['other']['hex'] is None, 'Other colour is an open preference, not an invented shade'
    assert 'not stock' in palette['purpose'].lower(), 'Palette must not imply verified inventory'
    # The measurement illustration implementation is shared with fabrics and
    # must not be redesigned by an ordinary suit journey change.
    old = original('scripts/customer_guides.py').decode()
    new = (ROOT / 'scripts/customer_guides.py').read_text()
    measurement = lambda s: s.split('def measurements():', 1)[1].split('def options():', 1)[0]
    assert measurement(old) == measurement(new), 'Measurements Guide function changed'

OUT.mkdir(parents=True, exist_ok=True)
(OUT / ('before-preservation.json' if args.capture_baseline else 'preservation.json')).write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
if report['errors']:
    print('\n'.join(report['errors']))
    raise SystemExit(1)
print(('CAPTURED' if args.capture_baseline else 'PASS') + f' {len(html)} existing HTML SEO/image identities; unrelated pages and {report["protectedCount"]} protected files; R47 technicalSEO preserved')
