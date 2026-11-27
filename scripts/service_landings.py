"""Compact service information, using existing approved facts and request routes.

This is a presentation layer, not a new price, policy, form or contact database.
"""
import json
from html import escape
from pathlib import Path
from urllib.parse import urlencode

ROOT = Path(__file__).resolve().parents[1]


def contact_actions():
    result = json.loads((ROOT / '_data/service-contact-actions.json').read_text())
    result['label'] = __import__('customer_interface').action('whatsapp')
    return result


def whatsapp_url(service):
    phone = json.loads((ROOT / '_data/business.json').read_text())['telephone']
    digits = ''.join(character for character in phone if character.isdigit())
    assert digits and len(digits) <= 15
    return 'https://wa.me/' + digits + '?' + urlencode({'text': contact_actions()['messages'][service]})


def contact_link(service, css='home-button home-button-gold'):
    return '<a class="' + escape(css, quote=True) + '" href="' + escape(whatsapp_url(service), quote=True) + '">' + escape(contact_actions()['label']) + '</a>'


def combined_card():
    return '''<aside class="service-combined" aria-labelledby="combined-service-title">
      <h3 id="combined-service-title">Need Both Repairs and Cleaning?</h3>
      <p>Arrange clothing alterations or repairs and professional garment cleaning through one coordinated enquiry.</p>
      <p class="service-small">Each service is assessed and priced individually. There is no automatic combined-service discount. Additional paid work needs your approval, and the same applicable transport service is not charged twice.</p>
      ''' + contact_link('combined') + '</aside>'


def _section(title, content, ident=None, css=''):
    return '<section class="service-section ' + css + '"' + (' id="' + escape(ident, quote=True) + '"' if ident else '') + '><h2>' + escape(title) + '</h2>' + content + '</section>'


def _paragraph(text):
    return '<p>' + escape(text) + '</p>'


def _list(items):
    return '<ul class="service-scope">' + ''.join('<li>' + escape(item) + '</li>' for item in items) + '</ul>'


def content(service, hero, link):
    """Render four independent service pages; all original forms stay in place."""
    from customer_policies import facts, sections
    from public_content import public_texts

    ident = service['id']
    assert ident in {'alterations', 'garment-care', 'mobile-fitting', 'vip'}
    policy = facts()
    texts = public_texts(policy['texts'])
    body = '<div class="service-overview">' + hero(ident)
    if ident == 'alterations':
        body += _section('Fit Adjustments & Garment Repairs',
            _paragraph('Discuss changes to an existing garment. We inspect its fit, condition and construction before confirming what can be done.') +
            _list(['Shirts and trousers', 'Jackets and suits', 'Dresses and other garments requiring assessment']) +
            _paragraph('Tell us what feels wrong, what you would like changed and any previous repairs. Measurements or a fitting may be needed. Not every garment can be altered or repaired.'))
    elif ident == 'garment-care':
        body += _section('Care That Starts with Your Garment',
            _paragraph('Ask about cleaning and garment care for shirts, trousers, jackets, dresses and suits. The suitable method is confirmed after assessment.') +
            _list(['Share the care label and any known material information', 'Explain stains, damage and previous treatment', 'Agree suitable care, limitations and handover arrangements']) +
            _paragraph('Complimentary suit-package cleaning and separately requested cleaning are different services. An included initial standard cleaning is not charged twice.'))
    elif ident == 'mobile-fitting':
        options = [
            ('Order Measurement Visit', texts['policyMobileMeasurement']),
            ('Consultation & Fitting', texts['policyMobileConsultation']),
            ('Independent Tailoring Assistance', texts['policyMobileAssistance']),
        ]
        body += _section('Choose the Assistance You Need',
            '<div class="service-comparison">' + ''.join('<article><h3>' + escape(title) + '</h3>' + _paragraph(text) + '</article>' for title, text in options) + '</div>' +
            _paragraph('Professional measurement, consultation and styling visits are separate from garment collection and delivery. Tell us your city, country, location, preferred time and the number of people involved.'), 'service-info-mobile')
    else:
        body += _section('Personalised Assistance for Your Occasion',
            _paragraph('Discuss the service, setting and level of assistance you need. We assess the scope, feasibility and availability before offering an individual quotation.') +
            _list(['Wedding and event styling', 'Personalised tailoring and complex alterations', 'Individually assessed garment care', 'Group coordination and assistance at customer locations']))

    # Customer policy facts remain the authoritative source. Preserve existing
    # anchors used by FAQs rather than discarding useful shared links.
    rows = sections(ident)
    if ident == 'mobile-fitting':
        rows = [row for row in rows if row[0] != 'mobile']
    body += '<div class="service-facts">'
    for anchor, title, text in rows:
        if anchor == 'payment' and ident in {'alterations', 'garment-care'}:
            text = __import__('customer_information').information()['standalonePayment'] + ' ' + text
        body += _section(title, _paragraph(text), 'service-info-' + anchor)
    body += '</div>'

    body += _section('How to Arrange Your Service',
        '<ol class="service-steps"><li><strong>Tell us what you need</strong><span>Contact us with the garment or assistance required and your preferred timing.</span></li>'
        '<li><strong>Review the quotation</strong><span>We assess the request and confirm the scope, price, applicable payment and proposed arrangements.</span></li>'
        '<li><strong>Confirm before relying on a date</strong><span>An enquiry or preferred appointment does not confirm an accepted order, visit or completion date.</span></li></ol>' +
        '<p class="service-small">Service prices are individually quoted. Read the <a href="/customer-information/">order and payment guidance</a> and <a href="/terms-and-conditions/current/">currently effective Terms &amp; Conditions</a> before accepting an arrangement.</p>')

    if ident in {'alterations', 'garment-care'}:
        body += combined_card()

    body += _section('Discuss Your Request',
        _paragraph('Share your requirements with our team, or use the existing website request form.') +
        '<div class="service-contact-actions">' + contact_link(ident) + link('/request/' + ident + '/', __import__('customer_interface').action('requestQuote'), 'home-button') + '</div>' +
        '<p class="service-small">You review and send the message in WhatsApp. Opening the conversation does not submit a request or confirm an order.</p>' +
        '<p class="service-policy-links"><a href="/faq/">FAQs</a><a href="/refund-policy/">Refund &amp; Cancellation Policy</a><a href="/privacy-policy/">Privacy Policy</a></p>')
    return body + '</div>'
