# Terms document recovery — 25 November 2026

## Scope and decision

Inspected the complete current upload, both versioned Version 1.0 copies, original Version 1.0 upload, five prior derived page images/manifest, registry, reader/controller/CSS, attempted import, workflow references, relevant Git upload history and owner approval/recovery instructions. Searched the accessible workspace PDF inventory. The ChatGPT Library approved Version 1.1 is unavailable; the library-files directory contains no document. No claim of full Library comparison or legal review is made.

The latest original upload **actually declares Version 1.2**, both in its metadata and each page footer. Its 6 pages contain **20 numbered sections**, not the owner's described 14-section Version 1.1. Full text was extracted and read, and page 1 was rasterized and visually inspected. The owner subsequently directed use of the newer uploaded files for staging. Therefore the actual Version 1.2 is integrated for **staging review under its real identity**, while Version 1.0 archives and current contractual consent remain intact. This review authorization does not retroactively establish a match to the missing approved Version 1.1.

## Exact sources and checksums

| Record | Result |
| --- | --- |
| Initial staging commit | `0acf34dc9c606c0fe283d48177c39ebc7a92b20f` |
| Upload commit | `bc3c62cc9987775e22238e0ff7d63930177bea45` replaced the old Version 1.0 root filename with newer bytes |
| Recovery commit | `a039e70aefb9d3d88642a19031f4940767dc27e4` restored the immutable Version 1.0 and preserved the new upload under the v1.1-named path |
| Attempted automated verification | `0acf34dc` added an unconditional importer expecting a text fingerprint different from the actual upload |
| Latest upload path | `Mr_Sewing_Fashion_Terms_and_Conditions_v1.1_Uploaded.pdf` — historical filename retained |
| Actual latest PDF bytes | 1,264,717; PDF 1.4; 6 A4 pages; unencrypted; no JavaScript or form; selectable text; not tagged |
| Actual latest byte SHA-256 | `d12476d31e6ac6d2943a6f18c2577774b5905f985ca9d8d5521624a5f4a77cb0` |
| Actual latest normalized full-text SHA-256 | `5c7123f88ea7971cb38c9d5dea052167041d50ba42763316b14af59ba57b7d45` |
| Historical attempted expected text SHA-256 | `4ba45807fd3568002c116a5df1ab9677e13adb044b8b5888426d610a0fd1eb1c` — no independently accessible approved source supporting it |
| Version 1.0 byte SHA-256 | `9b35d9384cf4d06dec88e92cfcde4c30d687ea1b126b6e0a8164784f5ee057c0`; 87,547 bytes; 5 pages; all three original/internal/public copies unchanged |
| Version 1.0 normalized full-text SHA-256 | `b3d997deeee3c6ad31947382556db3461de8b9163a16c8c70ca1d7cc36fb618d` |

The differing full-text hash is not merely PDF metadata or a different filename. Version 1.2 restructures and rewrites the document. Equal page counts cannot establish equivalence.

## All original 14 sections reviewed against the newer upload

This maps the **available Version 1.0** and actual latest Version 1.2. It is not an invented comparison against the unavailable Version 1.1.

| Original Version 1.0 section | Corresponding actual Version 1.2 content |
| --- | --- |
| 1. About these terms | 1. Company identity and scope; 2. Agreement and related policies |
| 2. Our services and enquiries | 3. Services and availability; 4. Enquiries, quotations and acceptance |
| 3. Quotations and order acceptance | 4. Enquiries, quotations and acceptance; 5. Pricing, benefits and promotions |
| 4. Fabric, designs and measurements | 9. Custom tailoring, fabric and design; 10. Measurements, fittings and fit |
| 5. Payments and order release | 6. Payments and exceptional arrangements; 7. Individually approved payment exceptions |
| 6. Production, fittings and changes | 8. Production stages and scheduling; 15. Order changes, suspension and cancellation |
| 7. Express and outside-hours services | 12. Express, outside-hours and mobile services |
| 8. Mobile assistance, collection and delivery | 12. Mobile services; 14. Collection, delivery and international orders |
| 9. Alterations, garment care and Shop purchases | 11. Alterations, repairs and garment care; 13. Shop, showroom and product orders |
| 10. Cancellations and refunds | 15. Order changes, suspension and cancellation; 16. Refunds, returns and exchanges |
| 11. Quality concerns and corrections | 17. Quality, corrections, damage and loss |
| 12. Customer information and photographs | 19. Customer information, photographs and communication |
| 13. Communication, disputes and changes | 18. Customer and company responsibilities; 20. Complaints, applicable law and updates |
| 14. Document version and effective date | Version 1.2 footers and section 20 official-publication condition |

The actual Version 1.2 does not explicitly repeat the fixed 70%/30% figures, 35%/25%/60% surcharges or a three-calendar-day exception settlement rule. Its payment/exceptions clauses defer detailed eligibility and amounts to disclosed quotations/FAQ. It preserves generalized verification, suspension without automatic forfeiture, individual cancellation/refund assessment and mandatory-rights language. These are substantive drafting differences. The explicit current owner-approved service policies are not silently superseded by this review copy. Operational/legal reconciliation remains necessary before official activation.

## Implemented technical repair

- Preserved all original uploaded bytes and Version 1.0 copies, five page images and historical receipt.
- Added the actual Version 1.2 review receipt with `approvalStatus: approved-for-staging-review`, actual source/hash, 20 sections, six pages and explicit unavailable Version 1.1 comparison. No fake approved-v1.1 record or effective date was added.
- Created exact byte-identical `.github/policy-documents/terms-and-conditions/1.2.pdf` and `assets/policy-documents/terms-and-conditions/1.2.pdf`.
- Generated six real PDF-derived PNG pages at 1360px width using Poppler. Added document-only image inventory records, the current shared manifest and `manifest-1.2.json`; preserved `manifest-1.0.json` and its original page hashes. The rendering metadata records a width target rather than claiming an inaccurate DPI for the A4 upload.
- Updated the same existing full-screen reader, scroll, zoom, close/back and direct-PDF fallback. Visible download filename identifies Version 1.2 Staging Review; original upload name remains traceable in the registry.
- Strengthened reader validation: retained receipts all have original/internal/public hashes checked; current manifest version/state/source hash, page order/path, PNG dimensions and per-image hashes are validated before rendering. A later receipt cannot hide a corrupt older archive.
- Converted the historical v1.1 import command to explicit read-only `--inspect`/`--check`. Its default fails with the precise version/section discrepancy and performs no writes. No unsupported hash is changed merely to make a build pass.
- Preserved `currentVersion: null`, staged `effectiveDate: null`, the separate current Terms route, legacy clause behavior and existing consent. No Main or official activation occurred.

## Tests actually run by document recovery

| Check | Result |
| --- | --- |
| Complete `pdftotext` extraction/read, `pdfinfo`, byte/text checksums and original section mapping | PASS; actual Version 1.2 identity established, approved Version 1.1 comparison unavailable |
| `python scripts/import_owner_terms_v1_1.py --inspect` | PASS; truthful full identity report |
| `python scripts/import_owner_terms_v1_1.py --check` | PASS; actual registered Version 1.2 review document, not an approved-v1.1 claim |
| Import command without flags | Correctly BLOCKED with no registry mutation; tested using temporary/synthetic comparison checks |
| `python scripts/render_terms_page_images.py` and `--check` | PASS; six genuine current PDF-derived pages |
| `python tests/terms_recovery.py` | PASS: 4 tests covering identity, no mutation, identical PDFs, current/archived hashes, image tamper and duplicate-page rejection |
| Python compile and `git diff --check` | PASS at recovery handoff |
| `tests/terms_reader_main_base.py`, browser scroll/zoom/close/download tests and full site build | Delegated to parent after generated pages rebuild; report parent’s actual results separately |
| Actual deployed staging HTTP/browser | Not independently performed by this document subtask; no success claim |
| Legal review / Library content verification / production activation | NOT VERIFIED / NOT PERFORMED |

## Remaining decisions

The uploaded Version 1.2 may be reviewed on staging under the latest owner direction. Before treating it as the operative contractual document, verify the actual approved Version 1.1 source or obtain explicit contractual approval of this complete actual Version 1.2 text, reconcile the scoped operational rules and record the real official publication event under separate authorization. No need to re-upload existing repository files or reapprove the prior Version 1.0 content.

See `docs/POLICY_DOCUMENT_WORKFLOW.md` for the future replacement process. Raw extraction/audit evidence resides outside the published checkout at `/workspace/recovery/2026-11-25/terms/`.
