# R48 — Complete ordinary-suit customer journey refinement

Owner instruction:13November2026. Implementation baseline `c1428b991b809ee0b8b3289086f07d831c4549c7`. Development branch `phase1/customer-journey-repairs`; staging only. Production main baseline `4d972f29417fa60366ebdb6348e1599208f6ae08` remains protected.

## Existing routes and completed behavior

1. Homepage `/` → `/services/custom-tailoring/` → `/mensuits/` or `/womensuits/` → the existing category and individual design routes. These entry pages, images, categories, prices and design-selection actions are preserved.
2. `/services/custom-tailoring/selected-designs/` keeps review, quantities, removal, WhatsApp Terms consent, optional sharing and the existing continuation.
3. `/services/custom-tailoring/fabric/?multiple=1` now asks exactly one shared fabric preference, with a compact expandable selected-design summary and an edit action. Choosing a fabric continues to the guide. Advice or own fabric continues directly to the existing quotation.
4. `/guides/fabrics/?fabricSelect=1&multiple=1` in a valid selection context displays the existing eight fabric references, native View Fabric Details disclosures, Select This Fabric actions, one shared colour selector and a concise selection confirmation. Continue to Quotation uses the existing `/request/` route. Standalone `/guides/fabrics/` remains a useful guide without quotation controls or a required selection session.
5. `/request/?multiple=1` presents one compact design summary, one read-only fabric/colour summary with an Edit Fabric Preference link, required contacts/address/deadline, optional email/requirements, existing consent, **Review Quotation Request**, then the existing explicit review and Submit Quotation Request.

No new quotation form, provider, upload, payment or accepted-order promise was introduced. All five men's categories (including Kaunda and Tuxedos & Formalwear) and four women's categories use the same system; mixed collections remain supported.

## Shared preference and preserved data

The existing selection/session component stores one typed `fabricPreference` alongside each quotation snapshot: `choice`, `fabricRef`, `colour`, `colourDescription`. Validated `sharedFabric` URL snapshots preserve it on existing routes, refresh and fresh-browser restoration without customer contact details in URLs. Each quotation flow remains isolated from other flows and fresh browsing. The existing120-second browsing expiry, closed-session handoff and stale-history protections remain intact.

Existing row-level fabric keys are a compatibility projection for new shared requests, not separate customer decisions. The receiving endpoint validates the authoritative optional top-level shared object, reconstructs labels from approved catalogue/palette records and checks every photograph/design/project/quantity. It supports earlier request formats without the shared object using their existing per-design rules. Mixed enquiries can request one catalogue fabric without incorrectly enforcing the legacy first-design audience constraint; professional suitability is still assessed for each garment.

All original design identities, exact photograph URLs, individual quantities and total garments survive. New backend tests cover10mixed and28-design payloads; end-to-end tests preserve10designs/13garments in a complete mocked submission. Required contact/deadline/consent validation,30KB payload limit, allowlists, provider failure handling and positive-response acknowledgement remain enforced. Provider acceptance is not business inbox receipt, production acceptance or payment confirmation.

See [receiving-system contract](SHARED_FABRIC_BACKEND_2026-11-13.md) and [fictional complete enquiry example](SHARED_FABRIC_EXAMPLE_ENQUIRY_2026-11-13.json).

## Fabric Guide and verified information

The eight approved names, photos, categories and Tier / Quality assignments remain unchanged: men's Super1, Wool2, Polyester3, Cotton/Dubai4; women's Americano1, Star2, Polyester3, Cotton4. Cards show image/name/tier/short reference description plus expandable details. No new internet photographs, garment examples or fabric inventory were published.

Removed from the guide: own-fabric service button, per-card suit-price links, lengthy suit/package/surcharge text, Express/children's promotion paragraphs and unrelated enquiry instructions. Those approved business facts remain on their existing service/FAQ/Terms pages. Measurement rendering and other guide helpers remain unchanged.

Exact company fibre composition, weight, texture, performance, care and fabric-specific colour stock are not verified. Every reference makes this limitation clear without inventing specifications. Original OpenStax/Rice University publisher sources support two short general educational facts: cotton's relationship to cellulose and polyesters as polymers usable for clothing fibres. Four cotton/polyester entries show these facts separately from company specifications. No percentage, care, durability or breathability claim is inferred for Mr Sewing fabrics. The [research record](FABRIC_FACTS_RESEARCH_2026-11-13.md) identifies inspected immutable sources and separately records inaccessible FTC originals; unread documents are not treated as checked.

## Colour interface

A central [palette](SHARED_FABRIC_COLOUR_PALETTE_2026-11-13.md), sourced from `_data/fabric-colours.json`, contains22 owner-approved named colour preferences plus Other. HEX values are illustrative; none promises stock or an exact physical shade. Visual swatches are30px, with labelled44px-or-larger native input targets, visible selected indication, keyboard arrows and screen-reader names. One colour is active. Other accepts a short validated1–80character description; controls, HTML, URLs and incompatible stale values are rejected server-side.

The colour selector and confirmation explicitly state that actual shade, suitability and availability need confirmation. Customers can change their fabric/colour before quotation and through the existing edit route without losing selected designs or contact draft fields.

## Layout, preservation and SEO

Compact cards and disclosures reduce repeated forms and paragraphs. Breadcrumbs keep their existing hierarchy/destinations with scoped no-underline styling; heading contrast and tap targets were checked and improved. Header, footer, homepage, Shop, existing OFFER messages/75-second motion, images, prices, benefits, promotions, payment/delivery rules, FAQ/Terms and unrelated service forms are preserved.

Existing titles, descriptions, canonicals, structured data, image identity/alt information, internal routes, sitemap and robots/staging noindex are preserved. The R47 square favicon and real404 repairs remain intact. Shared asset cache versions and validated selection/palette data refresh where needed; there is no unrelated page redesign or production SEO change.

## Tests completed

- Full build and generated-output checks; JavaScript/Python syntax; diff validation.
- Shared preference backend tests:22colours+Other;10/28designs; exact identities/photographs/quantities; mixed collections; malformed/stale preferences; required data/consent; size and provider failures; backwards-compatible legacy requests.
- Local Cloudflare Pages worker compiles with the new colour module;18 GET-only route/resource checks pass, including real404 for an unknown path and405 for GET on the POST-only selected endpoint. Existing50redirect/twoheader rules parse; no actual submission was made.
- Existing selected-suit/photo/multi-design server regressions and16ordinary/4tuxedo price/benefit/FAQ/Fabric Guide consistency checks.
- Browser scenariosA–H at **320,360,375,390,430,768,1024,1440px**: choose fabric/Navy, advice, own fabric,10mixed designs/13garments, Other validation, edit/contact persistence, required fields/consent, review, provider failure/retry/mocked success, standalone guide and unrelated service forms.
- Keyboard navigation, labelled swatches/tap areas, no horizontal overflow, image decoding, mobile navigation and scoped axe checks. A low-contrast summary heading found during QA was corrected in both preference/guide contexts.
- Existing lifecycle regression adapted only for the intentional shared controls: exact120000ms,60-second return/121-second expiry, Back/Forward/BFCache, stale URLs, nine categories, independent quotation flows and current-page operation under denied/quota-limited storage. Quotation photographs/quantities/shared preference remain preserved.
- Static preservation guards audit **294 existing HTML pages** and **559 protected files**, allowing only the approved fabric/quote presentation, shared payload/source data and asset versions. Homepage, unrelated service content, commercial data, existing images and R47 technical protections remain intact. Existing measurement helper tail is byte-identical.
- Mandatory SEO/sitemap audits pass for64canonical routes, valid structured data syntax, unique metadata, working local links and staged noindex source rules. No Google ranking/indexing outcome or external rich-result certification is claimed.

Evidence lives in `/workspace/review/shared-fabric-journey-2026-11-13/`: browser.json, preservation.json, seo-final.json, provider-example.json and quote-ui-smoke.json. Screenshots at390/1440 were inspected. All external messages and enquiry submissions were mocked.

## Deployment and remaining limits

The final owner report supplies the exact staging commit and Cloudflare deployment result/preview after the actual release check. A successful Git push is not treated as proof of deployment or rendered access.

- No new company fabric specifications, additional approved photos or confirmed per-fabric colour-stock records were available; none was fabricated. Existing eight reference photographs are preserved.
- Without browser persistence, immediate validated URL transport works but persisted cross-navigation expiration guarantees cannot be established. No fingerprinting fallback was introduced.
- Native app/WhatsApp delivery and provider inbox receipt were not tested or claimed; mocks protect customers.
- Direct production/Pages preview access has previously been blocked by the managed proxy. Attempt the new preview and distinguish provider success from actual rendered verification.
- Special Tailoring, Alterations, Garment Care, Mobile, VIP, Measurements and the separate production SEO investigation receive no unrelated edits. Main/production remain unchanged; stop for owner review after staging.

[Exact changed-file list](SHARED_FABRIC_JOURNEY_FILES_2026-11-13.txt).
