"""Shared customer shell over existing public authorities, without a second catalogue.

Navigation presentation belongs to site-shell.json. Contacts/social/location,
hours, service/action labels and guides retain their existing source owners.
The Suits link deliberately uses the current useful category section until the
independent information hub is reviewed. The combined service uses its existing
WhatsApp enquiry, not a fictitious new form or unpublished page.
"""
from html import escape
import json
from pathlib import Path
import re
from urllib.parse import quote, unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]


def read(name, root=ROOT):
    return json.loads((Path(root) / '_data' / name).read_text())


def configuration(root=ROOT):
    data = read('site-shell.json', root)
    if data.get('schemaVersion') != 1:
        raise ValueError('Unsupported site shell schema')
    return data


def destination(key, root=ROOT):
    """Resolve a stable shell destination using its owning label/contact sources."""
    item = configuration(root)['destinations'][key]
    labels = read('customer-interface-labels.json', root)
    label = (item['navLabel'] if 'navLabel' in item else
             labels['services'][item['serviceId']] if 'serviceId' in item else
             labels['actions'][item['actionId']] if 'actionId' in item else item['label'])
    if 'whatsappMessageId' in item:
        number = re.sub(r'\D', '', read('business.json', root)['telephone'])
        if not number:
            raise ValueError('A verified business telephone is required')
        message = read('service-contact-actions.json', root)['messages'][item['whatsappMessageId']]
        href = 'https://wa.me/' + number + '?text=' + quote(message, safe='')
    else:
        href = item['href']
        if not href.startswith('/') or href.startswith('//'):
            raise ValueError('Shell page destinations must be local absolute routes')
    return {'id': key, 'label': label, 'href': href}


def link(item, current=None):
    href = item['href']
    selected = ' aria-current="page"' if current and href == current and '#' not in href else ''
    external = ' target="_blank" rel="noopener"' if href.startswith('https://wa.me/') else ''
    return '<a href="' + escape(href, quote=True) + '"' + selected + external + '>' + escape(item['label']) + '</a>'


def links(keys, root=ROOT, current=None):
    return ''.join('<li>' + link(destination(key, root), current) + '</li>' for key in keys)


def hours_summary(root=ROOT):
    hours = read('business-hours.json', root)
    business = read('business.json', root)
    short = {'Monday': 'Mon', 'Tuesday': 'Tue', 'Wednesday': 'Wed', 'Thursday': 'Thu',
             'Friday': 'Fri', 'Saturday': 'Sat', 'Sunday': 'Sun'}
    days = business['openingHoursSpecification'][0]['dayOfWeek']
    labels = [short[day.rsplit('/', 1)[-1]] for day in days]
    order = list(short.values())
    indices = [order.index(day) for day in labels]
    if len(labels) > 1 and indices == list(range(indices[0], indices[-1] + 1)):
        day_label = labels[0] + '–' + labels[-1]
    else:
        day_label = ', '.join(labels)
    result = f"{day_label} {hours['regularOpen']}–{hours['regularClose']} · Umuganda: {hours['umugandaOpen']}–{hours['umugandaClose']} by advance appointment"
    if hours['sundayByAppointment']:
        result += ' · Sunday: by appointment only'
    return result


def guide_links(root=ROOT):
    return ''.join('<li>' + link({'label': item['label'], 'href': item['href']}) + '</li>'
                   for item in read('homepage-guides.json', root) if item.get('href'))


def social_links(root=ROOT):
    socials = read('contact-v2.json', root)['social']
    classes = {'facebook': 'facebook-f', 'instagram': 'instagram', 'tiktok': 'tiktok', 'youtube': 'youtube'}
    labels = {'facebook': 'Facebook', 'instagram': 'Instagram', 'tiktok': 'TikTok', 'youtube': 'YouTube'}
    result = []
    for name in configuration(root)['socialOrder']:
        href = socials.get(name)
        if not href:
            continue
        if urlsplit(href).scheme != 'https':
            raise ValueError('Social links must use HTTPS')
        result.append('<a href="' + escape(href, quote=True) + '" target="_blank" rel="noopener" aria-label="' + escape(labels[name]) + '"><i class="fab fa-' + classes[name] + '"></i></a>')
    return ''.join(result)


def render(name, current=None, root=ROOT):
    if name not in ('header', 'footer'):
        raise ValueError('Unknown shared shell component')
    root = Path(root)
    config = configuration(root)
    business = read('business.json', root)
    contact = read('contact-v2.json', root)
    brand = business['name'].upper()
    prefix, suffix = (brand.rsplit(' ', 1) if brand.endswith(' FASHION') else (brand, ''))
    logo = urlsplit(business['logo'])
    if logo.netloc and logo.netloc != urlsplit(business['url']).netloc:
        raise ValueError('The logo must belong to the verified website')
    nav = []
    for key in config['primaryNavigation']:
        if key == 'services':
            nav.append('<li class="services-dropdown"><details><summary>Services <span aria-hidden="true">⌄</span></summary><ul>' + links(config['serviceNavigation'], root, current) + '</ul></details></li>')
        else:
            nav.append('<li>' + link(destination(key, root), current) + '</li>')
    workshop = contact['mainWorkshop']
    company = read('customer-information.json', root)['company']
    values = {
        'workshop_summary': escape(workshop['name'] + ' · ' + workshop['streetAddress']),
        'hours_summary': escape(hours_summary(root)),
        'brand_label': escape(business['name']), 'brand_prefix': escape(prefix), 'brand_suffix': escape(suffix),
        'logo_src': escape(unquote(logo.path).lstrip('/'), quote=True),
        'primary_navigation': ''.join(nav),
        'footer_services': links(config['footerServices'], root),
        'customer_guides': guide_links(root),
        'footer_information': links(config['footerInformation'], root),
        'footer_programs': links(config['footerPrograms'], root),
        'footer_policies': links(config['footerPolicies'], root),
        'social_links': social_links(root),
        'copyright': escape(str(config['copyrightYear']) + ' ' + company + '. All Rights Reserved.'),
        'telephone': escape(business['telephone']),
        'telephone_href': escape('tel:' + business['telephone'], quote=True),
        'email': escape(business['email']),
        'email_href': escape('mailto:' + business['email'], quote=True),
    }
    markup = (root / '_templates' / f'homepage-{name}.html').read_text()
    for key, value in values.items():
        markup = markup.replace('{{' + key + '}}', value)
    if re.search(r'{{\w+}}', markup):
        raise ValueError('Unexpanded shared shell placeholder')
    return markup
