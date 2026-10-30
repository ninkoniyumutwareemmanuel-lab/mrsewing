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

The homepage assembles `_templates/homepage-sections.html`,
`_templates/shared/site.css`, `_templates/homepage.html` and
`_templates/shared/footer.html` at build
time, so it needs no runtime HTML fetches. Standalone service/collection pages
keep their own content and styles. After changing these homepage sources or the
shared component, rebuild both V2 pages with `python3 scripts/build_site.py`
and commit their generated outputs. See [shared component architecture](../docs/shared-components.md).
For homepage-only content changes:

```sh
python3 scripts/build_homepage.py
python3 scripts/build_homepage.py --check
node tests/homepage.spec.cjs
node tests/homepage-journey.spec.cjs
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
no coordinates, reviews or ratings are invented. Regular Monday–Saturday hours are 09:00–17:00. Dated Umuganda
exceptions override the last Saturday to 12:00–17:00 by advance appointment;
Sunday has no invented fixed opening hours. Legitimate about-page extra fields
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

Business hours are now derived from `_data/business-hours.json`. Normal Saturday
visits are 09:00–17:00 without an appointment. The last Saturday (Umuganda) is
12:00–17:00 strictly by advance appointment; Sunday is by appointment only.
The calendar and form rules are documented below; no entire weekend day is
disabled in the booking forms.

Staging deployment: push `phase2/website-corrections` for review. If Cloudflare
continues to use `phase1/customer-journey-repairs`, first fetch/recheck that branch
and only fast-forward it from Phase 2 without force-pushing. A new branch alone
does not update the existing staging URL. Never change `main` or hosting/domain
settings as part of a staging push.

## Homepage performance specialization and current hours

Homepage resource substitutions live in `scripts/homepage_resources.py` and run
inside `build_homepage.py`. They affect the generated homepage only: standalone
collections/services retain their original image/icon delivery. Seven Font
Awesome Free 6.4.0 glyphs use the exact licensed SVG paths (CC BY4.0; see
`assets/fontawesome-LICENSE.txt`); no icon stylesheet or font is requested by home.
All existing accessible parent labels remain; decorative SVGs are hidden from
assistive technology. The footer copyright contrast correction is also homepage
only. No new visitor framework/runtime manifest fetch is introduced.

`optimize_homepage_images.py` requires authoring-time Pillow with AVIF support.
It generates only the hero/logo/client-strip derivatives under `assets/homepage/`
with content hashes; original files and the existing shared image inventory stay
untouched. Photos use quality82 AVIF (4:4:4 chroma for client images); logos use
lossless WebP. The recorded photo PSNR threshold is35dB against the same-size
reference; logo visible pixels/alpha compare exactly. Responsive slot sizes
match the three large 3:4 editorial portraits, including source pixels needed for
safe centered crops. Logo slot sizes match its actual CSS display size. Stage A
uses the existing `h1.jpeg` graduation portrait and its 480px WebP variant as the
hero; the eager/high-priority preload is derived directly from the source image's
srcset and sizes. Other homepage photographs remain lazy. Earlier background-hero
variants stay in the inventory for rollback; Stage A does not request them or
re-encode any originals. The original authoring script is retained, but no image
regeneration is needed to build Stage A.

The new filenames avoid stale image replacements. They do **not** change server
cache lifetimes: GitHub Pages does not expose general per-file Cache-Control
settings in this repository. No fake `_headers` or HTML meta-cache solution is
added. Reduced transfer/icon requests are the immediate gain; future longer
caching would require separately authorized hosting/CDN configuration.

```sh
python3 scripts/optimize_homepage_images.py  # only when regenerating media
python3 scripts/sync_business_hours.py
python3 scripts/sync_business_schema.py
python3 scripts/build_homepage.py
python3 scripts/build_clean_urls.py
python3 tests/homepage_media.py
node tests/business-hours.cjs
node tests/homepage-optimization.spec.cjs
```

`_data/business-hours.json` is the shared schedule source.
`_templates/business-hours.js` generates `assets/business-hours.js`, whose pure
UTC calendar-date calculation finds the actual last Saturday for any month,
including months with five Saturdays. It never interprets a picked Kigali date
through the customer's local time zone. Ordinary Saturdays remain bookable from
09:00; Umuganda morning choices are disabled, noon choices remain available,
and custom requests must be confirmed within12:00–17:00. Sunday requests have no
published fixed opening hours and require confirmation. The four booking pages
include static schedule guidance so script loading does not insert an unexpected
new layout block. Existing validation, submission/consent protection and recovery
remain in the shared controller. No form is an automatic appointment guarantee.

Schema.org cannot express a recurring “last Saturday” OpeningHoursSpecification.
The synchronizer publishes24 explicit, correctly calculated dated exceptions for
the current and following Kigali calendar year, plus the perpetual written rule.
**Regenerate these static dates at least annually** and commit the synchronized
JSON-LD/homepage/clean copies. The calendar and booking logic itself is perpetual;
its tests cover1,212 months/36,890 dates from2000 through2100. `--check` detects
stale dated schema rather than silently claiming future exceptions are current.

Local Lighthouse evidence uses version12.8.2, three cold mobile and three desktop
runs before/after, identical presets, gzip and a600-second cache model. Because
the live site/CDN are blocked here, the baseline used the unchanged commit with
exact6.4.0 icon CSS/fonts mirrored locally. DNS/TLS/CDN behavior and real-user
performance therefore remain unverified. The results are controlled comparisons,
not production PageSpeed scores or field INP; Lighthouse TBT is reported as TBT.
Existing regression suites and the new homepage/calendar/media suites must pass
before staging pushes. Never change production hosting/DNS to pursue these scores.

## Agentic Browsing discovery files

`llms.txt` is Markdown guidance for the bespoke, made-to-order tailoring business.
It has one H1, a summary, and categorized links to existing customer pages. Links
are origin-relative clean URLs so they resolve on staging now and on production
when the tested branch is approved and published. Current hours/prices are not
duplicated; readers are directed to the existing contact/services/policy pages.
This file does not change robots permissions, privacy terms, or training policy.

`ai-catalog.json` uses the ARD manifest format (Agentic Resource Discovery,
current v0.91): https://agenticresourcediscovery.org/spec/ section5.1 and
https://github.com/ards-project/ard-spec/blob/f073b1ea9b01a5f068d0b0986426f2ea49fa30b2/spec/schemas/ard-entry.schema.json
(`$defs/ArdManifest`). `entries` is intentionally empty: no public agent tools,
MCP/A2A interfaces or automated booking API are advertised by this website.
Physical tailoring services are not fabricated agent resources or stock products.
The name/description are permitted transport metadata; ARD ignores those extra
root members. A valid empty manifest is explicitly allowed by the official
schema and conformance test; it does not imply new AI functionality.

Both current `rel="ard"` and predecessor `rel="ai-catalog"` links advertise the
root JSON on all32 preferred pages. The shared tags are maintained in
`build_clean_urls.py`; the homepage template/builder and directory-page builder
reuse them. This is a supported ARD discovery mechanism, avoids reliance on
hidden `.well-known` directories/Jekyll deployment changes, and works with both
current and legacy relation-aware readers. No robots `Agentmap` directive is
added: current Lighthouse's SEO robots validator does not safelist it. No global
404/SPA routing, HTTP header, domain/DNS or hosting configuration is changed.

```sh
python3 scripts/build_homepage.py
python3 scripts/build_clean_urls.py
node tests/agentic-discovery.spec.cjs
```

The test checks HTTP200, actual JSON/text MIME types, strict JSON parsing,
Markdown H1/links, all linked local pages, discovery metadata on every preferred
page, and no extra ordinary-visitor requests. Official validation was also run
with ARD's conformance tool/JSON Schema and Lighthouse13.6.0 audits `llms-txt` and
`ard-schema`. Audit tooling is installed outside the website repository; it is
not a visitor dependency. Future catalog entries require real authorized agent
resources and full schema/conformance validation, not invented capabilities.

Live staging responses can differ while a deployment is pending or protected.
After a confirmed build, verify `/llms.txt` returns Markdown text and
`/ai-catalog.json` returns application/json rather than an HTML fallback. A local
passing audit is not proof of Cloudflare's served version when network access is
blocked. Preserve all existing performance/SEO/customer regression suites.


## Homepage design-sharing journey

`tests/homepage-journey.spec.cjs` checks the seven-section order, real existing
collection/service destinations and FAQ fragments, two prefilled WhatsApp
intents with navigation prevented, all homepage image decoding, compact header,
menu keyboard activation/Escape/focus return/outside dismissal, and the visible
no-JavaScript navigation fallback. It covers 320, 360, 390, 430, 768, 1024 and 1440px.
The responsive disclosure and footer are homepage-only; other pages retain their
shared headers and footers.
Premium garment-care eligibility is linked to Contact because the current FAQ
does not publish those conditions. No tiers or additional entitlements are invented.


## V2 Stage A visual system

The homepage imports none of the shared header/footer CSS. Its portrait hero,
ivory editorial gallery, inspiration index, service rows and compact footer are
maintained in the dedicated homepage templates and stylesheet. Normal hours and
Sunday availability are visible in the footer; the native Umuganda disclosure
reveals the full last-Saturday exception and confirms ordinary Saturday walk-ins.
Desktop navigation exposes five essential links; comments reserve insertion
points for future Shop/Rewards after launch, without advertising inactive pages.
The original shared components and all other standalone pages are unchanged.

`tests/homepage-journey.spec.cjs` also verifies the icon-only mobile menu, absence
of the mobile header order action, seven named services with explanations, three
large editorial portraits, five desktop footer columns, footer disclosure and
compactness, and the retained order-popup focus trap. Passing these checks is
technical verification; the owner must still approve the Stage A visual design.

### Contact Us V2

Contact-only content lives in `_templates/contact.html`, `_templates/contact.css`
and `_data/contact-v2.json`. The generator reuses the approved homepage header,
footer, common CSS and menu controller at build time; it never writes homepage
sources. Contact metadata comes from the existing page SEO data. Keep MIC's
`verifiedMapsUrl` null until a real destination is verified.

```sh
python3 scripts/build_contact.py
python3 scripts/build_clean_urls.py
python3 scripts/build_contact.py --check
node tests/contact-v2.spec.cjs
```

Run `python3 scripts/build_site.py` after changing a shared component, then
`python3 scripts/build_site.py --check` and `python3 tests/shared_components.py`. Browser
checks block external requests and never send messages or real bookings.


### About Us V2

About-only editorial content is maintained in `_templates/about.html` and
`_templates/about.css`; metadata remains in `_data/page-seo.json`. The registered
`scripts/build_about.py` imports the existing shared components without changing
the homepage or Contact. The portrait uses existing, uncropped customer-image
variants from `_data/homepage-media.json`; no new photo asset is generated.

```sh
python3 scripts/build_site.py
python3 scripts/build_site.py --check
python3 tests/shared_components.py
node tests/about-v2.spec.cjs
```

The browser check blocks external services and checks the approved brand story,
founding year, parent company, mission/vision, values, services, metadata,
responsive image delivery, menu behavior, both CTA routes and legacy URL. It
saves review screenshots outside the repository under the review workspace.


### Collections V3 — Luxury Minimalist Showroom

Three galleries and eligible static garment pages are generated from the existing
registry. See [Collections V3 maintenance and verification](../docs/collections-v3.md).
No original images, registry IDs, rights rules or approved shared pages changed.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_site.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_site.py --check
PYTHONDONTWRITEBYTECODE=1 python3 tests/collections_data.py
PYTHONDONTWRITEBYTECODE=1 python3 tests/collections_pages.py
PYTHONDONTWRITEBYTECODE=1 python3 tests/shared_components.py
node tests/collections-v3.spec.cjs
```

Start the static server on port 8000 first. The V2 test filename remains an alias
for V3; favourites and shortlists are retired. Browser tests cover all 111 eligible
URLs, seven gallery widths, filters/Load More, legacy links, related designs,
WhatsApp encoding, full-screen focus/keyboard/swipe, share mocks and no-JS access.
Screenshots default to `/workspace/artifacts/collections-v3` outside the checkout;
set `REVIEW_ARTIFACTS` to choose another artifact directory.

Optional automated WCAG scans use @axe-core/playwright 4.14.0 installed outside the
repository. Expose that package and the existing Playwright through NODE_PATH,
then run `node tests/collections-accessibility.cjs`. Tests block external requests
and never send actual enquiries. Automated scans complement manual keyboard and
responsive checks; they do not establish complete accessibility conformance.


## Customer Journey V1 — current integration

The final consolidated implementation and owner approval requirements are in
[Customer Journey V1](../docs/customer-journey-v1.md). This section supersedes older
hero-button, Shop and service-route assertions described above. Collections V3
remains the garment experience. Services has seven canonical details; old service
URLs are aliases, not separate indexable offerings. Our Work has no published
customer stories until completion/permission evidence is supplied. Care has no
published subservices or price tables until availability, content and rates are
approved. Candidate care categories in JSON are not customer-facing services.

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_site.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_site.py --check
PYTHONDONTWRITEBYTECODE=1 python3 tests/customer_journey.py
PYTHONDONTWRITEBYTECODE=1 python3 tests/garment_care.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/prepare_journey_media.py --check
node tests/customer-journey.spec.cjs
node tests/project_template.spec.cjs
```

Use the standard local static server on port 8000 for browser suites. For exact
redirect/header simulation, separately start `python3 tests/preview_server.py
--port 8001`, then run `node tests/routing.spec.cjs`. This simulation verifies the
generated rules; it does not prove Cloudflare deployed or enforced them. Existing
homepage, header, About/Contact, phase1/phase2, metadata, image-delivery, discovery,
business-hours and Collections V3 suites remain relevant and were run.

Optional axe scans use the externally installed @axe-core/playwright package:
`node tests/journey_accessibility.cjs` with that module directory on NODE_PATH.
Screenshots/logs default to `/workspace/artifacts/customer-journey-v1/`.
No live enquiries are sent. Project and price fixtures are in-memory/intercepted
only; no invented story or sample rate is generated into the website.
