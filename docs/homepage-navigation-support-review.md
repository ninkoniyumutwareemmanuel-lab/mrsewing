# Homepage navigation, footer and support corrections

Date: 4 November 2026. Scope: homepage only, staging branch `phase1/customer-journey-repairs`.

## Completed

- Header order: Home, Services, Our Work, Measurements Guide, Fabric Guide, About Us, Contact Us, followed by the existing gold Shop action. The mobile logo, Shop action and hamburger remain; the menu has no duplicate Shop entry.
- Services disclosure contains exactly the four approved full service names. The homepage footer and support-topic options use those same four names, including **Mobile Tailoring, Styling & Event Assistance**. Existing service routes are retained.
- Customer Guides contains exactly Measurements Guide and Fabric Guide. No Garment Care Guide or visible Planned Guide labels remain. Header/footer guides use the same data configuration.
- Quick Information retains Location and Opening Hours. Its Policies accordion contains Terms & Conditions, Privacy Policy and Refund Policy exactly once each. All three use existing working pages; no policy wording was changed or invented.
- Removed “Start with a conversation.” The message field reads “How Can We Help You?” Support topic has four service choices plus an empty required prompt. Customer contact fields, consent, validation, provider integration, independent quotation journey and confirmed-success handling remain unchanged.
- No other approved homepage section was changed. Moments photographs remain static; the four-second carousel, three dots and touch-hold behaviour remain unchanged.

## Pending destinations

- **Fabric Guide:** planned route `/guides/fabrics/` does not yet exist. Its name is plain text in the header/footer, without a fake link or visible status label. A hover title explains that the page will be developed separately. The route remains recorded in `_data/homepage-guides.json`.
- **Measurements Guide:** existing `/measurements/` resolves and is used now; its later rebuild is outside this task.
- **Fourth service:** existing `/services/mobile-fitting/` resolves. Expanding that dedicated page to cover the full styling/event-assistance scope remains future page work; this task does not represent that expansion as completed.
- All requested policy pages already exist and resolve. There is no pending policy-page route.
- Shop remains the existing honest informational page; commerce was not introduced.

## Verification

- Production build and generated consistency check passed.
- All 13 Python suites passed.
- Focused browser test passed at 320, 360, 390, 430, 768, 1024, 1100, 1280 and 1440px: exact header order/service lists/guide names, no overlapping header controls or horizontal overflow, keyboard/mobile disclosures, one Shop action, policy destinations, static photographs and preserved carousel controls.
- Four separately intercepted support submissions confirmed the exact selected service reaches the request payload. No real message or customer data was sent; actual provider-to-mailbox delivery is unverified.
- Existing support/quotation suite passed validation, consent, success, rejection, false-success, malformed/server/network failure, duplicate, timeout and honeypot cases.
- Existing carousel suite passed exact four-second sequence/loop, hover/focus/manual selection, single timer, reduced motion and Pixel 7/iPhone 13 Chromium touch-hold/release/cancel emulation. These are not physical-device or Safari results.
- Existing homepage, homepage-phase1, customer-journey and final-v2 browser regressions passed. An obsolete How It Works navigation expectation was replaced with a test of the requested Measurements Guide destination. Other pages were tested read-only and left unchanged.
- JavaScript syntax and `git diff --check` passed. No configured ESLint/TypeScript task exists; syntax checks are not claimed as those tools.
- Every homepage internal link and fragment resolves locally. External social/call/email availability and real Cloudflare rendering cannot be established by local checks.
- Source comparison proves all sections before Customer Support are byte-identical to `6aa203b00aa716438b122fc5bc32e3e1bde38e0a`. Quotation source/integration JS, carousel JS, shared header/footer, SEO data, robots/sitemap, redirects, hosting headers and domain file are unchanged. No photographs were edited.

This is the requested correction verification, not a new comprehensive performance/security/SEO sign-off. Stop for owner review before that next audit or any further page development.

## Files modified

Homepage sources/configuration: `_templates/homepage-header.html`, `_templates/homepage-footer.html`, `_templates/homepage-sections.html`, `_templates/homepage-phase1.css`, `_data/homepage-guides.json`.

Build/output: `scripts/build_homepage.py`, `index.html`.

Tests: `tests/navigation-support-corrections.spec.cjs`, `tests/homepage.spec.cjs`, `tests/homepage-phase1.spec.cjs`, `tests/customer-journey.spec.cjs`, `tests/final-v2.spec.cjs`, `tests/support-refinements.spec.cjs`.

Review report: `docs/homepage-navigation-support-review.md`.

## Evidence and staging

Artifacts: `/workspace/artifacts/navigation-support-corrections/` — full `homepage-390.png` / `homepage-1440.png`, header, mobile menu, expanded four-service menus, support and footer/policy captures; `logs/` contains the actual build/test output.

Staging URL: https://mrsewing-staging.pages.dev/

Exact commit/push and Cloudflare availability are reported in the completion message. A GitHub push is not claimed as verified Cloudflare publication. Production, main and hosting/domain settings are not modified.
