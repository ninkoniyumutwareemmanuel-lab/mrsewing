# Terms and Conditions document workflow

**R53 current state,19 November2026:** the owner supplied and explicitly approved `Mr_Sewing_Fashion_Terms_and_Conditions_v1_Approved.pdf` in upload commit `ce98ee3`. Its actual five-page content has been inspected and registered in `_data/policy-documents.json` → `receivedVersions`, with an immutable approved archive, public review copy and exact checksum. The Terms page embeds that real document and offers Open PDF separately / Download PDF. No content reapproval is requested.

`currentVersion` remains null because the PDF takes effect on publication on the official website, and this task authorizes staging only. Its preparation date is not its effective date or company registration date. The existing readable online Terms remain below a clearly marked review viewer until official activation and the operational source transition are reconciled. Approved document section5 establishes a future standalone-service default70%/30%, while current operational guidance defers standalone payments to each accepted quotation. Section7's approved contractual surcharge disclosure also needs a scoped mapping against the existing public service-rate presentation policy. See [actual reconciliation](R53_PDF_RECONCILIATION.md). These are activation requirements, not missing content approval. Other arbitrary PDFs remain rejected.

This is a repository workflow. There is no browser upload screen, CMS or automatic legal approval service. The owner replaces the document and approves its version; a developer records that approval and runs the existing build. Viewer code does not need to be rewritten for each replacement.

## Where information lives

| Purpose | Actual path |
| --- | --- |
| Document identity, current version, dates, approval, history | `_data/policy-documents.json` |
| Validation and viewer rendering | `scripts/policy_documents.py` |
| Prepare/review/publish commands | `scripts/publish_policy_document.py` |
| Approved asset generation and synchronization check | `scripts/build_policy_documents.py` |
| Viewer structure, styling and anchor handling | `_templates/policy-document.html`, `_templates/policy-document.css`, `_templates/policy-document.js` |
| Immutable approved source PDFs, after approval only | `.github/policy-documents/terms-and-conditions/{version}.pdf` |
| Version-specific public PDF, generated from approved source | `/assets/policy-documents/terms-and-conditions/{version}.pdf` |
| Stable public reading/download entry | `/terms-and-conditions/` |
| Temporary-fixture regression tests | `tests/policy_documents.py` |

The registry's `operationalSources` list identifies the current structured rules, explanatory FAQ/service data, business details and hours to review alongside the document. It stores checksums, not independent copies of those rules. Neither this public repository nor a hidden folder is confidential storage.

## Prepare a replacement

1. Prepare and review the document outside this checkout. A readable, selectable-text, accessible PDF is preferable to a scan. Check its company identity, version, effective date, headings/contents and approved terms. The website cannot certify legal accuracy or PDF accessibility.
2. Keep drafts and pending review records **outside the repository and deployed tree**, for example in `/tmp/mrsewing-terms/` while testing. `/tmp` is temporary: keep the owner's working originals securely elsewhere too. Do not commit unapproved PDFs, customer information or private company records.
3. Use the staging branch `phase1/customer-journey-repairs`. Generate a review template:

```bash
python scripts/publish_policy_document.py prepare \
  --pdf /tmp/mrsewing-terms/Terms-and-Conditions-v1.pdf \
  --version v1 \
  --effective-date 2026-12-01 \
  --review-out /tmp/mrsewing-terms/v1-review.json
```

These dates/names are **command examples**, not an approved company version or effective date. The template is marked `pending`; it cannot be published in that state. Its PDF checksum binds the review to the actual bytes, and source fingerprints identify the exact operational records being reviewed. The configured PDF size limit is20MiB.

## Record genuine approval and resolve conflicts

The owner and responsible reviewer must check the PDF against current facts and explanatory FAQs. Do not extract a paragraph automatically and assume it is approved policy. If a document introduces or changes a material rule, record the approved decision in the customer-information reference, reconcile the authoritative structured record and dependent FAQ/service content, then prepare/review the PDF against those final sources.

Only after actual approval, complete the external review JSON:

- `approvalStatus`: `approved`; `approvedBy`, `approvalDate` and `sourceReference`: the real approval evidence.
- `reconciliation.status`: `approved`; `reviewedBy`, `reviewedOn` and `reference`: the real review of contractual and operational consistency.
- Keep the exact `documentSha256` and `reconciliation.sourceFingerprints` that were reviewed. Do not replace checksums just to silence a failed check.
- Check `version`, `effectiveDate` and `lastUpdatedDate` against the approved document. Selection of the current published version is explicit; the website does not schedule legal changes automatically by date.

The software checks recorded metadata and integrity. It does **not** authenticate a human signature or decide legal approval itself. An arbitrary `approved` flag is not permission to publish.

Use concise, sanitised approval references suitable for a public repository. Keep private correspondence and the owner's review working files outside Git; do not paste confidential emails, customer records or internal financial information into the registry.

## Validate, publish locally and review staging

Run a dry run first:

```bash
python scripts/publish_policy_document.py publish \
  --pdf /tmp/mrsewing-terms/Terms-and-Conditions-v1.pdf \
  --review /tmp/mrsewing-terms/v1-review.json
```

The dry run validates without changing repository files. When the review is genuinely approved and the dry run passes, use the same command with `--write`:

```bash
python scripts/publish_policy_document.py publish \
  --pdf /tmp/mrsewing-terms/Terms-and-Conditions-v1.pdf \
  --review /tmp/mrsewing-terms/v1-review.json \
  --write
python scripts/build_site.py
python scripts/build_site.py --check
python scripts/publish_policy_document.py check
python tests/policy_documents.py
```

The command creates immutable approved source/public files, archives prior version metadata and changes the current pointer last. It refuses a reused version, changed reviewed bytes, pending approval, unresolved source fingerprints or unsafe paths. A failed write removes newly created files and preserves the previous registry pointer. It never commits, pushes or deploys.

Inspect the diff, test and deploy **staging only** through the existing project process. Check the actual PDF on phone and desktop: scrolling, document-reader zoom where available, direct open/download, text legibility, keyboard access and fallback links. Publication to production requires its own owner authorization. Do not treat a successful build as proof that a deployed reader or a particular mobile PDF application works.

## What customers see

With an approved current PDF, the Terms route displays its version and effective/updated dates, the embedded reader, **Open PDF separately** and **Download PDF**. Download/open links remain available even if the browser cannot render the embedded object. Native PDF controls and zoom depend on the browser or installed reader; there is no claim of identical controls on every device.

The full legacy website Terms body is then removed from that page's rendering, so it does not compete with the approved document. Its historical source remains in Git. Existing section URLs such as `#2`, `#5`, `#6`, `#7`, `#8` and `#mobile-fees` continue to reach the document and focus its heading. No PDF page numbers are invented for those anchors; customers can use the document's approved contents/search.

Until an approved PDF exists, the current online Terms remain the readable fallback. Keep all enquiry and WhatsApp Terms-consent links working. Do not replace them with an empty document notice.

## History, later changes and recovery

- Every replacement uses a new version and immutable filename. The registry retains previous version references and their approval/reconciliation records. Existing approved source and public version URLs remain recoverable for earlier agreed quotations; only the current version is linked prominently in the viewer.
- Archives in this public repository are version history, **not private storage**. Never store unapproved legal drafts or confidential documents there. Removing historical public files or routes is a separate migration decision, not part of ordinary replacement.
- The normal build rejects unregistered PDFs in the deployed source tree. This does not undo the privacy exposure of someone manually committing a draft to a public Git service: keep drafts outside Git from the start.
- A change to a fingerprinted operational source while a PDF is current blocks normal document generation until a human review is recorded for a new approved replacement. Fingerprinting is conservative: even an editorial change can require review. It does not automatically change FAQs, legal wording or the PDF.
- A new approved replacement can be prepared while the previous current PDF has stale operational fingerprints; the final replacement still has to match today's sources. Prior fingerprints remain historical.
- If publication or deployment fails, retain the prior approved version and compare the Git diff. Do not overwrite an old PDF or clear validation gates. Restore an already approved prior version only through a separately reviewed change to the current-version registry and normal staging tests.

## Current verification boundary

Temporary tests verify approval gates, checksum/path safety, stray-PDF rejection, current-reference replacement, historical files, conflict detection, write rollback and generated viewer/fallback links. The actual received owner-approved PDF is checked read-only; all test mutations use temporary synthetic fixtures. Content approval is already supplied. Legal review is not claimed, and device/native-reader or assistive-technology behavior requires actual testing rather than an integrity assertion.

## Accessibility and reviewed scope

Use a searchable, readable and appropriately accessible approved PDF. The publication helper checks integrity and recorded approval; it cannot certify legal sufficiency or PDF tagging. Review the actual document with assistive technology where appropriate. Separate open/download links remain available even when a browser cannot embed the file.

Operational reconciliation also covers the ordinary-suit benefit/pricing source, tuxedo schedule and public presentation policy. Changing benefits or service-price visibility must not leave an activated document silently out of sync. Source fingerprints prompt human review rather than extracting or guessing replacement policy wording.


## Register an approved upload for staging review without a false effective date

Use `receive` only when the owner has actually approved the supplied content and the original uploaded file already exists in the repository. It records that approval separately from official activation. Keep a byte-identical review copy and review JSON outside the repository; the original filename must match `originalUploadPath` in the root, and all three upload/archive/public checksums must agree. The command validates the full candidate registry, including stray-PDF protections, before writing immutable copies and updating the pointer metadata last.

The actual R53 commands were:

```sh
python scripts/publish_policy_document.py receive --pdf /workspace/review/r53-media-pdf-2026-11-19/Mr_Sewing_Fashion_Terms_and_Conditions_v1_Approved.pdf --review /workspace/review/r53-media-pdf-2026-11-19/approved-received-review.json
python scripts/publish_policy_document.py receive --pdf /workspace/review/r53-media-pdf-2026-11-19/Mr_Sewing_Fashion_Terms_and_Conditions_v1_Approved.pdf --review /workspace/review/r53-media-pdf-2026-11-19/approved-received-review.json --write
python scripts/publish_policy_document.py check
```

The received record uses `approvalStatus: approved`, `publicationStatus: staging-review`, `activationStatus: awaiting-official-publication`, `effectiveDate: null` and `effectiveDateBasis: official-website-publication`. It cannot be assigned as `currentVersion`; checks reject that attempted bypass. Owner approval evidence, preparation date, technical inspection and the explicit remaining activation requirements are recorded. Reviewed source fingerprints are snapshots, not independent policy values. A changed source while this is the active staging review requires a new technical comparison.

For later separately authorized official publication, activate this same approved version1.0 rather than overwriting its PDF or inventing a new document version. The new `prepare-activation` / `activate` workflow preserves the owner's existing content approval and reuses the exact immutable archive/public paths. It moves the original receipt metadata unchanged into `receiptHistory`, records the actual official publication event/date and fresh operational reconciliation, then atomically changes only the registry. A failed write leaves all prior metadata and PDFs intact.

```sh
python scripts/publish_policy_document.py prepare-activation --version 1.0 --official-publication-date YYYY-MM-DD --review-out /tmp/review/activation.json
python scripts/publish_policy_document.py activate --version 1.0 --review /tmp/review/activation.json
python scripts/publish_policy_document.py activate --version 1.0 --review /tmp/review/activation.json --write
```

`YYYY-MM-DD` is a placeholder for the actual separately authorized official publication date, not an assigned date. The pending template cannot activate anything: record `officialPublication.status: confirmed`, the real event evidence and date, and the completed operational reconciliation. A future planned date, missing evidence, stale source fingerprints or changed PDF checksum is rejected. No second content approval is requested. After activation the full HTML fallback is replaced by the authoritative PDF, with the received history retained; normal future `prepare` / `publish` replacements continue to work.

Do not change agreed historical quotations, set the preparation date as a company registration date, or infer completed legal review. This task did not run official activation or authorize production publication.
