"""Service messages, policy source reuse, compatibility and unpublished offers."""
import json
import re
import sys
from html import unescape
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from customer_site import hero, service_map, service_page
from service_landings import combined_card, contact_actions, whatsapp_url
from customer_policies import sections

business = json.loads((ROOT / '_data/business.json').read_text())
phone = ''.join(c for c in business['telephone'] if c.isdigit())
actions = contact_actions()
for ident in ['alterations', 'garment-care', 'mobile-fitting', 'vip']:
    url = urlsplit(whatsapp_url(ident))
    assert url.scheme == 'https' and url.netloc == 'wa.me'
    assert url.path == '/' + phone
    assert parse_qs(url.query)['text'] == [actions['messages'][ident]]
    header = hero(ident)
    assert 'Contact Us on WhatsApp' in header
    assert unescape(whatsapp_url(ident)) in unescape(header)
    page = service_page(ident)
    assert '<h1>' + service_map()[ident]['title'].replace('&', '&amp;') + '</h1>' in page
    assert '/request/' + ident + '/' in page, 'existing service form route must remain'
    assert 'id="customerRequestForm"' not in page, 'landing must not duplicate the form'
    assert 'service-landings.css' in page
    assert 'VIP Subscription' not in page and 'being developed' not in page
    assert '/terms-and-conditions/current/' in page
    assert 'Submit Request' not in header, 'a conversation is not a submission'
    assert not re.search(r'\b[\d,]+\s+RWF\b', page), 'quotation-first public tariff rule'
    for anchor, title, text in sections(ident):
        assert 'id="service-info-' + anchor + '"' in page
    if ident in {'alterations', 'garment-care'}:
        assert '70% advance' in page and '30% before release or delivery' in page
        assert parse_qs(urlsplit(whatsapp_url('combined')).query)['text'] == [actions['messages']['combined']]
        assert 'Need Both Repairs and Cleaning?' in page

card = combined_card()
assert 'no automatic combined-service discount' in card
assert 'Additional paid work needs your approval' in card
assert 'not charged twice' in card
assert '/request/' not in card
assert parse_qs(urlsplit(whatsapp_url('combined')).query)['text'] == [
    'Hello Mr Sewing Fashion, I need both garment repairs and professional cleaning.']
facts = json.loads((ROOT / '_data/customer-policy-facts.json').read_text())
assert '35,000 RWF' in facts['texts']['policyMobileConsultation']
assert '10,000 RWF' in facts['texts']['policyMobileMeasurement']
assert '50,000 RWF' in facts['texts']['policyMobileAssistance']
assert 'five people and three hours' in service_page('mobile-fitting')
assert '25,000 RWF' not in facts['texts']['policyMobileConsultation']
print('PASS four service hero messages and official contact source, preserved forms/anchors, compact policy-backed landings, combined direct contact, no unfinished VIP offer, latest scoped internal fees and quotation-first publication')
