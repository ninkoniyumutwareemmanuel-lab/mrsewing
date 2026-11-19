# R52 — Tailoring-first positioning and WhatsApp journey

Owner follow-up19November2026. Branch `phase1/customer-journey-repairs`; prior reviewed staging commit `749b21d99f0dacf21d260b1adfc3ebca52a76447`. This is additive to R51, staging only. No main edit, reset, merge, push, production deployment or settings change is authorized or performed. Final SHA/provider result is supplied separately after staging publication.

## Fit, audit and preservation

Read the root instructions/current2026-11-19-02 reference, required brief, source matrix/unresolved register/page map, SEO preservation rules, prior R51 report/source map and actual source/build/consent/media/quotation implementations. [Audit](R52_TAILORING_FIRST_AUDIT.md) and the [required brief](../.github/customer-content-reference/R52_TAILORING_FIRST_BRIEF_2026-11-19.md) record the plan before implementation. Existing tracked work was clean; existing tooling/cache directories were preserved and excluded. Independent read-only review found no critical blocker.

The work reuses the central eligible media library, curated feature IDs, shared navigation/business settings, Terms-consent controller, complete selected-design sharing and quotation/provider pipeline. It creates no competing gallery, form, upload, catalogue, contact or consent system. Internal rates, policy facts, benefits, Shop stock/price/payment/publication gates and the pending PDF state remain unchanged. All409original images/videos plus the favicon are byte-preserved; no media was added, replaced, deleted or newly approved.

## Homepage

The first section below the existing header now has the sole H1 **Professional Tailor in Kigali, Rwanda**, the approved concise custom-suit/special-tailoring/alterations message and the prominent **Send Your Design on WhatsApp** action. Tailoring Services and Showroom are secondary choices. Two approved men's/women's tailoring cards and the larger approved genuine-work feature remain sourced from the central library. They do not represent reference designs as ready stock or Mr Sewing workmanship.

A **Have a Design in Mind?** card directly beneath explains design assessment, fabric guidance, manual photograph attachment and the existing website-enquiry alternative. Mobile buttons are large normal-flow controls, without a new floating overlay that could cover navigation, inputs or selections. The retained brand hero is a supporting H2; its photograph, service links, booking, process, galleries, programmes, support and Shop remain below. The existing lower design action uses the same central wording/flow.

No clothing video currently has publication permission. The requested video-first direction remains pending approved video records; approved photographs supply the current fallback. Existing video/poster/native-control/reduced-motion capability remains available without publishing the seven held MP4s. No claim is made that the preferred two videos are live.

## Tailoring Services and stable routes

The public service label is **Tailoring Services**, sourced once from `_data/customer-release.json`; its stable URL and internal request ID remain `/services/custom-tailoring/` and `custom-tailoring`. The shared header/footer and relevant breadcrumbs/form labels inherit the new name. No new public route, redirect, canonical migration or keyword landing page was necessary. Existing aliases, men's/women's categories, design details and sitemap remain.

Three prominent overview cards give access to:

1. **Suit Tailoring** — existing `/services/custom-tailoring/design-choice/` and `/standard-order/` entry, men's/women's Showroom filters and current design/fabric/quotation steps.
2. **Special Tailoring** — existing `/services/custom-tailoring/special-order/`, supported garments and separate tuxedo conditions.
3. **Alterations & Repairs** — existing `/services/alterations/` and its own assessment/form/policies.

The main hero gains the primary WhatsApp action; its existing exploration destinations remain. Fabric guidance explains choosing an available preference, requesting help or using customer-supplied fabric, with suitability/colours/availability confirmed. Existing ordinary-suit benefits, scoped payment, production, measurement/fitting, delivery and correction information remain. No service prices were restored and no suit policy was applied to Alterations or Special garments by analogy.

## WhatsApp placements and behavior

Shared actions are present in the initial homepage showcase, sharing card and retained lower design section; Tailoring Services hero; existing Suit Tailoring entry and men's/women's landings; Special Tailoring; Showroom introduction; and each of the28approved individual design details. The Selected Designs page keeps its direct complete-list WhatsApp action and secondary native/copy options. Website forms remain alternatives. Gallery photograph cards remain simple, with existing navigation.

The reusable helper is `scripts/tailoring_positioning.py`; approved wording/event description is `_data/tailoring-positioning.json`. Phone authority stays `_data/business.json` through `business_settings`, with no new hardcoded number. Generic prepared text is:

> Hello Mr Sewing Fashion, I have a clothing design I'd like you to make. I'd like to share a photo and request a quotation.

Design-detail messages include the actual friendly name, exact approved viewed photograph and existing detail URL. The browser validates against the page's approved design data and uses the current staging origin with an explicit preview notice. It updates after a photograph change; an unrelated/foreign photograph cannot become the shared reference. Prepared messages use friendly names without internal codes; existing detail headings and records are otherwise preserved. No private filesystem path, contact detail or other enquiry personal data is added to these links.

All new actions use the existing unchecked per-use Terms modal. Consent is required before the official WhatsApp handoff; the customer attaches their picture and presses Send inside WhatsApp. After the handoff attempt, a same-tab link to the existing standalone consent page preserves the prepared message as a popup fallback. No UI claims message delivery, staff receipt, accepted quotation or order. Large multi-selection sharing remains in its existing complete-entry splitting/copy fallback, not the short-message helper.

## SEO and discovery

Intentional metadata changes are scoped to the homepage, Tailoring Services and the existing noindex Special request:

| Route | Title | Description |
| --- | --- | --- |
| `/` | Professional Tailor in Kigali, Rwanda | Mr Sewing Fashion | Professional tailoring in Kigali, Rwanda: custom suits, special tailoring and alterations. Share your design with Mr Sewing Fashion for assessment and a quotation. |
| `/services/custom-tailoring/` | Tailoring Services in Kigali | Mr Sewing Fashion | Explore suit tailoring, special tailoring and alterations in Kigali. Discuss your design, fabric options and fittings with Mr Sewing Fashion for a quotation. |
| `/services/custom-tailoring/special-order/` | Special Tailoring Request in Kigali | Mr Sewing Fashion | Request custom shirts, trousers, dresses, jackets, coats or other approved garments. Share your idea for feasibility, fabric advice and a personal quotation. |

The service's existing aliases inherit the main service metadata; `/request/custom-tailoring/` inherits the new service label. The two existing noindex Suit entry pages now use H1 **Suit Tailoring**; their title/description/canonical/robots stay unchanged. All other captured metadata is preserved. The Fabric Guide's stale editorial primary-topic label mentioning starting prices was corrected to fabric/quality information; no unrelated page rewrite occurred.

Canonicals, all65sitemap routes, redirect targets, robots/header rules, image descriptions, approved business identity/contact/location and JSON-LD remain valid. No new review, award, stock, service area, historical statistic or keyword-volume claim was added. Candidate search phrases guide natural copy only; no meta-keywords, keyword stuffing or ranking promise. Staging protections remain; actual deployed headers must still be checked independently where access permits.

No analytics collector was verified. A local `mrsewing:enquiry-action` DOM event exposes only action/context/hasDesign; it creates no network telemetry, personal-data collection or persistence. No paid analytics or Google Business Profile edit occurred. The source map documents a future authorized consistency review against verified name/contact/location/hours; clicks are not confirmed enquiries or sales.

## Actual verification

PASS:

- `python scripts/build_site.py` and `python scripts/build_site.py --check`: reproducible generated sources/assets, all existing builders and65canonical routes.
- `python tests/r52_tailoring_first.py`: immutable Git749b21d baseline; media, internal prices, policy/Shop/API/deployment inputs,62existing forms/providers, stable URLs/canonicals/robots, precise approved metadata exceptions, central-label fixture and approved design/photo rejection.
- `python tests/quotation_first_publication.py`, `python tests/media_showroom.py`, `python tests/policy_documents.py`: public tariff suppression, approved media/Shop/video gates and document workflow remain correct with temporary fixtures.
- `python tests/seo_preservation.py`, `python tests/sitemap_discovery.py`, `python tests/business_schema.py`: unique metadata/headings/canonicals, alt/link/JSON-LD syntax,65canonical routes and staging protections.
- `node tests/quotation-completion-validation.mjs`, `node tests/shared-fabric-validation.mjs`, `node tests/selected-photo-validation.mjs`, `node tests/multi-design-validation.mjs`, `node tests/main-api-cors.mjs`, `node tests/r51_shop_prices.mjs`: complete validated enquiries, scoped server calculations, consent/security/failure/Shop fixtures.
- `node tests/r52-tailoring-first.spec.cjs`: local Chromium at320/360/375/390/430/768/1024/1440px; six scoped axe checks; no horizontal overflow, browser errors or missing resources; homepage/service structure, generic/exact-design consent/manual handoff, preview links, invalid-photo rejection, local event hook, mixed men's/women's sharing→fabric advice→quotation→review and a full actual-validator/mocked-provider payload.
- Temporary intercepted two-photo fixture verifies thumbnail2 updates WhatsApp to its exact alternate photo and excludes the first; the actual approved company allowlist currently has one photo per design, so no real multi-photo publication is claimed.
- Python/JS syntax, manifest hashes/history and `git diff --check`. Independent review also verified all28reference-to-photo/detail mappings.

No real WhatsApp message, call, customer enquiry, order or payment was sent. Provider acceptance is never described as inbox receipt. Screenshots and test evidence are in `/workspace/artifacts/r52-tailoring-first/` and `/workspace/review/r52-tailoring-first-2026-11-19/`. Exact changed files are in `R52_CHANGED_FILES.txt`; generated HTML changes reflect the shared label/controller and do not mean unrelated page redesigns.

## Remaining decisions and limits

- Actual approved video files/rights/classification are needed for the preferred two-video showcase. Current approved photographs remain.
- The official Terms PDF/version/effective date and manual operational reconciliation remain pending from R51; no draft was invented or published. Original operating handbooks/exact fabric specifications/stock limitations remain recorded.
- Shop sale approvals, destructive legacy-URL migration, new analytics integration and any production release require their own authorization/evidence. Existing Shop functions remain.
- SEO/GBP account performance, Google indexing/ranking/conversion changes and WhatsApp device/inbox delivery are not established by these tests.
- Actual Pages-domain HTTP/browser access has previously been blocked at the execution proxy. Record the fresh staging provider result separately from independent deployed rendering; do not infer an origin error from CONNECT403.

No conflict required undoing R51. The only presentation supersessions are the owner-approved tailoring-first homepage, main service naming/grouping and WhatsApp priority. All previously approved policies and protected systems remain. Stop after staging review; no production action.
