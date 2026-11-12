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
 from customer_information import expand
 return '<section class="release-section"'+(' id="'+escape(id,quote=True)+'"' if id else '')+'><h2>'+escape(title)+'</h2>'+''.join('<p>'+escape(expand(p))+'</p>' for p in (paragraphs if isinstance(paragraphs,list) else [paragraphs]))+'</section>'
def related():
 return ''
def hero(ident):
 s=service_map()[ident]
 image=json.loads((ROOT/'_data/service-hero-images.json').read_text())['images'][ident]
 assert (ROOT/image['src'].lstrip('/')).is_file(),image['src']
 photo='<img src="'+escape(image['src'],quote=True)+'" width="'+str(image['width'])+'" height="'+str(image['height'])+'" alt="'+escape(image['alt'],quote=True)+'" loading="eager" fetchpriority="high" decoding="async">'
 actions=[('/mensuits/','Explore Men’s Suits'),('/womensuits/','Explore Women’s Suits')] if ident=='custom-tailoring' else [('/request/'+ident+'/',{'alterations':'Request Service','garment-care':'Request Service','mobile-fitting':'Request Service','vip':'Request VIP Service'}[ident])]
 if ident=='custom-tailoring':actions.append((BASE+'special-order/','Special Tailoring'))
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
 if route==BASE:source=__import__('custom_tailoring_mobile').decorate(source)
 return source

def service_page(ident):
 s=service_map()[ident]
 if ident=='custom-tailoring':
  body=__import__('custom_tailoring_mobile').content(s,hero,section,link)
  return frame(s['route'],s['title'],s['intro'],body,service=s)
 body=hero(ident)
 for title,text in s['sections']:
  if ident=='custom-tailoring':text=text.replace('Choose Standard Service or individually assessed VIP Service before choosing a website design (Standard Order) or your own inspiration (Special Order).','Browse Men’s or Women’s Suits, or use the Special Order alternative to describe your own inspiration.')
  body+=section(title,text)
 if ident=='custom-tailoring':
  pass

 else:
  if ident=='vip':body+=section('VIP Subscription','The combined VIP Garment Care & Alterations Membership is being developed. It is not available to purchase. Details are subject to further review.')+link('/request/vip-subscription/','VIP Subscription Enquiry','home-text-link')
  if ident=='vip':body+='<p class="service-request-action">'+link('/request/'+ident+'/','Request Service','home-button home-button-gold')+'</p>'
 body+=__import__('customer_policies').render(ident)
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
 body=intro('Choose Your Fabric','Choose your fabric or ask for help. Availability and your final quotation will be confirmed with you.')+'<p data-design-line></p><form id="fabricChoiceForm"><fieldset><legend>Fabric Selection or Assistance</legend><label class="fabric-choice"><input type="radio" name="fabricChoice" value="now" required> Choose Fabric</label><label class="fabric-choice"><input type="radio" name="fabricChoice" value="advice" required> Help Me Choose Fabric</label><label class="fabric-choice"><input type="radio" name="fabricChoice" value="own" required> I Have My Own Fabric</label><p>Customer-supplied fabric requires assessment for suitability. Advice is available without choosing a fabric. All fabric references, availability and the final quotation require business confirmation.</p></fieldset><section id="fabricSelection" hidden aria-labelledby="fabric-selection-title"><h2 id="fabric-selection-title">Choose Fabric</h2><p class="guide-notice">Illustrative fabric references. Confirm material, available colours and quotation with our team.</p><label for="fabricCategory">Suit category</label><select id="fabricCategory"><option value="men">Men’s Suits</option><option value="women">Women’s Suits</option></select>'
 for category in ['men','women']:body+='<fieldset data-fabric-category="'+category+'"><legend>'+('Men’s' if category=='men' else 'Women’s')+' suit fabrics</legend>'+guides.cards(category,True)+'</fieldset>'
 body+='</section><div class="request-actions">'+link('/mensuits/','Back','home-button fabric-back')+'<button type="submit" class="home-button home-button-gold">Continue</button></div></form>'
 from build_collections import load,design_route
 from portfolio_requests import model as portfolio_model
 body+='<script id="requestDesignMedia" type="application/json">'+json.dumps(__import__('selected_designs').design_media(),ensure_ascii=False).replace('<','\\u003c')+'</script><script src="/assets/selected-design.js" defer></script>'
 body+='<script id="portfolioRequestData" type="application/json">'+json.dumps(portfolio_model(),ensure_ascii=False).replace('<','\\u003c')+'</script>'
 body+='<script id="fabricDesignRoutes" type="application/json">'+json.dumps({d['id']:design_route(d) for d in load()[0]}).replace('<','\\u003c')+'</script>'+guides.script()
 return frame(BASE+'fabric/','Choose Fabric or Request Advice','Choose an illustrative fabric reference or request advice before your suit quotation enquiry.',body)

def subscription():
 return frame('/services/vip/subscription/','VIP Subscription Enquiries','Request an individually assessed quotation for garment-care and alterations subscription needs.',breadcrumb([('Home','/'),('VIP Services','/services/vip/'),('VIP Subscription',None)])+intro('VIP Subscription','Tell us about your garment care and alterations needs. Our team will assess your request and prepare a personalised quotation. No subscription, contract, price or payment is confirmed by an enquiry.')+'<p>'+link('/request/vip-subscription/','VIP Subscription Enquiry','home-button home-button-gold')+'</p>')

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
  if service_id=='vip':body+=input_('requestVIPAssistance','Requested VIP assistance','VIP Assistance',required=True,extra='maxlength="300"')+input_('requestOccasion','Occasion or purpose','Occasion or Purpose',extra='maxlength="300"')
  if service_id=='mobile-fitting':body+=input_('requestAssistance','Type of assistance','Assistance Type',required=True,extra='maxlength="180"')+input_('requestTime','Preferred time (Kigali)','Preferred Time','time')+input_('requestParticipants','Participants','Participants','number',extra='min="1" step="1"')+input_('requestEvent','Event details','Event Details',extra='maxlength="300"')
 return body+'</div><div><label for="requestMessage">'+('Describe the issue, relevant dates, remedy requested and any supporting information' if kind=='refund' else 'Consultation purpose' if kind=='consultation' else 'Describe the alteration or repair you need' if service_id=='alterations' else 'Describe the care or cleaning you need' if service_id=='garment-care' else 'Describe your VIP requirements' if service_id=='vip' else 'Describe your garment or design requirements' if kind=='quotation' else 'How Can We Help You?')+' <small>(required)</small></label><textarea id="requestMessage" name="Customer Message" rows="5" maxlength="4000" required></textarea></div>'

def request_form(kind='quotation',special=False,service_id=None):
 existing=(ROOT/'_templates/homepage-quotation.html').read_text();action=unescape(re.search(r'<form[^>]*action="([^"]+)"',existing)[1]);key=unescape(re.search(r'name="access_key" value="([^"]+)"',existing)[1]);assert action=='https://api.web3forms.com/submit'
 body='<section class="release-section" aria-labelledby="request-title"><h2 id="request-title">'+('Refund Request' if kind=='refund' else 'Tell Us About Your Design' if special else 'Your Request')+'</h2><p id="request-guidance">'+('Your request is for human review, not automatic refund approval. Describe available documentation; do not enter payment PINs, full card details or ID scans.' if kind=='refund' else 'Your consultation preferences require review. Submission does not confirm an appointment, service, order or quotation.' if kind=='consultation' else 'This enquiry is for assessment and quotation. A preferred date is not confirmed, and measurements are not required to begin.')+'</p><noscript><p>JavaScript is required for selection review and confirmed submission. Please use the official contact details on the Contact page instead.</p></noscript><form id="customerRequestForm" data-kind="'+kind+'" data-special="'+str(special).lower()+'" data-service="'+(service_id or '')+'" action="'+escape(action,quote=True)+'" method="post"><input type="hidden" name="access_key" value="'+escape(key,quote=True)+'"><input type="hidden" name="subject" value="'+('Refund Review' if kind=='refund' else 'Customer Support' if kind=='support' else 'Consultation Request' if kind=='consultation' else 'Quotation Request')+' - Mr Sewing Fashion"><input type="hidden" name="from_name" value="Mr Sewing Website"><div class="honey-field" aria-hidden="true"><label for="requestWebsite">Leave empty</label><input id="requestWebsite" name="botcheck" tabindex="-1" autocomplete="off"></div>'
 if kind=='consultation':body+='<script src="/assets/consultation.js" defer></script>'
 if kind!='refund':
  body+='<fieldset><legend>'+('Service details' if kind=='quotation' else 'Consultation service' if kind=='consultation' else 'Support topic')+'</legend>'
  if kind in ['support','consultation']:body+='<label for="requestService">Service'+(' (required)' if kind=='consultation' else '')+'</label><select id="requestService" name="Service"'+(' required' if kind=='consultation' else '')+'>'+('<option value="">Select a service</option>' if kind=='consultation' else '')+''.join('<option value="'+s['id']+'">'+escape(s['title'])+'</option>' for s in data()['services'] if kind!='consultation' or s['id'] in ['custom-tailoring','alterations','garment-care'])+'</select>'
  else:
   body+='<input type="hidden" id="requestService" name="Service" value="'+(service_id or 'custom-tailoring')+'"><input type="hidden" id="requestExperience" name="Service Experience" value="'+('vip' if service_id=='vip' else 'standard')+'"><input type="hidden" id="requestOrder" name="Design Order Type" value="'+('special' if special else 'standard')+'"><p id="requestContextSummary"></p><p class="portfolio-context" id="portfolioRequestContext" hidden></p><input type="hidden" id="requestSuitCategory" name="Suit Category"><div data-standard-design><label for="requestDesign">Selected design record</label><input id="requestDesign" name="Design Reference" readonly><div id="selectedDesignPreview" hidden></div><a data-edit-designs href="/services/custom-tailoring/">Add or Change Designs</a></div><div data-custom-only><label for="requestFabricChoice">Fabric Selection or Assistance</label><select id="requestFabricChoice" name="Fabric Choice"><option value="advice">I would like help choosing my fabric.</option><option value="now">Choose Fabric</option><option value="own">I Have My Own Fabric</option></select><div id="requestFabricReferenceField"><label for="requestFabricSelection">Choose Fabric</label><select id="requestFabricSelection" name="Selected Fabric"><option value="">Select a fabric</option>'+guides.options()+'</select><p class="request-note">We will confirm the fabric, availability and final price with you.</p></div></div><p data-standard-design><a class="request-back" href="/services/custom-tailoring/fabric/">Edit Fabric Selection</a></p><label for="requestPriority">Production priority</label><select id="requestPriority" name="Order Priority"><option value="standard">Standard Priority</option><option value="express">Express Priority</option></select><label class="request-check"><input type="checkbox" id="requestAfterHours" name="After-hours Request" value="Requested">Request after-hours availability (17:00–22:00 Kigali time)</label><p id="priority-guidance" class="request-note"></p>'
   if special:body+='<div><label for="requestCategory">Garment category (optional)</label><select id="requestCategory" name="Originating Suit Category"><option value="">Not specified</option><option value="men">Men’s Suits</option><option value="women">Women’s Suits</option></select></div>'
  body+='</fieldset>'
 if special:body=body.replace('<p data-standard-design><a class="request-back" href="/services/custom-tailoring/fabric/">Edit Fabric Selection</a></p>','')
 if kind=='quotation' and special:body+='<p>After reviewing your request, our team may contact you on WhatsApp to discuss your design and request reference pictures if needed. No photograph upload is required to submit.</p>'
 if kind=='quotation' and not special:body+='<aside id="designPictureSharing" hidden><button type="button" id="shareDesignPictures" class="home-button home-button-gold">Send Your Design Pictures on WhatsApp</button><p>Attach your photographs in WhatsApp and press Send. Pictures are not sent automatically. You can submit the quotation details first.</p></aside>'
 body+=fields(kind,service_id)+'<label class="request-check"><input id="requestConsent" name="Consent" type="checkbox" value="Read and requested review" required><span>'+('I agree to the '+link('/terms-and-conditions/','Terms & Conditions','')+' and have read the '+link('/privacy-policy/','Privacy Policy','') if kind in ['quotation','consultation'] else 'I have read the '+link('/privacy-policy/','Privacy Policy',''))+'. I am requesting human review, not automatic acceptance.</span></label><button type="button" id="reviewRequest" class="home-button home-button-gold" disabled>Continue</button></form><section id="requestReview" hidden aria-labelledby="review-title"><h2 id="review-title" tabindex="-1">Review Your Request</h2><dl id="reviewDetails"></dl><p>No order, appointment, payment or refund is confirmed by submitting.</p><div class="request-actions"><button id="editRequest" type="button" class="home-button">Back</button><button id="sendRequest" type="submit" disabled form="customerRequestForm" class="home-button home-button-gold">Submit '+('Refund Request' if kind=='refund' else 'Quotation Request' if kind=='quotation' else 'Consultation Request' if kind=='consultation' else 'Support Request')+'</button></div></section><p id="requestStatus" role="status" aria-live="polite"></p><section id="requestSuccess" hidden tabindex="-1" role="status"><h2>Request Submitted for Review</h2><p>The submission service accepted your request. This is not confirmation of an order, appointment, production start, payment or refund approval. Our team will review the details.</p></section></section>'
 if kind=='consultation':body=body.replace('No order, appointment, payment or refund is confirmed by submitting.','No appointment, service, order or quotation is confirmed by submitting.').replace('The submission service accepted your request. This is not confirmation of an order, appointment, production start, payment or refund approval. Our team will review the details.','The submission service accepted your consultation request for review. This does not confirm an appointment, service, order or quotation. Our team will review your preferences.')
 # Only publication-authorised references may be included in an enquiry.
 from build_collections import load,design_name,design_route
 designs=load()[0]
 from suit_references import assignment,model as suit_model
 from portfolio_requests import model as portfolio_model
 media=__import__('selected_designs').design_media();portfolio=portfolio_model()
 if kind!='quotation':
  media={id:{k:v[k] for k in ['name','image','route']} for id,v in media.items()}
  portfolio={id:{k:v[k] for k in ['name','designRef','route','image']+(['category','suitCategory'] if assignment(v['designRef']) else [])} for id,v in portfolio.items()}
 body+='<script id="requestDesignMedia" type="application/json">'+json.dumps(media,ensure_ascii=False).replace('<','\\u003c')+'</script>'+('<script src="/assets/selected-design.js" defer></script>' if kind=='quotation' else '')
 body+='<script id="portfolioRequestData" type="application/json">'+json.dumps(portfolio,ensure_ascii=False).replace('<','\\u003c')+'</script>'
 body+='<script id="requestSuitCategories" type="application/json">'+json.dumps({d['id']:{'id':assignment(d['id'])['id'],'gender':assignment(d['id'])['gender']} for d in designs if assignment(d['id'])}).replace('<','\\u003c')+'</script>'
 body+='<script id="requestBackendConfig" type="application/json">'+json.dumps(json.loads((ROOT/'_data/customer-request-backend.json').read_text())).replace('<','\\u003c')+'</script><script src="/assets/request-storage.js" defer></script><script src="/assets/customer-refinements.js" defer></script>'
 return body+'<script src="/assets/request-draft.js" defer></script><script id="requestDesigns" type="application/json">'+json.dumps({d['id']:suit_model()['references'].get(d['id'],{}).get('label') or design_name(d) for d in designs},ensure_ascii=False).replace('<','\\u003c')+'</script>'+guides.script()

def request_page(special=False):
 route=BASE+'special-order/' if special else '/request/'
 body=breadcrumb([('Home','/'),('Custom Tailoring & Suits',BASE),('Special Order' if special else 'Quotation Request',None)])+intro('Tell Us About Your Design' if special else 'Your Quotation Request','Describe your requirements for assessment. Review the details before submitting; an enquiry does not confirm a production order.')+'<ol class="request-progress" aria-label="Request steps"><li>Design & fabric preference</li><li>Priority</li><li>Customer details</li><li>Review</li></ol>'+request_form(special=special)
 return frame(route,'Special Order Design Enquiry' if special else 'Your Service Quotation Request','Review design, fabric preferences, priority and contact details before sending a quotation enquiry.',body)

def information(route):
 d=data()['pages'][route];body=breadcrumb([('Home','/'),(d['title'],None)])+intro(d['title'],d['intro'])
 if route=='/guides/fabrics/':
  body+='<p><a class="home-button home-button-gold" data-own-fabric href="/services/custom-tailoring/special-order/?fabricChoice=own">I Have My Own Fabric</a></p><p>Customer-supplied fabric is assessed for suitability before requirements and quotation are agreed.</p>'+guides.fabric_guide()
  from selected_designs import design_media
  from portfolio_requests import model as portfolio_model
  body+='<script id="requestDesignMedia" type="application/json">'+json.dumps(design_media()).replace('<','\\u003c')+'</script><script id="portfolioRequestData" type="application/json">'+json.dumps(portfolio_model()).replace('<','\\u003c')+'</script><script src="/assets/selected-design.js" defer></script>'
 if route=='/measurements/':body+=guides.measurements()
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
 if route=='/measurements/':body+='<p>'+link('/measurement-submission/','Submit Measurements','home-button home-button-gold')+'</p>'
 if route=='/refund-policy/':body+=request_form('refund')
 if route=='/customer-support/':body+=request_form('support')
 if route=='/contact/' or route=='/customer-support/':body+='<section class="release-section"><h2>Official Contacts</h2>'+link('tel:+250787411501','+250 787 411 501')+link('mailto:mrsewingfashiondesigner@gmail.com','mrsewingfashiondesigner@gmail.com')+link('https://wa.me/250787411501','WhatsApp Mr Sewing')+'</section>'
 if route=='/about/':body+='<div class="release-logo"><img src="/assets/images/mr-logo-480.webp" width="1244" height="802" alt="Official Mr Sewing Fashion logo" decoding="async"></div>'
 return frame(route,d['title'],d['intro'],body+related())

def process_page(route):
 if route=='/our-process/':return frame(route,'How Your Order Works','Understand quotation, acceptance, payment, sourcing, confirmation, production and handover.',intro('How Your Order Works','From enquiry to an individually confirmed service.')+''.join(section(s['title'],s['paragraphs']) for s in data()['pages']['/customer-information/']['sections'])+related())
 return frame(route,'Made-to-Measure Tailoring','Plan your design, measurements, fittings and quotation with Mr Sewing Fashion.',intro('Made Around Your Measurements','Start with a design and preferences. Consultation and measurements are arranged where applicable; feasibility, fabric and the quotation are confirmed before production.')+related())

def extra_routes():return ['/request/vip-subscription/','/media-kit/','/services/vip/','/services/vip/subscription/',BASE+'fabric/','/guides/fabrics/','/customer-information/','/delivery-and-collection/','/benefits/','/customer-support/','/request/',BASE+'design-choice/']
def outputs():
 from whatsapp_consent import page as whatsapp_page
 out={ROOT/r.strip('/')/'index.html':information(r) for r in extra_routes() if r in data()['pages']}
 out[ROOT/'whatsapp/index.html']=whatsapp_page()
 from build_collections import load,design_route
 from suit_references import assignment,category_label,model
 from portfolio_requests import model as portfolio_model
 portfolio=portfolio_model()
 out[ROOT/'_data/portfolio-request-allowlist.json']=json.dumps(portfolio,ensure_ascii=False,indent=2)+'\n'
 out[ROOT/'_data/request-reference-allowlist.json']=json.dumps({d['id']:{'name':model()['references'].get(d['id'],{}).get('label',d['name']),'image':d['images'][0]['src'],'route':design_route(d),'audience':d['gender'],'images':[{k:i[k] for k in ['src','alt','width','height']}|{'url':__import__('selected_designs').image_url(i['src'])} for i in d['images']],**({'category':category_label(assignment(d['id'])),'audience':assignment(d['id'])['gender']} if assignment(d['id']) else {})} for d in load()[0]},ensure_ascii=False,indent=2)+'\n'
 refs=json.loads(out[ROOT/'_data/request-reference-allowlist.json'])
 out[ROOT/'scripts/edge/request-data.mjs']='/* Generated from publication-gated references; no customer data. */\nexport const references='+json.dumps(refs,ensure_ascii=False).replace('<','\\u003c')+';\nexport const portfolio='+json.dumps(portfolio,ensure_ascii=False).replace('<','\\u003c')+';\nexport const fabrics='+json.dumps({f['id']:f for f in guides.fabrics()},ensure_ascii=False).replace('<','\\u003c')+';\n'
 out[ROOT/'staff/customer-requests/index.html']=frame('/staff/customer-requests/','Customer Requests','Authorised staff review of privately submitted enquiries.',intro('Customer Requests','Authorised Mr Sewing Fashion staff only.')+'<p id="staffStatus" role="status">Loading secure request service…</p><div id="staffRequests"></div><script src="/assets/staff-requests.js" defer></script>')
 out[ROOT/'assets/staff-requests.js']=(ROOT/'_templates/staff-requests.js').read_text()
 out[ROOT/'assets/request-uploads.js']=(ROOT/'_templates/request-uploads.js').read_text()
 out[ROOT/'assets/customer-interactions.js']=(ROOT/'_templates/customer-interactions.js').read_text()
 out[ROOT/'assets/customer-interactions.css']=(ROOT/'_templates/customer-interactions.css').read_text()
 out[ROOT/'assets/consultation.js']=(ROOT/'_templates/consultation.js').read_text()
 out[ROOT/'assets/request-storage.js']=(ROOT/'_templates/request-storage.js').read_text()
 out[ROOT/'assets/selected-design.js']=(ROOT/'_templates/selected-design.js').read_text()
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
 for ident in ['custom-tailoring','alterations','garment-care','mobile-fitting','vip']:
  service=service_map()[ident];route='/request/'+ident+'/'
  out[ROOT/route.strip('/')/'index.html']=frame(route,'Request '+service['title'],'Tell Mr Sewing Fashion about your '+service['title'].lower()+' requirements for assessment and quotation.',breadcrumb([('Home','/'),(service['title'],service['route']),('Request Service',None)])+intro('Request '+service['title'],'Review your details before submitting. A request does not confirm an order or appointment.')+request_form(special=ident=='custom-tailoring',service_id=ident))
 out[ROOT/'booking.html']=frame('/booking/','Book a Consultation','Request a consultation with Mr Sewing Fashion in Kigali.',breadcrumb([('Home','/'),('Contact Us','/contact/'),('Book Consultation',None)])+intro('Book a Consultation','Tell us what you would like to discuss. Normal consultation requests follow the approved business schedule shown for your selected date. Your preferred date and time are subject to confirmation; submitting does not book an appointment.')+request_form('consultation'))
 from v2_pages import subscription_page,media_page
 out[ROOT/'request/vip-subscription/index.html']=subscription_page();out[ROOT/'media-kit/index.html']=media_page()
 out[ROOT/'request/index.html']=request_page();out[ROOT/(BASE+'design-choice/').strip('/')/'index.html']=design_choice()
 config=json.loads((ROOT/'_data/public-api.json').read_text());assert config['backendOrigin']=='https://main.mrsewing-staging.pages.dev'
 out[ROOT/'assets/public-api.js']=(ROOT/'_templates/public-api.js').read_text().replace('/* public-api-config */{}',json.dumps(config))
 out[ROOT/'functions/_lib/public-api-config.js']='// Non-secret public intake routing.\nexport const config='+json.dumps(config)+';\n'
 out[ROOT/'assets/customer-site.css']=(ROOT/'_templates/customer-site.css').read_text()
 import shared_components as shared
 from suit_references import categories,category_label
 out[ROOT/'assets/customer-site.js']=shared.menu_script()+'\n'+(ROOT/'_templates/customer-site.js').read_text().replace('/* suit-category-labels */{}',json.dumps({c['id']:category_label(c) for c in categories()}))
 out[ROOT/'assets/design-selections.js']=(ROOT/'_templates/design-selections.js').read_text()
 out[ROOT/'assets/design-selections.css']=(ROOT/'_templates/design-selections.css').read_text()
 out[ROOT/'services/custom-tailoring/selected-designs/index.html']=frame('/services/custom-tailoring/selected-designs/','Selected Designs','Review your selected suit designs before fabric preferences and a quotation request.',breadcrumb([('Custom Tailoring & Suits',BASE),('Selected Designs',None)])+intro('Selected Designs','Keep browsing, adjust quantities or remove designs. Each selection is for assessment and quotation, not a purchase or confirmed order.')+'<div data-selection-list></div><p>'+link(BASE,'Browse More Designs')+'</p><a class="home-button home-button-gold" data-selected-continue href="/services/custom-tailoring/fabric/?multiple=1">Continue to Fabric Preferences</a>')
 out[ROOT/'assets/request-context.js']=(ROOT/'_templates/request-context.js').read_text().replace('/* public-browse-routes */[]',json.dumps(sorted(__import__('site_seo').INDEXABLE_ROUTES))).replace('/* fabric-reference-ids */[]',json.dumps([f['id'] for f in guides.fabrics()])).replace('/* suit-category-ids */[]',json.dumps([c['id'] for c in categories()])).replace('/* portfolio-reference-ids */[]',json.dumps(list(portfolio))).replace('/* selected-photo-urls */[]',json.dumps(sorted({i['url'] for d in refs.values() for i in d['images']}|{i['url'] for p in portfolio.values() for i in p['images']})))
 return out
