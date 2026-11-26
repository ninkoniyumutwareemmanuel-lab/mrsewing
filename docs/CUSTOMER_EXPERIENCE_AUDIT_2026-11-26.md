# Customer-experience, SEO and integration audit — 26 November 2026

## Scope and immutable baseline

Authorized implementation branch: `phase1/customer-journey-repairs`. Initial staging commit: `b388644796fcb24b747bb6818dd211422fab9cff`. Main and production are read-only for this assignment. This report concerns the new comprehensive 26 November assignment; the earlier recovery report remains preserved.

Read sources: root `AGENTS.md`; `.github/customer-content-reference/README.md`; current `versions/2026-11-25-01` customer master, policy source matrix, unresolved register and page map; source map; actual build, customer interaction, Meta, route, SEO, policy, media, request and Shop implementations. Original private company handbooks, ChatGPT Library documents, Cloudflare account settings, Search Console and advertising accounts were not accessible and are not represented as independently inspected.

The full initial route inventory was extracted from the immutable initial Git commit, not a working tree being edited by other agents. `scripts/audit_customer_experience.py` records **305 generated HTML routes/aliases** and **64 sitemap-listed canonical routes**. Its JSON includes every route's purpose, title, H1/H2, description, canonical, robots, sitemap inclusion, actions, complete internal/external links, image alt/dimensions/loading, forms/field names/required status, JSON-LD types, visible-content excerpt and static findings. Hidden form values and credentials are deliberately excluded.

Internal evidence is stored outside the deployment root:

- `/workspace/review/2026-11-26/before/route-inventory.json`
- `/workspace/review/2026-11-26/before/route-inventory.md`
- `/workspace/review/2026-11-26/before/seo-page-map.json`
- `/workspace/review/2026-11-26/before/three-tailoring-pages.json`
- `/workspace/review/2026-11-26/before/browser/results.json`
- `/workspace/review/2026-11-26/before/browser/*.png`
- `/workspace/review/2026-11-26/acceptance-checklist.json`

Reproduce initial inventory:

```sh
python scripts/audit_customer_experience.py --revision b388644796fcb24b747bb6818dd211422fab9cff --output /workspace/review/2026-11-26/before
```

Reproduce final generated-tree inventory after building:

```sh
python scripts/audit_customer_experience.py --output /workspace/review/2026-11-26/after
```

The script rejects an evidence output directory inside the deployable repository. The existing Pages middleware excludes `docs`, `scripts`, `tests` and other internal roots on staging; a public Git repository is still public, so no confidential records or credential values belong in this report or Git history.

## Confirmed initial findings

- **124 generated pages contain visible technical `MS-` identifiers**, including individual design presentation. IDs must remain in validated data/URLs/backend relationships while customer captions, headings and SEO text are cleaned.
- No unresolved static local link target was found in the full HTML inventory. Unicode asset names are decoded correctly. This does not prove external links, deployed redirect behavior or every fragment; run the separate rendered-fragment test after implementation.
- All parsed JSON-LD blocks are syntactically valid. This is not a Google rich-result or schema-vocabulary certification.
- The three primary tailoring pages have independent production canonicals, unique titles/descriptions, one H1, `index, follow` source directives and sitemap entries. Actual Google indexing is **BLOCKED / unverified** without Search Console. Staging runtime noindex and host-specific HTTP header safeguards are distinct from production source eligibility.
- Current Showroom/source data has publication and provenance gates. A reference design is not verified Mr Sewing workmanship. A `Made by Mr Sewing` mark must derive only from verified completed-work evidence; unknown origin remains unconfirmed.
- Existing request infrastructure already has shared selection, separate browsing/quote state, server-reconstructed photograph validation, quantities, review, consent and provider-positive acknowledgements. It should be reused by the guided dialog, not replaced by a competing enquiry implementation.
- Existing individual-selected-design summaries and fabric controls are large. Baseline pages are captured before changing layout, including empty-state visits; seeded multi-design screenshots require the task's functional browser suite.
- The current R65 dialog embeds the existing quotation/booking form. It does not by itself provide the complete guided design→fabric→review journey requested on 26 November.
- Shop is an enquiry-oriented catalogue with separate publication rules. Source/config retains its existing public API routing and must not be reinterpreted as automatic stock, checkout, payment or confirmed purchase.

## Three primary tailoring pages: initial SEO state

| Route | Initial title | H1 | Canonical | Source / sitemap | Google status |
| --- | --- | --- | --- | --- | --- |
| `/services/custom-tailoring/` | Custom Tailoring & Clothing in Kigali \| Mr Sewing Fashion | Tailoring & Clothing Services | `https://mrsewingfashion.com/services/custom-tailoring/` | `index, follow`; included | BLOCKED: no URL Inspection access |
| `/mensuits/` | Men's Suits in Kigali \| Mr Sewing Fashion | Men's Suits | `https://mrsewingfashion.com/mensuits/` | `index, follow`; included | BLOCKED: no URL Inspection access |
| `/womensuits/` | Women's Suits in Kigali \| Mr Sewing Fashion | Women's Suits | `https://mrsewingfashion.com/womensuits/` | `index, follow`; included | BLOCKED: no URL Inspection access |

Keyword hypotheses are not measured search-demand claims. Existing `_data/seo-search-intent.json` supplies the source-backed per-page map. Broad local tailor searches belong to Home; custom tailoring, men's suits, women's suits, tuxedos, fabrics, alterations, cleaning, mobile assistance and VIP each keep their actual page intent. Individual garment and fabric detail routes require useful distinct content; this assignment must not blanket-index or blanket-noindex them. Aliases and transactional steps are evaluated separately from sitemap-listed marketing pages.

Initial social metadata, schema types, alt findings and complete internal link sets are recorded per route in the JSON. Final metadata changes must agree with the visible garment/service names and preserve established canonical URLs. No ranking, Google Images inclusion or indexing result is promised.

## Commercial conflicts and safe boundaries

1. **Independent consultation:** the 13 November R49 explicit owner decision and current policy facts set Independent Consultation & Fitting to **35,000 RWF**, superseding the older 25,000 reference. The 26 November task quotes 25,000 as a reference and explicitly requires reconciliation; do not restore it silently. The separate eligible order-related visit remains 10,000 and independent assistance 50,000 under their existing scopes.
2. **Public starting prices:** the current approved R51/R67 presentation source has public service tariff schedules disabled, with internal prices, Shop prices, accepted quotations, payment obligations and approved surcharge disclosures retained. The new task provides V8 starting-price references but also requires newer approvals to prevail. Record the actual reconciled decision; never blindly replace all instances of a number or publish a historical tariff merely because it is supplied as a reference.
3. **Flexible Advance Payment:** the latest message explicitly marks the expanded proposal pending, including one-week cancellation review, extensions, initial-payment treatment and restart conditions. Do not activate or advertise that proposal. The previously approved 25 November Standard-only individually agreed lower-advance exception is a separate established rule; do not silently erase or expand it. Preserve Express exclusion, full outstanding balance within three calendar days, payment verification and suspension/reassessment as approved, with no automatic forfeiture or cancellation fee.
4. **Fabric imagery:** the 25 November baseline deliberately removed fabric photos/simulations. The new task requests representative images but prohibits portraying them as verified stock. Any chosen image needs accurate provenance and unambiguous illustrative labeling. If no suitable eligible image is established, keep the safe text-first implementation and report the unmet visual request rather than invent inventory.
5. **Leadership:** owner identity in references is not approval of a CEO/Founder title, biography, portrait, qualifications or achievements. Prepare a gated component and keep incomplete content unpublished.
6. **PDF:** latest uploaded bytes identify Version 1.2, six pages/20 sections, not the unavailable claimed six-page/14-section Version 1.1. Staging review/current effective contractual consent remain separate; this new assignment does not authorize production activation or a fabricated effective date.

## Analytics and integrations

| Integration | Source status | Verification / observed scope | External verification |
| --- | --- | --- | --- |
| Meta Pixel | Installed; owner-enabled production flag; optional consent required | `_data/meta-pixel.json`, `assets/meta-pixel.js`, shared loader. Config authorizes only PageView, not Lead/Purchase/WhatsApp conversion events. Staging/demo prevents sends; production is exact-host gated. | Installed but account receipt/diagnostics NOT VERIFIED |
| Meta Conversions API | Not installed in inspected application sources | No server CAPI endpoint/token/event pipeline found | Not applicable unless separately introduced/approved |
| GA4 | Not installed in inspected application sources | No GA measurement initialization found | Not applicable |
| Google Tag Manager | Not installed in inspected application sources | No GTM container found | Not applicable |
| Google Ads conversion tags | Not installed in inspected application sources | No Ads conversion tag found | Not applicable |
| Search Console | No verification tag/file located in inspected application | DNS/account verification cannot be inferred from absent HTML tags | BLOCKED: account/DNS access unavailable |
| WhatsApp | Existing official destination/shared direct/manual handoff | Service-specific messages and selection references must be tested with intercepted navigation; customer manually sends | Actual message delivery NOT TESTED and not claimed |
| Web3Forms / validated public request APIs | Installed existing provider pipeline | Existing server allowlists, original-photo validation, consent, payload limits and positive-provider acknowledgement must remain | Mock only; inbox delivery not claimed |
| Private D1/R2/staff intake | Implemented behind disabled prerequisites | No authorization to enable private recording/uploads | Not activated |

`node tests/analytics_privacy.cjs` **PASS** against the inspected implementation using synthetic DOM/network-free execution: no events/third-party load on staging, preview, unrelated hosts or localhost; no production events before consent; query and supported sensitive-request routes excluded; one production PageView after opt-in; no fabricated Lead/Purchase events. This confirms tested client guards, not Meta receipt. The initial inspection found that the direct Special Order form was not named in the sensitive-route regex; corrected the sensitive-route and actual-form guard; the expanded synthetic tests passed. No new event destinations or conversions were enabled.

No analytics destination, campaign, paid tool or conversion event was activated. A WhatsApp click remains a click, a provider-positive enquiry remains an enquiry, and neither is a verified sale. The existing production-only public API backend origin must not be changed while modifying staging UI.

## Security and privacy findings

- Preserve server-side allowlists, photo reconstruction, quantity/context validation, origin/host checks, payload limits, consent/honeypot checks, duplicate prevention and provider failure handling. UI-only validation is insufficient.
- Keep audits, draft policies and internal rules outside deployed customer assets. Existing source-boundary middleware needs actual deployed verification; local source/hosting tests do not establish remote enforcement.
- Preserve the separate 120-second browsing lifetime and 24-hour non-sensitive Express recovery; do not persist unnecessary contact details in broad cross-session storage or put private information in share URLs.
- Existing PageView consent uses local storage and a memory fallback. Query strings and sensitive enquiry pages must not be passed to advertising tracking. New dialog steps must not emit fictitious conversions.
- No production secrets, external account settings or customer records were modified by this audit. Static pattern checks cannot certify that no secret exists anywhere in historical sources; any actual exposure must be reported by path/type without reproducing values, and production rotation requires authorization.
- The website has no application package manifest/dependency lock in its existing architecture; browser/build tooling is separate from a customer runtime. Do not invent an `npm audit` result or introduce a framework solely for dependency reporting.

## Before browser, accessibility and performance evidence

An immutable Git archive of the starting revision was served locally on `127.0.0.1:3077`. Actual system Chromium visited 17 representative routes at 390 and 1440px (**34 visits**). All returned local HTTP200 with no horizontal overflow, JavaScript page errors or missing-response statuses. Screenshot filenames and exact observations are in `before/browser/results.json`; this is not actual Cloudflare or production testing.

Conditions: headless system Chromium; 900px viewport height; reduced motion; local unthrottled HTTP; unthrottled CPU; external network blocked; one visit per route/width; browser context/cache reused within a width. These observations are useful for comparable local before/after checks, not field Core Web Vitals, real-network mobile speed, ranking evidence or Lighthouse scores. On mobile, initial observed load-event times ranged roughly 171–406ms; Shop transferred about 2.08MB of measured local resources, more than the other sampled routes. Measurements are machine/cache-sensitive and must not be presented as guaranteed customer performance.

Representative screenshots include Home, main hub, men, women, Showroom, MS-142 detail, Our Work, Selected Designs, Fabric Preference, Fabric Guide, About, Alterations, Care, Mobile, VIP, Shop and Request. Empty selected-design/fabric snapshots are supplemented by seeded state screenshots from functional tests after implementation.

Automated axe and keyboard/dialog tests require the final application and are **NOT TESTED in this initial report**. The earlier recovery's passes are historical evidence, not a substitute for rerunning the new journey. Known uninterrupted OFFER motion accessibility limitation remains documented; no complete WCAG conformance claim is made. Physical devices, Firefox/WebKit, actual mobile keyboard behavior and external account receipt are not established by Chromium/source tests.

## Required finalization

The new acceptance checklist records each owner requirement explicitly with PASS, FAIL, BLOCKED or NOT TESTED and evidence. Populate final results after build, all relevant regressions, seeded dialog journeys, responsive/axe checks, source/output synchronization, safe provider mocks and exact staging deployment observation. Preserve Main and production throughout.

Actual permanent staging HTTP/rendering/account settings were blocked in the previous task by the managed network policy and missing account connection. Recheck access rather than assuming the blocker cleared. A successful GitHub push or Cloudflare preview status is not proof of what the permanent hostname serves. The final report must state the actual branch/start/end hashes, clean/dirty state, provider deployment ID, preview URL, and whether permanent origin rendering was independently verified.
