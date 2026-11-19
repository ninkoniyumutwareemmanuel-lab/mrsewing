"""Tailoring Services overview with scoped suit information and shared enquiries."""
import json
from html import escape
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def pricing():
    """Public tier/benefit comparison; internal selling schedules remain untouched."""
    from suit_pricing import rows,compact_benefits,cleaning_benefits,gift_benefits
    out='<section class="release-section" id="service-info-prices"><h2>Suit Quality Options &amp; Included Benefits</h2><p>Choose a Tier / Quality with guidance from our team. Your individual quotation considers the complete garment, fabric, design and order requirements.</p><div class="tailoring-price-grid">'
    for audience,label in [('men','Men’s'),('women','Women’s')]:
        out+='<table class="tailoring-price-table ordinary-benefit-table" data-audience="'+audience+'"><caption>'+label+' Suit Quality Options</caption><thead><tr><th scope="col">Tier / Quality</th><th scope="col">Included Benefits</th></tr></thead><tbody>'
        for r in rows(audience):
            out+='<tr><th scope="row">Tier '+str(r['tier'])+' / Quality '+str(r['tier'])+'</th><td>'+escape(compact_benefits(r['tier']))+'</td></tr>'
        out+='</tbody></table>'
    out+='</div><details class="tailoring-disclosure" id="suit-benefit-conditions"><summary>Cleaning benefits &amp; collection gifts</summary><div class="tailoring-detail-content"><p>'+escape(cleaning_benefits())+'</p><p>'+escape(gift_benefits())+'</p></div></details>'
    out+='<section id="tuxedo-prices"><h3>Tuxedos &amp; Special Garments</h3><p>Men’s tuxedos retain their separate approved package eligibility and accessories, confirmed in your quotation. Ordinary-suit gifts and follow-up cleaning must not be assumed to apply.</p><p><a href="/showroom/?style=tuxedos-formalwear">Explore tuxedo references</a> or <a href="/services/custom-tailoring/special-order/">request Special Tailoring</a>.</p></section>'
    return out+'</section>'

def children():
    from customer_policies import facts
    f=facts()['texts']
    return '<section class="release-section tailoring-family" id="service-info-children"><p class="home-eyebrow">Family tailoring</p><h2>Children’s Tailoring &amp; Family Benefits</h2><p>'+escape(f['policyChildren'])+'</p><p>'+escape(f['policyParentChild'])+'</p><p><a href="/faq/prices-packages-payments/#children-cost">Family discount and quotation information</a></p></section>'

def payments():
    from customer_policies import facts
    f=facts();p=f['payments']
    return '<section class="release-section" id="service-info-payments"><h2>Payment and Order Confirmation</h2><div class="tailoring-payment-grid"><article><h3><span class="tailoring-card-amount">'+str(p['domesticCustomAdvancePercent'])+'%</span>Advance Payment</h3><p>Required before production for applicable domestic custom garment orders after quotation acceptance.</p></article><article><h3><span class="tailoring-card-amount">'+str(p['domesticCustomBalancePercent'])+'%</span>Final Balance</h3><p>Payable when tailoring is complete and before final cleaning, delivery or release.</p></article></div><p>International custom orders follow their separate approved advance-payment arrangement. Payment must be received and verified; an enquiry or screenshot does not start production.</p><p><a href="/faq/prices-packages-payments/#domestic-deposit">Domestic payment conditions</a> · <a href="/faq/prices-packages-payments/#international-payment">International payments</a> · <a href="/faq/prices-packages-payments/#payment-verification">Payment verification</a></p></section>'

def disclosure(ident,title,paragraphs):
    return '<details class="tailoring-disclosure" id="service-info-'+ident+'"><summary>'+escape(title)+'</summary><div class="tailoring-detail-content">'+''.join('<p>'+escape(p)+'</p>' for p in paragraphs)+'</div></details>'

def service_categories(link):
    """An overview, not a merger of the services' eligibility or order rules."""
    cards = [
        ('suits', 'Suit Tailoring', 'Custom-made men’s and women’s suits, with guidance on fabric, measurements, construction and fittings. Share a reference design for assessment or explore the Showroom.', '/services/custom-tailoring/design-choice/', 'Choose a Suit Design Online'),
        ('special', 'Special Tailoring', 'Discuss shirts, trousers, dresses, coats, special-occasion garments or tuxedo requirements. We assess your design, feasibility and quotation; tuxedos retain their separate package conditions.', '/services/custom-tailoring/special-order/', 'Request Special Tailoring'),
        ('alterations', 'Alterations & Repairs', 'Adjustments, resizing, repairs and fitting improvements for clothing you already own. Visit the dedicated service page for garment assessment and its applicable conditions.', '/services/alterations/', 'Explore Alterations & Repairs'),
    ]
    body = '<section class="release-section tailoring-categories" aria-labelledby="tailoring-categories-title"><h2 id="tailoring-categories-title">Find the Right Tailoring Service</h2><div class="tailoring-category-grid">'
    for ident, title, text, destination, action in cards:
        body += '<article class="tailoring-category-card tailoring-category-'+ident+'">'
        if ident == 'suits':
            body += '<p class="home-eyebrow">Custom suits</p>'
        body += '<h3>'+escape(title)+'</h3><p>'+escape(text)+'</p>'+link(destination, action, 'home-button'+(' home-button-gold' if ident == 'suits' else ''))+'</article>'
    return body + '</div></section>'

def content(service,hero,section,link):
    from customer_policies import facts,sections
    from tailoring_positioning import whatsapp_action
    f=facts();body=hero('custom-tailoring')
    body=body.replace('<div class="service-hero-actions">','<div class="service-hero-actions">'+whatsapp_action(context='tailoring-services',css='home-button home-button-gold'),1)
    body=body.replace('</div><ul class="service-features">','</div><p class="tailoring-design-note">Attach your photograph in WhatsApp. We’ll assess the design and discuss fabric, measurements and your quotation.</p><ul class="service-features">',1)
    body+=service_categories(link)
    body+='<section class="release-section tailoring-fabric-intro" id="suit-tailoring" aria-labelledby="tailoring-fabric-title"><p class="home-eyebrow">Suit Tailoring</p><h2 id="tailoring-fabric-title">Choose Your Design. We’ll Help With the Fabric and Tailoring.</h2><p>Explore men’s and women’s suit references or share your own design for assessment. Discuss fabric options supplied by Mr Sewing, request help choosing, or bring your own fabric under the applicable conditions. We confirm suitability, colours and availability before accepting the order.</p><p>For a website quotation, select your designs in the Showroom, choose one shared fabric preference, and tell us about measurements, fittings and your requested completion deadline.</p><p>'+link('/guides/fabrics/','Explore Fabric Options')+' · '+link('/faq/custom-tailoring/#own-fabric','Customer-supplied fabric information')+'</p></section>'
    body+=pricing()+children()+payments()+disclosure('bulk','Bulk-order discount',[f['texts']['policyBulk']])
    body+='''<section class="release-section" id="service-info-timing"><h2>Planning Your Tailoring Order</h2><div class="tailoring-service-grid"><article><h3>Standard Tailoring</h3><p>We agree your completion date after reviewing your order, design, fabric availability and production capacity.</p></article><article><h3>Express Service</h3><p>Priority tailoring is subject to availability, feasibility and an individually confirmed completion date.</p></article></div><details class="tailoring-disclosure"><summary>Turnaround estimates &amp; additional charges</summary><div class="tailoring-detail-content"><p>'''+escape(f['texts'][f['services']['custom-tailoring']['timingTextKey']])+'''</p><div id="service-info-charges"><p>'''+escape(f['texts']['policyCharges'])+'''</p></div></div></details></section>'''
    body+='<section class="release-section" id="tailoring-inclusions"><h2>Included with Your Standard Suit</h2><p>'+escape(f['texts']['policyAllSuitBenefits'])+'</p></section>'
    body+='<section class="release-section" id="tailoring-details"><h2>Helpful Order Information</h2>'
    body+=disclosure('fabric','Your design & customer-supplied fabric',[f['texts']['policyOwnFabric'],'Use the Showroom to explore approved references for men’s and women’s garments. Select one or more designs, then choose a shared fabric preference or request advice before your quotation. Special Tailoring remains available for other custom garments.'])
    body+=disclosure('measurements','Measurements, fittings & garment choices',['Measurements and fitting arrangements are reviewed with your design and garment requirements. We agree these arrangements and the quotation before production.',service['sections'][1][1],service['sections'][2][1]])
    body+=disclosure('transport','Collection & delivery arrangements',['Initial Kigali delivery is included with your standard suit package as shown above. Confirm the delivery address, timing and required payment before dispatch. Additional or outside-Kigali delivery and international shipping require the applicable agreed quotation; no universal price or transit time is promised.'])
    correction=next(row[2] for row in sections('custom-tailoring') if row[0]=='corrections')
    body+=disclosure('corrections','Fitting & workmanship concerns',[correction])+'</section>'
    body+='<nav class="tailoring-bottom-nav release-section" aria-labelledby="tailoring-next"><h2 id="tailoring-next">Find Your Next Design</h2><div>'+link('/showroom/?audience=men','Explore Men’s Tailoring','home-button home-button-gold')+link('/showroom/?audience=women','Explore Women’s Tailoring','home-button home-button-gold')+link('/services/custom-tailoring/special-order/','Special Tailoring','home-button home-button-gold')+'</div></nav>'
    return body

def decorate(source):
    from announcement_bar import decorate as with_offer
    styles=(ROOT/'_templates/custom-tailoring-mobile.css').read_text()+'\n'
    source=source.replace('</style>',styles+'</style>',1).replace('class="tailoring-page customer-site"','class="tailoring-page customer-site custom-tailoring-mobile"')
    return with_offer(source)
