"""R37: Custom Tailoring presentation using shared approved tier prices and benefits."""
import json
from html import escape
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def pricing():
    from suit_pricing import rows,compact_benefits,cleaning_benefits,gift_benefits
    out='<section class="release-section" id="service-info-prices"><h2>Starting Suit Prices &amp; Benefits</h2><p>These are complete-garment starting prices by Tier / Quality, not fabric-only prices. Your final quotation depends on the confirmed tier, fabric, design and order requirements.</p><div class="tailoring-price-grid">'
    for audience,label in [('men','Men’s'),('women','Women’s')]:
        for pieces,key in [('Two-Piece','twoPieceRwf'),('Three-Piece','threePieceRwf')]:
            out+='<table class="tailoring-price-table ordinary-benefit-table" data-audience="'+audience+'" data-pieces="'+key+'"><caption>'+label+' '+pieces+' Suits</caption><thead><tr><th scope="col">Tier / Quality</th><th scope="col">Price <span>(RWF)</span></th><th scope="col">Included Benefits</th></tr></thead><tbody>'
            for r in rows(audience):
                out+='<tr><th scope="row">Tier '+str(r['tier'])+' / Quality '+str(r['tier'])+'</th><td>'+format(r[key],',')+'</td><td>'+escape(compact_benefits(r['tier']))+'</td></tr>'
            out+='</tbody></table>'
    out+='</div><details class="tailoring-disclosure" id="suit-benefit-conditions"><summary>Cleaning benefits &amp; collection gifts</summary><div class="tailoring-detail-content"><p>'+escape(cleaning_benefits())+'</p><p>'+escape(gift_benefits())+'</p><p>Initial standard professional cleaning, initial Kigali delivery, and a branded hanger and protective garment cover are included at every ordinary suit tier. No unlimited cleaning or gift entitlement is offered.</p></div></details>'
    tux=json.loads((ROOT/'_data/tuxedo-package-prices.json').read_text())['tiers']
    out+='<div id="tuxedo-prices"><table class="tailoring-price-table tuxedo-price-table"><caption>Men’s Tuxedos — Separate Schedule</caption><thead><tr><th scope="col">Tier / Quality</th><th scope="col">Two-piece <span>(RWF)</span></th><th scope="col">Three-piece <span>(RWF)</span></th></tr></thead><tbody>'
    for r in tux:out+='<tr><th scope="row">Tier '+str(r['tier'])+' / Quality '+str(r['tier'])+'</th><td>'+format(r['twoPieceRwf'],',')+'</td><td>'+format(r['threePieceRwf'],',')+'</td></tr>'
    return out+'</tbody></table><p class="tailoring-fabric-note">Tuxedos retain their separate approved package eligibility and accessories, confirmed in your quotation. Ordinary-suit gifts and follow-up cleaning must not be assumed to apply.</p></div></section>'

def children():
    return '''<section class="release-section tailoring-family" id="service-info-children"><p class="home-eyebrow">Family tailoring</p><h2>Children’s Suits: 50% Off</h2><p>Children under 12 automatically receive 50% off each eligible suit when the same order includes at least one adult suit at its normal price.</p><details class="tailoring-disclosure"><summary>Family discount conditions &amp; example</summary><div class="tailoring-detail-content"><ul class="tailoring-list"><li>Applies to children younger than 12, across all suit tiers and quality levels.</li><li>Each eligible child’s suit receives the discount; the adult suit stays at its normal applicable price.</li><li>Children’s normal starting prices follow the corresponding suit pricing schedule above. Without an adult suit, children’s suits are charged at the normal applicable price.</li><li>Customer discounts do not stack on the same suit; the highest eligible customer discount applies.</li></ul><aside class="tailoring-example" aria-labelledby="family-example"><h3 id="family-example">A simple family example</h3><p>One adult Tier 2 two-piece suit: <strong>400,000 RWF</strong>. Two eligible children’s Tier 2 two-piece suits: each reduced from 400,000 RWF to <strong>200,000 RWF</strong>.</p><p class="tailoring-total">Total: <strong>800,000 RWF</strong>, excluding separately quoted charges.</p></aside></div></details></section>'''

def payments():
    return '''<section class="release-section" id="service-info-payments"><h2>Payment and Order Confirmation</h2><div class="tailoring-payment-grid"><article><h3><span class="tailoring-card-amount">70%</span>Advance Payment</h3><p>Required before production, under the approved order process.</p></article><article><h3><span class="tailoring-card-amount">30%</span>Final Balance</h3><p>Payable before garment release, when tailoring is completed and before final cleaning and delivery.</p></article></div><details class="tailoring-disclosure"><summary>Payment verification for all customers &amp; international orders</summary><div class="tailoring-detail-content"><h3>International custom tailoring</h3><p>After feasibility confirmation and quotation acceptance, 100% advance payment is required before production. Shipping and applicable additional charges are quoted for your specific order; no universal shipping fee or guaranteed transit time is promised.</p><h3>All customer payments</h3><p>Workplace cash must be received, recorded and acknowledged. Bank transfers and Mobile Money require verification of actual receipt; screenshots alone do not prove cleared funds, and pending transactions are not completed payments.</p><p>After verification, customers receive payment confirmation and the next steps. Verification alone is not official production commencement. Necessary order requirements, the approved confirmation/start process and owner-authorised exceptions remain applicable. Use verified instructions and protect PINs and account credentials.</p></div></details></section>'''

def disclosure(ident,title,paragraphs):
    return '<details class="tailoring-disclosure" id="service-info-'+ident+'"><summary>'+escape(title)+'</summary><div class="tailoring-detail-content">'+''.join('<p>'+escape(p)+'</p>' for p in paragraphs)+'</div></details>'

def content(service,hero,section,link):
    from customer_policies import facts,sections
    f=facts();body=hero('custom-tailoring').replace(escape(service['intro']),'Tailoring shaped around your style, with guidance on fabrics, measurements and fit.',1)
    body+='<section class="release-section tailoring-special-intro" aria-labelledby="special-tailoring-heading"><h2 id="special-tailoring-heading">Special Tailoring &amp; Custom Garments</h2><p>Need something beyond a standard suit? We tailor shirts, trousers, dresses, coats and other custom garments. Share your requirements or design idea, and our team will review your request and prepare a quotation.</p></section>'
    body+=pricing()+children()+payments()+disclosure('bulk','Bulk-order discount',[f['texts']['policyBulk']])
    body+='''<section class="release-section" id="service-info-timing"><h2>Tailoring Around Your Order</h2><div class="tailoring-service-grid"><article><h3>Standard Tailoring</h3><p>We agree your completion date after reviewing your order, design, fabric availability and production capacity.</p></article><article><h3>Express Service — +35%</h3><p>Priority tailoring is subject to availability, feasibility and an individually confirmed completion date.</p></article></div><details class="tailoring-disclosure"><summary>Turnaround estimates &amp; additional charges</summary><div class="tailoring-detail-content"><p>'''+escape(f['texts'][f['services']['custom-tailoring']['timingTextKey']])+'''</p><div id="service-info-charges"><p>'''+escape(f['texts']['policyCharges'])+'''</p></div></div></details></section>'''
    body+='''<section class="release-section" id="tailoring-inclusions"><h2>Included with Your Standard Suit</h2><ul class="tailoring-inclusions"><li>Initial standard garment cleaning</li><li>Branded hanger and protective cover</li><li>Initial Kigali delivery</li></ul><p>These inclusions apply to the standard custom-suit package. Men’s tuxedo inclusions and any separately quoted requirements are confirmed in your quotation.</p></section>'''
    body+='<section class="release-section" id="tailoring-details"><h2>Helpful Order Information</h2>'
    body+=disclosure('fabric','Your design & customer-supplied fabric',[f['texts']['policyOwnFabric'],'Browse Men’s or Women’s Suits and select one or more website designs, or use the Special Order alternative for your own inspiration. Fabric preferences or assistance follow before your quotation.'])
    body+=disclosure('measurements','Measurements, fittings & garment choices',['Measurements and fitting arrangements are reviewed with your design and garment requirements. We agree these arrangements and the quotation before production.',service['sections'][1][1],service['sections'][2][1]])
    body+=disclosure('transport','Collection & delivery arrangements',['Initial Kigali delivery is included with your standard suit package as shown above. Confirm the delivery address, timing and required payment before dispatch. Additional or outside-Kigali delivery and international shipping require the applicable agreed quotation; no universal price or transit time is promised.'])
    correction=next(row[2] for row in sections('custom-tailoring') if row[0]=='corrections')
    body+=disclosure('corrections','Fitting & workmanship concerns',[correction])+'</section>'
    body+='<nav class="tailoring-bottom-nav release-section" aria-labelledby="tailoring-next"><h2 id="tailoring-next">Find Your Next Design</h2><div>'+link('/mensuits/','Explore Men’s Suits','home-button home-button-gold')+link('/womensuits/','Explore Women’s Suits','home-button home-button-gold')+link('/services/custom-tailoring/special-order/','Special Tailoring','home-button home-button-gold')+'</div></nav>'
    return body

def decorate(source):
    styles=(ROOT/'_templates/custom-tailoring-mobile.css').read_text()+'\n'+(ROOT/'_templates/announcement-bar.css').read_text()
    source=source.replace('</style>',styles+'</style>',1).replace('class="tailoring-page customer-site"','class="tailoring-page customer-site custom-tailoring-mobile"')
    offer=json.loads((ROOT/'_data/custom-tailoring-page.json').read_text())['announcement']
    messages=''.join('<span class="announcement-message">'+escape(message)+'</span>' for message in offer['messages'])
    bar=(ROOT/'_templates/announcement-bar.html').read_text().replace('{{offer_messages}}',messages)
    assert source.count('</div><main id="main-content"')==1
    source=source.replace('</div><main id="main-content"',bar+'</div><main id="main-content"',1)
    return source.replace('</body>','<script>'+ (ROOT/'_templates/announcement-bar.js').read_text()+'</script></body>',1)
