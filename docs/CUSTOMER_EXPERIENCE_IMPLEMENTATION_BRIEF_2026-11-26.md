# Customer experience implementation brief — 26 November 2026

Internal development reference, not customer policy or legal advice. This document records the pre-writing applicability/route brief required by `AGENTS.md`. It does not claim implementation, testing or deployment has finished.

## Baseline, scope and authority

- Repository: `ninkoniyumutwareemmanuel-lab/mrsewing`.
- Authorized branch: `phase1/customer-journey-repairs`.
- Starting commit: `b388644796fcb24b747bb6818dd211422fab9cff`.
- Initial Main reference: `33620fe4dc38ec81905fd2556a19db15f5c06db3`; recheck before final delivery.
- Intended permanent staging: `https://mrsewing-staging.pages.dev/`. The prior Cloudflare provider receipt reports staging preview `https://7a780f7f.mrsewing-staging.pages.dev/`; actual origin/settings remained unverified because of network/account access. Neither receipt proves what the permanent domain serves today.
- Latest authority: owner's comprehensive26November2026audit/design/implementation task, directly read in this conversation. Current reference `versions/2026-11-26-01` preserves the prior five-document snapshot as exact prefixes and appends this scope. No production/Main authority is given.
- Original company handbook archives, private Library's approved1.1PDF, Search Console and analytics/account dashboards remain unavailable unless separately connected. Do not claim those sources were inspected.

## Actual source map / edit discipline

Source-level changes must be rebuilt; do not patch only generated output. Current verified responsibilities:

| Area | Existing authoritative source |
|---|---|
| Build orchestration and SEO projection | `scripts/build_site.py`, `scripts/site_seo.py`, `_data/page-seo.json`, `_data/seo-search-intent.json` |
| Shared header/footer/navigation | `_templates/homepage-header.html`, `_templates/homepage-footer.html`, `scripts/shared_components.py` |
| Homepage and About | `scripts/build_homepage.py`, `_templates/homepage-tailoring.html`, `_templates/homepage-tailoring.css`; `scripts/build_about.py`, `_templates/about.html` |
| Service landing pages | `scripts/customer_site.py`, `scripts/build_journey.py`, `scripts/tailoring_services_hub.py`, `_data/customer-release.json` |
| Showroom and design data | `scripts/build_collections.py`, `_templates/collections.html`, `_templates/collections.css`, `assets/collections-v3.js`, `_data/collection-designs.json`, `_data/clothing-category-config.json` |
| Genuine project work | `_data/customer-projects.json`, existing project/portfolio builders and publication records |
| Fabric catalogue | `scripts/customer_guides.py`, `scripts/fabric_collections.py`, `_data/fabric-collections.json`, `_data/fabric-colours.json`, `_templates/fabric-showroom.js` |
| Shared selection/quotation state | `_templates/design-selections.js`, `_templates/request-context.js`, `_templates/quotation-arrangements.js`, `_templates/customer-site.js`, `scripts/selected_designs.py` |
| Receiving validation | `functions/api/`, `functions/_lib/selected-design-handler.js`, `functions/_lib/quotation-details.js`, `functions/_lib/fabric-preferences.js` |
| Approved commercial facts/publication | `_data/customer-policy-facts.json`, `scripts/customer_policies.py`, `_data/public-content-policy.json`; internal suit/tuxedo price records remain separate |
| FAQ and policy projections | `_data/customer-faqs.json`, `scripts/faq_help.py`, `scripts/refund_page.py`, `scripts/privacy_page.py` |
| Shop | `_data/shop-products.json`, `_data/shop-public-enquiries.json`, `scripts/shop_catalog.py`, `scripts/shop_preview.py`, existing Shop Functions |
| Contacts / business / hours | `_data/business.json`, `_data/contact-v2.json`, `_data/business-hours.json`; use verified existing WhatsApp configuration |
| Terms reader/current contract | `_data/policy-documents.json`, `scripts/terms_reader.py`, `_templates/terms-reader.*`; `/terms-and-conditions/current/` remains contractual fallback |
| Source exposure boundary | `functions/_middleware.js`; blocking deployed source paths does not make the public Git repository/history confidential |

See `docs/WEBSITE_SOURCE_MAP.md` for the complete established architecture. New sources introduced during this task must be added there at integration; this brief does not invent names for files not yet implemented.

## Pre-writing page and action contracts

| Page/audience/purpose | Permitted presentation/action improvement | Existing action/context contract and failure behavior |
|---|---|---|
| Home: prospective tailoring customer | Compact garment-first messaging/navigation; correct “Made for your style” crop; consistent labels | Existing service/Showroom/WhatsApp destinations remain; preserve official number, manual image attachment and no-send/no-delivery distinction; retain reduced-motion video/photo behavior |
| Public tailoring men/women/category/design pages | Preserve standalone browsing; hide unnecessary visible technical IDs; improve photo/name/card layouts | Category/card remains ordinary crawlable link to correct existing design; Select This Design preserves actual canonical original photo, internalID and quantity in shared selection system |
| Guided selected-suit request | One reusable accessible dialog, compact thumbnails/quantity controls, shared fabric preference, conditional details/review/explicit submit | Reuse existing state/forms/backend; keep direct selected-design/fabric/request routes; close/add-more/back/resume do not overwrite separate active quotation. No personal information in URL; no new provider/upload or automatic order |
| Showroom / Our Work | Photos first, compact working search/filters, meaningful names, genuine-work marks only, newest eligible date evidence | Actual data filtering/order/family/photo mapping remains; unknown-date fallback documented; Reference Design is not stock or company-made work; sparse collections show fewer items |
| Fabric Guide and collections | Compact general-information comparison; truthful representative images only when eligible mapping is verified | One shared preference/fabric/pattern/colour applies to entire request subject to garment suitability; advice/own paths bypass unnecessary browsing; existing designs/contact drafts retained |
| About | Concise brand/legal relationship, approved mission/vision/story; gated leadership preparation | No public unfinished portrait/title/bio; preserved valid services/contact actions and no invented achievements/company dates |
| Alterations / Care / Mobile / VIP / Special | Concise scope/conditions and direct “Contact Us on WhatsApp” hero | Verified official destination, service-specific editable prepared text, user manually sends; existing dedicated forms/API routes remain. No WhatsApp click counted as submitted enquiry |
| Combined repairs and cleaning card | Direct official WhatsApp message: “Hello Mr Sewing Fashion, I need both garment repairs and professional cleaning.” | Separate assessment/pricing, no automatic discount; additional paid work needs agreement; do not charge same applicable transport twice; existing combined URL retained if useful |
| Shop / product enquiries | Preserve existing option/quantity/request/consent/error paths | Server reconstructs trusted product/price/eligibility; no automatic catalogue publication/stock reservation/purchase claim/new payment gateway |
| FAQ/payment/refund/privacy/currentTerms | Correct factual duplication and direct anchors, scope-aware short notices | Shared facts project to text/search/schema; no new proposed contract, invented refund/forfeiture or Terms reviewPDF becoming current by accident |

All controls must have accurate labels, comfortable tap targets, keyboard/focus/error semantics and no clipping. Modal focus/close/background scroll/browser-back behavior need real browser tests. Labels standardize only truly equivalent actions; viewing, selecting, sharing, reviewing, submitting and acceptance must remain distinct.

## Applicable rules and business reconciliation

Relevant source IDs: C06/C12 design/fabric truthfulness; C13 measurements; C17–C25 quotation/payment/confirmation (historical details must be read with later R49/25Nov supersession); C31–C37 handover/corrections/refund/privacy; C44 benefits with R37 approved clarification; C46 form behavior; C47 identity; C48 provenance; C50 staging. Current task adds NOV26-01 through NOV26-10 in the dated source matrix.

Confirmed preservation:

- Relevant domestic custom tailoring normally70%advance before official start and30%at completed work before release, with standard suits before final cleaning/delivery; international/mobile/VIP retain their own accepted conditions.
- The25November approved exceptional advance is individually assessed, domestic Standard tailoring only, full outstanding balance due within three calendar days, not Express; suspension and case-by-case cancellation/refund safeguards remain. The26November Flexible Advance Payment concept is a separate inactive proposal.
- R49 Independent Consultation & Fitting35,000RWF supersedes25,000 for that service. Eligible order-related Kigali measurement visit10,000RWF is separate; independent assistance50,000RWF has existing up-to-five-people/three-hour scope; beyond either limit requires VIP assessment.
- Latest quotation-first service tariff presentation remains authoritative while26Nov olderV8 starting-price references are reconciled. Do not restore historical public prices or erase internal approved values. Shop commercial records remain independent.
- Existing Standard/Express screening,35%Express/25%necessary agreed after-hours/additive60% disclosure and individually assessed overnight scope are not free upgrades or confirmed deadlines. Production starts only under the approved separate start notice.
- No new fabric composition, stock, material origin, colour availability, manufacturing history or unlimited benefit is inferred. Collection labels are not supplier specifications.
- Existing benefits/promotions remain scope-specific: no discount stacking engine or new gift quantities.
- Latest Terms upload is actually1.2/6pages20sections, staging review only. Preserve1.0/current consent and no fabricated official effective date or claim to match unavailable approved14section1.1.

## Explicit held decisions

1. Public service tariff reinstatement versus newer quotation-first instruction:26Nov contains oldV8 examples and a newer-information reconciliation requirement; do not silently assume repeal.
2. Flexible Advance Payment proposal: new minimum/scope/funding/extensions/cancellation/refund/restart rules inactive; see separate draft/readiness report.
3. Leadership portrait/public title/biography and any company history not already evidenced.
4. Workmanship origin for unverified reference images; repository usage permission is not proof of company manufacture.
5. Representative fabric image mapping/specifications/stock evidence; do not publish a simulation as actual material.
6. Actual Search Console indexing, analytics receipt, Cloudflare permanent domain/settings, production HTTP status and field performance remain unverified where access is absent.

## Testing and evidence obligations

Capture before/after representative mobile/desktop pages and measured conditions before comparison. Inventory every generated route including hidden aliases; baseline page metadata/actions/links/schema/images and existing regressions. Run the existing site build and `--check`, media/policy/SEO/sitemap plus scoped Shop/selection/request/backend/consent checks. Use synthetic mocked submissions and intercepted WhatsApp/phone/native-share/analytics: no real enquiries/messages/payments/customer records.

Exercise one/many/mixed designs, quantities/removal/add-more, shared fabric/advice/own, back/close/resume/expiration, required/conditional fields, exact payload, provider failure/retry/duplicate/positive acknowledgement, Shop requests, FAQ/search/policy anchors and all primary service messages. Test320/390/768/1440px at minimum; record available browser engines, screenshot paths, actual accessibility findings and comparable lab performance rather than field claims.

Report PASS/FAIL/BLOCKED/NOT TESTED per requirement. Prior recovery results are baseline evidence, not automatic passes for changed code. Staging deployment provider success is separate from actual rendered permanent-site verification. No Main/production action is authorized.
