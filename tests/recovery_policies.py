"""25Nov recovery: approved policies remain scoped and public tariffs stay internal.

No customer submissions, legal-review assertion or official activation.
"""
import copy
import json
import re
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from customer_policies import facts, sections
from customer_information import expand
from public_content import policy, public_texts
from faq_help import catalogue, search_data

f = facts()
before = copy.deepcopy(f['texts'])
projected = public_texts(f['texts'])
assert f['texts'] == before, 'Public presentation mutated approved internal facts'
assert f['payments']['domesticCustomAdvancePercent'] == 70
assert f['payments']['domesticCustomBalancePercent'] == 30
assert f['payments']['internationalCustomAdvancePercent'] == 100
assert f['charges']['expressPercent'] == 35
assert f['charges']['afterHoursPercent'] == 25
assert f['charges']['combinedPercent'] == 60
assert f['latestPolicyApproval']['date'] == '2026-11-25'
assert 'three calendar days' in f['texts']['policyFlexibleAdvance']
assert 'entire outstanding balance' in f['texts']['policyFlexibleAdvance']
assert 'not available for Express' in f['texts']['policyFlexibleAdvance']
assert 'does not automatically apply to international' in f['texts']['policyFlexibleAdvance']
assert 'production is suspended' in f['texts']['policyOverdueAdvance']
assert 'does not itself mean cancellation or forfeiture' in f['texts']['policyOverdueCancellation']
assert 'permitted by applicable law' in f['texts']['policyRefundBeforeProduction']
assert 'not the official production-start notice' in f['texts']['policyPaymentVerification']
for key in ['policyDomesticPayment', 'policyInternationalPayment', 'policyFlexibleAdvance',
            'policyExpressAdvance', 'policyOverdueAdvance', 'policyOverdueCancellation',
            'policyRefundBeforeProduction', 'policyRefundAfterProduction', 'policyRefundAssessment',
            'policyPaymentVerification', 'policyParentChild', 'policyBulk', 'policyCharges']:
    assert projected[key] == before[key], ('Approved obligation/benefit/surcharge changed', key)
for key in ['policyMobileMeasurement', 'policyMobileConsultation', 'policyMobileAssistance',
            'policyTransport', 'policyCustomDelivery', 'policyOutsideKigaliDelivery', 'policySuitPrices']:
    assert not re.search(r'\b[\d,]+\s*RWF\b', projected[key]), key
    assert 'quot' in projected[key].lower(), key
assert '35%' in projected['policyCharges'] and '25%' in projected['policyCharges'] and '60%' in projected['policyCharges']
assert '10,000 RWF' in before['policyMobileMeasurement']
assert '35,000 RWF' in before['policyMobileConsultation']
assert '5,000 RWF per garment' in before['policyCustomDelivery']
with patch('public_content.policy', return_value={**policy(), 'servicePricesVisible': True}):
    assert public_texts(before) == before, 'Projection cannot recover original approved text'

# Internal selling records, sale inventory and provider fee inputs are unchanged.
for filename in ['_data/suit-package-prices.json', '_data/tuxedo-package-prices.json',
                 '_data/shop-products.json', '_data/custom-tailoring-fees.json']:
    path = ROOT / filename
    if path.is_file():
        assert path.read_bytes() == subprocess.check_output(['git', 'show', '0acf34dc:' + filename], cwd=ROOT), filename

qs = catalogue()[2]
mapping = {'flexible-advance': 'policyFlexibleAdvance', 'express-advance': 'policyExpressAdvance',
           'overdue-advance': 'policyOverdueAdvance', 'overdue-cancellation': 'policyOverdueCancellation'}
for ident, key in mapping.items():
    assert qs[ident]['answer'] == '{{' + key + '}}'
    assert expand(qs[ident]['answer']) == before[key]
for ident in ['suit-starting-cost', 'mens-suit-cost', 'womens-suit-cost', 'tuxedo-cost',
              'workplace-measurement', 'alterations-cost', 'washing-suit-cost']:
    assert not re.search(r'\b[\d,]+\s*RWF\b', expand(qs[ident]['answer'])), ident
for row in search_data()['entries']:
    assert '{{' not in row['answer'], row['id']
    assert not re.search(r'(?:after|within) (?:ten|10) calendar days.*(?:cancel|forfeit)', row['answer'], re.I), row['id']
assert not any('600,000 RWF' in answer or '250,000 RWF' in answer
               for _, _, answer in sections('custom-tailoring'))
print('PASS recovery policies: exact scoped70/30/100/35+25/three-day/no-forfeiture; shared FAQ/search; quotation-first public tariffs; internal schedules/Shop/fee inputs preserved')
