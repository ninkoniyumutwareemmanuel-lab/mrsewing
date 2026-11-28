"""S01 editorial projection; business rules, media and form contracts stay shared.

Custom clothing owns this page. Suits information belongs to the queued I01 hub;
until it is approved the existing category anchor keeps its useful destinations.
"""
from html import escape
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def content_data(root=ROOT):
    data = json.loads((Path(root) / '_data/custom-tailoring-content.json').read_text())
    if data.get('schemaVersion') != 1 or data.get('pageId') != 'S01':
        raise ValueError('Unsupported Custom Tailoring content')
    return data


def text(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError('Custom Tailoring copy must be non-empty text')
    return escape(value, quote=True)


def page_link(url, label, css='home-text-link'):
    # Editorial data cannot introduce an external host, script or private URL.
    if not isinstance(url, str) or not url.startswith('/') or url.startswith('//') or '\\' in url or any(ord(c) < 32 for c in url):
        raise ValueError('Custom Tailoring destinations must be local routes')
    return '<a class="' + text(css) + '" href="' + text(url) + '">' + text(label) + '</a>'


def paragraph(value):
    return '<p>' + text(value) + '</p>'


def section(ident, record, body):
    aliases = {
        'fabric-and-fitting': ['tailoring-hub-fabric-title'],
        'tailoring-process': ['tailoring-hub-intro'],
        'tailoring-conditions': ['tailoring-hub-essentials-title'],
        'tailoring-guidance': ['tailoring-hub-faq-title'],
        'tailoring-enquiry': ['tailoring-hub-final-title', 'tailoring-hub-additional'],
    }
    anchors = ''.join('<span class="s01-legacy-anchor" id="' + old + '" aria-hidden="true"></span>' for old in aliases.get(ident, []))
    return '<section class="release-section s01-section" aria-labelledby="' + ident + '">' + anchors + '<h2 id="' + ident + '">' + text(record['title']) + '</h2>' + (paragraph(record['description']) if record.get('description') else '') + body + '</section>'


def actions():
    from customer_interface import action
    from service_landings import contact_link
    # Existing Special Tailoring is the direct custom-clothing enquiry. No new
    # form, selection storage, provider or WhatsApp implementation is introduced.
    return page_link('/services/custom-tailoring/special-order/', action('requestQuote'), 'home-button home-button-gold') + contact_link('special-order', 'home-button s01-secondary')


def render(service, hero):
    from build_collections import load, picture
    from clothing_categories import active
    from customer_policies import facts
    from public_content import public_texts
    from customer_interface import action

    data = content_data()
    policy = facts()
    texts = public_texts(policy['texts'])
    cover = hero('custom-tailoring')
    cover = cover.replace('<h1>' + escape(service['title']) + '</h1>', '<h1>' + text(data['hero']['title']) + '</h1>', 1)
    cover = cover.replace(escape(service['intro']), text(data['hero']['description']), 1)
    cover = re.sub(r'(<div class="service-hero-actions">).*?(</div>)', lambda match: match[1] + actions() + match[2], cover, count=1, flags=re.S)

    scope = '<div class="s01-columns">' + ''.join('<article><h3>' + text(item['title']) + '</h3>' + paragraph(item['description']) + '</article>' for item in data['scope']['items']) + '</div>'
    prep = data['preparation']
    preparation = '<div class="s01-columns"><article><h3>' + text(prep['fabricTitle']) + '</h3>' + paragraph(prep['fabricDescription']) + page_link('/guides/fabrics/', 'Explore the Fabric Guide') + '</article><article><h3>' + text(prep['measurementsTitle']) + '</h3>' + paragraph(prep['measurementsDescription']) + page_link('/measurements/', 'Read the Measurements Guide') + '</article></div><details class="s01-detail"><summary>' + text(prep['ownFabricSummary']) + '</summary>' + paragraph(texts[prep['ownFabricPolicyKey']]) + '</details>'
    process = '<ol class="s01-steps">' + ''.join('<li><span aria-hidden="true">' + f'{i:02}' + '</span><div><h3>' + text(step['title']) + '</h3>' + paragraph(step['description']) + '</div></li>' for i, step in enumerate(data['process']['steps'], 1)) + '</ol>'

    tailoring = policy['services']['custom-tailoring']
    payments = policy['payments']
    facts_rows = [
        ('Standard tailoring estimate', tailoring['standardTurnaround'], 'Actual timing depends on the assessed garment and accepted order.'),
        ('Express estimate', tailoring['expressTurnaround'], 'Feasibility, capacity and the agreed surcharge apply.'),
        ('Normal domestic advance', str(payments['domesticCustomAdvancePercent']) + '%', 'Before official work begins; accepted order requirements still apply.'),
        ('Domestic completion balance', str(payments['domesticCustomBalancePercent']) + '%', 'For standard suits: after tailoring completion, before final cleaning and release.')
    ]
    conditions = '<div class="tailoring-hub-fact-grid">' + ''.join('<article class="tailoring-hub-fact"><h3>' + text(title) + '</h3><strong>' + text(value) + '</strong>' + paragraph(description) + '</article>' for title, value, description in facts_rows) + '</div>'
    # Full shared rules are projected by key rather than independently rewritten.
    conditions += '<div class="s01-conditions">' + ''.join('<details class="s01-detail" id="' + text(item['id']) + '"><summary>' + text(item['title']) + '</summary>' + ''.join(paragraph(texts[key]) for key in item['policyKeys']) + '</details>' for item in data['conditions']['details']) + '</div>'
    conditions += paragraph('Full payment must be verified before garment release. Read the payment guidance and applicable Terms before confirming your order.')
    conditions += page_link('/customer-information/', 'Read order & payment guidance')

    cards = []
    # This uses the single gated category/design catalogue, never a second list
    # of garment photographs. Keep category orientation before design selection.
    for category in active(load()[0]):
        route = category.get('landingRoute', category['url'])
        page_link(route, category['name'])  # Validate centrally configured routes.
        cards.append('<a class="tailoring-hub-category" href="' + text(route) + '">' + picture(category['cover']['images'][0]) + '<span><h3>' + text(category['name']) + '</h3><strong>' + text(action('browseDesigns')) + '<span aria-hidden="true"> →</span></strong></span></a>')
    suits = '<div class="tailoring-hub-category-grid">' + ''.join(cards) + '</div>' + page_link('/collections/', 'Browse All Designs in the Showroom')
    support = '<ul class="s01-guidance-links">' + ''.join('<li>' + page_link(item['href'], item['label']) + '</li>' for item in data['support']['links']) + '</ul>'
    final = '<div class="service-hero-actions">' + actions() + '</div><p class="s01-related">Need work on an existing garment? ' + page_link('/services/alterations/', 'Alterations & Repairs') + ' · ' + page_link('/services/garment-care/', 'Garment Care') + '</p>'
    return cover + '<div class="s01-content">' + section('custom-clothing', data['scope'], scope) + section('fabric-and-fitting', prep, preparation) + section('tailoring-process', data['process'], process) + section('tailoring-conditions', data['conditions'], conditions) + section('tailoring-hub-categories', data['suits'], suits) + section('tailoring-guidance', data['support'], support) + section('tailoring-enquiry', data['final'], final) + '</div>'
