"""Approved quotation-first service presentation; internal facts stay unchanged.

Fixed service tariffs are not a second editable price source. This small adapter
projects the approved source text for public information; quotation calculators,
Shop records and agreed customer prices do not call this adapter.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def policy():
    value = json.loads((ROOT / '_data/public-content-policy.json').read_text())
    assert value['approvalStatus'] == 'APPROVED FOR STAGING ONLY'
    assert value['paymentObligationsVisible'] and value['benefitEligibilityVisible']
    assert value['shopProductPricesVisible'] and value['existingIndividualQuotationsUnaffected']
    return value


def public_texts(source):
    result = dict(source)
    if policy()['servicePricesVisible']:
        return result
    for key in ['policyMobileMeasurement', 'policyMobileConsultation', 'policyMobileAssistance']:
        result[key] = re.sub(r':\s*[\d,]+\s+RWF\b', ' is individually quoted', source[key])
    result['policyTransport'] = re.sub(
        r'have a [\d,]+\s+RWF total collection-and-return charge',
        'have a separately quoted collection-and-return charge', source['policyTransport'])
    result['policyCustomDelivery'] = re.sub(
        r'For eligible Custom Tailoring orders delivered elsewhere in Rwanda,.*?RWF\.',
        'For eligible Custom Tailoring orders delivered elsewhere in Rwanda, delivery is individually quoted.',
        source['policyCustomDelivery'])
    result['policyOutsideKigaliDelivery'] = (
        'Delivery elsewhere in Rwanda for eligible Custom Tailoring orders is individually quoted. '
        + ' '.join(sentence for sentence in re.split(r'(?<=[.!?])\s+', source['policyOutsideKigaliDelivery'])
                   if 'RWF' not in sentence))
    result['policyChargeExample'] = 'Your quotation identifies applicable charges separately for your agreement.'
    for key in ['policyMobileMeasurement', 'policyMobileConsultation', 'policyMobileAssistance',
                'policyTransport', 'policyCustomDelivery', 'policyOutsideKigaliDelivery', 'policyChargeExample']:
        assert not re.search(r'\b[\d,]+\s*RWF\b', result[key]), 'Review public price projection: ' + key
    for key, label in [('policyMensStarting', 'Men’s'), ('policyWomensStarting', 'Women’s')]:
        result[key] = label + ' ordinary suits are individually quoted after review of the fabric, design and order requirements.'
    result['policySuitPrices'] = ('Ordinary suits are quoted by the applicable Tier / Quality and confirmed garment requirements. '
        'Men’s tuxedos retain their separate package conditions and quotation. These are complete garments, not fabric-only purchases.')
    return result
