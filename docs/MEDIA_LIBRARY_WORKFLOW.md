# Clothing media library and Showroom workflow

The library reuses approved files in place. No upload service, paid AI classifier, second Shop catalogue or new quotation form is installed.

## Find a photograph by its original filename

Use the Showroom search field for published photographs. Original filenames appear on the cards. For every recovered file, including held media, search the generated `docs/media-recovery-inventory.json` or `docs/MEDIA_RECOVERY_INVENTORY.md`:

```sh
rg -n -F 'm-kaundasuits3.jpeg' docs/media-recovery-inventory.json
```

`mediaId` identifies the stored path using SHA256, so `a/photo.jpg` and `b/photo.jpg` remain distinct even though both original filenames are `photo.jpg`. A build rejects duplicate media identities. The full hash and exact stored path in the recovery report also identify byte-identical files; duplicate groups are retained, not deleted. A filename is a reference, not proof of rights.

## Where facts are maintained

| Information | Authoritative source |
| --- | --- |
| Existing design ID, original images, publication/right evidence, garment metadata | `_data/collection-designs.json` and `_data/collection-id-registry.json` |
| Approved suit audience/style assignments and customer-friendly names | `_data/suit-reference-categories.json` |
| Genuine completed-work status and photo permissions | `_data/customer-projects.json`, through `scripts/project_catalog.py` |
| Existing image recovery records | `_data/collection-image-inventory.json` |
| Separate video publication/classification evidence | `_data/media-video-records.json` |
| Homepage feature choices | `_data/media-library-settings.json` |
| Shop products, stock, prices and checkout eligibility | `_data/shop-products.json`, through its existing gates |
| Narrow permission to display existing Shop enquiry listings | `_data/shop-public-enquiries.json` |

`scripts/media_library.py` derives the reusable library through `build_collections.load()` and the approved-project loader. It also projects separately validated, published clothing merchandise through `shop_catalog.load()`; it does not promote enquiry-only drafts. Never publish raw collection `published:true` flags: many older records still lack permission. The generated `_data/media-library-index.json` contains eligible customer-facing items only; it is an output, not a second editable source. The generated recovery reports cover all image records and discovered MP4/WebM files, including held and non-clothing support assets, without exposing them in the Showroom.

## Add an image and activate its category

1. Obtain explicit publication permission and confirm whether it is Reference Design, genuine Our Work or a separately approved Shop Product. A reference photograph must never be called completed Mr Sewing work without project evidence.
2. Preserve the original filename and store the file once. Register its stable design identity and exact original path using the existing collection records/inventory. Supply genuine title, alt text, dimensions and the required provenance/permission evidence. Do not fabricate creator names, fibre facts or stock.
3. Review audience, garment type and style tags. Existing suit assignments belong in `suit-reference-categories.json`; new garment metadata must have its approval evidence in the collection record. Suggestions or recovered filenames do not approve classifications.
4. Set publication only after the effective permission gate accepts the record. Genuine project photographs also require completion and per-photo association/permission evidence in `customer-projects.json`.
5. Rebuild. The Showroom computes facets from eligible published records; a reviewed `dress` or `shirt` garment automatically activates that category when it first has an eligible item. Held or archived records cannot activate it. A garment without a verified audience remains in All rather than acquiring an invented gender.
6. Test the card, original filename, exact design detail link and the existing selection → fabric → quotation journey. Existing internal design IDs stay in the system; customer cards show friendly names and the requested original filename.

No image rights approval is inferred from Git presence, an older gallery, a Shop association or a technical thumbnail. Existing images and previously approved public URLs are retained for compatibility. Any destructive file/URL migration requires a separate reviewed plan.

## Videos and homepage featuring

Seven existing MP4 files were recovered at the initial audit. **None has a separate approved clothing-video record, so none is activated in the new Showroom or showcase.** Image fallbacks provide the initial experience.

The empty `_data/media-video-records.json` is the authoritative record for future video facts, not a copy of image approvals. To publish a video, the owner must review a record containing:

```json
{
  "assetPath": "/original-reviewed-video.mp4",
  "title": "An accurately described clothing video",
  "alternativeText": "Description of the content",
  "audience": "men",
  "garmentType": "suit",
  "styleTags": ["single-breasted"],
  "classification": "reference-design",
  "publicationStatus": "draft",
  "sourceOrCreator": null,
  "durationSeconds": 20,
  "posterMediaId": "THE_EXISTING_APPROVED_PHOTOGRAPH_MEDIA_ID",
  "usageRights": {"approved": false, "evidenceRef": null, "date": null},
  "metadataApproval": {"approved": false, "evidenceRef": null, "date": null},
  "uploadMetadata": null
}
```

This is an instructional draft example, not a published product or permission statement. Actual paths/posters must exist, both approvals need real references and dates, and publication must be explicitly approved. `our-work` also needs a genuine approved `projectSlug`; `shop-product` needs a fully published `shopProductId`. Photograph permission does not automatically approve a video. A linked `designId`, if used, must already be eligible for the existing enquiry system. Unrelated videos, logos and measurement diagrams are never automatically classified into clothing.

Videos use native controls, are muted by default, have an approved poster and a separate-open fallback, and preload no video data. They do not autoplay, so reduced-motion users do not encounter automatic video movement. No paid/dynamic classification is performed.

To change homepage features, edit only `_data/media-library-settings.json`:

```json
{
  "homepage": {
    "cards": [
      {"audience": "men", "mediaId": "EXISTING_APPROVED_MEDIA_ID"},
      {"audience": "women", "mediaId": "EXISTING_APPROVED_MEDIA_ID"}
    ],
    "featuredMediaId": "ANOTHER_EXISTING_APPROVED_MEDIA_ID"
  }
}
```

Use the real generated IDs, not these example labels. The two cards must match their reviewed audiences. The larger feature can use an eligible approved photograph or separately approved video. A draft/archived/unapproved item causes validation to fail rather than silently appear. The initial features reuse already approved men's/women's references and genuine completed work; original homepage content remains beneath them.

## Rebuild, inspect and recover

```sh
python scripts/build_site.py
python scripts/build_site.py --check
python tests/media_showroom.py
```

`scripts/showroom.py:outputs()` generates `/showroom/`, its small local JS/CSS, the eligible library index and recovery reports. `homepage_showcase()` and `homepage_css()` are reused by the homepage builder. Showroom filter URLs use `audience`, `garment`, `style`, `kind` and `q`; other quotation/selection parameters are preserved. Existing detail routes and canonical original-photo links remain the quotation authority.

All originals remain in their original paths and in Git history. Before changing a physical reference, retain the current committed version and its recovery hash report. Restore a missing original from the recorded Git version, then verify its SHA256 before rebuilding. Do not delete a duplicate just because hashes match: existing links may depend on both paths. No unapproved deletion or automatic recovery publication is part of this workflow.

Shop links lead to existing listings and do not imply ready stock or direct purchase. An existing clothing design may link to a matching enquiry-only Shop listing without gaining new image rights. Separately published clothing products that pass `shop_catalog.load()` can supply Shop-only media automatically, using their approved image rights and exact product destination. These cards are labeled Shop Product; no suit design ID or quotation identity is invented. Price and stock are never copied into a second catalogue.

Known clothing category labels are mapped conservatively to garment tags. Unknown clothing groups need the product's reviewed `showroom` metadata (`audience`, `garmentType`, `styleTags`, and `metadataApproval` with approved/evidenceRef/date). Non-clothing hangers, covers and footwear remain excluded. Shared physical photographs are not duplicated. Current data still contains no sale-published products, so the Showroom initially has 28 approved design/project photographs only.

## New garment enquiry scope

Current selected-design quotation references are approved suits/tuxedos. New non-suit reference collections need a reviewed garment-appropriate enquiry mapping before publication; do not apply the ordinary-suit seven-day deadline screen to shirts or dresses by assumption. The existing Special Tailoring form provides human assessment for those requests. Published Shop-only clothing uses its actual Shop destination rather than being assigned a fabricated ordinary-suit identity. Generic filters alone do not establish new production commitments.


## R53 — Owner uploads integrated19November2026

The actual upload commit is `ce98ee3991a43483357304b5fe9f2f0a83f7ae27`, fetched before integration. It adds25named fashion photographs and two videos. The25files are prepared as22new stable design/variant records MS-152–MS-173 across17families. No original was resized, renamed, deleted or replaced. Actual dimensions are stored; the catalogue's1200×1500standard is not fabricated as the source size. See [R53_IMAGE_MATCHING.md](R53_IMAGE_MATCHING.md) for every filename, catalogue number, ID, category and exact blocker.

- New records remain `published:false`, `rightsStatus:review_required`. Upload/catalogue text is metadata evidence, not a licence. The existing28eligible photographs remain the public Showroom.
- `family` and `family.variant` belong to existing collection records. `catalogueNumbers`, each image's `viewLabel`/`catalogueNo`, and prepared category assignments retain exact identities. No second image or quotation database was added.
- Sovereign has four colour-reference records; Admiral has three. Ivory Heritage has one record with angled/front/detail photos. The file labelled Olive for catalogue12actually shows Burgundy, different from actual Olive6; it is prepared with Burgundy5pending the explicit correction. Pearl Gold10has completed individual visual review; the owner-provided name is retained without claiming gold hardware, and its rights hold remains.
- Held assignments live under `suit-reference-categories.json:preparedAssignments`. After actual rights and metadata approval, move a reviewed assignment into its existing category's published `designIds`/`references`, record actual permission evidence, clear resolved blockers and approve the record. The loader refuses a family publication without these steps. Never clear a blocker merely to make a build pass.
- `scripts/design_families.py` renders same-family/same-audience colour-reference links from effective published records only. Existing detail components show each design's multiple views and retain exact photo selection through WhatsApp/fabric/quotation. Its optional metadata is preserved by the loader.

Both `1024X768VIDEO.mp4` and `1024X768black.mp4` are actually720×1280portrait men's suit videos. They are registered draft records with verified hash, bytes, codecs, durations, fast-start and successful full-decode results; no filename-derived resolution claim is made. Explicit video/audio rights, publication/classification approval and an approved exact poster remain missing. Extracted poster candidates stay outside the deployed tree.

`homepage.pendingVideoShowcase` describes the two proposed video cards with truthful men's audiences and approved image fallbacks. It cannot activate media: the build validates its hashes/status/fallbacks while rendering only `homepage.cards`/`featuredMediaId`. Existing approved men's/women's image cards and the genuine large suit photograph remain active. See [R53_VIDEO_REVIEW.md](R53_VIDEO_REVIEW.md).
