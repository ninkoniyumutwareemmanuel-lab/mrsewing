"""Sanitised customer release driven by the owner's explicit 5 November decisions.
Internal source registers/reconciliations live outside the deployment root.
"""
from pathlib import Path
from html import escape,unescape
import json,re
import customer_guides as guides
from customer_navigation import breadcrumb
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
 return ''
def hero(ident):
 s=service_map()[ident]
 image=json.loads((ROOT/'_data/service-hero-images.json').read_text())['images'][ident]
 assert (ROOT/image['src'].lstrip('/')).is_file(),image['src']
 photo='<img src="'+escape(image['src'],quote=True)+'" width="'+str(image['width'])+'" height="'+str(image['height'])+'" alt="'+escape(image['alt'],quote=True)+'" loading="eager" fetchpriority="high" decoding="async">'
 actions=[('/mensuits/','Explore Men’s Suits'),('/womensuits/','Explore Women’s Suits')] if ident=='custom-tailoring' else [('/request/'+ident+'/',{'alterations':'Request Alteration','garment-care':'Request Garment Care','mobile-fitting':'Request Mobile Service','vip':'Request VIP Service'}[ident])]
 return '<section class="service-hero" style="--hero-mobile-position:'+escape(image.get('mobilePosition','50% 50%'),quote=True)+'"><div class="service-hero-copy"><p class="service-breadcrumb" role="navigation" aria-label="Breadcrumb">'+link('/','Home','')+' / '+link('/services/','Services','')+'</p><p class="home-eyebrow">Our Service</p><h1>'+escape(s['title'])+'</h1><p>'+escape(s['intro'])+'</p><div class="service-hero-actions">'+''.join(link(u,t,'home-button home-button-gold') for u,t in actions)+'</div><ul class="service-features"><li><span aria-hidden="true">◇</span> Personal guidance</li><li><span aria-hidden="true">✂</span> Individually assessed</li><li><span aria-hidden="true">✓</span> Agreed quotation</li></ul></div><div class="service-hero-photo">'+photo+'</div></section>'
def frame(route,title,description,content,kind='WebPage',service=None):
 from custom_tailoring import component
 import shared_components as shared
 from homepage_resources import CSS as ICON_CSS
 seo=json.loads((ROOT/'_data/page-seo.json').read_text()).get(route.strip('/')+'.html')
 if seo:title,description=seo['title'],seo['description']
 else:title=title+' | Mr Sewing Fashion, Kigali'
 if 'aria-label="Breadcrumb"' not in content and 'service-hero' not in content:content=breadcrumb([('Home','/'),(title.split(' | ')[0],None)])+content
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
 s=service_map()[ident];body=hero(ident)
 for title,text in s['sections']:
  if ident=='custom-tailoring':text=text.replace('Choose Standard Service or individually assessed VIP Service before choosing a website design (Standard Order) or your own inspiration (Special Order).','Browse Men’s or Women’s Suits, or use the Special Order alternative to describe your own inspiration.')
  body+=section(title,text)
 if ident=='custom-tailoring':
  body+=section('How Long Does Custom Tailoring Take?','The time required to complete your garment depends on the selected design, fabric availability, measurements, fitting requirements and production schedule. Standard and Express requests are assessed according to the work involved and available capacity. We will confirm the applicable completion timeframe before your order is accepted.')
 else:
  if ident=='vip':body+=section('VIP Subscription','The combined VIP Garment Care & Alterations Membership is being developed. It is not available to purchase. Details are subject to further review.')+link('/services/vip/subscription/','VIP Subscription','home-text-link')
  body+='<p class="service-request-action">'+link('/request/'+ident+'/','Request Service','home-button home-button-gold')+'</p>'
 return frame(s['route'],s['title'],s['intro'],body,service=s)

def overview():
 body=intro('Our Services','Explore four ordinary service categories and the dedicated VIP Services entry point.')+'<div class="release-cards">'
 for s in data()['services']:body+='<article class="release-card"><h2>'+escape(s['title'])+'</h2><p>'+escape(s['intro'])+'</p>'+link(s['route'],'Explore Service','home-button home-button-gold')+'</article>'
 return frame('/services/','Tailoring & Garment Services','Explore Mr Sewing Fashion tailoring, alterations, garment care, mobile assistance and personalised VIP enquiries in Kigali.',body+'</div>')

def design_choice():return standard().replace(DOMAIN+BASE+'standard-order/',DOMAIN+BASE+'design-choice/')

def standard():
 body=breadcrumb([('Home','/'),('Custom Tailoring & Suits',BASE),('Suit Categories',None)])+intro('Choose Your Suit Category','Explore approved website designs, or share your own inspiration using the Special Order alternative within either gallery.')+'<div class="release-cards">'
 for title,src,route,alt in [("Men’s Suits",'/r7.jpeg','/mensuits/','Approved Mr Sewing light-grey jacket and navy-trouser tailoring photograph'),("Women’s Suits",'/h2.jpeg','/womensuits/','Approved Mr Sewing off-white graduation tailoring photograph')]:
  body+='<article class="release-card"><img src="'+src+'" width="'+('2048' if 'r7' in src else '750')+'" height="'+('2056' if 'r7' in src else '938')+'" alt="'+alt+'" loading="lazy" decoding="async"><h2>'+title+'</h2>'+link(route,'Explore '+title,'home-button home-button-gold')+'</article>'
 return frame(BASE+'standard-order/','Men’s & Women’s Suit Design Selection','Browse the two approved suit design categories.',body+'</div>')

def fabric_page():
 body=intro('Choose Your Fabric','Choose your fabric or ask for help. Availability and your final quotation will be confirmed with you.')+'<p data-design-line></p><form id="fabricChoiceForm"><fieldset><legend>Fabric Selection or Assistance</legend><label class="fabric-choice"><input type="radio" name="fabricChoice" value="now" required> I would like to choose my fabric.</label><label class="fabric-choice"><input type="radio" name="fabricChoice" value="advice" required> I would like help choosing my fabric.</label><p>Advice is available without choosing a fabric. All fabric references, availability and the final quotation require business confirmation.</p></fieldset><section id="fabricSelection" hidden aria-labelledby="fabric-selection-title"><h2 id="fabric-selection-title">Choose Fabric</h2><p class="guide-notice">Illustrative fabric references. Confirm material, available colours and quotation with our team.</p><label for="fabricCategory">Suit category</label><select id="fabricCategory"><option value="men">Men’s Suits</option><option value="women">Women’s Suits</option></select>'
 for category in ['men','women']:body+='<fieldset data-fabric-category="'+category+'"><legend>'+('Men’s' if category=='men' else 'Women’s')+' suit fabrics</legend>'+guides.cards(category,True)+'</fieldset>'
 body+='</section><div class="request-actions">'+link('/mensuits/','Back','home-button fabric-back')+'<button type="submit" class="home-button home-button-gold">Continue</button></div></form>'
 from build_collections import load,design_route
 from portfolio_requests import model as portfolio_model
 body+='<script id="portfolioRequestData" type="application/json">'+json.dumps(portfolio_model(),ensure_ascii=False).replace('<','\\u003c')+'</script>'
 body+='<script id="fabricDesignRoutes" type="application/json">'+json.dumps({d['id']:design_route(d) for d in load()[0]}).replace('<','\\u003c')+'</script>'+guides.script()
 return frame(BASE+'fabric/','Choose Fabric or Request Advice','Choose an illustrative fabric reference or request advice before your suit quotation enquiry.',body)

def subscription():
 return frame('/services/vip/subscription/','VIP Subscription — In Development','Information about the planned combined garment-care and alterations membership.',breadcrumb([('Home','/'),('VIP Services','/services/vip/'),('VIP Subscription',None)])+intro('VIP Subscription','Details are being finalised. This is not an available paid membership.')+section('VIP Garment Care & Alterations Membership','The planned combined membership concerns Clothing Alterations & Repairs and Garment Care & Cleaning. It does not cover subscriptions for Custom Tailoring or Mobile Tailoring. Allowances, visit definitions, pricing, coverage, billing, cancellation and refund conditions are not final. There is no checkout or subscription payment.'))

def fields(kind,service_id=None):
 if kind=='consultation':
  from consultation_form import fields as consultation_fields
  return consultation_fields()
 def input_(id,label,name=None,type='text',required=False,extra=''):
  return '<div><label for="'+id+'">'+label+(' <small>(required)</small>' if required else ' <small>(optional)</small>')+'</label><input id="'+id+'" name="'+(name or label)+'" type="'+type+'"'+(' required' if required else '')+' '+extra+'></div>'
 body='<div class="request-fields">'+input_('requestName','Full name','Full Name',required=True,extra='autocomplete="name" maxlength="160"')+input_('requestPhone','Phone / WhatsApp','Phone Number','tel',True,'autocomplete="tel" inputmode="tel" maxlength="40"')+input_('requestEmail','Email address','Email Address','email',extra='autocomplete="email" maxlength="254"')
 if kind=='quotation':body+=input_('requestLocation','Country or location','Location',required=True,extra='maxlength="160"')+input_('requestQuantity','Number of garments','Quantity','number',True,'min="1" step="1" value="1"')+input_('requestDate','Preferred date','Preferred Date','date',extra='aria-describedby="request-guidance"')+'<div data-custom-only><label for="requestFabric">Fabric preferences (optional)</label><input id="requestFabric" name="Fabric Preferences" maxlength="200"></div><div data-measurement><label for="requestMeasurements">Measurements</label><select id="requestMeasurements" name="Measurements"><option>Not sure yet</option><option>Have measurements</option><option>Need measurement guidance</option></select></div>'
 if kind=='consultation':body+=input_('requestDate','Preferred consultation date','Preferred Consultation Date','date')+input_('requestTime','Preferred consultation time (Kigali)','Preferred Consultation Time','time',extra='min="09:00" max="17:00"')+input_('requestAdditional','Additional information','Additional Information',extra='maxlength="1000"')
 if kind=='refund':body+=input_('requestReference','Order or quotation reference','Order Reference',extra='maxlength="160"')
 if kind=='quotation':
  body+=('<div><label for="requestGarment">Garment type (required)</label><select id="requestGarment" name="Garment Type" required><option value="">Select your garment</option><option>Men’s Suits</option><option>Women’s Suits</option><option value="other">Other Clothing — Specify Your Garment</option></select><div id="otherGarmentField" hidden><label for="requestOtherGarment">Describe your garment (required)</label><input id="requestOtherGarment" name="Other Garment" maxlength="160" disabled></div></div>' if service_id=='garment-care' else input_('requestGarment','Garment type or category','Garment Type',extra='maxlength="160"'))
  if service_id in ['garment-care','alterations']:body+=input_('requestCondition','Garment condition or work required','Garment Condition',extra='maxlength="300"')
  if service_id=='garment-care':body+='<div><label for="requestCollection">Collection or delivery preference (optional)</label><select id="requestCollection" name="Handover Preference"><option>Discuss arrangements</option><option>Request collection assessment</option><option>Request delivery assessment</option></select></div>'
  if service_id=='mobile-fitting':body+=input_('requestAssistance','Type of assistance','Assistance Type',required=True,extra='maxlength="180"')+input_('requestTime','Preferred time (Kigali)','Preferred Time','time')+input_('requestParticipants','Participants','Participants','number',extra='min="1" step="1"')+input_('requestEvent','Event details','Event Details',extra='maxlength="300"')
 return body+'</div><div><label for="requestMessage">'+('Describe the issue, relevant dates, remedy requested and any supporting information' if kind=='refund' else 'Consultation purpose' if kind=='consultation' else 'How Can We Help You?')+' <small>(required)</small></label><textarea id="requestMessage" name="Customer Message" rows="5" maxlength="4000" required></textarea></div>'

def request_form(kind='quotation',special=False,service_id=None):
 existing=(ROOT/'_templates/homepage-quotation.html').read_text();action=unescape(re.search(r'<form[^>]*action="([^"]+)"',existing)[1]);key=unescape(re.search(r'name="access_key" value="([^"]+)"',existing)[1]);assert action=='https://api.web3forms.com/submit'
 body='<section class="release-section" aria-labelledby="request-title"><h2 id="request-title">'+('Refund Request' if kind=='refund' else 'Tell Us About Your Design' if special else 'Your Request')+'</h2><p id="request-guidance">'+('Your request is for human review, not automatic refund approval. Describe available documentation; do not enter payment PINs, full card details or ID scans.' if kind=='refund' else 'Your consultation preferences require review. Submission does not confirm an appointment, service, order or quotation.' if kind=='consultation' else 'This enquiry is for assessment and quotation. A preferred date is not confirmed, and measurements are not required to begin.')+'</p><noscript><p>JavaScript is required for selection review and confirmed submission. Please use the official contact details on the Contact page instead.</p></noscript><form id="customerRequestForm" data-kind="'+kind+'" data-special="'+str(special).lower()+'" data-service="'+(service_id or '')+'" action="'+escape(action,quote=True)+'" method="post"><input type="hidden" name="access_key" value="'+escape(key,quote=True)+'"><input type="hidden" name="subject" value="'+('Refund Review' if kind=='refund' else 'Customer Support' if kind=='support' else 'Consultation Request' if kind=='consultation' else 'Quotation Request')+' - Mr Sewing Fashion"><input type="hidden" name="from_name" value="Mr Sewing Website"><div class="honey-field" aria-hidden="true"><label for="requestWebsite">Leave empty</label><input id="requestWebsite" name="botcheck" tabindex="-1" autocomplete="off"></div>'
 if kind=='consultation':body+='<script src="/assets/consultation.js" defer></script>'
 if kind!='refund':
  body+='<fieldset><legend>'+('Service details' if kind=='quotation' else 'Consultation service' if kind=='consultation' else 'Support topic')+'</legend>'
  if kind in ['support','consultation']:body+='<label for="requestService">Service'+(' (required)' if kind=='consultation' else '')+'</label><select id="requestService" name="Service"'+(' required' if kind=='consultation' else '')+'>'+('<option value="">Select a service</option>' if kind=='consultation' else '')+''.join('<option value="'+s['id']+'">'+escape(s['title'])+'</option>' for s in data()['services'] if kind!='consultation' or s['id'] in ['custom-tailoring','alterations','garment-care'])+'</select>'
  else:
   body+='<input type="hidden" id="requestService" name="Service" value="'+(service_id or 'custom-tailoring')+'"><input type="hidden" id="requestExperience" name="Service Experience" value="'+('vip' if service_id=='vip' else 'standard')+'"><input type="hidden" id="requestOrder" name="Design Order Type" value="'+('special' if special else 'standard')+'"><p id="requestContextSummary"></p><p class="portfolio-context" id="portfolioRequestContext" hidden></p><input type="hidden" id="requestSuitCategory" name="Suit Category"><div data-standard-design><label for="requestDesign">Selected design record</label><input id="requestDesign" name="Design Reference" readonly><div id="selectedDesignPreview" hidden></div><label for="changeDesign">Change selected design</label><select id="changeDesign"><option value="">Choose another design</option></select></div><div data-custom-only><label for="requestFabricChoice">Fabric Selection or Assistance</label><select id="requestFabricChoice" name="Fabric Choice"><option value="advice">I would like help choosing my fabric.</option><option value="now">I would like to choose my fabric.</option></select><div id="requestFabricReferenceField"><label for="requestFabricSelection">Choose Fabric</label><select id="requestFabricSelection" name="Selected Fabric"><option value="">Select a fabric</option>'+guides.options()+'</select><p class="request-note">We will confirm the fabric, availability and final price with you.</p></div></div><p data-standard-design><a class="request-back" href="/services/custom-tailoring/fabric/">Edit Fabric Selection</a></p><label for="requestPriority">Production priority</label><select id="requestPriority" name="Order Priority"><option value="standard">Standard Priority</option><option value="express">Express Priority</option></select><label class="request-check"><input type="checkbox" id="requestAfterHours" name="After-hours Request" value="Requested">Request after-hours availability (17:00–22:00 Kigali time)</label><p id="priority-guidance" class="request-note"></p>'
   if special:body+='<div><label for="requestCategory">Garment category (optional)</label><select id="requestCategory" name="Originating Suit Category"><option value="">Not specified</option><option value="men">Men’s Suits</option><option value="women">Women’s Suits</option></select></div>'
  body+='</fieldset>'
 if special:body=body.replace('<p data-standard-design><a class="request-back" href="/services/custom-tailoring/fabric/">Edit Fabric Selection</a></p>','')
 if kind=='quotation':body+='<aside id="designPictureSharing" hidden><button type="button" id="shareDesignPictures" class="home-button home-button-gold">Send Your Design Pictures on WhatsApp</button><p>Attach your photographs in WhatsApp and press Send. Pictures are not sent automatically. You can submit the quotation details first.</p></aside>'
 body+=fields(kind,service_id)+'<label class="request-check"><input id="requestConsent" name="Consent" type="checkbox" value="Read and requested review" required><span>'+('I agree to the '+link('/terms-and-conditions/','Terms & Conditions','')+' and have read the '+link('/privacy-policy/','Privacy Policy','') if kind in ['quotation','consultation'] else 'I have read the '+link('/privacy-policy/','Privacy Policy',''))+'. I am requesting human review, not automatic acceptance.</span></label><button type="button" id="reviewRequest" class="home-button home-button-gold" disabled>Continue</button></form><section id="requestReview" hidden aria-labelledby="review-title"><h2 id="review-title" tabindex="-1">Review Your Request</h2><dl id="reviewDetails"></dl><p>No order, appointment, payment or refund is confirmed by submitting.</p><div class="request-actions"><button id="editRequest" type="button" class="home-button">Back</button><button id="sendRequest" type="submit" disabled form="customerRequestForm" class="home-button home-button-gold">Submit '+('Refund Request' if kind=='refund' else 'Quotation Request' if kind=='quotation' else 'Consultation Request' if kind=='consultation' else 'Support Request')+'</button></div></section><p id="requestStatus" role="status" aria-live="polite"></p><section id="requestSuccess" hidden tabindex="-1" role="status"><h2>Request Submitted for Review</h2><p>The submission service accepted your request. This is not confirmation of an order, appointment, production start, payment or refund approval. Our team will review the details.</p></section></section>'
 if kind=='consultation':body=body.replace('No order, appointment, payment or refund is confirmed by submitting.','No appointment, service, order or quotation is confirmed by submitting.').replace('The submission service accepted your request. This is not confirmation of an order, appointment, production start, payment or refund approval. Our team will review the details.','The submission service accepted your consultation request for review. This does not confirm an appointment, service, order or quotation. Our team will review your preferences.')
 # Only publication-authorised references may be included in an enquiry.
 from build_collections import load,design_name,design_route
 designs=load()[0]
 from suit_references import assignment,model as suit_model
 from portfolio_requests import model as portfolio_model
 body+='<script id="requestDesignMedia" type="application/json">'+json.dumps({d['id']:{'name':suit_model()['references'].get(d['id'],{}).get('label') or design_name(d),'image':d['images'][0]['src'],'route':design_route(d)} for d in designs},ensure_ascii=False).replace('<','\\u003c')+'</script>'
 body+='<script id="portfolioRequestData" type="application/json">'+json.dumps(portfolio_model(),ensure_ascii=False).replace('<','\\u003c')+'</script>'
 body+='<script id="requestSuitCategories" type="application/json">'+json.dumps({d['id']:{'id':assignment(d['id'])['id'],'gender':assignment(d['id'])['gender']} for d in designs if assignment(d['id'])}).replace('<','\\u003c')+'</script>'
 body+='<script id="requestBackendConfig" type="application/json">'+json.dumps(json.loads((ROOT/'_data/customer-request-backend.json').read_text())).replace('<','\\u003c')+'</script><script src="/assets/request-storage.js" defer></script><script src="/assets/customer-refinements.js" defer></script>'
 return body+'<script src="/assets/request-draft.js" defer></script><script id="requestDesigns" type="application/json">'+json.dumps({d['id']:suit_model()['references'].get(d['id'],{}).get('label') or design_name(d) for d in designs},ensure_ascii=False).replace('<','\\u003c')+'</script>'+guides.script()

def request_page(special=False):
 route=BASE+'special-order/' if special else '/request/'
 body=breadcrumb([('Home','/'),('Custom Tailoring & Suits',BASE),('Special Order' if special else 'Quotation Request',None)])+intro('Tell Us About Your Design' if special else 'Your Quotation Request','Describe your requirements for assessment. Review the details before submitting; an enquiry does not confirm a production order.')+'<ol class="request-progress" aria-label="Request steps"><li>Design & fabric preference</li><li>Priority</li><li>Customer details</li><li>Review</li></ol>'+request_form(special=special)
 return frame(route,'Special Order Design Enquiry' if special else 'Your Service Quotation Request','Review design, fabric preferences, priority and contact details before sending a quotation enquiry.',body)

def information(route):
 d=data()['pages'][route];body=breadcrumb([('Home','/'),(d['title'],None)])+intro(d['title'],d['intro'])
 if route=='/guides/fabrics/':body+=guides.fabric_guide()
 if route=='/measurements/':body+='<p>'+link('/measurement-submission/','Submit Your Measurements','home-button home-button-gold')+'</p>'+guides.measurements()
 old=json.loads((ROOT/'_data/policy-pages.json').read_text()).get(route.strip('/'),{});oldids=[s['id'] for s in old.get('sections',[])]+list(old.get('legacyAnchors',{}))
 used=set();nav=[]
 for i,s in enumerate(d['sections']):
  ident='locations-heading' if route=='/contact/' and s['title']=='Location' else 'hours-heading' if route=='/contact/' and s['title']=='Hours' else s['id'];used.add(ident);nav.append((ident,s['title']))
 # No repeated jump-navigation bar; section information and anchors stay intact.
 targets={
 '/terms-and-conditions/':{'about':1,'orders':3,'services':8,'pricing':2,'bookings':2,'timelines':6,'design':5,'responsibilities':5,'delivery':8,'returns':10,'photos':12,'contact':7},
 '/refund-policy/':{'scope':1,'before':5,'after':5,'deposit':5,'changes':5,'fit':3,'ours':2,'visits':2,'collection':2,'review':2,'contact':2},
 '/privacy-policy/':{'who':1,'collect':2,'how':3,'why':6,'share':3,'photos':4,'website':5,'rights':7,'contact':7}}.get(route,{})
 for alias,dest in old.get('legacyAnchors',{}).items():targets[alias]=targets.get(dest,1)
 for s,(ident,_) in zip(d['sections'],nav):
  if route=='/guides/fabrics/' and s['title']=='Reference pictures are not stock guarantees':continue
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

def extra_routes():return ['/services/vip/','/services/vip/subscription/',BASE+'fabric/','/guides/fabrics/','/customer-information/','/delivery-and-collection/','/benefits/','/customer-support/','/request/',BASE+'design-choice/']
def outputs():
 from whatsapp_consent import page as whatsapp_page
 out={ROOT/r.strip('/')/'index.html':information(r) for r in extra_routes() if r in data()['pages']}
 out[ROOT/'whatsapp/index.html']=whatsapp_page()
 from build_collections import load
 from suit_references import assignment,category_label,model
 from portfolio_requests import model as portfolio_model
 portfolio=portfolio_model()
 out[ROOT/'_data/portfolio-request-allowlist.json']=json.dumps(portfolio,ensure_ascii=False,indent=2)+'\n'
 out[ROOT/'_data/request-reference-allowlist.json']=json.dumps({d['id']:{'name':model()['references'].get(d['id'],{}).get('label',d['name']),'image':d['images'][0]['src'],**({'category':category_label(assignment(d['id'])),'audience':assignment(d['id'])['gender']} if assignment(d['id']) else {})} for d in load()[0]},ensure_ascii=False,indent=2)+'\n'
 refs=json.loads(out[ROOT/'_data/request-reference-allowlist.json'])
 out[ROOT/'scripts/edge/request-data.mjs']='/* Generated from publication-gated references; no customer data. */\nexport const references='+json.dumps(refs,ensure_ascii=False).replace('<','\\u003c')+';\nexport const portfolio='+json.dumps(portfolio,ensure_ascii=False).replace('<','\\u003c')+';\n'
 out[ROOT/'staff/customer-requests/index.html']=frame('/staff/customer-requests/','Customer Requests','Authorised staff review of privately submitted enquiries.',intro('Customer Requests','Authorised Mr Sewing Fashion staff only.')+'<p id="staffStatus" role="status">Loading secure request service…</p><div id="staffRequests"></div><script src="/assets/staff-requests.js" defer></script>')
 out[ROOT/'assets/staff-requests.js']=(ROOT/'_templates/staff-requests.js').read_text()
 out[ROOT/'assets/request-uploads.js']=(ROOT/'_templates/request-uploads.js').read_text()
 out[ROOT/'assets/customer-interactions.js']=(ROOT/'_templates/customer-interactions.js').read_text()
 out[ROOT/'assets/customer-interactions.css']=(ROOT/'_templates/customer-interactions.css').read_text()
 out[ROOT/'assets/consultation.js']=(ROOT/'_templates/consultation.js').read_text()
 out[ROOT/'assets/request-storage.js']=(ROOT/'_templates/request-storage.js').read_text()
 out[ROOT/'assets/customer-refinements.js']=(ROOT/'_templates/customer-refinements.js').read_text()
 out[ROOT/'assets/request-draft.js']=(ROOT/'_templates/request-draft.js').read_text()
 out[ROOT/'assets/whatsapp-consent.js']=(ROOT/'_templates/whatsapp-consent.js').read_text()
 # Legacy references are retained without unverified imagery.
 for slug in ['m-classicsuits','m-doublebreasted','m-modernsuits','w-classicsuits','w-doublebreasted','w-modernsuits','reviews','happy-customers','suits']:
  route='/'+slug+'/'
  content=intro('Continue to Our Approved Designs','This earlier gallery is held while publication permission and reference details are verified. Browse the approved references or completed projects.')+'<nav class="release-related" aria-label="Approved galleries">'+link('/mensuits/','Men’s Suits')+link('/womensuits/','Women’s Suits')+link('/our-work/','Completed Mr Sewing Projects')+'</nav>'
  out[ROOT/(slug+'.html')]=frame(route,'Earlier Design Gallery','Browse approved references and evidenced Mr Sewing project photographs.',content).replace('<main ', '<main data-publication-hold ',1)
 out[ROOT/'why-choose.html']=frame('/why-choose/','Why Choose Mr Sewing','Personal attention, careful planning and clear communication for your garment needs.',intro('Why Choose Mr Sewing','Personal tailoring and garment assistance, planned around your requirements.')+section('Thoughtful details','Discuss your design, fit and finishing preferences with the team. Assessment, measurements and fittings help refine the agreed result.')+section('Clear arrangements','Your quotation identifies the scope, requirements and confirmed arrangements. Enquiries, official order confirmation and the separate production-start notice are distinct steps.')+section('Professional communication','Ask for clarification and confirmed updates. Customer Support operates Monday–Friday 09:00–17:00 Kigali time excluding Rwandan public holidays; the first-response target is within 24 support working hours.')+related())
 out[ROOT/'services/vip/index.html']=service_page('vip');out[ROOT/'services/vip/subscription/index.html']=subscription();out[ROOT/(BASE+'fabric/').strip('/')/'index.html']=fabric_page()
 for ident in ['alterations','garment-care','mobile-fitting','vip']:
  service=service_map()[ident];route='/request/'+ident+'/'
  out[ROOT/route.strip('/')/'index.html']=frame(route,'Request '+service['title'],'Tell Mr Sewing Fashion about your '+service['title'].lower()+' requirements for assessment and quotation.',breadcrumb([('Home','/'),(service['title'],service['route']),('Request Service',None)])+intro('Request '+service['title'],'Review your details before submitting. A request does not confirm an order or appointment.')+request_form(service_id=ident))
 out[ROOT/'booking.html']=frame('/booking/','Book a Consultation','Request a consultation with Mr Sewing Fashion in Kigali.',breadcrumb([('Home','/'),('Contact Us','/contact/'),('Book Consultation',None)])+intro('Book a Consultation','Tell us what you would like to discuss. Normal consultation requests follow the approved business schedule shown for your selected date. Your preferred date and time are subject to confirmation; submitting does not book an appointment.')+request_form('consultation'))
 out[ROOT/'request/index.html']=request_page();out[ROOT/(BASE+'design-choice/').strip('/')/'index.html']=design_choice()
 out[ROOT/'assets/customer-site.css']=(ROOT/'_templates/customer-site.css').read_text()
 import shared_components as shared
 from suit_references import categories,category_label
 out[ROOT/'assets/customer-site.js']=shared.menu_script()+'\n'+(ROOT/'_templates/customer-site.js').read_text().replace('/* suit-category-labels */{}',json.dumps({c['id']:category_label(c) for c in categories()}))
 out[ROOT/'assets/request-context.js']=(ROOT/'_templates/request-context.js').read_text().replace('/* fabric-reference-ids */[]',json.dumps([f['id'] for f in guides.fabrics()])).replace('/* suit-category-ids */[]',json.dumps([c['id'] for c in categories()])).replace('/* portfolio-reference-ids */[]',json.dumps(list(portfolio)))
 return out
