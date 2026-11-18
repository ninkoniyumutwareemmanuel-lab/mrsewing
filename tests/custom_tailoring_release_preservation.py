#!/usr/bin/env python3
"""R49 release boundaries: protect approved SEO, images and unrelated journeys.

This compares immutable Git source with the candidate build. It is not evidence
of a rendered staging/production response, provider inbox receipt or indexing.
"""
from pathlib import Path
from html.parser import HTMLParser
from html import escape
import argparse
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
BASE = '663c8f5d5f4fde2afa693201e11ab108ff95adff'
OUT = Path('/workspace/review/custom-tailoring-release-2026-11-13')
# Only these routes receive new form/policy presentation, as expressly approved.
AFFECTED_HTML = {
    'request/index.html', 'request.html',
    'services/custom-tailoring/special-order/index.html',
    'services/custom-tailoring/index.html', 'service-standard.html',
    'services/mobile-fitting/index.html', 'service-housecall.html', 'service-workplace.html',
    'terms-and-conditions.html', 'terms-and-conditions/index.html',
    'privacy-policy.html', 'privacy-policy/index.html',
    'faq.html', 'faq/index.html', 'faq/search/index.html',
    'customer-information/index.html', 'delivery-and-collection/index.html',
    'customer-support/index.html', 'contact.html', 'contact/index.html',
}
SPECIAL = 'services/custom-tailoring/special-order/index.html'
TECHNICAL = {'sitemap.xml', 'robots.txt', '_headers', '_redirects', 'CNAME',
             '404.html', '_templates/not-found.html', 'favicon.ico',
             'assets/images/favicon-192.png', 'assets/images/logo-icon.png',
             '_data/favicon-assets.json'}
ALLOWED_SOURCE = {
    '_templates/selected-suit-quote.js', '_templates/selected-suit-quote.css',
    '_templates/customer-site.js', '_templates/customer-site.css',
    '_templates/request-draft.js', '_templates/design-selections.js',
    '_templates/selection-session.js', '_templates/shared-fabric.js',
    '_templates/fabric-journey.js', '_templates/fabric-journey.css',
    'assets/selected-suit-quote.js', 'assets/selected-suit-quote.css',
    'assets/customer-site.js', 'assets/customer-site.css',
    'assets/request-draft.js', 'assets/design-selections.js', 'assets/design-selections.css',
    '_data/customer-policy-facts.json', '_data/customer-faqs.json',
    '_data/customer-release.json', '_data/customer-information.json', '_data/policy-pages.json',
    '_data/fabric-colours.json',
    'functions/_lib/selected-design-handler.js', 'functions/_lib/fabric-preferences.js',
    '_templates/terms-and-conditions.html', '_templates/privacy-policy.html',
}
# These facts may legitimately repeat on older source pages. Their exact changed
# strings are normalized; this does not authorize arbitrary unrelated body edits.
SECTION_EQUIVALENTS = []
FACT_KEYS = {
    'policyMobileMeasurement', 'policyMobileConsultation', 'policyTransport',
    'policyTailoringTime', 'policyProductionStart', 'policyDeadlineAssessment',
    'policyQuotationResponse', 'policyMeasurementAppointments', 'policyCustomDelivery',
    'policyCustomerDelay', 'policyCustomerDelays', 'policyLocations', 'policyMeasurementLocations', 'policyOnlineMeasurements',
    'policySubmissionAcknowledgement',
}
# The old Special controller must defer to R49's shared form and tolerate its
# removed legacy container. Preserve every other byte of this shared script.
LEGACY_GARMENT_HANDLER = "function garmentChange(){if(!other)return;const yes=garment.value==='other';$('otherGarmentField').hidden=!yes;other.disabled=!yes;other.required=yes;}"
R49_GARMENT_HANDLER = "function garmentChange(){if(!other||window.MrCustomQuotation?.active?.())return;const yes=garment.value==='other',container=$('otherGarmentField');if(container)container.hidden=!yes;other.disabled=!yes;other.required=yes;}"


def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)


def original(path):
    return git('show', BASE + ':' + path)


def sha(value):
    return hashlib.sha256(value).hexdigest()


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.tags, self.schemas, self.headings = [], [], []
        self.current, self.buffer = None, ''
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if tag in {'title', 'h1'} or (tag == 'script' and attrs.get('type') == 'application/ld+json'):
            self.current, self.buffer = tag, ''

    def handle_data(self, value):
        if self.current:
            self.buffer += value

    def handle_endtag(self, tag):
        if tag == self.current:
            if tag == 'script':
                self.schemas.append(json.loads(self.buffer))
            else:
                self.headings.append((tag, self.buffer.strip()))
            self.current = None

    def attrs(self, tag):
        return [attrs for name, attrs in self.tags if name == tag]


def schemas_without_faq(schemas):
    result = []
    for value in schemas:
        if isinstance(value, dict) and value.get('@type') == 'FAQPage':
            continue
        if isinstance(value, dict) and '@graph' in value:
            value = {**value, '@graph': [n for n in value['@graph'] if n.get('@type') != 'FAQPage']}
        result.append(value)
    return result


def special_schema(value):
    if isinstance(value, list):
        return [special_schema(row) for row in value]
    if not isinstance(value, dict):
        return value
    value = {key: special_schema(item) for key, item in value.items()}
    if value.get('@type') in {'WebPage', 'BreadcrumbList'}:
        if value.get('@type') == 'WebPage':
            if 'name' in value:
                value['name'] = '__APPROVED_SPECIAL_TITLE__'
            if 'description' in value:
                value['description'] = '__APPROVED_SPECIAL_DESCRIPTION__'
        else:
            value['itemListElement'] = '__APPROVED_SPECIAL_BREADCRUMB_PATH__'
    return value


def seo(source, path):
    d = Document(source)
    result = {
        'metadata': d.attrs('meta'),
        'canonical': [a for a in d.attrs('link') if a.get('rel') == 'canonical'],
        'headings': d.headings,
        'schema': schemas_without_faq(d.schemas) if path.startswith('faq') else d.schemas,
        'images': [{k: a.get(k) for k in ['src', 'srcset', 'alt', 'width', 'height']} for a in d.attrs('img')],
        'stagingGuard': re.findall(r'<script data-staging-indexing>.*?</script>', source, re.S),
    }
    # New Special purpose/breadcrumb is explicit; URL/indexing/image identity is
    # still protected and the exact visible heading is checked independently.
    if path == SPECIAL:
        result.pop('headings')
        result['schema'] = special_schema(d.schemas)
        # Do not infer a new indexable purpose from the user-facing title.
        result['metadata'] = [{**a, 'content': '__APPROVED_SPECIAL_TITLE_DESCRIPTION__'} if a.get('property') in {'og:title', 'og:description'} or a.get('name') in {'description', 'twitter:title', 'twitter:description'} else a for a in result['metadata']]
    return result


def selection_data(source):
    m = re.search(r'<script id="designSelectionData"[^>]*>(.*?)</script>', source, re.S)
    return json.loads(m[1]) if m else None


def normalize(source, replacements=()):
    source = re.sub(r'(/assets/[^\s"\'<>]+\.(?:js|css))\?v=[^\s"\'<>]+', r'\1', source)
    source = re.sub(r'<script id="designSelectionData"[^>]*>.*?</script>', '__SELECTION_DATA__', source, flags=re.S)
    for value, token in SECTION_EQUIVALENTS:
        source = source.replace(value, token)
    for value, token in replacements:
        source = source.replace(value, token)
    return source


def protected(path):
    return path in TECHNICAL or path.startswith(('_data/', '_templates/', 'assets/', 'functions/')) or Path(path).suffix.lower() in {'.png', '.jpg', '.jpeg', '.webp', '.avif', '.gif', '.svg', '.mp4'}


p = argparse.ArgumentParser()
p.add_argument('--capture-baseline', action='store_true')
args = p.parse_args()
paths = git('ls-tree', '-r', '--name-only', BASE).decode().splitlines()
html = [name for name in paths if name.endswith('.html') and not name.startswith('_templates/')]
replacements = []
if not args.capture_baseline:
    oldfacts = json.loads(original('_data/customer-policy-facts.json'))['texts']
    newfacts = json.loads((ROOT/'_data/customer-policy-facts.json').read_text())['texts']
    for key in FACT_KEYS:
        if key in oldfacts and key in newfacts and oldfacts[key] != newfacts[key]:
            for value in {oldfacts[key], newfacts[key], escape(oldfacts[key]), escape(newfacts[key])}:
                replacements.append((value, '__APPROVED_R49_' + key + '__'))
    replacements.sort(key=lambda row: len(row[0]), reverse=True)
    # Existing process/Express pages reuse the approved information source.
    # Normalize only exact old/new paragraph groups, not whole page bodies.
    oldrelease = json.loads(original('_data/customer-release.json'))
    sequence = oldrelease['pages']['/customer-information/']['sections'][1]['paragraphs'][0]
    for text in [sequence, sequence + ' ' + newfacts['policyProductionStart']]:
        SECTION_EQUIVALENTS.append(('<p>' + escape(text) + '</p>', '__APPROVED_R49_PRODUCTION_SEQUENCE__'))
    for title in ['Express and after-hours arrangements', 'Standard and Express Priority']:
        section_prefix = '<section class="release-section"><h2>' + title + '</h2>'
        for texts in [[oldfacts['policyCharges'], oldfacts['policyChargeExample']],
                      [newfacts['policyDeadlineAssessment'], newfacts['policyCustomerDelays'], newfacts['policyCharges']]]:
            SECTION_EQUIVALENTS.append((section_prefix + ''.join('<p>' + escape(text) + '</p>' for text in texts) + '</section>', '__APPROVED_R49_EXPRESS_EXPLANATION__'))
    communications = oldrelease['pages']['/customer-information/']['sections'][5]['paragraphs']
    for texts in [communications, [newfacts['policyQuotationTargets'], *communications]]:
        section = '<section class="release-section"><h2>Your communications and updates</h2>' + ''.join('<p>' + escape(text) + '</p>' for text in texts) + '</section>'
        SECTION_EQUIVALENTS.append((section, '__APPROVED_R49_QUOTATION_TARGETS__'))
report = {'baseline': BASE, 'existingHTML': len(html), 'pages': {}, 'protectedFiles': {},
          'technicalSEOUnchanged': True, 'errors': [], 'liveVerification': False,
          'allowedPresentationRoutes': sorted(AFFECTED_HTML)}
for path in html:
    before = original(path).decode()
    report['pages'][path] = {'beforeSEO': seo(before, path), 'beforeSha256': sha(before.encode())}
    if args.capture_baseline:
        continue
    target = ROOT / path
    if not target.is_file():
        report['errors'].append(path + ': existing page removed')
        continue
    after = target.read_text()
    if seo(before, path) != seo(after, path):
        report['errors'].append(path + ': metadata/H1/canonical/schema/image/staging guard changed')
    if path not in AFFECTED_HTML and not path.startswith('faq/') and normalize(before, replacements) != normalize(after, replacements):
        report['errors'].append(path + ': unrelated HTML changed beyond approved fact strings/cache versions/selection data')
    old, new = selection_data(before), selection_data(after)
    if bool(old) != bool(new):
        report['errors'].append(path + ': selection context inclusion changed')
    if old and new:
        if old.get('designs') != new.get('designs') or old.get('projects') != new.get('projects'):
            report['errors'].append(path + ': design/project identities or original photograph references changed')
        oldf, newf = old.get('fabrics', {}), new.get('fabrics', {})
        if oldf != newf:
            report['errors'].append(path + ': approved fabric records changed')
for path in paths:
    if not protected(path) or path in ALLOWED_SOURCE:
        continue
    before = original(path)
    report['protectedFiles'][path] = sha(before)
    if args.capture_baseline:
        continue
    target = ROOT / path
    if not target.is_file():
        report['errors'].append(path + ': protected file removed')
        continue
    after = target.read_bytes()
    if path == 'functions/_lib/shop-preview-pages.js':
        equal = normalize(before.decode(), replacements) == normalize(after.decode(), replacements)
    elif path in {'_templates/customer-refinements.js', 'assets/customer-refinements.js'}:
        equal = before == after or before.decode().replace(LEGACY_GARMENT_HANDLER, R49_GARMENT_HANDLER) == after.decode()
    else:
        equal = before == after
    if not equal:
        report['errors'].append(path + ': protected content/asset/technical configuration changed')
    if path in TECHNICAL and before != after:
        report['technicalSEOUnchanged'] = False
if not args.capture_baseline:
    palette = json.loads((ROOT/'_data/fabric-colours.json').read_text())
    colours = palette['colours']
    if len(colours) != 50:
        report['errors'].append('Owner-approved expanded palette must contain 50 preferences including Other')
    required = ['Black', 'White', 'Ivory', 'Cream', 'Grey', 'Charcoal', 'Silver', 'Beige',
                'Navy', 'Blue', 'Royal Blue', 'Cobalt', 'Sky Blue', 'Ocean Blue', 'Powder Blue',
                'Turquoise', 'Teal', 'Red', 'Wine Red', 'Burgundy', 'Maroon', 'Pink', 'Blush Pink',
                'Purple', 'Lavender', 'Lilac', 'Brown', 'Chocolate Brown', 'Tan', 'Camel', 'Khaki',
                'Copper', 'Rust', 'Champagne', 'Gold', 'Golden Yellow', 'Yellow', 'Mustard', 'Orange',
                'Peach', 'Coral', 'Olive', 'Army Green', 'Dark Green', 'Forest Green', 'Emerald', 'Mint', 'Sage']
    names = [c['name'] for c in colours]
    for name in required:
        if not any(name == actual or actual.startswith(name + ' /') or name in {'Navy','Cobalt','Emerald','Olive'} and actual.startswith(name) for actual in names):
            report['errors'].append('Missing owner-approved colour preference: ' + name)
    if len({c['id'] for c in colours}) != len(colours):
        report['errors'].append('Duplicate colour IDs')
    if not all(c['id']=='other' or re.fullmatch('#[0-9A-Fa-f]{6}', c['hex'] or '') for c in colours):
        report['errors'].append('Invalid central illustrative swatch HEX')
    oldmeasure = original('scripts/customer_guides.py').decode().split('def measurements():', 1)[1].split('def options():', 1)[0]
    newmeasure = (ROOT/'scripts/customer_guides.py').read_text().split('def measurements():', 1)[1].split('def options():', 1)[0]
    if oldmeasure != newmeasure:
        report['errors'].append('Measurements Guide renderer changed')
    facts = json.loads((ROOT / '_data/customer-policy-facts.json').read_text())
    previous = json.loads(original('_data/customer-policy-facts.json'))
    expected_mobile = {**previous['mobile'], 'consultationAndFittingRwf': 35000}
    if facts['mobile'] != expected_mobile:
        report['errors'].append('Mobile fees/scope changed beyond the approved 35000 consultation amendment')
    for key in ['charges', 'payments', 'transport', 'services']:
        if facts[key] != previous[key]:
            report['errors'].append('Unrelated approved payment/surcharge/transport/service rule changed: ' + key)
    delivery = facts.get('customTailoringDelivery', {})
    if delivery.get('outsideKigaliRwandaPerGarmentRwf') != 5000 or delivery.get('initialEligibleKigaliSuitDeliveryIncluded') is not True or delivery.get('internationalShipping') != 'individual quotation':
        report['errors'].append('Owner-approved Custom Tailoring delivery conditions missing')
    targets = facts.get('customTailoringQuotationTargets', {})
    if (targets.get('expressHours'), targets.get('standardMinimumHours'), targets.get('standardMaximumHours')) != (24, 24, 48):
        report['errors'].append('Owner-approved provisional quotation targets missing')
    screening = facts.get('ordinarySuitDeadlineScreening', {})
    if (screening.get('planningAllowanceHours'), screening.get('standardMinimumPlanningDays')) != (24, 7):
        report['errors'].append('Owner-approved ordinary-suit deadline rule missing')
    oldrelease = json.loads(original('_data/customer-release.json'))
    newrelease = json.loads((ROOT / '_data/customer-release.json').read_text())
    allowed_pages = {'/terms-and-conditions/', '/privacy-policy/', '/contact/',
                     '/customer-information/', '/delivery-and-collection/'}
    for route, page in oldrelease['pages'].items():
        if route not in allowed_pages and page != newrelease['pages'].get(route):
            report['errors'].append('Unrelated customer-information page source changed: ' + route)
    oldservices = {row['id']: row for row in oldrelease['services']}
    newservices = {row['id']: row for row in newrelease['services']}
    for ident, service in oldservices.items():
        if ident != 'custom-tailoring' and service != newservices.get(ident):
            report['errors'].append('Unrelated service source redesigned: ' + ident)
    oldinfo = json.loads(original('_data/customer-information.json'))
    newinfo = json.loads((ROOT / '_data/customer-information.json').read_text())
    for key, value in oldinfo.items():
        if key not in {'delivery', 'timing'} and value != newinfo.get(key):
            report['errors'].append('Unrelated customer information fact changed: ' + key)
    oldfaq = json.loads(original('_data/customer-faqs.json'))
    newfaq = json.loads((ROOT / '_data/customer-faqs.json').read_text())
    changed_questions = {'start-order', 'deadline-not-accepted', 'delivery-arrangements',
                         'express-request', 'international-shipping', 'locations',
                         'measure-options', 'mobile-fees', 'outside-kigali',
                         'production-start', 'workplace-measurement'}
    if not set(oldfaq['questions']).issubset(newfaq['questions']):
        report['errors'].append('Existing FAQ questions removed')
    for ident, question in oldfaq['questions'].items():
        if ident not in changed_questions and question != newfaq['questions'].get(ident):
            report['errors'].append('Unrelated FAQ answer changed: ' + ident)
    for oldtopic, newtopic in zip(oldfaq['topics'], newfaq['topics']):
        if {k: v for k, v in oldtopic.items() if k != 'questions'} != {k: v for k, v in newtopic.items() if k != 'questions'}:
            report['errors'].append('Unrelated FAQ topic purpose changed: ' + oldtopic['slug'])
    if len(oldfaq['topics']) != len(newfaq['topics']):
        report['errors'].append('FAQ topics duplicated or removed')
    special = (ROOT / SPECIAL).read_text()
    if [text for tag, text in Document(special).headings if tag == 'h1'] != ['Special Tailoring Request']:
        report['errors'].append('Special Tailoring heading not implemented')
OUT.mkdir(parents=True, exist_ok=True)
destination = OUT / ('before-preservation.json' if args.capture_baseline else 'preservation.json')
destination.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
if report['errors']:
    print('\n'.join(report['errors']))
    raise SystemExit(1)
print(('CAPTURED' if args.capture_baseline else 'PASS') +
      f' {len(html)} HTML metadata/image identities and {len(report["protectedFiles"])} protected files; approved R49 exceptions only; live verification not inferred')
