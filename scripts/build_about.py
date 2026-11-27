#!/usr/bin/env python3
"""Build About Us V2 with the existing shared V2 components and verified assets."""
from site_seo import finalize
import argparse
from html import escape
import json
from pathlib import Path
import re
from build_homepage import reserve_image_space
from build_clean_urls import legacy_script
from homepage_resources import delivery, source_set, CSS as ICON_CSS
import shared_components as shared

ROOT = Path(__file__).resolve().parents[1]
PAGE = 'https://mrsewingfashion.com/about/'


def leadership_section(record=None):
    """Render only a deliberately published, owner-approved leadership record."""
    if record is None:
        record = json.loads((ROOT/'_data/about-leadership.json').read_text())
    if not record.get('published'):
        return ''
    if record.get('approvalStatus') != 'approved':
        raise ValueError('Leadership publication requires approved public content')
    for field in ('name', 'title', 'biography'):
        if not isinstance(record.get(field), str) or not record[field].strip():
            raise ValueError('Leadership publication requires ' + field)
    portrait = record.get('portrait')
    if not isinstance(portrait, dict) or portrait.get('publicationApproved') is not True:
        raise ValueError('Leadership portrait publication permission is required')
    path = portrait.get('path', '')
    image = (ROOT/path).resolve()
    if not path or not image.is_relative_to(ROOT) or not image.is_file() or image.suffix.lower() not in ('.jpg', '.jpeg', '.png', '.webp', '.avif'):
        raise ValueError('Leadership portrait must resolve to an approved local image')
    if not isinstance(portrait.get('alt'), str) or not portrait['alt'].strip():
        raise ValueError('Leadership portrait needs descriptive alternative text')
    if any(not isinstance(portrait.get(k), int) or isinstance(portrait[k], bool) or portrait[k] <= 0 for k in ('width', 'height')):
        raise ValueError('Leadership portrait needs positive intrinsic dimensions')
    photo = ('<img src="/'+escape(path.lstrip('/'), quote=True)+'" alt="'+escape(portrait['alt'], quote=True)+'" '
        f'width="{portrait["width"]}" height="{portrait["height"]}" loading="lazy" decoding="async">')
    copy = [record['biography']]
    copy.extend(record[k] for k in ('motivation', 'philosophy', 'vision') if isinstance(record.get(k), str) and record[k].strip())
    values = {'leadership_portrait':photo, 'leadership_name':escape(record['name']),
        'leadership_role':escape(record['title']), 'leadership_copy':''.join('<p>'+escape(p)+'</p>' for p in copy)}
    output = (ROOT/'_templates/about-leadership.html').read_text()
    for key, value in values.items():
        output = output.replace('{{'+key+'}}', value)
    return output


def render():
    return legacy_render()

def legacy_render():
    seo = json.loads((ROOT/'_data/page-seo.json').read_text())['about.html']
    business = json.loads((ROOT/'_data/business.json').read_text())
    organization = {'@type':'Organization','@id':business['@id'],
        **{k:business[k] for k in ['name','url','logo','telephone','email']},
        'alternateName':'Mr Sewing',
        'description':'Kigali-based bespoke tailoring brand creating personalized clothing in Rwanda.',
        'parentOrganization':{'@type':'Organization','name':'NINKONIYUMUTWARE NEXUS LTD'}}
    schema = {'@context':'https://schema.org','@graph':[
        {'@type':'AboutPage','@id':PAGE+'#webpage','url':PAGE,'name':seo['title'],
         'about':{'@id':business['@id']},'mainEntity':{'@id':business['@id']},
         'isPartOf':{'@id':'https://mrsewingfashion.com/#website'}},organization,
        {'@type':'BreadcrumbList','itemListElement':[
            {'@type':'ListItem','position':1,'name':'Home','item':'https://mrsewingfashion.com/'},
            {'@type':'ListItem','position':2,'name':'About Mr Sewing','item':PAGE}]}]}
    # Keep the operating-company logo subordinate to the Mr Sewing brand story.
    image = ('<img class="about-hero-image about-logo" src="assets/images/nexus-logo-480.webp" '
        'srcset="assets/images/nexus-logo-480.webp 480w, assets/images/nexus-logo-960.webp 960w" '
        'sizes="140px" width="1536" height="1024" loading="lazy" '
        'decoding="async" alt="NINKONIYUMUTWARE NEXUS LTD operating-company logo">')
    header = delivery(re.sub(r'<img\b[^>]*>', reserve_image_space, shared.header('/about/')), 'header')
    values = {'services_picker':shared.services_picker(),'header':header,'footer':delivery(shared.footer(),'footer'),
        'styles':shared.component_css()+'\n'+ICON_CSS+'\n'+(ROOT/'_templates/about.css').read_text(),
        'schema':json.dumps(schema,ensure_ascii=False,indent=2),'hero_image':image,'leadership':leadership_section(),
        'legacy_redirect':legacy_script('about.html'),
        'page_title':escape(seo['title'],quote=True),'page_description':escape(seo['description'],quote=True)}
    output = (ROOT/'_templates/about.html').read_text()
    for key,value in values.items():output = output.replace('{{'+key+'}}',value)
    if re.search(r'{{\w+}}',output):raise ValueError('Unexpanded About template placeholder')
    return '<!-- Generated by scripts/build_about.py; edit _templates/about.html/about.css or page SEO data. -->\n'+output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true');args=parser.parse_args()
    outputs = {ROOT/'about.html':render(), ROOT/'assets/about-navigation.js':
        '/* Generated from _templates/shared/navigation.js. */\n'+shared.menu_script()+
        '\n/* Preserve legacy order bookmarks using the existing homepage flow. */\nif (location.hash === "#orderModal") location.replace("/#orderModal");\n'}
    outputs[ROOT/'assets/about-navigation.js']+=(ROOT/'_templates/services-picker.js').read_text()
    for path,value in outputs.items():
        if path.suffix=='.html':value=finalize(value,path)
        if args.check:
            if not path.exists() or path.read_text()!=value:raise SystemExit('About V2 out of date: '+str(path.relative_to(ROOT)))
        else:path.write_text(value)
    print('PASS: About V2 template, shared components and outputs are synchronized.' if args.check else 'Generated About V2 and lightweight shared navigation.')

if __name__=='__main__':main()
