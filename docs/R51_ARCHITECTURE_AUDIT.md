# R51 — Architecture audit and safe implementation plan

18November2026. Staging branch `phase1/customer-journey-repairs`, baseline `b2b8946882929da4ce7e0e01de4ba1511eed818a`. Remote main/staging both matched that baseline at audit. Tracked tree clean; existing `.wrangler/` and Python caches are tooling, not source changes. This new task does not authorize main/production changes.

## Actual architecture

- `scripts/build_site.py` runs14Python builders. Source JSON/templates/Python produce committed HTML and browser assets; edit sources, rebuild generated output.
- Shared modern navigation comes from `_templates/homepage-header.html` and `_templates/homepage-footer.html` through `scripts/custom_tailoring.py:component` and `scripts/shared_components.py`. Root `header.html`/`footer.html` and `_templates/shared/` are older parallel copies.
- Homepage: `_templates/homepage.html`, `_templates/homepage-sections.html`, `scripts/build_homepage.py`; current photo projections in `scripts/homepage_galleries.py` already reuse approved collection/project sources.
- Services/forms: `_data/customer-release.json`, `scripts/customer_site.py`, existing `_templates/` selection, fabric, quotation, consent and draft modules. Existing Pages Functions receive validated enquiries; private intake remains disabled.
- Rules: `_data/customer-policy-facts.json` with `scripts/customer_policies.py` and `scripts/customer_information.py`. `_data/customer-information.json` retains independently written payment/delivery text. Numeric form/server guidance is also duplicated.
- FAQ: `_data/customer-faqs.json`, `scripts/faq_help.py`, existing interface and search/schema builders;14topics/123questions at baseline.
- Active Terms: `_data/customer-release.json` rendered by `customer_site.information()`. `_data/policy-pages.json` supplies historical anchors. `build_customer_information.py` creates legacy policy output and then replaces it with modern output; avoid mistaking the old template for the authoritative body.
- Approved ordinary/tuxedo prices: `_data/suit-package-prices.json`, `_data/tuxedo-package-prices.json`, `scripts/suit_pricing.py`. Men's Tier3 is verified300,000/400,000RWF, source decision12November2026. Preserve amounts and history, change public presentation separately.
- Media: `_data/collection-designs.json`, image inventory, permission/category records, `_data/customer-projects.json`; effective gate is `scripts/build_collections.py:load()`, not raw `published:true`.
- Shop: `_data/shop-products.json`, `_data/shop-public-enquiries.json`, commerce builders/runtime.26enquiry-only displays, zero sale-published products. Price/stock/checkout gates remain authoritative.
- SEO: `_data/page-seo.json`, `_data/public-page-seo.json`, `_data/seo-search-intent.json`, `scripts/site_seo.py`, `scripts/build_public_routes.py`;64canonical pages at baseline.

## Verified duplication and risks

1. Shared contact/location/hours have literal copies alongside settings. Several builders produce overlapping outputs.
2. Payment/transport/service-fee facts exist in policy JSON, information JSON, service rendering, frontend and server code. Reuse authoritative records with explicit service scope rather than applying suit rules to every service.
3. Raw151design records include124published flags, but only28pass current permission gates. Publishing raw flags would leak103held references. The28eligible photos comprise21reference photographs and7genuine-work photos associated with5approved projects.
4. Inventory includes402image files and7MP4s; no broken referenced file found. Three exact-duplicate groups were found. Keep originals; hashes/manifests support recovery without physical duplication.
5. No verified per-video rights record and no approved Terms PDF exist. Support video/document capabilities, but do not invent approvals or activate a draft. Existing Terms access/consents must remain available until a real approved document replaces the fallback.
6. PDFs committed to a static public tree may be directly accessible regardless of registry status. Keep unapproved PDFs outside the deployed repository; publication tooling must validate before copying approved documents into public paths.
7. Public service-price emitters include Python pricing/service/policy builders, FAQ literals/search/schema and dynamic quotation JS. Preserve internal prices, benefit eligibility, existing individual quotations and Shop pricing; do not use blind number replacement.
8. Existing gallery URLs carry SEO and selected-design context. Make Showroom primary through navigation/filter links; retain old routes/detail identities rather than destructively removing them.
9. `_data` and a public Git repository are not private storage. Add no confidential costs or customer records.

## Safe plan and ownership

A. Record latest scope and authoritative ownership; create `docs/WEBSITE_SOURCE_MAP.md` using verified paths. Avoid framework migration/bulk renaming.

B. Centralize shared fact consumption and component rendering through small adapters, preserving original approved records and service-specific exceptions.

C. Add a version/approval-gated Terms document registry, viewer, download/open/fallback and repository replacement workflow. Existing approved online Terms remain the transitional fallback until the approved PDF is provided. The active approved PDF will replace that full HTML rendering; no parallel independently editable full document.

D. Derive a reusable media index from current effective gates, plus filename/hash recovery inventory and curated feature settings. No recovered image/video is automatically published.

E. Add `/showroom/` with audience/type/style/classification filters and original-filename lookup. Hide empty categories; reuse exact existing detail, selection, fabric and quotation paths. Keep legacy URLs compatible and document any later migration decision.

F. Add two selected-media cards and one larger feature below the homepage header, reusing approved images; support but do not activate unapproved videos. Preserve existing homepage beneath.

G. Use quotation-first service presentation centrally, retain internal prices and Shop behavior, improve focused Custom Tailoring content and link shared explanations to existing FAQ/policies. Public surcharge-rate visibility is being clarified; payment obligations and benefit eligibility remain scoped facts.

H. Run build synchronization, source/price/media/document invariants, SEO/sitemap/link tests, existing backend/selection/quotation regressions and mobile/desktop browser checks. Test new publication behavior with temporary fixtures only. Push/deploy staging only and re-read remote main to prove no production mutation.

## Current limitations and owner review items

- Approved official Terms PDF/version/effective date is not supplied. Viewer readiness can be completed; activating official PDF authority remains pending the document and approval.
- Seven videos and held/recovered media need explicit publication/classification review before use. Approved photographs can provide all initial showcase fallbacks.
- No verified stock/price/checkout approvals exist for Shop sale products. Preserve enquiry-only behavior; do not activate direct purchase.
- Original named company handbooks remain inaccessible; use inspected repository references and explicit current owner decisions without claiming exhaustive source coverage.
- Existing execution proxy blocks staging/live browser access; local rendering and provider deployment status must be reported separately from actual deployed verification.
- Removing old public routes, physical files or policy history is not necessary here and will not occur without a separate concrete approval.
