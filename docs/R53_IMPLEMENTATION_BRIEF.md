# R53 — Actual uploaded media and approved PDF implementation brief

19 November 2026. Work only on `phase1/customer-journey-repairs`; current uploaded baseline `ce98ee3991a43483357304b5fe9f2f0a83f7ae27`, following the reviewed R52 commit `812aaca489bec127308520dce166b9298419d9d2`. This is an implementation brief, not a completed-test or deployment report. No main/production change is authorized.

## Actual sources and correction

The latest owner instruction is **“CODEX — CORRECTIVE IMPLEMENTATION TASK: FINISH THE UPLOADED MEDIA AND PDF INTEGRATION”**, 19 November 2026. The owner says the files are already uploaded and explicitly approves the supplied Terms PDF content. The actual new Git commit contains 25 named WebP photographs, `1024X768VIDEO.mp4`, `1024X768black.mp4` and `Mr_Sewing_Fashion_Terms_and_Conditions_v1_Approved.pdf`. Its filenames correspond to the owner's 25-entry fashion catalogue and family/view instructions.

The earlier audit used the older local checkout. Fetching the requested branch supplies the uploaded commit; its file absence statements must not be reused as current evidence or as a reason to ask the owner to upload again. Existing historical reports remain recoverable. Inspect the actual branch tip/FETCH_HEAD, not a stale remote-tracking ref, before an ordinary safe fast-forward.

Instructions read for this brief: root `AGENTS.md`; current customer-reference README and applicable latest sections of the master, source matrix, unresolved register, page map and communication library; required page-brief checklist; `docs/WEBSITE_SOURCE_MAP.md`; `docs/MEDIA_LIBRARY_WORKFLOW.md`; `docs/POLICY_DOCUMENT_WORKFLOW.md`; actual upload commit/file list. Actual photograph/video/PDF content and technical findings are assigned to implementation reviews. This brief does not claim the missing original company operating handbooks, image licensing originals or a completed legal review were read or established.

## Applicable rules and preserved customer information

Current reference: `versions/2026-11-19-03`. R53 supersedes the older upload-absence/draft-only handling and establishes existing PDF content approval. R51/R52 still own the current architecture, universal Showroom, tailoring-first homepage, quotation-first public service presentation, central sources and manual WhatsApp priority. Existing R41 SEO, R46 selection lifetime, R48 shared fabric/colour and R49 quotation/measurement/delivery rules remain scoped and unchanged unless actual PDF reconciliation identifies a separately approved change.

- Services and eligibility remain in their existing records. No unsupported garment capability, stock, fibre composition, price, completion or manufacturing claim is added from a photograph.
- Service experience, design source and priority remain independent axes. Preserve men's/women's selections, exact photographs, individual quantities, shared fabric/colour, quotation review and explicit submission.
- Quotation, acceptance, payment verification, official order confirmation and production-start notice remain different events. Existing domestic/international exceptions, delivery/collection and benefits are not silently rewritten by media metadata.
- Existing Terms/Refund/Privacy, fabric/measurements guidance, official contacts and separate service rules remain available. Do not replace a working Terms route with an empty notice if PDF activation is blocked.
- No new provider, image upload service, payment integration, private feature, tracking or automatic message is introduced. Existing consent/honeypot/allowlist/failure safeguards remain.

## File ownership and safe implementation

| Area | Existing authoritative paths | Required implementation |
| --- | --- | --- |
| New photographs | `_data/collection-designs.json`, `_data/collection-id-registry.json`, `_data/collection-image-inventory.json` | Add missing stable reference records from actual originals, preserving IDs/paths/history. Supply verified names, visible-feature descriptions, dimensions, alt text and evidence. |
| Category/family relationships | `_data/suit-reference-categories.json` and existing collection/detail components | Verify Sovereign colour family/Olive files, Admiral colours and Ivory Heritage views; retain exact view identity and safe current category mapping. No second gallery database. |
| Showroom/media projection | `scripts/media_library.py`, `scripts/showroom.py`, existing templates | Display eligible references only. Colour/view controls choose photographed references, not confirmed fabric stock; preserve exact quotation/WhatsApp context. |
| Videos/homepage features | `_data/media-video-records.json`, `_data/media-library-settings.json`, existing showcase renderer | Inspect actual requested files, register real technical/content metadata, review posters/performance and prepare both slots. Keep approved image fallbacks until genuine publication approvals pass. |
| Approved Terms PDF | `_data/policy-documents.json`, `scripts/policy_documents.py`, `scripts/publish_policy_document.py`, existing viewer templates | Inspect/validate supplied content-approved bytes, version/checksum/history and operational consistency. Do not fabricate a legal review or dates. Preserve current readable Terms if a precise blocker prevents activation. |
| Existing quotation and consent | Current selection/request-context, validators, provider and Terms controller | Reuse complete-photo/quantity handling and manual-send safeguards; no duplicate form or competing workflow. |
| SEO/build/deployment | Current SEO intent/metadata, sitemap/robots/headers and builders | Preserve URLs, canonical structure, alt text and indexing purpose. Test actual outputs; stage only. |

No original file is deleted, renamed or overwritten. Held means excluded from approved customer-facing components; a file committed to a public/static repository is not thereby private. Do not misrepresent a draft flag as access control or as publication permission.

## Specific approvals and remaining evidence

### Photographs

The catalogue is a visible-style/name/grouping reference, explicitly not proof of manufacture, price, composition, stock or publication rights. The corrective task authorizes technical implementation and directs that records without genuine permission remain held with an exact blocker. Do not invent creator information or approval evidence. Previously approved media keep their permission, but a related design or new upload does not inherit it automatically.

Sovereign: Black, Navy Blue, Burgundy and Olive variants; compare the two Olive files by actual bytes/content before duplicate/view assignment. The Burgundy additional view must join its real identified reference, not an invented missing photograph. Admiral: Pink, Crimson Red and Burgundy retain distinct exact photographs/descriptions. Ivory Heritage: angled, front and close-up views belong to one verified design. Pearl Gold Executive gets an individual visual review; uncertain exact details remain explicitly held. Other records stay separate unless actual review proves another relationship.

### Videos

Inspect both named MP4s directly for duration, dimensions, codecs, audio, actual clothing content, file size, playback suitability and poster relation. File names alone do not establish their audience, authorship or rights. Register facts through the existing workflow. Required rights/metadata/publication approvals remain a gate to activating either video on public pages. The approved image fallbacks and the tailoring-first headline/Send Your Design on WhatsApp action remain.

### PDF

The owner has already approved `Mr_Sewing_Fashion_Terms_and_Conditions_v1_Approved.pdf` content. Do not request that approval again or falsely claim the document is absent. Preparation date is 19 November 2026; it is not company registration. Intended effective date is the actual official publication date, not a guessed implementation or staging-preview date. Do not assert completed legal review. Actual content/metadata/technical checks and operational reconciliation must be recorded honestly through the existing registry/tooling.

If an actual contradiction, unresolved date or technical requirement blocks authoritative activation, complete safe source registration/preparation, identify the precise issue and preserve working Terms access. Do not mark reconciliation approved merely to make a test pass, rewrite agreed legal clauses by inference or bypass general publication controls.

## Visible-action contracts

| Action | Existing destination/behavior | Context and failure safeguards |
| --- | --- | --- |
| Showroom reference card | Existing design/detail route | Friendly verified name, exact photo/design identity, no fabricated stock/product; held records cannot leak through raw flags. |
| Family colour/view selector | Existing family/detail components | Select the actual reference photograph/variant; preserve IDs and selection context. No automatic inventory or fabric-availability claim. |
| Select design / review selections | Existing Selected Designs → fabric → quotation routes | Every original photo/quantity survives; no separate family cart/form. |
| Send design on WhatsApp | Existing official configuration and Terms consent | Prepared relevant exact reference/name; customer manually sends/attaches. Do not claim message delivery or order acceptance. |
| Homepage media card | Current Showroom/tailoring destination | Validated eligible asset/poster or approved fallback, touch/keyboard usable, native muted controls/reduced-motion behavior where appropriate. |
| Terms reader/open/download | Stable `/terms-and-conditions/` and approved version path | Scroll/read/zoom where supported, separate open/download/fallback, keyboard/focus and legacy anchors. Specific activation blockers preserve usable existing Terms. |

## Required validation and release evidence

Run the owner's actual commands after implementation:

```sh
python scripts/build_site.py
python scripts/build_site.py --check
python tests/media_showroom.py
python tests/policy_documents.py
python tests/seo_preservation.py
python tests/sitemap_discovery.py
```

Add meaningful family/view/colour, held-asset, exact photograph/quantity/WhatsApp/quotation, document/date/reconciliation and mobile/desktop checks as needed. Use synthetic/mocked customer interactions; no real messages, calls, quotations or payments. Record PASS, FAIL or NOT TESTED and distinguish unit fixtures from actual asset behavior.

Audit before/after titles/descriptions/headings/canonicals/alt/internal links/JSON-LD/sitemap/robots for affected pages. Keep staging noindex, public production canonicals and intentional noindex forms. No ranking/indexing guarantee. Previously approved page content is not blanket permission for new media.

A read-only main check observed `ff1248ce8d558b63a0de814133c4290b2224976b`, independent of this staging work. Do not edit, reset, merge or deploy main. Recheck staging and main before a normal authorized staging-only push; preserve unrelated external changes and branch protection. Provider deployment success is separate from actual rendered staging access, which may be proxy-limited.

The completion report must supply exact changed files, branch/SHA, registered image design/variant counts, all visible versus held items with reasons, each video's active/held reason, PDF viewer or specific activation blocker, actual build/test results and genuine staging preview/provider status. Do not stop at saving another draft report; continue all safe implementation first.
