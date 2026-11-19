"""R51 public presentation policy, separate from approved internal business facts.

This adapter hides published service tariffs, never changes an existing quotation,
Shop price, payment obligation or eligibility rule. Public operational wording is
projected from the current authoritative texts rather than a second policy copy.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def policy():
    value = json.loads((ROOT / '_data/public-content-policy.json').read_text())
    assert value['approvalStatus'] == 'APPROVED FOR STAGING ONLY'
    return value


def service_prices_visible():
    return policy()['servicePricesVisible']


def surcharge_rates_visible():
    return policy()['serviceSurchargeRatesVisible']


def _quoted_fee(text):
    """Project a named fixed-fee service while preserving its exact conditions."""
    return re.sub(r':\s*[\d,]+\s+RWF\b', ' is individually quoted', text)


def public_texts(source):
    result = dict(source)
    payment=source['policyDomesticPayment']
    standalone='Standalone '+payment.split('Standalone ',1)[1] if 'Standalone ' in payment else payment
    full_payment=re.search(r'Full payment[^.]+\.',payment)
    result['policyStandalonePayment']=standalone+(' '+full_payment[0] if full_payment else '')
    if not service_prices_visible():
        for key in ['policyMobileMeasurement', 'policyMobileConsultation', 'policyMobileAssistance']:
            result[key] = _quoted_fee(source[key])
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
    if not surcharge_rates_visible():
        text = source['policyCharges']
        text = re.sub(r'Express adds \d+% of the eligible quoted base service\.',
                      'Express service and its eligible charges are individually quoted.', text)
        text = re.sub(r'adds \d+% of the same eligible base',
                      'is separately quoted on the same eligible base', text)
        text = re.sub(r'When both apply, the additive surcharge is \d+%, not compounded\.',
                      'When both apply, charges are additive on the same eligible base, not compounded.', text)
        result['policyCharges'] = text.replace('Ordinary-service percentages', 'Ordinary-service charges')
        result['policyExpressTailoring'] = re.sub(
            r'The approved eligible Express surcharge is \d+%, separately quoted and agreed',
            'Any eligible Express charge is separately quoted and agreed', source['policyExpressTailoring'])
        assert not re.search(r'\d+%', result['policyCharges'] + result['policyExpressTailoring'])
    return result


# Stable shared explanations. Service pages link here instead of reproducing
# full universal conditions, and the FAQ retains their explicit service scopes.
RULE_LINKS = {
    'charges': ('/faq/express-tailoring/#express-charge', 'Express, after-hours and overnight conditions'),
    'payments': ('/faq/prices-packages-payments/#domestic-deposit', 'Payment and order confirmation information'),
    'transport': ('/faq/production-delivery/#delivery-arrangements', 'Collection and delivery information'),
    'visits': ('/faq/measurements-fittings/#measurement-appointments', 'Measurement and visit arrangements'),
}
