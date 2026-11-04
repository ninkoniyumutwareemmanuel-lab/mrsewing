# Mr Sewing Fashion — final homepage QA and sign-off review

Date: 4 November 2026. Company: NINKONIYUMUTWARE NEXUS LTD.

Branch: `phase1/customer-journey-repairs`.

Tested implementation commit: `a4600b44a7e62d9a7c35ccf4f378073ef263f115`.

Previous approved-design reference: `f752755e65be98d5c2eb245774e38f51aea54a98`.

Staging: https://mrsewing-staging.pages.dev/

This report's later documentation commit does not change the tested website. The exact pushed branch head is supplied in the completion message and is available with `git rev-parse HEAD`.

## 1. Executive summary

**CONDITIONALLY READY — Only documented non-blocking issues remain in the locally verified homepage.**

No blocking local functional, rendering or automated accessibility defect remains. This is a recommendation for owner review, not owner approval, a full WCAG certification, or permission for production publication. Verification gaps remain: live staging deployment/headers, actual mailbox delivery, external destinations, unavailable browser engines/real devices, Google Search Console/field performance and the current handbook. These must not be treated as passed or as a completed production-release checklist.

| Check | Result | Evidence / limitation |
| --- | --- | --- |
| Requested static Moments photographs | PASS | Both links removed; no navigation, modal, pointer/zoom cursor or hover transform; original photographs, captions, alt text, lazy loading and responsive sources retained. |
| Approved layout and other sections | PASS | Source comparison proves no other section copy/layout changed. All 303 existing image assets are byte-identical. |
| Header label accessibility correction | PASS | Added one whitespace separator between the visible brand words. No logo, colour, layout or visual redesign. The label-in-name audit now passes. |
| Owner final approval | NEEDS OWNER DECISION | Owner must review this report and staging before the homepage is marked complete. |
| Production isolation | PASS | No main, hosting, domain, headers, redirects, robots, sitemap or production deployment changes. |

## 2. Homepage functionality

| Check | Result | Detail |
| --- | --- | --- |
| Desktop header, Services disclosure, Escape | PASS | Opens/closes with keyboard; focus returns appropriately. |
| Mobile menu and Escape | PASS | Tested at each mobile/tablet width; correct expanded state and visible navigation. |
| Header Shop destination | PASS | `/shop/` resolves locally and honestly describes its forthcoming status; no active commerce implied. |
| Hero Request a Quote | PASS | Opens independent native quotation dialog. Keyboard cannot move to background controls; browser chrome may receive focus as native browser behaviour. Escape/close return focus. |
| Four hero highlights | PASS | All four present. They are intentionally informational, not broken buttons. |
| Four service cards | PASS | All four links resolve to existing local service pages. Fourth page's scope limitation is listed separately below. |
| Customer Information Highlights | PASS | Unchanged label, heading, introduction and four informational blocks. |
| Section links, footer links and fragments | PASS | Every distinct internal homepage destination returns local HTTP 200; referenced anchors exist. Footer policy disclosure and existing guide route retained. |
| Two Moments photographs | PASS | Mouse click does not change URL or open an enlargement. No links/buttons/tab stops. Captions and optimised image loading remain. |
| Customer Support form | PASS | Required fields, phone/message validation, unchecked consent, support topic and independent success state tested. |
| Quotation form | PASS | Original service categories, endpoint and integration retained; independent subject/state and no-JavaScript fallback tested. |
| Form failure handling | PASS | Mocked rejection, false success, invalid JSON, HTTP 500, network error, timeout, duplicate submission and honeypot cases. Success shown only for an HTTP-success response with explicit provider success. Inputs preserved on failure. |
| Real provider-to-mailbox delivery | NOT TESTED | All requests intercepted; no customer data or actual messages submitted. Provider account configuration and receipt cannot be verified locally. |
| WhatsApp, phone and email links | PASS | Syntax, public business contact consistency and encoded design-sharing message checked. No call, email or WhatsApp message sent. |
| Live social-account destinations | NOT TESTED | Existing Facebook, Instagram, TikTok and YouTube URLs preserved. External account ownership/redirects/availability cannot be confirmed through the restricted network. |
| Order slider start/sequence/loop | PASS | Standard → Express → VIP → Standard; one slide, exactly 4,000 ms between automatic selections, leftward transition and three accessible dots. |
| Touch hold/release/cancel | PASS | Pixel 7 and iPhone 13 Chromium emulation holds current slide and starts a fresh four-second interval after release/cancel; passive pointer events do not prevent scrolling. |
| Hover, keyboard focus and manual dots | PASS | Pause/resume, labelled selection, arrow/Home/End support, full delay after selection and single timer verified. |
| Reduced motion and no-JavaScript content | PASS | No automatic sliding under reduced motion; manual selection remains. All three descriptions remain available without JavaScript. |

Incomplete dedicated pages, separate from homepage defects:

- **NEEDS OWNER DECISION:** develop Garment Care Guide `/guides/garment-care/` and Fabric Guide `/guides/fabrics/` later. Current footer entries are plain text, not broken links. Measurements Guide already uses `/measurements/`.
- **NEEDS OWNER DECISION:** `/services/mobile-fitting/` is valid but covers fitting/measurement arrangements rather than the entire approved styling/event-assistance offering. A fuller dedicated page remains future work.
- **NEEDS OWNER DECISION:** dedicated VIP and Loyalty & Referral pages, and eventual Shop functionality, require their separate approved development phases. No other pages were changed.

## 3. Mobile and browser compatibility

| Check | Result | Actual coverage |
| --- | --- | --- |
| Desktop Chrome-compatible rendering | PASS | Installed Chromium 155.0.8059.79; not branded Google Chrome. |
| Android Chrome behaviour | PASS | Pixel 7 viewport/touch emulation using Chromium only; no physical Android device. |
| iPhone viewport/touch behaviour | PASS | iPhone 13 emulation using Chromium only; this is not iOS Safari testing. |
| Physical Android/iPhone devices | NOT TESTED | Not available. |
| Firefox | NOT TESTED | Neither system Firefox nor Playwright Firefox executable installed. |
| Edge | NOT TESTED | Not installed; Chromium results are not claimed as Edge results. |
| Safari / WebKit | NOT TESTED | No Safari host or Playwright WebKit executable available. |
| Responsive widths | PASS | 320, 360, 390, 430, 768, 1024, 1280 and 1440px. No horizontal page overflow; photographs decode correctly. |
| Layout and sticky header | PASS | Screenshots inspected at 390/1440px; no unexpected overlap in reviewed states. Sixty keyboard steps at each width had no focused control covered at its centre. Section-only captures temporarily put the header in normal flow; deployed CSS is unchanged. |
| JavaScript and local network errors | PASS | No page errors or failed local responses in the exercised states. External requests intentionally blocked/mocked. |
| Touch targets | PASS | Automated WCAG 2.2 target-size scan has no violation. Primary controls and dots have comfortable targets. Small inline legal links and the consent checkbox use text/label context; this is not a claim that every inline link is 44px tall. |

## 4. Performance measurements

**PASS — local Lighthouse 13.6.0 audits**, final runs at 18:25 UTC. Each profile is one laboratory run, not an average, percentile, field result or prediction of deployed response time. Local HTTP Python server, simulated throttling and system Chromium were used. Mobile: 412×823, 4× simulated CPU slowdown, 150 ms RTT / 1.6 Mbps profile. Desktop: 1350×940, 1× CPU, 40 ms RTT / 10 Mbps profile. JSON contains exact settings.

| Measurement | Mobile lab | Desktop lab | Result |
| --- | --- | --- | --- |
| Performance score | 100 | 100 | PASS for these runs |
| Accessibility / Best Practices / SEO scores | 100 / 100 / 100 | 100 / 100 / 100 | PASS for scored automated checks only |
| LCP | 1.74 s | 0.47 s | PASS against 2.5 s lab comparison target |
| FCP | 1.34 s | 0.37 s | PASS as measured; not a Core Web Vital |
| CLS | 0 | 0 | PASS against 0.1 lab comparison target |
| Total Blocking Time | 11 ms | 0 ms | PASS as measured; not INP |
| Initial measured transfer | 180.6 KiB | 361.0 KiB | PASS as recorded; responsive viewport selection differs |
| INP / 75th-percentile field LCP and CLS | Unavailable | Unavailable | NOT TESTED — no CrUX, RUM or Search Console data |

Google's field targets remain LCP ≤2.5 s, INP ≤200 ms and CLS ≤0.1 at the 75th percentile. These laboratory results do not establish that field targets pass. TBT must not be substituted for INP.

**PASS — payload inventory:** HTML 109,720 bytes, including 56,364 bytes inline CSS; external homepage JavaScript 13,929 bytes; 277 bytes inline executable JavaScript. These raw source sizes overlap and must not be added as independent HTML/CSS transfers. No remote webfont, icon font or external runtime script is loaded. A single prioritised responsive hero is requested; below-fold images use lazy responsive loading.

**PASS — full-page loading measurement:** forcing all images to decode produced approximately 313.2 KiB at 390px and 599.9 KiB at 1440px, including navigation and resource transfer accounting on localhost. This is separate from the initial Lighthouse viewport measurement and not a deployed compressed-page measurement.

**NEEDS OWNER DECISION — optional future optimisation:** Lighthouse identifies roughly 4 KiB CSS and 2 KiB JS minification savings, 31 KiB potentially unused CSS and about 9 KiB image-delivery savings. Legacy/shared rules must be audited before pruning so dialogs, no-JS states and future pages are not damaged. Local server caching/compression findings cannot establish Cloudflare behaviour. Check deployed Brotli/cache policies first. No substantial optimisation or visual change was implemented.

## 5. Technical SEO

| Check | Result | Finding |
| --- | --- | --- |
| Title | PASS | `Mr Sewing Fashion | Tailoring & Alterations in Kigali`; unique homepage title. |
| Description | PASS | Accurate Kigali/Rwanda description covering bespoke suits, tailoring, alterations, garment care, work/designs/service information; no keyword stuffing. |
| Canonical and social URL | PASS | Single `https://mrsewingfashion.com/` canonical; matching Open Graph URL. Staging is not made canonical. |
| Production indexing intent | PASS | Source robots `index, follow`, production robots allows crawling and references the production sitemap. No new production noindex rule. |
| Staging noindex configuration | PASS | Existing hostname-scoped X-Robots-Tag rules, plus pages.dev meta override. Local routing simulation confirms staging and branch-preview noindex and no corresponding production header. This is configuration/local evidence only. |
| Actual live indexing headers/status | NOT TESTED | Staging and production CONNECT requests denied with proxy 403 / origin status 000. No origin response was observed. |
| Sitemap | PASS | 160 canonical indexable pages; valid local destinations; excludes intentional noindex pages. Main URL and existing service/project URLs retained. |
| Redirects | PASS | Fifty exact permanent redirects tested locally; no chains; query strings/fragments retained where appropriate. Live edge behaviour not established. |
| Internal links | PASS | Homepage destinations/anchors resolve; whole-site static check covers 6,585 local references. Removing photo links did not delete project routes or sitemap entries. |
| Headings | PASS | One H1, meaningful H2/H3 structure; six process steps are an ordered list. Hidden dialog/success headings do not create additional H1s. |
| Images and alternative text | PASS | Existing meaningful alt text, intrinsic dimensions and responsive sources retained. No broken homepage images in tested states. |
| Structured data | PASS | JSON parses; website and business identity consistent with repository data, no invented reviews/ratings. Postal addresses, contacts/hours retained. Current-handbook verification remains separate. |
| Duplicate metadata/content handling | PASS | Single title/description/canonical, sitewide unique canonical metadata checks and existing legacy URL handling. No new doorway pages. Actual search-engine duplicate clustering is unverified. |
| Open Graph / Twitter | PASS | Matching title, description and official JPEG preview; declared dimensions 1244×802 match the local asset. Image URL is absolute HTTPS and maps to the retained asset. |
| Public preview image retrieval/social rendering | NOT TESTED | The live URL and third-party preview crawlers are inaccessible; no public-retrievability claim. Existing logo aspect ratio is retained rather than inventing a new social image. |
| Crawlable initial content / mobile | PASS | Important copy, links and images are built into HTML. Rendering without JavaScript works; JavaScript does not fetch homepage fragments. |
| Meta keywords | PASS | Existing terms preserved. Google does not use the keywords meta tag for ranking; no frequency-driven additions made. |

## 6. Keyword research and page targeting

**NOT TESTED — current SERP/volume/competition research:** public Google search is denied by the proxy; no keyword provider or Search Console connector is available. The following is an intent-led recommendation based on approved service scope, existing content and owner-supplied historical query themes, not measured search volume or verified current demand. No ranking, competition or traffic numbers are invented. No approved copy was rewritten for keyword frequency.

| Theme / example terms | Likely intent | Appropriate targeting | Result |
| --- | --- | --- | --- |
| Mr Sewing, Mr Sewing Fashion, tailor Kigali, tailoring services Kigali, Kigali tailor shop | Brand discovery / local service overview | Homepage: brand, Kigali/Rwanda, concise service overview and legitimate contact information | PASS — already represented naturally; preserve |
| custom tailoring Kigali, made-to-measure clothing Kigali | Commissioning fitted garments | Homepage service summary; deeper detail on Custom Tailoring & Suits page | NEEDS OWNER DECISION — future page depth |
| made-to-measure suits Kigali, suit tailor Kigali, bespoke suits Kigali | Suit-specific consideration / quotation | Dedicated suits/tailoring page with accurate process/photos; homepage brief mention | NEEDS OWNER DECISION — use “bespoke” only where actual service method supports it |
| clothing alterations Kigali, trouser alterations Kigali, clothing repairs Kigali | Repair/fit problem with local purchase intent | Alterations & Repairs dedicated page; homepage category | NEEDS OWNER DECISION — expand approved actual tasks, not speculative services |
| garment care Kigali, clothing cleaning Kigali | Care/cleaning service discovery | Garment Care & Cleaning page; future care guide for informational intent | NEEDS OWNER DECISION — do not infer unapproved specialist cleaning methods |
| mobile tailor Kigali, office tailoring consultation Kigali, workplace measurements Kigali | On-site assistance | Existing mobile-fitting route then fuller mobile tailoring/styling page | NEEDS OWNER DECISION — explain approved availability/arrangements on its page |
| personal styling Kigali, event outfit assistance Kigali, VIP styling Kigali | Personalised styling / occasion support | Dedicated styling/VIP information, individual quotation; homepage short introduction | NEEDS OWNER DECISION — handbook-backed scope/conditions required |
| tailor near me, tailor shop near me | Proximity / local availability | Accurate visible address, business schema and verified Google Business Profile information | NEEDS OWNER DECISION — location/profile reconciliation; avoid repeating “near me” unnaturally |
| tailoring measurements, garment care guide, fabric selection | Informational research | Measurements Guide and planned guide pages | NEEDS OWNER DECISION — develop useful guidance, not duplicate homepage text |
| Historical owner themes: sur-mesure, seamstress, uniform tailors, “tailer” | Mixed language, service and misspelling intent | Validate with future Search Console evidence; only target services actually approved | NEEDS OWNER DECISION — no blanket service claim, misspelling paragraph or keyword stuffing |

## 7. Verified search visibility

| Check | Result | Limitation |
| --- | --- | --- |
| Search Console indexing, queries, clicks, impressions, CTR, position and errors | NOT TESTED | No authorised Search Console tool/data connection is available. |
| Current Google rankings and indexed snippets | NOT TESTED | Public search inaccessible. Owner-supplied historical queries are not treated as fresh ranking evidence. |
| Business Profile/local pack visibility | NOT TESTED | No connected profile access or live search evidence. |
| Production retains intended repository SEO configuration | PASS | SEO data, canonical policy, sitemap, robots and redirects unchanged. Live server behaviour remains unverified. |

## 8. Accessibility — WCAG 2.2 AA-oriented review

| Check | Result | Evidence / scope |
| --- | --- | --- |
| Automated WCAG 2/2.1/2.2 A/AA rules | PASS | Axe 4.14 scans at 390 and 1440px, homepage and open quotation dialog: zero reported violations. Lighthouse accessibility scores 100. |
| Header label-in-name defect | PASS | Previously detected by Lighthouse; fixed with a whitespace separator and re-audited successfully. |
| Keyboard navigation / visible focus / modal interaction | PASS | Menu/dropdown, quote open/close/return, native modal background exclusion, dots and 60 sequential keyboard positions tested. Focus outlines visible. No centre-point focus occlusion in tested paths. |
| Form labels, validation, consent and status feedback | PASS | Explicit labels, required semantics, valid error/success handling and independent form state tested. |
| Photograph semantics | PASS | Descriptive images/captions, no fake controls or enlargement hint. |
| Carousel movement and keyboard interaction | PASS | Reduced-motion suppression, hold/hover/focus pause and manual labelled dots work. |
| Automated contrast checks | PASS | No machine-reported violation in scanned states. |
| Complete manual contrast / assistive-technology certification | NOT TESTED | Axe marks image-background/other nodes for manual review: colour contrast, three generic-container aria-label cases, and a dialog label case. Inspected screenshots and obvious labels, but did not certify every background pixel, text-zoom state or combination of assistive technology. These are incomplete checks, not proven violations. |
| Real screen readers (NVDA, VoiceOver, TalkBack) | NOT TESTED | No configured screen-reader/device access. Semantic HTML/automated browser checks do not substitute for listening tests. |
| All WCAG 2.2 AA success criteria | NOT TESTED | This is a scoped technical audit, not a blanket conformance declaration. |

No unresolved confirmed critical/serious automated accessibility violation remains. Independent screen-reader and manual contrast review is recommended before a production release.

## 9. Security and privacy

| Check | Result | Finding |
| --- | --- | --- |
| HTTPS URLs and mixed-content source references | PASS | Public destinations/form action use HTTPS; no rendered HTTP resource references. |
| Actual TLS certificate, redirects, HSTS and deployed security headers | NOT TESTED | Live origin access blocked; no TLS certificate or origin headers verified. |
| Explicit repository security-header hardening baseline | FAIL | `_headers` contains only hostname-scoped staging noindex. It does not explicitly set CSP, frame restrictions, nosniff, Referrer-Policy or Permissions-Policy. Hosting may add headers, which is unverified. This is a medium-priority hardening gap, not evidence of an exploited vulnerability. No headers/settings changed. |
| Known secret-pattern scan | PASS | No tracked environment file, recognised private-key block, AWS access identifier, GitHub token or Stripe live-secret pattern found in scanned tracked text. Heuristic scan cannot prove every possible secret/private fact is absent. Values are not included in this report. |
| Public form integration | PASS | Existing browser-intended public access key retained; it is not described as a private server credential. User-provided content is not injected as HTML. |
| Browser-side validation / errors | PASS | Required fields, trimmed message, phone validation, controlled error messages, no raw provider response injection and confirmed-only success. |
| Spam controls | PASS | Existing honeypot and duplicate-request protection tested. |
| Provider rate limiting, domain restrictions, server validation and abuse resistance | NOT TESTED | No provider-admin access, destructive abuse tests or real submissions performed. Client validation alone is not a server-side security boundary. |
| Consent / privacy links / customer data storage | PASS | Consent initially unchecked, legal destinations valid, data sent over configured HTTPS form action, no localStorage/sessionStorage use in homepage JS. No real personal data entered or sent. |
| Retention, access controls, mailbox handling and provider agreements | NOT TESTED | Administrative practices and provider retention cannot be verified in source. |
| Third-party runtime scripts | PASS | None loaded by the homepage. External form provider is contacted only on submission. |
| Website dependency vulnerability audit | NOT TESTED | No project package/lock or Python third-party dependency manifest exists. Static HTML/CSS/JS and standard-library builders have no manifest-based runtime dependency scan to run; this is not proof of zero vulnerabilities. |
| Isolated QA-tool dependency audit | FAIL | Newly installed local-only Lighthouse audit toolchain reports five moderate advisories, zero high/critical. It lives under `/workspace/tools/homepage-qa`, outside the repository, and is not deployed or a customer runtime dependency. No untrusted glob patterns or remote audit target executed. Review/update tooling separately. |
| Business/customer information exposure | PASS | No new photographs, customer identities, policy documents, confidential finances or customer submissions added. Existing public business details unchanged. Full historical repository/privacy clearance is not claimed. |

Recommended header hardening requires a separate scoped proposal: a CSP must account for existing inline scripts/styles and the form endpoint; an untested restrictive policy could break working functionality. Production settings were deliberately untouched.

## 10. Code quality and maintainability

| Check | Result | Finding |
| --- | --- | --- |
| Production build and generated consistency | PASS | `python3 scripts/build_site.py` and `--check`. |
| Static/unit-style Python suites | PASS | All 13 suites pass; `preview_server.py` is a server utility, not a test suite. |
| Browser/integration suites | PASS | Ten: final QA, homepage, homepage-phase1, support-refinements, order-carousel, final-v2, customer-journey, homepage-optimization, phase1 and routing. Logs retained. |
| JavaScript syntax and whitespace checks | PASS | `node --check` for generated and relevant source JavaScript; `git diff --check`. |
| Configured lint / type-check task | NOT TESTED | No package task, linter configuration or typed-project setup. Syntax checks are not represented as ESLint or TypeScript checks. |
| Asset/import/resource consistency | PASS | Existing static asset, image dimension, media inventory, source regeneration and local-link checks pass. |
| Error handling / unnecessary runtime requests | PASS | Form error paths and carousel timers tested; no runtime HTML-fragment fetching or external font/icon dependency. |
| Maintainability follow-up | NEEDS OWNER DECISION | Legacy order-modal/slider delegation and historical preview helpers remain; homepage CSS contains rules for older states. Separate support/quotation forms share JS but duplicate accessible field markup. Prune/refactor only in an authorised follow-up with existing behaviour preserved. No unrelated refactoring performed. |

Only production-code changes: two photograph anchor removals and one header whitespace separator; regenerated homepage follows its sources. Test expectations were updated because gallery links are now intentionally absent. Other pages and image bytes are unchanged.

## 11. Business-content verification

| Check | Result | Evidence / limitation |
| --- | --- | --- |
| Four categories and six-step sequence retained | PASS | Source matches prior approved homepage; order confirmation/payment precedes production. |
| Standard, Express and VIP summaries retained | PASS | Existing conditional wording unchanged; no price, timing guarantee or new benefit. |
| Loyalty / Referral active status | PASS | Prior explicit owner confirmation preserved; no Coming Soon labels added to active programmes, no historical rewards published. |
| Complimentary Photoshoot | PASS | Remains Coming Soon, without invented eligibility or launch date. |
| Shipping/delivery wording | PASS | Retained as enquiries/arrangements, without an invented worldwide guarantee. |
| Public contacts/location/hours vs repository | PASS | Matches current business data: main workshop KN 441 St, Norvège; ordinary Mon–Sat 09:00–17:00, Umuganda appointment exception and Sunday by appointment. Existing phone/email preserved. |
| Terms/privacy/refund destinations and corporate copyright | PASS | Pages exist; exact `© 2026 NINKONIYUMUTWARE NEXUS LTD. All Rights Reserved.` retained and readable. |
| Full comparison with latest approved company policy | NEEDS OWNER DECISION | Missing document: **Master Operating Handbook V8 — latest dated approved sections and later approved addenda**. Neither accessible repository nor the two text attachments contains the handbook. No document connector is available. Cannot certify exact current programme conditions, VIP/order policy, shipping, payment terms, locations or hours against it. This does not imply the owner-confirmed programmes are unapproved. |
| Secondary business-schema location | NEEDS OWNER DECISION | Existing structured data also retains MIC Building, Downtown. Confirm its continued public business status against V8; no address was removed or invented. |

## 12–13. Outstanding items and severity-ranked recommendations

| Priority | Result | Action |
| --- | --- | --- |
| Critical/high confirmed local defects | PASS | None found in exercised paths. This does not turn untested remote checks into passes. |
| Medium: live staging and delivery evidence | NOT TESTED | Verify Cloudflare publishes the pushed SHA; confirm actual staging noindex/TLS/security headers; perform an authorised non-customer test with mailbox receipt evidence. No false-success claim. |
| Medium: current handbook reconciliation | NEEDS OWNER DECISION | Provide/access the exact V8 approved addenda and confirm current business/schema details. Preserve owner-confirmed short programme copy meanwhile. |
| Medium: security-header hardening | FAIL | Source baseline lacks explicit hardening policy. Propose/test a compatible policy separately; do not silently alter production. |
| Medium: unavailable browser/assistive-tech checks | NOT TESTED | Complete real iPhone Safari, Firefox/Edge and representative screen-reader/manual contrast checks where access becomes available. |
| Low: future dedicated pages | NEEDS OWNER DECISION | Schedule guide, styling/VIP and programme pages after homepage sign-off; keep pending guide entries unlinked. |
| Low: isolated audit tooling advisories | FAIL | Update/replace the local QA toolchain as a separate tooling task; do not add it to production dependencies. |
| Low: payload/legacy cleanup | NEEDS OWNER DECISION | Consider measured CSS/JS/image and cache improvements only after confirming deployed behaviour and regression impact. |
| Search visibility evidence | NOT TESTED | Connect authorised Search Console/field metrics to verify indexing, queries and real-user performance; no rankings or search volume invented. |

## 14. Evidence and reproduction

Evidence directory: `/workspace/artifacts/homepage-final-qa/`.

- `lighthouse-mobile.report.html` / `.json` and `lighthouse-desktop.report.html` / `.json`: final laboratory reports; `performance-summary.json` includes settings and measurements.
- `functional-accessibility.json`: eight viewport results, metadata/headings/schema, internal destinations, unavailable browser executables and axe incomplete checks.
- `keyboard-review.json`, `full-page-payload.json`, `source-security.json`, `preservation.json`, `tool-vulnerability-audit.json`.
- `homepage-390.png`, `homepage-1440.png`; `moments-*`, `support-*`, `footer-*`, `orders-*` section captures. Screenshots are local rendered evidence, not proof of live Cloudflare publication.
- `logs/`: build, Python, ten browser suites, tool installation/audit and public access failures. External denied requests record proxy CONNECT 403 and origin status 000, not an origin HTTP 403.

Reproduce using the repository's Python preview server and installed Playwright/system Chromium. The final QA test expects the external audit-only axe tool at `/workspace/tools/homepage-qa/node_modules/axe-core/axe.min.js`; it is not a production dependency. Previous tests use installed environment tools as described in `tests/README.md`.

## 15. Staging publication

**PASS — branch isolation:** work and commits are on `phase1/customer-journey-repairs`; exact implementation SHA recorded above. GitHub push confirmation and remote SHA are reported in the completion message after publication attempt.

**NOT TESTED — Cloudflare build/publication and remote rendering:** the established staging workflow may run after push, but this environment cannot observe its deployment. Staging requests are denied by the enforced outbound destination policy. No Cloudflare settings/custom domains changed and no publication success is inferred from GitHub push alone.

## 16. Homepage baseline and production protection

**PASS — production unchanged by this work:** remote main remains `ba27bab0425a9df1948fe8f45dd3b941cb322f4c`; no merge, reset, rebase, main commit/push, live deployment, hosting or domain change performed. Live page equality cannot be independently fetched through the blocked network, so this statement describes our actions and verified remote main/config preservation, not a successful live crawl.

**NEEDS OWNER DECISION — protected baseline:** this is a baseline candidate, not a signed-off homepage. After explicit owner sign-off, record the exact approved branch-head SHA, screenshot/evidence bundle and limitations, then establish the protected baseline. No approval tag or declaration is created prematurely.

Baseline component inventory: `_templates/homepage.html`, `homepage-header.html`, `homepage-sections.html`, `homepage-footer.html`, `homepage-quotation.html`, `homepage-phase1.css`, `homepage-interactions.js`, `homepage-corrective.js`, `order-carousel.js`; `scripts/build_homepage.py`, `scripts/homepage_resources.py`, shared site/navigation/SEO helpers; `_data/homepage-guides.json`, `_data/page-seo.json`, `_data/business.json`; generated `index.html`, `assets/homepage.js` and the existing responsive media assets.

Preserve the approved black/gold/cream layout, typography, logo, all current text/photos, header/footer, forms and navigation. Future pages may reuse components; a shared change that affects the homepage requires an explained impact and owner authorisation before implementation, plus regression testing. Necessary bug/security/maintenance changes must have their effects reviewed. Do not silently change the homepage while building another page.

Stop here for owner review. No other page development or production deployment is authorised by this report.
