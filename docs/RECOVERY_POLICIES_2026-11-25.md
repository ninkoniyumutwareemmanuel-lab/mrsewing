# Policy and quotation-first recovery — 25 November 2026

Implementation checkout: `phase1/customer-journey-repairs`; inspected remote baseline `0acf34dc9c606c0fe283d48177c39ebc7a92b20f`. This report records source-level and targeted-test results. It does not certify a deployed website, legal compliance, official Terms activation, customer receipt or production publication.

## Approval and sources examined

- Owner's25November2026 Master Website Recovery instruction: ordinary domestic70/30; Express35%; individually approved eligible Standard lower advance; full outstanding payment within three calendar days; verified receipt; notified suspension and human cancellation/refund assessment; no automatic ten-day cancellation/forfeiture.
- `docs/POLICY_V1_1_OWNER_APPROVAL_2026-11-25.md` and commit55cef7cc: scoped owner-approved v1.1 policy implementation. Most requested rules were already present in the current facts, FAQ and refund source before this repair.
- Current reference pointer `versions/2026-11-22-01/`: master, source matrix, unresolved register and page map. Historical references are preserved and do not supersede the newer explicit decisions.
- `docs/R67_TAILORING_HUB_CUSTOMER_GUIDE_2026-11-23.md`: presentation approval includes Express+35%, agreed after-hours+25% and additive+60%; no blanket surcharge suppression is appropriate.
- Historical approved R51 quotation-first instruction and `749b21d:_data/public-content-policy.json` / `scripts/public_content.py`: public service tariff removal was lost when later staging work rebased on Main. Shop pricing, internal approved prices, agreed quotations, payment obligations and benefit eligibility are exceptions to hiding public service tariffs.
- Current `_data/customer-policy-facts.json`, `_data/customer-information.json`, `_data/customer-release.json`, `_data/customer-faqs.json`, `_data/policy-pages.json`; current builders, hub, FAQ search/schema and form notices.
- Actual root PDF extraction was shared with the separate Terms audit: the file named v1.1 contains a v1.2 document. No business rule was inferred from that filename or its generalized clauses, and no official activation occurred in this work.

## Findings and source repairs

1. Existing v1.1 rules are preserved. Shared fact strings now supply the flexible-advance, Express-advance, overdue-payment and cancellation/refund explanations in FAQs and refund pages instead of separately editable copies. The active tailoring hub reads its existing flexible/Express/overdue paragraphs from the same facts. This changes maintenance ownership, not the approved customer wording.
2. Added `latestPolicyApproval` metadata scoped to25November2026 without overwriting the original7Novemberapproval/history or claiming completed legal review.
3. Restored `_data/public-content-policy.json` and `scripts/public_content.py` as a presentation-only adapter. Public information requests a quotation instead of displaying ordinary suit/tuxedo starting schedules or fixed service tariffs. The adapter does not mutate internal records or calculated customer-specific quotation charges.
4. Preserved explicit surcharge disclosure35/25/additive60, normal70/30, international100%, family/bulk conditions and service-specific scope. Hypothetical surcharge examples are not passed off as actual service tariffs.
5. Customer-information expansion, FAQ answers/search/structured data and service-policy sections share the projection. Former numeric tuxedo/measurement/transport FAQ duplicates now provide quotation guidance. Internal suit/tuxedo prices, Shop product records and fee inputs remain unchanged.
6. Garment Care pricing-table and fixed additional-charge output honour the same presentation setting. Assessment, timing, eligibility and quotation requirements remain available. No other service journey or payment provider changes were made.
7. Ordinary suit-price FAQ links now lead to the existing tier/benefit FAQ rather than a missing numeric table on the newer hub. Existing FAQ IDs, search interface and question navigation remain.

## Scope and preserved conditions

The lower-advance exception remains individually approved, limited to eligible domestic Standard custom tailoring, and unavailable for Express. Full outstanding settlement is due within three calendar days even if the garment is unfinished. A missed deadline leads to notified suspension, not automatic cancellation or forfeiture. Actual receipt is verified; screenshots/pending transactions and provider acknowledgements are not production-start notices. Resumption, completion reassessment, cancellation and refund remain human decisions under accepted terms and mandatory rights.

The `payments.standaloneAdvancePercent:null` machine field is preserved: it is not an instruction to activate a universal automatic standalone-service payment engine. Accepted quotation/service conditions still govern. This recovery does not apply custom tailoring's completion/final-cleaning sequence indiscriminately to other services.

Public tariff removal does not erase internal approved fees or required customer-specific charges from an actual quotation/review. The existing validated outside-Kigali delivery calculation, internal35,000RWF independent consultation/10,000RWF eligible order-related visit and existing receiving pipeline were not changed.

## Tests actually run

- **PASS** `python tests/recovery_policies.py`: exact70/30/100 and35/25/60; Standard exception/three-day/suspension/no-forfeiture; quotation-first projections do not mutate facts; all projected operational qualifications remain; shared FAQ expansion/search; internal ordinary/tuxedo schedules, Shop catalogue and available server fee inputs match baseline.
- **PASS** Python compilation of changed source modules.
- Full build, deployed HTTP/browser, legal review and official contractual activation are **NOT TESTED by this scoped agent**. Parent recovery report must supply its actual integrated build/browser/deployment evidence separately.

## Changed files

- `_data/public-content-policy.json`
- `scripts/public_content.py`
- `_data/customer-policy-facts.json`
- `_data/customer-faqs.json`
- `_data/customer-release.json`
- `scripts/customer_policies.py`
- `scripts/customer_information.py`
- `scripts/tailoring_services_hub.py`
- `scripts/build_journey.py`
- `tests/recovery_policies.py`

## Remaining review items

The actual uploaded PDF's version/content identity is handled by the separate Terms recovery report. It must not silently supersede the preserved operational rules or contractual consent. No new commercial decision was invented. The permanent staging address and actual displayed content still require independent final deployment verification.
