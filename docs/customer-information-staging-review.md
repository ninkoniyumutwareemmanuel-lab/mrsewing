# Hero and customer-information staging review

Historical audit baseline: `ac639f145fc976ecefe02e2b8ff5b82f1aae184b`.
Branch: `phase1/customer-journey-repairs`. This phase continues that clean tree;
no earlier checkout, reset, main merge or production publication is involved.
The owner's latest scoped instruction authorizes these staging drafts. It does
not approve final legal terms or production readiness.

## Changes

- The existing hero uses 10,000 milliseconds of active time per slide, retaining
  the same photographs/order, headline wording, crossfade and image derivatives.
  Previous/next arrow controls replace visible numbers. Pause/resume is a small
  inline-SVG toggle with accessible action name and state, no visible label,
  position caption, dots or countdown. Reduced motion disables automatic changes
  and retains keyboard-operable manual arrows. Hidden tabs suspend the timer;
  pause/resume preserves remaining time. No image or animation dependency added.
- The existing business description is unchanged, with responsive 18–22px type
  and 1.65 line height. The headline remains larger; narrow screens wrap naturally.
- Existing FAQ, Terms, Refund & Cancellation and Privacy routes are generated
  from JSON using their existing page shells/styles and legacy URL architecture.
  No duplicate help centre or new public route was introduced. Six existing FAQ
  topic anchors remain, with 30 questions and matching generated FAQPage answers.
- `_data/customer-information.json` is the common source for payment phases,
  Cotton prices, contents, included package, quotations, stage estimates and
  delivery. `_data/policy-pages.json` and `_data/customer-faqs.json` contain the
  customer text; `scripts/customer_information.py` expands shared facts;
  `scripts/build_customer_information.py` renders the four existing sources.
  The existing build pipeline regenerates clean aliases, metadata and output.
  The four revised pages render the same existing legacy header fragment and
  navigation styles during the build, preventing later header-fetch layout
  movement without changing its design or destinations.
- Standard Cotton prices (RWF): men two-piece 200,000; men three-piece 250,000;
  women two-piece 150,000; women three-piece 200,000. These are standard jacket/
  trouser packages, plus waistcoat for three-piece. Shirts are not automatic;
  skirt-suit options and special requirements need a quotation. Higher collection
  prices are not published, and no old unnamed tier was renamed. No calculator,
  automatic surcharge or unsupported fabric-composition claim was introduced.
- Suit payment: 70% advance; balance when tailoring is complete, before final
  cleaning/delivery; full payment before release. Standalone alterations and
  cleaning: 70%/30%, balance on service completion before release/delivery.
  The actual unpaid balance is the agreed total minus received payments.
- Included suit package: agreed suit/standard tailoring, branded hanger,
  protective cover, one initial standard professional cleaning and initial
  door-to-door Kigali delivery. Included items are not charged again. Outside-
  Kigali courier/agency charges are customer-paid and confirmed before dispatch;
  no courier deadline is promised. Mobile visits/follow-up transport are separate.
- Standard tailoring usually 2–4 days; express usually 12–15 hours; alterations
  usually one maker day. These are work-stage estimates, not end-to-end deadlines.
  Sourcing, scheduling, fittings, changes, cleaning and delivery affect the total.
- Owner-reported numerical cleaning estimates remain OUT of customer
  HTML/schema pending cleaning-service publication approval. The care
  catalogue gates, unpublished treatment categories and empty price rows remain.
- Booking/measurement sources retain fields, integration values and destinations.
  Buttons/success text describe requests, not accepted orders or confirmed
  appointments. Fixed 24-hour response promises and old speed/35% options are
  removed. A readable Privacy link near submission controls explains that
  Web3Forms forwards requests by email, rather than claiming direct browser-to-
  business receipt. The existing submission controller is unchanged.
- Current suit/alteration/care/process pages use the relevant confirmed facts.
  No blanket delivery fee, historical mobile charge or express surcharge is used.
- Unapproved reward/loyalty/referral/photoshoot promotions and premium gift or
  follow-up cleaning promises are removed. Initial included suit cleaning remains.
  A still-fetchable legacy why-choose component no longer promises old deadlines
  or guaranteed delivery. Existing media files remain preserved.

## Draft boundaries and decisions still required

Customer-facing pages contain no internal decision lists or editorial placeholders.
They provide the confirmed information and a practical contact/review route where
final conditions cannot be supported. The historical pre-production case-by-case
cancellation approach is retained as drafting material, without automatic refund
or automatic advance forfeiture. Post-start requests are described as requests
for review; this is not a newly approved final entitlement or penalty schedule.
Existing exceptions for business non-completion and applicable rights are retained
without blanket no-refund language.

Before final publication, owner and appropriate legal review must resolve:

1. Final cancellation/refund rules, advance treatment and processing arrangements.
2. Post-start change feasibility, quote revisions and additional-charge approval.
3. Fitting correction eligibility, reporting windows, repeat work, supplied
   measurements and transport costs. Historical 72-hour/free-correction terms
   are not presented as current approved conditions.
4. Uncollected garments, reminders, storage and handover arrangements. No 10%-per-
   day charge, day-12 abandonment, forfeiture, resale power or other penalty is
   reactivated. No blanket liability exclusion is carried into the drafts.
5. Cleaning availability, treatment limitations, stains, pre-existing condition,
   damage/loss/claims, provider responsibilities and numerical timing publication.
6. Courier responsibilities, coverage, failed delivery and dispatch/receipt details.
7. Privacy/photo/marketing consent processes, retention, provider arrangements,
   request handling and any international-transfer requirements. Ordering does
   not itself authorize advertising use of customer photographs. The authorized
   project photographs remain intact; existing permissions are not revoked.
8. Final express/mobile scope, retail charges/surcharge bases and higher-collection
   publication approval. No unapproved higher-collection prices are stored here.
9. Gifts, follow-up care, loyalty and referrals remain outside active offers.

No supplier cost, maker fee, margin, budget, owner pay, reserve or target is exposed.

## Legal verification limit

Read-only requests to the official Rwanda data-protection authority website
`https://www.dpo.gov.rw/` and Ministry of Justice `https://www.minijust.gov.rw/`
were blocked by the managed proxy: CONNECT tunnel HTTP 403. This is a network
restriction, not evidence of their content or current law. No legal conclusions,
claim of full compliance, statutory deadlines or international-transfer safeguards
were added. The revised Privacy content describes observed form processing and
contact channels; unverified provider locations, retention periods, consent
records, security practices and transfer arrangements are not asserted.
This draft requires owner/legal review before any production approval.

## Preservation and routes

Public paths remain `/faq/`, `/terms-and-conditions/`, `/refund-policy/` and
`/privacy-policy/`, with original `.html` aliases and applicable historical
section anchors. Header/footer/navigation, approved About/Contact, 111 garment
pages, gallery filters/sharing/viewers, stable registry, five project pages,
photographs and integrations remain intact. No framework, dependency, credential,
account, DNS or hosting setting change is part of this phase. Sitemap remains
146 canonical indexable routes. Existing staging noindex protections remain;
actual deployed behavior requires live verification.

## Verification and delivery

Actual results, screenshots and the changed-file inventory are recorded with the
completed delivery. Evidence directory:
`/workspace/artifacts/customer-information-review/`.
No real form submission, customer message or Search Console submission is made.
Only the authorized staging branch may be committed/pushed after checks pass.

## Completed functional and accessibility checks

- Full build and `python3 scripts/build_site.py --check`: passed; generated output
  is reproducible. Fifteen static/build/data suites passed.
- Fourteen existing browser suites passed, including phase1/phase2 intercepted
  form outcomes, Collections V3, routing, headers, SEO, image delivery, discovery,
  homepage, About and Contact. No external forms/messages were sent.
- Updated `tests/final-v2.spec.cjs`: passed exact 9,999-ms hold / 10,000-ms advance,
  headline/photo synchronization, stable frame, explicit pause and hidden-page
  remaining-time suspension, plus 45 responsive preservation combinations.
- `tests/customer-information.spec.cjs`: passed 76 page/viewport combinations at
  320, 390, 768 and 1440 pixels; larger description, icon/keyboard/manual controls,
  30 FAQ disclosures/search, policy fragments/canonicals, form privacy notices,
  no page errors and no missing local responses. All 14 axe scans passed with
  zero detected violations (WCAG 2 A/AA, 2.1 AA and best practices). Low-contrast
  dates/links and affected-page landmark issues were corrected during review.
- New data regression verifies exact Cotton rates, FAQ visible/schema parity,
  publication boundaries and unchanged form fields, integration values/controller,
  original media, registry, all 111 garment pages and five project pages.
- Complete sitemap inventory: 146 unique canonical pages, metadata/H1/OG/JSON-LD
  checks and 6,010 existing local link/resource destinations passed.

Exact changed-file inventory: [customer-information-files.txt](customer-information-files.txt).
Screenshots in the evidence directory cover homepage, FAQ, Terms, Refund, Privacy,
booking and measurement pages at 390 and 1440 pixels, plus both hero images at
320/390/1440 pixels. Local automated checks do not replace owner/legal review.

## Final local performance measurements

Lighthouse 13.6.0 / Chromium 154, local preview, one cold measurement for each
mobile/desktop preset. Third-party HTTPS was blocked. These are laboratory
measurements, not verified staging field results or real-user INP.

| Page | Mobile performance | Desktop performance | Accessibility / Best practices / SEO, both |
| --- | ---: | ---: | --- |
| Homepage | 99 | 100 | 100 / 100 / 100 |
| FAQs | 99 | 100 | 100 / 100 / 100 |
| Terms & Conditions | 100 | 100 | 100 / 100 / 100 |
| Privacy | 100 | 100 | 100 / 100 / 100 |

Final FAQ/Terms/Privacy CLS is zero on both presets. Homepage CLS is zero on
mobile and 0.00048 on desktop. An initial diagnostic exposed movement caused
by the later header fetch; after the shared-header rendering fix, the affected
pages were functionally and accessibly rechecked and remeasured. The original
diagnostic reports are retained under `before-header-stability/`. Final report
JSON/HTML and screenshots are outside the public site in the evidence directory.

## Delivery boundary

Commit/push is restricted to `phase1/customer-journey-repairs`. No main merge,
production deployment, DNS/hosting/account change or Search Console action is
authorized here or performed. Staging revision verification must be reported
separately from a successful Git push. The environment proxy has blocked the
staging hostname in prior checks; no deployment success is claimed without
live evidence. These remain owner-review drafts, not approved final legal terms
or a claim of production readiness.
