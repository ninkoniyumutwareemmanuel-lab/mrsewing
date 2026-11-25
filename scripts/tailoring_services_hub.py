"""Staging: customer-first Tailoring & Clothing Services hub; existing routes and approved policies."""
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def content(service, hero, section, link):
    from build_collections import load, picture
    from clothing_categories import active

    policies = json.loads((ROOT / "_data/customer-policy-facts.json").read_text(encoding="utf-8"))
    tailoring = policies["services"]["custom-tailoring"]
    charges = policies["charges"]
    payments = policies["payments"]
    standard = escape(tailoring["standardTurnaround"])
    express = escape(tailoring["expressTurnaround"])
    advance = int(payments["domesticCustomAdvancePercent"])
    balance = int(payments["domesticCustomBalancePercent"])
    express_rate = int(charges["expressPercent"])
    after_hours = int(charges["afterHoursPercent"])
    combined = int(charges["combinedPercent"])

    cover = hero("custom-tailoring")
    cover = cover.replace(
        "<h1>" + escape(service["title"]) + "</h1>",
        "<h1>Tailoring &amp; Clothing Services</h1>", 1
    )
    cover = cover.replace(
        escape(service["intro"]),
        "Professional tailoring in Kigali, Rwanda. Clothing made around your design, style, measurements and agreed quotation.",
        1,
    )

    # Policy amounts and estimates come from the owner-approved customer facts,
    # not from retail price assumptions or historical internal costing.
    facts = [
        ("Standard tailoring", standard,
         "Usually for custom suits. Your completion date is confirmed for your order."),
        ("Express tailoring", express,
         f"Subject to feasibility and capacity; +{express_rate}% on the eligible quoted base."),
        ("Domestic custom advance", f"{advance}%",
         f"Normally before production; the remaining {balance}% is due before final cleaning and delivery."),
        ("Customer-supplied fabric", "Assessment first",
         "We check suitability, quantity and condition before confirming a quotation."),
    ]
    fact_cards = "".join(
        '<article class="tailoring-hub-fact"><h3>' + escape(title) +
        '</h3><strong>' + value + '</strong><p>' + escape(description) + '</p></article>'
        for title, value, description in facts
    )
    essentials = f'''<section class="release-section tailoring-hub-essentials" aria-labelledby="tailoring-hub-essentials-title">
      <p class="home-eyebrow">01 · Before you order</p>
      <h2 id="tailoring-hub-essentials-title">Know What to Expect</h2>
      <p>These are the usual terms for domestic custom tailoring, not a confirmed quotation or guaranteed completion date. We assess your request before accepting an order.</p>
      <div class="tailoring-hub-fact-grid">{fact_cards}</div>
      <div class="tailoring-hub-policy-details" id="payment-arrangements"><h3>Payment &amp; Order Confirmation</h3><p><strong>Standard orders:</strong> Ordinary domestic custom garment orders normally require a 70% advance before official work begins and the remaining 30% before release or delivery, unless a different approved arrangement is confirmed in the quotation. For standard suits, the balance is due after tailoring completion and before final cleaning and delivery. Full payment must be confirmed before garment release.</p><details><summary>Request a flexible advance payment</summary><p>For eligible domestic Standard custom tailoring orders, customers unable to pay the usual 70% advance may request an individually agreed lower initial payment. This is not an automatic entitlement. Production may begin only when operationally and financially feasible and the applicable order conditions are confirmed. The entire outstanding balance must be paid within three calendar days of the initial payment, even if the garment is not yet finished. The initial amount, remaining balance and exact deadline must be communicated and accepted. This exception is not available for Express orders and does not automatically apply to international orders, mobile assistance, consultations or VIP arrangements.</p><p>Under an agreed exceptional advance arrangement, production is suspended if the full outstanding balance is not paid by the three-calendar-day deadline. We notify the customer of the overdue amount and its effect on the order. Payment must be settled before work resumes on an order that remains open; the completion date may need reassessment.</p></details><details><summary>Express payment arrangements</summary><p>For domestic Express tailoring, the normal 70% advance applies to the total agreed quotation, including the 35% Express surcharge and any other charges included in that quotation. The remaining 30% is due at completion, before release, subject to applicable final-cleaning arrangements. Express deadlines are agreed individually; the below-70% exception does not apply.</p></details><p>For cancellations, refunds and changes, read our <a href="/refund-policy/">Refund &amp; Cancellation Policy</a> and <a href="/faq/prices-packages-payments/">payment FAQs</a>.</p></div>
      <details class="tailoring-hub-policy-details"><summary>How are Express and after-hours charges calculated?</summary>
        <p>Eligible Express service adds {express_rate}% to the agreed base service price. Necessary, agreed after-hours work from 17:00 to 22:00 Kigali time adds {after_hours}% of the same eligible base. When both apply, the total additional charge is {combined}%, not compounded. Work after 22:00 is individually quoted. Your quotation must show agreed charges before work begins.</p>
      </details>
      <p class="tailoring-hub-small-note">International custom orders have a different advance arrangement: 100% of the agreed quotation before production, following feasibility assessment. Alterations, garment care, mobile assistance and VIP requests follow the payment terms in their accepted quotations.</p>
      <a class="home-text-link" href="/customer-information/">Read the full order and payment guidance</a>
    </section>'''

    process = '''<section class="release-section tailoring-hub-overview" aria-labelledby="tailoring-hub-intro">
      <p class="home-eyebrow">02 · How tailoring works</p>
      <h2 id="tailoring-hub-intro">From Your Idea to a Finished Garment</h2>
      <ol class="tailoring-hub-steps">
        <li><span class="tailoring-hub-step-number" aria-hidden="true">01</span><div><h3>Tell Us What You Need</h3><p>Choose a clothing reference or describe your own design. Tell us the occasion, requested date, style and preferred fabric.</p></div></li>
        <li><span class="tailoring-hub-step-number" aria-hidden="true">02</span><div><h3>Fabric, Measurements &amp; Fittings</h3><p>We discuss fabric suitability and availability, measurements, fitting arrangements and any necessary materials.</p></div></li>
        <li><span class="tailoring-hub-step-number" aria-hidden="true">03</span><div><h3>Accept the Quotation</h3><p>We confirm design requirements, price, applicable payment and proposed completion date. An enquiry or payment screenshot is not a confirmed production order.</p></div></li>
        <li><span class="tailoring-hub-step-number" aria-hidden="true">04</span><div><h3>Production, Final Payment &amp; Handover</h3><p>The production period starts with our separate official production-start notice. We arrange agreed fittings, final payment, cleaning where included, and collection or delivery.</p></div></li>
      </ol>
      <p class="tailoring-hub-policy">Read the <a href="/terms-and-conditions/current/">currently effective Terms &amp; Conditions</a>. The <a href="/terms-and-conditions/">PDF reader</a> is available for review; official activation is being reconciled.</p>
    </section>'''

    fabric = '''<section class="release-section tailoring-hub-fabric" aria-labelledby="tailoring-hub-fabric-title">
      <p class="home-eyebrow">03 · Fabric and measurements</p>
      <h2 id="tailoring-hub-fabric-title">Choose Fabric with Confidence</h2>
      <p>Start with your preferred garment, colour, feel and occasion. We assess what is suitable and available before agreeing the materials and quotation.</p>
      <div class="tailoring-hub-fabric-grid">
        <article class="tailoring-hub-fabric-card"><h3>Choose Fabric with Our Guidance</h3><p>Explore fabric options and discuss how they suit your design. Website photographs do not guarantee exact material, colour or availability.</p><a class="home-text-link" href="/guides/fabrics/">Explore the Fabric Guide</a></article>
        <article class="tailoring-hub-fabric-card"><h3>Have Your Own Fabric?</h3><p>We can assess customer-supplied fabric for quantity, condition, design suitability and any extra materials. Assessment comes before acceptance; we agree changes with you.</p><a class="home-text-link" href="/services/custom-tailoring/special-order/">Discuss Your Fabric or Design</a></article>
      </div>
      <p class="tailoring-hub-small-note">You may begin an enquiry without final measurements. <a href="/measurements/">See the Measurements Guide</a> to prepare for the fitting discussion.</p>
    </section>'''

    categories = []
    for category in active(load()[0]):
        image = picture(category["cover"]["images"][0])
        categories.append(
            '<a class="tailoring-hub-category" href="' + escape(category["url"], quote=True) + '">'
            + image + '<span><h3>' + escape(category["name"]) + '</h3><p>'
            + escape(category["description"])
            + '</p><strong>Explore designs <span aria-hidden="true">→</span></strong></span></a>'
        )
    collections = '''<section class="release-section tailoring-hub-categories" aria-labelledby="tailoring-hub-categories">
      <p class="home-eyebrow">04 · Clothing categories</p>
      <h2 id="tailoring-hub-categories">Explore Clothing Designs</h2>
      <p>Browse approved design references for men's and women's clothing. Choose a reference and request a quotation; a picture does not guarantee fabric availability or a completed garment.</p>
      <div class="tailoring-hub-category-grid">''' + "".join(categories) + '''</div>
      <p><a class="home-text-link" href="/collections/">See All Designs in the Showroom</a></p>
    </section>'''

    # Keep the four owner-approved service journeys distinct. A combined repair
    # and cleaning request is explained separately, not invented as a fifth form.
    services = [
        ("Special Tailoring", "Have a design of your own? Discuss garments, reference pictures, fabric and an individually assessed quotation.",
         "/services/custom-tailoring/special-order/", "Explore Special Tailoring"),
        ("Clothing Alterations & Repairs", "Ask about fit adjustments and repairs. We inspect the garment and confirm what is feasible, the price and the completion date.",
         "/services/alterations/", "Explore Alterations"),
        ("Garment Care & Cleaning", "Request garment-cleaning assessment based on condition, fabric and care labels. Timing and suitability are confirmed before acceptance.",
         "/services/garment-care/", "Explore Garment Care"),
        ("Mobile Tailoring & Fittings", "Discuss measurement or fitting visits, location and professional assistance. Visits and charges require individual confirmation.",
         "/services/mobile-fitting/", "Explore Mobile Assistance"),
    ]
    service_cards = "".join(
        '<article class="tailoring-hub-service"><h3>' + escape(title) +
        '</h3><p>' + escape(description) + '</p>' +
        link(url, label, "home-button home-button-gold") + '</article>'
        for title, description, url, label in services
    )
    additional = '''<section class="release-section tailoring-hub-additional" aria-labelledby="tailoring-hub-additional">
      <p class="home-eyebrow">05 · Additional services</p>
      <h2 id="tailoring-hub-additional">How Else Can We Help?</h2>
      <p>Open a service to learn what is assessed and how to request its own quotation. No request automatically confirms acceptance or a booking.</p>
      <div class="tailoring-hub-service-grid">''' + service_cards + '''</div>
      <aside class="tailoring-hub-combined"><h3>Need Both Repairs and Cleaning?</h3>
        <p>Ask for Garment Repair &amp; Care in one coordinated enquiry. Each service is assessed and quoted separately; there is no automatic bundle discount or approval for extra work.</p>
        <a class="home-text-link" href="/request/?general=1">Request a Combined Assessment</a>
      </aside>
      <p class="tailoring-hub-small-note">For complex garments, special events or personalised cross-service assistance, <a href="/services/vip/">explore VIP Services</a>. Each request is assessed individually.</p>
    </section>'''

    faq = '''<section class="release-section tailoring-hub-faq" aria-labelledby="tailoring-hub-faq-title">
      <p class="home-eyebrow">06 · Common questions</p>
      <h2 id="tailoring-hub-faq-title">Helpful Answers Before You Enquire</h2>
      <div class="tailoring-hub-faq-list">
        <details><summary>When does my production time begin?</summary><p>When Mr Sewing issues an official production-start notice after the required order steps are complete, not when you first enquire or share proof of payment.</p></details>
        <details><summary>Can I request tailoring without measurements?</summary><p>Yes. Tell us what you want to make and we can discuss the measurements and fittings needed before your order is confirmed.</p></details>
        <details><summary>Can you copy an exact design or colour from a photo?</summary><p>Reference photographs help explain your preferences, but the final design, fabric, colour and feasibility must be assessed and agreed before acceptance.</p></details>
      </div>
      <p><a class="home-text-link" href="/faq/">Visit Frequently Asked Questions</a></p>
    </section>
    <section class="release-section tailoring-hub-final" aria-labelledby="tailoring-hub-final-title">
      <h2 id="tailoring-hub-final-title">Ready to Discuss Your Garment?</h2>
      <p>Share your preferred design, occasion, fabric needs and requested date. We will review your enquiry and confirm the next steps.</p>
      <a class="home-button home-button-gold" href="/request/?general=1">Request a Quotation</a>
    </section>'''

    return cover + essentials + process + fabric + collections + additional + faq
