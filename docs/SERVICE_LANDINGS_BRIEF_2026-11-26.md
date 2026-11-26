# Service landing implementation — 26 November 2026

Scope: `/services/alterations/`, `/services/garment-care/`, `/services/mobile-fitting/`, `/services/vip/`, and the combined Repairs and Cleaning card on the tailoring hub. Starting implementation is `b388644796fcb24b747bb6818dd211422fab9cff`; staging branch only.

## Before-edit audit and source applicability

Read `AGENTS.md`, current customer reference README and applicable master, policy matrix, unresolved register and page map in `versions/2026-11-25-01`; inspected actual customer-site generators, policy facts, service records, public-content publication adapter and official contact record. Named original company handbooks remain unavailable; the current owner prompt supplies historical excerpts, not a new independently inspected handbook.

The four service heroes led to forms with inconsistent Request Service/Request VIP Service labels. Each page then repeated long sequential sections and policy paragraphs. VIP advertised an unfinished Subscription section. The hub's combined card went to the general request page, requiring an unnecessary extra journey. Existing request forms and backend routes are functioning protected assets, not removal candidates.

Latest owner 26 November sections17–22 approve compact informational landing pages, service-specific direct WhatsApp actions and removal of unfinished membership advertising. Service scopes remain those in `_data/customer-release.json` and `_data/customer-policy-facts.json`. R49-06 supersedes historical independent consultation25,000 with35,000RWF; eligible order visit10,000 and independent assistance50,000 remain separate. The current50,000 assistance source includes up tofivepeople/threehours, exceeding either requires VIP assessment.

**Publication conflict resolution:** R51 quotation-first service-price publication remains effective in `_data/public-content-policy.json`. The latest prompt requests reconciliation of historical starting prices, not automatic replacement of newer applicable decisions. No old alteration/cleaning tariff or25,000 consultation was restored. The public mobile comparison explains eligibility and scope with individually quoted prices, preserving exact approved prices internally. Restoring public tariff schedules remains an explicit owner decision, separate from accurate internal fee preservation.

## Implemented presentation and action contracts

- `scripts/service_landings.py`: shared presentation of four distinct services; approved policy text/anchors reused, not a second policy database. Essential timing, agreed surcharges, payment and transport conditions remain visible. Standalone payment wording comes from `customer_information.information()['standalonePayment']`; custom-suit final-cleaning sequencing is not automatically applied to other services.
- `_data/service-contact-actions.json`: one central action label and exact owner-provided service messages. The official number is read from `_data/business.json`, never duplicated as a new number. A user click opens an editable WhatsApp message through the existing adapter; it neither sends nor acknowledges a message.
- `scripts/customer_site.py`: service hero actions and service-page delegation; emits the scoped stylesheet. Existing request/form functions and submission contracts are preserved.
- `_templates/service-landings.css`: compact responsive typography, service comparisons, visible keyboard focus, wrapping actions and scoped gold-button contrast; no homepage/global design replacement.
- `scripts/tailoring_services_hub.py`: combined card opens the exact combined WhatsApp message. Separate assessment/pricing, no automatic discount, approval before additional paid work and no double applicable transport charge remain disclosed.
- VIP membership/subscription information is removed from the public main VIP landing page; historical implementations and existing request routes are preserved.

Current contractual links point to `/terms-and-conditions/current/`, not the not-yet-effective review PDF. Refund, Privacy and FAQ links remain available. No payment integration, stock, new service capability or timeframe guarantee was activated. Selecting a preferred appointment is not a confirmed booking or request for payment.

## Testing and limitations

`python tests/service_landings.py` validates generated source rendering, exact decoded service messages/official destination, existing form routes and policy anchor preservation, no unfinished VIP offer, quotation-first tariff protection and correct unchanged internal mobile fees. Root integration will record actual build, browser/mobile/keyboard, SEO and deployed-origin outcomes separately. This focused test does not send messages or submit forms and does not claim actual WhatsApp delivery.

Physical devices, actual WhatsApp account delivery and live provider inbox receipt are not verified by static unit checks. Main/production publication is not authorized.
