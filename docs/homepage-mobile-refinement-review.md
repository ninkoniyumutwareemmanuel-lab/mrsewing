# Homepage mobile refinement — owner review

4 November 2026. Branch: `phase1/customer-journey-repairs`. Baseline: `521840cb40c951617d2b97b4bdc8204f9ac118cf`.

The uploaded implementation task explicitly restores functional quotation and navigation journeys, superseding the previous disconnected visual-review mode. The existing website was refined; it was not rebuilt from scratch. The current-problem mobile screenshots mentioned in the upload were not attached. Verification therefore uses the written criteria, prior supplied design references and actual new browser screenshots; no comparison against unavailable problem screenshots is claimed.

## Completed changes

- Mobile header contains only the authentic logo/brand, one gold Request Quote link and hamburger. Search and chat icons are removed. Narrow-screen spacing is tested from 320px upward.
- Desktop upper bar contains only Kigali Main Workshop location and verified hours, including the Umuganda and Sunday exceptions. Social links, phone and quote action were removed from that bar; the primary quote action is in the main header.
- Mobile hero uses the existing authorized suit illustration as a full-section background behind its text, with a dark gradient. Height follows content; no separate lower image block or fragile fixed-height mobile layout remains. The suit stays recognizable without stretching. Desktop composition stays intact apart from the required CTA simplification.
- Explore Our Services is removed from the hero. Its only action is Request a Quote. Three non-interactive icon highlights describe the services without adding repeated buttons.
- What We Offer has four image-free, icon-led cards: Custom Tailoring & Suits; Clothing Alterations & Repairs; Garment Care & Cleaning; Mobile Tailoring & Consultation. Cards stack on phones, use two columns on tablets and four columns on wide screens. Each has one distinct existing service destination. The redundant link cluster and booking link beneath the cards are removed.
- Fourth-card scope was checked against `_data/journey-services.json` and approved customer-information references: measurements/fitting support at a home, office or hotel in Kigali, arranged with the team. No fixed coverage, availability or transport charge is promised. Mobile assistance is also preserved in the existing Assistance option; there was no separate standalone homepage mobile-tailoring section to delete or replace.
- Customer Information Highlights and Made Around Your Needs/Order Options retain their core content and behavior. How It Works retains all five approved stages with shorter mobile spacing and readable descriptions.
- Why Choose is image-free, using supported text/icon advantages. No invented reviews, guarantees, achievements or new commercial conditions were added.
- Collection & Inspiration is absent from homepage sources and output. The separate customer-work gallery remains. All underlying collections pages, designs and media remain untouched.
- Looking Ahead retains exact approved Loyalty Program, Referral Program and Complimentary Photoshoot wording, all Coming Soon, directly before Let’s Make It Personal.
- Let’s Make It Personal is photo-free, with centered black/gold typography and its existing design-sharing WhatsApp action. The duplicate Contact Us button was consolidated into the main navigation and substantial contact section below.
- The quotation form is active again, using the unchanged existing Web3Forms integration and controller. Inputs are sized at 16px/48px on phones, labels/feedback are readable, and privacy/terms handling remains. No second duplicate contact form was added: contact methods remain distinct from the quotation form.
- Removed repeated quote actions inside order panels, the process section's duplicate quote button, and the contact section's four redundant WhatsApp links. Distinct option/service routes, production guidance, direct phone/email/WhatsApp and workplace booking remain.
- Homepage copyright is now exactly “© 2026 NINKONIYUMUTWARE NEXUS LTD. All Rights Reserved.” Shared footer sources and every other page's copyright are unchanged.

## Preservation and boundaries

No photograph, logo or derivative was deleted or changed. This task generated no new image. Existing title, description, keyword tag, canonical, social metadata, business schema, sitemap, robots, redirects and staging noindex safeguards are preserved. The parent-company copyright is a homepage-rendering override. Shared navigation/CSS/footer sources, standalone booking/measurement form controller, unrelated pages and production settings remain unchanged.

The homepage builder now uses its connected mode (`HOMEPAGE_VISUAL_REVIEW = False`) because the latest task requires working journeys. The previous preview helper is retained for historical/future use but is not shipped into the active homepage JavaScript.

## Validation

- Complete site build consistency check passes.
- All 14 Python static suites passed.
- Mobile-first browser suite passes at 320, 360, 390, 430, 768, 1024, 1280 and 1440px: no page overflow; compact header; full-hero background geometry; one hero CTA; four photo-free service cards; no photos in Why Choose/personal invitation; removed collection section; company copyright; keyboard menus/options; all retained homepage links; image decoding; metadata; no-JavaScript behavior.
- Quotation tests pass for required fields/consent, invalid phone, confirmed success, false success, rejection, malformed JSON, server/network errors, duplicate protection, timeout and honeypot. No real submission or customer message was sent. Confirmed success requires HTTP success plus provider JSON `success: true`; live email notification delivery is not claimed.
- Automated axe WCAG 2/2.1 A/AA scans report zero violations at 320, 390, 768 and 1440px. These scans supplement keyboard checks and do not establish complete accessibility certification.
- Existing homepage consent/gallery, Final V2 cross-page, Customer Journey and optimization/business-hours checks pass. Existing Phase 1 tests cover all five standalone forms with intercepted external requests. No live provider delivery is inferred from mocks.
- Hero still downloads once. Parsed homepage is approximately 106 KB; this is a delivery sanity check, not a production performance score.

## Visual evidence

Artifacts are outside the checkout at `/workspace/artifacts/mobile-refinement/`:

- `homepage-390.png`, `homepage-768.png`, `homepage-1440.png` — current full-page mobile, tablet and desktop.
- `header-390.png`, `hero-390.png`, `services-390.png`, `why-390.png`, `process-390.png`, `personal-390.png`, `contact-390.png` — actual mobile section screenshots.
- Corresponding `-1440.png` images show desktop sections; `programs-390.png` and `programs-1440.png` verify preserved future programs.
- `accessibility.json` — scan evidence.

## Files and review

Product/build changes: `_templates/homepage-header.html`, `_templates/homepage-sections.html`, `_templates/homepage-phase1.css`, `_templates/homepage.html`, `scripts/build_homepage.py`, generated `index.html` and `assets/homepage.js`.

Tests updated for intentional scope changes: `tests/homepage-phase1.spec.cjs`, `tests/homepage.spec.cjs`, `tests/customer-journey.spec.cjs`, `tests/final-v2.spec.cjs`, `tests/shared_components.py`, `tests/faq_help.py`. The changes preserve assertions for other pages while updating the deliberately removed homepage photos/collection block and homepage-only corporate copyright.

No broken retained link or unexplained test failure remains. Owner visual review is still required. Missing current-problem screenshots limited direct before/after comparison, but the written acceptance criteria were tested. The source of truth for mobile scope is the approved service registry and existing policies; no further business fact is needed to review this version.

Staging URL: https://mrsewing-staging.pages.dev/. A GitHub push and Cloudflare publication must be reported separately if proxy restrictions block the site or deployment checks. Main, live deployment, production settings and custom domains must remain untouched.
