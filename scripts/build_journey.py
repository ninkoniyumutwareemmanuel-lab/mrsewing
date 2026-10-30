#!/usr/bin/env python3
"""Evidence-led Services / Our Work pages. No project is published without permission."""
from site_seo import finalize
import argparse,json,re
from html import escape
from pathlib import Path
from urllib.parse import urlencode
import shared_components as shared
from homepage_resources import delivery,CSS as ICON_CSS
from build_homepage import reserve_image_space,image_size
from build_clean_urls import legacy_script,DISCOVERY_LINKS
from garment_care import catalog as care_catalog,care_information,care_navigation,care_summary
ROOT=Path(__file__).resolve().parents[1]
DOMAIN='https://mrsewingfashion.com'

def services():
    data=json.loads((ROOT/'_data/journey-services.json').read_text())
    assert len({s['route'] for s in data})==len(data)
    assert all(all((ROOT/p).is_file() for p in s['sources']) for s in data)
    return data

def projects():
    records=json.loads((ROOT/'_data/customer-projects.json').read_text())['projects'];published=[]
    for p in records:
        assert re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',p['slug'])
        if not p.get('published'):continue
        assert p.get('completedWorkEvidence') and p.get('publicationPermission',{}).get('approved') is True and p['publicationPermission'].get('evidenceRef'),'Completion and publication permission required'
        assert p.get('title') and p.get('context') and p.get('images')
        for image in p['images']:
            assert image.get('permissionEvidenceRef') and image.get('projectAssociationEvidenceRef')
            path=(ROOT/image['src'].lstrip('/')).resolve()
            assert image['src'].startswith('/') and path.is_relative_to(ROOT) and path.is_file() and path.suffix.lower() in ['.jpg','.jpeg','.png','.webp','.avif']
            assert image.get('alt') and image.get('width') and image.get('height')
        if p.get('testimonial'):assert p['testimonial'].get('approvalEvidenceRef') and p['testimonial'].get('text')
        published.append(p)
    assert len({p['slug'] for p in records})==len(records)
    return published

def enquiry(name,route):
    text='Hello Mr Sewing! I would like to enquire about '+name+'.\n'+DOMAIN+route
    return '<a class="journey-enquiry" target="_blank" rel="noopener" href="https://wa.me/250787411501?'+escape(urlencode({'text':text}),quote=True)+'">Enquire with Mr Sewing <span class="home-arrow" aria-hidden="true"></span></a>'

def page(route,title,description,content,schema_type='WebPage',schema_extra=None):
    schema={'@context':'https://schema.org','@type':schema_type,'name':title,'description':description,'url':DOMAIN+route,**(schema_extra or {})}
    if route.startswith('/services/') and route!='/services/':
        schema['breadcrumb']={'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':DOMAIN+'/'},{'@type':'ListItem','position':2,'name':'Services','item':DOMAIN+'/services/'},{'@type':'ListItem','position':3,'name':title.split(' | ')[0],'item':DOMAIN+route}]}
        content='<nav class="journey-back" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true"> / </span><a href="/services/">Services</a><span aria-hidden="true"> / </span><span>'+escape(title.split(' | ')[0])+'</span></nav>'+content
    vals={'title':escape(title,quote=True),'description':escape(description,quote=True),'route':route,'content':content,'schema':json.dumps(schema,ensure_ascii=False).replace('<','\\u003c'),'styles':shared.component_css()+'\n'+ICON_CSS+'\n'+(ROOT/'_templates/journey.css').read_text(),'header':delivery(re.sub(r'<img\b[^>]*>',reserve_image_space,shared.header('/services/garment-care/' if route.startswith('/services/garment-care/') else '/services/' if route.startswith('/services/') or route.startswith('/service-') or route in ['/our-process/','/made-to-measure/'] else '/shop/' if route=='/shop/' else '/our-work/')),'header'),'footer':delivery(shared.footer(),'footer')}
    out=(ROOT/'_templates/journey-page.html').read_text().replace('</head>',DISCOVERY_LINKS+'</head>',1)
    for key,value in vals.items():out=out.replace('{{'+key+'}}',value)
    assert not re.search(r'{{\w+}}',out)
    if route=='/services/' or route.startswith('/service-'):out=out.replace('<head>','<head>'+legacy_script(route.strip('/')+'.html'),1)
    return out

def metadata(route,default_title,description):
    name=route.strip('/')+'.html';seo=json.loads((ROOT/'_data/page-seo.json').read_text()).get(name)
    return (seo['title'],seo['description']) if seo else (default_title+' | Mr Sewing Fashion, Kigali',description)

def service_picture(service,eager=False):
    src=service['visual'];alt=escape(service['visualAlt'],quote=True)
    if src.startswith('assets/journey/'):
        width,height=1672,941;srcset='/assets/journey/garment-care-480.webp 480w, /assets/journey/garment-care-960.webp 960w'
    else:
        width,height=image_size(ROOT/src);variants=json.loads((ROOT/'_data/image-delivery.json').read_text()).get(src,{}).get('variants',[])
        srcset=', '.join('/'+v['src']+' '+str(v['width'])+'w' for v in variants if v['src'].endswith('.webp'))
        if srcset:srcset+=', '
        srcset+='/'+src+' '+str(width)+'w'
    return '<img class="service-card-image" src="/'+src+'" srcset="'+srcset+'" sizes="(min-width: 1100px) 360px, (min-width: 700px) 45vw, 90vw" alt="'+alt+'" width="'+str(width)+'" height="'+str(height)+'" loading="'+('eager' if eager else 'lazy')+'" decoding="async">'

def overview(data):
    content='<section class="journey-intro"><p class="home-eyebrow">Mr Sewing · Kigali</p><h1>Tailoring, made personal.</h1><p>From a first idea to a considered fit. Find the service that meets your needs, then talk with us about the details.</p></section><div class="journey-grid">'
    for n,service in enumerate(data):content+='<a class="journey-card" href="'+service['route']+'">'+service_picture(service,n<3)+'<span class="journey-number">'+str(n+1).zfill(2)+'</span><h2>'+escape(service['title'])+'</h2><p>'+escape(service['intro'])+'</p><span class="home-text-link">Explore service <span class="home-arrow" aria-hidden="true"></span></span></a>'
    content+='</div><p class="journey-image-note">Garment photographs show design inspiration, not verified customer projects. Measurement illustrations explain fitting concepts. The garment-care still life is AI-generated and does not depict Mr Sewing premises, staff or customer work.</p>'
    title,desc=metadata('/services/','Tailoring Services','Explore custom tailoring, wedding and graduation outfits, mobile fittings, garment-care enquiries, alterations and express requests with Mr Sewing in Kigali.')
    return page('/services/',title,desc,content,'CollectionPage')

def service_page(service):
    if service['id']=='garment-care':return care_page(service)
    route=service['route'];kind=service['id']
    content='<div class="service-kind-'+kind+'"><section class="journey-intro"><p class="home-eyebrow">A personal service · Kigali</p><h1>'+escape(service['title'])+'</h1><p>'+escape(service['intro'])+'</p></section><section class="service-feature" aria-label="Service introduction">'+service_picture(service,True)+'<div><h2>'+{'custom-tailoring':'Your wardrobe. Your expression.','wedding-tailoring':'For a moment that matters.','graduation-tailoring':'Mark your milestone.','mobile-fitting':'A fitting around your day.','alterations':'A considered refinement.','express':'Tell us your exact deadline.'}.get(kind,'Made personal.')+'</h2><p>'+escape(service['audience'])+'</p><p class="journey-image-note">'+('Measurement illustration; not a customer appointment photograph.' if kind in ['mobile-fitting','alterations'] else 'Garment design inspiration; not a documented customer project.')+'</p></div></section><div class="service-layout"><div class="service-copy">'
    for title,text in service['sections']:content+='<section><h2>'+escape(title)+'</h2><p>'+escape(text)+'</p></section>'
    content+='<section><h2>What to share with us</h2><ul class="service-requirements">'+''.join('<li>'+escape(item)+'</li>' for item in service['requirements'])+'</ul></section><section><h2>How to begin</h2><ol class="service-steps">'+''.join('<li>'+escape(step)+'</li>' for step in service['steps'])+'</ol></section>'
    related={'custom-tailoring':[('/mensuits/','Men’s collection'),('/womensuits/','Women’s collection')],'wedding-tailoring':[('/collections/?occasion=wedding','Wedding inspiration'),('/collections/?occasion=civil-wedding','Civil wedding inspiration')],'graduation-tailoring':[('/collections/?occasion=graduation','Graduation inspiration')],'mobile-fitting':[('/measurements/','Measurement guide')],'alterations':[('/booking-adjustment/','Request an assessment')]}.get(kind,[])
    if related:content+='<nav class="service-related" aria-label="Related guidance">'+''.join('<a class="home-text-link" href="'+url+'">'+escape(title)+'</a>' for url,title in related)+'</nav>'
    content+='</div><aside class="service-enquiry" aria-label="Service enquiry"><p class="home-eyebrow">Let’s begin with a conversation</p><p>'+escape({'mobile-fitting':'Include your Kigali location and preferred dates. Coverage, visit charges and appointment availability must be confirmed.','express':'Include the exact date and time you need the garment. Capacity, fees and timing must be confirmed before production.'}.get(kind,'Share your garment needs and references. We will discuss suitable options, a quote and arrangements before you proceed.'))+'</p>'+enquiry(service['title'],route)+'</aside></div></div>'
    title,desc=metadata(route,service['title'],service['intro']+' Discuss your requirements with Mr Sewing in Kigali.')
    return page(route,title,desc,content,'WebPage',{'mainEntity':{'@type':'Service','serviceType':service['title'],'provider':{'@id':DOMAIN+'/#organization'},'areaServed':'Kigali, Rwanda'}})

def care_page(service,category=None):
    _,published=care_catalog();route=service['route']+(category['slug']+'/' if category else '')
    title=category['title'] if category else 'Mr Sewing Garment Care'
    description=category['description'] if category else 'Discuss garment care with Mr Sewing in Kigali. Confirm suitable care options, eligibility, a quote and timing before arranging a service.'
    content='<div class="home-shell">'+care_navigation()+'<section class="care-hero"><div class="care-hero-copy"><p class="home-eyebrow">Premium Clothing Care · Kigali, Rwanda</p><h1>'+escape(title)+'</h1><p>'+escape(description)+'</p></div><img src="/assets/journey/garment-care-960.webp" srcset="/assets/journey/garment-care-480.webp 480w, /assets/journey/garment-care-960.webp 960w" sizes="(min-width: 1240px) 1200px, 100vw" width="1672" height="941" alt="AI-generated still life of a black jacket, folded shirt and garment brush" loading="eager" fetchpriority="high" decoding="async"></section><p class="care-disclosure">AI-generated editorial illustration. This is not a photograph of Mr Sewing premises, equipment, staff, customer garments or completed work.</p>'+care_summary(category)+'<section id="care-options" class="care-section"><p class="home-eyebrow">Consider the garment first</p><h2>'+escape(category['title'] if category else 'Care tailored to your garment.')+'</h2>'
    if category:
        content+='<p>'+escape(category['description'])+'</p><div class="care-details">'
        for heading,key in [('Suitable garments','suitableGarments'),('How it works','process'),('Before you request care','customerPreparation')]:content+='<section><h3>'+heading+'</h3><ul>'+''.join('<li>'+escape(v)+'</li>' for v in category[key])+'</ul></section>'
        content+='</div><div class="care-details"><section><h3>Care limitations</h3><ul>'+''.join('<li>'+escape(v)+'</li>' for v in category['limitations'])+'</ul></section>'
        if category.get('treatmentOptions'):content+='<section><h3>Treatment options</h3><ul>'+''.join('<li>'+escape(v)+'</li>' for v in category['treatmentOptions'])+'</ul></section>'
        if category.get('pickupDelivery'):content+='<section><h3>Collection arrangements</h3><p>'+escape(category['pickupDelivery'])+'</p></section>'
        content+='</div>'
    elif published:content+='<div class="care-options">'+''.join('<a class="care-option" href="/services/garment-care/'+v['slug']+'/"><h3>'+escape(v['title'])+'</h3><p>'+escape(v['description'])+'</p><span class="home-text-link">Explore care service</span></a>' for v in published)+'</div>'
    else:content+='<p>Tell us about your garment and its care label. We will confirm which care options are available and suitable before accepting a request. Specific treatments are not listed until their availability and conditions are confirmed.</p><div class="care-details"><section><h3>The garment</h3><p>Share the garment type, care label and any condition concerns. A photograph can help begin the conversation.</p></section><section><h3>The conversation</h3><p>Ask which options and conditions apply. Care benefits associated with premium orders depend on eligibility; they are not universal.</p></section><section><h3>The agreement</h3><p>Confirm suitability, any charges and the estimated timing directly with the team before proceeding.</p></section></div>'
    content+='</section><section id="care-pricing" class="care-section"><p class="home-eyebrow">Clear details, before you proceed</p><h2>Quotes &amp; timing</h2>'
    rows=[r for r in category['pricing']['rows'] if r.get('approved')] if category else []
    if rows:
        content+='<div class="care-price-scroll"><table class="care-price-table"><caption>Approved care prices in Rwandan francs (RWF)</caption><thead><tr><th scope="col">Garment</th><th scope="col">Service</th><th scope="col">Standard price</th></tr></thead><tbody>'+''.join('<tr><td>'+escape(r['garmentType'])+'</td><td>'+escape(r['serviceType'])+'</td><td>RWF '+format(r['standardPriceRwf'],',')+'</td></tr>' for r in rows)+'</tbody></table></div>'
        for row in rows:
            for charge in row.get('additionalCharges',[]):
                if charge.get('approved'):content+='<p class="care-rate-notes">'+escape(charge['label'])+': RWF '+format(charge['amountRwf'],',')+'</p>'
            if row.get('notes'):content+='<p class="care-rate-notes">'+escape(row['notes'])+'</p>'
    else:content+='<p>Request an assessment and quote for your garment. We will confirm the applicable care options, charges and estimated turnaround before you agree. No prices or completion times are implied by this page.</p>'
    if category:
        timing=category['pricing']['standardTurnaround'];express=category['pricing']['express']
        if timing['approved']:content+='<p class="care-rate-notes">Standard turnaround estimate: '+str(timing['minimum'])+'–'+str(timing['maximum'])+' '+escape(timing['unit'].replace('_',' '))+'. Confirm the timing for your garment before proceeding.</p>'
        if express['approved'] and express['available']:content+='<p class="care-rate-notes">Express service may be requested, subject to confirmation.'+(' Additional charge: RWF '+format(express['additionalChargeRwf'],',')+'.' if express.get('additionalChargeRwf') else '')+'</p>'
    content+='</section><section class="care-section"><h2>Before you enquire</h2><p>Have your garment details, care-label information, any condition concerns and preferred completion date ready. The team must confirm what is possible. Do not assume that a particular treatment, collection visit or delivery arrangement is available.</p></section><section id="care-request" class="care-request"><h2>A considered next step.</h2><p>Ask about '+escape(category['title'] if category else 'care for your garment')+'. Opening a conversation does not confirm a service, order or appointment.</p>'+enquiry(title,route)+'</section></div>'
    out=page(route,title+' | Mr Sewing Fashion, Kigali',description,content)
    return out.replace('class="journey-main home-shell"','class="care-main"').replace('</style>','\n'+(ROOT/'_templates/garment-care.css').read_text()+'\n'+(ROOT/'_templates/completion.css').read_text()+'</style>',1)

def project_picture(image,eager=False,sizes='(min-width: 1000px) 900px, 90vw'):
    src=image['src'];name=src.lstrip('/');optim=json.loads((ROOT/'_data/image-delivery.json').read_text()).get(name,{})
    candidates=[{'src':'/'+v['src'],'width':v['width']} for v in optim.get('variants',[]) if v['src'].endswith('.webp')]
    candidates.append({'src':src,'width':image['width']})
    srcset=image.get('srcset') or ', '.join(v['src']+' '+str(v['width'])+'w' for v in candidates)
    tag='<img src="'+escape(src,quote=True)+'" srcset="'+escape(srcset,quote=True)+'" sizes="'+sizes+'" alt="'+escape(image['alt'],quote=True)+'" width="'+str(image['width'])+'" height="'+str(image['height'])+'" loading="'+('eager' if eager else 'lazy')+'"'+(' fetchpriority="high"' if eager else '')+' decoding="async">'
    return tag

def project_page(p):
    route='/our-work/'+p['slug']+'/'
    sections=''.join('<section><h2>'+label+'</h2><p>'+escape(p[key])+'</p></section>' for key,label in [('requestedDesign','The requested design'),('process','The tailoring process')] if p.get(key))
    sections+=''.join('<section><h2>'+escape(e['heading'])+'</h2><p>'+escape(e['text'])+'</p></section>' for e in p.get('editorial',[]))
    vals={'project_title':escape(p['title']),'context':escape(p['context']),'photos':''.join('<a class="project-photo" data-project-photo="'+str(n)+'" href="'+escape(i['src'],quote=True)+'">'+project_picture(i,n==0)+'</a>' for n,i in enumerate(p['images'])),'documented_sections':sections,'testimonial':'<blockquote class="project-quote">'+escape(p['testimonial']['text'])+'</blockquote>' if p.get('testimonial') else '', 'enquiry':enquiry(p['title'],route)}
    content=(ROOT/'_templates/customer-project.html').read_text()
    for k,v in vals.items():content=content.replace('{{'+k+'}}',v)
    content+='<dialog id="project-viewer" class="project-viewer" aria-label="Completed project photographs"><button type="button" id="project-close">Close photograph</button><img alt=""><div class="project-viewer-controls"><button type="button" id="project-previous" aria-label="Previous photograph">←</button><p id="project-photo-count" role="status" aria-live="polite"></p><button type="button" id="project-next" aria-label="Next photograph">→</button></div></dialog><script id="project-photos" type="application/json">'+json.dumps([{k:i[k] for k in ['src','alt','width','height']} for i in p['images']]).replace('<','\\u003c')+'</script>'
    out=page(route,p['title']+' | Mr Sewing Fashion',p['context'],content).replace('</head>','<meta property="og:image:alt" content="'+escape(p['images'][0]['alt'],quote=True)+'"><script src="/assets/project-gallery.js" defer></script></head>',1)
    return out.replace(DOMAIN+'/assets/images/mr-logo-480.webp',DOMAIN+p['images'][0]['src'])

def work_page(approved):
    content='<section class="journey-intro"><p class="home-eyebrow">Our Work</p><h1>Every garment has a story.</h1><p>A personal design. A considered fit. A meaningful occasion. Explore finished Mr Sewing projects through garment photographs, considered silhouettes and the details that make each look distinct.</p></section>'
    if approved:
        content+='<div class="work-project-grid">'+''.join('<article class="work-project"><a href="/our-work/'+p['slug']+'/">'+project_picture(p['images'][0],n==0,'(min-width: 1100px) 380px, (min-width: 700px) 45vw, 90vw')+'<h2>'+escape(p['title'])+'</h2></a><p>'+escape(p['context'])+'</p></article>' for n,p in enumerate(approved))+'</div>'
    else:content+='<section class="work-note"><div><p class="home-eyebrow">Stories, shared with care</p><h2>Details matter.<br>Permission does too.</h2></div><p>Our individual customer project features are being prepared. We publish a story only when the completed work, photograph association and permission to share are confirmed. In the meantime, explore the design collection for inspiration or talk with us about your own tailoring plans.</p></section>'
    content+='<nav class="work-links" aria-label="Continue exploring"><a class="home-text-link" href="/collections/">Explore design inspiration <span class="home-arrow" aria-hidden="true"></span></a><a class="home-text-link" href="/services/">Discover our services <span class="home-arrow" aria-hidden="true"></span></a><a class="home-text-link" href="/contact/">Discuss your project <span class="home-arrow" aria-hidden="true"></span></a></nav>'
    return page('/our-work/','Our Work & Customer Projects | Mr Sewing Fashion','Explore how Mr Sewing presents customer tailoring projects with confirmed details and permission, or discover design inspiration and tailoring services in Kigali.',content,'CollectionPage')

def outputs():
    data=services();approved=projects();out={ROOT/'services.html':overview(data),ROOT/'our-work/index.html':work_page(approved),ROOT/'assets/journey-navigation.js':shared.menu_script()+'''\n/* Keep service enquiries on the current origin on staging. */
document.querySelectorAll('.journey-enquiry').forEach(a=>{const u=new URL(a.href),text=u.searchParams.get('text');if(text)u.searchParams.set('text',text.replace('https://mrsewingfashion.com',location.origin));a.href=u.href;});
'''}
    for service in data:out[ROOT/service['route'].strip('/')/'index.html']=service_page(service)
    care=next(s for s in data if s['id']=='garment-care')
    for category in care_catalog()[1]:out[ROOT/'services/garment-care'/category['slug']/'index.html']=care_page(care,category)
    for project in approved:out[ROOT/'our-work'/project['slug']/'index.html']=project_page(project)
    aliases=json.loads((ROOT/'_data/route-aliases.json').read_text())
    for name,target in aliases.items():
        if ROOT/target.strip('/')/'index.html' not in out:continue
        value=out[ROOT/target.strip('/')/'index.html']
        out[ROOT/name]=value.replace('<head>','<head><script data-legacy-url>location.replace('+json.dumps(target)+'+location.search+location.hash)</script>',1)
    stale=set((ROOT/'our-work').glob('*/index.html'))-{ROOT/'our-work'/p['slug']/'index.html' for p in approved}
    stale |= set((ROOT/'services/garment-care').glob('*/index.html'))-{ROOT/'services/garment-care'/c['slug']/'index.html' for c in care_catalog()[1]}-{ROOT/'services/garment-care'/n/'index.html' for n in ['services','planning']}
    if stale:raise AssertionError('Unpublished project/care output requires review: '+str(stale))
    return out

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    for path,value in outputs().items():
        if path.suffix=='.html':value=finalize(value,path)
        if args.check:
            if not path.exists() or path.read_text()!=value:raise SystemExit('Stale journey page: '+str(path.relative_to(ROOT)))
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(value)
    print(f'PASS: {len(services())} service details; {len(projects())} evidence-approved project stories; journey pages '+('synchronized.' if args.check else 'generated.'))
if __name__=='__main__':main()
