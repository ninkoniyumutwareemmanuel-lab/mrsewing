# Final homepage content corrections — 4 November 2026

Branch: `phase1/customer-journey-repairs`. Baseline: `e4d5b57425aaa4b26cbe5def93d7ec4e8f73f86f`.

The owner approved the overall visual design. This revision changes only the requested homepage content, actions and layout counts. The existing black/gold/cream system, logo, mobile hero background, Why Choose section, Send Us Your Design direction and backend integration remain.

## Implemented corrections

- Main header's gold action is now **Shop**, on mobile and desktop. It links to the existing `/shop/` information page. That page explicitly says Shop — Coming Soon and has no products, checkout, payment or launch date. The link's accessible name and title make this status explicit; no functioning commerce is implied. The upper desktop bar still contains only approved workshop location and hours.
- Hero has four short, non-interactive service highlights. The fourth is shortened to “Mobile Tailoring, Styling & Events” for readability. Mobile uses a two-by-two arrangement over the same photograph; desktop uses four cards. The hero retains exactly one action, Request a Quote, at `#quotation`. Explore Our Services remains absent.
- Four service cards use the owner's exact short descriptions and full requested titles. Existing service routes remain; the fourth uses `/services/mobile-fitting/`. Its current dedicated page covers measurements/fittings, so a fuller styling/event-assistance page remains future page-development work. No placeholder or new service page was created.
- Customer Information is four informational, non-interactive blocks: Delivery & Shipping, Express Service, VIP Assistance, Customer Assistance. Copy is exactly the supplied concise wording; shipping is an enquiry, not a worldwide-service or carrier-partnership guarantee.
- How It Works has the six supplied stages and descriptions. Icons follow each stage's meaning. Mobile keeps the existing vertical timeline, intermediate desktops use three-by-two cards, and wide desktop uses six cards. No percentages, deadlines or new guarantees were added.
- Order Options has exactly three static summaries: Standard Order, Express Order and VIP Order, using the supplied conditional descriptions. All buttons, option selectors, links and duplicate quotation actions are removed from this section. Existing photographic composition is retained.
- Moments in Tailoring contains exactly two actual, previously owner-authorized photographs: `r7.jpeg` (Men’s Tailoring) and `h2.jpeg` (Women’s Tailoring). They link to their existing completed-project pages. The third photograph is removed from homepage placement only; its file and project route remain. Gallery arrows and the extra View Gallery link are removed because two balanced photographs require no carousel.
- Loyalty Program and Referral Program no longer have Coming Soon badges. The owner subsequently confirmed that the Loyalty & Referral Programme is approved. Short current-programme introductions and “Customer programme” eyebrows replace the historical development wording, with no published reward structure. Complimentary Photoshoot alone retains Coming Soon within this area. No dates, benefits, rewards or eligibility terms were invented.
- Let’s Make It Personal / Send Us Your Design is unchanged. The existing exact design-sharing WhatsApp URL remains; it asks permission to send inspiration and is not advertised as a website upload.
- Contact form service selection contains exactly four actual categories, plus the empty selection prompt: Custom Tailoring & Suits; Clothing Alterations & Repairs; Garment Care & Cleaning; Mobile Tailoring, Styling & Event Assistance. Name/phone/optional email/message/unchecked terms consent remain. Endpoint and integration values are unchanged.
- Removed the contact-area workplace-appointment link and its accompanying Main Workshop schedule paragraph, corresponding to the unwanted appointment area in the instruction. Header workshop location/hours, the actual contact address and legitimate footer details remain. Booking/workplace routes and functionality are preserved.
- Copyright remains exactly “© 2026 NINKONIYUMUTWARE NEXUS LTD. All Rights Reserved.” It is now 13px with higher contrast (`#e5e0d6`) on the existing dark footer, with unchanged company spelling.

## Policy verification and owner review

The owner confirmed that the latest approved Master Operating Handbook V8 and later approved addenda contain VIP Styling & Event Assistance and Loyalty & Referral policies, superseding historical repository notes. This confirmation is used as the authority for the short homepage introductions. VIP is described as personalised styling and event support, with pricing by individual quotation. Loyalty/referral copy introduces the approved programme without historical rewards, discounts or eligibility rules. Complimentary Photoshoot remains the future Coming Soon feature.

**Document not accessible:** Master Operating Handbook V8, specifically its latest dated approved sections and later approved addenda. Searches of repository and supplied attachment filenames found no copy, and no connected document-search tool is available. Detailed policy wording, exact addendum dates, benefits, eligibility and procedures cannot be independently checked here. No assumption is made that the programmes are unapproved. Those details should be checked against V8 when developing the dedicated pages; the homepage uses only the facts confirmed directly by the owner. Shop remains a Coming Soon dependency for actual commerce.

## Functional, visual and accessibility validation

- Full homepage generation and complete site consistency check pass.
- All 14 Python static suites pass after updating only assertions superseded by the requested two-photo gallery and programme-badge changes.
- Homepage browser checks pass at 320, 360, 390, 430, 768, 1024, 1280 and 1440px: no horizontal overflow; approved hero background geometry; correct Shop route; four hero/service categories; six process stages; three action-free order summaries; two approved photographs; one future-feature badge; exact form choices; unchecked consent; removed contact appointment widget; copyright; keyboard navigation and no-JavaScript access.
- All retained homepage internal links resolve locally, including Shop, services, project destinations and Terms & Conditions. No new broken destination was found.
- Quotation tests intercept every external submission and verify required values, invalid phone, unchecked consent, message input, correct Service payload, confirmed success, false success/rejection, malformed responses, server/network errors, duplicate protection, timeout and honeypot. Success requires both HTTP success and JSON `success: true`. No real enquiry was sent; live mailbox delivery/notifications have not been verified.
- Existing cross-page, collection/occasion, business-hours, consent and standalone five-form regressions remain relevant; requests are intercepted. No live message or payment is sent by these checks.
- Automated axe WCAG 2/2.1 A/AA scans report zero violations at 320, 390, 768 and 1440px; keyboard checks supplement these results. This is not complete accessibility certification.
- Actual rendered mobile and desktop screenshots were inspected. The layout remains consistent with the previously approved design; changes are the requested content/count/action adjustments. Hero downloads once; parsed homepage is approximately 103 KB. No production-performance score is claimed.

## Evidence and changed files

Review artifacts: `/workspace/artifacts/final-corrections/`. Full-page `homepage-390.png`, `homepage-768.png` and `homepage-1440.png`; corresponding header/hero/services/information/process/options/programs/personal/contact screenshots; `accessibility.json`.

Product changes: `_templates/homepage-header.html`, `_templates/homepage-sections.html`, `_templates/homepage-phase1.css` and generated `index.html`. No build architecture, unrelated page or backend change was needed.

Regression updates: `tests/customer_information.py`, `tests/faq_help.py`, `tests/final_v2.py`, `tests/homepage-phase1.spec.cjs`, `tests/homepage.spec.cjs`, `tests/final-v2.spec.cjs`, `tests/customer-journey.spec.cjs`, `tests/homepage-optimization.spec.cjs`, `tests/phase1.spec.cjs`. These retain checks for unchanged pages/assets while reflecting deliberately removed controls, gallery item and badges.

SEO metadata/data, canonical/social previews, business schema, original images, authentic logo, source registry, policies, sitemap, robots, redirects, shared components, form integration/controller and all unrelated page outputs remain unchanged. No production deployment or production settings change is authorized or performed.

Staging URL: https://mrsewing-staging.pages.dev/. Report GitHub push and Cloudflare publication separately if network restrictions block independent deployment verification. Owner visual approval and a later technical QA review remain outstanding; this report does not mark the site ready for production.
