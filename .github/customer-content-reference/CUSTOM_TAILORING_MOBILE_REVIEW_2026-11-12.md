# R35 Custom Tailoring mobile staging review — 12 November 2026

## Scope and authority

Owner task12November2026: staging only, Custom Tailoring only, mobile first. Branch phase1/customer-journey-repairs is verified against its actual Cloudflare check (9fe41cd/run130695643572) and current remote head4d972f2. No main push/merge, production deployment or environment/settings changes are authorised or performed. Main baseline4d972f29417fa60366ebdb6348e1599208f6ae08. Original company handbooks remain unavailable; repository approved prices/policy references and latest explicit owner instructions were inspected.

## Completed

- Three semantic tables for men's ordinary suits, women's ordinary suits and men's tuxedos, driven by unchanged approved price JSON. All20amounts exactly match owner supplied values, including men's Tier4two/threepiece250,000/250,000. No price conflicts. Captions, Tier / Quality row headings and RWF column headers; complete-garment starting-price and final-quotation explanation retained.
- Owner-approved automatic50%discount on each eligible under12child's suit with at least one normal-price adult suit in the same order; all tiers/qualities. Child-only suits use corresponding normal schedule. Example400,000+200,000+200,000=800,000RWF excluding separately quoted charges. No discretionary/individually negotiated condition on this page.
- Single payment section with separate domestic70/30, international100% and verification cards. Balance timing before final cleaning/delivery, full payment before release, order-specific shipping, verified funds/screenshots/PIN protection and official order requirements explained without duplicate paragraphs or unrelated service-payment clauses.
- Existing service/fabric/design/fitting/turnaround/surcharge/delivery information and enquiry destinations preserved. Pricing/children/payments/details jump navigation added.
- Reusable, compact black/gold announcement activated only on this page, immediately after header. Exact neutral new-customer-offer placeholder links to a real offer-information section and existing consultation journey. No invented promotion. Child discount kept distinct. Gentle38sright-to-left seamless duplicate track, pause/resume, hover/focus/Escape, reduced-motion and no-JavaScript static fallback. No new dependencies, tracking or requests.
- All page-local anchors include the canonical page path to work correctly with the site's root base URL. Testing found and corrected the initial bare-hash link behaviour before staging deployment.

## Preservation

Only generated /services/custom-tailoring/index.html and its three pre-existing redirect aliases (service-cmt, service-sketches, service-standard; root and directory variants) changed. All unrelated tracked page outputs, homepage, Shop, FAQ, Terms, Refund, Privacy, global scripts/styles, source price JSON and global policy facts remain byte-identical to4d972f2. Page-specific supporting builder/templates, relevant tests and mandatory source-reference records are included. The new child policy is intentionally scoped to this page under the owner's route restriction; FAQ/Terms retain their existing wording and need a separate authorised consistency update before any broader policy rollout.

## Tests actually completed

PASS normal full website build and parity check; Python/JS syntax checks; git diff --check. PASS policy arithmetic/source-link tests,55-route sitemap eligibility,27selected-photo mappings and multi-design server validation with mocked provider. Updated existing price assertion to read table cells instead of expecting RWF repeated after each amount; RWF headers/exact20prices are tested independently.

PASS Chromium browser widths320,360,375,390,768,1024,1440: all prices/headers readable with no cell/page overflow, child conditions/example and single payment copy correct, mobile navigation/gallery links, seven main-content Axe checks, no page script errors. PASS announcementRTL/hoverpause/buttonpause+resume/Escape/focus/offer link/reducedmotion/noJS fallback and absence on home/FAQ/Shop/Alterations. Screenshots at320,390,1440inspected locally. No physical phone/Safari or real messages/payments tested.

PASS existing multi-design end-to-end regression against updated local build: selections/quantities/add/remove/refresh/contact draft, per-design men's/women's fabric browsing and return/cancel/validation, all photograph links in review/provider payload, rejection preserves entries and positive provider response alone acknowledges success; existing7width/sharedFAQ/Shop/About/fabricAxe checks. No email delivery claimed.

## Deployment and remaining verification

Push only HEAD:phase1/customer-journey-repairs. Exact commit/deployment URL and provider status are recorded in final delivery after push. Actual staging browser/mobile verification must be attempted; managed network policy has previously blocked pages.dev with proxyCONNECT403. Do not interpret pipeline success as deployed rendered verification. No production publication requested. Owner reviews staging only.
