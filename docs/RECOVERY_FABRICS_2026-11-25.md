# Fabric Guide recovery — 25 November 2026

Implementation branch: `phase1/customer-journey-repairs`. Initial recovered staging tip: `0acf34dc9c606c0fe283d48177c39ebc7a92b20f`. No Main or production edits/deployment.

## Evidence and scope

The latest owner recovery instruction confirms the seven-collection, text-first guide. Existing approved implementations were found in `291a1567` (collection guide) and `b4210fe2` (remove fabric photographs and simulated previews). Current staging already had all seven collection routes and the correct 26 style names, 17 pattern options and 50 colour preferences. Those implementations are retained rather than replaced by the older audience/tier cards.

The active customer-reference snapshot, R59–R67 service instructions and existing source/template/request implementations were inspected. Historical audience/tier assignments remain supported for existing request formats; Premium/Standard collection groups do not assign a selling tier or price to new styles.

## Confirmed problems and repairs

1. `customer_guides.fabric_guide()` switched selected-design customers back to a hidden legacy eight-reference guide. It now keeps the same text-first seven-collection guide for all visitors.
2. New collection-detail pages sent an unstructured fabric string to the generic enquiry route. Selected suits could lose their design quotation journey. Collection navigation now carries the existing quotation flow and exact selected photographs/quantities; its action returns to the existing selected-suit quotation form.
3. Pattern selection was not part of the structured selected-suit preference. The existing shared preference now accepts an optional canonical pattern ID, preserves it in browser/query/quotation/recovery state, displays its approved name in summaries and review, and includes it in Express enquiry text and the existing submission payload.
4. The backend now reconstructs collection, style and pattern names from the same approved catalogue. Unknown IDs and invalid combinations are rejected before the mocked provider. It does not trust customer-supplied collection labels or infer prices/stock/composition.
5. The current detail templates lacked an explicit care consideration. A single conservative notice asks customers to confirm care for the actual material and follow the confirmed finished-garment label. It does not invent washing or dry-cleaning instructions.
6. Ordinary selection browsing now includes the actual Universal Showroom `/collections/` and its `/showroom/` compatibility entry. This keeps the same existing browsing session; its expiry and closed-quotation rules remain unchanged.

## Authoritative source map

- `_data/fabric-collections.json`: current seven collection IDs/groups, 26 style names, 17 patterns, conservative care notice, and clearly marked owner-reported supplier evidence.
- `_data/fabric-colours.json`: the existing 50 illustrative colour preferences. Colours are not inventory.
- `scripts/fabric_collections.py`: validated public/request projection; validates the existing editorial templates against the catalogue, with no new selling tier.
- `_templates/fabric-showroom-{super,americano,wool,star,linen,polyester,cotton}.html`: approved general characteristics, texture, climate and use descriptions and their existing presentation. Selectable labels and embedded data are checked against the central catalogue during generation; update the relevant verified editorial explanation if a style is substantively revised.
- `_templates/fabric-showroom.js`: one standalone/selected-enquiry controller; no third-party image generation or additional enquiry form.
- `scripts/customer_guides.py`, `scripts/customer_site.py`, `scripts/site_seo.py`: generate the same guide and shared allowlists for pages, browser state and server validation.
- `_templates/shared-fabric.js`, `fabric-journey.js`, `design-selections.js`, `selection-session.js`: existing shared preference and photograph-selection system; optional pattern extends, rather than replaces, supported request formats.
- `_templates/selected-suit-quote.js`, `quotation-arrangements.js`, `express-enquiry.js`: concise fabric/pattern/colour summary and existing review/contact/recovery behavior.
- `functions/_lib/selected-design-handler.js`: validates canonical styles/patterns and reconstructs readable provider fields.
- Generated projections remain `scripts/edge/request-data.mjs`, `functions/_lib/fabric-preferences.js`, `/assets/design-selections.js`, `/assets/fabric-showroom.js` and the generated guide/quotation pages. Edit source, rebuild, then verify; do not patch only generated HTML.

## Collections and routes

Premium: Super, Americano, Wool, Star, Linen. Standard: Polyester, Cotton.

Main guide: `/guides/fabrics/`. Detail routes: `/guides/fabrics/super/`, `/americano/`, `/wool/`, `/star/`, `/linen/`, `/polyester/`, `/cotton/` under that same base.

Selected enquiry: Selected Designs → `/services/custom-tailoring/fabric/?multiple=1` → `/guides/fabrics/?fabricSelect=1&multiple=1` plus existing flow context → collection/style/pattern/colour → `/request/?multiple=1` plus preserved context → existing review/submission. Advice and own-fabric preferences continue directly to quotation. Standalone browsing keeps its existing general quotation alternative.

## Verified versus unverified textile information

The 26 names and general explanations are approved reference choices. Exact fibre percentages, origin, fabric weight, care instructions and stock are not established by names such as Super, Americano, Star or Dubai.

The current instruction reports Jindeli113096 with T/R/SP; Lycra Breezer; Madagascar208 labelled100%Polyester/Made in India; and Fashion First polyester/Made in India. No corresponding original supplier image/document was located in this checkout's relevant sources. These reports are preserved internally as owner-reported evidence only. No percentages are invented, no commercial collection is assigned, and no new stock item is published.

## Validation

PASS:

- Python syntax for modified source modules and JavaScript syntax checks.
- Text-first source inspection: seven collections, 26 styles, 17 patterns, no fabric photographs/canvas, and care guidance.
- `node tests/recovery_fabric_validation.mjs`: all26styles, all17patterns,50colour records; mixed men's/women's exact photographs and quantities; canonical server labels; invalid IDs rejected before provider; old four-part and new five-part preference round trips; no invented tier.
- `node tests/shared-fabric-validation.mjs`: existing shared preference/security/legacy and payload regressions.
- `node tests/quotation-completion-validation.mjs`: existing ordinary/Special customer, measurements, delivery, deadline and submission validator regressions.
- `node tests/multi-design-validation.mjs`: existing multi-design reconstruction and security checks.

PASS: `node tests/recovery-fabric-browser.cjs` at320,390,768,1440px. Actual local Chromium visited all7collectionpages, verified17patterns/50colourcontrols/noimages/nooverflow; followed real Kaunda+women selected-design controls into the new guide, selected Wool/Tweed/Herringbone/Navy, preserved exact photographs/quantities into quotation, and returned through Edit Fabric Preference, changed Navy to Burgundy through the colour-group disclosure, and retained the previously entered fictional full name, all exact design photographs and quantities when returning to quotation. Evidence and four screenshots: `/workspace/recovery/2026-11-25/fabric-browser/`. No real submissions/messages; external traffic was blocked. The first run detected a stale generated care notice and stopped; the scoped generation was rerun. A subsequent browser launch was blocked by an automatic approval-review usage failure, not an unsafe-action finding. Do not report that blocked invocation as a pass. The fresh browser run subsequently executed and passed; the blocked attempt is not counted as a pass. Final integrated generation and deployed verification remain the parent recovery task's responsibility.
