"""Sanitised customer release driven by the owner's explicit 5 November decisions.
Internal source registers/reconciliations live outside the deployment root.
"""
from pathlib import Path
from html import escape,unescape
import json,re
from urllib.parse import urlencode
ROOT=Path(__file__).resolve().parents[1]
DOMAIN='https://mrsewingfashion.com'
BASE='/services/custom-tailoring/'

def data():return json.loads((ROOT/'_data/customer-release.json').read_text())
def service_map():return {s['id']:s for s in data()['services']}
def link(url,label,cls='home-text-link'):return '<a class="'+cls+'" href="'+escape(url,quote=True)+'">'+escape(label)+'</a>'
def intro(title,text,label='Mr Sewing Fashion · Kigali, Rwanda'):
 return '<section class="release-intro"><p class="home-eyebrow">'+escape(label)+'</p><h1>'+escape(title)+'</h1><p>'+escape(text)+'</p></section>'
def section(title,paragraphs,id=None):
 return '<section class="release-section"'+(' id="'+escape(id,quote=True)+'"' if id else '')+'><h2>'+escape(title)+'</h2>'+''.join('<p>'+escape(p)+'</p>' for p in (paragraphs if isinstance(paragraphs,list) else [paragraphs]))+'</section>'
def related():
 return '<nav class="release-related" aria-label="Customer guidance">'+''.join(link(u,t) for u,t in [('/services/','Four Services'),('/customer-information/','Orders & Payments'),('/guides/fabrics/','Fabric Guide'),('/measurements/','Measurements Guide'),('/delivery-and-collection/','Delivery & Collection'),('/benefits/','Suit Benefits'),('/customer-support/','Customer Support')])+'</nav>'
def frame(route,title,description,content,kind='WebPage',service=None):
 from custom_tailoring import component
 import shared_components as shared
 from homepage_resources import CSS as ICON_CSS
 seo=json.loads((ROOT/'_data/page-seo.json').read_text()).get(route.strip('/')+'.html')
 if seo:title,description=seo['title'],seo['description']
 else:title=title+' | Mr Sewing Fashion, Kigali'
 graph=[{'@type':kind,'@id':DOMAIN+route+'#page','name':title,'url':DOMAIN+route,'description':description,'isPartOf':{'@id':DOMAIN+'/#website'}},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Home','item':DOMAIN+'/'},{'@type':'ListItem','position':2,'name':title.split(' | ')[0],'item':DOMAIN+route}]}]
 if route=='/about/':
  business=json.loads((ROOT/'_data/business.json').read_text());graph.append({'@type':'Organization','@id':business['@id'],**{k:business[k] for k in ['name','url','telephone','email','logo']},'alternateName':'Mr Sewing','parentOrganization':{'@type':'Organization','name':'NINKONIYUMUTWARE NEXUS LTD'}})
 if route=='/contact/':
  from build_contact import contact_schema
  graph.extend(n for n in contact_schema()['@graph'] if n.get('@type') in ['Organization','Place'])
 if service:graph.append({'@type':'Service','name':service['title'],'serviceType':service['title'],'url':DOMAIN+route,'provider':{'@id':DOMAIN+'/#organization'},'areaServed':'Kigali, Rwanda'})
 source=(ROOT/'_templates/custom-tailoring-page.html').read_text()
 values={'title':escape(title,quote=False),'title_attr':escape(title,quote=True),'description':escape(description,quote=True),'route':route,'content':'<div class="home-shell release-main">'+content+'</div>','header':component('header',route),'footer':component('footer')+'<script src="/assets/request-context.js" defer></script>','schema':json.dumps({'@context':'https://schema.org','@graph':graph},ensure_ascii=False).replace('<','\\u003c'),'styles':shared.site_css()+'\n'+(ROOT/'_templates/homepage-phase1.css').read_text()+'\n'+ICON_CSS}
 for key,value in values.items():source=source.replace('{{'+key+'}}',value)
 source=source.replace('class="tailoring-page"','class="tailoring-page customer-site"').replace('/assets/custom-tailoring.js','/assets/customer-site.js').replace('</head>','<link rel="stylesheet" href="/assets/customer-site.css"></head>')
 assert not re.search(r'{{\w+}}',source)
 return source

def service_page(ident):
 s=service_map()[ident];body=intro(s['title'],s['intro'])
 details=''.join(section(title,text) for title,text in s['sections'])
 body+=section('Choose Your Service Experience','Standard Service and VIP Service describe your assistance experience. They are separate from a Standard/Special design order and from Standard/Express Priority.')+'<div class="release-cards">'
 for exp,title,text in [('standard','Standard Service','The normal service experience using established ordering and assistance arrangements.'),('vip','VIP Service','Personalised requirements are individually assessed and quoted. Requests may involve on-location, cross-service, Express or after-hours assistance, subject to feasibility and the agreed scope.')]:
  dest=BASE+'design-choice/' if ident=='custom-tailoring' else '/request/'
  body+='<article class="release-card"><h2>'+title+'</h2><p>'+text+'</p>'+link(dest+'?'+urlencode({'service':ident,'experience':exp}),'Choose '+title,'home-button home-button-gold').replace('<a ','<a data-experience-choice ',1)+'</article>'
 body+='</div>'+details+section('Before you proceed','Your selection starts an enquiry. Review the quotation and relevant conditions before acceptance and required payment. Availability, official confirmation and a separate production-start notice follow the approved workflow.')+related()
 return frame(s['route'],s['title'],s['intro'],body,service=s)

def overview():
 body=intro('Our Four Services','Choose the service that matches your garment or assistance needs, then choose Standard or individually assessed VIP assistance.')+'<div class="release-cards">'
 for s in data()['services']:body+='<article class="release-card"><h2>'+escape(s['title'])+'</h2><p>'+escape(s['intro'])+'</p>'+link(s['route'],'Explore Service','home-button home-button-gold')+'</article>'
 return frame('/services/','Tailoring & Garment Services','Explore the four official Mr Sewing Fashion tailoring, alterations, garment-care and mobile/styling services in Kigali.',body+'</div>'+related())

def design_choice():
 body=intro('Choose Your Design Order Type','First choose your service experience, then choose where your design comes from. These are separate decisions.')+'<p class="context-line" data-context-line></p><div class="release-cards">'
 for order,title,text,path in [('standard','Standard Order','Choose a design displayed on our website, then explore Men’s Suits or Women’s Suits.',BASE+'standard-order/'),('special','Special Order','Provide your own pictures, sketches or ideas for assessment. You do not need to browse a gallery first.',BASE+'special-order/')]:body+='<article class="release-card"><h2>'+title+'</h2><p>'+text+'</p>'+link(path+'?'+urlencode({'service':'custom-tailoring','order':order,'experience':'standard'}),'Choose '+title,'home-button home-button-gold')+'</article>'
 body+='</div>'+link(BASE,'Back to Service Experience')+related()
 return frame(BASE+'design-choice/','Choose Standard or Special Order','Choose a website design or customer-provided design for a tailoring quotation, independently of your Standard or VIP service experience.',body)

def standard():
 body=intro('Choose Your Suit Category','Standard Order means selecting a website design. Your service experience and order priority remain separate choices.')+'<p class="context-line" data-context-line></p><div class="release-cards">'
 for title,src,route,alt in [("Men’s Suits",'/r7.jpeg','/mensuits/','Approved Mr Sewing light-grey jacket and navy-trouser tailoring photograph'),("Women’s Suits",'/h2.jpeg','/womensuits/','Approved Mr Sewing off-white graduation tailoring photograph')]:
  thumb='/assets/images/r7-480.webp' if 'r7' in src else '/assets/images/h2-480.webp'
  variants='/assets/images/r7-480.webp 480w, /assets/images/r7-960.webp 960w' if 'r7' in src else '/assets/images/h2-480.webp 480w, /h2.jpeg 750w'
  body+='<article class="release-card"><img src="'+thumb+'" srcset="'+variants+'" sizes="(min-width: 760px) 520px, calc(100vw - 40px)" width="'+('2048' if 'r7' in src else '750')+'" height="'+('2056' if 'r7' in src else '938')+'" alt="'+alt+'" loading="lazy" decoding="async"><h2>'+title+'</h2><p>Explore approved design references and request a quotation for your preferred style. No stock or exact fabric availability is implied.</p>'+link(route+'?service=custom-tailoring&order=standard&experience=standard','Explore '+title,'home-button home-button-gold')+'</article>'
 return frame(BASE+'standard-order/','Men’s & Women’s Suit Design Selection','Browse the two approved suit design categories and retain your service experience for a quotation request.',body+'</div>'+link(BASE+'design-choice/','Back to Design Order Type'))

def fields(kind):
 def input_(id,label,name=None,type='text',required=False,extra=''):
  return '<div><label for="'+id+'">'+label+(' <small>(required)</small>' if required else ' <small>(optional)</small>')+'</label><input id="'+id+'" name="'+(name or label)+'" type="'+type+'"'+(' required' if required else '')+' '+extra+'></div>'
 body='<div class="request-fields">'+input_('requestName','Full name','Full Name',required=True,extra='autocomplete="name" maxlength="160"')+input_('requestPhone','Phone / WhatsApp','Phone Number','tel',True,'autocomplete="tel" inputmode="tel" maxlength="40"')+input_('requestEmail','Email address','Email Address','email',extra='autocomplete="email" maxlength="254"')
 if kind=='quotation':body+=input_('requestLocation','Country or location','Location',required=True,extra='maxlength="160"')+input_('requestQuantity','Number of garments','Quantity','number',True,'min="1" step="1" value="1"')+input_('requestDate','Preferred date','Preferred Date','date',extra='aria-describedby="request-guidance"')+'<div data-custom-only><label for="requestFabric">Fabric preferences (optional)</label><input id="requestFabric" name="Fabric Preferences" maxlength="200"></div><div data-measurement><label for="requestMeasurements">Measurements</label><select id="requestMeasurements" name="Measurements"><option>Not sure yet</option><option>Have measurements</option><option>Need measurement guidance</option></select></div>'
 if kind=='refund':body+=input_('requestReference','Order or quotation reference','Order Reference',extra='maxlength="160"')
 return body+'</div><div><label for="requestMessage">'+('Describe the issue, relevant dates, remedy requested and any supporting information' if kind=='refund' else 'How Can We Help You?')+' <small>(required)</small></label><textarea id="requestMessage" name="Customer Message" rows="5" maxlength="4000" required></textarea></div>'

def request_form(kind='quotation',special=False):
 existing=(ROOT/'_templates/homepage-quotation.html').read_text();action=unescape(re.search(r'<form[^>]*action="([^"]+)"',existing)[1]);key=unescape(re.search(r'name="access_key" value="([^"]+)"',existing)[1]);assert action=='https://api.web3forms.com/submit'
 body='<section class="release-section" aria-labelledby="request-title"><h2 id="request-title">'+('Refund Request' if kind=='refund' else 'Tell Us About Your Design' if special else 'Your Request')+'</h2><p id="request-guidance">'+('Your request is for human review, not automatic refund approval. Describe available documentation; do not enter payment PINs, full card details or ID scans.' if kind=='refund' else 'This enquiry is for assessment and quotation. A preferred date is not confirmed, and measurements are not required to begin.')+'</p><noscript><p>JavaScript is required for selection review and confirmed submission. Please use the official contact details on the Contact page instead.</p></noscript><form id="customerRequestForm" data-kind="'+kind+'" data-special="'+str(special).lower()+'" action="'+escape(action,quote=True)+'" method="post"><input type="hidden" name="access_key" value="'+escape(key,quote=True)+'"><input type="hidden" name="subject" value="'+('Refund Review' if kind=='refund' else 'Customer Support' if kind=='support' else 'Quotation Request')+' - Mr Sewing Fashion"><input type="hidden" name="from_name" value="Mr Sewing Website"><div class="honey-field" aria-hidden="true"><label for="requestWebsite">Leave empty</label><input id="requestWebsite" name="botcheck" tabindex="-1" autocomplete="off"></div>'
 if kind!='refund':
  body+='<fieldset><legend>Review and edit your choices</legend><div class="request-fields"><div><label for="requestService">Service</label><select id="requestService" name="Service">'+''.join('<option value="'+s['id']+'">'+escape(s['title'])+'</option>' for s in data()['services'])+'</select></div>'
  if kind=='quotation':body+='<div><label for="requestExperience">Service Experience</label><select id="requestExperience" name="Service Experience"><option value="standard">Standard Service</option><option value="vip">VIP Service</option></select></div><div data-custom-only><label for="requestOrder">Design Order Type</label><select id="requestOrder" name="Design Order Type"><option value="standard">Standard Order — website design</option><option value="special">Special Order — your design</option></select></div><div><label for="requestPriority">Order Priority</label><select id="requestPriority" name="Order Priority"><option value="standard">Standard Priority</option><option value="express">Express Priority</option></select></div></div><div data-standard-design><label for="requestDesign">Selected design reference</label><input id="requestDesign" name="Design Reference" readonly><p>'+link(BASE+'standard-order/','Choose or change the design')+'</p></div><label class="request-check"><input type="checkbox" id="requestAfterHours" name="After-hours Request" value="Requested">Request after-hours availability (17:00–22:00 Kigali time)</label><p id="priority-guidance" class="request-note"></p>'
  else:body+='</div>'
  body+='</fieldset>'
 if kind=='quotation':body+='<aside data-upload-notice><p>Online file uploads are not enabled. Describe your design now and arrange reference sharing with the team through official WhatsApp or email. No files are attached by this form.</p><label for="requestFiles">Reference pictures or sketches — not enabled</label><input type="file" id="requestFiles" disabled accept="image/jpeg,image/png,image/webp" multiple></aside>'
 body+=fields(kind)+'<label class="request-check"><input id="requestConsent" name="Consent" type="checkbox" value="Read and requested review" required><span>I have read the '+link('/privacy-policy/','Privacy Policy','')+(' and '+link('/terms-and-conditions/','Terms & Conditions','') if kind=='quotation' else '')+'. I am requesting human review, not automatic acceptance.</span></label><button type="button" id="reviewRequest" class="home-button home-button-gold" disabled>Review Request</button></form><section id="requestReview" hidden aria-labelledby="review-title"><h2 id="review-title" tabindex="-1">Review Your Request</h2><dl id="reviewDetails"></dl><p>No order, appointment, payment or refund is confirmed by submitting.</p><div class="request-actions"><button id="editRequest" type="button" class="home-button">Edit Request</button><button id="sendRequest" type="submit" form="customerRequestForm" class="home-button home-button-gold">Submit '+('Refund Request' if kind=='refund' else 'for Quotation' if kind=='quotation' else 'Support Request')+'</button></div></section><p id="requestStatus" role="status" aria-live="polite"></p><section id="requestSuccess" hidden tabindex="-1" role="status"><h2>Request Submitted for Review</h2><p>The submission service accepted your request. This is not confirmation of an order, appointment, production start, payment or refund approval. Our team will review the details. No files were attached.</p></section></section>'
 # Only publication-authorised references may be included in an enquiry.
 from build_collections import load,design_name
 designs=load()[0]
 return body+'<script id="requestDesigns" type="application/json">'+json.dumps({d['id']:design_name(d) for d in designs},ensure_ascii=False).replace('<','\\u003c')+'</script>'

def request_page(special=False):
 route=BASE+'special-order/' if special else '/request/'
 body=intro('Tell Us About Your Design' if special else 'Request a Quotation','Share your requirements for feasibility assessment. Service experience, design order and priority are independent choices, all editable before submission.')+'<ol class="request-progress" aria-label="Request steps"><li>Service</li><li>Experience</li><li>Design or garment</li><li>Priority</li><li>Review</li></ol>'+request_form(special=special)+related()
 return frame(route,'Special Order Design Enquiry' if special else 'Review Your Service Quotation Request','Review service experience, design preferences and priority before sending an enquiry to Mr Sewing Fashion.',body)

def information(route):
 d=data()['pages'][route];body=intro(d['title'],d['intro'])
 if route in ['/terms-and-conditions/','/refund-policy/','/privacy-policy/']:body+='<p class="release-notice">Staging review: unresolved legal, financial or processing details are identified below; this is not a claim of legal compliance.</p>'
 old=json.loads((ROOT/'_data/policy-pages.json').read_text()).get(route.strip('/'),{});oldids=[s['id'] for s in old.get('sections',[])]+list(old.get('legacyAnchors',{}))
 used=set();nav=[]
 for i,s in enumerate(d['sections']):
  ident='locations-heading' if route=='/contact/' and s['title']=='Location' else 'hours-heading' if route=='/contact/' and s['title']=='Hours' else s['id'];used.add(ident);nav.append((ident,s['title']))
 body+='<nav class="release-toc" aria-label="On this page">'+''.join(link(route+'#'+a,t) for a,t in nav)+'</nav>'
 targets={
 '/terms-and-conditions/':{'about':1,'orders':3,'services':8,'pricing':2,'bookings':2,'timelines':6,'design':5,'responsibilities':5,'delivery':8,'returns':10,'photos':12,'contact':7},
 '/refund-policy/':{'scope':1,'before':5,'after':5,'deposit':5,'changes':5,'fit':3,'ours':2,'visits':2,'collection':2,'review':2,'contact':2},
 '/privacy-policy/':{'who':1,'collect':2,'how':3,'why':6,'share':3,'photos':4,'website':5,'rights':7,'contact':7}}.get(route,{})
 for alias,dest in old.get('legacyAnchors',{}).items():targets[alias]=targets.get(dest,1)
 for s,(ident,_) in zip(d['sections'],nav):
  anchors=''.join('<span class="legacy-anchor" id="'+escape(a,quote=True)+'" aria-hidden="true"></span>' for a in dict.fromkeys(oldids) if a not in used and str(targets.get(a,1))==s['id'])
  body+=anchors+section(s['title'],s['paragraphs'],ident)
 if route=='/refund-policy/':body+=request_form('refund')
 if route=='/customer-support/':body+=request_form('support')
 if route=='/contact/' or route=='/customer-support/':body+='<section class="release-section"><h2>Official Contacts</h2>'+link('tel:+250787411501','+250 787 411 501')+link('mailto:mrsewingfashiondesigner@gmail.com','mrsewingfashiondesigner@gmail.com')+link('https://wa.me/250787411501','WhatsApp Mr Sewing')+'</section>'
 if route=='/about/':body+='<div class="release-logo"><img src="/assets/images/mr-logo-480.webp" width="1244" height="802" alt="Official Mr Sewing Fashion logo" decoding="async"></div>'
 return frame(route,d['title'],d['intro'],body+related())

def process_page(route):
 if route=='/our-process/':return frame(route,'How Your Order Works','Understand quotation, acceptance, payment, sourcing, confirmation, production and handover.',intro('How Your Order Works','From enquiry to an individually confirmed service.')+''.join(section(s['title'],s['paragraphs']) for s in data()['pages']['/customer-information/']['sections'])+related())
 return frame(route,'Made-to-Measure Tailoring','Plan your design, measurements, fittings and quotation with Mr Sewing Fashion.',intro('Made Around Your Measurements','Start with a design and preferences. Consultation and measurements are arranged where applicable; feasibility, fabric and the quotation are confirmed before production.')+related())

def extra_routes():return ['/guides/fabrics/','/customer-information/','/delivery-and-collection/','/benefits/','/customer-support/','/request/',BASE+'design-choice/']
def outputs():
 out={ROOT/r.strip('/')/'index.html':information(r) for r in extra_routes() if r in data()['pages']}
 # Legacy references are retained without unverified imagery.
 for slug in ['m-classicsuits','m-doublebreasted','m-modernsuits','w-classicsuits','w-doublebreasted','w-modernsuits','reviews','happy-customers','suits']:
  route='/'+slug+'/'
  content=intro('Continue to Our Approved Designs','This earlier gallery is held while publication permission and reference details are verified. Browse the approved references or completed projects.')+'<nav class="release-related" aria-label="Approved galleries">'+link('/mensuits/','Men’s Suits')+link('/womensuits/','Women’s Suits')+link('/our-work/','Completed Mr Sewing Projects')+'</nav>'
  out[ROOT/(slug+'.html')]=frame(route,'Earlier Design Gallery','Browse approved references and evidenced Mr Sewing project photographs.',content).replace('<main ', '<main data-publication-hold ',1)
 out[ROOT/'why-choose.html']=frame('/why-choose/','Why Choose Mr Sewing','Personal attention, careful planning and clear communication for your garment needs.',intro('Why Choose Mr Sewing','Personal tailoring and garment assistance, planned around your requirements.')+section('Thoughtful details','Discuss your design, fit and finishing preferences with the team. Assessment, measurements and fittings help refine the agreed result.')+section('Clear arrangements','Your quotation identifies the scope, requirements and confirmed arrangements. Enquiries, official order confirmation and the separate production-start notice are distinct steps.')+section('Professional communication','Ask for clarification and confirmed updates. Customer Support operates Monday–Friday 09:00–17:00 Kigali time excluding Rwandan public holidays; the first-response target is within 24 support working hours.')+related())
 out[ROOT/'request/index.html']=request_page();out[ROOT/(BASE+'design-choice/').strip('/')/'index.html']=design_choice()
 out[ROOT/'assets/customer-site.css']=(ROOT/'_templates/customer-site.css').read_text()
 import shared_components as shared
 out[ROOT/'assets/customer-site.js']=shared.menu_script()+'\n'+(ROOT/'_templates/customer-site.js').read_text()
 out[ROOT/'assets/request-context.js']=(ROOT/'_templates/request-context.js').read_text()
 return out
