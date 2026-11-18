# R49 — Approved customer-information reconciliation

Owner authority: **13 November 2026**, “FINAL CUSTOM TAILORING COMPLETION & PRODUCTION RELEASE”, Parts C–H. This authorizes these exact commercial/customer-information changes and the full approved release only after successful critical verification. Earlier staging-only statements and review labels do not require a second approval for these express decisions. Unresolved proposals and unapproved refund/liability clauses remain unpublished.

## Sources actually reviewed

- Root `AGENTS.md`, current reference pointer and the applicable `versions/2026-11-13-03` customer master, policy matrix, unresolved register and page-map R48 sections.
- `R49_RELEASE_BRIEF_2026-11-13.md` and the owner's full R49 instruction.
- Current `_data/customer-policy-facts.json`, `_data/customer-faqs.json`, `_data/customer-information.json`, `_data/customer-release.json`, legacy `_data/policy-pages.json` anchor records, and `scripts/customer_policies.py`, `scripts/customer_information.py`, `scripts/faq_help.py` rendering/search architecture.
- Existing browser-draft implementation shows a per-tab30-minute contact draft. Parent confirmed R49 Express recovery stores a separate24-hour order snapshot without contact fields, exact addresses or free-form additional information. This is a browser recovery feature, not server/email retention.

Named original operating handbooks remain unavailable. No inaccessible document is treated as inspected; this scoped update uses the latest explicit owner decisions and preserves earlier unsuperseded approvals.

## Latest approved changes

| Subject | Prior current source | R49 rule and implementation |
| --- | --- | --- |
| Independent Consultation & Fitting |25,000RWF | **35,000RWF**, effective13November2026, only for this independent service. Source fee integer, shared text, FAQ comparison question and workplace-measurement explanation updated. |
| Order-related measurement visit |10,000RWF | Unchanged for eligible Kigali visits after garment-quotation acceptance and required70% advance. No second independent-consultation fee for the same approved measurement service. Choosing a preferred appointment does not require payment. |
| Initial eligible Kigali suit delivery |Included package benefit | Preserved. No second charge. Address optional at enquiry, confirmed before dispatch. This does not promise free delivery for unrelated services or every Special garment. |
| Eligible Custom Tailoring delivery elsewhere in Rwanda |Individually agreed additional delivery | **5,000RWF per garment**, address required.1/2/3garments examples5,000/10,000/15,000. A calculation is not an accepted final quotation. No automatic extension to Alterations or Garment Care. |
| International delivery |Individual shipping quotation | Preserved; complete address required, no universal price/transit deadline. International payment rule remains separate. |
| Collection |Agreed collection arrangements | Preferred collection location instead of delivery address; readiness/location/full payment/release confirmed. |
| Locations |Existing workshop/MIC references | Main Workshop **KN441St, Norvège, Kigali**. Downtown **MICBuilding, by appointment**. No permanently staffed Downtown claim. |
| Production clock |Separate official start notice | Explicitly starts at the official production-start notice, not enquiry/provider acceptance/payment screenshot. Other prerequisite steps remain separate. |
| Ordinary-suit deadline screening |No automatic classification in prior form | `deadline − now −24hours`; at least7days planning → provisional Standard; less → Express. Not a confirmed schedule or automatic surcharge. Special Tailoring needs service-specific human assessment. |
| Customer delays |General reviewed changes | Reply/acceptance/measurement/requirements delays can change completion arrangements. Reassess Express feasibility/charges with agreement; no automatic fee. |
| Quotation targets |Distinct earlier first-response/order-confirmation targets | Express quotation target24hours; Standard24–48hours, subject to operating hours, sufficient information and assessment. Targets, not unconditional guarantees. Keep provider acceptance, first human reply, quotation delivery/acceptance, order confirmation and production start separate. |
| Express recovery privacy |Temporary per-tab selections/contact draft | Separate same-browser order-only snapshot with24-hour expiry checked on return. No contact fields, full addresses or free-form additional information in that snapshot. Existing per-tab30-minute contact draft remains described separately. No cross-device/deleted-browser-data recovery guarantee or unverified encryption/compliance claim. |

The earlier1–3week Standard and2–3day Express customer estimates remain approved estimates subject to capacity and the agreed completion date. The new screening threshold is **not** a seven-day delivery promise and does not start the production period at form submission.

## Direct FAQ contract — all16 required subjects

Each entry is a genuine native FAQ `<details>` answer with unique topic ownership, search-index inclusion and generated FAQ structured data. Existing question IDs/anchors are retained; new answers have their own stable IDs.

| Subject | Exact destination |
| --- | --- |
| Production commencement |`/faq/production-delivery/#production-start` |
| Standard Tailoring |`/faq/production-delivery/#standard-tailoring` |
| Express Tailoring |`/faq/express-tailoring/#express-request` |
| Urgent deadline assessment |`/faq/express-tailoring/#urgent-deadline-assessment` |
| Customer-caused delays |`/faq/production-delivery/#customer-delays` |
| Quotation targets |`/faq/production-delivery/#quotation-response-times` |
| Measurement appointments |`/faq/measurements-fittings/#measurement-appointments` |
| Independent consultation35,000 |`/faq/measurements-fittings/#independent-consultation-cost` |
| Order-related visit10,000 |`/faq/measurements-fittings/#order-measurement-visit` |
| Online measurements |`/faq/measurements-fittings/#online-measurements` |
| Main workshop/Downtown visits |`/faq/booking-visiting/#locations` |
| Included Kigali delivery |`/faq/production-delivery/#kigali-delivery` |
| Outside-Kigali delivery |`/faq/production-delivery/#outside-kigali` |
| International shipping |`/faq/production-delivery/#international-shipping` |
| Customer collection |`/faq/production-delivery/#customer-collection` |
| Submission vs confirmation |`/faq/production-delivery/#submission-confirmation` |

Terms preserve existing section anchors: `#2` enquiry/acceptance, `#5` measurements/appointments, `#6` timing/screening/delays, `#7` production/response, `#8` delivery/collection and `#mobile-fees` service-fee distinction. The source search index already links these exact sections. No duplicate policy page was created.

Existing mobile-fee, workplace-measurement, measurement-options, delivery-arrangements and deadline-rejection answers were reconciled using the same shared facts. Their anchors remain valid. The Terms, customer guidance, delivery page, privacy notice and Contact location paragraph use the updated source facts.

## Exact source files changed by this subtask

- `_data/customer-policy-facts.json`
- `_data/customer-faqs.json`
- `_data/customer-information.json`
- `_data/customer-release.json`
- `scripts/customer_policies.py`
- This reconciliation document.

The parent owns the new dated reference snapshot/manifest/changelog, form integration, tests, generated pages and any release. No generated file, main branch, production setting or deployment was changed by this subtask.

## Checks completed

- JSON parsing and Python syntax pass.
- FAQ catalogue checks pass:16required IDs, unique question owners, nonempty expanded answers and search entries.
- All policy placeholders expand without unresolved tokens.
- Current source scan for25,000/25000 leaves only the legitimate25% surcharge calculation example,250,000suit values and an explicitly dated supersession record. No active independent-consultation25,000 claim remains in source data/templates/scripts.
- Existing exact numeric Terms anchors are retained; native FAQ rendering and schema are reused.
- No refund, cancellation, legal entitlement, VIP price, new stock guarantee, payment gateway or unrelated-service delivery rate was invented. Existing10,000alteration/garment-care round-trip transport and50,000independent assistance limits are preserved.

Full build, rendered-page anchors/search/schema, customer-form links, responsive layout, provider mocks and production gates remain the parent's integrated verification responsibility.

Final source QA also corrected the existing start-order FAQ and Custom Tailoring service introduction: they now ask for a requested deadline with provisional ordinary-suit screening, instead of instructing customers to manually select Standard/Express. Special Tailoring remains subject to human assessment. No unrelated service priority selector wording was changed.
