# R54 — Terms PDF-only reader from latest main copy
Date: 21 November 2026 | Staging-only owner instruction

## Implementation brief
Scope is only /terms-and-conditions/ and the required current-effective-Terms access.
Foundation: main f07e3b3839b0faf133af77f3aca62779b3369be5.
Prior staging 7f2bda869fab476775206049adf22535354ced54 was independently saved at backup/staging-before-terms-2026-11-21. No main changes authorized.

## Terms rendering and current contractual access
The stable /terms-and-conditions/ page shows the real 5-page R53 PDF in a near-full-size native reader with Open PDF and Download PDF buttons. No repeated HTML terms, service cards or multi-section introduction are placed below it.
Original PDF bytes remain at their root upload path. Both immutable R53 source and generated public asset use exactly that Git object. Approval status remains content-approved staging-review, currentVersion null, effectiveDate null.
The current main-branch HTML Terms have been retained as a static, noindex historical/current transition route /terms-and-conditions/current/ for consent and direct reference. The Terms page links to it prominently. The existing shared quick-link for consent opens this current effective copy, and old deep-fragment links are routed to the existing content rather than pretending to match PDF page numbers.

## Unresolved activation
The owner did not activate the PDF as the officially effective site policy. R53 sourceFingerprint checks correspond to old R53 staging metadata; several current main-sourced JSON files differ. The prior R53 review is retained for history, but a fresh technical review against main and explicit owner-authorized official publication event are required before activation. PDF section 5 standalone payment default and section 7 contractual surcharge presentation must be reconciled without rewriting approved document content. This commit does not claim legal review.

## Safety, testing and deployment
No production/main publication or Cloudflare settings modifications are authorized.
Source builder changes are limited to rendering the Terms page and producing its CSS/JS assets. Existing quotation/consent routes, policies and all other pages are retained from main. A full Python/site/browser build is still required in an environment with a checked-out repository; this GitHub connector session cannot execute the repository's test suite. Do not mark those tests PASS until run.
