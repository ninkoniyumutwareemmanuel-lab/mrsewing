# Final Homepage, Our Work and Customer Forms — Implementation Report

6 November 2026, Africa/Kigali. Development branch `phase1/customer-journey-repairs`. Baseline `9a54b91883828f9dfe2417704fbe38a711666c79`.

## Homepage

All three photograph tracks now move **right to left**. Their identical loop halves, slow CSS transforms, noninteractive pictures, responsive sources, source synchronisation and reduced-motion fallback remain. View All Men/Women and Explore Our Work retain their destinations. The existing explicit accessibility pause/resume control is retained; touching photographs does not pause or navigate.

Chat with Mr Sewing on WhatsApp now opens the existing same-page Terms dialog, as does Send Us Your Design with its original prepared message. Consent is unchecked each time; Continue is disabled until accepted. Full Terms link, Cancel, Close, Escape and focus return are supported. Official WhatsApp destination is unchanged and no message is sent automatically.

Homepage support fields, provider configuration, validation and exact approved success wording remain. Positive provider acceptance alone permits success; failures preserve inputs/retry, duplicate pending sends are blocked, and no WhatsApp action appears in support success. Hero quotation/consultation still opens `/booking/`. Programme/Shop links and homepage SEO data remain unchanged.

## Our Work and project pages

Preserved the existing five-project gallery, seven associated photographs, approved descriptions/editorial and related-work cards. Each project remains one record rather than one card per photograph. Removed two redundant generic gallery actions. No project, testimonial, customer identity, price, material composition or personal story was invented.

Permanent project routes:

1. `/our-work/off-white-graduation-suit/`
2. `/our-work/light-grey-and-navy/`
3. `/our-work/soft-ivory-tailoring/`
4. `/our-work/cobalt-blue-suit/`
5. `/our-work/blue-jacket-black-trousers/`

Every page retains its approved photos, details and Explore More of Our Work section. **Inquire About This Design** routes to fabric selection. The accessible photo viewer can enquire about the exact photograph being viewed; the primary enquiry reflects that selection too. Selection count is visible. Related cards open their own project pages.

Visual review found an inherited homepage icon-card CSS grid squeezing project editorial text into narrow columns. A project-scoped wrapper/style fixes the collision without changing the homepage cards. Viewer enquiry no longer overlaps its navigation controls. Quotation review headings now scroll below the sticky header; this correction is scoped to quotation requests, preserving booking behaviour.

## Shared photograph → fabric → quotation flow

Both entry points use the same `request_form()` builder, `/request/` page, validation, review/edit and submission controller:

- Custom Tailoring → Men's/Women's category → design/photo → fabric selection/advice → quotation → review → submit.
- Our Work → project → chosen photo → Inquire → fabric selection/advice → **the same quotation page** → review → submit.

The shared media model derives exclusively from existing publication-gated collection data and permission/completion-gated project records. The project loader is shared by gallery, homepage, metadata and selection consumers; no extra maintained homepage picture list was added.

`photo` carries the full canonical original-image URL through navigation and the per-tab context. The model validates that the photograph belongs to the selected design/project. Preview shows the actual image/name/link; review shows a clickable full **Selected Photograph URL**. Legacy Design Image and supplementary design/project references remain in the email payload for compatibility. Changing fabric retains the photo and common customer fields.

Example actually tested: the project's second photograph remains **https://mrsewingfashion.com/h2.jpeg**, not its first photo, filename or an internal ID. Named WebP URL encoding was tested, including **https://mrsewingfashion.com/Midnight%20Elegance%20Women%27s%20Double-Breasted%20Suit.webp**.

No website photograph is uploaded, attached, converted to Base64 or requested again from the customer.

## Email-only validation and distinct service forms

Both selected-design paths use `/api/selected-design-request`. This email-only Pages Function revalidates photograph membership and fabric choice against generated authoritative allowlists, normalises canonical URLs/name/category and forwards textual fields through the existing free Web3Forms configuration. Customer-supplied routing/credentials, unrelated/external photos and incompatible fabric choices are not trusted. Terms, honeypot, host/origin/method/body-size checks and positive-only provider acceptance are enforced. No database, file store or staff feature is activated; no new provider account/key or paid service introduced. Existing gated private API also preserves production canonical image URLs rather than replacing them with staging origins.

Distinct service journeys:

- `/request/custom-tailoring/`: general garment/tailoring enquiry, no website photograph required.
- `/request/alterations/`: alteration/repair description and existing garment/condition fields.
- `/request/garment-care/`: garment choices, quantity, requested care, condition and handover preferences.
- `/request/vip/`: requested VIP assistance, occasion/purpose and existing date/location/contact requirements; no unfinished subscription/contract promises.
- `/request/mobile-fitting/`: existing assistance/location/time/participants/event questions.
- `/services/custom-tailoring/special-order/`: own-design enquiry, no compulsory selected design/upload; explains that the team may request pictures through WhatsApp after review. No separate picture-sharing button is required to submit.

The legacy general service selector now opens the relevant dedicated form, retaining common contacts in the existing per-tab draft mechanism without carrying consent. Service enquiries do not inherit stale selected-design/fabric requirements. Existing Standard email and Express/manual WhatsApp service routing is preserved. Booking, homepage support and Shop product quotations remain separate journeys.

## SEO

Homepage SEO data was preserved byte-for-byte. Existing project pages now have their unique approved titles/descriptions/H1, self-canonicals, actual image metadata, Twitter/Open Graph and CreativeWork/image/breadcrumb data. Removed duplicate logo alt metadata. Only the five approved project routes were added to indexing eligibility/sitemap: **22 current public sitemap routes**, with forms/private pages excluded and staging noindex preserved. No broader indexing rewrite, search-volume/ranking claim or sitemap submission.

Original business-source coverage remains incomplete. No new commercial or project facts were inferred; unverified project fabric information was omitted.

## Actual checks

| Check | Result | Scope |
|---|---|---|
| Production generation and `--check` parity | PASS | Normal repository build |
| Python suites | PASS | All 19 relevant existing suites; historical preservation/count assertions narrowly updated for authorised R15 changes |
| Selected-photo model/API | PASS | 22 approved design/project mappings; canonical URI membership, external/cross-project URL rejection, fabric/consent/honeypot validation, provider success and four failure modes; mocks only |
| End-to-end selected-design journeys | PASS | Men, Women, project second photograph, named WebP; fabric/advice, contact retention, same form, review link and server email payload; no files |
| Distinct service/Special journeys | PASS | Five dedicated services plus Special, rejection/retry/success with mocks, no mandatory website photo; legacy selector retains contacts and resets consent |
| Three gallery directions | PASS | All three sampled transforms negative; seamless geometry/reduced motion/noninteractive pictures in homepage regression |
| Support WhatsApp popup | PASS | Same page, unchecked consent, disabled Continue, Cancel/Escape/focus and official destination intercepted |
| Homepage support email states | PASS | Existing five mocked provider outcomes/retry/duplicate protection/no success WhatsApp button |
| Responsive layouts | PASS | 320/360/390/430/768/1024/1440, including long URL review; project editorial width and non-overlap asserted |
| New journey accessibility | PASS | Five WCAG 2.2 AA-tag Axe scans including selected review and 320px dialog, plus keyboard/lightbox/focus tests |
| Booking regression | PASS | 24 cases; generated booking HTML and consultation script unchanged |
| Shop/programme regression | PASS | Existing Shop suite including eight Axe scans; catalogue and programme pages unchanged |
| Existing private API security | PASS | 12 local emulation groups; no live private activation or storage claim |
| JavaScript syntax / source checks | PASS | Changed runtime scripts and normal builder imports |
| Actual business inbox / email-client link rendering | NOT TESTED | Provider requests inspected through controlled mocks only |
| Real devices, Safari/Firefox, screen-reader software | NOT TESTED | Chromium emulation/keyboard/automated checks only |
| Direct staging origin | BLOCKED if managed proxy denies | Exact-commit Cloudflare status and final HTTP attempt recorded after push |

Project-detail local simulated-mobile Lighthouse: **100 performance / 100 accessibility / 100 SEO**, LCP **1.806s**, CLS **0**, TBT **0ms**, measured transfer **505,790 bytes**. External fonts/CDN blocked, local server only. This is lab evidence, not real-user Core Web Vitals/INP, complete WCAG compliance or a live deployment measurement.

## Changed source groups and evidence

- Homepage gallery CSS and support WhatsApp trigger.
- Shared Terms, request context/draft, selected-photo preview/model, quotation controller and service field generation.
- `scripts/project_catalog.py`, `selected_designs.py`, portfolio enquiry builder and Our Work generator; existing photo-viewer assets.
- New email-only selected-design Function/handler; generated public allowlists and private API canonical validation.
- Scoped project/review CSS, project sitemap eligibility and generated outputs.
- New journey/photo validation tests and narrowly updated historical assertions; R15 versioned reference/brief.

Full changed-file list and logs: `/workspace/review/final-journeys/`. Screenshots: `/workspace/artifacts/final-journeys/` (Our Work, project, VIP mobile; selected-design review mobile/desktop).

Verified unchanged: booking HTML/consultation script, Shop and programme pages, Shop draft catalogue, original project records/photographs, homepage SEO data and private-feature flag. No main/production/DNS/provider-credential/payment changes.

## Outstanding verification and review

Ready for owner staging visual review of the implemented journeys. Actual deployed provider acceptance, business-inbox receipt and email-client link rendering need a controlled live check before publication; no delivery claim is made. Canonical photograph URLs intentionally use the production domain and were verified against repository assets, not live production HTTP. Direct origin access remains subject to the managed network policy. Physical-device and assistive-technology checks remain unperformed. Existing unrelated commercial/Shop/VIP/legal holds remain unchanged.

Commit SHA, exact staging deployment and preview are supplied in the delivery message and external report after push. Stop for owner review; no production publication authorised.
