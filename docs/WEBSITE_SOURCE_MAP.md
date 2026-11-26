# Website source map

Last reconciled: 25 November 2026. Start with [the dated master register](WEBSITE_RECONCILIATION_2026-11-25.md), `AGENTS.md` and `.github/customer-content-reference/README.md`. The authorized implementation branch is **phase1/customer-journey-repairs**. Main and the official website are read-only during this recovery.

## Sources and generated outputs

Edit the source named below, rebuild, inspect the diff and commit its generated output together. Direct edits to generated HTML/assets can disappear on the next build.

| Area | Authoritative source | Generated/customer destination |
|---|---|---|
| Build orchestration | `scripts/build_site.py` | Root HTML, clean route directories, browser assets, redirects, sitemap |
| Header, footer and navigation | `_templates/homepage-header.html`, `_templates/homepage-footer.html`, `scripts/custom_tailoring.py:component`, `scripts/shared_components.py`, `_data/homepage-guides.json` | Shared rendered navigation; retain responsive controllers and deliberate legacy wrappers |
| Homepage | `scripts/build_homepage.py`, `_templates/homepage-tailoring.html`, `_templates/homepage-tailoring.css`, homepage section templates | `/`, `assets/homepage.js` |
| Homepage photos, order, videos | `scripts/homepage_galleries.py`, `scripts/media_sorting.py`, `scripts/homepage_video_cards.py`, `_data/media-video-records.json`, `_data/collection-designs.json` | Two opposite-direction photo rows, silent video cards or approved fallbacks |
| About / Contact | `scripts/build_about.py`, `_templates/about.html`; `scripts/build_contact.py`, `_templates/contact.html`, `_data/contact-v2.json` | `/about/`, `/contact/` and legacy aliases |
| Services hub | `scripts/tailoring_services_hub.py`, `_templates/tailoring-services-hub.css`, `_data/customer-release.json`, `scripts/customer_site.py`, **generator `scripts/build_journey.py`** | `/services/custom-tailoring/` |
| Other service pages | `_data/customer-release.json`, `scripts/customer_site.py`, `scripts/build_journey.py`, `scripts/garment_care.py` | Alterations, care, mobile, VIP and service-specific detail pages |
| Central Showroom and categories | `scripts/build_collections.py`, `_templates/collections.html`, `_templates/collections.css`, `assets/collections-v3.js`, `_data/clothing-category-config.json`, `scripts/clothing_categories.py` | `/collections/`, `?gender=men` / `?gender=women`, existing men's/women's categories and design details |
| Design and media records | `_data/collection-designs.json`, `_data/collection-id-registry.json`, `_data/collection-image-inventory.json`, `_data/suit-reference-categories.json`, `_data/customer-projects.json` | Approved design/project photographs; originals retain filename/path and exact selection identity |
| Shop catalogue | `_data/shop-products.json`, `_data/shop-public-enquiries.json`, `scripts/shop_catalog.py`, `scripts/public_enquiries.py`, `scripts/build_commerce.py`, `_templates/commerce.*` | `/shop/` and product/category pages; API reconstructs trusted stock/price |
| Shop staging preview | `scripts/shop_preview.py`, `functions/shop/[[path]].js`, `functions/_lib/shop-preview-handler.js` | Host-gated enquiry display; no automatic stock or purchase approval |
| Fabric Guide | `scripts/customer_guides.py`, `scripts/fabric_collections.py`, `_data/fabric-collections.json`, `_templates/fabric-showroom-*.html`, `_templates/fabric-showroom.js`, `_templates/fabric-journey.*`, `_data/fabric-colours.json` | Text-first `/guides/fabrics/` and seven collection pages; see fabric recovery report for selection data contract |
| Measurements Guide | `scripts/customer_guides.py`, `_data/measurement-guide-images.json`, `_data/customer-guide-images.json` | `/measurements/`; approved measurement illustrations are distinct from rejected fabric imagery |
| Policy facts | `_data/customer-policy-facts.json`, `scripts/customer_policies.py` | Shared service-scoped operational wording/placeholders |
| Customer information / order process | `_data/customer-information.json`, `_data/customer-release.json`, `scripts/customer_information.py`, `scripts/customer_site.py` | `/customer-information/`, `/our-process/`, service guidance |
| FAQs / search / schema | `_data/customer-faqs.json`, `scripts/faq_help.py`, `scripts/customer_policies.py` | `/faq/`, topic pages and synchronized answers/search/FAQ JSON-LD |
| Refund / privacy | `scripts/refund_page.py`, `scripts/privacy_page.py`, shared approved facts and existing page data | `/refund-policy/`, `/privacy-policy/` |
| Terms registry and reader | `_data/policy-documents.json`, `scripts/terms_reader.py`, `scripts/render_terms_page_images.py`, `_templates/terms-reader.*` | `/terms-and-conditions/`, exact PDF download and genuine rendered pages; `/terms-and-conditions/current/` preserves effective consent |
| Internal approved prices | `_data/suit-package-prices.json`, `_data/tuxedo-package-prices.json`, `scripts/suit_pricing.py` | Internal quotation inputs; public presentation and Shop prices have separate approval scopes |
| Business settings | `_data/business.json`, `_data/contact-v2.json`, `_data/business-hours.json`, `scripts/sync_business_hours.py`, `scripts/sync_business_schema.py` | Verified identity/contacts/locations/hours; preserve Downtown appointment qualification |
| Selected designs and request context | `_templates/design-selections.js`, `_templates/design-selection-sharing.js`, `_templates/request-context.js`, `_templates/quotation-arrangements.js`, `scripts/selected_designs.py` | Selected Designs → shared fabric → quotation; exact photographs/quantities preserved |
| Quotation / booking / service forms | `scripts/customer_site.py`, `scripts/consultation_form.py`, `_templates/customer-site.js`, relevant request/quotation templates | Existing request/review/explicit-submit journeys and R65 modal wrappers |
| Source boundary / release preparation | `functions/_middleware.js`, `scripts/prepare_release_candidate.py` | Internal source/data 404 on every runtime host. Static hosts require the separate public-only artifact; private compiler inputs are never static assets. Public Git history is unaffected. |
| Receiving pipeline | `functions/api/`, `functions/_lib/selected-design-handler.js`, `functions/_lib/quotation-details.js`, `functions/_lib/fabric-preferences.js`, `scripts/edge/request-data.mjs` | Validated existing provider; mocked in tests; no automatic order/appointment confirmation |
| Consent / analytics | `scripts/whatsapp_consent.py`, `_templates/whatsapp-consent.js` where retained, `_data/meta-pixel.json` and shared interactions | Latest direct WhatsApp flow; forms retain consent; opt-in analytics scoped to approved hosts |
| SEO | `_data/page-seo.json`, `_data/seo-search-intent.json`, `_data/route-aliases.json`, `scripts/site_seo.py`, `scripts/build_public_routes.py` | Canonicals, clean URLs, exact redirects, sitemap, robots, host-scoped staging noindex |
| CI | `.github/workflows/r59-staging-build.yml`, `.github/workflows/terms-reader-qa.yml` | Exact-event, verification-only checks; no automatic generated commits |

The table describes actual responsibilities; it does not grant publication rights or imply every historic source is active. See the recovery reports for obsolete and pending records.

## Owner workflows

**Find a photograph:** search its original filename using `rg -n --fixed-strings 'filename.webp' _data docs`. Check the design ID, original path, view/family, approval/classification and image inventory. Reuse its existing asset rather than duplicating or renaming it. Do not infer ready stock or company authorship.

**Add a clothing category:** use `_data/clothing-category-config.json` plus genuinely eligible designs in the collection records and category assignments. Keep the current two initial categories. Empty/unpublished groups must not appear automatically. Future categories need reviewed garment-specific quotation support, not only a new visible card.

**Change featured homepage media:** use the existing approved homepage gallery/video source and exact publication metadata. Original MP4s are preserved; playback must use validated silent derivatives and matching approved posters. Use the preparation script and tests; never substitute an original with audio when a derivative is missing.

**Update a shared customer rule:** verify scope/date/approval, update the authoritative fact once, use existing placeholders in FAQs/service guidance, preserve service exceptions and prior approvals. Rebuild and test rendered text, search and schema together. New proposals remain pending.

**Update an internal price:** edit the approved internal price record with its source/effective scope; preserve historical quotations. Do not publish it merely by changing a JSON value. Shop products retain their own independently approved price/availability records.

**Replace Terms:** follow [policy document workflow](POLICY_DOCUMENT_WORKFLOW.md). Preserve original bytes and version archives; compare full text/sections, record actual version and approval, render genuine page images, update manifests/download/reader together and test identical bytes. Staging review is separate from contractual activation. A filename or six-page count alone is insufficient.

## Build, test and deployment

Run `python scripts/build_site.py`, then `python scripts/build_site.py --check`. Run the recovery test runner, source/SEO/sitemap checks, PDF/media checks and relevant browser mocks listed in the master register. Review the complete diff and commit both sources and generated outputs. CI uses the event commit and never pushes a generated commit over later work.

Push only `HEAD:phase1/customer-journey-repairs`. Verify its exact Cloudflare check and actual served content at **https://mrsewing-staging.pages.dev/**. Preview URLs are evidence for that deployment, not proof that the permanent address follows the same branch. See [staging deployment workflow](STAGING_DEVELOPMENT_WORKFLOW.md) for required settings/access and production-backend protection.

Main release is a separate owner-authorized process. Do not promote new staging policies or unfinished features automatically.

## Backups and cross-session handoff

The original dirty R54 workspace remains at `/workspace/mrsewing`. Its binary patch/archive and all-ref Git bundle are under `/workspace/recovery/2026-11-25/`; the active clean recovery implementation is `/workspace/mrsewing-recovery`. Keep these distinct. The local `recovery/staging-before-reconciliation-2026-11-25` reference preserves the initial remote staging tip. Do not reset or copy entire older trees over this baseline.

Every future task should record branch/HEAD, owner instruction, applicable source version, unfinished changes, tests, exact deployment evidence and unresolved decisions in the dated reconciliation register before handing off.

## 26 November pre-launch preparation

See [the pre-launch brief](PRELAUNCH_BRIEF_2026-11-26.md). This is release preparation only; no Main merge or production deployment is authorized. `scripts/audit_release_routes.py` and `tests/prelaunch_routes_browser.cjs` create complete local HTTP/rendered canonical evidence outside the checkout. They do not verify Google indexing or actual Cloudflare/production responses.

`python scripts/prepare_release_candidate.py --output /tmp/mrsewing-candidate-unique` prepares a public-only production projection and separately stored runtime compiler inputs, without deploying. `--check` verifies exact public and runtime bytes. Choose a fresh output path; existing candidates are preserved. Production Terms use the existing effective HTML body while staging retains the actual received PDF reader. No PDF activation or effective date is inferred. The final source must be committed and clean before freezing a candidate. Follow the separately authorized hosting/API verification and rollback procedure before any future Main release.

### Final targeted release preparation

Read [the final release brief](FINAL_RELEASE_PREPARATION_2026-11-26.md) and current source `versions/2026-11-26-02`. `_data/shop-release.json` and `scripts/shop_release_hold.py` control temporary Shop navigation/indexing and production-only holding views; the real staging catalogue/APIs/forms remain intact. Restore only after a reviewed decision and regression checks. `_data/advertising-measurement.json` records unavailable Google configuration; `_templates/enquiry-measurement.js` and existing request/WhatsApp hooks emit non-network, non-PII first-party signals only. Google/Meta conversion transport is not activated by adding a signal or changing a configuration label; genuine destination, consent/privacy and external receipt validation are required.

##26November customer experience additions

- Shared labels: `_data/customer-interface-labels.json`, `scripts/customer_interface.py`. Header Services/Guides and keyboard/mobile behavior: `_templates/shared/navigation.js` and `navigation.css`.
- Guided selected-suit dialog: `_templates/tailoring-request-dialog.js`/`.css`, included by `scripts/customer_site.py` in existing design-selection outputs. Same-origin existing routes and actual validators/provider are reused; no second form backend. Existing standalone bookmarks remain supported.
- Compact design/quantity review: `_templates/design-selections.js`/`.css`. Explicit Add/Change handoffs inherit only their own unexpired per-tab draft through `_templates/selection-session.js` and `_templates/request-draft.js`; deliberate independent selections do not inherit another enquiry.
- Service landing renderer: `scripts/service_landings.py`, `_templates/service-landings.css`, `_data/service-contact-actions.json`. WhatsApp number is read from approved business data; existing forms remain available. Legacy unfinished subscription entry routes fall back to VIP, with internal implementation preserved.
- About profile: `_data/about-leadership.json`, `_templates/about-leadership.html`, `scripts/build_about.py`. Missing/unapproved title/biography/portrait never render.
- Audit inventory/SEO comparison: `scripts/audit_customer_experience.py`; full internal review package and evidence are outside deployed app assets under `/workspace/review/2026-11-26/`.
- Regression commands: existing build/check, SEO/sitemap/recovery checks, six backend validation scripts, `tests/analytics_privacy.cjs`, `tests/tailoring_request_dialog.cjs`, `tests/customer_gallery_browser.cjs`, `tests/customer_navigation.spec.cjs`, `tests/home_about_customer_experience.cjs`, `tests/service_landings_browser.cjs`. See the current comprehensive review report for results and limitations.
