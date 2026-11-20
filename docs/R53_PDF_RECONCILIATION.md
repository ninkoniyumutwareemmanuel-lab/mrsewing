# R53 actual approved PDF — technical reconciliation

19November2026, staging only. Source upload `ce98ee3991a43483357304b5fe9f2f0a83f7ae27`; original `Mr_Sewing_Fashion_Terms_and_Conditions_v1_Approved.pdf`. The owner's corrective instruction explicitly confirms its content approval. No second request for that approval is needed or made. The file and its approved wording are unchanged.

## Actual inspection

- SHA256 `9b35d9384cf4d06dec88e92cfcde4c30d687ea1b126b6e0a8164784f5ee057c0`;87,547bytes;5pages;PDF1.7;Letter612×792points.
- `pdfinfo`: not encrypted; no JavaScript; no forms; tagged text metadata present. `pdftotext -layout` successfully extracts all pages; first page rendered and visually inspected. A PDF parser/tagging flag is not a legal review or accessibility certification.
- Actual title: Customer Terms & Conditions; Mr Sewing Fashion operated by NINKONIYUMUTWARE NEXUS LTD, Kigali, Rwanda.
- Actual document version1.0; prepared19November2026. The document explicitly says it becomes effective on publication on the official Mr Sewing Fashion website and that preparation is not company registration. No company registration date appears or is invented in the registry.
- Section14 has a heading without a following body paragraph; version/preparation/effectivity text is already explicit on page1. The approved PDF was not rewritten to add inferred content.

## Comparison with the nine current authoritative inputs

| Source | Actual comparison and scope |
| --- | --- |
| `_data/customer-policy-facts.json` | Domestic custom70/30, international100%, Express35%, after-hours25%, additive60%, individual overnight review and correction/complaint principles match. PDF§5 additionally sets the approved future standard standalone default70/30 unless a different approved quotation arrangement is confirmed; current facts leave standalone percentages unspecified and use each accepted quotation. That source transition must occur at official activation. The official production-start notice remains useful additional operational detail; no enquiry/automatic start is promised by the PDF. |
| `_data/customer-information.json` | Same legal operator and quotation/order distinction; contact instructions remain verified-source links. No PDF claim requires new location, fabric composition or stock data. |
| `_data/customer-faqs.json` | Questions/anchors remain, but payment explanations must be reconciled with the new standalone default at activation. Approved PDF§10 supplies a pre-production refund baseline less genuine documented nonrecoverable disclosed lawful costs, rather than an automatic forfeiture; existing human assessment and mandatory rights remain. Explanatory records must cite this approved document when effective. |
| `_data/customer-release.json` | Current HTML Terms/Refund/Privacy and service pages are preserved during the transition. Future effective PDF replaces the full HTML Terms rendering; current individual-assessment/standalone payment descriptions need scoped reconciliation before that activation. |
| `_data/business.json` | Brand identity matches. PDF uses the official website's verified contacts rather than introducing a new telephone/email/address or registration date. |
| `_data/business-hours.json` | PDF complaint acknowledgement24support working hours matches scoped support guidance; it does not introduce a new operating schedule or guarantee every service's response time. |
| `_data/suit-package-prices.json` | PDF does not replace ordinary tier prices or benefits; accepted quotations/conditions remain. No internal selling amount, gift or cleaning entitlement is changed. |
| `_data/tuxedo-package-prices.json` | PDF does not replace the separate tuxedo schedule/accessory eligibility; no extra ordinary-suit entitlement is inferred. |
| `_data/public-content-policy.json` | Current R51 service presentation hides public cost-surcharge rates. Approved PDF§7 explicitly discloses35/25/60; the internal rates agree. Official activation needs an explicit contractual-document disclosure mapping, not deletion of the approved PDF numbers or a silent internal rate change. |

These comparisons are a technical consistency review of actual sources, not a completed legal opinion. New owner-approved PDF content is not called an unapproved proposal. Existing agreed quotations and mandatory rights remain independent of a future website version.

## Implementation completed

The `receive` command extends the existing version registry/tooling. The approved PDF is registered as received version1.0, source `.github/policy-documents/terms-and-conditions/1.0.pdf`, public review `/assets/policy-documents/terms-and-conditions/1.0.pdf`, with the root uploaded filename separately registered and all copies checksum-bound. The source has actual owner content-approval evidence and preparation metadata. No unregistered-PDF wildcard or general bypass was added.

`/terms-and-conditions/` now renders the actual owner-approved PDF in the existing responsive viewer with native scroll/zoom where supported, explicit Open PDF separately and Download PDF controls, and a clear effective-date-pending notice. The panel uses `data-policy-document-review="1.0"`; it does not claim to be the active authoritative `data-policy-document-current` version. The existing readable HTML Terms and section anchors remain below it. A separate Current Online Terms heading clearly distinguishes the retained current HTML conditions. Consent links remain unchanged.

`currentVersion` stays null and `effectiveDate` stays null. The blocker is the actual official website publication event/date and coordinated operational activation of the approved document's standalone-payment/default and disclosure rules. Staging publication is not invented as official production publication. No production release is authorized here.

## Later official activation is implemented, not performed

`prepare-activation` preserves the received content approval and prepares a pending record for a verified official publication event/date and current operational reconciliation. `activate` dry-runs by default; `--write` makes an atomic registry-only transition after validation. It reuses the same approved version1.0 and exact PDF bytes/paths, moves the original receipt metadata unchanged into `receiptHistory`, preserves earlier versions and rejects missing event evidence, a future date, mismatched checksum or stale rule review. No new PDF version or effective date is invented. Failure rolls back the registry and leaves every PDF intact. Existing normal replacement publication continues to work after activation.

The actual document remains in review state; only temporary synthetic fixtures exercised activation.

## Verification performed

PASS: actual PDF integrity/metadata/text extraction/first-page rendering; receipt dry run; immutable local receipt; registry check; `python tests/policy_documents.py` including all prior normal publication/history/rollback/fingerprint/path/stray guards and new received-approval/date/current-pointer/tamper gates, same-version activation, missing/future publication-event rejection, fresh-review enforcement, atomic activation failure recovery and subsequent normal replacement history. Every test mutation uses temporary fixtures. No production, real enquiry, document rewrite, fabricated signature, registration date or legal-review completion. Full build/browser/deployed checks are coordinated by the parent executor and must be reported separately.
