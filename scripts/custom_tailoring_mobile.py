"""R37: Custom Tailoring presentation using shared approved tier prices and benefits."""
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

def content(service,hero,section,link):
    from customer_policies import facts,sections
    f=facts();body=hero('custom-tailoring').replace(escape(service['intro']),'Tailoring shaped around your style, with guidance on fabrics, measurements and fit.',1)
    body+='<section class="release-section tailoring-special-intro" aria-labelledby="special-tailoring-heading"><h2 id="special-tailoring-heading">Special Tailoring &amp; Custom Garments</h2><p>Need something beyond a standard suit? We tailor shirts, trousers, dresses, coats and other custom garments. Share your requirements or design idea, and our team will review your request and prepare a quotation.</p></section>'
    body+=pricing()+children()+payments()+disclosure('bulk','Bulk-order discount',[f['texts']['policyBulk']])
    body+='''<section class="release-section" id="service-info-timing"><h2>Tailoring Around Your Order</h2><div class="tailoring-service-grid"><article><h3>Standard Tailoring</h3><p>We agree your completion date after reviewing your order, design, fabric availability and production capacity.</p></article><article><h3>Express Service</h3><p>Priority tailoring is subject to availability, feasibility and an individually confirmed completion date.</p></article></div><details class="tailoring-disclosure"><summary>Turnaround estimates &amp; additional charges</summary><div class="tailoring-detail-content"><p>'''+escape(f['texts'][f['services']['custom-tailoring']['timingTextKey']])+'''</p><div id="service-info-charges"><p>'''+escape(f['texts']['policyCharges'])+'''</p></div></div></details></section>'''
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
