#!/usr/bin/env python3
"""R47: local technical SEO boundaries; never evidence of a live Googlebot response."""
from collections import deque
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
import argparse
import hashlib
import json
import re
import struct
import subprocess
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASELINE = 'ce312f68b9ace4bd7d5df0334589007ff329a0e8'
DOMAIN = 'https://mrsewingfashion.com'
OUT = Path('/workspace/review/technical-seo-2026-11-13')
PRIORITY = ['/', '/services/custom-tailoring/', '/services/alterations/',
            '/services/garment-care/', '/services/mobile-fitting/', '/services/vip/',
            '/mensuits/', '/womensuits/']
RETIRED = ['/product-category/sewing-for-you/', '/product/sunday-dresses-church/feed/',
           '/product/workshop-work-clothes/feed/', '/feed/', '/comments/feed/']


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.tags, self.schemas, self.headings = [], [], []
        self.current, self.buffer, self.main, self.main_text = None, '', 0, []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag == 'main':
            self.main += 1
        if tag in {'title', 'h1', 'h2', 'h3'} or (tag == 'script' and attrs.get('type') == 'application/ld+json'):
            self.current, self.buffer = tag, ''

    def handle_data(self, text):
        if self.current:
            self.buffer += text
        if self.main and self.current != 'script':
            self.main_text.append(text)

    def handle_endtag(self, tag):
        if tag == 'main':
            self.main -= 1
        if tag == self.current:
            if tag == 'script':
                self.schemas.append(json.loads(self.buffer))
            else:
                self.headings.append((tag, self.buffer.strip()))
            self.current = None

    def attrs(self, tag):
        return [attrs for name, attrs in self.tags if name == tag]


def route_file(route):
    path = ROOT / unquote(route).lstrip('/')
    return path / 'index.html' if route.endswith('/') or path.is_dir() else path


def source_from_git(path):
    return subprocess.check_output(['git', 'show', BASELINE + ':' + path], cwd=ROOT).decode()


def metadata(doc):
    return {'headings': doc.headings, 'meta': doc.attrs('meta'),
            'canonical': [a for a in doc.attrs('link') if a.get('rel') == 'canonical'],
            'schema': doc.schemas,
            'images': doc.attrs('img'), 'base': doc.attrs('base')}


def local_target(value, route):
    target = urlsplit(urljoin(DOMAIN + route, value))
    if target.scheme not in {'http', 'https'} or target.netloc not in {'mrsewingfashion.com', 'www.mrsewingfashion.com'}:
        return None
    return target.path


def resources(doc, route):
    base = doc.attrs('base')
    route = urlsplit(urljoin(DOMAIN + route, base[0]['href'])).path if base else route
    found = []
    for tag, a in doc.tags:
        values = []
        if tag == 'img':
            values.append(a.get('src'))
            values.extend(part.strip().split()[0] for part in a.get('srcset', '').split(',') if part.strip())
        if tag == 'script':
            values.append(a.get('src'))
        if tag == 'link' and a.get('rel') in {'stylesheet', 'icon', 'shortcut icon', 'preload'}:
            values.append(a.get('href'))
        for value in filter(None, values):
            target = local_target(value, route)
            if target:
                found.append(target)
    return sorted(set(found))


def normalize_icon_links(source):
    def normalize(match):
        tag = match.group(0)
        attrs = Document(tag).attrs('link')[0]
        if 'icon' in attrs.get('rel', '').split():
            tag = re.sub(r'href=[\"\'][^\"\']*[\"\']', 'href="__approved_favicon__"', tag)
            return re.sub(r'type=[\"\'][^\"\']*[\"\']', 'type="__approved_favicon_type__"', tag)
        return tag
    return re.sub(r'<link\b[^>]*>', normalize, source, flags=re.I)


def check_standard_icons(source):
    for attrs in Document(source).attrs('link'):
        if 'icon' in attrs.get('rel', '').split():
            assert attrs.get('href') == '/assets/images/favicon-192.png', 'Unexpected standard favicon destination'
            assert attrs.get('type') in {None, 'image/png'}, 'Any declared favicon MIME must match PNG bytes'


def preserved_paths():
    names = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', BASELINE], cwd=ROOT, text=True).splitlines()
    html = [p for p in names if p.endswith('.html') and not p.startswith('_templates/')]
    protected = [p for p in names if p.startswith(('_data/', '_templates/', 'assets/', 'functions/')) or Path(p).suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp', '.avif', '.gif', '.svg', '.mp4'}]
    return html, protected


def check_icon():
    path = ROOT / 'favicon.ico'
    assert path.is_file(), 'Root favicon.ico must exist after the approved repair'
    data = path.read_bytes()
    reserved, kind, count = struct.unpack_from('<HHH', data)
    assert (reserved, kind) == (0, 1) and 1 <= count <= 16, 'Invalid ICO header'
    sizes = []
    for i in range(count):
        width, height, colors, reserved, planes, bit_count, size, offset = struct.unpack_from('<BBBBHHII', data, 6 + 16 * i)
        width, height = width or 256, height or 256
        assert width == height and width > 0 and size > 0, 'ICO entries must be square, nonempty'
        assert offset >= 6 + 16 * count and offset + size <= len(data), 'Truncated ICO entry'
        content = data[offset:offset + size]
        assert content.startswith(b'\x89PNG\r\n\x1a\n') or struct.unpack_from('<I', content)[0] >= 40, 'Invalid ICO image payload'
        sizes.append(width)
    assert {16, 32, 48}.issubset(sizes), 'Favicon must support standard16/32/48px sizes'
    return {'bytes': len(data), 'sizes': sorted(sizes), 'sha256': hashlib.sha256(data).hexdigest()}


parser = argparse.ArgumentParser()
parser.add_argument('--capture-baseline', action='store_true')
parser.add_argument('--report')
args = parser.parse_args()
OUT.mkdir(parents=True, exist_ok=True)
report = {'baseline': BASELINE, 'scope': 'Local initial HTML and configuration only; live HTTP/headers/rendering/indexing are separate evidence.',
          'priority': {}, 'errors': [], 'noRealRequests': True}
for route in PRIORITY:
    file = route_file(route)
    before = Document(source_from_git(str(file.relative_to(ROOT))))
    report['priority'][route] = {'before': metadata(before)}
    if args.capture_baseline:
        continue
    doc = Document(file.read_text())
    report['priority'][route]['after'] = metadata(doc)
    assert metadata(doc) == metadata(before), route + ': approved SEO/headings/schema/images changed'
    robots = [a.get('content') for a in doc.attrs('meta') if a.get('name') == 'robots']
    assert robots == ['index, follow'], route + ': intended production source robots'
    assert [a.get('href') for a in doc.attrs('link') if a.get('rel') == 'canonical'] == [DOMAIN + route]
    assert len([h for h in doc.headings if h[0] == 'h1']) == 1
    main_text = ' '.join(' '.join(doc.main_text).split())
    assert len(main_text) >= 150, route + ': substantive initial HTML main content missing'
    local_resources = resources(doc, route)
    for target in local_resources:
        assert route_file(target).is_file(), route + ': missing local resource ' + target
    report['priority'][route]['initialMainTextCharacters'] = len(main_text)
    report['priority'][route]['localResources'] = local_resources

html_paths, protected_paths = preserved_paths()
report['htmlPreservation'] = {}
for path in html_paths:
    old = source_from_git(path)
    value = {'beforeNormalizedSHA256': hashlib.sha256(normalize_icon_links(old).encode()).hexdigest()}
    if not args.capture_baseline:
        after = (ROOT / path).read_text()
        assert normalize_icon_links(old) == normalize_icon_links(after), path + ': HTML changed beyond approved icon href/type correction'
        check_standard_icons(after)
        value['afterNormalizedSHA256'] = hashlib.sha256(normalize_icon_links(after).encode()).hexdigest()
    report['htmlPreservation'][path] = value
report['protectedFiles'] = {}
for path in protected_paths:
    old = subprocess.check_output(['git', 'show', BASELINE + ':' + path], cwd=ROOT)
    value = {'beforeSHA256': hashlib.sha256(old).hexdigest()}
    if not args.capture_baseline:
        current = (ROOT / path).read_bytes()
        if path == '_data/collection-image-inventory.json':
            previous, updated = json.loads(old), json.loads(current)
            assert {k: v for k, v in previous.items() if k != 'images'} == {k: v for k, v in updated.items() if k != 'images'}
            assert updated['images'][:-1] == previous['images'] and len(updated['images']) == len(previous['images']) + 1
            added = updated['images'][-1]
            assert added['originalImagePath'] == 'assets/images/favicon-192.png' and added['sourceOriginal'] == 'assets/images/logo-icon.png'
            assert added['designId'] is None and added['galleryLocation'] is None and added['provenance'] == 'not_a_design_record' and added['excludedReason']
            value['approvedDifference'] = 'One excluded non-design favicon derivative appended; every previous record and all other fields unchanged'
        elif path == 'functions/_lib/shop-preview-pages.js':
            old_prefix, old_values = old.decode().split('export const pages=', 1)
            new_prefix, new_values = current.decode().split('export const pages=', 1)
            assert old_prefix == new_prefix
            previous = json.loads(old_values.strip().removesuffix(';'))
            updated = json.loads(new_values.strip().removesuffix(';'))
            assert previous.keys() == updated.keys()
            assert all(normalize_icon_links(previous[k]) == normalize_icon_links(updated[k]) for k in previous)
            for html in updated.values():
                check_standard_icons(html)
            value['approvedDifference'] = 'Generated server-only Shop HTML values normalize favicon href/type only; module structure and every other byte preserved'
        else:
            assert current == old, path + ': protected customer data/template/asset/provider changed'
        value['afterSHA256'] = hashlib.sha256(current).hexdigest()
    report['protectedFiles'][path] = value

if not args.capture_baseline:
    urls = [x.text for x in ET.parse(ROOT / 'sitemap.xml').findall('.//{*}loc')]
    assert len(urls) == len(set(urls))
    assert all(u.startswith(DOMAIN + '/') and '.pages.dev' not in u for u in urls)
    routes = {urlsplit(u).path for u in urls}
    assert set(PRIORITY).issubset(routes)
    assert '/services/' not in routes, 'Intentionally noindex Services directory must not enter sitemap'
    directory = Document(route_file('/services/').read_text())
    assert any(a.get('name') == 'robots' and 'noindex' in a.get('content', '') for a in directory.attrs('meta'))
    graph = {}
    for route in routes:
        doc = Document(route_file(route).read_text())
        assert [a.get('href') for a in doc.attrs('link') if a.get('rel') == 'canonical'] == [DOMAIN + route]
        assert any(a.get('name') == 'robots' and a.get('content') == 'index, follow' for a in doc.attrs('meta'))
        base_route = urlsplit(urljoin(DOMAIN + route, doc.attrs('base')[0]['href'])).path if doc.attrs('base') else route
        graph[route] = sorted({target for a in doc.attrs('a') if (target := local_target(a.get('href', ''), base_route)) in routes})
    distances, queue = {'/': 0}, deque(['/'])
    while queue:
        route = queue.popleft()
        for target in graph[route]:
            if target not in distances:
                distances[target] = distances[route] + 1
                queue.append(target)
    assert set(PRIORITY).issubset(distances), 'Important services must be linked in ordinary initial HTML'
    report['priorityDiscoveryDepth'] = {r: distances[r] for r in PRIORITY}
    report['sitemap'] = {'uniqueCanonicalURLs': len(urls), 'servicesDirectoryExcluded': True}
    headers = (ROOT / '_headers').read_text()
    blocks = {}
    for line in headers.splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        if not line[0].isspace():
            current = line.strip(); blocks[current] = []
        else:
            blocks[current].append(line.strip())
    noindex_patterns = [pattern for pattern, rules in blocks.items() if any('x-robots-tag:' in r.lower() and 'noindex' in r.lower() for r in rules)]
    assert noindex_patterns and all(p.startswith('https://') and '.mrsewing-staging.pages.dev/' in p.replace('https://mrsewing-staging.pages.dev/', 'https://root.mrsewing-staging.pages.dev/') for p in noindex_patterns), 'No global or production noindex HTTP rule allowed'
    assert 'https://mrsewing-staging.pages.dev/*' in noindex_patterns
    assert any(':preview.mrsewing-staging.pages.dev/*' in p or '*.mrsewing-staging.pages.dev/*' in p for p in noindex_patterns)
    assert 'Sitemap: ' + DOMAIN + '/sitemap.xml' in (ROOT / 'robots.txt').read_text()
    report['stagingNoindex'] = {'scopedPatterns': noindex_patterns, 'productionApexAndWWWNotMatched': True, 'runtimeHeaderResponseVerified': False}
    redirects = {}
    for line in (ROOT / '_redirects').read_text().splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        fields = line.split()
        assert len(fields) == 3, 'Unexpected redirect rule shape'
        old, target, status = fields
        assert old not in redirects, 'Duplicate redirect source: ' + old
        assert status == '301' and '*' not in old and ':' not in old, 'Only exact approved permanent aliases permitted'
        assert target.startswith('/') and target != old, 'Redirect loop/external target: ' + old
        redirects[old] = target
    for old, target in redirects.items():
        assert target not in redirects, 'Redirect chain: ' + old + ' -> ' + target
        assert route_file(urlsplit(target).path).is_file(), 'Missing redirect target: ' + target
    for old in RETIRED:
        assert old not in redirects, 'Unrelated WordPress URL must retain genuine missing status: ' + old
        assert not route_file(old).exists()
    report['historicalRoutes'] = {'retiredWithoutInventedReplacement': RETIRED, 'redirectRules': len(redirects), 'exactOnlyNoChains': True}
    report['favicon'] = check_icon()
    square = (ROOT / 'assets/images/favicon-192.png').read_bytes()
    assert square.startswith(b'\x89PNG\r\n\x1a\n') and struct.unpack_from('>II', square, 16) == (192, 192)
    missing = Document((ROOT / '404.html').read_text())
    assert any(a.get('name') == 'robots' and a.get('content') == 'noindex, follow' for a in missing.attrs('meta'))
    assert DOMAIN + '/404.html' not in urls and DOMAIN + '/404/' not in urls
    assert len([h for h in missing.headings if h[0] == 'h1']) == 1
    assert not any(a.get('http-equiv', '').lower() == 'refresh' for a in missing.attrs('meta')), '404 must not soft-redirect elsewhere'
    assert not missing.attrs('script'), '404 must not run a client-side homepage redirect'
    for a in missing.attrs('a'):
        target = local_target(a.get('href', ''), '/')
        if target:
            assert route_file(target).is_file(), '404 navigation target missing: ' + target
    report['explicit404'] = {'noindex': True, 'excludedFromSitemap': True, 'workingNavigation': True, 'liveResponseStatusVerified': False}
    protected = ['assets/design-selections.js', 'assets/design-selections.css', '_templates/design-selections.js', '_templates/selection-session.js', '_templates/selected-suit-quote.js', '_templates/design-selection-sharing.js', '_templates/customer-site.js', 'functions/_lib/selected-design-handler.js', '_data/suit-package-prices.json', '_data/tuxedo-package-prices.json']
    for path in protected:
        old = subprocess.check_output(['git', 'show', BASELINE + ':' + path], cwd=ROOT)
        assert (ROOT / path).read_bytes() == old, path + ': unrelated journey/pricing/provider changed'
    report['protectedJourneyFiles'] = protected

report['limitations'] = ['Local source/build tests do not establish production status codes, response headers, Cloudflare host behavior or Googlebot delivery.', 'Valid metadata/JSON-LD and sitemap inclusion do not guarantee indexing or rich-result eligibility.']
destination = Path(args.report) if args.report else OUT / ('before-priority-pages.json' if args.capture_baseline else 'technical-static.json')
destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
print('CAPTURED priority8 initialHTML metadata baseline' if args.capture_baseline else 'PASS priority8 initialHTML/SEO preservation, discovery/resources, sitemap/noindex agreement, scoped staging headers, exact redirects, favicon and protected customer journey')
