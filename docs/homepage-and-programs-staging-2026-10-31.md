# Homepage and approved customer programs — staging review

Owner-approved scope: combined homepage and defined program implementation, approved in Website & Customer Experience on 31 October 2026. Baseline `1113e0a1e237ee3072c0eecd594d6cd3a1e06f73`; branch `phase1/customer-journey-repairs`. This implementation pass updates staging only. Main/production is unchanged.

## Homepage

- Preserved the photographs, synchronized headlines, 10-second slideshow, controls, shared navigation and overall layout.
- Added a first-screen WhatsApp quotation-enquiry link using the verified existing contact number. It opens a prefilled enquiry for the customer; it does not send a message automatically.
- Plain-language description now identifies custom suits for men and women, alterations and garment care in Kigali. A secondary link leads to the existing price/payment guide.
- Preserved four process cards while explaining the custom-suit sequence: requirements/measurements, written quote/date and 70% advance, tailoring/fittings and balance, final cleaning and handover.
- Replaced “Perfect Fit” with “a Suit Made for You.”
- Added visible visit guidance identifying the Norvège main workshop and MIC Building consultations by appointment, using existing contact data. Addresses, opening hours, Maps destinations and the shared footer are unchanged.
- Loyalty and Referral cards now link to the published information. The Complimentary Photoshoot card is preserved exactly as Coming Soon.

## Defined program content

Existing routes `/loyalty-program/` and `/referral-program/` now contain the approved content rather than placeholders. No duplicate FAQ routes were created. The FAQ hub links to these existing destinations and searches their answers. Native FAQ disclosures also work without JavaScript; direct answer hashes open the relevant disclosure when JavaScript is available.

Loyalty content explains the suit-only 3% discount from the third separate qualifying purchase onward, one purchase counted for a multi-suit order, and collection-specific second-purchase gifts. Each second qualifying order has one gift package; gifts do not repeat on every later purchase. Women's gifts are identified as inner tops worn under the suit jacket. Historical purchase verification and mixed-collection edge cases remain for team review.

Referral content separates the first-time buyer's 2% suit discount from salesperson guidance. The latter explains assigned codes recorded before the advance, 6,000 RWF per qualifying suit, full-payment/handover eligibility, exclusions and the defined 14-day windows/carry-forward rules. No unapproved existing-customer referrer reward is advertised. No signup, code issuance, checkout, commission tracking or payout automation is activated.

The shared discount rule applies the eligible 2% referral OR 3% loyalty discount only to the original standard suit price. Express/mobile percentages use that same original base; extras/transport are separate and not discounted by these suit-only benefits. The approved eligible-loyal-customer example totals 384,000 RWF. Discount interaction is explained on the pricing, express, mobile, program and Terms pages; it is not an automatic calculator.

Garment-care and suit-benefit content explains three shared standard cleaning occasions for Wool/Star and Super/Americano, including initial cleaning as occasion one and two follow-ups within three months from initial handover. Bringing only one covered piece still uses one whole occasion; no separate piece credits remain. Cotton/Polyester include the initial cleaning only. Transport, packaging and unresolved express treatment are distinguished from paid-cleaning package inclusions.

## Placement and routes

- `/`: enquiry, process, visible location roles and program introductions.
- `/loyalty-program/`: loyalty, second-purchase gifts, scope, discount calculation and FAQs.
- `/referral-program/`: buyer guidance, salesperson section, eligibility, payment windows and FAQs.
- `/faq/`: sixteen topic cards and 101 searchable unique answers, with matching structured answers at their actual destinations.
- `/faq/prices-packages-payments/`, `/faq/express-tailoring/`, `/faq/mobile-fitting/`, `/faq/garment-care/`: related questions updated consistently.
- `/services/custom-tailoring/`, wedding/graduation tailoring and collection overviews: suit benefits and links.
- `/services/express-tailoring/`, `/services/mobile-fitting/`: original-price discount/surcharge relationship.
- `/services/garment-care/`, `/services/garment-care/services/`, `/services/garment-care/planning/`: included cleaning benefit and shared counter, separate from paid cleaning.
- `/terms-and-conditions/`: defined commercial program, discount and cleaning-benefit facts.

The two existing program pages become canonical indexable production destinations and are added to the sitemap: 160 + 2 = 162 URLs. Existing canonical routes remain unchanged. Staging-host HTTP and runtime noindex safeguards remain in place. No Search Console, Maps or DNS action is performed.

## Preserved and unresolved

The consultation booking page is byte-identical to the baseline and has no header or footer. Form endpoints, scripts, fields and customer-photo permissions are unchanged. Gallery media, design IDs, gallery controllers/CSS, Shop pages, payment integrations, shared header/footer, business data and verified contacts are preserved.

Shop inventory, Photoshoot, PayPal and Visa remain Coming Soon. No subscriptions or bulk offer are created. Undefined cancellation/refund, fit responsibility, damage/loss, privacy-retention, tax and program operational edge-case policies are not invented. Refund and Privacy source content is unchanged; unresolved Terms sections remain exact. This is not a legal-compliance certification.

Only defined customer and participant information is stored in public source. Confidential supplier costs, maker fees, margins, budgets, owner pay and sales targets are not copied into the repository.

## Implementation and validation

Sources: `_data/customer-information.json`, `_data/customer-faqs.json`, `_data/policy-pages.json`, existing homepage templates, existing service/FAQ builders and `scripts/customer_programs.py`. Existing Python generation remains the build workflow. New `assets/customer-programs.js` only enhances direct links to native disclosures.

- Build and `python3 scripts/build_site.py --check`: passed.
- Sixteen Python static suites: passed, including approved program/gift/shared-counter facts, original-price arithmetic, answer/schema/search parity, publication gates and exact preservation checks.
- Thirteen representative routes at eight widths (320, 390, 600, 768, 1099, 1100, 1280, 1440): 104 layout combinations passed without horizontal overflow; first-screen homepage enquiry access verified in the tested 850px-high frames.
- Expanded mobile gift FAQ, mobile menu, four program search queries, program search-result navigation and direct payout-answer links checked.
- Homepage and loyalty content visually reviewed in the available Chromium environment. No full accessibility-compliance or Google-indexing guarantee is made.
- No live form submission, customer message, payment, enrollment or production release performed.

Exact changed-file inventory: `docs/homepage-and-programs-staging-2026-10-31-files.txt`.
