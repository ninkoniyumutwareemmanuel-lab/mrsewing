# Homepage Phase 1 — owner review

4 November 2026. Work is local to `phase1/customer-journey-repairs`.
Authoritative reference: remote `main`, `ba27bab0425a9df1948fe8f45dd3b941cb322f4c`.
The clean restored checkout and both remote branch tips matched that commit before editing.
No main branch update, push, deployment, publication, domain change or hosting-setting change was performed.

## Audit and inventory

Inspected `index.html`, `_templates/homepage.html`, `_templates/homepage-sections.html`, shared header/footer/CSS/navigation, homepage interactions/slideshow/resources, `_data/page-seo.json`, business/contact/policy data, image registries, booking forms and submission controller, `robots.txt`, sitemap, redirects and indexing helpers.

The original homepage began with a photograph slideshow and editorial headline without a quotation action, followed by customer photographs and collections. Seven service links, a four-step process, care information and future program announcements were farther down the page. The homepage is assembled at build time; it needs no framework or runtime HTML fetches.

Preserved:

- All original image files and responsive derivatives, official MS logo and favicon; the two hero photographs, three project photographs and four collection cards.
- Useful occasion content: graduation, wedding, civil wedding, men's and women's suits, business outfits, bespoke tailoring, measurements and fitting, own-design enquiries.
- Existing keyword metadata verbatim: Mr Sewing Fashion, bespoke tailoring Kigali, custom suits Rwanda, men’s suits Kigali, women’s suits Kigali, graduation outfits Kigali, wedding suits Rwanda, civil wedding outfits, professional clothing alterations, custom tailoring and fitting.
- The root self-canonical, unique metadata, WebSite/business identities, contact information, social profiles, all opening-hour exceptions, discovery links, root sitemap URL, robots policy, legacy redirects and staging noindex behavior.
- Contact, phone, email, WhatsApp design-sharing, booking and workplace-booking routes; existing Web3Forms endpoints, validation and failure handling are unchanged.
- Legacy consent dialog, photograph controls, pause/hidden-page/reduced-motion behavior, swipeable customer gallery, keyboard menu, focus return, skip link and no-JavaScript access.
- Original shared components and every other generated page; forthcoming programs remain visibly displayed as Coming Soon immediately before “Let’s make it personal.” FAQs, care availability/rate gates, policy wording and all 160 indexable routes remain intact.

Improved and added:

- Homepage-only information bar and seven-link navigation, with a visible Request a Quote action on mobile and desktop. Additional useful destinations remain in content/footer.
- Stable branded headline: “Mr Sewing Fashion — Your Clothing. Our Craft.” Two clear hero actions and crawlable local service text.
- Six requested service categories, with workplace assistance explained; repair/care and special orders lead to enquiries rather than fabricated detail pages.
- Customer information, five-step journey with confirmation/advance-payment gate, standard/express/special/assistance pathways and assessment-based care descriptions.
- Black/charcoal/ivory palette, restrained gold, responsive service cards, consistent spacing, clear light-surface focus indicators and reduced-motion support.
- Dedicated tailoring, alterations, care and workplace WhatsApp enquiry links. These are review-and-send actions, not website form submissions; the page explicitly says that it submits no enquiry. No customer data collection, new backend or false success state was introduced.
- Homepage title/description now describe custom tailoring, alterations, bespoke suits, garment care and Kigali. Social cards use the existing official logo, with matching image/title/description and accurate 1244 × 802 dimensions.

## Files

Product/build:

- `_templates/homepage-header.html` — dedicated homepage header; shared header stays unchanged.
- `_templates/homepage-phase1.css` — homepage-only responsive styling.
- `_templates/homepage-sections.html` — revised and additional sections, retained galleries/programs.
- `_templates/homepage.html` — section order, social metadata and matching navigation schema.
- `_data/page-seo.json` — homepage entry only.
- `scripts/build_homepage.py` — assembles the dedicated header, additional sections and stylesheet.
- `index.html` — generated output.

Regression coverage:

- `tests/homepage-phase1.spec.cjs` — new responsive journey/SEO/link/delivery checks.
- `tests/homepage.spec.cjs`, `tests/customer-journey.spec.cjs`, `tests/final-v2.spec.cjs` — updated only assertions for deliberately changed homepage content/navigation.
- `tests/shared_components.py` — verifies dedicated homepage header and retained shared footer/CSS propagation.
- `tests/faq_help.py` — replaces historical homepage byte-freeze with deterministic build validation; all other page metadata and existing asset/policy/config preservation assertions remain.

## Build and SEO maintenance

Run from `/workspace/mrsewing`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_site.py
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_site.py --check
```

The complete build synchronizes source SEO first, then homepage, Contact, About, Collections, Journey, Completion, clean URLs and public route outputs. Full build and consistency check pass without changes to other generated pages.

For later phases, use each page's unique `_data/page-seo.json` entry and its existing builder; use `site_seo.finalize` for canonical/indexing safeguards. Social titles/descriptions must match the page, and image dimensions must be checked against the real asset. Retain `NOINDEX` for booking, measurement, alias and unfinished Shop routes; publish sitemap entries only for canonical indexable routes through `build_public_routes.py`. No future page was redesigned in this phase.

## Validation and review

- Full site build and `--check`: passed.
- All 14 existing Python static suites: passed. Inventory covers 160 sitemap pages and 6,618 local links/resources.
- Homepage structure, consent, slider and no-JS tests: passed.
- Homepage optimization suite: passed at seven widths, including one high-priority hero download, no third-party icon/font CSS and intercepted business-hours booking tests.
- New Phase 1 suite: passed at 320, 360, 390, 430, 768, 1024, 1100 and 1440px; section order, keyboard focus/menu, quote actions, local links, image decoding, advance gate, metadata/schema, no-JS and HTML budget checked. Measured homepage document about 80 KB, seven resource requests on initial local desktop load, one hero download. This is a delivery sanity check, not a live Lighthouse/Core Web Vitals claim.
- Final V2 integration: passed, including exact slideshow clock/pause, 45 responsive page/viewport combinations and all five project viewers.
- Customer Journey regression: passed at seven widths, service detail pages, collections state, legacy aliases, no-JS and simulated staging noindex.
- Automated axe WCAG 2/2.1 A/AA scans: zero violations at 390, 768 and 1440px, and in the open mobile menu and legacy consent dialog. These supplement keyboard checks and do not establish complete accessibility conformance.
- Existing Phase 1 regression: passed across 32 complete pages, 1,037 rendered local references, 48 page/viewport combinations, 30 mocked submission outcomes on five forms, duplicate/consent protection, invalid-phone rejection, measurement requirements and timeout recovery. No JavaScript errors or missing local resources were observed. External submissions are intercepted; these checks do not establish live provider delivery or actual appointment acceptance.

Review artifacts are outside the checkout in `/workspace/artifacts/phase1/`: before-desktop.png, before-mobile.png, after-390.png, after-768.png, after-1440.png, accessibility.json and accessibility-interactions.json.

For local review, run `python3 -m http.server 8000 --bind 127.0.0.1` from the checkout and use the locally attached browser. The browser tests default to this server; `REVIEW_BASE_URL` and `REVIEW_ARTIFACTS` can override it. No public staging deployment was created.

## Limitations and owner review

- The earlier design-reference images were not present in this conversation. Implementation follows the handoff's explicit palette, typography and photography direction; visual approval remains with the owner.
- The public logo URL is an existing main-branch business-schema asset, verified locally as JPEG 1244 × 802. An outbound proxy CONNECT 403 prevented checking its live-domain response. Public social-card fetch/caching must still be verified from a network with domain access.
- No new business facts, prices, testimonials, deadlines or guarantees were invented. Care/cleaning treatments and rates remain subject to direct confirmation. Workplace location, scope, availability and charges remain enquiry-based.
- Owner approval is required before any later live deployment. None was performed here.

## Section J — promotions, programs and final invitation

Inspected the authoritative main snapshot's exact `#programs-section`, `#programs` and following final invitation. The eyebrow is “Looking ahead,” repeated on three cards: Loyalty Program, Referral Program and Complimentary Photoshoot. Main contains no active promotional discount, reward amount, program signup, program link, or program-specific enquiry handler in this block. All three are explicitly Coming Soon. The photoshoot copy says availability, eligibility and conditions will be announced when ready.

The complete original programs markup and wording are preserved byte-for-byte. The cards are now visible, never collapsed in Order Options, immediately before the final invitation. Homepage-only charcoal cards, gold borders/status badges and ivory typography improve presentation without new benefits or conditions. The original “Let’s make it personal” eyebrow, “Your Next Special Outfit Starts Here” headline, descriptive paragraph, Contact Us destination and exact Send Us Your Design WhatsApp URL are retained. The Phase 1 additional enquiry pathways remain below these original actions.

Policy check: approved customer-information review excludes unapproved loyalty/referral/photoshoot promotions from active offers (`docs/customer-information-staging-review.md`, including its owner-review items). FAQ assertions prohibit invented discounts, rewards and eligibility. No current approved activation terms were found for these programs. They therefore remain Coming Soon, not currently redeemable. Owner review remains necessary before activating any promotion, reward or photoshoot eligibility; none was silently deleted or advertised as active.

The owner confirmed that existing main-branch pictures are the intended assets for this phase. They remain unchanged; picture substitutions are deferred to later owner direction.

Review/test checklist: visible program cards and all three status badges; exact policy/eligibility wording; no invented promotion or signup; direct adjacency to the final invitation; original final copy and both enquiry destinations; mobile/tablet/desktop layout; keyboard access and contrast. Dedicated program/final screenshots are `programs-390.png`, `programs-768.png`, `programs-1440.png` and `personal-390.png`, `personal-768.png`, `personal-1440.png` under `/workspace/artifacts/phase1/`. The refreshed full-page screenshots include both sections.

Section J validation completed: full build consistency, exact main programs markup and final-link preservation checks, eight-width homepage checks, legacy consent/design-sharing regression, and refreshed three-width WCAG scans all passed. No external enquiry was sent. No deployment or publication occurred.
