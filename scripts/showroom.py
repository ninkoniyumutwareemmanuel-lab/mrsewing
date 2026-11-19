"""Universal, publication-gated clothing Showroom and reusable home showcase."""
from html import escape
from pathlib import Path
from urllib.parse import urlencode
import json
import re

from media_library import ROOT, DOMAIN, published_items, facets, settings, public_item, inventory, inventory_markdown


def _json(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')


def _picture(item, eager=False, home=False):
    from build_collections import picture
    if item['mediaType'] == 'video':
        poster = item['poster']
        source = escape(item['assetPath'], quote=True)
        result = '<video controls muted playsinline preload="none" poster="' + escape(poster['image']['thumb'], quote=True) + '" aria-label="' + escape(item['alternativeText'], quote=True) + '"><source src="' + source + '" type="' + ('video/webm' if source.endswith('.webm') else 'video/mp4') + '"><p>Your browser cannot play this video. <a href="' + source + '">Open the video separately</a>.</p></video>'
        return result + '<p class="showroom-video-fallback"><a href="' + source + '">Open video separately</a></p>'
    value = picture(item['image'], eager=eager)
    if home:
        value = re.sub(r'sizes="[^"]*"', 'sizes="(min-width:1100px) 560px,(min-width:700px) 50vw,100vw"', value)
    return value


def _card(item, index=0):
    attrs = {
        'data-media-id': item['mediaId'], 'data-audience': item['audience'],
        'data-garment-type': item['garmentType'], 'data-style-tags': ' '.join(item['styleTags']),
        'data-classification': item['classification'],
    }
    attributes = ''.join(' ' + key + '="' + escape(value, quote=True) + '"' for key, value in attrs.items())
    url = escape(item['detailUrl'], quote=True)
    link_class = 'showroom-shop-link' if item['classification'] == 'shop-product' else 'showroom-design-link'
    body = '<div class="showroom-card-copy"><span class="showroom-badge">' + escape(item['classificationLabel']) + '</span><h2>' + escape(item['title']) + '</h2><span class="showroom-filename">' + escape(item['originalFilename']) + '</span></div>'
    if item['mediaType'] == 'video':
        primary = _picture(item) + '<a class="' + link_class + '" href="' + url + '">' + body + '</a>'
    else:
        primary = '<a class="' + link_class + '" href="' + url + '">' + _picture(item, eager=index < 2) + body + '</a>'
    links = []
    if item.get('projectUrl'):
        links.append('<a href="' + escape(item['projectUrl'], quote=True) + '">View completed work</a>')
    if item.get('shopUrl') and item['classification']!='shop-product':
        links.append('<a href="' + escape(item['shopUrl'], quote=True) + '">View Shop listing</a>')
    if links:
        primary += '<div class="showroom-card-links">' + ''.join(links) + '</div>'
    return '<article class="showroom-card"' + attributes + '>' + primary + '</article>'


def _select(identifier, name, label, options):
    return '<div class="showroom-filter-field"><label for="' + identifier + '">' + label + '</label><select id="' + identifier + '" name="' + name + '"><option value="">All</option>' + ''.join('<option value="' + escape(key, quote=True) + '">' + escape(text) + '</option>' for key, text in options.items()) + '</select></div>'


def render():
    from tailoring_positioning import whatsapp_action,service_label
    service_title=escape(service_label())
    from customer_site import frame
    from customer_navigation import breadcrumb
    from announcement_bar import decorate
    items = published_items()
    groups = facets(items)
    controls = _select('showroomAudience', 'audience', 'For whom?', groups['audiences']) + _select('showroomGarment', 'garment', 'Clothing', groups['garments']) + _select('showroomStyle', 'style', 'Style', groups['styles']) + _select('showroomClass', 'kind', 'Collection source', groups['classifications'])
    controls += '<div class="showroom-search-field"><label for="showroomSearch">Search designs or original filenames</label><input id="showroomSearch" name="q" type="search" maxlength="160" placeholder="Try Kaunda or m-kaundasuits3.jpeg" autocomplete="off"></div><div class="showroom-filter-actions"><button id="showroomClear" type="button">Clear filters</button></div>'
    body = '<div class="showroom-view">' + breadcrumb([('Home', '/'), ('Showroom', None)]) + '<header class="showroom-intro"><p class="home-eyebrow">Mr Sewing Fashion · Kigali, Rwanda</p><h1>Clothing Showroom</h1><p>Explore approved clothing photographs, find a style you like and continue to its details for a personal tailoring request.</p><p class="showroom-note">Reference Design means inspiration; Our Work identifies confirmed Mr Sewing projects. Photographs do not confirm ready-made stock, fabric availability or a fixed service price.</p><div class="showroom-enquiry-action">' + whatsapp_action(context='showroom') + '<p>Open a design for an enquiry about that exact photograph, or send your own picture in WhatsApp.</p></div></header><form id="showroomFilters" class="showroom-filters" role="search" aria-label="Filter the clothing Showroom">' + controls + '</form><p id="showroomCount" class="showroom-count" role="status" aria-live="polite">' + str(len(items)) + ' designs</p><p id="showroomEmpty" class="showroom-empty" hidden>No designs match these filters. Try another search or clear the filters.</p><section id="showroomGrid" class="showroom-grid" aria-label="Published clothing designs">' + ''.join(_card(item, i) for i, item in enumerate(items)) + '</section><noscript><p>All approved items are shown. Enable JavaScript to filter by audience, garment, style or filename.</p></noscript><nav class="showroom-actions" aria-label="Plan your tailoring request"><a class="home-button home-button-gold" href="/services/custom-tailoring/">' + service_title + '</a><a class="home-button" href="/services/custom-tailoring/selected-designs/">Your Selected Designs</a><a class="home-button" href="/services/custom-tailoring/special-order/">Request Special Tailoring</a><a class="home-button" href="/shop/">Visit the Shop</a></nav><p class="showroom-note">Open a design photograph to see its details and select it using the existing tailoring journey. A Shop listing has its own availability and enquiry conditions.</p></div>'
    html = frame('/showroom/', 'Clothing Showroom', 'Explore approved clothing photographs, custom suit references and genuine Mr Sewing work in Kigali, Rwanda. Filter by audience, garment and style, then request a personal quotation.', body, kind='CollectionPage')
    html = html.replace('</head>', '<link rel="stylesheet" href="/assets/showroom.css?v=staging-r51"></head>')
    schema = {'@context': 'https://schema.org', '@type': 'ItemList', 'name': 'Mr Sewing Fashion clothing Showroom', 'numberOfItems': len(items), 'itemListElement': [{'@type': 'ListItem', 'position': i + 1, 'name': item['title'], 'url': DOMAIN + item['detailUrl'].split('?')[0]} for i, item in enumerate(items)]}
    html = html.replace('</head>', '<script type="application/ld+json">' + _json(schema) + '</script></head>')
    return decorate(html.replace('</body>', '<script id="showroomData" type="application/json">' + _json({'items': [public_item(item) for item in items], 'facets': groups}) + '</script><script src="/assets/showroom.js?v=staging-r51" defer></script></body>'))


def homepage_showcase():
    from tailoring_positioning import whatsapp_action,service_label
    service_title=escape(service_label())
    items = published_items()
    config = settings(items)['homepage']
    by_id = {item['mediaId']: item for item in items}
    cards = []
    for card in config['cards']:
        item = by_id[card['mediaId']]
        audience = card['audience']
        url = '/showroom/?' + urlencode({'audience': audience})
        label = "Men’s Suit Tailoring" if audience == 'men' else "Women’s Tailoring"
        image = _picture(item, eager=True, home=True)
        copy = '<div class="home-showcase-copy"><span class="home-showcase-badge">' + escape(item['classificationLabel']) + '</span><h2>' + label + '</h2><p>' + escape(item['title']) + '</p><span>Explore tailoring designs →</span></div>'
        if item['mediaType'] == 'video':
            content = image + '<a href="' + url + '">' + copy + '</a>'
        else:
            content = '<a href="' + url + '">' + image + copy + '</a>'
        cards.append('<article class="home-showcase-card" data-feature-media="' + item['mediaId'] + '">' + content + '</article>')
    feature = by_id[config['featuredMediaId']]
    feature_url = feature.get('projectUrl') or feature['detailUrl']
    feature_label = 'Made by Mr Sewing' if feature['classification'] == 'our-work' else 'Find your next tailoring inspiration'
    feature_picture = _picture(feature, eager=False, home=True)
    feature_copy = '<div class="home-showcase-feature-copy"><span class="home-showcase-badge">' + escape(feature['classificationLabel']) + '</span><h2>' + escape(feature_label) + '</h2><p>' + escape(feature['title']) + '</p><p>Explore a completed tailoring project, then share your own requirements for assessment.</p><a class="home-button home-button-gold" href="' + escape(feature_url, quote=True) + '">Explore this look</a><a class="home-button" href="/services/custom-tailoring/">' + service_title + '</a></div>'
    introduction = '<header class="home-tailoring-intro"><p class="home-eyebrow">Mr Sewing Fashion · Kigali, Rwanda</p><h1>Professional Tailor in Kigali, Rwanda</h1><p>Custom-made suits, special tailoring, clothing alterations and professional garment services.</p><p>Have a design in mind? Share it with us and request a personalized quotation.</p><div class="home-tailoring-actions">' + whatsapp_action(context='homepage-showcase') + '<a class="home-button" href="/services/custom-tailoring/">' + service_title + '</a><a class="home-button" href="/showroom/">Explore the Showroom</a></div></header>'
    showcase = '<section class="home-fashion-showcase" aria-label="Tailoring at Mr Sewing Fashion"><div class="home-shell">' + introduction + '<div class="home-showcase-grid">' + ''.join(cards) + '</div><article class="home-showcase-feature" data-feature-media="' + feature['mediaId'] + '"><div class="home-showcase-feature-photo">' + feature_picture + '</div>' + feature_copy + '</article></div></section>'
    sharing = '<section class="home-design-sharing" aria-labelledby="home-design-sharing-heading"><div class="home-shell"><div class="home-design-sharing-card"><div><p class="home-eyebrow">Your design, assessed with care</p><h2 id="home-design-sharing-heading">Have a Design in Mind?</h2><p>Already have a photo of the suit or outfit you want? Send it to Mr Sewing Fashion on WhatsApp. We’ll review your requirements, discuss fabric options and help you request a personalized quotation.</p><h3>Choose Your Design. We’ll Help With the Fabric and Tailoring.</h3><p>Discuss fabric options with our team, choose a preference through the Fabric Guide, or ask about using your own fabric. Suitability, colours and availability require confirmation.</p></div><div class="home-design-sharing-action">' + whatsapp_action(context='homepage-design-card') + '<p>WhatsApp opens after your consent. Attach your photograph and press Send there. Your design is subject to assessment.</p><a href="/booking/">Prefer a website enquiry? Request a quotation.</a></div></div></div></section>'
    return showcase + sharing


def homepage_css():
    return (ROOT / '_templates/homepage-showcase.css').read_text()


def outputs():
    items = published_items()
    settings(items)
    recovery = inventory()
    return {
        ROOT / 'showroom/index.html': render(),
        ROOT / 'assets/showroom.css': (ROOT / '_templates/showroom.css').read_text(),
        ROOT / 'assets/showroom.js': (ROOT / '_templates/showroom.js').read_text(),
        ROOT / '_data/media-library-index.json': json.dumps({'schemaVersion': 1, 'generatedFrom': ['collection-designs.json', 'customer-projects.json', 'media-video-records.json', 'shop-products.json'], 'items': [public_item(item) for item in items]}, ensure_ascii=False, indent=2) + '\n',
        ROOT / 'docs/media-recovery-inventory.json': json.dumps(recovery, ensure_ascii=False, indent=2) + '\n',
        ROOT / 'docs/MEDIA_RECOVERY_INVENTORY.md': inventory_markdown(recovery),
    }
