#!/usr/bin/env python3
"""Build Contact V2 from its template and the approved homepage design components.

Homepage/unrelated pages are never written. Run this before build_clean_urls.py.
Contact-specific locations/social data stay scoped to this page during the V2 rollout.
"""
import argparse
from copy import deepcopy
from html import escape
import json
from pathlib import Path
import re
from build_homepage import Section, reserve_image_space
from homepage_resources import delivery, CSS as ICON_CSS
from build_clean_urls import legacy_script

ROOT = Path(__file__).resolve().parents[1]
PAGE = 'https://mrsewingfashion.com/contact/'


def component(source, tag, identifier=None):
    parser = Section(source, tag, identifier)
    parser.feed(source)
    if parser.markup is None:
        raise ValueError(f'Missing Contact component: {identifier or tag}')
    return parser.markup


def shared_css(source):
    """Select common design rules without shipping homepage gallery/hero styles.

The approved stylesheet uses ordinary rules and nested @media only. Unknown
at-rules fail explicitly so a future design change cannot silently corrupt CSS.
"""
    source = re.sub(r'/\*.*?\*/', '', source, flags=re.S)
    common = re.compile(r'^(?::root|\*|html|body|img|a(?=\s|$)|button|figure|h[123]|p(?=\s|$)|ul|ol|dl|dd|:focus-visible|\.home-shell|\.home-section|\.home-eyebrow|\.section-heading|\.home-button|\.home-text-link|\.home-arrow|\.visually-hidden|\.skip-link|#site-header|\.homepage-header|\.header-|\.home-brand|\.brand-name|\.home-menu-toggle|\.coming-soon|\.shop-nav|\.mobile-shop|\.js |\.home-final|\.final-|\.homepage-footer|\.footer-|\.social-icons)')
    output = []
    pos = 0
    while pos < len(source):
        start = source.find('{', pos)
        if start == -1:
            if source[pos:].strip():raise ValueError('Unexpected trailing design CSS')
            break
        selector = source[pos:start].strip()
        depth, end, quote = 1, start + 1, None
        while end < len(source) and depth:
            char = source[end]
            if quote:
                if char == quote and source[end-1] != '\\':quote = None
            elif char in "\"'":quote = char
            elif char == '{':depth += 1
            elif char == '}':depth -= 1
            end += 1
        if depth:raise ValueError('Unbalanced approved CSS')
        body = source[start+1:end-1]
        if selector.startswith('@media'):
            nested = shared_css(body)
            if nested.strip():output.append(selector + ' {\n' + nested + '\n}')
        elif selector.startswith('@'):
            raise ValueError('Unsupported design at-rule: ' + selector)
        else:
            selectors = [s.strip() for s in selector.split(',') if common.match(s.strip())]
            if selectors:output.append(', '.join(selectors) + ' {' + body + '}')
        pos = end
    return '\n'.join(output)


def contact_schema():
    business = json.loads((ROOT/'_data/business.json').read_text())
    data = json.loads((ROOT/'_data/contact-v2.json').read_text())
    org_id = business['@id']
    main_id, mic_id = PAGE+'#main-workshop', PAGE+'#downtown-consultation'
    def address(place):
        return {'@type':'PostalAddress', **{k:place[k] for k in ['streetAddress','addressLocality','addressCountry']}}
    # Organization + separately qualified Places avoids assigning workshop hours
    # to the appointment-only consultation venue or inventing a staffed branch.
    organization = {'@type':'Organization','@id':org_id,'name':business['name'],
        'alternateName':'Mr Sewing','url':business['url'],'telephone':business['telephone'],
        'email':business['email'],'logo':business['logo'],'sameAs':list(data['social'].values()),
        'location':[{'@id':main_id},{'@id':mic_id}]}
    main = {'@type':'Place','@id':main_id,'name':data['mainWorkshop']['name'],
        'address':address(data['mainWorkshop']),'hasMap':data['mainWorkshop']['mapsUrl'],
        'openingHoursSpecification':deepcopy(business['openingHoursSpecification']),
        'specialOpeningHoursSpecification':deepcopy(business['specialOpeningHoursSpecification']),
        'description':business['disambiguatingDescription']}
    mic = {'@type':'Place','@id':mic_id,'name':data['consultationLocation']['name'],
        'address':address(data['consultationLocation']),
        'description':'MIC Building, Downtown Kigali, Rwanda. Consultations by appointment only; not a walk-in workshop.'}
    if data['consultationLocation']['verifiedMapsUrl']:
        mic['hasMap'] = data['consultationLocation']['verifiedMapsUrl']
    return {'@context':'https://schema.org','@graph':[
        {'@type':'ContactPage','@id':PAGE+'#webpage','url':PAGE,'name':'Contact Mr Sewing Fashion in Kigali',
         'isPartOf':{'@id':'https://mrsewingfashion.com/#website'},'about':{'@id':org_id},'mainEntity':{'@id':org_id}},
        organization,main,mic]}


def render():
    data = json.loads((ROOT/'_data/contact-v2.json').read_text())
    seo = json.loads((ROOT/'_data/page-seo.json').read_text())['contact.html']
    home = (ROOT/'_templates/homepage-sections.html').read_text()
    header = component(home, 'header')
    header = header.replace(' aria-current="page"', '')
    header = header.replace('href="#customers-section"','href="/#customers-section"').replace('href="#services"','href="/#services"')
    header = header.replace('<a href="/contact/">','<a href="/contact/" aria-current="page">')
    header = delivery(re.sub(r'<img\b[^>]*>', reserve_image_space, header), 'header')
    footer = (ROOT/'_templates/homepage-footer.html').read_text()
    # Reuse the exact approved layout, with Contact-only confirmed venue details.
    location = '''<div class="footer-col footer-location"><h3>Location</h3><p><strong>Main Workshop</strong><br>Karama, Norvege, KN 441 St, Nyarugenge, Kigali</p><p><strong>MIC Building</strong><br>Downtown Kigali<br>By appointment only</p><a class="home-text-link" href="'''+escape(data['mainWorkshop']['mapsUrl'],quote=True)+'''" target="_blank" rel="noopener">Workshop Directions <span class="home-arrow" aria-hidden="true">↗</span></a></div>'''
    old_location = component(footer,'div',('class','footer-col footer-location'))
    footer = footer.replace(old_location,location)
    # Social links are rendered once, in the page's dedicated social section.
    socials = component(footer,'div',('class','social-icons'))
    footer = footer.replace(socials,'')
    footer = footer.replace('Usually Monday–Saturday','Main workshop: Monday–Saturday')
    footer = delivery(footer,'footer')
    social_names = {"instagram":"Instagram","facebook":"Facebook","tiktok":"TikTok","youtube":"YouTube"}
    social_markup = '\n'.join(f'<a href="{escape(url,quote=True)}" target="_blank" rel="noopener"><i class="fab fa-{name if name!="facebook" else "facebook-f"}"></i><span>{social_names[name]}</span><span class="home-arrow" aria-hidden="true">↗</span></a>' for name,url in data['social'].items())
    social_markup = delivery(social_markup,'social')
    css = shared_css((ROOT/'_templates/homepage.css').read_text()) + '\n' + ICON_CSS + '\n' + (ROOT/'_templates/contact.css').read_text()
    template = (ROOT/'_templates/contact.html').read_text()
    replacements = {'header':header,'footer':footer,'social_links':social_markup,'styles':css,
        'legacy_redirect':legacy_script('contact.html'),
        'page_title':escape(seo['title'],quote=True),'page_description':escape(seo['description'],quote=True),
        'schema':json.dumps(contact_schema(),ensure_ascii=False,indent=2),
        'main_map':escape(data['mainWorkshop']['mapsUrl'],quote=True)}
    mic_map=data['consultationLocation']['verifiedMapsUrl']
    replacements['mic_directions']=(f'<a class="home-text-link" href="{escape(mic_map,quote=True)}" target="_blank" rel="noopener">Get Directions <span class="home-arrow" aria-hidden="true">↗</span></a>' if mic_map else '<p class="contact-note">Please contact us for directions when arranging your appointment.</p>')
    for key,value in replacements.items():template=template.replace('{{'+key+'}}',value)
    if re.search(r'{{\w+}}',template):raise ValueError('Unexpanded Contact template placeholder')
    return '<!-- Generated by scripts/build_contact.py; edit _templates/contact.html/contact.css or _data/contact-v2.json. -->\n'+'\n'.join(line.rstrip() for line in template.splitlines())+'\n'


def navigation():
    # Reuse the approved menu controller verbatim, without the homepage gallery/
    # consent code. No runtime imports or third-party navigation dependency.
    source=(ROOT/'assets/homepage.js').read_text()
    start=source.index('(function setupHomepageMenu()')
    controller=source[start:]
    return ('/* Generated by scripts/build_contact.py from the approved menu controller. */\n'+controller+
        '\n/* Preserve old Contact order bookmarks via the existing homepage consent flow. */\nif (location.hash === "#orderModal") location.replace("/#orderModal");\n')


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--check',action='store_true');args=p.parse_args()
    outputs={ROOT/'contact.html':render(),ROOT/'assets/contact-navigation.js':navigation()}
    for path,output in outputs.items():
        if args.check:
            if not path.exists() or path.read_text()!=output:raise SystemExit('Contact V2 out of date: '+str(path.relative_to(ROOT)))
        else:path.write_text(output)
    print('PASS: Contact V2 matches its template, approved design and scoped data.' if args.check else 'Generated contact.html and its lightweight navigation; homepage unchanged.')

if __name__=='__main__':main()
