"""H01 content projection: shared destinations, approved media and editable copy.

This module renders only the homepage. Service policies, pricing, eligibility,
designs and request state remain with their existing authorities.
"""
import json
import re
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def content():
    data = json.loads((ROOT / '_data/homepage-content.json').read_text())
    if data.get('schemaVersion') != 1:
        raise ValueError('Unsupported homepage content schema')
    return data


def text(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('Homepage copy must be non-empty text')
    return escape(value, quote=True)


def href(value):
    from urllib.parse import urlsplit
    if not isinstance(value, str) or '\\' in value or any(ord(c) < 32 for c in value):
        raise ValueError('Homepage destination must be a local route')
    if not value.startswith('/') or value.startswith('//'):
        business = json.loads((ROOT / '_data/business.json').read_text())
        number = re.sub(r'\D', '', business['telephone'])
        url = urlsplit(value)
        if url.scheme != 'https' or url.netloc != 'wa.me' or url.path != '/' + number:
            raise ValueError('External homepage actions must use the verified WhatsApp number')
    return text(value)


def heading(record, ident):
    description = '<p>' + text(record['description']) + '</p>' if record.get('description') else ''
    return '<div class="section-heading centered"><p class="home-eyebrow">' + text(record['eyebrow']) + '</p><h2 id="' + ident + '">' + text(record['title']) + '</h2>' + description + '</div>'


def section(ident, classes, record, body):
    # Preserve established homepage heading anchors through the source refactor.
    title_id = {
        'customer-information': 'tailor-essentials-title',
        'tailoring-process': 'tailor-process-title',
        'tailoring-benefits': 'tailor-benefits-title',
        'order-options': 'tailor-options-title',
        'customer-programs': 'tailor-programs-title',
        'tailoring-final': 'tailor-final-title',
    }.get(ident, ident + '-title')
    return '<section class="home-section ' + classes + '" id="' + ident + '" aria-labelledby="' + title_id + '"><div class="home-shell">' + heading(record, title_id) + body + '</div></section>'


def design_contact():
    from urllib.parse import urlencode
    return '/whatsapp/?' + urlencode({'text': content()['designMessage']})


def actions(items):
    from customer_interface import action
    result = []
    for index, item in enumerate(items):
        target = design_contact() if item.get('designContact') else item['href']
        label = item.get('label') or action(item['action'])
        attributes = ' data-whatsapp-modal' if item.get('designContact') else ''
        classes = 'home-button home-button-gold' if index == 0 else 'home-button tailoring-outline'
        result.append('<a class="' + classes + '"' + attributes + ' href="' + href(target) + '">' + text(label) + '</a>')
    return ''.join(result)


def feature(settings=None):
    """Resolve a deliberately featured photo through the effective public loader.

    The settings select an existing design/image; they never confer permission.
    A held/removed design cannot remain visible through this homepage module.
    """
    from build_collections import load, picture
    settings = settings or json.loads((ROOT / '_data/media-library-settings.json').read_text())
    selected = settings['homepage'].get('featuredDesign')
    if not selected:
        return ''
    design = next((d for d in load()[0] if d['id'] == selected['designId']), None)
    if not design:
        return ''
    image = next((i for i in design['images'] if i['src'] == selected['imageSrc']), None)
    if not image:
        return ''
    record = content()['feature']
    photo = re.sub(r'sizes="[^"]*"', 'sizes="(min-width: 761px) 600px, 100vw"', picture(image))
    return '<a class="tailoring-feature-photo" href="' + href(record['href']) + '">' + photo + '<span>' + text(record['title']) + ' <span aria-hidden="true">→</span></span></a>'


def business_display():
    business = json.loads((ROOT / '_data/business.json').read_text())
    information = json.loads((ROOT / '_data/customer-information.json').read_text())
    contact = json.loads((ROOT / '_data/contact-v2.json').read_text())
    number = re.sub(r'\D', '', business['telephone'])
    display = ('+' + number[:3] + ' ' + ' '.join(number[i:i+3] for i in range(3, len(number), 3))) if len(number) == 12 else business['telephone']
    workshop = contact['mainWorkshop']
    return {
        'support_phone': business['telephone'], 'support_phone_display': display,
        'support_whatsapp_number': number, 'support_email': business['email'],
        'support_workshop_address': workshop['streetAddress'] + ', ' + workshop['addressLocality'],
        'brand_intro': business['name'].upper() + ' · ' + information['location'].upper(),
    }


def support(markup):
    """Replace display/link facts only; never rebuild the protected support form."""
    for key, value in business_display().items():
        markup = markup.replace('{{' + key + '}}', text(value))
    return markup


def render_sections():
    from site_shell import destination
    from homepage_video_cards import render as videos
    data = content()
    result = {}
    hero = data['hero']
    # Preserve the approved hero markup and responsive asset authority.
    source = (ROOT / '_templates/homepage-tailoring.html').read_text()
    backdrop = re.search(r'<div class="hero-backdrop">.*?</div>', source, re.S).group()
    result['hero'] = '<section class="hero-section tailoring-first-hero" aria-labelledby="hero-title">' + backdrop + '<div class="home-shell hero-grid"><div class="hero-content"><p class="home-eyebrow">' + text(business_display()['brand_intro']) + '</p><h1 id="hero-title">' + text(hero['title']) + ' <em>' + text(hero['emphasis']) + '</em></h1><p class="hero-description">' + text(hero['description']) + '</p><div class="hero-actions tailoring-hero-actions">' + actions(hero['actions']) + '</div></div></div></section>'
    cards = []
    for card in data['services']['cards']:
        target = destination(card['destinationId'])
        attributes = ' data-whatsapp-modal' if card['destinationId'] == 'combined' else ''
        cards.append('<a class="tailoring-primary-card" href="' + href(target['href']) + '"' + attributes + '><span class="tailoring-card-kicker">' + text(card['kicker']) + '</span><h3>' + text(target['label']) + '</h3><p>' + text(card['description']) + '</p><span class="tailoring-card-link">' + text(card['action']) + ' <span aria-hidden="true">→</span></span></a>')
    suits = destination('suits')
    entry = '<a class="home-suits-entry" href="' + href(suits['href']) + '"><span><strong>' + text(data['suits']['title']) + '</strong><span>' + text(data['suits']['description']) + '</span></span><span class="tailoring-card-link">' + text(data['suits']['action']) + ' <span aria-hidden="true">→</span></span></a>'
    result['services'] = '<section class="home-services home-section tailoring-first-showcase" id="services" aria-labelledby="services-title"><div class="home-shell"><div class="tailoring-photo-duo" role="group" aria-label="Suit design reference videos">' + videos() + '</div>' + heading(data['services'], 'services-title') + '<div class="tailoring-primary-grid">' + ''.join(cards) + '</div>' + entry + feature() + '</div></section>'
    information = ''.join('<a href="' + href(c['href']) + '"><strong>' + text(c['title']) + '</strong><span>' + text(c['description']) + '</span><small>' + text(c['action']) + ' →</small></a>' for c in data['information']['cards'])
    result['information'] = section('customer-information', 'tailor-essentials', data['information'], '<div class="tailor-info-grid">' + information + '</div>')
    steps = ''.join('<li><span>' + f'{i:02}' + '</span><strong>' + text(c['title']) + '</strong><p>' + text(c['description']) + '</p></li>' for i, c in enumerate(data['process']['steps'], 1))
    result['process'] = section('tailoring-process', 'tailor-process', data['process'], '<ol class="tailor-process-grid">' + steps + '</ol><div class="section-action"><a class="tailor-text-link" href="' + href(data['process']['href']) + '">' + text(data['process']['action']) + ' →</a></div>')
    benefits = ''.join('<article><strong>' + text(c['title']) + '</strong><p>' + text(c['description']) + '</p></article>' for c in data['benefits']['cards'])
    result['benefits'] = section('tailoring-benefits', 'tailor-benefits', data['benefits'], '<div class="tailor-benefit-grid">' + benefits + '</div><div class="section-action"><a class="tailor-text-link" href="' + href(data['benefits']['href']) + '">' + text(data['benefits']['action']) + ' →</a></div>')
    options = ''.join('<a href="' + href(c['href']) + '"><span class="tailor-option-label">' + text(c['kicker']) + '</span><h3>' + text(c['title']) + '</h3><p>' + text(c['description']) + '</p><span>' + text(c['action']) + ' →</span></a>' for c in data['options']['cards'])
    result['options'] = section('order-options', 'tailor-options', data['options'], '<div class="tailor-options-grid">' + options + '</div>')
    programmes = ''.join('<a href="' + href(c['href']) + '"><strong>' + text(c['title']) + '</strong><span>' + text(c['description']) + '</span></a>' for c in data['programs']['cards'])
    result['programs'] = section('customer-programs', 'tailor-programs', data['programs'], '<div class="tailor-programs-grid">' + programmes + '</div>')
    final = data['final']
    result['final'] = section('tailoring-final', 'tailor-final', final, '<div class="tailor-final-actions">' + actions(final['actions']) + '</div>')
    return result
