"""Staging R59: compact Tailoring & Clothing Services hub using the existing verified service routes."""
from html import escape

def content(service, hero, section, link):
    from build_collections import load,picture
    from clothing_categories import active
    cover=hero('custom-tailoring')
    cover=cover.replace('<h1>'+escape(service['title'])+'</h1>', '<h1>Tailoring &amp; Clothing Services</h1>',1)
    cover=cover.replace(escape(service['intro']),'Professional tailoring in Kigali, Rwanda. Clothing made around your design, style, measurements and agreed quotation.',1)
    general='''<section class="release-section tailoring-hub-overview" aria-labelledby="tailoring-hub-intro">
      <p class="home-eyebrow">01 · How tailoring works</p>
      <h2 id="tailoring-hub-intro">Professional Tailoring, Made Personal</h2>
      <p>Tell us about the outfit you want to make, or begin with a clothing design reference. We assess your style, fit, garment requirements and what can be made before confirming a quotation.</p>
      <div class="tailoring-hub-info">
        <article><h3>Design &amp; Fabric</h3><p>Share your design preferences. We can discuss fabric options or assess customer-supplied fabric for suitability.</p></article>
        <article><h3>Measurements &amp; Fittings</h3><p>Measurement and fitting arrangements are discussed for your garment and location. We confirm what is required before production.</p></article>
        <article><h3>Quotation &amp; Confirmation</h3><p>Production, price, payment requirements and any proposed completion date are confirmed through the accepted quotation and formal order process.</p></article>
        <article><h3>Handover &amp; Care</h3><p>Collection, delivery and any further garment-care requirements are agreed for the individual order.</p></article>
      </div>
      <p class="tailoring-hub-policy">Read the full <a href="/terms-and-conditions/current/">currently effective Terms &amp; Conditions</a>, or review the <a href="/terms-and-conditions/">approved PDF reader</a>. The PDF's official activation is being reconciled.</p>
    </section>'''
    cards=[]
    for category in active(load()[0]):
        image=picture(category['cover']['images'][0])
        cards.append('<a class="tailoring-hub-category" href="'+escape(category['url'],quote=True)+'">'+image+'<span><h3>'+escape(category['name'])+'</h3><p>'+escape(category['description'])+'</p><strong>Explore designs <span aria-hidden="true">→</span></strong></span></a>')
    collections='<section class="release-section tailoring-hub-categories" aria-labelledby="tailoring-hub-categories"><p class="home-eyebrow">02 · Clothing categories</p><h2 id="tailoring-hub-categories">Explore Clothing Designs</h2><p>Browse eligible reference photographs in our one Showroom. You can change categories or view all designs there.</p><div class="tailoring-hub-category-grid">'+''.join(cards)+'</div><p><a class="home-text-link" href="/collections/">See All Designs in the Showroom</a></p></section>'
    services=[
        ('Special Tailoring','Have your own idea? Discuss a photograph or proposed garment, fabric preferences, measurements and a personalised quotation.','/services/custom-tailoring/special-order/'),
        ('Clothing Alterations & Repairs','Request an assessment of fit adjustments, repairs or changes to your existing garment.','/services/alterations/'),
        ('Garment Care & Cleaning','Discuss appropriate cleaning or garment care after reviewing the fabric, care label and condition.','/services/garment-care/'),
        ('Mobile Tailoring & Fittings','Request individually arranged measurement, fitting, location or event assistance, subject to availability and quotation.','/services/mobile-fitting/')
    ]
    service_cards=''.join('<article class="tailoring-hub-service"><h3>'+escape(title)+'</h3><p>'+escape(desc)+'</p>'+link(url,'Explore Service','home-button home-button-gold')+'</article>' for title,desc,url in services)
    extra='<section class="release-section tailoring-hub-additional" aria-labelledby="tailoring-hub-additional"><p class="home-eyebrow">03 · Additional services</p><h2 id="tailoring-hub-additional">How Else Can We Help?</h2><div class="tailoring-hub-service-grid">'+service_cards+'</div><p>For personalised cross-service assistance, <a href="/services/vip/">explore VIP Services</a>. Each request is assessed under its own requirements.</p></section>'
    return cover+general+collections+extra
