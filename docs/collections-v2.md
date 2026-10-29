# Collections V2 — architecture, migration and review

Working branch: `phase1/customer-journey-repairs`.
Audit baseline: `4a8b61d9ec16d6d191b0d39af77234d0dd341454`.
No production branch, DNS, hosting configuration or approved page design changed.

## What is built

One static/Python build and one dependency-free gallery controller power three
existing routes: `/collections/`, `/mensuits/` and `/womensuits/`. The latter two
initialize the appropriate gender filter. All use the approved shared header,
footer, SVG icons and navigation, without browser component fetching.

Editorial hero and collection photography lead into an inspiration showroom:
combined search, category/style/occasion controls, counts, explicit Load More,
local favourites, a shortlist and a full-screen accessible design viewer. The
viewer supports original-ratio photographs, ordered multi-photo records, keyboard
and touch/swipe navigation, focus trapping/restoration, Escape, background scroll
locking, verified metadata, design enquiry and sharing. No checkout, prices,
inventory availability, promotions or guaranteed tailoring timelines were added.

Initial cards are server-rendered and enhanced in place; design JSON is emitted
below the page content so it does not delay hero discovery. Only thumbnail-sized
candidates are used in cards; original photographs load on viewer selection.
No new image files, external hosting, paid service or framework was introduced.

## Data and migration

- `_data/collection-designs.json`: schema version, next ID, retired IDs, records.
- `_data/collection-id-registry.json`: permanent ID to immutable source anchor.
- `_data/collection-image-inventory.json`: all asset mappings, legacy references,
  audit commit, source-document hashes, exclusions and missing-reference review.
- [CSV migration inventory](collection-image-migration.csv): generated current
  mappings for originals and derivatives, publication locations, grouping, rights,
  provenance and exclusions.
- [Rights review](collection-rights-review.md): every garment/editorial record,
  including excluded originals; owner confirmation is required before production.

Final inventory: **295 image assets**, **155 root original images** and **138
original garment/editorial candidates** assigned stable IDs. Of these, **111**
were already shown in legacy galleries and are carried into staging; **27** are
excluded from new showroom publication. **265** original/derivative asset rows
map to design IDs; the remaining **30** rows are logos, diagrams, fabric/support
assets or their derivatives. No assets were deleted or modified. No different
photographs have been grouped: one source photograph per current record.
`published` controls showroom exposure, not file privacy; preserved repository
assets remain directly addressable at their existing paths.

The service editorial `standard.jpeg` is recorded separately as MS-138 and kept
out of the showroom: it is not a verified individual garment photograph. Its
existing service-page use was not changed. Fabric-selection/support images are
accounted for but not introduced as garment designs.

No publication licence or authorship proof was inferred from old website use.
All 138 candidate records currently require rights review and have unverified
provenance. No “Made by Mr Sewing” / “Design Inspiration” ownership badge is shown
without explicit evidence. Existing-public usage is the limited basis for the
111 staging inclusions, not a declaration of licence or authenticity. Owner
rights/provenance review is a prerequisite to approving any production release.

Gender/style classifications come from explicit legacy category context, with
source evidence retained. Conflicting/absent classifications are left unknown;
57 published designs remain unclassified by gender rather than guessed. Colours
and descriptive fabric claims were not inferred. Graduation context for h1/h2/h3
comes from approved homepage captions. Consequently, **Graduation is the only
active occasion shortcut**. Wedding/civil, business/executive, celebrations and
modern-African occasion filters require owner-verified assignments before they
are advertised as populated categories. This is intentional, not fabricated data.

## Record schema and future dashboard readiness

Each record contains:

| Field | Rule |
| --- | --- |
| `id` | Permanent `MS-###` reference, never reused or derived from display order |
| `sourceAnchor` | Immutable initial source identity, independent of photo order |
| `slug`, `name` | Stable machine slug and factual display name |
| `gender` | `men`, `women`, or `unclassified` |
| `styles`, `occasions`, `colors`, `garmentType`, `description` | Verified descriptive metadata; unknown values stay empty |
| `images` | Ordered local photographs with source path, alt, intrinsic dimensions and focal position |
| `provenance` | `made_by_mr_sewing`, `design_inspiration`, `unverified`; verified labels need evidence |
| `rightsStatus` | `review_required`, `approved`, `restricted` |
| `published` | Boolean; new imagery requires rights approval, not repository presence |
| `publicationBasis`, `sources`, `metadataEvidence` | Traceable prior use/classification, never invented claims |
| `groupingEvidence` | Required before multiple photographs are assigned to one garment |

A future authenticated dashboard can edit these records and trigger the same
build. No admin, database, authentication or CMS is implemented now.

### Adding or changing content through Codex

1. Preserve original files; record their source and rights status in the inventory.
2. Allocate `nextId`, increment it, and append the ID/source anchor to the registry.
   Do not renumber, recycle IDs or rewrite anchors when sorting or changing names.
3. Add records unpublished until rights review is complete. Verify metadata; keep
   uncertain colours, occasions, fabrics and provenance empty/unverified.
4. Use existing derivative tooling if needed; map every derivative to its source.
   Supply accurate dimensions/alt text and positions (`center`, directional words,
   or bounded percentage coordinates). Preserve original-ratio full-size photos.
5. Group photos only with explicit same-garment evidence. Ordering the image array
   must not change ID/source anchor. Retired IDs stay in the registry; removing a
   record requires adding its ID to `retiredIds`, not recycling it.
6. Build and check all generated outputs, review the migration/rights reports,
   test, and commit generated pages. No three-page manual data duplication.

```sh
python3 scripts/build_site.py
python3 scripts/build_site.py --check
python3 tests/collections_data.py
python3 tests/shared_components.py
node tests/collections-v2.spec.cjs
```

Check mode does not rewrite files. It rejects stale generated HTML/navigation/
reports, duplicate IDs/slugs, ID reuse, missing/uninventoried assets, malformed
records, invalid provenance claims, unsupported grouping, and inappropriate new
publication. The actual page template/CSS live in `_templates/collections.*`;
`assets/collections-v2.js` is the single gallery interaction source.

## Legacy URL compatibility and canonical strategy

No new collection route names or server redirect rules were needed. Existing
`.html` aliases retain query/hash-preserving browser redirects to clean URLs;
these are not claimed HTTP 301 responses. Canonicals remain production URLs.
Filtered/deep-link URLs canonicalize to their page's base route; no additional
indexable product pages or product-for-sale schema were created.

| Existing URL | Compatible behavior | Equivalent new gallery view |
| --- | --- | --- |
| `/collections/` | New complete showroom; same canonical | `/collections/` |
| `/mensuits/` | New Men's collection; same canonical | `/mensuits/` |
| `/womensuits/` | New Women's collection; same canonical | `/womensuits/` |
| `/m-classicsuits/` | Existing specialist category view preserved | `/mensuits/?style=classic` |
| `/m-doublebreasted/` | Existing specialist category view preserved | `/mensuits/?style=double-breasted` |
| `/m-kaundasuits/` | Existing specialist category view preserved | `/mensuits/?style=kaunda` |
| `/m-modernsuits/` | Existing specialist category view preserved | `/mensuits/?style=modern` |
| `/w-classicsuits/` | Existing specialist category view preserved | `/womensuits/?style=classic` |
| `/w-doublebreasted/` | Existing informational/coming-soon view preserved | Women's filter has no verified matches yet |
| `/w-modernsuits/` | Existing informational/coming-soon view preserved | Women's filter has no verified matches yet |
| `/suits/` | Original functional mixed gallery preserved | `/collections/` for the new combined experience |

The new pages link the specialist routes through a compact disclosure. Useful
legacy pages were not swept into a generic redirect. Their canonicals/search
visibility and existing behaviour remain intact; no redirect loops were added.

## Sharing, favourites and progressive enhancement

Deep links use the current origin and `/collections/?design=MS-045#design-MS-045`.
Staging links therefore stay on staging; future production copies use production
without a code change. Direct loads, reload, history navigation and unavailable
IDs are handled. Filter state is also encoded in query parameters.

The native share sheet is used when available, with clipboard and a selectable
link fallback. Cancel/failure feedback and duplicate-share protection are tested.
Design WhatsApp messages contain name, reference and the public deep link, not
internal asset paths or prices. Messages are constructed locally, not sent by
this implementation/test process.

Favourites store only stable IDs in `mr-sewing:favourites:v1`. No account, personal
data, tracker or cross-device synchronization. Blocked storage has a truthful
page-only fallback; unknown/retired IDs are discarded safely. WhatsApp shortlists
are split into explicitly labelled groups of eight, with a Next Group control.

The viewer/search/saved features require JavaScript. Without it, initial cards,
final booking/contact links and a complete named reference index with original
photo links remain available. Static hosts cannot emit a unique social metadata
response per query-selected design: social previews use the appropriate generic
collection metadata/image. This limitation is explicit; no unsupported dynamic
server route or per-design preview service is claimed.

## Review and validation

See the accompanying staging validation report for exact files, tests,
measurements, screenshot paths, deployment status and owner review checklist.
Visual approval is separate from automated test success.
