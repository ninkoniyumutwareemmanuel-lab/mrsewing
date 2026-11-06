# Homepage order carousel — staging review

4 November 2026. Branch: `phase1/customer-journey-repairs`. Baseline: `01371819f0bf51ac3a93ad800a82423d074f03d1`.

## Changes

Explore Your Order Options is now text-only. It starts with Standard Order and automatically advances Standard → Express → VIP → Standard every 5,000ms. The 550ms horizontal transition always moves right to left, including the VIP-to-Standard wrap. Exactly three original slide elements are used; there are no duplicated/cloned slides. A clipped viewport displays one option at a time, with a height determined by the longest text so changing slides does not move the surrounding page.

There are no photographs, links or buttons inside the slides. Below the viewport, three small position controls allow manual reading, and a separate Pause/Play control supports accessibility. These controls are outside slide content; they are not additional order or quotation actions. Hover suspends rotation temporarily. Pointer/keyboard/manual selection pauses until Play is chosen. Hidden-page time does not count toward the next five-second change. Reduced-motion mode does not auto-advance or animate and retains manual selection. Without JavaScript, all three descriptions remain readable as static content.

The current owner-confirmed descriptions are retained. Master Operating Handbook V8, its latest dated approved sections and later approved addenda remain unavailable in the repository/attachments. The latest request explicitly calls its wording a presentation guide rather than permission to override policy. No new order terms were inferred: Express retains its approved capacity/confirmation wording, and VIP retains the owner's confirmed styling/event support with an individual quotation. Detailed handbook verification remains a document-access limitation.

## “Concept Tailoring” investigation

The visible text came from two HTML captions: `.hero-image-note` over the hero and the order photograph's figcaption. The captions are removed, and the entire photograph/figure is removed from the order section. The obsolete hero-caption CSS is removed rather than used to hide anything.

Header markup, authentic `MR LOGO.jpeg` and responsive logo/image assets were inspected. Neither the authentic logo nor the hero illustration has embedded “Concept Tailoring” lettering; no matching header or CSS-generated phrase was found. No image was edited, obscured with a patch or replaced. Accurate non-visible image/provenance descriptions are preserved, and original asset files remain available for other existing uses.

## Preservation

A direct comparison with the baseline proves that What We Offer, Customer Information, Why Choose, six-step How It Works, two-photo Moments in Tailoring, programme cards, Send Us Your Design and Contact are exactly unchanged in their source markup. The hero differs only by removal of the caption. The Made Around Your Needs heading remains above the carousel. Header, logo, image bytes, footer, metadata, original form/menu logic, policies, redirects, sitemap and robots files are unchanged. No unrelated page or production setting was changed.

## Requested checks

- Full build consistency and all 14 static Python suites passed.
- Dedicated clock tests passed on mobile and desktop: initial Standard, 4,999ms unchanged, advance at 5,000ms, exact sequence and looping, leftward wrapping, three original slides, hover/pointer/keyboard/manual/Pause-Play behaviour, hidden-page remaining time and reduced-motion behaviour.
- A real intermediate rendered animation frame was checked for a negative horizontal displacement between zero and one viewport width, followed by clean completion.
- Eight-width checks passed at 320, 360, 390, 430, 768, 1024, 1280 and 1440px: stable carousel height, no page overflow, no section photograph, no visible Concept Tailoring text, correct original logo and every required section present.
- Existing homepage navigation, consent/gallery and quotation validation/success/error/timeout/duplicate/honeypot checks passed with intercepted external requests. No real enquiry was sent; no live provider-delivery claim is made.
- Automated axe WCAG A/AA checks found zero violations at 390 and 1440px. This supplements the requested keyboard/pause checks; it is not the separate full technical QA phase.

Artifacts: `/workspace/artifacts/order-carousel/homepage-390.png`, `homepage-1440.png`, `order-options-390.png`, `order-options-1440.png`, `header-390.png`, `header-1440.png`, and `accessibility.json`. The main review screenshots use reduced motion for a stable Standard slide. Additional `order-options-controls-390.png` and `order-options-controls-1440.png` show normal-motion controls paused on Standard. Automatic operation and both motion settings were tested separately.

## Files

- `_templates/homepage-sections.html`, `_templates/homepage-phase1.css` — localised markup/caption/styling corrections.
- `_templates/order-carousel.js` — isolated rotation/interaction enhancement.
- `scripts/build_homepage.py` — includes the carousel module; generated `index.html` and `assets/homepage.js`.
- `tests/order-carousel.spec.cjs` — timing/transition/pause/layout/preservation coverage.
- `tests/customer_information.py`, `tests/faq_help.py`, `tests/homepage-phase1.spec.cjs`, `tests/final-v2.spec.cjs` — expectations updated for caption removal, generated JS and controls outside the slides.

Staging URL: https://mrsewing-staging.pages.dev/. GitHub push and Cloudflare publication are reported separately where proxy restrictions block deployment checks. Main and production must remain unchanged. Stop for owner visual approval after this limited correction; do not start the separate technical QA phase.
