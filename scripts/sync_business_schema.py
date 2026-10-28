#!/usr/bin/env python3
"""Synchronize existing business JSON-LD from verified repository contact details.

No runtime fetches. Only existing business nodes, their identity references and
WebSite names are updated; product/FAQ/navigation content is preserved. Regenerate
the homepage with build_homepage.py afterward. --check never writes files.
"""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
BLOCK = re.compile(r'(<script\b[^>]*type=["\']application/ld\+json["\'][^>]*>)(.*?)(</script>)', re.S | re.I)
BUSINESS_TYPES = {'Tailor', 'ClothingStore', 'LocalBusiness'}
LEGACY_IDS = {'https://mrsewingfashion.com/#tailor', 'https://mrsewingfashion.com/#localbusiness'}


def update(node, business):
    if isinstance(node, list):
        return [update(value, business) for value in node]
    if not isinstance(node, dict):
        return node
    result = {key: update(value, business) for key, value in node.items()}
    if result.get('@id') in LEGACY_IDS:
        result['@id'] = business['@id']
    if result.get('@type') in BUSINESS_TYPES:
        # Preserve legitimate extra fields, such as the about page's description,
        # alternate names and parentOrganization. Do not retain unverified geo data.
        for key in ('geo', 'openingHours', 'specialOpeningHoursSpecification'):
            result.pop(key, None)
        result.update(deepcopy(business))
    elif result.get('@type') == 'WebSite':
        if result.get('@id') == 'https://mrsewingfashion.com/#website':
            result['name'] = business['name']
    # ProductCollection inherits Product: manufacturer is the appropriate
    # relationship to the maker, whereas provider is not in Product's domain.
    if result.get('@type') == 'ProductCollection' and isinstance(result.get('provider'), dict):
        provider = result['provider']
        if provider.get('@id') == business['@id']:
            result['manufacturer'] = result.pop('provider')
    return result


def synchronize(source, business):
    def replace(match):
        old = json.loads(match[2])
        new = update(old, business)
        if new == old:
            return match[0]
        prefix = re.match(r'\s*\n([ \t]*)\{', match[2])
        indent = prefix[1] if prefix else ''
        rendered = '\n'.join(indent + line if line else line for line in json.dumps(new, ensure_ascii=False, indent=2).splitlines())
        return match[1] + '\n' + rendered + '\n' + match[3]
    return BLOCK.sub(replace, source)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    business = json.loads((ROOT / '_data/business.json').read_text())
    files = [path for path in ROOT.glob('*.html') if path.name != 'index.html']
    files.append(ROOT / '_templates/homepage.html')
    stale = []
    for path in sorted(files):
        source = path.read_text()
        result = synchronize(source, business)
        if result != source:
            stale.append(path.relative_to(ROOT).as_posix())
            if not args.check:
                path.write_text(result)
    if args.check and stale:
        raise SystemExit('Business schema is out of date: ' + ', '.join(stale))
    print('PASS: business schema is synchronized.' if args.check else f'Updated business metadata in {len(stale)} source documents; regenerate index.html next.')


if __name__ == '__main__':
    main()
