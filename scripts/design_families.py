"""Family navigation over the existing publication-gated collection records.

No separate catalogue, new selection state or availability promise. Callers pass
only the effective loader output; raw held records are additionally excluded.
"""
from html import escape
from urllib.parse import urlencode


def family_navigation(design, published_designs, picture):
    family = design.get('family')
    if not isinstance(family, dict) or not family.get('id'):
        return ''
    def eligible(other):
        return (other.get('published') is not False
                and other.get('rightsStatus', 'approved') == 'approved'
                and other.get('metadataReviewStatus', 'approved') == 'approved'
                and not other.get('publicationBlockers'))
    if not eligible(design):
        return ''
    current_gender = design.get('gender')
    members = [other for other in published_designs
               if eligible(other) and other.get('family', {}).get('id') == family['id']
               and other.get('gender') == current_gender]
    unique = {}
    for other in members:
        unique.setdefault(other['id'], other)
    if len(unique) < 2:
        return ''
    from build_collections import design_route
    cards = []
    seen = set()
    for other in unique.values():
        image = other['images'][0]
        if image['src'] in seen:
            continue
        seen.add(image['src'])
        variant = other['family'].get('variant', {})
        label = variant.get('label') or variant.get('colour') or other['name']
        url = design_route(other) + '?' + urlencode({'design': other['id'], 'photo': 'https://mrsewingfashion.com' + image['src']})
        current = ' aria-current="page"' if other['id'] == design['id'] else ''
        cards.append('<a class="design-family-variant" href="' + escape(url, quote=True) + '"' + current + '>'
                     + picture(image) + '<span>' + escape(label) + '</span></a>')
    if len(cards) < 2:
        return ''
    return ('<section class="design-family" aria-labelledby="design-family-heading">'
            '<h2 id="design-family-heading">' + escape(family.get('name') or design['name']) + '</h2>'
            '<p>Explore the colour references in this design family. Fabric colours and availability require confirmation.</p>'
            '<nav class="design-family-options" aria-label="Choose a design colour reference">'
            + ''.join(cards) + '</nav></section>')
