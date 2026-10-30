#!/usr/bin/env python3
"""Extend existing Journey builders with care information, process and Shop status."""
import argparse,json,re
from customer_information import expand as customer_text
from html import escape
from pathlib import Path
from site_seo import ROOT,DOMAIN,finalize
from build_journey import page,enquiry,services
from garment_care import catalog as care_catalog,care_information,care_navigation,care_summary
from preparation_pages import outputs as preparation_outputs,routes as preparation_routes,shop_cards

def intro(eyebrow,title,text):return '<section class="help-intro"><p class="home-eyebrow">'+escape(eyebrow)+'</p><h1>'+escape(title)+'</h1><p>'+escape(text)+'</p></section>'
def complete_page(route,title,description,content,kind='WebPage',extra=None):
    return page(route,title+' | Mr Sewing',description,content,kind,extra).replace('</style>','\n'+(ROOT/'_templates/completion.css').read_text()+'\n'+(ROOT/'_templates/preparation.css').read_text()+'</style>',1)
def related(links):return '<nav class="help-related" aria-label="Related information">'+''.join('<a href="'+url+'">'+escape(title)+'</a>' for url,title in links)+'</nav>'
def care_info_page(kind):
    info=care_information();route='/services/garment-care/'+kind+'/'
    if kind=='services':
        title='Garment Care Services';desc='Learn how to enquire about suitable clothing care with Mr Sewing Garment Care in Kigali, and confirm available treatments before proceeding.'
        content=intro(info['brand'],'Care starts with the garment.','Describe your clothing and its care label. We will confirm available options and suitability before a care service is agreed.')+'<section class="care-section"><h2>Available care options</h2><p>'+escape(info['servicesStatus'])+'</p>'
        approved=care_catalog()[1]
        if approved:content+='<div class="care-options">'+''.join('<a class="care-option" href="/services/garment-care/'+c['slug']+'/"><h3>'+escape(c['title'])+'</h3><p>'+escape(c['description'])+'</p></a>' for c in approved)+'</div>'
        content+='</section><section class="care-section"><h2>How to request care</h2><div class="care-details"><section><h3>Describe</h3><p>Send the garment type, care-label information and any condition concerns. Include photographs if useful.</p></section><section><h3>Discuss</h3><p>Confirm whether a suitable service is available. Do not assume a particular cleaning method or treatment is offered.</p></section><section><h3>Agree</h3><p>Confirm the quote, timing, conditions and handover arrangements before proceeding.</p></section></div></section>'+care_summary()
    else:
        title='Garment Care Quotes & Planning';desc='Understand the pricing, turnaround and handover status for Mr Sewing Garment Care in Kigali. Request confirmed arrangements for your garment.'
        content=intro(info['brand'],'Plan care with clarity.','Confirm the practical details before you hand over a garment. Prices, timing and collection arrangements must relate to the actual service agreed.')+care_summary()
        for ident,heading,text in [('prices','Prices in RWF',info['pricingStatus']),('turnaround','Turnaround times',info['turnaroundStatus']),('pickup-delivery','Pickup & delivery arrangements',info['arrangementsStatus'])]:content+='<section class="care-section" id="'+ident+'"><h2>'+heading+'</h2><p>'+escape(text)+'</p><p>Share your garment details and preferred date. Ask the team to confirm the applicable options and conditions before you agree.</p></section>'
    content+='<section class="care-section"><h2>Standalone care payments</h2><p>'+customer_text('{{standalonePayment}} {{balance}}')+'</p><p>The standard suit package includes one initial standard professional cleaning; separately requested care is quoted as its own service.</p></section>'
    content+='<section class="care-request"><h2>Ask about your garment.</h2><p>Opening WhatsApp starts a conversation; it does not confirm an order, service availability or an appointment.</p>'+enquiry(info['brand']+' — '+title,route)+'</section>'+related([('/services/garment-care/','Garment Care home')])
    out=complete_page(route,title+' — Mr Sewing Garment Care',desc,'<div class="home-shell care-info">'+care_navigation()+content+'</div>')
    return out.replace('class="journey-main home-shell"','class="care-main"').replace('</style>','\n'+(ROOT/'_templates/garment-care.css').read_text()+'</style>',1)

def information_page(kind):
    if kind=='shop':
        route='/shop/';title='Shop — Coming Soon';desc='Mr Sewing’s online shop is not available yet. Explore tailoring inspiration and services while online shopping is being prepared; no launch date is announced.'
        content=intro('Mr Sewing',title,'Online shopping is not available yet. Our website currently helps you explore designs, discover completed work and discuss tailoring services.')+'<section class="shop-status"><h2>A considered next chapter.</h2><p>There are no online products, checkout or payment facilities on this page, and no launch date has been announced. For current tailoring enquiries, explore the service you need and contact the team directly.</p></section>'+shop_cards()+related([('/collections/','Explore Collections'),('/services/','Find a tailoring service')])
    elif kind=='our-process':
        route='/our-process/';title='Our Tailoring Process';desc='Understand Mr Sewing’s tailoring process in Kigali: references, design and fabric choices, measurements, production planning, fittings and agreed handover.'
        content=intro('From idea to garment','A timeline, thoughtfully agreed.','Each garment starts with a conversation. Your design, available materials, measurements and fitting needs inform the plan; an enquiry is not a guaranteed completion date.')+'<div class="info-prose">'
        for h,t in [('1. Share your direction','Bring a reference, sketch or description and tell us your garment category and occasion. Share any event date so feasibility can be discussed.'),('2. Agree the details','Discuss available fabrics, design features, measurements and a quote. Confirm the order requirements and official terms before proceeding.'),('3. Plan production and fittings','The team agrees the appropriate production and fitting arrangements for your garment. Current capacity and any changes can affect scheduling; confirm a feasible timetable directly.'),('4. Confirm collection or delivery','Agree final fitting needs and handover arrangements with the team. Wait for readiness confirmation rather than treating an estimate as a ready notice.')]:content+='<section><h2>'+h+'</h2><p>'+t+'</p></section>'
        content+='</div>'+related([('/services/custom-tailoring/','Custom Tailoring'),('/services/express-tailoring/','Urgent tailoring enquiries')])
    else:
        route='/made-to-measure/';title='Measurements & Made-to-Measure Fittings';desc='Learn how measurements, fit preferences and fitting appointments relate to custom tailoring, workshop visits and mobile fitting with Mr Sewing in Kigali.'
        content=intro('Made to your measurements','The fit begins with you.','Measurements and fitting conversations help translate a design into a garment shaped around your requirements. This guide connects the practical steps without replacing an individual assessment.')+'<div class="info-prose">'
        for h,t in [('Prepare for measurements','Share your garment needs, design references and any existing measurements. If you are discussing an adjustment, have the relevant garment available.'),('Discuss the fit','Talk about your preferred silhouette and fit concerns. Measurements and a fitting review serve different purposes; agree the appointments needed for your garment.'),('Workshop or mobile fitting','Arrange a workshop appointment or request customer-location fitting support in Kigali. Mobile coverage, timing and any charges must be confirmed directly.'),('Connect the details','Design options, fabric selection and fitting arrangements belong to the same tailoring conversation. Confirm what is feasible before ordering.')]:content+='<section><h2>'+h+'</h2><p>'+t+'</p></section>'
        content+='</div>'+related([('/services/custom-tailoring/','Custom Tailoring'),('/services/mobile-fitting/','Mobile Fitting'),('/measurements/','Measurement guide')])
    if kind=='our-process':content+='<section class="info-prose"><h2>Payment, cleaning and handover</h2><p>'+customer_text('{{suitPayment}} {{balance}} {{package}}')+'</p><p>'+customer_text('{{timing}}')+'</p><p>'+customer_text('{{delivery}}')+'</p></section>'
    return complete_page(route,title,desc,content)

def outputs():
    out={}
    for kind in ['services','planning']:out[ROOT/'services/garment-care'/kind/'index.html']=care_info_page(kind)
    for kind in ['shop','our-process','made-to-measure']:out[ROOT/kind/'index.html']=information_page(kind)
    out.update(preparation_outputs())
    return out

def routes():return ['/services/garment-care/services/','/services/garment-care/planning/','/shop/','/our-process/','/made-to-measure/']+preparation_routes()
def main():
    p=argparse.ArgumentParser();p.add_argument('--check',action='store_true');a=p.parse_args()
    for path,source in outputs().items():
        value=finalize(source,path)
        if a.check:
            if not path.exists() or path.read_text()!=value:raise SystemExit('Stale completion output: '+str(path.relative_to(ROOT)))
        else:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(value)
    print('PASS: care/process/Shop information '+('synchronized.' if a.check else 'generated.'))
if __name__=='__main__':main()
