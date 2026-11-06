# Main/staging parity repair — 6 November 2026

Owner authorisation: investigate and repair main/live, prioritising phones. Baseline main a2ae98f5d51549e05adee35f809e3f364645ba1a and development 501ccc1643774568ff39a4f452b01164dd9dbd17 have identical trees. The discrepancy is deployment architecture: public GitHub Pages serves static files; staging executes Cloudflare Pages Functions. Successful deployment alone was not proof of equivalent behaviour.

## Corrections

- Static production Shop now generates 21 explicitly approved enquiry displays, 21 product detail routes and six category routes. White storefront, search, filtering, two-column phone grid, detail-only Terms-gated manual WhatsApp and canonical product links are retained. Original catalogue commercial draft status, unknown prices/stock and strict sale gate remain unchanged. Fingerprinted explicit approvals prevent future drafts silently becoming public. No Product/Offer data, checkout or sales claims are generated for these enquiries.
- Public selected-design and referral intake map exact production origins to the existing main-branch Cloudflare runtime. Strict CORS accepts only two public paths, exact production origins and approved methods/headers. Existing design/photo/quantity/consent validation and provider-response checks remain. Private/staff APIs are not routed cross-origin. No credentials or paid services changed.
- Normal phone touch/scroll no longer permanently pauses the three source-driven right-to-left galleries. Escape and OS reduced-motion remain supported. Changed scripts carry cache versions.
- Consent popup paragraph contrast corrected. Shop body has an explicit white-background fallback for browsers lacking :has support.
- Privacy technical descriptions corrected to identify GitHub Pages, Cloudflare validation and Web3Forms; public uploads/private records remain disabled. No new privacy guarantees or commercial rules.

## Verification

PASS — Production build and generated parity; 19 Python regression suites. Public-enquiry gate excludes future/modified unapproved entries and retains original commercial records.

PASS — Plain-static/live-origin Chromium browser tests: 21 products and 147 image decodes across seven widths (320–1440), six category counts/search, all detail routes, detail WhatsApp consent and correct canonical product URL, 19 important public routes without overflow, selected-photo/fabric quote and referral using the production API mapping with actual validators and mocked provider responses.

PASS — Pixel 7 and iPhone 13 Chromium profiles plus desktop: all three galleries move right to left and continue after touch scroll; reduced-motion intentionally disables animation. These are emulations, not physical iOS/Safari tests.

PASS — Consultation regression (24 cases); full V2 and design/service regressions, successful/failed mocked provider responses, exact selected photograph URL, independent service questions, homepage consent focus/keyboard behaviour, seven responsive widths and accessibility scans with no reported violations in tested scopes.

PASS — Static link/resource audit: 61 pages, 3,526 internal references, no missing target. Local actual Wrangler preflight returns 204 with exact origin; malformed intake returns 400 with CORS and useful error. No real customer messages sent.

## Deployment and limits

Rollback preserved remotely: rollback/production-before-parity-repair-2026-11-06 → a2ae98f5d51549e05adee35f809e3f364645ba1a. Restore via reviewed revert/normal deployment; no force/reset required.

Deployment commit and GitHub Pages/Cloudflare checks are recorded after push in the delivery report. Both runtimes must deploy the repair: public static site and existing main.mrsewing-staging.pages.dev intake. Direct requests to public/Cloudflare domains are blocked by this environment proxy; direct live rendering must not be described as verified. Real inbox receipt remains unverified and requires a controlled post-deployment owner-confirmed test. Browser tests mocked submissions and WhatsApp; opening a chat does not send a message. Private storage/staff features remain disabled. No payment, DNS or hosting settings changed.

Screenshots and detailed local evidence: /workspace/artifacts/main-parity and /workspace/review/main-parity. Modified files are recorded in the repair commit; many HTML changes are generated script-version/API-loader references, not page redesigns.
