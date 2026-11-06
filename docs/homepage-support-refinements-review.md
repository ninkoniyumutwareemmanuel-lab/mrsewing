# Homepage final refinements — owner review

Date: 4 November 2026. Scope: `phase1/customer-journey-repairs`, staging only.

## Changes

- Converted the bottom contact section to **Customer Support**, using the exact requested introduction and concise support topics. Retained the photograph, contact methods, existing submission provider, consent, honeypot, validation, duplicate protection and confirmed-success handling. Removed the visible forwarding/sensitive-document paragraph.
- Preserved the separate hero quotation journey using the original quotation form in a native accessible dialog. Escape, close and backdrop interactions return focus to the initiating link. Without JavaScript, the form remains available at the existing `#quotation` fragment. Support and quotation submissions have independent state and subjects.
- Replaced only the homepage footer with three columns: Service Links, Customer Guides and Quick Information. Preserved approved social destinations and the exact parent-company copyright. Other pages retain their existing shared footer.
- Updated only the requested Moments introduction and two captions. Both original photographs remain.
- Changed the existing three-slide text carousel to a four-second interval. Removed playback controls and counter, retained three accessible selection dots and the existing slide content. Touch hold, hover and keyboard focus pause rotation; release/cancel/leave starts a fresh four seconds. Reduced motion disables automatic sliding. Pointer listeners are passive and do not block scrolling.

## Preservation

Compared with the previous approved commit `30b55a8e6e1ef8b555ee047b27f83328d76db6ba`: Customer Information Highlights, hero, service cards, Why Choose, six-step process, programme content and Send Us Your Design source sections are byte-for-byte unchanged. Header/logo markup, SEO configuration, sitemap, robots, redirects, hosting headers and all 303 existing image assets are unchanged. No commercial wording or programme status was changed.

## Guides and destinations

- Measurements Guide links to the existing `/measurements/` page.
- Garment Care Guide is plain text, awaiting the planned `/guides/garment-care/` page.
- Fabric Guide is plain text, awaiting the planned `/guides/fabrics/` page.
- `_data/homepage-guides.json` holds the future route configuration. Planned routes are not rendered as links. Existing location, hours, policies, terms and service destinations resolve locally.

## Verification

- Production site build and generated-output consistency check: passed.
- Python test suites: 13 suites passed; `tests/preview_server.py` is a local server utility, not a test suite.
- JavaScript syntax checks and `git diff --check`: passed.
- Focused support/quotation tests: passed required fields, phone validity, consent, distinct request payloads, confirmed success, rejected response, malformed JSON, server/network failure, duplicate submission, timeout and honeypot cases. The tests intercepted submissions; no real customer enquiry was sent. Actual provider-to-mailbox delivery remains unverified.
- Carousel tests: four-second start/sequence/loop, right-to-left transition, hover/focus, manual selection, timer reset, passive touch hold/release/cancel, reduced motion and no-JavaScript fallback passed.
- Chromium responsive checks: 320, 360, 390, 430, 768, 1024, 1280 and 1440px; no horizontal overflow. Pixel 7 and iPhone 13 touch emulation passed. Real Android/iPhone devices and Safari/WebKit were unavailable; these were not tested.
- Axe WCAG 2/2.1 A/AA scans at 390 and 1440px, both homepage and open quotation dialog: zero reported violations. This is an automated check, not a complete accessibility certification.
- Existing browser regression suites: homepage, homepage-phase1, final-v2, customer-journey, homepage-optimization and phase1 passed; include other pages, navigation, gallery and existing forms. No JavaScript page errors were reported by the suites.
- Screenshots were inspected for the support section, footer and Moments messaging. Screenshot-only styling moves the sticky header into normal flow for unobstructed section captures; it does not change deployed CSS.

## Changed files

Homepage source: `_templates/homepage-sections.html`, `_templates/homepage.html`, `_templates/homepage-phase1.css`, `_templates/homepage-corrective.js`, `_templates/order-carousel.js`.

New homepage-only sources: `_templates/homepage-footer.html`, `_templates/homepage-quotation.html`, `_data/homepage-guides.json`.

Builder and generated output: `scripts/build_homepage.py`, `index.html`, `assets/homepage.js`.

Tests: `tests/support-refinements.spec.cjs`, `tests/order-carousel.spec.cjs`, `tests/homepage-phase1.spec.cjs`, `tests/homepage.spec.cjs`, `tests/homepage-optimization.spec.cjs`, `tests/customer-journey.spec.cjs`, `tests/clean_urls.py`, `tests/shared_components.py`.

## Review artifacts

Local directory: `/workspace/artifacts/support-refinements/`.

Full homepage: `homepage-390.png`, `homepage-768.png`, `homepage-1440.png`.

Section screenshots: `support-*`, `footer-*`, `moments-*`, `information-*`, `quotation-*`, `order-options-*`. Automated accessibility results: `accessibility.json`.

Staging URL: https://mrsewing-staging.pages.dev/

Only the development branch is eligible for the authorized push. No production configuration, custom domain or main-branch change is included. A successful GitHub push does not by itself verify Cloudflare publication; deployment availability is reported separately in the completion message.
