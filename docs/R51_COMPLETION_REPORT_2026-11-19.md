# R51 — Staging restructuring and universal Showroom

Owner instruction18November2026; implementation19November2026. Branch:`phase1/customer-journey-repairs`. Production baseline:`b2b8946882929da4ce7e0e01de4ba1511eed818a`. This task is staging only; no main merge/push or production settings change is authorized or performed.

## Audit, source organization and ownership

The original architecture is documented in [R51_ARCHITECTURE_AUDIT.md](R51_ARCHITECTURE_AUDIT.md): JSON business/content records, Python builders, reusable HTML/CSS/JS templates and committed generated pages/assets. The prior14-step build had overlapping policy/page generation, independent shared-rule copies and older header/footer sources alongside the modern components. No framework, database or CMS migration was needed.

The current [WEBSITE_SOURCE_MAP.md](WEBSITE_SOURCE_MAP.md) identifies actual paths and owner procedures. `_data/content-ownership.json` maps fact ownership and service scope. `scripts/business_settings.py` projects identity/contacts, location/social, hours, legal operator and navigation from their named sources; `_data/site-navigation.json` owns navigation ordering. Header/footer markup remains in the existing homepage templates and is now shared by the homepage and other modern builders. The About service picker uses the same five-service disclosure. Older unused files remain recoverable and are identified as legacy rather than competing active sources.

The ordinary build now also synchronizes business hours/schema, derives backend operational inputs, validates/builds document assets and builds the Showroom. The inactive legacy policy-rendering pass is no longer computed and discarded before the real renderer. Generated outputs remain rebuildable; no bulk file renaming or destructive migration occurred.

## Universal and service-specific rules

| Information | Authority and scope |
| --- | --- |
| Identity/primary contact | `_data/business.json`; shared brand/contact projection |
| Location/social | `_data/contact-v2.json`; workshop and appointment-only MIC location |
| Hours | `_data/business-hours.json`; shared schedule and Umuganda distinctions |
| Service rules/payment/fees/timing | `_data/customer-policy-facts.json`; explicit service scopes and exceptions |
| Ordinary tiers/benefits | `_data/suit-package-prices.json`; ordinary suits only |
| Tuxedos | `_data/tuxedo-package-prices.json`; separate package scope |
| Public visibility | `_data/public-content-policy.json`; presentation only, no price change |
| Shared explanatory projection | `scripts/public_content.py`, `scripts/customer_policies.py`, `scripts/customer_information.py` |
| FAQ organization | `_data/customer-faqs.json`; stable questions/anchors with shared placeholders |
| Shop | `_data/shop-products.json` and existing approval gate; product price/stock is independent |
| Official document/version | `_data/policy-documents.json`; actual approved PDF required |

Full universal payment, visit, transport and complaint explanations belong in the relevant FAQ/Terms information, with contextual service-page links. Timing and assessment stay service-specific. A tailoring deposit/visit fee is not automatically applied to Alterations or Garment Care. Generated `functions/_lib/operational-facts.js` feeds the existing backend from approved fee data, replacing independently maintained numeric constants.

## Terms document viewer and replacement

The stable `/terms-and-conditions/` page has a dedicated document-viewer implementation with version/effective metadata, native PDF embedding, scrolling and browser zoom where available, separate open/download actions and accessible fallback. Existing section anchors remain usable without invented PDF page numbers. Keyboard focus for an initial legacy fragment was corrected and tested.

**No approved Terms PDF was supplied.** Current registry `currentVersion` remains null; the page honestly says the PDF edition is not available and retains the readable existing online Terms. It has no fake download link. On activation of an approved PDF, the full transitional HTML rendering is replaced by the viewer. FAQ search now links concise document/section references instead of publishing a second full contractual text.

`scripts/publish_policy_document.py` provides a repository-based prepare/review/dry-run/publish workflow. Approval metadata, immutable version paths, checksums and manual reconciliation against nine current operational sources are required. Those sources include ordinary-suit benefits, tuxedo conditions and public visibility, so their changes cannot silently leave an activated PDF out of sync. Unregistered PDFs must remain outside the deployed tree; paths, symlinks, stray files, tamper, stale fingerprints and failed publication rollback are validated. Previous approved versions/history remain recoverable. No browser upload service or CMS is claimed. See [POLICY_DOCUMENT_WORKFLOW.md](POLICY_DOCUMENT_WORKFLOW.md).

An actual document's legal sufficiency, searchable/tagged text and assistive-technology readability still require review of the supplied file; the technical integrity validator cannot certify them.

## Media library and recovery

`scripts/media_library.py` derives eligible media through the existing effective collection/project publication gates. It never treats raw legacy `published:true` as permission. Generated `_data/media-library-index.json` is a projection, not a second editable rights catalogue. Curated homepage IDs are in `_data/media-library-settings.json`. New video rights/classification, when genuinely approved, belong in `_data/media-video-records.json`.

At completion there are **28 eligible photographs:21 Reference Design and7 Our Work**, associated with five approved genuine projects. Eight historically approved men's Kaunda photographs remain included with their original identities. Creator information remains unknown where unverified; reference imagery is not claimed as Mr Sewing work or ready stock.

Recovery reports [MEDIA_RECOVERY_INVENTORY.md](MEDIA_RECOVERY_INVENTORY.md) and `media-recovery-inventory.json` retain **402 images and7 video files**, original filenames/paths, hashes, publication/supporting/held status and three identical-file groups. No original asset was deleted, changed or physically duplicated. NUL-delimited Git baseline capture also protects Unicode filenames, covering all409original media files.

Seven MP4s lack separate publication/classification approval and remain unpublished in the new features. Video capability includes muted native controls, approved posters, no autoplay, conservative preload and separate-open fallback; no actual approved video playback is claimed. Manual tagging/review is documented; no paid AI categorization or per-request classifier was introduced.

## Showroom and category behavior

`/showroom/` is the primary universal browse destination, with audience, garment, style and source-classification filters, original-filename search, clear-filter/history behavior and no empty published categories. Current content activates suits/tuxedos and applicable styles; unsupported dresses/shirts do not become empty public categories. Stable path-based media IDs handle duplicate basenames. Cards show approved photographs, existing friendly names, original filenames and Reference Design/Our Work classification.

Design cards open the existing detail pages carrying both design identity and the exact photograph URL. They reuse the existing Select This Design, multi-selection, quantity, sharing, fabric/colour and quotation systems. Add/Change and Browse More links return to the Showroom. No duplicate cart, form or enquiry provider was built. Existing120-second browsing expiry and24-hour Express recovery remain intact, including Showroom browsing.

Published Shop-only clothing can also enter the media projection through the full `shop_catalog.load()` gate, with exact product links and Shop Product classification. No fictitious suit design ID, duplicated price/stock record or new sale entitlement is created. Unknown clothing categories require reviewed metadata; non-clothing hangers/covers/footwear and enquiry-only drafts are excluded. Current real Shop data has zero sale-published products, so this future capability is verified with temporary fixtures only. Existing design photos may link to matching already approved enquiry listings without widening photo permissions.

Old men's/women's/category/detail URLs remain compatible, with unchanged canonicals and metadata and access to the universal Showroom. Primary homepage, service, edit and consultation-inspiration actions now use Showroom filters. No destructive URL deletion or new redirect was performed. See [MEDIA_LIBRARY_WORKFLOW.md](MEDIA_LIBRARY_WORKFLOW.md).

## Homepage and Custom Tailoring

The homepage now begins with two curated men's/women's fashion media cards and one larger genuine-work feature beneath the existing header. These initial features use approved photographs. The existing hero, services, customer guidance, process, programmes, support and customer journeys remain beneath them. Media choices are owner-editable by central ID, not a second hardcoded photograph list.

Custom Tailoring keeps its hero, brand, supported men's/women's garments, tuxedo/Special alternative, customer fabric, measurement/fitting, standard/Express assessment, package benefits, payment and enquiry information. Quality/benefit comparisons replace public price columns; shared rule explanations link to FAQ/policy rather than copying full universal sections. Top/bottom actions lead to gender-filtered Showroom views and the existing Special Tailoring form.

## Public pricing and Shop exception

Public base service prices, fixed service fees, price examples and cost-surcharge percentages are removed from service content, FAQs/search/schema and dynamic quotation presentation. The optional surcharge-visibility question was unanswered; this is the recorded quotation-first staging interpretation, not a change to internal rates. Payment obligations/deposit percentages and approved benefit eligibility/discounts remain. The distinct6,000RWF referral commission remains a benefit, not a service tariff.

Approved internal suit/tuxedo/policy fact files are byte-preserved. Men's Tier3 remains300,000/400,000RWF, owner decision12November2026; no price was inferred or silently changed. Actual individual-quotation backend calculations and agreed quotation disclosures remain separate from public service presentation. No historic quotation/financial record was rewritten. Public Git/static source paths are not confidential storage; no costs, margins, salaries or private customer data were added.

Shop product prices/stock/publication and existing checkout/enquiry restrictions remain authoritative and unchanged. Current26Shop enquiry displays have no invented stock or prices; zero products were activated for sale. Temporary approved-stock fixtures verify visible product prices, canonical subtotal calculation, stock validation and rejection of injected prices. No payment integration was changed.

## Test results

PASS:

- `python scripts/build_site.py` and `python scripts/build_site.py --check`: all generated outputs synchronize, including repeated finalization. A final duplicate-versioned-consent-script issue was fixed; cleanup now removes/reinserts one controller consistently.
- `python tests/r51_restructure.py`: protected facts/settings, all409original media, existing metadata/routes/forms/providers, internal prices, no public fixed service prices, Shop fixtures, FAQ display/search/schema, source map and finalizer/controller uniqueness.
- `python tests/quotation_first_publication.py`: public service tariff/rate hiding, unchanged internal approvals, payment/benefit/Shop exceptions, scoped shared explanations and future-source fixtures.
- `python tests/media_showroom.py`:28eligible media, rights-held records, filenames/IDs/hash recovery, nonempty facets, curated features, future approved video and Shop-only clothing fixtures, no second inventory or original changes.
- `python tests/policy_documents.py`: absent-document fallback, approval-only publication, immutable replacement/history, fingerprints/conflicts, anchors/embed/open/download, path/checksum/stray-PDF/rollback cases using valid temporary one-page PDFs outside Git.
- `python tests/seo_preservation.py`, `python tests/sitemap_discovery.py`, `python tests/business_schema.py`:65canonical routes; all64previous sitemap routes plus Showroom, unique titles/canonicals, metadata/alt/schema syntax/link targets and staging noindex. Sitemap count64→65 and no-public-priceRange assertions were narrowly updated for R51. Approved social schema now follows the existing contact source.
- `node tests/quotation-completion-validation.mjs`, `node tests/shared-fabric-validation.mjs`, `node tests/selected-photo-validation.mjs`, `node tests/multi-design-validation.mjs`, `node tests/main-api-cors.mjs`: complete canonical selections/photographs/quantities, legacy compatibility, source-derived fee reconstruction, typed forms, consent, origin/CORS, body/field limits and failure paths with mocks.
- `node tests/r51_shop_prices.mjs`: canonical Shop unit prices/subtotals/stock and positive mock-provider response; no actual order/payment/publication.
- `node tests/r51-restructure.spec.cjs`: full local browser suite at320/360/375/390/430/768/1024/1440px, six axe checks, two mocked provider calls, zero JavaScript errors or missing resources. Includes filters/filename/history, home features, pending Terms and approved-PDF fixture/focus at four widths, ten mixed designs/twelve garments, fabric advice, full payload, failure preservation, consent, sharing/manual handoff,24-hour recovery and120-second departure expiry, FAQ search and Shop gates.
- Final targeted390/1440px checks: same-origin Showroom consultation links preserve form entries; all28Showroom and73homepage images load; no overflow/errors/failed requests/POST. Additional header geometry checks at1100/1120/1180/1200/1440 found no horizontal overflow or header/Shop overlap. Custom Tailoring checks at320/390/1440 confirm two benefit comparisons, no service prices, oneH1 and working top/bottom Showroom/Special actions. Final consent checks confirm one controller and exactly one manual handoff, with no actual message.
- Python/JavaScript syntax and `git diff --check`.

All browser/provider/WhatsApp/call interactions used safe synthetic data and mocks. No real enquiry, message, call, order or payment was sent. Existing historical tests whose assertions require public service tariffs are superseded by the scoped R51 internal-preservation/public-absence checks; no pricing approval was weakened.

Evidence is in `/workspace/review/r51-restructure-2026-11-19/`, with screenshots in `/workspace/artifacts/r51-restructure/`. Exact changed files are listed in `R51_CHANGED_FILES.txt`.

## Pending owner review and unavailable checks

- Supply the actual approved Terms PDF, approval/version/effective date and human rule reconciliation before activating PDF authority. No official PDF was invented or published.
- Approve any recovered video or held third-party media/classification before publication. Initial features use approved photographs only.
- Review the quotation-first presentation, including hidden public surcharge rates and retained payment/benefit obligations. Applicable Rwanda-specific mandatory disclosures were not independently verified from legal originals; no compliance claim is made. Preserve individual quotation and Shop disclosures before any later production decision.
- No new ready-stock, price, checkout or fulfilment evidence was supplied for Shop sale products; existing gates remain.
- Destructive old-URL removal/redirects remain a separate decision. Current compatibility routes are preserved.
- Original named operating handbooks and exact fabric/colour-stock specifications remain unavailable as previously recorded.
- Actual staging HTTP/browser verification remains subject to the execution proxy. Source/local checks and Cloudflare deployment status must be distinguished from independent rendering. No production change or Google indexing result is claimed.

Final commit/provider deployment evidence is supplied separately after staging publication. Owner review of the staging preview is required before any future production authorization.
