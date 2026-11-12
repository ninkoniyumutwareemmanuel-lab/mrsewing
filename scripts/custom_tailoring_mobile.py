"""R35: page-scoped owner-approved Custom Tailoring presentation; no global policy rewrite."""
import json
from html import escape
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def pricing():
    ordinary=json.loads((ROOT/'_data/suit-package-prices.json').read_text())['prices']
    tuxedos=json.loads((ROOT/'_data/tuxedo-package-prices.json').read_text())['tiers']
    groups=[('Men’s Ordinary Suits',sorted((p for p in ordinary.values() if p['category']=='men' and p['publicationApproved']),key=lambda p:p['tier'])),('Women’s Ordinary Suits',sorted((p for p in ordinary.values() if p['category']=='women' and p['publicationApproved']),key=lambda p:p['tier'])),('Men’s Tuxedos',tuxedos)]
    out='<section class="release-section" id="service-info-prices"><h2>Starting Suit Prices</h2><p>These are complete-garment starting prices, not fabric-only prices. Your final quotation depends on the confirmed fabric, design and order requirements. Men’s tuxedos have their own pricing schedule.</p><div class="tailoring-price-grid">'
    for name,rows in groups:
        out+='<table class="tailoring-price-table"><caption>'+name+'</caption><thead><tr><th scope="col">Tier / Quality</th><th scope="col">Two-piece <span>(RWF)</span></th><th scope="col">Three-piece <span>(RWF)</span></th></tr></thead><tbody>'
        for row in rows:
            out+='<tr><th scope="row">Tier '+str(row['tier'])+'</th><td>'+format(row['twoPieceRwf'],',')+'</td><td>'+format(row['threePieceRwf'],',')+'</td></tr>'
        out+='</tbody></table>'
    return out+'</div></section>'

def children():
    return '''<section class="release-section tailoring-family" id="service-info-children"><p class="home-eyebrow">Family tailoring</p><h2>Children’s Suits: 50% Off with an Adult Suit</h2><p>Dress the family together. Children under 12 automatically receive a 50% discount on each eligible child’s suit when the same order includes at least one adult suit.</p><ul class="tailoring-list"><li>The discount applies to children younger than 12, across all suit tiers and quality levels.</li><li>Each eligible child’s suit receives the discount. The adult suit stays at its normal applicable price.</li><li>Children’s normal starting prices follow the corresponding suit pricing schedule above. Without an adult suit in the order, children’s suits are charged at the normal applicable suit price.</li></ul><aside class="tailoring-example" aria-labelledby="family-example"><h3 id="family-example">A simple family example</h3><p>One adult Tier 2 two-piece suit: <strong>400,000 RWF</strong>.</p><p>Two eligible children’s Tier 2 two-piece suits: each reduced from 400,000 RWF to <strong>200,000 RWF</strong>.</p><p class="tailoring-total">Total: <strong>800,000 RWF</strong>, excluding separately quoted charges.</p></aside></section>'''

def payments():
    return '''<section class="release-section" id="service-info-payments"><h2>Payment and Order Confirmation</h2><div class="tailoring-payment-grid"><article><h3>Domestic custom tailoring</h3><ul class="tailoring-list"><li><strong>70% advance payment</strong> before production.</li><li>The remaining <strong>30%</strong> is payable when tailoring is completed, before final cleaning and delivery.</li><li>Full payment is required before garment release.</li></ul></article><article><h3>International custom tailoring</h3><ul class="tailoring-list"><li>We confirm feasibility and the quotation first. You then accept the quotation.</li><li><strong>100% advance payment</strong> is required before production.</li><li>Shipping and applicable additional charges are quoted for your specific order. There is no universal international shipping fee or guaranteed transit time.</li></ul></article><article><h3>Payment verification</h3><ul class="tailoring-list"><li>Payment must be received and verified. A transfer screenshot is not proof of receipt.</li><li>Production begins only after verified payment, all necessary order requirements and the applicable official order confirmation and production-start notice.</li><li>Use verified payment instructions from Mr Sewing Fashion. Protect your PINs and account credentials.</li></ul></article></div></section>'''

def content(service,hero,section,link):
    body=hero('custom-tailoring')+'<nav class="tailoring-section-nav" aria-label="Custom Tailoring information"><a href="/services/custom-tailoring/#service-info-prices">Suit prices</a><a href="/services/custom-tailoring/#service-info-children">Children’s suits</a><a href="/services/custom-tailoring/#service-info-payments">Payments</a><a href="/services/custom-tailoring/#service-info-timing">Service details</a></nav>'
    body+=pricing()+children()+payments()
    for title,text in service['sections']:
        if title=='Payment and confirmation':continue
        body+=section(title,text)
    from customer_policies import sections
    for ident,title,text in sections('custom-tailoring'):
        if ident in ['prices','children','payments']:continue
        body+='<section class="release-section" id="service-info-'+ident+'"><h2>'+escape(title)+'</h2><p>'+escape(text)+'</p></section>'
    body+='<section class="release-section" id="tailoring-offers"><h2>New-Customer Offers</h2><p>Discover our new-customer offers — ask us about available benefits.</p><p>The children’s family discount explained above is a separate offer.</p>'+link('/booking/','Ask About Available Benefits','home-button home-button-gold')+'</section>'
    return body

def decorate(source):
    styles=(ROOT/'_templates/custom-tailoring-mobile.css').read_text()+'\n'+(ROOT/'_templates/announcement-bar.css').read_text()
    source=source.replace('</style>',styles+'</style>',1).replace('class="tailoring-page customer-site"','class="tailoring-page customer-site custom-tailoring-mobile"')
    source=source.replace('<main id="main-content"',(ROOT/'_templates/announcement-bar.html').read_text()+'<main id="main-content"',1)
    return source.replace('</body>','<script>'+ (ROOT/'_templates/announcement-bar.js').read_text()+'</script></body>',1)
