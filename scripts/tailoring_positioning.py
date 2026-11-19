"""R52 tailoring presentation and existing Terms-gated WhatsApp action.

The phone remains owned by business.json/business_settings. This module owns
presentation copy, not a contact record, selection system or consent controller.
Design arguments must identify a publication-gated request reference. Browser
enhancement uses the current host and actual selected approved photograph.
"""
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import urlencode, urlparse, unquote

ROOT = Path(__file__).resolve().parents[1]


def settings():
    data = json.loads((ROOT / '_data/tailoring-positioning.json').read_text())
    assert data['schemaVersion'] == 1
    assert data['whatsapp']['label']
    assert len(data['whatsapp']['message']) < 1000
    # Validate/use the established contact authority; never duplicate its value.
    from business_settings import settings as business
    assert business()['phoneDigits']
    return data


def service_label():
    from business_settings import services
    return next(service['title'] for service in services() if service['id']=='custom-tailoring')


def _path(value):
    parsed = urlparse(str(value))
    if parsed.scheme or parsed.netloc:
        assert parsed.scheme == 'https' and parsed.netloc == 'mrsewingfashion.com', 'Unapproved reference host'
    assert parsed.path.startswith('/') and not parsed.query and not parsed.fragment, 'Invalid reference path'
    assert not any(part in {'.', '..'} for part in unquote(parsed.path).split('/')), 'Invalid reference path'
    return unquote(parsed.path)


def _design_context(design, photo, detail):
    references = json.loads((ROOT / '_data/request-reference-allowlist.json').read_text())
    if isinstance(design, dict):
        ident = design.get('id') or design.get('designId')
        requested_name = design.get('name')
    else:
        ident, requested_name = design, None
    assert ident in references, 'WhatsApp design must be a publication-approved reference'
    record = references[ident]
    # Builders may pass the existing approved customer-facing detail heading.
    name = str(requested_name or record['name'])
    assert 0 < len(name) <= 200 and not re.search(r'[\r\n\x00-\x1f]', name), 'Invalid design name'
    name = re.sub(r'\s*[—·-]\s*MS-\d+\b', '', name).strip()
    route = record['route']
    if detail is not None:
        assert _path(detail) == _path(route), 'Design route does not match approved reference'
    images = record['images']
    selected = images[0] if photo is None else next((image for image in images if _path(photo) == _path(image['src'])), None)
    assert selected, 'Photograph does not belong to the approved design'
    return str(ident), name, selected['src'], route


def whatsapp_action(context='homepage-showcase', css='home-button home-button-gold', label=None, design=None, photo=None, detail=None):
    """Return one existing-consent anchor. No message or photograph is sent.

    For a detail page, use design={'id': d['id'], 'name': approved_heading};
    optionally supply its approved photo source and existing detail route. The
    static fallback identifies the design without inventing a production link.
    The client adds exact current-host photograph/detail links before consent.
    """
    data = settings()
    assert re.fullmatch(r'[a-z][a-z0-9-]{0,63}', context), 'Invalid CTA context'
    assert all(re.fullmatch(r'[A-Za-z_][A-Za-z0-9_-]*', part) for part in css.split()), 'Invalid CTA classes'
    attrs = {'class': ('tailoring-whatsapp-action ' + css).strip(), 'data-whatsapp-modal': '', 'data-tailoring-whatsapp': context}
    message = data['whatsapp']['message']
    if design is not None:
        ident, name, source, route = _design_context(design, photo, detail)
        attrs.update({'data-tailoring-design': ident, 'data-tailoring-design-name': name, 'data-tailoring-photo': source, 'data-tailoring-detail': route})
        message = data['whatsapp']['designIntroduction'] + '\nDesign: ' + name + '\n' + data['whatsapp']['manualPhotoNote']
    else:
        assert photo is None and detail is None, 'A photograph/detail requires an approved design'
    attrs['href'] = '/whatsapp/?' + urlencode({'text': message})
    attrs['target'] = '_blank'
    attrs['rel'] = 'noopener'
    return '<a ' + ' '.join(key if value == '' else key + '="' + escape(value, quote=True) + '"' for key, value in attrs.items()) + '>' + escape(label or data['whatsapp']['label']) + '</a>'


def client_script():
    config = json.dumps(settings(), ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')
    return (ROOT / '_templates/tailoring-enquiry.js').read_text().replace('{{tailoring_positioning_config}}', config)


def outputs():
    return {
        ROOT / 'assets/tailoring-enquiry.js': client_script(),
        ROOT / 'assets/tailoring-enquiry.css': (ROOT / '_templates/tailoring-enquiry.css').read_text(),
    }
