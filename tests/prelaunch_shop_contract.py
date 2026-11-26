#!/usr/bin/env python3
"""Current Shop gates plus the existing complete backend contract, synthetic only."""
from pathlib import Path
import copy
import json
import os
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from shop_catalog import load
from build_commerce import outputs

fixture = {'id': 'QA_0', 'slug': 'qa-only-product', 'name': 'Synthetic QA only',
    'category': "Men's Suits", 'description': 'Synthetic test fixture, never published.',
    'publicationStatus': 'published', 'approval': {'publicDisplay': True, 'source': 'Synthetic fixture only', 'date': '2026-11-26'},
    'images': [{'src': '/hero-custom-tailoring.webp', 'alt': 'Synthetic fixture image', 'width': 1024, 'height': 1024,
                'rightsApproved': True, 'approvalSource': 'Fixture only'}],
    'availability': 'Available in Stock', 'priceRwf': 12345, 'priceApproved': True, 'stockQuantity': 3,
    'variations': [{'id': 'qa-a', 'size': 'QA M', 'colour': 'QA blue', 'stockQuantity': 2},
                   {'id': 'qa-b', 'size': 'QA L', 'colour': 'QA blue', 'stockQuantity': 1}],
    'specifications': {}, 'careInstructions': 'Fixture only', 'orderingNotes': 'Not merchandise',
    'seoTitle': 'Synthetic QA', 'seoDescription': 'Not published', 'socialImage': '/hero-custom-tailoring.webp'}
assert load() == [], 'No approved sale stock may be fabricated'
products = []
for number, status in enumerate(['Available in Stock', 'Available on Backorder', 'Out of Stock']):
    product = copy.deepcopy(fixture)
    product.update(id='QA_' + str(number), slug='qa-only-' + str(number), availability=status)
    if number:
        product.update(priceRwf=None, stockQuantity=0)
        for variation in product['variations']:
            variation['stockQuantity'] = 0
    products.append(product)
source = {'schemaVersion': 1, 'products': products}
assert load(source) == products
for change in [{'availability': 'Available on Orders'}, {'priceApproved': False}, {'stockQuantity': 9},
               {'approval': {}}, {'images': []}]:
    invalid = copy.deepcopy(fixture)
    invalid.update(change)
    try:
        load({'schemaVersion': 1, 'products': [invalid]})
    except AssertionError:
        pass
    else:
        raise AssertionError('Invalid catalogue fixture accepted')
draft = copy.deepcopy(fixture)
draft['publicationStatus'] = 'draft'
assert load({'schemaVersion': 1, 'products': [draft]}) == []
generated = outputs(products)
assert '12345' in generated[ROOT / 'shop/qa-only-0/index.html']
assert 'Available on Backorder' in generated[ROOT / 'shop/qa-only-1/index.html']
assert '"availability": "https://schema.org/InStock"' in generated[ROOT / 'shop/qa-only-0/index.html']
assert not (ROOT / 'shop/qa-only-0').exists(), 'Fixtures must never reach the website'
with tempfile.TemporaryDirectory(prefix='mrsewing-shop-fixture-') as folder:
    target = Path(folder) / 'fixtures.json'
    target.write_text(json.dumps(products))
    subprocess.run(['node', 'tests/commerce-server.mjs'], cwd=ROOT,
                   env={**os.environ, 'SHOP_FIXTURE_PATH': str(target)}, check=True)
print('PASS current Shop publication/price/stock gates and existing backend suite; fixture HTML remained in memory, no real submissions')
