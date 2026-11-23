# R67 — Tailoring & Clothing Services customer guide (staging only)

**Date:** 23 November 2026  
**Owner decision:** After reviewing current mobile screenshots and the proposed clearer order/fabric/service information, owner agreed to implement the proposed page improvements. **Staging only; no main/live publication permission.**  
**Page:** `/services/custom-tailoring/`  
**Audience:** Customers browsing tailoring, garments and related services.

## Reference and approvals reviewed

- Current customer reference pointer: `.github/customer-content-reference/README.md` → `versions/2026-11-22-01/`; inspected customer information master, policy source matrix, unresolved register, page content map, R59 owner directive and page brief checklist.
- R59 owner directive, 22 November 2026: preserve tailoring-first hub, two authorised image-driven gender category cards and four separate extra service routes; keep Showroom publication gate, home/Shop/Terms holds.
- Owner-approved `_data/customer-policy-facts.json`, 7 November 2026 and latest completion release 13 November 2026: standard custom tailoring 1–3 weeks; express 2–3 days subject to feasibility; 70/30 domestic custom garment payment; international 100% before production after assessment; express +35%, agreed after-hours +25%, both +60% additive; official production-start notice; customer-fabric assessment; service-specific quotation/payment distinctions.
- `_data/customer-information.json`, 7–13 November updates: verified completion/delivery distinctions, qualifying initial suit package cleaning and Kigali delivery; avoid universal charges or dates.
- Owner's Master Operating Handbook V8, 2 November 2026, Part I (inspected from owner-provided document): combined Garment Repair & Care is an individually assessed coordinated enquiry with separate service lines; no automatic discount. The newer 7 November customer-policy wording governs standalone service payments where source wording differs.
- Customer-supplied fabric stand-alone service rules file is **PROPOSAL ONLY**; do not announce its proposed rates, liability, inclusions or fixed contract as approved.

## Page scope and safe customer experience

1. Add quick facts before the longer process, sourced from approved policy JSON instead of hardcoded percentage/estimate values; explicitly distinguish estimates from accepted order deadlines.
2. Replace the four lengthy generic process cards with a compact four-step journey: request → assess design/materials/measurements → accept quotation → official production start/fit/handover.
3. Add two fabric information cards: advice from the existing Fabric Guide or assessment of fabric already owned. No exact colour/stock guarantees, uploads or fixed customer-fabric terms.
4. Preserve **exactly two existing, source-driven** Men’s and Women’s image category cards with existing Showroom/approved design references. No photo/publication status changes.
5. Preserve four discrete service links: Special Tailoring, Alterations, Garment Care, Mobile; add only an explanation/link for an *optional combined* Repair & Care enquiry via the existing generic request page. No invented fifth service-specific backend or automatic combined charge.
6. Add three short native disclosure FAQs and a general quote CTA. Customer enquiries are not automatically accepted or recorded as confirmed orders.

## Button / route contract

| Action | Existing destination | Expected result / limits |
| --- | --- | --- |
| Learn detailed payment/ordering rules | `/customer-information/` | Existing guidance page, not a checkout |
| Fabric Guide | `/guides/fabrics/` | Existing fabric education |
| Own fabric / special design | `/services/custom-tailoring/special-order/` | Existing enquiry workflow, not file upload |
| Measurement preparation | `/measurements/` | Existing advice, not booked fitting |
| Men's / Women's cards | Existing publication-gated `category['url']` from loader | Showroom reference browsing; no stock promise |
| All designs | `/collections/` | Approved Showroom |
| Four extra-service buttons | Existing `/services/custom-tailoring/special-order/`, `/services/alterations/`, `/services/garment-care/`, `/services/mobile-fitting/` | Existing dedicated pages/forms preserved |
| Combined garment assessment / general quotation | `/request/?general=1` | Existing generic enquiry; describe both services; no automatic paired backend record claim |
| VIP | `/services/vip/` | Existing separate assessment |
| FAQ | `/faq/` | Existing customer FAQs |
| Currently effective Terms | `/terms-and-conditions/current/` | Existing effective HTML |
| PDF Terms reader | `/terms-and-conditions/` | Existing PDF preview, activation unresolved |

## Holds and non-changes

- No changes to homepage source, hero, shared CSS/components, photos, gallery source, SEO title/description/canonical/sitemap policy, quote provider integrations, user data, confidential finance, payment account, Terms activation or production hosting.
- All staging routes remain noindex; no Google indexing or live-page alteration.
- No customer messages are sent and no payment is requested/collected by this change.
- There is **no new commercial-policy approval**: this is a staging presentation of already approved policy facts plus approved site layout; existing 2026-11-22-01 policy snapshot remains the reference.
- Public preview HTTP response, physical device behavior, provider form receipt, and production deployment require independent verification; do not infer from GitHub code checks.

## Validation

Modified source: `scripts/tailoring_services_hub.py`, `_templates/tailoring-services-hub.css`; extended existing 320/390/768/1440-pixel browser suite `tests/r59_tailoring_browser.cjs`. GitHub Actions R59 workflow rebuilds generated pages, checks the site and uploads browser screenshots; check the latest run before claiming PASS. Source file commits alone are not a deployment verification. Owner review is required before any main/live release.
