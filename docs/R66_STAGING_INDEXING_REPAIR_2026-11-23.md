# R66 — Staging SEO indexing and canonical consolidation
**Date:** 23 November 2026  
**Scope:** `phase1/customer-journey-repairs` only; no main/live-domain change, customer intake, policy, or paid provider action.

## Problem and verified evidence
- Connected Google Search Console, property `sc-domain:mrsewingfashion.com`: homepage is indexed, while `/services/custom-tailoring/` and `/services/garment-care/` were unknown to Google, and `/services/alterations/`, `/mensuits/`, `/womensuits/` were discovered but not indexed (read-only URL inspections on 23 Nov 2026). These are Google's stored indexing observations, not live fetch tests.
- The production `main` repository contains all five pages, and the staging sitemap lists them with their clean canonical URLs. The generated staging source has one title, description, H1, and `index, follow` per selected service page; HTML alone cannot guarantee indexing.
- Search Console still reports legacy `.html` URLs alongside clean routes; `/about.html` and `/about/` were each reported indexed. The production static frontend is GitHub Pages, which does not interpret Cloudflare Pages `_redirects`. Source-level JavaScript forwarding is not an HTTP 301; it is not an independent crawl test.
- Staging deployment response headers, actual HTTP redirects, browser rendering, live Google indexing, PageSpeed and Core Web Vitals **are not verified** in this environment.

## Implemented staging-only
1. `scripts/site_seo.py` now adds an immediate `<meta http-equiv="refresh" content="0;url=/canonical/">` fallback to legacy root `.html` pages; the existing JavaScript forwarding continues to preserve query strings and fragments where present. The homepage `index.html` is excluded to avoid a redirect loop.
2. `scripts/build_clean_urls.py` strips this legacy redirect marker when constructing clean `/index.html` pages. This preserves the final canonical pages and prevents self-redirects.
3. All 31 legacy root `.html` source files have been synchronised to the new fallback. No canonical route, public page copy, commercial rule or customer form was rewritten.
4. Added `tests/seo_legacy_redirects.py` for 31 legacy aliases and canonical safety, and `tests/seo_core_services.py` for seven core routes, their sitemap/metadata and crawlable links. The build pipeline now invokes both after generation.

## Read-only source QA performed through GitHub
- 31/31 original `.html` documents: exact redirect fallback to their canonical destination; original canonical tag preserved.
- 31/31 clean directory documents: no legacy refresh marker; canonical target preserved.
- 7/7 service and suit pages: title, description, one H1, canonical URL, sitemap inclusion and `index, follow` in committed HTML.
- The homepage links directly to custom tailoring, clothing alterations and garment care. The tailoring services hub links to men's and women's suits.
- `_headers` still declares staging-host `X-Robots-Tag: noindex, nofollow, noarchive`. Actual Cloudflare response header behavior remains untested.
- The above are **static GitHub source assertions**, not a successful execution of the full Python build or a browser regression suite.

## Outstanding release gates — do not mark as passed
1. Run `python3 scripts/build_site.py` and `python3 scripts/build_site.py --check` in an authorised repository runner; run `python3 tests/seo_preservation.py`, `python3 tests/sitemap_discovery.py` and applicable browser tests. Collect exit codes/build evidence.
2. Verify actual Cloudflare `mrsewing-staging` deployment ID, branch, commit SHA and successful build; inspect HTTP status for canonical service pages and legacy alias redirects, and the staging `X-Robots-Tag` header on actual responses. This environment cannot independently reach the Pages or live origin.
3. Check real mobile/desktop service navigation, forms, accessibility and noindex staging isolation. Never claim Google will index staging: that environment must remain noindex.
4. Before **any** production release, request owner approval and reconcile the exact scoped changes with production host (GitHub Pages) and production-only configuration. Real HTTP 301 redirects for legacy aliases need host-level support; an HTML refresh is a fallback, not a 301.
5. Only after approved live deployment and live indexing tests, use Google Search Console to request indexing of the final canonical public service pages as needed. Google decides whether/when to include them; requesting indexing does not guarantee a ranking.
6. Google Analytics 4 currently has a selected property but no configured web stream or key events. Configuration is a separate staging-first task; no GA changes made.

**Release assessment:** Source-level R66 repairs committed on staging. **Not ready to declare deployed, live-indexed or fully regression tested.** No paid SEO provider checks or subscription changes were performed.
