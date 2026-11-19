# R52 — Follow-up fit, audit and non-destructive plan

19November2026; inspected staging branch `phase1/customer-journey-repairs`, baseline `749b21d99f0dacf21d260b1adfc3ebca52a76447`. Tracked implementation was clean before the follow-up; `.wrangler/` and Python caches are existing tooling and must not enter the commit. Main/production are outside authorization. This document is an audit/plan, not a completed-test report.

## What already works and is reused

R51 already established the JSON/Python/template source architecture, `business_settings.py` shared contact/navigation projection, effective approved media library and `/showroom/`, reusable two-card plus larger-feature homepage showcase, quotation-first public services, unchanged internal pricing/Shop gates and prepared Terms PDF infrastructure. Reuse these sources and current selection/fabric/quotation/consent functions rather than introduce a second system.

The actual service remains keyed `custom-tailoring` and its established route is `/services/custom-tailoring/`; shared header/footer consume `_data/customer-release.json` service labels. Publicly renaming the entry to **Tailoring Services** does not require moving the route or losing existing inbound links/canonical URLs. The main service overview may group **Suit Tailoring**, **Special Tailoring**, and **Alterations & Repairs**, while dedicated Alterations/Special pages and their distinct policies/forms remain authoritative. No redirect or new keyword-variation page is needed for this label change.

Official business contact is projected from `_data/business.json` through existing helpers; existing WhatsApp Terms consent supports safe manual handoffs. Existing selected-design sharing already preserves friendly names, exact photo references, quantities and long-message fallback. Reuse those mechanisms and preserve native sharing/copy/website quotation alternatives. No new provider, browser upload, payment integration or contact number is needed.

## Gaps this follow-up closes

1. The first R51 homepage cards lead with “Men's Fashion”/“Women's Fashion” and the underlying main H1 is the brand alone. The new owner direction explicitly authorizes clearer professional-tailor positioning and custom-suit emphasis without a homepage rebuild.
2. Existing Send Design actions/WhatsApp consent can be made easier to discover through the exact **Send Your Design on WhatsApp** wording, initial showcase, immediate design-sharing card and an unobstructive mobile entry.
3. Current service display name **Custom Tailoring & Suits** can become **Tailoring Services**, retaining URL, stable data IDs and scoped commercial rules.
4. Existing page SEO is valuable, but targeted home/service/Special/Showroom messaging may better describe the approved tailoring enquiry purpose. The baseline capture is in `.github/customer-content-reference/R52_SEO_BASELINE_2026-11-19.json` and includes initial titles/descriptions/headings/canonicals/robots/alt/links/JSON-LD for seven relevant routes. It is Git evidence, not production HTTP verification.

## Scope boundaries and conflicts

- **Video preference versus permissions:** R51 has28eligible photographs, while `_data/media-video-records.json` has no approved video record. Seven recovered MP4s remain held. Build on existing video-capable cards but keep approved-photo fallbacks until real rights/classification/poster approvals exist. The layout request is not blanket video permission.
- **Grouping versus policy merger:** Alterations/Special requests must not inherit ordinary-suit production screening, payment, delivery, packages or benefits merely by appearing on the Tailoring Services overview.
- **WhatsApp versus quotation:** opening a prepared conversation does not attach a picture, send it, establish receipt, submit the website form or accept an order. Current Terms/manual-Send safeguards remain. Both contact paths remain available.
- **Fabric expectations versus inventory:** owner observations guide UX without invented percentages. Show actual choose/advice/own-fabric choices and suitability/availability confirmation, not a supply guarantee.
- **Shop and service pricing:** quotation-first public service presentation remains; Shop stays functional and retains legitimate product prices/gates. Internal rates and agreed quotations are unaffected.
- **SEO/analytics:** retain stable routes/canonicals/sitemap/indexing purpose. No paid analytics or unsupported search-volume/ranking/conversion claims. Existing source inspection found no configured gtag/dataLayer/Plausible/Umami instrumentation in the main homepage/contact files checked; implementation must not claim event collection without evidence.
- **Release/approval:** no destructive migration or production action is needed. The approved PDF, held-media permissions, actual supplier specifications and legal disclosure review remain pending from R51. Reattempt deployed staging checks without bypassing the managed network policy; report any block separately from provider status.

## Coordinated safe plan

Reference updates are isolated from implementation edits. Parent implementation owns source/UI/SEO changes and rebuilds only after coordinated edits. Reuse central service/contact/media/CTA sources; keep homepage's useful existing content below the refined showcase. Add concise service grouping and fabric support, retain existing forms/context, then test consent/manual handoff and selected-reference integrity with mocked external interactions.

Run build synchronization, SEO/sitemap, public-price/internal-source preservation, media/rights/document and relevant quotation/session regressions. Review mobile/desktop layout, one-H1 hierarchy, tappable CTA, keyboard focus, sticky/header/selection-bar overlap and fallback behavior. Record exact commands, actual PASS/FAIL/NOT TESTED, staging commit/provider URL and any unavailable rendered check in the final report. Do not infer an enquiry/order or Google indexing result from a click or successful build.

Current approved scope and full pre-writing checklist: [R52 brief](../.github/customer-content-reference/R52_TAILORING_FIRST_BRIEF_2026-11-19.md). Developer ownership/procedures remain in [WEBSITE_SOURCE_MAP.md](WEBSITE_SOURCE_MAP.md).
