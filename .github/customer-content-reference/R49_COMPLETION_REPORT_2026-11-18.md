# R49 — Custom Tailoring completion and prepared complete release

Owner authorization:13November2026. Implementation resumed and reviewed18November2026. Development branch:`phase1/customer-journey-repairs`.

## Status and critical release gate

The complete R35–R49 candidate is prepared on staging. **Production release is blocked pending actual deployed staging verification.** The owner already authorized production after critical checks; no second production approval is requested. The managed workspace proxy rejects CONNECT to Pages/live domains with403 before reaching the origins. Chromium reports `ERR_TUNNEL_CONNECTION_FAILED`. The supported environment configuration update returned `CONFLICT / draft_not_editable`; no network change was applied. This is not an origin403 or evidence about Googlebot.

Staging entry:[Custom Tailoring](https://mrsewing-staging.pages.dev/services/custom-tailoring/). Provider deployment and exact candidate SHA are recorded in the final deployment evidence after commit. This document deliberately does not invent a self-referential commit SHA or claim rendered staging success.

Production baseline remains `4d972f29417fa60366ebdb6348e1599208f6ae08`. No main push, production merge, live settings change, real enquiry, WhatsApp message, call, payment or private-service activation was performed. See `R49_NETWORK_ACCESS_PROPOSAL.json` for the specific execution-environment access needed to finish mandatory live checks.

## Completed customer journey

Existing routes remain: `/` → `/services/custom-tailoring/` → `/mensuits/` or `/womensuits/` → existing category → `/collections/designs/{existing-slug}/` → `/services/custom-tailoring/selected-designs/` → `/services/custom-tailoring/fabric/?multiple=1` → `/guides/fabrics/` in selection context where requested → `/request/` → existing review → explicit submission. Flow parameters preserve independent quotations. Advice/own-fabric customers skip fabric browsing. Special Tailoring retains `/services/custom-tailoring/special-order/` and the existing manual WhatsApp picture arrangements.

- One or many approved designs, including mixed men/women/Kaunda/tuxedos, retain canonical original photographs, internal identities and quantities. Customer summaries/messages omit unnecessary technical codes.
- One shared fabric preference and, if selected, one shared fabric/colour apply to the enquiry, subject to professional suitability assessment per garment. The expanded central palette has49 named colours plus Other Colour with an optional validated description. Accessible named circular controls, groups and selection indicators remain; swatches do not establish stock. See `R49_COLOUR_PALETTE.md`.
- Fabric Guide remains about approved reference labels/tiers, existing photographs, concise details and selection; no separate suit-price schedule or unrelated promotion paragraphs. No new exact fibre composition, certifications, fabric-specific colour inventory, stock or performance guarantees were invented. Original supplier specifications/handbooks remain unavailable; prior recorded general-textile citations and limitations remain intact.
- Suit and Special forms use the same six-section framework: Your Order; Your Information; When Do You Need It?; Measurements & Fitting; Delivery or Collection; Review Your Request. Existing field nodes, consent, review, provider and security validation are reused.
- Suit order summary is compact and expandable with exact photographs/quantities and edit links. Fabric/colour are read-only with edit access. No repeated garment-type/fabric/priority/after-hours questions.
- Special form has one garment-type question (shirt, trousers, dress, skirt, jacket, coat or Other), quantity, design description, fabric preference and optional Additional Information. No new uploads or duplicate form/provider.
- Contact requires name, phone/WhatsApp, country and city; email optional. No street address in contact section. Future completion date/time is mandatory, explicitly Africa/Kigali UTC+02. Terms/Privacy remain mandatory.
- Workshop measurement appointments collect location/date/time; MIC Downtown is by appointment. Requested representative visits collect address/date/time and an explicit independent-consultation or order-related purpose. Online option links to the Measurements Guide without requiring measurements before initial quotation. Preferences do not confirm availability or make payment due.
- Delivery/collection requirements depend on method/country/city. Kigali eligible suit delivery is included, address optional at enquiry and confirmed before dispatch. Outside-Kigali Rwanda address required; eligible Custom Tailoring delivery calculated at quantity ×5,000RWF. International address required and shipping individually quoted. Collection asks location without requiring an address. Stale hidden fields are not submitted as applicable arrangements.
- Final review shows order/photos/quantities/fabric/colour/contact/deadline/provisional status/measurements/appointment/receipt preferences and clearly qualified calculated charges. Submission requires unchanged reviewed data and consent. Failed submissions preserve entries. Only positive provider responses show “Request Submitted for Review”, the approved contact acknowledgement and “Your order and requested completion date are not yet confirmed.” Provider acceptance does not establish staff-inbox receipt, order acceptance or production start.

## Approved fees and commercial preservation

| Subject | Current rule |
| --- | --- |
| Independent Consultation & Fitting |35,000RWF, replaces25,000 only for this service |
| Eligible order-related Kigali measurement visit |10,000RWF after accepted garment quotation and required advance; unchanged |
| Same approved measurement service |Do not charge both visit fees; choosing a preference alone does not require payment |
| Eligible Custom Tailoring delivery elsewhere in Rwanda |5,000RWF per garment; calculated amount distinguished from accepted quotation |
| Initial eligible Kigali ordinary-suit delivery |Included; no duplicate charge |
| International shipping |Individually assessed/quoted; no fixed fee or transit promise |

All16 ordinary-suit and4 tuxedo prices remain unchanged from the latest owner-approved tier sources. Men's two/three-piece:Tier1 600,000/800,000;Tier2 400,000/550,000;Tier3 300,000/400,000;Tier4 250,000/300,000RWF. Women's:500,000/550,000;350,000/400,000;220,000/270,000;150,000/200,000RWF. Tuxedos:800,000/1,000,000 and600,000/800,000RWF. Four ordinary-suit tier/price/benefit tables, cleaning/gifts, approved child/bulk eligibility, no discount stacking, domestic70%/30%, international100%, Express35% and additive after-hours rules remain intact. Alterations/Care round-trip transport and other service fees were not assigned the new delivery rate.

## Express handling and recovery

Ordinary provisional assessment is `requested deadline − current time −24hours`:at least7days planning is Standard; less is Express. Exact boundary is inclusive. Invalid/past deadlines are rejected. Standard shows no Express notice. Special garments require human assessment; the ordinary threshold is not applied. No automatic surcharge or accepted completion promise follows screening.

Express presents WhatsApp, Call Us and Continue Quotation Request. Calls open `tel:+250787411501`; WhatsApp uses existing company consent/manual-send handling. Complete names/photos/quantities/fabric/colour/deadline are prepared; long requests use explicit complete multipart/manual-copy fallback rather than dropping designs. No action sends a message automatically.

Choosing WhatsApp/Call stores an independent order-only recovery snapshot in same-browser localStorage for exactly86,400,000ms. It preserves canonical selections, shared fabric/colour, deadline, country/city and non-sensitive measurement/appointment/receipt preferences. It excludes name, phone, email, full visit/delivery addresses, location details and free-form additional/design text. Existing contact drafts remain separate30-minute per-tab data. Expiry is persisted and checked on return; explicit restore creates a new quotation flow without reviving browsing selections. Legacy single-design URLs now gain a stable quotation session before draft initialization; repeat contacts/reload reuse the same recovery. Independent enquiries are isolated. Storage failure gives honest keep-page-open guidance. Clearing browser data prevents recovery; no cross-device guarantee.

Normal120-second browsing departure expiry, scoped floating review visibility, quotation closure and Back/Forward protections remain. Sharing does not itself erase selections. The floating bar never reappears on quotation/fabric/review/unrelated pages simply because recovery exists.

## FAQs, Terms, privacy and sources

`R49_POLICY_RECONCILIATION_2026-11-13.md` lists all16 required directly linkable FAQ subjects and exact anchors. Existing topic ownership, search, FAQ schema and Terms anchors are preserved. Added/reconciled explanations cover production-start notice; Standard/Express/urgent assessment; customer delays; conditional quotation targets; measurement choices/locations/35k/10k; online measurements; Kigali/outside-Kigali/international delivery; collection; and enquiry versus acceptance.

Quotation targets:Express24hours; Standard24–48hours, subject to operating hours, sufficient information and assessment. Production time starts official production-start notice. Customer delays can require reassessment; Express charges require agreement. Privacy distinguishes24-hour order-only recovery from the30-minute contact draft. No cancellation/refund/legal entitlement was invented. New reference version `2026-11-18-01` records approval13November and implementation18November, while preserving original documents and source-coverage limitations.

## Accumulated staging improvements included in the prepared release

`R49_RELEASE_RECONCILIATION_2026-11-13.md` audits every one of14 R35–R48 commits, not only this latest form delta:mobile service pricing/payment cards; current four tier/benefit tables and price consistency; sticky non-interactive75-second OFFER; third Special Tailoring action; concise category landings; specifically authorized eight Kaunda images/gallery; two-level SEO; image/name-only category cards; sharing/compact selected review; same-category and diverse same-gender recommendations; required selected-suit quotation data;120-second browsing sessions; favicon/real404/indexing work; and shared fabric/colour journey. All are retained in the staging candidate.

Main was an ancestor of staging with zero production-only commits at audited tips. CNAME, production public-API/CORS configuration, production robots, intentional noindex routes, Shop publication gates and disabled private backend are protected. No migration, new paid dependency or payment/private binding activation. After actual staging verification, re-read remote main; use a normal fast-forward if ancestry remains valid, otherwise preserve/reconcile newer production work and retest. Never force-push or bypass protection. Verify both GitHub Pages static and Cloudflare main API deployments and live behavior; keep staging coordinated afterward.

## Verification evidence

Passed current-candidate checks:

- `python scripts/build_site.py` and `python scripts/build_site.py --check` — generated outputs synchronized, including Cloudflare preview bundle.
- `python tests/custom_tailoring_release_preservation.py` —294 HTML metadata/image identities and556 protected files, only scoped owner-approved exceptions.
- `python tests/seo_preservation.py` —64 canonical public pages, unique titles/canonicals, description/H1/alt, JSON-LD syntax, actual local link targets, page-specific search intent and host-scoped staging noindex rules.
- `python tests/sitemap_discovery.py` —64 intended canonical routes, no forms/private/draft/indexing disagreement. Nine additions since main55 are approved Kaunda category/eight designs.
- `python tests/pricing_benefits.py` —16 ordinary/4 tuxedo amounts, correct tier benefits/FAQ sources, no fabric suit-price schedule or obsolete ordinary men's prices.
- `python tests/customer_policy_review.py` —current fees/times/payment/additive surcharges, exact FAQ search anchors, privacy distinctions and private feature disabled.
- `node tests/quotation-completion-validation.mjs` —ordinary/Special typed backend, future Kigali deadlines/boundary, conditional measurement purpose/address/location, delivery calculations, complete canonical selections, security/consent/body-size/provider-failure cases and backward compatibility.
- `node tests/selected-suit-refinement.mjs`, `node tests/selected-photo-validation.mjs`, `node tests/multi-design-validation.mjs`, `node tests/shared-fabric-validation.mjs` —single/10/all approved designs, every exact photograph and quantity, central50colours, optional Other, canonical reconstruction, no silent truncation, invalid data rejected before mock provider.
- `node tests/main-api-cors.mjs` —production apex CORS/preflight, foreign host/origin/private-path rejection and actual underlying validator retained. Legacy fixture updated for the already-required contact/deadline contract.
- `node tests/shop-draft-request-gate.mjs`, `python tests/public_enquiries.py` —unapproved product-sale gate retained; no actual messages.
- `python tests/business_schema.py`, `python tests/shared_components.py` —verified business locations/hours/schema/shared component preservation.
- `node tests/selection-session-expiration.spec.cjs` —simulated60/121seconds, Back/Forward/stale history, mixed9categories, independent closed quotation and new-selection flows, all8widths320/360/375/390/430/768/1024/1440. No real external action.
- `node tests/custom-tailoring-completion.spec.cjs` —PASS scenarios1–24 at320/375/390/768/1440; ordinary/Special, legacy identity, appointments/delivery,24-hour recovery, complete mock payload and failure preservation. Four axe checks, four mocked provider calls, zero browser errors or missing resources. External actions were blocked/mocked. After the final redundant-heading removal, a targeted five-width DOM/layout/review smoke also passed with zero errors, preserving Additional Information; see heading-browser.json.
- Wrangler Pages emulation compiled Worker successfully and parsed50redirect/2header rules. Local GET probes returned200 for all14 tested valid pages/assets, including favicon, and404 for a deliberately missing route. Host-qualified live staging headers cannot be established from localhost.
- `git diff --check` passed.

Earlier diagnostic failures were fixed and rerun:legacy null-wrapper exception; early legacy recovery identity/init ordering and deferred arrangement restoration; redundant legacy Additional Requirements heading; and outdated current-policy/CORS/optional-Other fixture expectations. Two older scope-lock suites were also tried and remain intentionally inapplicable to this full release: `tests/customer_information.py` assumes the earlier cotton/suppressed-price/sitemap55 policy baseline; `tests/technical-seo-repair.py` forbids every change beyond the earlier icon-only task. Their initial failures were not application failures and were not hidden by weakening them. Current294HTML/556file preservation, pricing, policy, sitemap and SEO suites enforce the R49-approved scope instead.

Synthetic complete10design/12garment input and validator-produced provider data are in `R49_SYNTHETIC_ENQUIRY_EXAMPLE.json`;1737-byte envelope, no live provider call. Test evidence and screenshots are under `/workspace/review/custom-tailoring-release-2026-11-13/` and `/workspace/artifacts/custom-tailoring-completion/`. Browser tests use mocked WhatsApp/calls/provider and synthetic data; no staff-inbox delivery or real phone interaction is asserted.

## SEO and remaining checks

Preserved approved titles/descriptions/canonicals/alt, shared identity, page-specific intent, internal destinations, structured business facts, sitemap/robots and deliberate transactional noindex. Special visible heading/breadcrumb and FAQ schema content changed only for approved clarity; no generic keyword rewrite. Square/root approved-logo favicon, exact historical aliases, real404 boundaries and Kaunda discovery remain. LocalBusiness syntax is checked, not Google rich-result eligibility.

Actual deployed staging mobile/desktop behavior/headers, production HTTP status/canonicals/assets, HTTP-apex/www permanent redirect destinations and Googlebot responses remain unverified because of the proxy. Do not request indexing of redirect URLs or claim Google indexing/ranking success. After legitimate network access, verify deployed staging first; then publish the complete tested release only if critical checks pass, inspect both production deployment paths and actual live behavior, and monitor Search Console sitemap, page-indexing/crawl/error/redirect reports over subsequent days/weeks. “Discovered—currently not indexed” and “Crawled—currently not indexed” still have no established single cause.

Known limitations remain:continuous OFFER motion has reduced-motion support but no user-controlled stop by owner instruction; full motion accessibility compliance is not claimed. Exact fabric composition/stock/colour inventory and inaccessible original handbooks remain unverified. No unrelated Alterations, Care, Mobile or VIP redesign was started.

Complete candidate changed-file list:`R49_CHANGED_FILES.txt`. Exact staging SHA/provider URL/status and unchanged remote main SHA are supplied in final deployment evidence. Final release status: **Completed on staging; production release blocked by mandatory rendered staging verification access** if the documented network gate remains unresolved.
