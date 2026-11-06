# Corrective homepage visual rebuild — 4 November 2026

Branch: `phase1/customer-journey-repairs`. Baseline: `0e4059569693e88c6af30db78fc59448f94f5ee3`.
Owner approved the revised plan, cream mobile Why Choose/How It Works layouts, a background hero illustration and development/staging publication only.

## Visual implementation and reference comparison

Five references were supplied and inspected: header, hero, cream services/customer information, Why Choose and How It Works. The owner confirmed these are enough to guide the remaining areas. No comparison against three unavailable references is claimed. Reference screenshots are review material only, never website section images.

| Supplied reference | Implemented layout | Intentional differences |
| --- | --- | --- |
| 1000840409 — header | Black two-level desktop header, official logo, verified information, social links, Services dropdown, quote action and FAQ search; compact mobile logo/search/quote/menu. | Existing MS logo instead of the illustrative mockup logo. Collections leads to the valid existing destination, not an invented Fabrics page. Search is explicitly customer FAQ search. Verified hours link to the full exceptions. No placeholder phone number. |
| 1000840408 — hero | Full-width dark scene, right-weighted mannequin/tailoring tools, large left-aligned brand, gold Fashion accent, tagline, three icon cards, gold Explore Services and outlined Quote actions. Mobile text/actions precede a subject-focused lower crop. | Newly owner-authorized conceptual AI illustration, labelled as an illustration; no claim that it depicts an actual workshop. No automatic slider, fake signage or embedded screenshot text. Existing client photos remain in the galleries. |
| 1000840914 — What We Offer/information | Cream background, three equal image-led dark cards, gold icons and service links; four aligned information highlights. Mobile service cards stack, information becomes a compact list. | Existing garment photographs and a disclosed existing care illustration replace mockup photos. No false image of a real alteration appointment or cleaning facility. Additional existing pathways remain below the cards. |
| 1000840915 — Why Choose | Large authentic client photograph beside a six-card dark desktop grid; cream mobile feature list and gold icon discs. | Quality Fabrics and Reliable Timelines are replaced with supported themes: attention to detail, communication and careful finishing. No stock guarantee or fabric-availability promise. |
| 1000840919 — How It Works | Five dark connected desktop cards, gold markers/icons, subtle tailoring texture and Quote CTA; cream mobile vertical timeline. | Wording explicitly preserves required confirmation/payment and full payment before release. No internal financial figures. Photo texture uses an existing concept illustration. |

Order Options is a dark image-led, manually controlled selector: Standard, Express, Special Orders, Assistance. Arrow buttons and keyboard Left/Right/Home/End work; no automatic advance. Without JavaScript all four descriptions remain visible.

Looking Ahead retains its exact original three cards and Coming Soon wording, visible immediately before Let’s Make It Personal. That invitation retains its original title, paragraph, Contact Us link and exact design-sharing WhatsApp destination, with an authentic existing client photograph. A separate Contact & Quotation section follows it.

Desktop remains predominantly dark, with intentional cream services/information, customer gallery and Looking Ahead contrasts. Mobile Why Choose and How It Works deliberately follow the owner-approved cream references.

## Photography and provenance

No pre-existing photograph or derivative was deleted or modified.

| Source | Placement / crop | Alternative text / provenance |
| --- | --- | --- |
| `assets/homepage-corrective/tailoring-hero.jpg` and four WebP sizes | Hero background: centered wide desktop crop; right-weighted lower mobile image with text above. | AI-generated tailoring illustration with a navy suit and sewing tools. Owner-authorized concept, not actual premises or customer work. |
| `m1.jpeg` and existing WebP | Custom tailoring card; portrait cover, garment centered. | Black men’s suit design; existing asset. |
| `r7.jpeg` and existing WebP | Alterations card and Why Choose desktop photograph; center/top crops preserve the garment. | Completed light-grey jacket/navy trousers; existing authorized client photography, not a claimed repair before/after. |
| `assets/journey/garment-care-illustration.png` | Care card; cover crop. | Existing disclosed concept illustration, not actual premises; no new facility image or claim. |
| `standard.jpeg` and existing derivatives | Order selector, cover centered at 65%; subdued process background. | Existing concept tailoring illustration. |
| `h2.jpeg` and existing derivatives | Let’s Make It Personal; desktop landscape crop / mobile cover at 28%. | Existing off-white graduation tailoring photograph. |
| `fabric.jpeg` and existing derivative | Contact section; landscape cover. | Existing fabric-selection editorial image; no invented customer identity or testimonial. |
| Existing `h2.jpeg`, `r7.jpeg`, `r4.jpeg`, `h3.jpeg`, `m1.jpeg`, `w-classicsuittwo1.jpeg` | Original customer/collection sections retained, responsive existing crops. | Existing gallery descriptions preserved. |
| `MR LOGO.jpeg` and existing small logo derivatives | Header, proportional uncropped logo. | Official Mr Sewing MS logo; no replacement mark. |

New hero dimensions: 1672 × 941. JPEG fallback about 145 KB; WebP candidates approximately 16/29/51/67 KB at 640/960/1440/1672px. Responsive preload matches the hero source set. New files are registered in the required central image inventory as non-design conceptual assets; the collection migration/rights reports only add those five assets and update the count from 298 to 303. All 111 published collection designs are unchanged.

## Functionality, SEO and commercial accuracy

Existing homepage title, description, keyword tag, canonical, Open Graph/Twitter image and metadata, business structured data, favicon, robots, redirects, sitemap and staging noindex safeguards are unchanged. Relevant Kigali service and occasion content remains crawlable. Shared header/footer/CSS sources and all unrelated generated pages remain unchanged.

The new quotation form reuses the existing public Web3Forms integration and destination. Fields: name, phone, optional email, service, message, terms/privacy consent; no uploads, measurements, payment details or local data storage. A honeypot, phone validation, duplicate-request lock and 20-second abort are included. Success requires both a successful HTTP response and JSON `success: true`. Rejection, malformed response, server/network error and timeout preserve entries and offer direct contact; timeout warns that the request may have arrived. Success confirms service acceptance of submission only, not mailbox delivery, an accepted order or an appointment.

Existing standalone booking/measurement forms and their submission controller are unchanged. Direct WhatsApp/phone/email and workplace booking remain available. No real test enquiry was sent. Live provider delivery has not been tested.

No new prices, deadlines, discounts, VIP privileges, program rewards or eligibility rules are published. Care treatments and rates require direct confirmation. Loyalty, Referral and Complimentary Photoshoot remain Coming Soon.

## Changed subsystems

- Homepage header/sections/template and homepage-only CSS/interaction source; generated `index.html` and `assets/homepage.js`.
- Homepage builder includes the separate contact section and new progressive enhancements; legacy slideshow source remains available but is no longer shipped on this static hero.
- Five new hero image files and additive inventory/provenance reports.
- Regression assertions updated for the explicitly approved static hero, three primary photographic services, dropdown navigation, separate contact form and manual option selector. Existing policy, asset, collection and unrelated-page preservation checks remain.

## Validation and owner review

The complete site build and consistency check pass. All 14 Python static suites pass. New browser coverage exercises the eight requested widths, menus/dropdown keyboard behavior, manual options and stable frame, programs adjacency, all homepage internal links, image decoding, SEO, no-JS alternatives and the quotation validation/success/failure scenarios. Hero downloads once; measured parsed HTML is approximately 108 KB. This is a delivery sanity check, not a production Core Web Vitals score.

Automated axe WCAG 2/2.1 A/AA scans report zero violations at 390, 768 and 1440px. Keyboard testing supplements the scan; no complete accessibility certification is claimed. Additional existing suites verify the homepage consent/gallery, cross-page journeys, business-hours behavior and standalone form processing with mocked external requests.

Review folder: `/workspace/artifacts/corrective/`. `review.html` presents each reference beside desktop/mobile implementation screenshots. `homepage-390.png`, `homepage-768.png`, `homepage-1440.png` show the entire page. Individual header/hero/services/information/why/process/options/programs/personal/contact images are also provided. `accessibility.json` contains the scan evidence.

Remaining owner review: visual composition and choice of the authentic client images; no additional business facts are needed. Missing contact/order mockups were interpreted using the supplied visual system. Public Cloudflare and provider delivery checks remain subject to environment network access. A successful Git push must not be reported as a verified deployment without separate evidence. Production settings, custom domains and main must remain untouched.

## Files included in this correction

- `_data/collection-image-inventory.json`
- `_templates/homepage-corrective.js`
- `_templates/homepage-header.html`
- `_templates/homepage-phase1.css`
- `_templates/homepage-sections.html`
- `_templates/homepage.html`
- `assets/homepage-corrective/tailoring-hero-1440.webp`
- `assets/homepage-corrective/tailoring-hero-1672.webp`
- `assets/homepage-corrective/tailoring-hero-640.webp`
- `assets/homepage-corrective/tailoring-hero-960.webp`
- `assets/homepage-corrective/tailoring-hero.jpg`
- `assets/homepage.js`
- `docs/collection-image-migration.csv`
- `docs/collection-rights-review.md`
- `docs/homepage-corrective-review.md`
- `index.html`
- `scripts/build_homepage.py`
- `tests/customer-journey.spec.cjs`
- `tests/customer_information.py`
- `tests/faq_help.py`
- `tests/final-v2.spec.cjs`
- `tests/homepage-optimization.spec.cjs`
- `tests/homepage-phase1.spec.cjs`
- `tests/homepage.spec.cjs`

Verification completed: full build and consistency check; all 14 static suites; corrected homepage/reference-form suite; legacy homepage consent/gallery suite; Final V2 cross-page suite (45 combinations); Customer Journey suite (seven widths); optimization/business-hours suite; existing Phase 1 suite (32 complete pages, 1,051 local references, 48 viewport/page combinations, 30 mocked outcomes across five existing forms). All passed. No real enquiry was sent.
