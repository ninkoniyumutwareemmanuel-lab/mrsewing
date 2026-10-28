# Phase 1 browser checks

Start the existing static site from the repository root:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

With Playwright available to Node and Chromium installed:

```sh
node tests/phase1.spec.cjs
```

Optional environment variables: `REVIEW_BASE_URL` (default `http://127.0.0.1:8000/`) and `CHROMIUM_PATH` (default `/usr/bin/chromium`). In the prepared cloud environment Playwright is already installed; expose its module directory through `NODE_PATH=/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules` if needed.

The suite blocks all external requests. Form requests are intercepted and fulfilled with controlled responses; no live submission or customer message is sent. It checks all complete pages and rendered local links/assets, gallery keyboard interaction, responsive overflow, corrupted/unavailable storage, explicit form success, rejection, malformed/failed responses, duplicate submissions, consent toggling, measurement requirements, invalid phone numbers, and timeout recovery.

External icon styles/fonts are intentionally blocked. These checks do not establish live delivery, external account configuration, real appointment availability, Safari/Firefox compatibility, or full accessibility compliance.

## Static homepage generation and checks

The homepage reuses sections from the existing source pages at build time, so it
needs no runtime HTML fetches. After changing a shared header/footer, source
section, or `_templates/homepage.html`, regenerate and commit `index.html`:

```sh
python3 scripts/build_homepage.py
python3 scripts/build_homepage.py --check
node tests/homepage.spec.cjs
```

The script uses Python's standard library only and never edits standalone source
pages or image bytes. It copies section markup/styles, excludes document metadata
and component scripts, and adds intrinsic image dimensions. The generated HTML is
committed, so GitHub Pages and Cloudflare require no new build settings.

The homepage tests additionally check source synchronization, one H1/canonical,
metadata isolation, hero preloading, deferred scripts, image sizing/lazy loading,
absence of runtime component requests, navigation without JavaScript, slider
controls and WhatsApp consent. The WhatsApp destination is observed locally and
its navigation is prevented; no messages are sent.

## Business structured data

`_data/business.json` is the shared business identity, contacts and confirmed
working schedule. It reuses the existing contact-page branch addresses and phone;
no coordinates, reviews or ratings are invented. Weekend `00:00`/`00:00` entries
explicitly mean closed, not 24-hour opening. Legitimate about-page extra fields
and nonbusiness product/FAQ/navigation data remain separate.

After an authorized business-information change:

```sh
python3 scripts/sync_business_schema.py
python3 scripts/build_homepage.py
python3 tests/business_schema.py
```

The synchronizer updates static JSON-LD, not runtime scripts or form-service
account settings. Public email addresses/mailto links and visible hours must
also match the confirmed information. The static tests can additionally validate
all declared types, properties and domains against an official Schema.org
all-layer Turtle vocabulary downloaded separately:

```sh
python3 tests/business_schema.py --vocabulary /path/to/schemaorg-all-https.ttl
```

No network request or new package dependency is needed by either script. These
checks do not promise Google rich-result eligibility or verify mailbox delivery.

## Reviewed page metadata and outlines

`_data/page-seo.json` contains reviewed, page-specific titles and descriptions for
all 32 standalone documents (including forms that remain outside the sitemap).
Character lengths are editorial guidance, not Google indexing limits. No separate
wedding landing page or unsupported service claim is introduced.

```sh
python3 scripts/sync_page_seo.py
python3 scripts/build_homepage.py
node tests/page-seo.spec.cjs
```

The sync script changes only title/description and existing matching social
metadata fields. It does not alter canonicals, JSON-LD, robots or sitemap policy.
Heading tags are authored in the source pages; the homepage builder adapts reused
services/collections to its own H2/H3/H4 hierarchy. Existing heading typography is
retained through compatible selectors. Visually hidden section labels group
existing content for assistive technology without redesigning the pages.

The browser checks verify unique reviewed metadata, one H1 per standalone page,
rendered content outlines (including dynamically generated portfolio headings),
and all 32 pages at desktop/mobile widths. Run the existing homepage, business
schema and full regression suites as well before a staging push.

## Image delivery and performance

Original photographs, logos, video files and gallery enquiry source URLs remain
unchanged. Responsive WebP candidates are used only when smaller than their
originals; existing JPEGs remain full-resolution fallbacks. The logo uses lossless
WebP, and its favicon uses a small proportional PNG. No image service or visitor
runtime dependency is added.

Authoring requires Pillow (available in the development environment):

```sh
python3 scripts/optimize_images.py
python3 scripts/apply_image_delivery.py
python3 scripts/build_homepage.py
python3 tests/image_assets.py
node tests/image-delivery.spec.cjs
```

Review any newly added gallery files when regenerating: the four dynamic gallery
attribute maps are generated at authoring time. No runtime manifest fetch or image
observer is needed. Image dimensions reserve intrinsic space while existing CSS
continues to control presentation. Existing autoplay videos remain autoplay;
`preload="none"` alone does not suppress autoplay downloading. Only the below-fold
consultation video defers its source until it approaches the viewport. Existing
video bytes and playback settings are retained.

Performance evidence uses local Chromium, external requests blocked, three cold
runs per page/viewport with 100ms latency, 1.6Mbit/s download and 4x CPU slowdown.
A fixed eight-second observation after DOMContentLoaded reports local LCP/CLS/FCP;
resource byte totals include completed resources only, not in-flight video
transfers. These are diagnostic synthetic samples, not Lighthouse scores,
production Core Web Vitals, or real-user INP measurements. Shared host scheduling,
blocked external icon CSS/fonts, video playback and cache state limit comparisons.

The header regression suite verifies all 32 standalone pages at mobile/desktop
widths, the original eight navigation destinations in order, absence of the
header-only Book Consultation link, and preserved body/footer booking access:

```sh
node tests/header.spec.cjs
```

The image delivery suite covers the requested 320, 360, 390, 430, 768 and 1440px
widths across ten representative pages. Neither suite submits live forms or
opens external messaging destinations.

## Phase 2: appointments and clean URLs

The preferred URL format is `/page-name/` (trailing slash), with `/` for home.
All 31 non-homepage standalone source documents generate a matching
`page-name/index.html`; this uses ordinary GitHub Pages directory serving and
needs no hosting configuration or runtime framework. Root `.html` documents
remain authoring sources and full-content, canonicalized compatibility pages.
Their early, exact-path browser redirect preserves the entire query string and
fragment. It uses `location.replace`, so Back does not create redirect loops.
The browser compatibility code provides **no HTTP 301 redirect**: locally, a
legacy HTML request returns its content with HTTP 200. Cloudflare may add its own
platform URL normalization; deployed HTTP behavior remains to be verified. Without JavaScript, that original content and its
preferred canonical remain available. Canonicals and a single-route sitemap
consolidate indexing signals; search-engine recrawling is still required.

Generated directory pages contain `<base href="/">` so existing images, responsive
candidates, inline CSS backgrounds, videos and shared header/footer fetches remain
root-relative. Customer links and same-page fragment links are explicitly
qualified to their clean route; do not introduce bare `href="#section"` into a
directory page or resolve gallery images against `location.href`. The shared
gallery uses `document.baseURI`. Root legacy files never redirect clean paths.

Edit the original root HTML or homepage section/template, not generated directory
copies. The metadata registry still uses the original source filenames as keys.
For approved changes, run in this order and commit both sources and generated HTML:

```sh
python3 scripts/sync_business_schema.py
python3 scripts/sync_page_seo.py
python3 scripts/build_homepage.py
python3 scripts/build_clean_urls.py
python3 scripts/build_clean_urls.py --check
python3 tests/clean_urls.py
python3 tests/business_schema.py
node tests/phase2.spec.cjs
```

Also run every existing browser suite and `tests/image_assets.py`. The Phase 2
suite tests all 32 preferred/legacy routes, query/hash preservation, local
normalization of directory paths without a slash, all 192 page/viewport
combinations at 320/360/390/430/768/1440px, same-page anchors, no-JavaScript content,
and eight intercepted Saturday/Sunday booking requests. The local directory
normalization tests demonstrate expected static-server behavior; actual GitHub
Pages/Cloudflare HTTP behavior must be verified after authorized deployment.

Business schema lists fixed weekday hours only. Its
`disambiguatingDescription` explicitly describes weekend consultations and
customer-location visits by advance appointment, without inventing fixed weekend
opening hours. Visible hours show Saturday/Sunday “By appointment”; no booking
validation excludes weekends. This does not imply unrestricted weekend walk-ins.

Staging deployment: push `phase2/website-corrections` for review. If Cloudflare
continues to use `phase1/customer-journey-repairs`, first fetch/recheck that branch
and only fast-forward it from Phase 2 without force-pushing. A new branch alone
does not update the existing staging URL. Never change `main` or hosting/domain
settings as part of a staging push.
