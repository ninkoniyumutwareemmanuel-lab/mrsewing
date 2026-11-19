#!/usr/bin/env python3
"""R51 quotation-first projections, original approvals and scoped rules.

Temporary fixtures exercise future schedule edits; no approved data is modified,
no real submissions occur, and this is not deployed-browser evidence.
"""
from pathlib import Path
import hashlib
import importlib
import json
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import public_content
import customer_policies
import suit_pricing
import build_operational_facts
from customer_information import expand, information
from custom_tailoring_mobile import pricing, children, payments
from faq_help import catalogue, search_data

BASE = 'b2b8946882929da4ce7e0e01de4ba1511eed818a'
APPROVED = ['customer-policy-facts.json', 'suit-package-prices.json', 'tuxedo-package-prices.json']
for name in APPROVED:
    original = subprocess.check_output(['git', 'show', BASE + ':_data/' + name], cwd=ROOT)
    assert (ROOT / '_data' / name).read_bytes() == original, 'Internal approval changed: ' + name
source = json.loads((ROOT / '_data/customer-policy-facts.json').read_text())
prices = suit_pricing.catalogue()['prices']
assert prices['men-tier-3']['twoPieceRwf'] == 300000
assert prices['men-tier-3']['threePieceRwf'] == 400000
assert prices['men-tier-3']['sourceDecisionDate'] == '2026-11-12'
assert not public_content.service_prices_visible()
assert not public_content.surcharge_rates_visible()
assert public_content.policy()['shopProductPricesVisible']

public = customer_policies.facts()
internal = customer_policies.internal_facts()
assert any('300,000 RWF' in line and '400,000 RWF' in line for line in internal['priceLines'])
assert public['payments'] == source['payments']
assert '70%' in public['texts']['policyDomesticPayment']
assert '30%' in public['texts']['policyDomesticPayment']
assert '100%' in public['texts']['policyInternationalPayment']
assert '50%' in public['texts']['policyParentChild']
assert '3%' in public['texts']['policyBulk']
assert '70%' not in public['texts']['policyTransport'], 'Suit advance must not become an alteration/care rule'
assert 'alterations' in public['texts']['policyTransport'] and 'garment-care' in public['texts']['policyTransport']
assert 'Kigali' in public['texts']['policyMobileMeasurement']
assert 'after' in public['texts']['policyMobileMeasurement'] and 'quotation' in public['texts']['policyMobileMeasurement']
assert 'without a confirmed garment order' in public['texts']['policyMobileConsultation']
assert 'not charged' in public['texts']['policyCustomDelivery']

money = re.compile(r'\b[\d,]+\s*RWF\b')
cost_rates = re.compile(r'\b(?:35|25|60)%')
for key, text in public['texts'].items():
    assert not money.search(text), (key, text)
    assert not cost_rates.search(text), (key, text)
for text in [pricing(), children(), payments(), expand('{{suitPayment}} {{delivery}} {{cotton_table}}')]:
    assert not money.search(text), text
    assert not cost_rates.search(text), text
assert pricing().count('ordinary-benefit-table') == 2
assert 'Tier / Quality' in pricing() and 'Included Benefits' in pricing()
assert 'Tier 4 / Quality 4' in pricing()
assert '70%' in payments() and '30%' in payments()
assert '50%' in children()
assert '3 cleanings' in pricing() and 'Initial cleaning' in pricing()

faq, topics, questions, owners = catalogue()
assert 'quotation-request' in owners and 'workplace-visits' in owners
for key, row in questions.items():
    text = row['question'] + ' ' + expand(row['answer'])
    assert not money.search(text), (key, text)
    assert not cost_rates.search(text), (key, text)
for row in search_data()['entries']:
    if 'Referrer commission' in row['question']:
        assert '6,000 RWF' in row['answer'], 'A customer commission is not a service tariff'
        continue
    assert not money.search(row['question'] + row['answer']), row
    assert not cost_rates.search(row['question'] + row['answer']), row
    if row['id'].startswith('terms-and-conditions-'):
        assert row['answer'].startswith('Read the current Terms and Conditions'), row
for path, _ in public_content.RULE_LINKS.values():
    topic, answer = path.split('#')
    assert '/faq/' + owners[answer] + '/' == topic, path
assert '{{' not in expand('{{officialWhatsApp}} {{officialTelephone}} {{officialEmail}}')

# Future approved schedule edits do not accidentally re-publish a tariff.
modules = [public_content, customer_policies, suit_pricing, build_operational_facts]
roots = {module: module.ROOT for module in modules}
with tempfile.TemporaryDirectory(prefix='r51-price-fixture-') as tmp:
    fixture = Path(tmp)
    (fixture / '_data').mkdir()
    for name in APPROVED + ['public-content-policy.json']:
        (fixture / '_data' / name).write_bytes((ROOT / '_data' / name).read_bytes())
    value = json.loads((fixture / '_data/suit-package-prices.json').read_text())
    value['prices']['men-tier-3']['twoPieceRwf'] = 333333
    (fixture / '_data/suit-package-prices.json').write_text(json.dumps(value))
    value = json.loads((fixture / '_data/customer-policy-facts.json').read_text())
    value['mobile']['consultationAndFittingRwf'] = 48000
    (fixture / '_data/customer-policy-facts.json').write_text(json.dumps(value))
    try:
        for module in modules:
            module.ROOT = fixture
        assert '333,333 RWF' in ' '.join(customer_policies.internal_facts()['priceLines'])
        assert '333,333' not in pricing()
        assert '333333' not in json.dumps(customer_policies.facts()['priceLines'])
        generated = next(iter(build_operational_facts.outputs().values()))
        assert '48000' in generated and '35000' not in generated
    finally:
        for module, original in roots.items():
            module.ROOT = original

# Shop commercial sources and renderers remain under their own exact gates.
for filename in ['_data/shop-products.json', '_data/shop-public-enquiries.json', 'scripts/shop_catalog.py', 'scripts/build_commerce.py']:
    assert (ROOT / filename).read_bytes() == subprocess.check_output(['git', 'show', BASE + ':' + filename], cwd=ROOT), filename
from build_commerce import card
product = json.loads((ROOT / '_data/shop-products.json').read_text())
product = product[0] if isinstance(product, list) else product['products'][0]
fixture = dict(product, priceRwf=123456, availability='Available in Stock')
assert 'RWF 123,456' in card(fixture), 'Verified Shop price presentation must remain supported'
for path, text in build_operational_facts.outputs().items():
    assert path.read_text() == text

for template in ['_templates/customer-site.js', '_templates/quotation-arrangements.js']:
    text = (ROOT / template).read_text()
    assert not money.search(text), template
    assert not cost_rates.search(text), template
print('PASS R51 public service tariffs/rates absent; approved schedules unchanged; payment/benefit/Shop exceptions preserved; shared FAQ scopes and document references; future-source fixtures; no real submissions')
