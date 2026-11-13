#!/usr/bin/env python3
"""R46: selection lifetime must preserve every existing page and customer journey.

This is a static boundary check, independent of the mocked browser lifecycle tests.
Only generated asset cache-version queries may change within existing HTML.
"""
from pathlib import Path
from html.parser import HTMLParser
import argparse
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = 'ff7504621306976888a69076eed38538219102ec'
EVIDENCE = Path('/workspace/review/selection-session-expiration-2026-11-13')


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def original(path):
    return git('show', BASE + ':' + path)


def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def cache_normalized(source):
    return re.sub(
        r'((?:src|href)="/assets/[^"?]+\.(?:js|css))\?v=[^"]+', r'\1', source
    )


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.tags, self.headings, self.schemas = [], [], []
        self.current, self.buffer = None, ''
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag in {'title', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'} or (
            tag == 'script' and attrs.get('type') == 'application/ld+json'
        ):
            self.current, self.buffer = tag, ''

    def handle_data(self, value):
        if self.current:
            self.buffer += value

    def handle_endtag(self, tag):
        if self.current == tag:
            if tag == 'script':
                self.schemas.append(json.loads(self.buffer))
            else:
                self.headings.append((tag, self.buffer.strip()))
            self.current = None

    def attrs(self, tag):
        return [attrs for name, attrs in self.tags if name == tag]


def snapshot(source):
    page = Page(source)
    return {
        'headings': page.headings,
        'metadata': page.attrs('meta'),
        'canonicals': [a for a in page.attrs('link') if a.get('rel') == 'canonical'],
        'structuredData': page.schemas,
        'images': page.attrs('img'),
        'links': page.attrs('a'),
        'forms': {tag: page.attrs(tag) for tag in ['form', 'input', 'select', 'textarea']},
        'stagingIndexingScript': re.findall(
            r'<script data-staging-indexing>.*?</script>', source, re.S
        ),
        'normalizedSha256': hashlib.sha256(cache_normalized(source).encode()).hexdigest(),
    }


def fabric_block(source):
    start = "const fabricForm=document.getElementById('fabricChoiceForm');"
    end = "for(const a of document.querySelectorAll('[data-edit-designs]'))"
    assert start in source and end in source, 'Existing fabric implementation markers missing'
    return source.split(start, 1)[1].split(end, 1)[0]


def protected(path):
    # The R46 lifecycle implementation owns only the shared selection script and
    # its generated bundle. Prices, images, CSS, forms, sharing and providers are
    # outside this change. Repository instructions/docs/tests may be updated.
    return (
        path.startswith(('_data/', 'functions/', '_templates/', 'assets/'))
        or Path(path).suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp', '.avif', '.gif', '.svg', '.mp4'}
        or path in {'sitemap.xml', 'robots.txt', '_headers', '_redirects'}
    ) and path not in {'_templates/design-selections.js', 'assets/design-selections.js'}


parser = argparse.ArgumentParser()
parser.add_argument('--capture-baseline', action='store_true')
parser.add_argument('--report')
args = parser.parse_args()
tree = {}
for record in git('ls-tree', '-r', BASE).decode().splitlines():
    metadata, name = record.split('\t', 1)
    _, kind, ident = metadata.split()
    if kind == 'blob':
        tree[name] = ident
html_files = sorted(p for p in tree if p.endswith('.html') and not p.startswith('_templates/'))
protected_files = sorted(p for p in tree if protected(p))
report = {
    'baseline': BASE,
    'mode': 'baseline' if args.capture_baseline else 'preservation',
    'htmlPages': len(html_files),
    'pages': {},
    'protectedFiles': {},
    'fabricControlsAndRoutesPreserved': None,
    'limitations': [
        'Static comparison does not establish runtime expiration or browser storage behavior; separate mocked browser tests cover those scenarios.',
        'This audit does not verify live staging responses, external app support, real customer enquiries, inbox delivery or Google indexing.',
    ],
}
errors = []
for path in html_files:
    before = original(path).decode()
    report['pages'][path] = {'before': snapshot(before)}
    if args.capture_baseline:
        continue
    target = ROOT / path
    if not target.is_file():
        errors.append(path + ': existing page removed')
        continue
    after = target.read_text()
    report['pages'][path]['after'] = snapshot(after)
    if cache_normalized(before) != cache_normalized(after):
        errors.append(path + ': HTML changed beyond an asset cache version')
    if report['pages'][path]['before'] != report['pages'][path]['after']:
        errors.append(path + ': SEO/headings/schema/images/links/forms/indexing changed')

for path in protected_files:
    report['protectedFiles'][path] = {'beforeGitBlob': tree[path]}
    if args.capture_baseline:
        continue
    target = ROOT / path
    after = blob(target.read_bytes()) if target.is_file() else None
    report['protectedFiles'][path]['afterGitBlob'] = after
    if after != tree[path]:
        errors.append(path + ': protected data/image/style/template/provider changed')

if not args.capture_baseline:
    old_fabric = fabric_block(original('_templates/design-selections.js').decode())
    new_fabric = fabric_block((ROOT / '_templates/design-selections.js').read_text())
    report['fabricControlsAndRoutesPreserved'] = old_fabric == new_fabric
    if old_fabric != new_fabric:
        errors.append('Existing per-design fabric controls/rendering/guide and request routes changed')
    # Reconstruct the generated bundle check without writing generated files.
    lifecycle = (ROOT / '_templates/selection-session.js').read_text()
    source = (ROOT / '_templates/design-selections.js').read_text()
    quote = (ROOT / '_templates/selected-suit-quote.js').read_text()
    output = (ROOT / 'assets/design-selections.js').read_text()
    if lifecycle + '\n' + source + '\n' + quote != output:
        errors.append('Generated design-selections.js differs from lifecycle + shared source + unchanged quote source')

report['errors'] = errors
destination = Path(args.report) if args.report else EVIDENCE / (
    'before-preservation.json' if args.capture_baseline else 'preservation.json'
)
destination.parent.mkdir(parents=True, exist_ok=True)
destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
if errors:
    print('\n'.join(errors))
    raise SystemExit(1)
print(('CAPTURED' if args.capture_baseline else 'PASS') +
      f' {len(html_files)} existing HTML pages and {len(protected_files)} protected files; '
      'all metadata/headings/schema/links/photos/forms/indexing, CSS, pricing, sharing, provider and fabric controls preserved')
