# 26 November 2026 — Gallery and workmanship review

Scope: owner’s comprehensive website improvement instruction, sections9–15,27–29,34–35. Staging only on `phase1/customer-journey-repairs`; baseline `b388644796fcb24b747bb6818dd211422fab9cff`. This report is internal development evidence, not public website copy.

## Applicable authority and pre-edit audit

Read root `AGENTS.md`, the current `.github/customer-content-reference/README.md` and its25November master/source matrix/unresolved/page-map records. Existing R40 eight-image Kaunda approval, R41 SEO preservation, R44 category recommendations, R59 sorting and R61 media authorization remain applicable. The26November owner instruction authorizes compact photographic galleries, meaningful names, removal of public technical references and verified-workmanship marking. It does not approve new photographs, stock, manufacturing history, prices or a production release.

The effective publication-gated loader contained28design records. The original registry had meaningful approved names, but `design_name()` replaced most with generic “Tailored Suit”, “Women’s Suit” or “Tailoring Design”. The detail builder visibly injected “ReferenceMS-…” and repeated the identifier in search/social metadata. Showroom controls occupied multiple rows before the photographs. Category galleries reconstructed their array order and bypassed verified-date sorting. The OurWork loader had no shared date ordering even though the five projects were already completion/permission-gated.

## Changes in authoritative sources

- `scripts/build_collections.py`: meaningful registered names; no public technical reference captions/title/meta descriptions; exact IDs/routes/photos remain in selection data. Shared verified-date sorting also serves category galleries. Photo cards show a discreet workmanship classification derived from the gated project source, never from rights approval alone.
- `_templates/collections.html`, `_templates/collections.css`, `assets/collections-v3.js`: short Showroom header, compact category links, search and one accessible native Filters disclosure; functioning style/occasion/reset/load-more controls and browser-history state remain. All first12cards remain in initialHTML; the complete no-JavaScript link list remains. Two-column mobile photographs use `object-fit:contain`.
- `_templates/collection-design.html`: public name, category, photograph and existing selection/share/full-photo actions remain; no unnecessary reference label. Design page titles distinguish their design-detail purpose from genuine project pages.
- `scripts/suit_references.py`: same central date policy within each category, preserving category membership and undated ordering.
- `scripts/project_catalog.py`, `scripts/build_journey.py`, `_templates/customer-project.html`, `_templates/journey.css`: genuine-work source gates unchanged; compact two-column mobile project index and explicit Made by Mr Sewing marks; full project details remain accessible.

## Kaunda visual name review

All eight original files were visually inspected on26November2026, including a contact sheet stored outside deployment at `/workspace/review/2026-11-26/kaunda-inspection.png`. Names and descriptions concern visible features only. `collection-designs.json` and the existing category reference labels were updated together, preserving IDs, original paths, approval dates and rights/provenance status.

| Original file | Preserved ID | Public name |
|---|---|---|
|m-kaundasuits1.jpeg|MS-029|Kaunda Jacket Style Selection|
|m-kaundasuits2.jpeg|MS-030|Black Short-Sleeved Kaunda Suit|
|m-kaundasuits3.jpeg|MS-031|Black Stand-Collar Kaunda Suit|
|m-kaundasuits4.jpeg|MS-032|Burgundy Stand-Collar Kaunda Jacket|
|m-kaundasuits5.jpeg|MS-033|Teal Stand-Collar Kaunda Jacket|
|m-kaundasuits6.jpeg|MS-034|Light Blue Four-Pocket Kaunda Jacket|
|m-kaundasuits7.jpeg|MS-035|Navy Stand-Collar Kaunda Jacket|
|m-kaundasuits8.jpeg|MS-036|Cream Four-Pocket Kaunda Jacket|

These photographs remain **Design Inspiration**. Their permission does not establish manufacturing origin. To mark any as Made by Mr Sewing, the owner must provide/confirm completed-work and exact photograph association evidence through the existing project catalogue. No new permission request is needed merely because the files already exist in the repository.

The three existing Off-White Graduation Suit records keep their separate compatible IDs/URLs. Their already documented front/side/graduation views receive clear view labels, avoiding duplicate metadata without removing links or altering the garment identity.

## Sorting and unresolved evidence

Sorting uses only source-backed `mediaDateAdded` with `mediaDateEvidence` and an allowed verified-upload/publication/added basis. Known dates sort descending; ties and unknown dates preserve a stable existing order. Upload date is not represented as garment manufacturing date. Category filtering, search and load-more consume that order. No historical date was invented. A future approved dated item will automatically precede undated records. R53 prepared/held records remain held until deliberate placement; this visual task does not auto-publish them.

## Verification

`python tests/customer_gallery_experience.py`: PASS at source-render level for28eligible design identities/photos, unique meaningful detail titles, removal of visible technical codes, five permission-gated projects, strict workmanship eligibility, initial12HTML cards, compact filters, source-backed date/unknown/tie/category-order fixtures and unchanged category memberships. Python compilation and JavaScript syntax checks passed.

Integrated build, browser/mobile/keyboard screenshots, accessibility and deployed-origin verification are recorded by the parent task after generation. They are not inferred from source tests. Existing historical screenshot-preservation tests freezing November12copy may require the documented26November approved presentation changes to be distinguished from protected ID/photo/security contracts.
