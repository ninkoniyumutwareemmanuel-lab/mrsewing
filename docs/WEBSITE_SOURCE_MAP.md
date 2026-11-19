# Mr Sewing Fashion — developer and owner source map

R51 reference: owner task 18 November 2026; implementation resumed 19 November 2026. Work on `phase1/customer-journey-repairs`. **This task is staging-only. Do not publish these changes to main or production without a separate owner instruction.**

The site uses JSON records, Python builders, HTML/CSS/JavaScript templates and Cloudflare Pages Functions. It does not require a new framework, database or CMS. Generated HTML and browser assets are committed because the existing hosting process serves those outputs.

## Start here

1. Read [AGENTS.md](../AGENTS.md), the [current customer reference](../.github/customer-content-reference/README.md), its source matrix/unresolved register/page map, and [SEO_PRESERVATION.md](../.github/customer-content-reference/SEO_PRESERVATION.md).
2. Read [R51_ARCHITECTURE_AUDIT.md](R51_ARCHITECTURE_AUDIT.md) before reorganizing files or routes.
3. Check the branch and working tree. Preserve unrelated changes. Edit authoritative source files, rebuild, test, and inspect staging.
4. Record new owner-approved business decisions with their effective date/source and a new dated customer-reference version. Do not treat an old page, proposal or filename as policy approval.

A public Git repository and static `_data` directory are **not confidential storage**. “Internal pricing” below means an approved calculation/source input rather than a displayed service tariff. Never add supplier costs, margins, salaries, private budgets, credentials or customer records here.

## Source files versus generated output

| Purpose | Edit these sources | Generated output / consumer |
| --- | --- | --- |
| Build orchestration | `scripts/build_site.py` and its focused builders | Committed HTML, CSS/JS bundles, sitemap/redirect/header files and approved document assets |
| Business identity and primary contact | `_data/business.json` | `scripts/business_settings.py`, shared components and qualified business schema |
| Verified locations and social links | `_data/contact-v2.json` | Contact page/shared business presentation; `shortAddress` is the approved compact header label |
| Operating hours | `_data/business-hours.json` | Shared header/booking helper and derived hours schema; see `scripts/sync_business_hours.py` |
| Legal operator | `_data/customer-information.json` → `company` | Shared footer/business presentation; currently NINKONIYUMUTWARE NEXUS LTD |
| Navigation ordering and labels | `_data/site-navigation.json` | `scripts/business_settings.py` → shared header/footer |
| Service destinations/titles | `_data/customer-release.json` → `services` | Shared Services disclosure and service renderers |
| Guide links | `_data/homepage-guides.json` | Shared navigation/footer guide lists |
| Header/footer structure | `_templates/homepage-header.html`, `_templates/homepage-footer.html` | `scripts/custom_tailoring.py:component()`, `scripts/shared_components.py`, homepage and page builders |
| Homepage | `_templates/homepage.html`, `_templates/homepage-sections.html`, existing homepage section templates | `scripts/build_homepage.py` → `index.html` and `assets/homepage.js` |
| Homepage fashion showcase | `_data/media-library-settings.json`; `scripts/showroom.py:homepage_showcase()` / `homepage_css()` | Two curated cards and one larger feature; existing homepage content stays beneath |
| Universal Showroom | `scripts/showroom.py`, `_templates/showroom.css`, `_templates/showroom.js` | `showroom/index.html`, `assets/showroom.css`, `assets/showroom.js` |
| Reusable media projection | `scripts/media_library.py` | `_data/media-library-index.json`: eligible public records only |
| Image publication rights and design identity | `_data/collection-designs.json`, `_data/collection-id-registry.json`, `_data/suit-reference-categories.json`, existing approval references | Effective gate `scripts/build_collections.py:load()`; details and quotation allowlists |
| Genuine completed work | `_data/customer-projects.json`, `scripts/project_catalog.py` | Our Work pages and correctly classified media |
| Video publication metadata | `_data/media-video-records.json` | Build-time reviewed video records; empty means no approved public video |
| Media recovery inventory | Existing originals plus `_data/collection-image-inventory.json`; `media_library.inventory()` | `docs/media-recovery-inventory.json`, `docs/MEDIA_RECOVERY_INVENTORY.md`; generated, do not edit |
| Shop product price/stock/availability | `_data/shop-products.json`; existing catalogue helpers | `scripts/build_commerce.py`, `scripts/shop_catalog.py`, runtime sale gates |
| Shop enquiry-only publication | `_data/shop-public-enquiries.json`, `scripts/public_enquiries.py` | Existing approved enquiry displays; not automatic sale/stock approval |
| Custom Tailoring | `_data/customer-release.json`, `scripts/customer_site.py`, `scripts/custom_tailoring_mobile.py` | Existing service page and shared selected-suit/Special journeys |
| Alterations, Garment Care and other services | `_data/customer-release.json`, `_data/journey-services.json`, `scripts/customer_site.py`, `scripts/build_journey.py`, `scripts/garment_care.py` | Service-specific pages; preserve their separate requirements |
| Shared operational facts | `_data/customer-policy-facts.json` | `scripts/customer_policies.py`, `scripts/customer_information.py` and scoped consumers |
| Public quotation-first presentation | `_data/public-content-policy.json`, `scripts/public_content.py` | Service pages, FAQ/search/schema and public guidance without public service tariffs |
| Fact ownership catalogue | `_data/content-ownership.json` | Human/developer ownership map, not another independently editable value source |
| Approved ordinary-suit schedule/benefits | `_data/suit-package-prices.json`, `scripts/suit_pricing.py` | Internal pricing/benefit inputs; R51 public visibility is controlled separately |
| Approved tuxedo schedule | `_data/tuxedo-package-prices.json` | Separate internal schedule and eligibility; do not substitute ordinary-suit prices |
| FAQ topics/questions/anchors | `_data/customer-faqs.json` | `scripts/faq_help.py` → FAQ pages, search JSON and FAQ structured data |
| Customer-information/policy composition | `_data/customer-release.json`, compatibility placeholders in `_data/customer-information.json` | `scripts/customer_site.py:information()` and policy helpers |
| Terms document registry | `_data/policy-documents.json` | `scripts/policy_documents.py` validates current/archived approved versions and rule reconciliation |
| Terms document viewer | `_templates/policy-document.html`, `_templates/policy-document.css`, `_templates/policy-document.js` | Stable `/terms-and-conditions/`; generated viewer assets in `assets/` |
| Approved PDF publication workflow | `scripts/publish_policy_document.py`, `scripts/build_policy_documents.py` | Immutable approved source/public PDF paths, registry update and asset build; no browser upload |
| Other policies | Existing `_data/customer-release.json`/`_data/customer-policy-facts.json` and policy renderers | Privacy/Refund and operational guidance; no invented legal terms |
| Form pages/review/submission composition | `scripts/customer_site.py`, `_templates/customer-site.js`, `_templates/quotation-arrangements.js` | Existing `/request/`, Special, service and review pages; existing provider retained |
| Selection, sharing and browser session state | `_templates/design-selections.js`, `_templates/selection-session.js`, `_templates/design-selection-sharing.js`, `_templates/selected-suit-quote.js`, `_templates/express-enquiry.js` | Generated design-selection bundles; preserve exact photos/IDs/quantities and session rules |
| Fabric/colour selection | `_data/fabric-reference-catalogue.json`, `_data/fabric-colours.json`, `_templates/shared-fabric.js`, `_templates/fabric-journey.js` | Existing Fabric Guide, shared preference and quotation payload |
| Request context/draft/consent | `_templates/request-context.js`, `_templates/request-draft.js`, `_templates/customer-interactions.js`, `_templates/whatsapp-consent.js`, `scripts/whatsapp_consent.py` | Existing safe handoffs/consent; no automatic customer messages |
| Generated backend fee inputs | `_data/customer-policy-facts.json` → `scripts/build_operational_facts.py` | `functions/_lib/operational-facts.js`; generated numeric inputs for individual enquiries, not a second editable tariff |
| Enquiry backend/security | `functions/api/selected-design-request.js`, `functions/_lib/selected-design-handler.js`, `functions/_lib/quotation-details.js`, `functions/_lib/public-api-cors.js` | Existing validated intake and provider acceptance contract |
| Provider routing | `_data/public-api.json`, `_templates/public-api.js` | Production static frontend uses the existing allowlisted main Cloudflare intake; do not route private APIs cross-origin |
| SEO and canonical intent | `_data/page-seo.json`, `_data/public-page-seo.json`, `_data/seo-search-intent.json`, `scripts/site_seo.py` | Unique page metadata/schema/canonicals and deliberate index/noindex decisions |
| Sitemap, exact aliases and staging headers | `scripts/build_public_routes.py`, `_data/route-aliases.json` | `sitemap.xml`, `_redirects`, `_headers`, `robots.txt` |
| Tests | `tests/` and task-specific review evidence | Source, backend and mocked browser checks; see commands below |

Older root `header.html`/`footer.html`, `_templates/shared/header.html`/`footer.html` and historical policy templates remain for compatibility/history. They are not the modern shared header/footer authority. Do not edit one old copy and assume all current pages will change. Likewise, edit templates/data rather than generated `assets/*.js` or HTML pages.

## Current authority boundaries

- `_data/customer-policy-facts.json` retains approved operational values and scope. Public wording is a projection; it must not silently change an internal percentage or fee.
- `_data/customer-faqs.json` owns questions, topic ownership and source links. Prefer approved placeholders for shared answers instead of copying payment/delivery rules into another page.
- `_data/public-content-policy.json` controls service-price presentation. It is separate from approval of the actual rate. R51 hides service base/fixed prices and public surcharge cost rates, while preserving payment obligations, benefit eligibility and Shop prices.
- `_data/suit-package-prices.json` remains authoritative for ordinary suits. The verified men's Tier 3 values are 300,000/400,000 RWF, approved 12 November. Do not change `publicationApproved` to hide a price: current consumers also use that flag to identify valid internal schedules.
- Service scope matters: the ordinary-suit advance schedule, eligible Kigali delivery, outside-Kigali tailoring delivery and separate Care/Alterations transport rules are not interchangeable.
- Shop currently has 26 enquiry-only displays and no sale-published products. Existing unknown price/stock fields remain unknown; do not fill them with guesses.
- The effective media gate publishes 28 photographs at the audit baseline. A raw `published:true` collection flag is insufficient. Genuine-work evidence and reference-image permission remain different sources.

## Replace the approved Terms PDF

No approved Terms PDF was supplied for R51. The viewer is prepared, while the current online Terms stay readable as an explicit transitional fallback. A real approved active PDF replaces the full HTML fallback; the site must not maintain a second independently editable full contractual document.

The available workflow is repository-based, not a browser upload portal. Detailed procedure: [POLICY_DOCUMENT_WORKFLOW.md](POLICY_DOCUMENT_WORKFLOW.md).

1. Prepare the document and obtain actual owner/legal approval. Keep pending PDFs and review records outside this public/deployed repository, for example in a local review folder.
2. On `phase1/customer-journey-repairs`, create a pending review template with the actual PDF, a new immutable version and its approved effective date:

   ```bash
   python scripts/publish_policy_document.py prepare --pdf /tmp/review/terms.pdf --version YOUR_NEW_VERSION --effective-date YYYY-MM-DD --review-out /tmp/review/terms-review.json
   ```

3. The responsible reviewer checks the actual PDF against approved operational sources. Record genuine approver/date/source and reconciliation evidence in the external review record. Do not set approval flags merely to pass validation.
4. Run a dry run; it must reject missing approval, changed PDF bytes, stale operational-source fingerprints or reused version identity:

   ```bash
   python scripts/publish_policy_document.py publish --pdf /tmp/review/terms.pdf --review /tmp/review/terms-review.json
   ```

5. After real approval, add `--write` to copy the immutable approved PDF and update the registry locally. This command does not commit, push or deploy. Approved source versions use `.github/policy-documents/terms-and-conditions/VERSION.pdf`; public versions use `/assets/policy-documents/terms-and-conditions/VERSION.pdf`.
6. Run `python scripts/publish_policy_document.py check`, rebuild, test the viewer/open/download/fallback and relevant FAQ/policy links, then deploy staging for review.
7. Keep previous version metadata, checksums and files/history. Never overwrite a historical PDF. A changed contractual rule requires explicit reconciliation of affected FAQ/operational facts; there is no automatic PDF-to-approved-policy conversion.

The stable customer URL remains `/terms-and-conditions/`. Old section anchors remain available, but do not invent PDF page numbers for them. Embedded PDF zoom depends on the browser; separate open/download links are always needed. PDF format/checksum validation is not a legal, malware or accessibility certification.

## Find and reuse an image by original filename

Use the generated recovery inventory or the eligible library. Example from the repository root:

```bash
rg -n 'm-kaundasuits3.jpeg' docs/media-recovery-inventory.json docs/MEDIA_RECOVERY_INVENTORY.md _data/media-library-index.json
```

The recovery reports include held assets; the public library includes eligible items only. A filename match is not permission to publish it. Read the record's source evidence and classification first.

Each canonical media ID is derived from its stored path. Duplicate basenames in different paths therefore remain distinct. Use the media ID plus path when giving another developer an instruction. Exact duplicate content is recorded by hash, but originals are not deleted or physically copied for the Showroom.

Example instruction: “Find the approved `m-kaundasuits3.jpeg` library record, keep its stored path and original filename, and reuse its media ID on the men's homepage card.” Do not rename the original to make the instruction easier.

## Add a Showroom item or activate a category

Detailed workflow: [MEDIA_LIBRARY_WORKFLOW.md](MEDIA_LIBRARY_WORKFLOW.md).

1. For a photograph, add or update the actual collection/project records and inventory according to their existing schema and approval evidence. Preserve stable design IDs and original filenames. Update the registry only with actual image permission, source/authenticity and owner-reviewed classification.
2. Validate through the effective `build_collections.load()` gate. Do not flip a raw published flag or add an item directly to generated `_data/media-library-index.json`.
3. For a new approved video, use `_data/media-video-records.json` with separate usage-rights and metadata approvals, a valid existing poster media ID, audience/garment/style, duration and the appropriate genuine-project or Shop association. Recovered MP4s are not automatically approved.
4. Rebuild. `/showroom/` derives filters from eligible records, so a garment category appears only when a published approved item actually belongs to it. Held/archived records must not activate categories.
5. Test original-filename search, keyboard filters, classification label, detail link and existing quotation handoff. Do not claim a reference garment is ready stock or genuine Mr Sewing work without evidence.

Existing men's/women's/category/detail routes remain compatible. Making a new filter the primary navigation does not authorize silently deleting or redirecting those URLs.

## Feature a photograph or video on the homepage

Edit `_data/media-library-settings.json`, which owns curation only. Its `homepage.cards` contains exactly two `{audience, mediaId}` entries, one for men and one for women; `homepage.featuredMediaId` selects the larger feature. Choose IDs from the eligible library and rebuild. A feature setting does not override rights gates.

No video is currently approved at the audit baseline. To feature one later, first complete its separate rights/classification/poster approval through `_data/media-video-records.json`, then select that eligible media ID in homepage settings. Do not point directly to an arbitrary MP4. Cards use muted playback controls, poster/fallback behavior and reduced-motion support as implemented; inspect on real mobile browsers before promising specific autoplay or embed behavior.

## Update a shared customer rule

1. Find the owner in `_data/content-ownership.json` and the latest dated customer reference.
2. Verify the actual new owner-approved decision, effective date, service scope and exceptions. Preserve the prior decision in a new dated reference version.
3. Change the authoritative record, generally `_data/customer-policy-facts.json`, rather than copying a number into a page or browser script. Change composition/FAQ questions only where necessary; shared explanations should reference approved tokens and direct FAQ anchors.
4. Rebuild all dependent pages, search data, schema and generated backend constants. `scripts/build_operational_facts.py` derives `functions/_lib/operational-facts.js` from the unchanged authoritative fee record; do not edit that generated module independently. If a PDF is active, its reviewed-source fingerprints will require a new human reconciliation when relevant source files change.
5. Test the affected services and their exceptions. A workplace visit description must not automatically transfer a suit fee or deposit rule to Garment Care or Alterations.

Contact, location and hours changes also need a source review and relevant schema checks. `scripts/build_site.py` now runs `scripts/sync_business_hours.py` and `scripts/sync_business_schema.py` before the page builders, maintaining the derived schema/helper outputs during the normal rebuild. Inspect their scope before changing a source. Do not edit generated opening-hours schema independently from `_data/business-hours.json`.

## Change an approved internal price without publishing it

Update the appropriate approved ordinary-suit/tuxedo or scoped policy record with actual new approval evidence. Preserve prior versions/decisions and any existing accepted customer quotation. Do not change historical transactions.

Keep `_data/public-content-policy.json` service-price visibility false for the R51 quotation-first presentation. Rebuild and run public-price absence plus internal-price preservation tests. Do not edit Shop product prices through a service-price file, change approval flags merely to hide amounts, or add private costs/margins to these public repository files.

## Build and test

Run from the repository root:

```bash
python scripts/build_site.py
python scripts/build_site.py --check
python tests/seo_preservation.py
python tests/sitemap_discovery.py
python tests/r51_restructure.py
node tests/r51_shop_prices.mjs
python tests/policy_documents.py
python tests/media_showroom.py
node tests/r51-restructure.spec.cjs
node tests/quotation-completion-validation.mjs
node tests/selected-photo-validation.mjs
node tests/multi-design-validation.mjs
node tests/main-api-cors.mjs
```

The browser suite defaults to a local server at `http://127.0.0.1:8020`; run a development server or set its `REVIEW_BASE_URL` to the intended test origin. It mocks provider responses and external handoffs. Never use real customer submissions to test it.

These are commands, not a claim that this documentation change ran or passed them. The final R51 report records the actual run results, browser suites, widths, screenshots and unavailable checks. New publication tests must use temporary fixtures, not overwrite approved business data or deploy sample PDFs/products. Existing tests tied to older public-price tables need explicit scoped updates for the latest owner rule; do not weaken security, rights or current pricing-preservation assertions to hide failures.

## Staging and production procedure

Staging base: `https://mrsewing-staging.pages.dev/`. Expected new route: `/showroom/`; the actual deployed route and commit must be confirmed after the build/provider deployment. A known URL or provider success does not prove browser access. The execution environment has previously blocked these origins through its proxy; report such a limitation accurately.

For this task, commit/push only to `phase1/customer-journey-repairs`. Confirm Cloudflare's check for the exact SHA and inspect the rendered staging website where access allows. Re-read remote main to demonstrate it was not changed.

The existing production process is a separate future owner-authorized release: reconcile the complete approved development history with current main without overwriting production-only work, honor branch protection, then verify both GitHub Pages static deployment and the Cloudflare `main` public-API deployment. The preferred live canonical domain is `https://mrsewingfashion.com/`; the existing public API runtime is `https://main.mrsewing-staging.pages.dev`. Do not confuse that API host with permission to publish a new staging task, and do not route private/staff APIs through it.

After any later authorized release, keep staging coordinated with the approved production baseline. Future unfinished staging work must not automatically reach main. Never claim Google indexing, message delivery, staff-inbox receipt, accepted production or payment from a successful build or provider acknowledgement.

## Compatibility and Shop-only media

Showroom is the primary discovery destination in shared navigation, homepage previews, Custom Tailoring actions, design-edit links and consultation inspiration. `/mensuits/`, `/womensuits/`, all nine existing category routes and existing design details remain compatible and retain canonical URLs/metadata; they also offer access to the universal Showroom. No destructive URL migration or new redirect was performed.

`scripts/media_library.py:shop_image_items()` adds only separately validated published clothing products from `shop_catalog.load()`. Shop-only photos link to the actual product page with Shop Product classification, not a fabricated suit design. Unknown clothing categories require reviewed product `showroom` metadata; non-clothing items and enquiry-only drafts are excluded. Existing design photos can retain a matching Shop association without duplicating the file or inventory. Shop remains the only owner of product prices/stock.

Local browser QA uses a localhost-only server, for example `python -m http.server 8020 --bind 127.0.0.1`. Do not expose the repository through a network-wide static server. Actual deployed staging verification remains distinct from these local checks.

The approved document must itself be readable and accessible; PDF header/checksum validation cannot certify legal sufficiency, tagged text or assistive-technology compatibility. No real approved PDF is supplied yet. The viewer offers separate open/download paths when a genuine version is activated, and the existing online Terms remain readable until then.
