# R36 final Custom Tailoring staging refinement — 12 November 2026

## Scope and source verification

Baseline09fe4f70cc1c06a663c6ab4270fc8939baa1c587 on verified staging branchphase1/customer-journey-repairs. Production/main4d972f29417fa60366ebdb6348e1599208f6ae08 remains protected. Source: latest explicit owner final-refinement task, current R35 reference/master/matrix/unresolved/page-map, approved ordinary/tuxedo data, fabric reference catalogue and R8Tier1label decision. Original company handbooks remain inaccessible, not claimed inspected. This is a focused revision of the existing design, not a new page/journey.

## Implemented

- Fixed gold OFFER label at left; only the approved family-discount message moves right-to-left. No Pause button, moving-text underline or crowded announcement border. No undefined new-customer promotion. Message/link live separately in _data/custom-tailoring-page.json; label, layout and animation remain in reusable templates.38slinear loop; clipping limited to message window, no overlap with label. Hover/focus stop, Escape and touch stop, static reduced-motion/no-JavaScript fallback. Native keyboard-accessible offer link goes to actual children's section.
- Same hero photograph, heading, layout, men/women buttons and destinations. Shorter introductory sentence and locally removed breadcrumb underline. All four extra section shortcuts removed; actual information remains.
- Same three black/gold pricing-table design. Latest owner's men ordinary page prices: Tier1two600,000/three800,000; Tier2two400,000/three550,000; Tier3two300,000/three400,000; Tier4two250,000/three300,000RWF. Women and tuxedo values unchanged. Scoped override prevents unrelated public-route changes. Existing fabric labels displayed without composition/performance/availability guarantees; Tier1exact approvedSuper/Quality1, Tier2Wool, Tier3Polyester, Tier4Cotton/Dubai. Women's existing reference labels retained; no tuxedo material invented.
- Request Your Quotation immediately after prices opens existing /request/?general=1, which adds its normal context parameters. No new form or booking system.
- Prominent child50%message retained; all R35automatic under12conditions and400k+200k+200k=800kexample remain accessible in a native disclosure. Each eligible child, alltiers/qualities, at leastone normal-priceadult, child-onlynormalcorrespondingprice. No discretionary approval condition.
- Two70%AdvancePayment/30%FinalBalancecards. Domesticbalance timing before finalcleaning/delivery remains explicit. International100%, verifiedfunds/screenshots/PINs/officialorderrequirements remain in accessible details. Standard/Express35%cards with individually confirmed dates; source-backed1–3week/2–3dayestimates, feasibility/capacity, afterhours25/additive60/overnightquotation conditions retained in details.
- Approved standard-package inclusions: initial standard cleaning, branded hanger/protective cover, initialKigalidelivery. Explicit tuxedo quotation distinction. Compact fabric/design, measurements/fitting/garment scope, collection/delivery/shipping and correction disclosures; duplicate long sections removed without dropping conditions.
- Large bottom Explore Men’s Suits / Explore Women’s Suits / Visit the Shop buttons, before original footer, use existing /mensuits/,/womensuits/,/shop/ routes.

## Preservation

Exact header/footer markup, hero photograph, page title/meta/canonical/structured data are identical to R35. Global JS/CSS/form/WhatsApp/contacts untouched. Other tracked page outputs, homepage/Shop/FAQ/Terms/Refund/Privacy and global price/fabric/policy JSON unchanged. Regenerated only canonical Custom Tailoring and six redirect-alias files for service-cmt/service-sketches/service-standard, which already point to that same page. No production configuration or branch changes performed.

The latest men's amounts and family offer are deliberately scoped to this page. Other FAQ/Terms/Fabric Guide price and child-offer text still uses its previous version under the owner's explicit unrelated-page restriction. A separately authorised consistency update is needed before broader publication. No automated quotation price calculation is activated.

## Tests actually completed

PASS full website build and generated-output parity; Python/JS syntax; git diff --check; approved policy/source-link/sitemap tests;27selected-photo mappings and multi-design server validation with mocked provider.

PASS Chromium widths320/360/375/390/430/768/1024/1440: exact20prices/captions/RWF/rowlabels, no cell/page overflow, all native disclosures, familyconditions/example, two paymentcards, fixedOFFER/nooverlap/RTL/noPause/no underline, mobilemenu and eight main-content Axe scans. Separate announcement accessibility scan and normal screenshots320/390/1440. Hero/bottom links and quotation CTA tested at390and1440. Correct target after announcement link, touch/Escape/focus/hover stops and reducedmotion; no-JavaScript static announcement and native keyboard disclosure. Existing no-JavaScript header remains unchanged. No physical-device/Safari claim.

PASS existing end-to-end selected-design/fabric/quotation regression on updated local build: add/remove/qty/refresh/contact draft, own/advice/men/women fabric choices and round-trip, real photograph links, failurepreservation/positive-provider acknowledgement; sevenwidth shared-page and accessibility checks. No messages, payments or real inbox tests.

Browser test initially assumed an exact query string for quotation; corrected to verify route/general=1 because the existing form legitimately adds preserved context. Screenshots use instant scroll-to-top to avoid full-page sticky-header capture artefacts; no header redesign was made.

## Staging deployment verification

Push only HEAD:phase1/customer-journey-repairs. Exact commit, Cloudflare check and generated preview URL are recorded in the final delivery after push. Direct actual staging browser access must be attempted and distinguished from provider deployment success. Managed network policy has previously blocked pages.dev with CONNECT403; no successful rendered deployed-site claim without access. Verify main remains4d972f2 after deployment. Owner review on staging only; no production release requested.
