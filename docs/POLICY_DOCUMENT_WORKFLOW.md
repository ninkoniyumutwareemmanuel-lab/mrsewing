# Policy document workflow — recovered 25 November 2026

Work in `phase1/customer-journey-repairs` and the `mrsewing-staging` project only. Changing a PDF on staging is not authorization to activate its contractual effect on the official website. Preserve confirmed customer agreements and the separate currently effective consent destination.

## Actual current files

| Purpose | Authoritative path |
| --- | --- |
| Version/approval/review registry | `_data/policy-documents.json` |
| Latest original upload, misleading historical filename | `Mr_Sewing_Fashion_Terms_and_Conditions_v1.1_Uploaded.pdf` — contents actually declare Version 1.2 |
| Immutable original Version 1.0 | `Mr_Sewing_Fashion_Terms_and_Conditions_v1_Approved.pdf` |
| Internal versioned PDF copies | `.github/policy-documents/terms-and-conditions/1.0.pdf`, `.github/policy-documents/terms-and-conditions/1.2.pdf` |
| Public direct/open/download PDF copies | `assets/policy-documents/terms-and-conditions/1.0.pdf`, `assets/policy-documents/terms-and-conditions/1.2.pdf` |
| Reader source | `scripts/terms_reader.py` |
| Genuine PDF page renderer | `scripts/render_terms_page_images.py` |
| Historical import command, now inspection/check only | `scripts/import_owner_terms_v1_1.py` |
| Reader presentation/controller source | `_templates/terms-reader.css`, `_templates/terms-reader.js` |
| Current and historical PDF-derived images/manifests | `assets/policy-documents/terms-and-conditions/pages/` |
| Image inventory | `_data/collection-image-inventory.json` |
| Generated reader route | `/terms-and-conditions/` from `scripts/customer_site.py` through `scripts/build_customer_release.py` |
| Preserved current contractual consent route | `/terms-and-conditions/current/` |
| Recovery verification | `tests/terms_recovery.py`, `tests/terms_reader_main_base.py`, `tests/terms_popup_browser.cjs` |

The current reader shows the actual latest uploaded **Version 1.2 for staging review**. Its download name identifies Version 1.2 and Staging Review. The original upload filename is preserved for traceability. Do not relabel this PDF as verified approved Version 1.1.

The owner confirmed on 25 November that newer uploaded files should be used for staging. The registry records that review-display authorization as `approved-for-staging-review`. It does not claim that the inaccessible 14-section approved Version 1.1 was independently matched, that a legal review occurred, or that official activation occurred. Both `currentVersion` and the staged document's `effectiveDate` remain `null`.

## Inspect a replacement before changing the reader

1. Preserve the old original and committed versioned copies. Record the current staging commit and take a recoverable backup before editing.
2. Read the complete actual PDF with `pdftotext`; inspect PDF metadata with `pdfinfo` and render representative pages. Check every numbered section, page count, visible version, active content, readability and actual commercial terms. A filename or equal page count does not establish identity.
3. Compare the complete text to the actual owner-approved source. Record both byte SHA-256 and normalized-complete-text SHA-256. Document formatting-only differences separately from substantive differences. Do not replace a failed expected hash with the upload's hash and call it an approved match.
4. Record precise approval scope: approved contractual contents, authorized staging review, or still unapproved. A newer upload can be approved for review without becoming the effective contract.
5. Reconcile payment, exceptions, refunds, surcharges and other operational facts with their current approved structured sources. Resolve substantive conflicts before contractual activation; preserve the explicit service rules and confirmed customer agreements meanwhile.
6. Only with applicable authorization, add a new receipt to `_data/policy-documents.json`, give it its **actual** version, preserve its original upload path, and create immutable version-specific internal/public PDF copies. Never overwrite an old version's bytes. Do not invent a registration or effective date.
7. Extend receipt validation deliberately for a newly authorized version; it must not accept arbitrary uploads or infer approval from a filename. `scripts/terms_reader.py` validates every retained receipt, exact original/internal/public hashes, staging publication state and page count.
8. Run `python scripts/render_terms_page_images.py`. It rasterizes the registered PDF with Poppler; image files are not simulated or independently edited. Keep the prior version images and `manifest-<version>.json`. The shared `manifest.json` identifies the current review document. Add newly generated page images to `_data/collection-image-inventory.json` as document assets, not garment designs.
9. Rebuild generated pages using the normal site builder. Do not hand-edit generated reader HTML or copy guessed screenshots into the page directory.

This static repository has no browser-based document upload or approval system. Upload/replacement occurs through reviewed repository changes, using the actual approved document and registry. No CMS, paid service or new upload backend is introduced.

## Checks before staging push

```sh
python scripts/import_owner_terms_v1_1.py --inspect
python scripts/import_owner_terms_v1_1.py --check
python scripts/render_terms_page_images.py --check
python tests/terms_recovery.py
python scripts/build_site.py
python scripts/build_site.py --check
python tests/terms_reader_main_base.py
python tests/seo_preservation.py
python tests/sitemap_discovery.py
node tests/terms_popup_browser.cjs
```

The historical importer without flags deliberately exits `BLOCKED`: the upload is Version 1.2 with 20 sections, not the requested Version 1.1 with 14. `--inspect` reports the discrepancy; `--check` verifies the deliberately registered actual staging-review receipt without claiming a Version 1.1 match. Routine builds must not run an unconditional contractual-document import.

Browser checks must verify scroll to the final page, zoom, close/back navigation, mobile dimensions, keyboard use and direct/download PDF bytes. The generated reader validates every image's path, order, PNG dimensions and SHA-256 against the manifest before rendering. The Open and Download controls point to the same byte-identical public PDF.

## Official activation is separate

Review display on staging does not replace the currently effective consent conditions. Keep `/terms-and-conditions/current/` and existing clause anchors usable. Do not silently move transactional consent to the review document. The recovery register documents the unavailable approved Version 1.1 comparison and Version 1.2 operational reconciliation.

An official activation requires separate owner authorization, the correct approved contractual contents, reconciliation of operational sources and the actual official publication event/date. No production action is authorized by this workflow or the present recovery task. Historical versions and existing confirmed customer agreements remain recoverable.
