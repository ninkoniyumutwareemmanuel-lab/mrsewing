# R53 — Uploaded fashion photographs: actual matching and registration

Owner corrective instruction19November2026. Uploaded source commit `ce98ee3991a43483357304b5fe9f2f0a83f7ae27` was inspected directly after fetching the staging branch. This supersedes the earlier local-only missing-file diagnosis: the files were in a newer remote commit. All25originals are retained at their exact uploaded paths and have now been registered in the existing collection/ID/inventory/category sources. No additional gallery database or physical image copy was created.

## Implemented records and gates

- **22new stable design/variant records:** `MS-152` through `MS-173`; next available ID174. All151earlier records and registry mappings are unchanged.
- **25registered photographs**, grouped into **17families/standalone references**: four Sovereign colour-variant records, three Admiral colour-variant records, one three-view Ivory Heritage record and14standalone records.
- **All22new records remain held** (`published:false`, `rightsStatus:review_required`): neither the draft catalogue nor the corrective instruction supplies usage-rights/publication evidence for the third-party reference images. Exact blockers are stored on each record. Technical metadata is prepared; an approval flag was not invented. Existing28effective published photos remain visible; new held photos do not enter Showroom/cards/home/quotation allowlists.
- Prepared categories and friendly labels are in `_data/suit-reference-categories.json` → `preparedAssignments`, not inserted into the live `categories[].designIds`. The existing gallery architecture requires those arrays to contain eligible designs. Each new collection record also has `proposedCategoryId` and `family` metadata for the reusable renderer.
- References are identified as `design_inspiration` / `reference-design`. Creator remains unknown. No price, fibre composition, stock, package entitlement or manufactured-by-Mr-Sewing claim was invented.

## Direct visual findings and corrections

**Catalogue12 is Burgundy, not Olive.** Its actual file `sovereign-gold-button-double-breasted-suit-01-olive.webp` shows a burgundy gold-button jacket over a burgundy high-neck underlayer with ivory trousers. It is not a duplicate of the olive photograph in6: both SHA256 and decoded RGB pixels differ. It is prepared as the second Burgundy styling view with5under `MS-156`, with an explicit owner metadata-correction hold. The original misleading filename is preserved. Catalogue6 is the sole actual Olive Green variant `MS-157`. This is a visual classification, not proof of the same physical garment or publication approval.

**Pearl Gold Executive10** was inspected individually. It shows a white two-piece pantsuit with four black buttons, notched lapels, flap pockets and a black underlayer. No gold accessories are confirmed. It remains a separate record `MS-161` from Ivory Noir16`MS-166`, with its concise verified description. Individual review is complete: Pearl Gold Executive remains the owner-provided design name and does not assert gold hardware. Its publication-rights hold remains.

**Ivory Heritage19–21** shares the visible ivory colour, stitching, rounded pocket construction and button arrangement. One record `MS-169` retains the three actual paths in requested gallery order21angled,19front,20close-up, each with its own descriptive alt text and view label.

**Sovereign Burgundy5:** no pre-existing collection record named Burgundy Sovereign was found. A new prepared Burgundy variant holds the actual uploaded5and12views; no absent primary photograph or legacy identity was fabricated.

**Formal11and Contemporary Formal17** are prepared under the existing Men’s Tuxedos & Formalwear category as formalwear references. Their asymmetric styles remain descriptive metadata; this does not classify them as ordinary tuxedo packages, create empty categories or approve production capability.

**Image dimensions:** the supplied1200×1500image standard is not the actual upload metadata. Files are900×1200,1024×1536,1086×1448or1122×1402. All actual dimensions are stored; no original was resized, cropped or upscaled. Consistent presentation must be achieved by the existing responsive media container, not fabricated intrinsic dimensions.

## Exact uploaded-file mapping

| Catalogue | Stable ID | Design / variant | Existing original file | Prepared category | Actual pixels |
| --- | --- | --- | --- | --- | --- |
|1|`MS-152`|Stone Regent Elegance|`stone-regent-chain-brooch-double-breasted-suit-01.webp`|`men-double-breasted`|1086×1448|
|2|`MS-153`|Steel Grey Signature|`steel-grey-signature-three-piece-womens-suit.webp`|`women-three-piece`|1024×1536|
|3|`MS-154`|Sovereign Gold-Button Elegance — Black|`sovereign-gold-button-double-breasted-suit-04-black.webp`|`men-double-breasted`|1086×1448|
|4|`MS-155`|Sovereign Gold-Button Elegance — Navy Blue|`sovereign-gold-button-double-breasted-suit-03-navy.webp`|`men-double-breasted`|1122×1402|
|5|`MS-156`|Sovereign Gold-Button Elegance — Burgundy|`sovereign-gold-button-double-breasted-suit-02-burgundy-angle-02.webp`|`men-double-breasted`|1086×1448|
|6|`MS-157`|Sovereign Gold-Button Elegance — Olive Green|`olive-sovereign-gold-button-double-breasted-suit-01.webp`|`men-double-breasted`|1086×1448|
|7|`MS-158`|Scarlet Crest Elegance|`scarlet-crest-chain-brooch-double-breasted-suit-01.webp`|`men-double-breasted`|1086×1448|
|8|`MS-159`|Sandstone Navy Elegance|`sandstone-navy-gold-button-double-breasted-suit-01.webp`|`men-double-breasted`|1086×1448|
|9|`MS-160`|Admiral Chain-Brooch Elegance — Pink|`pink-admiral-chain-brooch-double-breasted-suit-02.webp`|`men-double-breasted`|1086×1448|
|10|`MS-161`|Pearl Gold Executive|`pearl-gold-executive-womens-suit.webp`|`women-double-breasted`|900×1200|
|11|`MS-162`|Onyx Silver-Chain Elegance|`onyx-silver-chain-asymmetric-suit-01.webp`|`men-tuxedos-formalwear`|1122×1402|
|12|`MS-156`|Sovereign Gold-Button Elegance — Burgundy|`sovereign-gold-button-double-breasted-suit-01-olive.webp`|`men-double-breasted`|1086×1448|
|13|`MS-163`|Navy Atelier Elegance|`navy-atelier-tailored-skirt-suit.webp`|`women-skirt-suits`|1024×1536|
|14|`MS-164`|Mahogany Paisley Elegance|`mahogany-paisley-asymmetric-double-breasted-suit-01.webp`|`men-double-breasted`|1086×1448|
|15|`MS-165`|Ivory Noir Shawl Elegance|`ivory-noir-shawl-collar-double-breasted-tuxedo-01.webp`|`men-tuxedos-formalwear`|1086×1448|
|16|`MS-166`|Ivory Noir Elegance|`ivory-noir-elegance-womens-suit.webp`|`women-double-breasted`|1024×1536|
|17|`MS-167`|Ivory Nocturne Elegance|`ivory-nocturne-sash-waist-formal-suit-01.webp`|`men-tuxedos-formalwear`|1086×1448|
|18|`MS-168`|Ivory Midnight Speckled Tuxedo|`ivory-midnight-speckled-tuxedo-jacket.webp`|`men-tuxedos-formalwear`|1122×1402|
|19|`MS-169`|Ivory Heritage Elegance|`ivory-heritage-patch-pocket-suit-03.webp`|`men-single-breasted`|1122×1402|
|20|`MS-169`|Ivory Heritage Elegance|`ivory-heritage-patch-pocket-suit-02.webp`|`men-single-breasted`|1122×1402|
|21|`MS-169`|Ivory Heritage Elegance|`ivory-heritage-patch-pocket-suit-01.webp`|`men-single-breasted`|1122×1402|
|22|`MS-170`|Ivory Diamond Lattice Elegance|`ivory-diamond-lattice-shawl-lapel-tuxedo-01.webp`|`men-tuxedos-formalwear`|1086×1448|
|23|`MS-171`|Admiral Chain-Brooch Elegance — Crimson Red|`crimson-admiral-chain-brooch-double-breasted-suit-03.webp`|`men-double-breasted`|1086×1448|
|24|`MS-172`|Champagne Cocoa Elegance|`champagne-cocoa-peak-lapel-double-breasted-suit-01.webp`|`men-double-breasted`|1086×1448|
|25|`MS-173`|Admiral Chain-Brooch Elegance — Burgundy|`burgundy-admiral-chain-brooch-double-breasted-suit-01.webp`|`men-double-breasted`|1086×1448|

Every table row is held for usage-rights/publication evidence. Rows5/12also have the source-colour correction hold;10has completed individual visual review and remains held only for publication rights. Names/descriptions identify visible reference styling only.

## Checks actually performed

PASS: direct contact-sheet review of all25files and individual review of Pearl10and mislabelled12; actual dimensions/SHA256/decode comparison; collection loader returns the existing28effective eligible references; exactly22new held records,25paths,17families; four Sovereign and three Admiral variants; Ivory view order21/19/20; Burgundy grouping5/12; all25uploaded file bytes unchanged against ce98ee3; original151records/registry entries preserved. This registration step did not build, commit, push, deploy, modify permissions or send customer enquiries. Parent task performs integrated build/browser/release checks.
