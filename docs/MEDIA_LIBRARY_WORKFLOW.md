# Clothing media workflow

Reconciled 25 November 2026. Reuse existing records rather than creating another gallery database.

## Sources

- `_data/collection-designs.json`: stable design IDs, original filenames/paths, descriptions, image views, audience, style, optional family/colour-variant metadata, rights and deliberate publication state.
- `_data/collection-id-registry.json`: append-only ID-to-source identity. Do not repurpose an old ID for another photograph.
- `_data/collection-image-inventory.json`: every actual website image, including explicitly excluded document/poster/technical assets. Local ignored QA/dependency output is excluded from the scan; real unregistered website media still fails the build.
- `_data/suit-reference-categories.json`: approved category membership and prepared assignments. `_data/clothing-category-config.json` supplies the two initial hub/Showroom categories.
- `_data/customer-projects.json`: verified completed work with scoped permission/project evidence. A fashion reference must not become “Our Work” merely because the owner permits display.
- `_data/media-video-records.json`: original-video evidence, owner-represented permission, approved silent playback and exact poster metadata.
- `_data/shop-products.json` and `_data/shop-public-enquiries.json`: independent Shop publication/visual-enquiry authority. Reusing a reference image does not grant stock, price or checkout approval.

The active Showroom is `/collections/`. The recovered `/showroom/` compatibility entry preserves old audience/filter/context links without introducing a second catalogue.

## Finding and grouping an original

Use `rg -n --fixed-strings 'original-filename.webp' _data docs`. Keep the original file and its ID. Duplicate basenames need separate path identities; do not delete duplicates without reviewing existing links.

R53's 25 uploaded photographs are prepared as 22 records, MS-152–MS-173. Sovereign and Admiral retain colour families; Ivory Heritage retains angled/front/detail views within one design. Catalogue image12 is actually Burgundy despite its original Olive filename; the corrected metadata preserves that filename. These prepared records remain unpublished until deliberate category/metadata placement is reviewed. Do not claim owner permission is still missing: R61 records the owner's repository-media authorization. That is owner-represented permission, not a completed independent third-party licence audit.

`scripts/design_families.py` and the existing collection/detail builder use only genuinely eligible records and exclude unpublished/current/other-audience choices. Test family membership, variant links and exact selected photograph mapping before publication.

## Publication and homepage reuse

1. Review actual image/video content, truthful name/category/views and evidence. A file upload is not inventory or completed-garment proof.
2. Record applicable permission and approval scope without inventing creator, fabric composition, production history, stock or technical guarantees.
3. Assign a deliberate eligible category and clear only genuinely resolved blockers. Set publication status through the existing records and loaders.
4. Reuse the existing design-detail, selected-design, fabric and quotation journey. Do not create another form or Shop product just to display a reference.
5. Use `scripts/media_sorting.py` for verified date-added/upload/publication metadata. Keep unknown dates in their documented stable order and ties stable. Never call an upload date a garment-manufacture date. Keep family/views together.
6. Homepage rows draw from the same approved records. Latest R63/R64 presentation uses opposite directions with tap/keyboard/Escape pause and reduced-motion support; do not restore an obsolete visible-button design.

## Silent homepage video preparation

The originals `1024X768VIDEO.mp4` and `1024X768black.mp4` are preserved. They are men's suit references; neutral cards do not relabel one as women's clothing.

Prepare temporary video-only copies with `python scripts/prepare_silent_homepage_videos.py --output-dir /tmp/mrsewing-silent-review`. The reviewed build workflow copies verified derivatives to `assets/videos/suit-light-silent.mp4` and `suit-black-silent.mp4`, with exact-frame posters alongside. Keep registered hashes/sizes/technical evidence synchronized after a genuinely reviewed replacement.

`scripts/homepage_video_cards.py` requires the actual original hash, derivative/poster hashes, safe paths and an MP4 containing one video track and no audio. It never falls back to the audible original. Missing or changed playback assets use approved photographs. Preparation does not grant permission or automatically activate a record.

## Recovery and verification

Keep originals, prior records and Git history. The pre-recovery workspace bundle/archive is documented in the master register. Restore missing files from their known commit, verify hashes and review publication status before rebuilding; recovery does not automatically approve display.

Run the full site build and `--check`, technical/media sorting/video/publication tests, actual browser checks and selection/payload mocks. Inspect generated outputs, card/detail/photo identity, responsive presentation and actual staging responses. Root/source records are protected by the staging Pages boundary; this does not make the public Git repository or old deployments private.
