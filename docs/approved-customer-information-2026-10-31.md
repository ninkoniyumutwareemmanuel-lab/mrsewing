# Approved customer-information update — staging review

Source: owner’s consolidated customer-information handoff dated 30 October 2026. Implementation approval: 31 October 2026 in Website & Customer Experience. Baseline: `ff43efe85a9ba098ef1d9231bf1639cba710ac6f`. Branch: `phase1/customer-journey-repairs`. Main/production publication requires separate approval.

This report contains customer-facing facts and implementation boundaries only. The confidential financial Business Reference is not copied into the public repository. Older repository review reports describe historical snapshots and do not override this decision record.

## Implemented

- Corrected the former brand name to Mr Sewing in customer facts, policy identity copy, the locations FAQ and two legacy keyword lists. Verified email addresses, Maps links, operating company, business schema, hours and contact details are unchanged.
- Added all sixteen owner-approved standard suit prices from the Cotton, Polyester, Wool / Star and Super / Americano schedules. Normal new-garment offers focus on suits and suit packages; standalone shirts, trousers and coats are by arrangement for existing customers.
- Kept two-/three-piece definitions, package inclusions and 70%/30% payment stages consistent. Added suit-order accessory and replacement-packaging prices without charging included items again.
- Replaced tailoring-stage estimates with customer planning windows: standard 7–10 working days, express 3–4 working days subject to availability; special work and actual completion dates are confirmed individually.
- Added the 35% express suit calculation, once-per-order 50% mobile suit fee, separately payable Kigali visit transport and the noncompounded combined calculation. Scope limitations remain explicit; there is no automatic calculator.
- Added assessed alteration starting prices, standard/express timelines, the express surcharge base and separate optional cleaning, packaging and transport quotations.
- Added standard paid suit-cleaning prices of 40,000 / 50,000 RWF, express totals of 54,000 / 67,500 RWF, package inclusions and complete collection-to-return planning windows. Included transport coverage still requires individual confirmation. No incomplete treatment category is activated.
- Added current manual payment methods and separated PayPal/Visa online payments as Coming Soon. No checkout, payment credentials or integration is activated.
- Updated existing service pages, collection overview information, FAQs/search/schema, Terms service facts and relevant form guidance. Individual design pages link to the shared price guide without inventing fabric classification or a photograph-specific price.
- Preserved the consultation booking page without a header/footer, all form fields/actions/integration scripts, customer photos/permissions, gallery behavior, design IDs, canonical routes, sitemap, robots, redirects and hosting headers.

## Review routes

| Topic | Existing routes |
| --- | --- |
| Main suit pricing and payments | `/faq/prices-packages-payments/` |
| Custom tailoring | `/services/custom-tailoring/`, `/services/wedding-tailoring/`, `/services/graduation-tailoring/` |
| Express | `/services/express-tailoring/`, `/faq/express-tailoring/` |
| Mobile | `/services/mobile-fitting/`, `/faq/mobile-fitting/` |
| Alterations | `/services/alterations/`, `/faq/alterations/` |
| Garment Care | `/services/garment-care/`, `/services/garment-care/services/`, `/services/garment-care/planning/`, `/faq/garment-care/` |
| Collections | `/collections/`, `/mensuits/`, `/womensuits/`; the existing 111 individual design pages link to price guidance |
| Process | `/our-process/`, `/made-to-measure/`, `/measurements/` |
| Forms | `/booking/`, `/booking-housecall/`, `/booking-workplace/`, `/booking-adjustment/`, `/measurement-submission/` |
| Policy | `/terms-and-conditions/`, `/refund-policy/`, `/privacy-policy/` |
| Programs | `/loyalty-program/`, `/referral-program/` remain Coming Soon |

The FAQ hub retains fourteen topics and now contains 86 unique published answers, with matching search entries and structured answers. Existing deep links remain valid, including `#cotton-prices`, whose question now displays the complete standard schedule.

## Held for further approval

No public program launch, signup, reward redemption, referral codes, discount interaction or payout automation. Loyalty, referral, second-purchase gifts, higher-collection follow-up cleaning details and unresolved benefit rules are retained in a separate owner-review knowledge record outside the public website repository. Photoshoot and Shop previews remain unchanged.

No replacement cancellation/refund, forfeiture, fit-correction, loss/damage, storage, courier-liability, privacy-retention or tax clauses were created. Existing unresolved policy wording remains for owner/legal review. Refund and Privacy data change only to the approved brand; the shared alteration timeline updates where referenced. Current Rwanda legal compliance is not verified by this implementation.

Outstanding commercial decisions include paid-cleaning transport area, other-garment cleaning prices, mixed/multi-suit mobile scope, extra visits, benefit qualification and express entitlement treatment. Subscription and bulk ideas remain unlaunched.

## Sources and generation

Customer-safe facts: `_data/customer-information.json`. Existing topic/policy/service/care sources are updated in place. Shared rendering: `scripts/customer_information.py`, `scripts/service_information.py`, `_templates/service-information.css` and existing builders. Generate via `python3 scripts/build_site.py`; verify via `--check`. Do not edit generated pages alone.

Exact changed-file inventory: `docs/approved-customer-information-2026-10-31-files.txt`.

## Validation

- Build and `--check`: passed.
- Fifteen applicable Python static suites, including the new approved-service-facts regression: passed.
- Approved price matrices and express/mobile arithmetic checked; unpublished category gates, exact form integrations, held legal sections and confidentiality boundaries tested.
- Responsive browser review: sixteen routes at eight widths (320, 390, 600, 768, 1099, 1100, 1280, 1440), 128 combinations. Narrow price-table and contact-email overflow found and corrected; all combinations passed after targeted rechecks.
- Expanded suit-price FAQ checked at all eight widths. Horizontal table regions are named, focusable and keyboard-scrollable.
- Mobile navigation, four updated FAQ search queries and search-result deep links reviewed. A search result opens the corresponding answer.
- Existing media, gallery data/CSS/controllers, Maps/business data, canonical metadata source, sitemap and hero controller remain protected by regression checks.
- No real form submission, customer message, payment or production deployment performed. Browser coverage is limited to the available Chromium environment; no full accessibility-compliance or Google-indexing guarantee is made.
