# Loyalty, Referral & Shop — Staging Implementation Report

Date: 6 November 2026. Branch: `phase1/customer-journey-repairs`.
Baseline preserved: `09be5c7d52cde29fdd4d4b5d53fa0454d2c7502a`.

## Pages completed

- `/loyalty-program/`: 3% from second separate qualifying suit purchase, first-order multi-suit distinction, men/women suit scope, exclusions, highest-discount rule, FAQs, existing suit galleries and booking enquiry.
- `/referral-program/`: customer and non-customer participation, 6,000 RWF/qualifying suit first order, referred customer 2%, no repeat commission, completion/full-payment/handover prerequisites, before-first-deposit/one-referrer/no-self requirements supplied by owner. Accessible participation form, review/edit, unchecked consent, provider-confirmed acknowledgement, preserved inputs/errors/retry. No automatic approval, codes or payouts.
- `/shop/`: professional mobile catalogue with categories, search, availability filter, price/name sorting and truthful empty state. **There are zero verified merchandise products, so no fictional merchandise or live product detail pages were published.**
- `/shop/cart/`: anonymous persistent cart, quantity changes/removal, contact/delivery and payment preference, review and purchase-request submission. Empty until stock products exist. Cart stores product/variation IDs and quantities only, not customer or payment credentials.
- `/shop/{slug}/`: build-time structure for approved published products, multiple photographs, optional responsive sources, specifications/care, stable links, size/colour combinations, quantities and exact three availability behaviours. Product pages were tested with synthetic fixtures outside the deployment root; none are real products.

Homepage programme headings now link to the new pages. Shared Shop button has the active Online Shop label and existing `/shop/` destination. No homepage redesign. A preservation comparison verified 236 existing HTML files changed only for this shared accessibility label; full homepage comparison permits only the two programme links and that label. Homepage JavaScript and consultation implementation/provider source remain unchanged.

## Policy authority and holds

Latest owner task “Loyalty, Referral and E-commerce Shop”, §§3–4,6–9,12–14 is the directly inspected approval. Existing current customer reference C38/C39/C40/C43 supports scoped suit benefits and non-stacking. R13 is recorded in version `2026-11-06-06`, matrix, unresolved register, page map, communication library and manifest; earlier snapshots remain preserved.

Original `Mr_Sewing_Complete_Approved_Commercial_Policy_and_Open_Decisions_2026-11-01.md` and latest approved referral operating reference remain inaccessible. The operating reference's exact filename was not supplied. **The seven-calendar-day payout promise is withheld pending verification of applicable original terms**, rather than presented as a verified final entitlement. Owner-supplied attribution prerequisites are explained, with human confirmation before participation. No historical discount ladder, points, unrelated-service rewards or automatic commissions added.

Real merchandise data, approved image rights, current inventory/variations, prices/specifications/care are missing. The live catalogue is empty as expressly allowed by the task. Shop-specific fulfilment, delivery charges, returns/cancellation/customer rights and privacy operational review require owner clearance before a real customer launch. Existing general policies are linked, not rewritten. Cryptocurrency remains disabled and server-rejected pending legal/operational approval. Bank Transfer/Mobile Money are preferences only; no accounts, numbers, wallets or payment instructions are published.

## Catalogue and purchasing architecture

`_data/shop-products.json` is the single source. Blank `_data/shop-product-template.json` and `docs/shop-catalogue.md` document the Git workflow. Published records require approval and photograph-permission evidence, valid unique IDs/slugs, metadata, exact availability, approved stock prices and consistent variation quantities. Draft/archived records do not publish. Published changes generate listing/detail/server catalogue in one build; withdrawal removes generated detail pages. Stable slugs/IDs should not be changed silently.

Exactly **Available in Stock**, **Available on Orders**, **Out of Stock**. Stock products allow cart quantities up to recorded variation stock. On-order products have no fixed price and open a dedicated accessible quotation dialog, not consultation. Out-of-stock products retain information but cannot be purchased. Prices are per product; different-price variants should be separate approved SKU records until variable pricing is separately implemented.

The cart persists public IDs/quantities through navigation/refresh when browser storage is available. Stale/unavailable records are removed and excessive quantities adjusted with a notice. Purchases/quotes preserve product and variation context through review. Cart requests do not reserve or deduct inventory. Final availability, delivery charges and amount require business confirmation.

`functions/api/shop-request.js` validates requests through `functions/_lib/shop-handler.js` against generated authoritative catalogue data, then reuses the existing free Web3Forms access-key configuration and recipient. Customer totals, names/prices/URLs for products, subject and routing are not trusted; server reconstructs them. No new provider account/key, paid service, payment gateway, database, upload or staff feature is activated.

Host/origin/method checks, JSON schema and streamed size limits, honeypot, quantity/status/variation checks, explicit consent, provider timeout and positive HTTP/JSON acceptance are enforced. Response is no-store/noindex and never exposes stored customer records. Frontend prevents duplicate pending sends, requires review, handles failure/retry and warns that timeout may already have delivered. Without JavaScript, submission buttons remain disabled and POST fallback prevents customer fields being placed in URL queries. Public email intake is not authentication or an internal record system; provider abuse handling/domain restrictions still need live verification.

## SEO

Unique titles/descriptions/H1, production self-canonicals, breadcrumbs and social metadata for the new pages. Published products generate their approved sharing image and Product schema; only verified prices/statuses enter Offer data. No fabricated ratings/reviews, volumes, ranking claims or native social-store integration.

Sitemap has 17 eligible public pages with the empty catalogue: previous 14 plus Loyalty, Referral and Shop. Approved real published products become eligible dynamically. Cart and request endpoints remain noindex; staging host restrictions are unchanged. No production sitemap submission.

## Tests and evidence

| Check | Result | Scope |
|---|---|---|
| Full production generation and `--check` parity | PASS | Normal existing Python build pipeline |
| Existing Python suites | PASS | All 17 suites; old deferral assertions updated only for R13-authorised links/routes |
| New catalogue tests | PASS | Publication/price/image/stock gates, exact statuses, isolated single-source update/withdrawal, schema/canonical, unchanged homepage/booking |
| Server validation | PASS | Tampered totals ignored; bad IDs/variants/quantities, duplicate lines, unavailable stock, invalid consent/payment rejected; positive-only acknowledgement; provider/network/malformed/config/origin/host/method/body-size failures |
| Exact deployed entrypoint import | PASS | Generated empty catalogue/provider reuse, mocked provider only |
| Browser customer flows | PASS | Chromium, synthetic unpublished merchandise only; listing/filter/sort, stock statuses, cart persistence/edit/remove/stale data, quote/dialog Escape/focus, referral review/edit, provider failures/retry, pending duplicate protection, actual mobile/desktop homepage links |
| Responsive checks | PASS | 320/360/390/430/768/1024/1440; product fixtures additionally 320/390/768/1440; no horizontal overflow |
| Automated accessibility | PASS | Eight WCAG 2.2 AA-tag Axe scans: three real new pages at mobile/desktop plus fixture cart/quote form states; keyboard/dialog tests |
| Booking regression | PASS | 24 Yes/No/link/service/review/provider cases and four widths; no consultation WhatsApp/upload regression |
| Homepage regression | PASS | Seven widths, source-driven galleries/motion/reduced motion, support mock outcomes, same-page Terms, booking link and two existing Axe scans |
| No-JavaScript form fallback | PASS | Disabled request controls, POST method, explanatory notice |
| Actual email/inbox receipt | NOT TESTED | All submissions controlled/mocked; no real customer messages sent |
| Physical devices/Safari/Firefox/assistive technology | NOT TESTED | Browser emulation and automated/manual Chromium checks only |
| Direct deployed browser/provider integration | BLOCKED | Managed outbound policy previously rejects staging/provider; final exact-host attempt and GitHub deployment evidence reported separately |

Local Lighthouse simulated-mobile **empty Shop**: performance/accessibility/SEO **100/100/100**, LCP/FCP **1.353s**, TBT **0ms**, CLS **0**, measured transfer **175,775 bytes**. External fonts/CDN blocked, local server only. These are lab observations, not field Core Web Vitals/INP or predictions for a populated catalogue.

Evidence: `/workspace/review/commerce/` logs, fixture-only browser data, Lighthouse JSON, preservation and changed-file list. Screenshots: `/workspace/artifacts/commerce/{loyalty,referral,shop}-{390,1440}.png`. Fixtures stay outside the repository deployment root and are never committed as products.

## Main changed sources

- `scripts/build_commerce.py`, `scripts/shop_catalog.py`, `_templates/commerce.{js,css}`, generated `assets/commerce.{js,css}`.
- `_data/shop-products.json`, `_data/shop-product-template.json`, `_data/shop-generated-pages.json`, `docs/shop-catalogue.md`.
- `functions/api/shop-request.js`, `functions/_lib/shop-handler.js`, generated server runtime catalogue/provider module.
- Build registration and sitemap/SEO integration: `scripts/build_site.py`, `build_completion.py`, `build_public_routes.py`, `site_seo.py`.
- Homepage header/section sources plus normal generated HTML outputs; new Loyalty/Referral/Shop/cart pages and sitemap. Existing generated page bodies otherwise unchanged.
- Three commerce test files and narrowly updated historical preservation/indexing assertions; R13 reference/governance records.

## Review decision

**Ready for owner staging review of the pages and architecture. Not ready for real Shop sales:** merchandise and operational approvals are missing, and real provider/inbox delivery is unverified. Before enabling real customers, review the final staging endpoint, submit controlled enquiries and independently confirm the business inbox; verify spam/provider restrictions. Review original referral payout terms and Shop fulfilment/returns/privacy conditions. No claim of legal compliance or production readiness.

Delivery commit, exact Cloudflare check and preview are supplied in the owner delivery message and external delivery evidence after push. `main`, production, DNS, live credentials and private-feature settings were not changed. Await owner approval.
