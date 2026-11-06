# Mr Sewing Fashion — Version 2 implementation, QA and staging review

6 November 2026 · Development branch `phase1/customer-journey-repairs` · Implementation baseline `9bd678ff5760a5446cf1c151b89b6ee4f9b596aa`.

**Recommendation: READY FOR OWNER STAGING REVIEW. Production publication is not authorised or recommended until the external delivery/policy checks below are completed.** No main merge, production/DNS/environment change, paid service, payment gateway, draft merchandise publication, subscription activation or PDF publication.

PASS means successfully checked in the stated environment; FAIL means tested failure; NOT TESTED means no verification; NEEDS OWNER DECISION means missing approval/evidence. Local/mock verification is distinct from live delivery and staging HTTP verification. Final delivery supplement records the exact pushed SHA/deployment URL and direct-origin result.

## Requirement-by-requirement results

| Requirement | Implementation / routes | Principal source files | Current result and evidence |
|---|---|---|---|
| Inspect/source audit | Read current reference, approved V2 brief and attachment; permanent R22/page brief/source audit updated | AGENTS.md; customer-content-reference README/manifest/2026-11-06-15; V2_IMPLEMENTATION_PAGE_BRIEF.md; V2_CUSTOMER_INFORMATION_AUDIT.md | PASS available-source inspection. NEEDS OWNER DECISION for inaccessible original policy archives/legal verification; no exhaustive-source claim. |
| Remove visible gallery pause | Homepage: three original source-driven RTL galleries retained; no playback button. Reduced-motion/no-JS fallback; visible instruction supports Escape and touch-on-container stopping, hover/focus pause | scripts/homepage_galleries.py; _templates/homepage-galleries.js/.css | PASS default movement, no photo links, mobile widths, reduced motion, Escape and synthetic touch-pointer event. No alternate visible pause button. Physical touch/device testing NOT TESTED. |
| Photo URL only | Collection and Our Work use the same `/request/` form after fabric; selected/review area shows original canonical URL and no image preview; exact secondary photo remains selected | _templates/customer-refinements.js; customer-site.js; selected-design.js; scripts/selected_designs.py; selected-design-handler.js | PASS men/women + Our Work second-photo journeys, review/edit/fabric changes, named WebP encoding and actual server validator with mocked provider. No files/attachments/Base64. |
| Three fabric choices | `/services/custom-tailoring/fabric/`: Choose Fabric, Help Me Choose Fabric, I Have My Own Fabric. `/guides/fabrics/` own-fabric entry preserves an existing design or opens general Custom enquiry. Existing optional description records fabric details | customer_site.py; request-context.js; customer-site.js; scripts/edge/customer-requests.mjs; selected-design-handler.js | PASS all three paths/payloads, own-fabric description, exact photo preservation, standalone Guide entry, no forced fabric selection for advice/own. Category derives from approved design/project, fixing direct-link mismatch. Suitability remains subject to assessment. |
| Measurements CTA | `/measurements/`: one Submit Measurements link after all ordered photographs/instructions → `/measurement-submission/` | scripts/customer_site.py | PASS placement/count/destination, existing images/order/enlargement retained, responsive/Axe checks. Actual measurement email receipt NOT TESTED. |
| Duplicate service actions | Alterations, Garment Care, Mobile Assistance each retain exactly one Request Service link in the approved hero to their own dedicated form | scripts/customer_site.py | PASS all three hero/destination counts and existing service form regression. Images/hero layouts retained. |
| VIP subscription | `/request/vip-subscription/`: separate individual/family enquiry, unrestricted actual people count, care/alterations requirements, frequency/location/notes/contact/privacy, review/edit and existing provider. VIP page links to it; old subscription route remains informational with a genuine enquiry link | scripts/v2_pages.py; customer_site.py; customer-site.js | PASS family17, invalid zero, service/context/email payload, unchecked consent, rejected and accepted mock provider responses. No subscription/contract/price/payment commitment. Actual inbox receipt NOT TESTED. |
| Searchable FAQs | `/faq/` plus existing 14 topics/77 answers: full search answers, Copy Answer, Copy Answer + Link, View Original Source. Canonical sources are original published FAQ topic/fragment URLs; no internal documents | scripts/faq_help.py; faq-actions.js; faq-help.js; faq.css; _data/customer-faqs.json | PASS exact copy payloads, clipboard error feedback, source/fragment checks for all77, search/synonyms/no-results/keyboard/no-JS/back/refresh and responsive regression. No new VIP contractual FAQ. Live production-source HTTP NOT TESTED. |
| Media Kit | `/media-kit/`: verified company/Kigali identity/services/public contacts, two permission-approved existing project images, media/collaboration enquiry, bilingual PDF pending; no download URL | scripts/v2_pages.py | PASS responsive/heading/links/Axe and local metadata checks. No draft PDF or invented claims. NEEDS OWNER DECISION for final PDF, reuse permissions, placement and publication. Page remains noindex proposal. |
| Customer information | Current general Terms/Refund/Privacy content retained; two obsolete experience-selection sentences corrected in general guidance and mobile service to the existing direct-service journey | _data/customer-release.json; V2_CUSTOMER_INFORMATION_AUDIT.md | PASS available-reference reconciliation/content preservation. NEEDS OWNER DECISION for original-source gaps, unsettled refund/legal/privacy/provider/retention questions. No legal compliance asserted. |
| Preserve existing work | Shop, booking HTML/consultation script, programmes, original project photographs, catalogue and private-disabled flag protected | existing Shop/source validation; tests/v2_preservation.py | PASS byte comparisons for protected artefacts, original-image tests and existing customer journeys. Shop server-only staging snapshots remain unchanged; drafts excluded from production catalogue/API. |
| Technical QA / SEO | 22 existing sitemap routes; 27 canonical pages inspected including new noindex pages; FAQ source pages separately tested | existing site_seo.py/_headers/robots/sitemap; local audit/test logs | PASS metadata uniqueness, H1/canonicals/JSON-LD/social tags/alt/local links and source indexing configuration. Staging origin HTTPS/header/HTTP verification separately stated. No sitemap submission or ranking claim. |
| Homepage Payment Methods | New section before Customer Support using the same original generic symbols as Shop: Mobile Money, Bank Transfer, Cryptocurrency; manual instructions only | scripts/payment_methods.py; build_homepage.py; homepage.html; payment-methods.css | PASS three labels/symbols, responsive/Axe/Lighthouse. Homepage sections/SEO/non-gallery interactions remain identical to approved baseline. No payment activation. |
| Delivery control | Only development branch; generated assets and Functions compiled; release marker labelled V2 staging owner review | build_release_marker.py; build-info.json; delivery supplement | Exact commit/Cloudflare check/direct staging result recorded after push. Owner review required before any production action. |

## Test evidence

- PASS production build and deterministic `--check`; Python compilation and changed JavaScript syntax checks. No separate TypeScript or lint configuration exists; no lint/type success is invented.
- PASS 19 Python regression suites, including 22-sitemap-page inventory with 1,120 existing local links/resources, clean aliases/schema, asset preservation and publication gates.
- PASS new V2 browser suite: all fabric options + Guide selected/general entry, URL-only review/email payload, VIP family17 and invalid0, provider rejection/acceptance, FAQ exact copy/source/error/no-results, measurement placement/service actions, homepage payments and gallery behaviour; seven widths 320/360/390/430/768/1024/1440 and five Axe-tag scans.
- PASS original collection men/women and Our Work selected-photo journeys, five distinct service enquiries + Special, support consent, seven widths and five Axe scans. Exact selected image URL is validated on the server, not trusted from the browser.
- PASS existing homepage regression: seven widths, source/loop geometry, right-to-left motion, reduced motion, five support provider states/duplicate protection, same-page Terms, booking and two Axe scans.
- PASS consultation:24 Yes/No/design-link/provider cases, review/edit/service switching and four widths. No WhatsApp/file-upload regression.
- PASS FAQ regression:14 destinations/77 anchors,60 responsive combinations, canonical/schema/header/footer, search/synonyms/back/refresh/legacy bookmarks, native keyboard/no-JS topics. Historical test expectations for already-approved programme activation/Terms fallback were corrected.
- PASS Shop through actual local HTTPS Worker:21cards/147image loads, seven widths, categories/search, product-only enquiry/Terms, accepted manual payment preference and two Axe scans. Existing commerce fixture suite passed seven widths/eight Axe scans, cart/checkout/quote/referral and mocked provider errors.
- PASS security regressions:22 approved design/project photo mappings; foreign/external/mismatched URL rejection; own-fabric stale-stock removal; all original host/consent/honeypot/provider-failure checks. Twelve private-backend local test groups passed with synthetic images/temporary SQLite and external services mocked. Private features remain disabled; this does not verify cloud storage/account configuration.
- No real customer data, messages, payments, uploads or real business inbox tests were used. A stopped local Worker was restarted for Shop checks; obsolete legacy test expectations were updated only where prior/current owner decisions explicitly superseded them. Resolved issues include direct-link fabric-category derivation and missing source-action attachment on original FAQ answers.

## Performance measurements

Single local simulated-mobile Lighthouse runs (not field Core Web Vitals, live-production scores or a 75th-percentile result):

| Page | Performance / Accessibility / SEO | LCP | FCP | TBT | CLS | Initial transferred bytes |
|---|---|---|---|---|---|---|
| Homepage | 98 / 100 / 100 | 2.25s | 1.57s | 72ms | 0 | 236,651 |
| FAQ | 98 / 100 / 100 | 1.50s | 1.50s | 136.5ms | 0 | 178,634 |

Initial transfer excludes lazy images not requested in that run. Field INP and real-user distributions are unavailable. Formal WCAG certification and physical Android/iPhone/Safari/Firefox/Edge/screen-reader checks are NOT TESTED; automated scores do not replace those checks. No substantial image/design optimisation was introduced.

## Outstanding conditions before publication

| Item | Status | Required verification/decision |
|---|---|---|
| Direct Cloudflare preview rendering, HTTPS and headers | NOT TESTED until delivery attempt; environment proxy may block | Open exact new preview; verify payment section, URL-only selected request, three fabric paths, VIP subscription, FAQ actions and Media Kit. Deployment success alone is not UI verification. |
| Provider acceptance/business-inbox receipt/email link rendering | NOT TESTED live | Controlled labelled synthetic enquiries with approved contact details through selected-design, subscription, consultation and support; confirm recipient inbox, all fields, exact photo URL, reply-to and no attachment. |
| Original company source and legal/privacy coverage | NEEDS OWNER DECISION | Supply/verify named original archives; reconcile exact fabric-unavailability/refund exceptions, retention/deletion/provider arrangements and Rwanda legal requirements. Existing approved prices are not being re-requested. |
| VIP final commercial/contract terms | NEEDS OWNER DECISION | Pricing/allowances/visit definition/billing/cancellation remain deliberately unfinished. Enquiry works without activating a membership. |
| Media Kit PDF and publication/reproduction approval | NEEDS OWNER DECISION | Approve final bilingual document/assets; upload/link only later. No fake download is present. |
| Shop commercial publication | NEEDS OWNER DECISION | Existing21candidates remain staged and protected; no missing rights/specifications/prices/stock are invented or published to production. |
| Remote private storage/staff features | NOT TESTED remotely | Keep disabled. Verify bindings/private access/auth/abuse/privacy/inbox prerequisites before any future activation. No current UI depends on enabling them. |
| Full browser/device/assistive-tech and field performance | NOT TESTED beyond local Chromium | Owner device review and subsequent targeted compatibility/field checks before production. |

No unresolved failing code test remains in the performed final checks. Staging is ready for owner review; production readiness remains conditional on the above evidence and explicit owner authorisation. Do not merge main, publish production, activate paid services or submit the production sitemap.

## Evidence and files

Machine-readable evidence and logs are in `/workspace/review/v2/`: browser.json, python-results.json, seo-audit.json, faq-source-coverage.json, performance.json, build/parity and individual suite logs. Screenshots in `/workspace/artifacts/v2/` are local browser evidence, not screenshots of a directly verified Cloudflare origin. Selected-design screenshots also appear in `/workspace/artifacts/final-journeys/`.

The delivered report includes the complete changed-file list and final deployment evidence. This repository report is preserved with the implementation commit; its own SHA is supplied by the delivery supplement to avoid a self-referential commit hash.
