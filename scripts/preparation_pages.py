"""Unfinished Shop and program destinations; no catalogue, checkout or benefits."""
from html import escape
from site_seo import ROOT
from build_journey import page

PAGES={
 '/shop/collections/':('Shop Collections — Coming Soon','Mr Sewing shop collections are being prepared. Browse the existing tailoring inspiration while future shop information is developed.','Shop collections.','This section is being prepared. Collections and product information will be added after they are confirmed.'),
 '/shop/ordering/':('Shop Ordering — Coming Soon','Mr Sewing online ordering information is being prepared. Current tailoring enquiries remain available through the existing contact page.','Shopping with Mr Sewing.','Online ordering information will be added here when it is ready. No shop ordering process or launch date has been announced.'),
 '/loyalty-program/':('Loyalty Program — Coming Soon','The Mr Sewing loyalty program is being developed. Its details and conditions will be announced when ready.','Loyalty Program','We’re developing a loyalty program for Mr Sewing customers. Details and conditions will be announced when it is ready.'),
 '/referral-program/':('Referral Program — Coming Soon','The Mr Sewing referral program is being developed. Its details and conditions will be announced when ready.','Referral Program','We’re developing a referral program for people who introduce others to Mr Sewing. Details and conditions will be announced when it is ready.')
}

def cards(items,label='Explore this section'):
    return '<nav class="preparation-grid" aria-label="'+escape(label,quote=True)+'">'+''.join('<a class="preparation-card" href="'+url+'"><h2>'+escape(title)+'</h2><p>'+escape(text)+'</p><span>View page <span aria-hidden="true">↗</span></span></a>' for url,title,text in items)+'</nav>'

def shop_cards():
    return cards([('/shop/collections/','Collections — Coming Soon','A space for future shop collections and product information.'),('/shop/ordering/','Ordering — Coming Soon','A space for future online shopping information.')],'Shop sections')

def care_cards():
    return cards([('/services/garment-care/services/','Care options','Find guidance on discussing garment suitability and available care options.'),('/services/garment-care/planning/','Quotes & planning','Confirm pricing, timing and handover arrangements for your garment.')],'Garment Care pages')

def outputs():
    out={}
    for route,(title,description,heading,text) in PAGES.items():
        content='<nav class="journey-back" aria-label="Breadcrumb"><a href="/">Home</a> / '+('<a href="/shop/">Shop</a> / ' if route.startswith('/shop/') else '')+'<span>'+escape(heading)+'</span></nav><section class="preparation-intro"><span class="preparation-status">Coming Soon</span><h1>'+escape(heading)+'</h1><p>'+escape(text)+'</p></section>'
        if route.startswith('/shop/'):
            content+='<section class="preparation-panel"><h2>A space for what comes next.</h2><p>The shop is still being prepared. Product availability, prices and shopping details will be added when confirmed.</p></section>'+shop_cards()
            links=[('/shop/','Shop home'),('/collections/','Current tailoring inspiration'),('/contact/','Contact Mr Sewing')]
        else:
            content+='<section class="preparation-panel"><h2>Details will follow.</h2><p>This program is still being developed. Its benefits, eligibility and conditions have not been announced.</p></section>'
            links=[('/#programs','Homepage previews'),('/loyalty-program/' if route.startswith('/referral') else '/referral-program/','Loyalty Program preview' if route.startswith('/referral') else 'Referral Program preview')]
        content+='<nav class="help-related" aria-label="Related pages">'+''.join('<a href="'+url+'">'+escape(label)+'</a>' for url,label in links)+'</nav>'
        source=page(route,title+' | Mr Sewing',description,content)
        source=source.replace('</style>','\n'+(ROOT/'_templates/completion.css').read_text()+'\n'+(ROOT/'_templates/preparation.css').read_text()+'</style>',1)
        out[ROOT/route.strip('/')/'index.html']=source
    return out

def routes():return list(PAGES)
