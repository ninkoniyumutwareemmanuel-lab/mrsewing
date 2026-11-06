# Shop staging storefront preview — 6 November 2026

## Implemented

The existing storefront now supports a build-time staging draft display without changing `_data/shop-products.json` or `shop_catalog.load()` publication validation. The 21 existing image candidates are rendered as real product cards with existing search, filters, sorting, category navigation, banner/header/footer and responsive grid. Six provisional categories: men's4, women's4, covers2, hangers7, shirts2, footwear2. Draft cards open permanent-pattern detail previews with proposed name/category/known description/photo and **Draft — Awaiting Approval**. No commercial values, availability labels, options, forms, Product/Offer structured data or purchase buttons are invented for drafts.

The server runtime and browser cart data still contain only validated published products. Draft IDs are rejected by the existing API before any provider request. Preview detail/category pages have noindex and are excluded from sitemap/public-product route generation. Exact three published availability labels are untouched.

## Isolation and build configuration

`shop_preview.enabled()` requires ALL of `CF_PAGES=1`, `CF_PAGES_BRANCH=phase1/customer-journey-repairs`, and an HTTPS Cloudflare preview URL under `mrsewing-staging.pages.dev`. These are build-time checks, not browser hostname hiding. A normal build, main branch, different Pages project or production domain excludes drafts; no additional provider credential or owner configuration was changed. Cloudflare standard Pages variables supply this gate. Generated draft pages are tracked by the existing generated-page manifest for safe withdrawal on a subsequent production/default build. Only production-safe generated output is committed. Temporary `/shop/draft-review/` is removed; no original images/records removed.

## Tests

PASS: all19Python regression suites; full default build and parity checks; preview mode21cards/21details/6categories; no drafts in production output or API runtime; gate mismatch tests; all147 image loads across320/360/390/430/768/1024/1440; mobile two-column grid/no page overflow; category counts/search/direct category navigation; draft details without actions or Product/Offer schema; empty checkout; Axe WCAG-tag scan; no browser exceptions. PASS: actual API rejects draft purchase and quote before provider. PASS: existing published-product fixture browser suite including cart/checkout/quote/referral,7widths and8Axe scans; commerce server validation/provider error suite. All provider responses mocked; no messages or customer data sent.

Existing image audit confirms original assets,21draft records/commercial unknowns,homepage/booking/programmes preserved. No image publication rights are inferred. Prices, sizes/colours, stock, availability, packages and selling conditions require owner verification. Draft descriptions/category/name remain proposed and review-only.

Exact deployment commit/check/URL and direct origin access result are provided after push in the delivery report. A Cloudflare deployment notification does not establish direct storefront verification. Production/main remain protected; stop for owner review.

## Corrective follow-up R17
Owner screenshots establish b69c930 deployed storefront had0products. The build-time gate was not established in actual CI. Added generated server-only28page snapshot and /shop/[[path]] Pages route. Exact staging hostname/project-subdomain gate on the server; production/cart/POST fall through. Default production static files and API remain published-only. Server route tests validate21cards on both staging host types,28routes,5production/foreign host rejections and noindex/no-store. Wrangler actual Functions compilation passes. No claim that owner saw21deployedcards until direct evidence.

R17 actual-runtime evidence: Wrangler4.158.0 compiled the2MB Worker successfully. Local HTTPS Worker with Host mrsewing-staging.pages.dev returned200,21cards andX-Mr-Sewing-Shop-Preview:draft-review. Same Worker with production Host returned0draftcards/static empty catalogue. Chromium tests proxied all site requests through that Worker:147image loads,7widths,6category counts/search,detail/category navigation,no draft actions/schema/checkout,noJSerrors,Axe passed. No live production request or real email made.
