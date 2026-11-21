# R54 — Terms source map (21 November 2026)
Owner scope: Terms and Conditions page only, on a copy of main f07e3b3839b0faf133af77f3aca62779b3369be5. Do not assume the R53 full website source map describes the main-derived foundation.

| Purpose | Authoritative file / route |
|---|---|
| Customer Terms HTML source | _data/customer-release.json → pages['/terms-and-conditions/'] |
| Customer Terms HTML renderer | scripts/customer_site.py → information(), original content |
| Pending approved PDF/version status | _data/policy-documents.json → receivedVersions; currentVersion:null |
| Approved original PDF | Mr_Sewing_Fashion_Terms_and_Conditions_v1_Approved.pdf |
| Archived copy and review public PDF | .github/policy-documents/terms-and-conditions/1.0.pdf; assets/policy-documents/terms-and-conditions/1.0.pdf |
| New PDF reader | scripts/terms_reader.py; _templates/terms-reader.css / .js |
| Reader outputs | terms-and-conditions.html; terms-and-conditions/index.html; assets/terms-reader.css / .js |
| Current HTML Terms fallback | terms-and-conditions/current/index.html, noindex |
| Consent link | scripts/customer_site.py; _templates/customer-interactions.js |
| Testing | tests/terms_reader_main_base.py and existing site regression suite |
| R53 historical technical comparison | docs/R53_PDF_RECONCILIATION.md on protected old staging branch |

The PDF content is owner-approved but not officially effective. R53 fingerprints have not been re-reviewed for newer main policy source changes. Do not activate or assert legal review. Maintain the fallback until actual official activation.
