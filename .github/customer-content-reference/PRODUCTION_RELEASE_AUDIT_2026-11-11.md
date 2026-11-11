# Production release audit — 11 November 2026

## Authority and scope

Owner explicitly requested an SEO/functionality check followed by merging the reviewed staging release to main. Release baseline 9fe41cdf84b94b1fdd099db2fd2d149f6928741a; previous production/rollback 4fefad3fb5fb1bbb5f5feb3af671035c6cec5628. Preserve the owner's original logo upload and every newer commit. This release includes the reviewed public policy/service information, FAQ Help Centre in black/gold, readable Shop mobile menu, Nexus About hero, approved starting-price clarification and multi-design/fabric quotations. The final R33 theme/fabric change leaves Shop and homepage files untouched relative to R32. Existing approved enquiry-only Shop display restrictions remain.

Reference: current master, matrix, unresolved register and page-map R31–R34; preceding staging links and owner discussion. No newly accessible company originals, no source coverage or legal-compliance guarantee. No newly invented business facts. Existing policy text is the reviewed staged public version; internal proposed clauses remain outside customer pages. No new gateways, accounts/wallets, stock/price invention or private-backend activation.

## SEO and discovery

PASS all 55 sitemap URLs: one H1, unique nonempty title and description, exact production canonical, indexable robots and parseable structured data. All checked local page links/assets exist and images have alternative text. Audit respects each page's base URL. No duplicate titles/descriptions. Sitemap and robots agree on https://mrsewingfashion.com/sitemap.xml; excluded forms/cart/staff/unapproved products remain excluded. Indexable-route parity tests passed. Existing titles use natural, service-specific Kigali/Rwanda and garment terms rather than keyword stuffing. No new rankings, Google submission, rich-result eligibility or indexing promise; no fabricated ratings.

## Functional and mobile checks

- PASS full production build/parity, shared policy consistency, approved surcharge/deposit arithmetic, business identity/hours/schema, sitemap eligibility.
- PASS all 14 FAQ categories/104 accordions, ten practical search queries, empty/clear behaviour, source links, no repeated copy buttons; service/policy responsive layouts at seven widths and accessibility checks.
- PASS multi-design add/remove/quantities, refresh, exact photo/name payloads, preserved contact draft, independent fabric collection round trips, correct men's/women's choices, return without selection, incomplete-choice validation, Continue to Customization and review. Server rejects invalid IDs/photos/projects/fabrics/quantities/duplicates/consent. Provider failure preserves entries; provider success alone acknowledges acceptance.
- PASS production-origin simulation using local release assets on https://mrsewingfashion.com, the actual publicIntake CORS adapter and selected-design handler, with only email provider acceptance/rejection mocked. Browser requests target https://main.mrsewing-staging.pages.dev/api/selected-design-request. No live API/email/inbox test claimed.
- PASS 36 consultation service/method/location combinations, required fields/date/time/consent, edit/service switching, failure preservation, four responsive widths and two accessibility checks. Clock fixed in test to exercise future appointment fixtures.
- PASS Pixel 7/iPhone 13/desktop Chromium profiles: three galleries move right-to-left, continue after touch/scroll, respect reduced motion; mobile menu works. Emulation is not physical-device Safari testing.
- PASS 26 approved Shop enquiry photographs decode, white mobile two-column grid, six category pages, search, local Home return, detail-only WhatsApp action and unchecked Terms gate. No cart navigation or card-level WhatsApp. No messages or payments sent.
- PASS published-only sale catalogue remains empty; exact fingerprint-approved enquiry displays total 26. Future draft excluded and unapproved content change rejected. Five owner photo originals unchanged; proportional variants and protected Moments/fabric/private flag unchanged.
- PASS existing selected-photo (27 mappings), commerce server and exact-origin CORS regressions with mocked provider. Unknown hosts/origins/private paths rejected.

Two historical tests still assumed 21 products or pre-approved price/policy snapshots. Updated these assertions for the five already-approved photographs and R32 price/policy change, retaining explicit future-draft/fingerprint and original-image protections. Current policy/price tests separately verify the approved facts. No customer implementation change was needed during this audit.

## Limitations and release verification

Direct requests to both staging and mrsewingfashion.com were blocked by the managed environment proxy with CONNECT 403 before reaching the websites. This is not evidence that either website returns 403. Local browser/build tests passed; exact-commit GitHub Pages and Cloudflare deployment results must be checked after pushing main. Deployment success is not a live rendered-page verification. Physical mobile browsers, real inbox delivery, Search Console indexing/traffic and field performance are not independently established here.

Merge uses the actual current main as first parent and retains the complete development history. No force push, DNS/hosting-setting change or secret changes. Rollback is available from the previous production commit via a reviewed revert, preserving history. Final deployment URLs, merge SHA and checks are recorded in the delivery report after publication.
