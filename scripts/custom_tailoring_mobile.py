"""R36: page-scoped owner-approved Custom Tailoring presentation; no global policy rewrite."""
import json
from html import escape
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def pricing():
    ordinary=json.loads((ROOT/'_data/suit-package-prices.json').read_text())['prices']
    tuxedos=json.loads((ROOT/'_data/tuxedo-package-prices.json').read_text())['tiers']
    page=json.loads((ROOT/'_data/custom-tailoring-page.json').read_text())
    labels={f['id']:('Super / Quality 1' if f['id']=='men-super' else f['name']) for f in json.loads((ROOT/'_data/fabric-reference-catalogue.json').read_text())['fabrics']}
    fabric_names={(p['category'],p['tier']):labels[id] for id,p in ordinary.items()}
    groups=[('Men’s Ordinary Suits',page['mensOrdinaryPrices']),('Women’s Ordinary Suits',sorted((p for p in ordinary.values() if p['category']=='women' and p['publicationApproved']),key=lambda p:p['tier'])),('Men’s Tuxedos',tuxedos)]
    out='<section class="release-section" id="service-info-prices"><h2>Starting Suit Prices</h2><p>These are complete-garment starting prices, not fabric-only prices. Your final quotation depends on the confirmed fabric, design and order requirements. Men’s tuxedos have their own pricing schedule.</p><div class="tailoring-price-grid">'
    for name,rows in groups:
        out+='<table class="tailoring-price-table"><caption>'+name+'</caption><thead><tr><th scope="col">Tier / Quality</th><th scope="col">Two-piece <span>(RWF)</span></th><th scope="col">Three-piece <span>(RWF)</span></th></tr></thead><tbody>'
        for row in rows:
            audience='men' if name=='Men’s Ordinary Suits' else 'women' if name=='Women’s Ordinary Suits' else None
            label=('<small>'+escape(fabric_names[(audience,row['tier'])])+'</small>') if audience else ''
            out+='<tr><th scope="row">Tier '+str(row['tier'])+label+'</th><td>'+format(row['twoPieceRwf'],',')+'</td><td>'+format(row['threePieceRwf'],',')+'</td></tr>'
        out+='</tbody></table>'
    return out+'</div><p class="tailoring-fabric-note">Fabric names are references for choosing a tier. We confirm the exact fabric, available options and suitability in your quotation.</p><div class="tailoring-quote-action"><a class="home-button home-button-gold" href="/request/?general=1">Request Your Quotation</a><p>Tell us what you would like made, or explore the suit designs below.</p></div></section>'

def children():
    return '''<section class="release-section tailoring-family" id="service-info-children"><p class="home-eyebrow">Family tailoring</p><h2>Children’s Suits: 50% Off</h2><p>Children under 12 automatically receive 50% off each eligible suit when the same order includes at least one adult suit at its normal price.</p><details class="tailoring-disclosure"><summary>Family discount conditions &amp; example</summary><div class="tailoring-detail-content"><ul class="tailoring-list"><li>Applies to children younger than 12, across all suit tiers and quality levels.</li><li>Each eligible child’s suit receives the discount; the adult suit stays at its normal applicable price.</li><li>Children’s normal starting prices follow the corresponding suit pricing schedule above. Without an adult suit, children’s suits are charged at the normal applicable price.</li></ul><aside class="tailoring-example" aria-labelledby="family-example"><h3 id="family-example">A simple family example</h3><p>One adult Tier 2 two-piece suit: <strong>400,000 RWF</strong>. Two eligible children’s Tier 2 two-piece suits: each reduced from 400,000 RWF to <strong>200,000 RWF</strong>.</p><p class="tailoring-total">Total: <strong>800,000 RWF</strong>, excluding separately quoted charges.</p></aside></div></details></section>'''

def payments():
    return '''<section class="release-section" id="service-info-payments"><h2>Payment and Order Confirmation</h2><div class="tailoring-payment-grid"><article><h3><span class="tailoring-card-amount">70%</span>Advance Payment</h3><p>Required before production, under the approved order process.</p></article><article><h3><span class="tailoring-card-amount">30%</span>Final Balance</h3><p>Payable before garment release, when tailoring is completed and before final cleaning and delivery.</p></article></div><details class="tailoring-disclosure"><summary>International orders &amp; payment verification</summary><div class="tailoring-detail-content"><h3>International custom tailoring</h3><p>After feasibility confirmation and quotation acceptance, 100% advance payment is required before production. Shipping and applicable additional charges are quoted for your specific order; no universal shipping fee or guaranteed transit time is promised.</p><h3>Verified payment</h3><p>Payment must be received and verified. A transfer screenshot is not proof of receipt. Production begins only after verified payment, all necessary order requirements and the applicable official confirmation and production-start notice.</p><p>Full payment is required before garment release. Use verified payment instructions from Mr Sewing Fashion and protect your PINs and account credentials.</p></div></details></section>'''

def disclosure(ident,title,paragraphs):
    return '<details class="tailoring-disclosure" id="service-info-'+ident+'"><summary>'+escape(title)+'</summary><div class="tailoring-detail-content">'+''.join('<p>'+escape(p)+'</p>' for p in paragraphs)+'</div></details>'

def content(service,hero,section,link):
    from customer_policies import facts,sections
    f=facts();body=hero('custom-tailoring').replace(escape(service['intro']),'Tailoring shaped around your style, with guidance on fabrics, measurements and fit.',1)
    body+=pricing()+children()+payments()
    body+='''<section class="release-section" id="service-info-timing"><h2>Tailoring Around Your Order</h2><div class="tailoring-service-grid"><article><h3>Standard Tailoring</h3><p>We agree your completion date after reviewing your order, design, fabric availability and production capacity.</p></article><article><h3>Express Service — +35%</h3><p>Priority tailoring is subject to availability, feasibility and an individually confirmed completion date.</p></article></div><details class="tailoring-disclosure"><summary>Turnaround estimates &amp; additional charges</summary><div class="tailoring-detail-content"><p>'''+escape(f['texts'][f['services']['custom-tailoring']['timingTextKey']])+'''</p><div id="service-info-charges"><p>'''+escape(f['texts']['policyCharges'])+'''</p></div></div></details></section>'''
    body+='''<section class="release-section" id="tailoring-inclusions"><h2>Included with Your Standard Suit</h2><ul class="tailoring-inclusions"><li>Initial standard garment cleaning</li><li>Branded hanger and protective cover</li><li>Initial Kigali delivery</li></ul><p>These inclusions apply to the standard custom-suit package. Men’s tuxedo inclusions and any separately quoted requirements are confirmed in your quotation.</p></section>'''
    body+='<section class="release-section" id="tailoring-details"><h2>Helpful Order Information</h2>'
    body+=disclosure('fabric','Your design & customer-supplied fabric',[f['texts']['policyOwnFabric'],'Browse Men’s or Women’s Suits and select one or more website designs, or use the Special Order alternative for your own inspiration. Fabric preferences or assistance follow before your quotation.'])
    body+=disclosure('measurements','Measurements, fittings & garment choices',['Measurements and fitting arrangements are reviewed with your design and garment requirements. We agree these arrangements and the quotation before production.',service['sections'][1][1],service['sections'][2][1]])
    body+=disclosure('transport','Collection & delivery arrangements',['Initial Kigali delivery is included with your standard suit package as shown above. Confirm the delivery address, timing and required payment before dispatch. Additional or outside-Kigali delivery and international shipping require the applicable agreed quotation; no universal price or transit time is promised.'])
    correction=next(row[2] for row in sections('custom-tailoring') if row[0]=='corrections')
    body+=disclosure('corrections','Fitting & workmanship concerns',[correction])+'</section>'
    body+='<nav class="tailoring-bottom-nav release-section" aria-labelledby="tailoring-next"><h2 id="tailoring-next">Find Your Next Design</h2><div>'+link('/mensuits/','Explore Men’s Suits','home-button home-button-gold')+link('/womensuits/','Explore Women’s Suits','home-button home-button-gold')+link('/shop/','Visit the Shop','home-button home-button-outline')+'</div></nav>'
    return body

def decorate(source):
    styles=(ROOT/'_templates/custom-tailoring-mobile.css').read_text()+'\n'+(ROOT/'_templates/announcement-bar.css').read_text()
    source=source.replace('</style>',styles+'</style>',1).replace('class="tailoring-page customer-site"','class="tailoring-page customer-site custom-tailoring-mobile"')
    offer=json.loads((ROOT/'_data/custom-tailoring-page.json').read_text())['announcement']
    bar=(ROOT/'_templates/announcement-bar.html').read_text().replace('{{offer_message}}',escape(offer['message'])).replace('{{offer_href}}',escape(offer['href'],quote=True))
    source=source.replace('<main id="main-content"',bar+'<main id="main-content"',1)
    return source.replace('</body>','<script>'+ (ROOT/'_templates/announcement-bar.js').read_text()+'</script></body>',1)
