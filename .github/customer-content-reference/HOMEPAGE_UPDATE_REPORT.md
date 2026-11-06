# Homepage improvement — staging review report
Date: 6 November 2026
Baseline: e2139dec2d96c1ec0d4083e860d9ab6445c145a7
Branch: phase1/customer-journey-repairs

## Implemented
- Explore Our Suit Collections between Six Simple Steps and Why Choose, with matching Men’s/Women’s previews and collection links. Six men’s and eight women’s eligible photos currently derive from the same published collection/category records as the galleries.
- Moments in Tailoring now derives seven photos from five approved Our Work projects, with Explore Our Work. Both source loaders enforce their existing publication/permission gates; no separate homepage photo list.
- Slow seamless CSS left-to-right galleries, non-clickable images, no arrows/dots or touch pause. One deliberate pause/resume control supports motion accessibility. Reduced-motion users get a static wrapping gallery; no-JS preview is stable. Existing four-second order carousel is preserved.
- Homepage quotation/consultation actions open /booking/. Existing consultation fields, validation, provider configuration and generated booking assets are unchanged. Obsolete homepage quote/order dialogs are no longer rendered.
- Support form fields/provider/consent remain identical. Positive provider response is required; duplicate submissions, failures, retained inputs and retry are tested. Exact approved support acknowledgement replaces the prior success action; no success WhatsApp redirect/button.
- Send Us Your Design reuses the existing same-page Terms modal, unchecked acceptance and explicit WhatsApp continuation. Opening WhatsApp does not send a message.
- Exact approved homepage description applied to metadata/social metadata; title retained, one H1 and visible Kigali/service context. Other page SEO values, sitemap, robots and staging noindex rules unchanged.

## Verification
PASS — Production generation and generated-output parity.
PASS — 17 Python test suites, including source mutation/removal/restoration tests proving collection and project updates reach the homepage. Temporary source mutations restored.
PASS — Chromium responsive checks at 320/360/390/430/768/1024/1440; no horizontal overflow; identical loop halves/coverage, left-to-right motion, touch does not pause, explicit pause/resume and reduced motion.
PASS — Two automated WCAG 2.2 AA-tag Axe scans; new heading contrast corrected. Keyboard/modal focus, Escape, consent reset and disabled continuation tested.
PASS — Five mocked support provider outcomes (success, rejection, HTTP failure, malformed response, network failure), retry, validation and duplicate protection. No real messages sent.
PASS — Existing consultation 24-case regression suite; existing order carousel interval/loop/hold/hover/focus/reduced-motion regression.
PASS — Preservation assertions: booking implementation, provider source, source-photo data, business data, redirects and indexing configuration unchanged.
PASS — JavaScript syntax checks.
NOT TESTED — Actual business inbox receipt, screen-reader software, physical devices and non-Chromium browsers.
BLOCKED — Direct staging/production HTTP and browser access from this managed environment (proxy CONNECT rejection). Exact-commit Cloudflare GitHub deployment check must be reported separately from browser/inbox verification.

## Local performance comparison
Lighthouse simulated mobile, identical local server, external fonts/CDN blocked; lab data, not field Core Web Vitals or INP.
Before → after: performance 99 → 99; accessibility 100 → 100; SEO 100 → 100; LCP 2.102s → 2.104s; CLS 0 → 0; FCP 1.352s → 1.504s; TBT 75ms → 26ms; measured transfer 194,334 → 234,535 bytes.
Additional source-driven previews increase measured initial transfer by about 40KB. Below-fold images retain lazy loading, dimensions and responsive sources; hero loading priority preserved. No new dependency/library or photos added. Scores do not establish complete accessibility or live performance.

## Source and schema review
Current approved reference advanced to R12 with previous snapshots preserved and manifest hashes updated. Original company source archive remains unavailable; no claim of exhaustive original-source verification. Existing business schema matches repository business/contact records and qualifies consultation/workshop locations and appointment hours separately. Existing priceRange $$ has no independently verified original-source interpretation; retained without inventing a numeric price. No new business fact, service guarantee, stock claim or testimonial introduced.

## Files and evidence
Application: scripts/homepage_galleries.py, scripts/build_homepage.py, _templates/homepage.html, _templates/homepage-sections.html, _templates/homepage-corrective.js, _templates/homepage-galleries.css, _templates/homepage-galleries.js, _data/public-page-seo.json; generated index.html and assets/homepage.js.
Tests: tests/homepage-gallery-sources.py, tests/homepage-update.spec.cjs and preservation assertions in customer_release.py, faq_help.py, final_v2.py, suit_references.py.
Governance: AGENTS.md and .github/customer-content-reference current pointer, manifest, changelog, R12 snapshots and homepage brief/report.
Screenshots: /workspace/artifacts/homepage-update/home-390.png, home-1440.png, terms-320.png.
Logs, Lighthouse JSON, source/preservation evidence: /workspace/review/homepage-update/.

Production/main were not modified. Owner visual review remains required. No publication approval is inferred. Final commit and exact staging deployment evidence are supplied in the delivery report after push.
