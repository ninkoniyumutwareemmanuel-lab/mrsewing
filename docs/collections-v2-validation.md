# Collections V2 — staging validation report

Baseline: `4a8b61d9ec16d6d191b0d39af77234d0dd341454`.
Authorized branch: `phase1/customer-journey-repairs`.

## Implementation and image migration

Three connected existing collection routes now share one dataset, build,
search/filter controller, persistent favourites, bounded shortlist sharing and
accessible fullscreen design viewer. All are custom-tailoring inspiration and
quotation experiences, not an inventory/checkout store. Native sharing falls
back to clipboard or selectable text; no unnecessary services or dependencies.

[Architecture, schema, maintenance and full legacy route table](collections-v2.md)
[Image migration CSV](collection-image-migration.csv)
[All candidate rights/provenance reviews](collection-rights-review.md)

Inventory: 295 image assets, 155 root originals, 138 garment/editorial candidate
records, 265 asset-to-record mappings, 111 existing-public designs carried forward,
27 excluded candidates, 0 different-photo groupings, 0 missing inventoried assets
or broken literal legacy image references. All originals/derivatives remain
byte-for-byte unchanged. The one service editorial candidate was explicitly
inventoried and excluded from the showroom. No new product photographs generated.

All 138 candidate records require owner rights review; no licence/authorship was
assumed from prior publication. No unverified ownership badges are displayed.
Fifty-seven published designs remain gender-unclassified; colours/descriptions
were not guessed. Graduation is the only active verified occasion category.
Other occasion groups need owner-provided assignments before they are populated.

## Build and automated verification

- `python3 scripts/build_site.py`: succeeds; outputs generated from maintained
  sources. `--check` succeeds and does not mutate files.
- Registry/inventory/schema guards pass, including negative tests for duplicate
  IDs, invalid IDs, missing images, unsupported provenance/publication and retired
  ID conflicts. Shared-component propagation checks pass for all V2 consumers.
- All nine existing browser suites pass: homepage-journey, homepage, header,
  page-seo, homepage-optimization, phase1, phase2, image-delivery, agentic-discovery.
- Existing Contact and About browser suites pass unchanged in functionality.
- New Collections suite passes 3 galleries × 7 widths: 320, 360, 390, 430, 768,
  1024 and 1440px. It checks search normalization/precision, combined filters,
  clear/empty states, pagination, image decoding and responsive overflow.
- Viewer tests pass: open/close, Escape, trapped/restored focus, arrow keys,
  previous/next designs, mobile swipe events, multi-photo ordering fixture,
  background scroll lock and available verified metadata.
- Deep links pass direct loading, refresh, browser back/forward, invalid IDs,
  percent-encoded references and the original leading-space r24 filename.
- Sharing tests mock native and clipboard APIs: copy/failure fallback, duplicate
  protection, and dynamic current-origin links/WhatsApp reference messages.
- Favourites pass save/remove, cross-gallery persistence, shortlist empty states,
  corrupt/blocked storage, unavailable saved IDs and bounded groups of eight.
- Pagination boundary check loads all 111 unique designs, hides Load More after
  the final partial batch, and introduces no duplicate cards.
- No-JavaScript content: initial cards, all 111 named photo-reference links,
  booking/contact actions and usable shared navigation remain present.
- All eight requested legacy category/suit paths return locally and retain their
  useful original content; no generic redirects, loops or unsupported 301 claims.
- Metadata synchronization, canonical/OG URLs, clean URL/sitemap checks, all 25
  JSON-LD blocks and 387 typed Schema.org nodes pass validation. New schema uses
  CollectionPage/ItemList with no fabricated Product prices, offers or ratings.
- Existing image/media checks, all 138 candidate source-image decodes and calendar/
  booking regressions pass. Actual booking requests are intercepted/mock-only.
- JavaScript syntax and git whitespace checks pass.

## Approved-page regression protection

Homepage, Contact and About source/generated HTML, their JS and all approved
shared component files remain byte-for-byte unchanged. Their full-page captures
at 390px and 1440px are pixel-identical before/after. All 295 pre-existing image
assets, sitemap, robots, business data and CNAME/domain file are unchanged.
No unrelated page, policy, price, service promise, loyalty offer or referral offer
was redesigned or changed. Existing browser assertions were updated only for
the intentionally migrated collection header, viewer details and reference IDs.

## Local synthetic performance

| Profile | Performance | Accessibility | Best practices | SEO | LCP | CLS | TBT |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Mobile | 98 | 100 | 100 | 100 | 2.5 s | 0 | 0 ms |
| Desktop | 99 | 100 | 100 | 100 | 0.3 s | 0.081 | 0 ms |

These are local Lighthouse results, not production Core Web Vitals or field INP.
The local audit server models gzip and a 600-second cache lifetime; actual
Cloudflare/GitHub Pages cache behavior and real-user responsiveness are not
established. Some original JPEG fallbacks and host cache lifetimes remain
optimization opportunities. No production cache settings were changed.

Raw reports, logs, responsive gallery screenshots, viewer screenshots and
approved-page comparisons are in `/workspace/phase1-review/collections-v2/`.
The review screenshots are `collections-390.png`, `collections-1440.png` and
`collections-viewer-390.png`; matching men's/women's and desktop viewer captures
are also included. Automated results do not constitute owner visual approval.

## Deployment and limits

Only the existing staging branch is to be pushed. Cloudflare/production/DNS
configuration is unchanged. Staging HTTP requests are blocked at the environment
proxy (CONNECT 403); a GitHub push can be verified, but Cloudflare's deployed
revision, staging protection/indexing headers and live preview cannot be
independently verified here. No production publication or main merge is authorized.

Tests used system Chromium. Bundled Firefox/WebKit engines were unavailable;
those engines, Safari/iOS, real phones and assistive technologies need owner/device
review. Local tests and mocked share/submission APIs do not establish real
WhatsApp messaging, external service availability or actual booking delivery.

Native sharing/clipboard depend on browser support, permissions and secure
context. Favourites are browser/origin-local; staging and production do not share
stored favourites. Query-selected designs share generic static collection social
previews, not unique per-design metadata. JavaScript is required for the viewer,
filters and favourites; the server-rendered fallback remains understandable.

## Owner review checklist

1. Open all three staging collections on phone and laptop; review hero, typography,
   photography, card proportions, controls, spacing and shared navigation/footer.
2. Search by reference; combine category/style/occasion filters; test Clear and
   Load More. Review whether conservative metadata assignments need corrections.
3. Open a design; test full original framing, close/navigation/swipe/focus controls.
4. Save/remove favourites across collections; inspect the shortlist and group labels.
5. Copy/share a design link and reopen it on staging. Inspect prefilled WhatsApp
   text without sending a message unless intentionally authorized by the owner.
6. Confirm image rights, provenance, gender/style classifications and occasion
   assignments before any production approval. No new unreferenced image should
   be published without review.
7. Verify Cloudflare deployed the reported commit and that staging remains protected
   from indexing/access as intended. No automated pass grants production approval.

## Exact changed files

- `_data/collection-designs.json`
- `_data/collection-id-registry.json`
- `_data/collection-image-inventory.json`
- `_data/page-seo.json`
- `_templates/collections.css`
- `_templates/collections.html`
- `assets/collections-navigation.js`
- `assets/collections-v2.js`
- `collections.html`
- `collections/index.html`
- `docs/collection-image-migration.csv`
- `docs/collection-rights-review.md`
- `docs/collections-v2-validation.md`
- `docs/collections-v2.md`
- `docs/shared-components.md`
- `mensuits.html`
- `mensuits/index.html`
- `scripts/build_collections.py`
- `scripts/build_site.py`
- `tests/README.md`
- `tests/business_schema.py`
- `tests/collections-v2.spec.cjs`
- `tests/collections_data.py`
- `tests/header.spec.cjs`
- `tests/phase1.spec.cjs`
- `tests/phase2.spec.cjs`
- `tests/shared_components.py`
- `womensuits.html`
- `womensuits/index.html`
