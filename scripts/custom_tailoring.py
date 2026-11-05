"""Homepage-protected tailoring landing/ordering pages; existing galleries and enquiry provider."""
from pathlib import Path
from html import escape, unescape
import json,re
import shared_components as shared
from homepage_resources import delivery,CSS as ICON_CSS
ROOT=Path(__file__).resolve().parents[1]
BASE='/services/custom-tailoring/'
STANDARD=BASE+'standard-order/'
SPECIAL=BASE+'special-order/'

def component(name,current=None):
    markup=(ROOT/f'_templates/homepage-{name}.html').read_text()
    items=[]
    for g in json.loads((ROOT/'_data/homepage-guides.json').read_text()):
        label=escape(g['label'])
        if g['label']=='Fabric Guide':g={**g,'href':'/guides/fabrics/'}
        if g['href']:
            assert g['href']=='/guides/fabrics/' or (ROOT/g['href'].strip('/')/'index.html').is_file()
            items.append('<li><a href="'+escape(g['href'],quote=True)+'">'+label+'</a></li>')
        else:
            cls='footer-guide-pending' if name=='footer' else 'nav-guide-pending'
            span='pending-guide' if name=='footer' else 'home-nav-pending'
            items.append(f'<li class="{cls}"><span class="{span}" title="This guide will be developed separately">{label}</span></li>')
    markup=markup.replace('{{customer_guides}}',''.join(items))
    if name=='header':
        markup=markup.replace(' href="/" aria-current="page"',' href="/"')
        markup=markup.replace('href="'+(current or BASE)+'"','href="'+(current or BASE)+'" aria-current="page"',1)
    return delivery(markup,name)

def render(kind='landing'):
    import customer_site as release
    return release.service_page('custom-tailoring') if kind=='landing' else release.standard() if kind=='standard' else release.request_page(True)

def legacy_render(kind='landing'):
    route={'landing':BASE,'standard':STANDARD,'special':SPECIAL}[kind]
    title={'landing':'Custom Tailoring & Suits in Kigali | Mr Sewing Fashion','standard':'Choose a Website Suit Design | Mr Sewing Fashion','special':'Submit a Special Tailoring Request | Mr Sewing Fashion'}[kind]
    description={'landing':'Custom tailoring and suits in Kigali, Rwanda. Choose a website design or share your own inspiration for personal assessment, measurements and an individual quotation.','standard':'Choose men’s or women’s suit designs from the Mr Sewing Fashion website. Explore existing galleries and request a quotation for your selected design reference.','special':'Describe your own garment design, sketches or reference ideas for a Special Order assessment with Mr Sewing Fashion. Enquiries require feasibility review and quotation.'}[kind]
    content=(ROOT/f'_templates/custom-tailoring-{kind}.html').read_text()
    process_source=(ROOT/'_templates/homepage-sections.html').read_text()
    process=re.search(r'<ol class="home-step-grid">.*?</ol>',process_source,re.S)[0]
    process=process.replace('We carry out the agreed tailoring, alteration or garment-care work.', 'We carry out the agreed tailoring and arrange fittings where applicable.')
    content=content.replace('{{six_steps}}',process)
    # Reuse the existing browser-intended provider configuration; never invent an upload backend.
    existing=(ROOT/'_templates/homepage-quotation.html').read_text()
    action=unescape(re.search(r'<form[^>]*action="([^"]+)"',existing)[1])
    access=unescape(re.search(r'name="access_key" value="([^"]+)"',existing)[1])
    assert action=='https://api.web3forms.com/submit'
    content=content.replace('{{form_action}}',escape(action,quote=True)).replace('{{form_key}}',escape(access,quote=True))
    schema={'@context':'https://schema.org','@graph':[{'@type':'WebPage','@id':'https://mrsewingfashion.com'+route+'#webpage','url':'https://mrsewingfashion.com'+route,'name':title,'description':description,'isPartOf':{'@id':'https://mrsewingfashion.com/#website'}},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':'https://mrsewingfashion.com/'},{'@type':'ListItem','position':2,'name':'Custom Tailoring & Suits','item':'https://mrsewingfashion.com'+BASE}]}]}
    if kind=='landing':schema['@graph'].append({'@type':'Service','name':'Custom Tailoring & Suits','serviceType':'Custom tailoring and made-to-measure suits','provider':{'@id':'https://mrsewingfashion.com/#organization'},'areaServed':{'@type':'Place','name':'Kigali, Rwanda'},'url':'https://mrsewingfashion.com'+route})
    else:schema['@graph'][1]['itemListElement'].append({'@type':'ListItem','position':3,'name':'Standard Order' if kind=='standard' else 'Special Order','item':'https://mrsewingfashion.com'+route})
    source=(ROOT/'_templates/custom-tailoring-page.html').read_text()
    vals={'title':escape(title),'title_attr':escape(title,quote=True),'description':escape(description,quote=True),'route':route,'content':content,'header':component('header'),'footer':component('footer'),'schema':json.dumps(schema,ensure_ascii=False).replace('<','\\u003c'),'styles':shared.site_css()+'\n'+(ROOT/'_templates/homepage-phase1.css').read_text()+'\n'+ICON_CSS}
    for k,v in vals.items():source=source.replace('{{'+k+'}}',v)
    assert not re.search(r'{{\w+}}',source)
    return source

def outputs():
    import customer_site as release
    return {ROOT/STANDARD.strip('/')/'index.html':release.standard(),ROOT/SPECIAL.strip('/')/'index.html':release.request_page(True),**release.outputs()}

def legacy_outputs():
    return {ROOT/STANDARD.strip('/')/'index.html':render('standard'),ROOT/SPECIAL.strip('/')/'index.html':render('special'),ROOT/'assets/custom-tailoring.js':shared.menu_script()+'\n'+(ROOT/'_templates/custom-tailoring.js').read_text(),ROOT/'assets/custom-tailoring.css':(ROOT/'_templates/custom-tailoring.css').read_text()}
