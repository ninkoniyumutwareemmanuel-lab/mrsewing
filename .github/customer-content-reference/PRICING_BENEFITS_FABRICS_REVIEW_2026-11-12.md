# R37 — Pricing, benefits, fabrics and FAQ staging review

Owner instruction12November2026; baseline0a446ad2b8360038b650a5853d3fc9007493d4f7. Branchphase1/customer-journey-repairs only. Main4d972f29417fa60366ebdb6348e1599208f6ae08 protected. No production publication, main merge/push, environment changes, payment activation or spend. Previous reviewed visual design and customer journeys preserved.

## Current authoritative prices — RWF

| Tier / Quality | Men two-piece | Men three-piece | Women two-piece | Women three-piece |
|---|---:|---:|---:|---:|
| 1 / 1 |600,000|800,000|500,000|550,000|
| 2 / 2 |400,000|550,000|350,000|400,000|
| 3 / 3 |300,000|400,000|220,000|270,000|
| 4 / 4 |250,000|300,000|150,000|200,000|

Men's tuxedos unchanged: Tier1two800,000/three1,000,000;Tier2two600,000/three800,000. Tuxedo JSON is byte-identical to reviewed baseline, with no new accessory/ordinary-benefit promises. No change to customer-supplied-fabric/Special/alteration/cleaning/other service rates.

Ordinary catalogue _data/suit-package-prices.json is keyed by audience+tier, not fabric IDs. Removed duplicate page-specific prices; minimum-price summaries and shared text derive from the catalogue. Existing women amounts and approved source dates retained. Latest men source recorded12November2026. Fabric classifications are independent list entries: many IDs may share one tier, demonstrated in a temporary in-memory test without creating a deployed product.

## Implemented customer information

Four ordinary tables: Men's Two-Piece, Men's Three-Piece, Women's Two-Piece, Women's Three-Piece. Exactly Tier / Quality | Price (RWF) | Included Benefits; no individual fabric labels under tiers. Existing black/gold style retained. Every row includes initial cleaning/Kigali delivery/hanger+cover; Tiers1/2 show3cleanings+collectiongift. Disclosure explains3total(initial+2followups), three-month period after garment receipt, qualifying suit+one-shirt follow-up scope, customer-paid follow-up transport and gifts: menTier1shirt+necktie/Tier2necktieorbowtie;womenTier1/2innertop. Tiers3/4initialonly/nogifts/noadditionalfreecleaning. No unlimited entitlement or invented multi-suit gift quantities.

Fabric Guide and fabric-selection cards show approved reference images, fabric names, assigned Tier/Quality, existing cautious descriptions/availability and links to Custom Tailoring prices. Removed ordinary and tuxedo numerical suit schedules from the guide. Existing eight IDs/classifications and image associations retained; no new Vigo/Prado/stock/composition guarantees. Legacy tuxedo-prices guide anchor now links to the actual separate Custom Tailoring schedule. Selection IDs, original-photo URLs and per-design return journey remain unchanged.

Shared facts/Terms/benefits/customer information/FAQ/search/structured answers now use current pricing and approved child/bulk/benefit/payment facts. Child under12automatic50%withnormal-priceadult in sameorder, alltiers, child-onlynormalcorrespondingprice;nostacking. Bulk>=2qualifyingsuitsoneorder, highestpricedatregularprice,3%second+subsequentonly, highesteligiblecustomerdiscount/notstacked; original separate group/loyalty/referral rules preserved. No automated discount engine added.

All-customer payment verification covers workplace cash received/recorded/acknowledged, actual bank/MobileMoney receipt, pendingnotcompleted/screenshotsnotproof, confirmation+nextsteps after verification, approved exceptions and separate production-start conditions. Domestic70/30balance timing and international100% retained. No new online payment facility.

Removed after-pricing RequestYourQuotation and bottomVisitShop actions. Hero and bottom each retain exactly two Men/Women exploration buttons. Header Shop and all existing enquiry/quotation/provider/WhatsApp integrations remain. Header/footer/hero photograph/title/meta/canonical/page schema unchanged; homepage and Shop files/commerce assets/catalogue/private flag unchanged.

## Announcement

Fixed, noninteractive OFFER span. Three exact approved uppercase messages, continuously progressing90slinear loop:
1.50% OFF CHILDREN'S SUITS WITH AN ADULT SUIT
2.FREE INITIAL SUIT DELIVERY WITHIN KIGALI
3.3% OFF ADDITIONAL QUALIFYING SUITS IN BULK ORDERS

No links, buttons, Seeconditions action, hover/touch/focus/Escape pause, tap expansion or underlines. Copy remains separate in data. Duplicate visual track is aria-hidden. Operating-system reduced-motion and no-JavaScript modes display static readable messages. Detailed terms are in the relevant page/FAQ. Manual accessibility limitation: nonessential movement lasting beyond5seconds has no on-page pause/stop/hide mechanism under the explicit owner requirement; reduced-motion support and zero automated findings do not establish full WCAG2.2.2conformance.

## FAQ changes

Eight new and eleven updated answers;112answers across14topics. Required11subjects include suit contents, tier differences, cleaning count/window/shirt coverage, transport, gifts, fabrics versus pricing, bulk, family and payment verification. Existing IDs retained where applicable; new answers participate in native accordions, source links, search index and FAQ JSON-LD. No duplicate contradictory benefit policy source or internal/confidential record search.

- UPDATED `suit-package`: What is included in every custom suit? — /services/custom-tailoring/#service-info-prices
- UPDATED `higher-collections`: What gifts are included in Tier 1 and Tier 2? — /services/custom-tailoring/#suit-benefit-conditions
- UPDATED `payment-methods`: How should I arrange and verify payment? — /terms-and-conditions/#3
- UPDATED `suit-starting-cost`: How much does a suit cost? — /services/custom-tailoring/#service-info-prices
- UPDATED `double-breasted-cost`: How much does a double-breasted suit cost? — /services/custom-tailoring/#service-info-prices
- UPDATED `tuxedo-cost`: How much does a tuxedo cost? — /services/custom-tailoring/#tuxedo-prices
- UPDATED `standard-service-cost`: How much is Standard service? — /terms-and-conditions/#starting-prices
- UPDATED `children-cost`: How much does children’s tailoring cost? — /terms-and-conditions/#childrens-tailoring
- UPDATED `parent-child-offer`: How does the children’s 50% discount work? — /terms-and-conditions/#childrens-tailoring
- UPDATED `mens-suit-cost`: How much is a men’s two-piece or three-piece suit? — /services/custom-tailoring/#service-info-prices
- UPDATED `womens-suit-cost`: How much is a women’s two-piece or three-piece suit? — /services/custom-tailoring/#service-info-prices
- ADDED `suit-tier-differences`: What is the difference between Tier 1, Tier 2, Tier 3 and Tier 4? — /services/custom-tailoring/#suit-benefit-conditions
- ADDED `suit-complimentary-cleanings`: How many complimentary cleanings do I receive? — /services/custom-tailoring/#suit-benefit-conditions
- ADDED `suit-cleaning-window`: When can I use my additional cleaning benefits? — /services/custom-tailoring/#suit-benefit-conditions
- ADDED `suit-followup-shirt`: Does complimentary cleaning include a shirt? — /services/custom-tailoring/#suit-benefit-conditions
- ADDED `suit-benefit-transport`: Is collection and delivery free? — /services/custom-tailoring/#service-info-transport
- ADDED `fabric-tier-pricing`: Do all fabric types have different prices? — /guides/fabrics/#fabric-references-title
- ADDED `bulk-order-discount`: What is the bulk-order discount? — /benefits/#4
- ADDED `payment-verification`: How are payments verified? — /terms-and-conditions/#3

## Consistency and preservation audit

Inspected active source JSON/templates/scripts/price references and all314trackedHTMLfiles (including aliases/templates), not historical decision versions. No obsolete men's650,000/450,000/320,000or250,000three-piece statements found in current rendered text. Contextual checks retain legitimate women's/tuxedo values. All16ordinary+4tuxedoamounts exact. No numerical suit schedules remain in guide/selectioncards. All FAQ sources/fragment IDs resolve.280JSON-LDblocks parsed; no unapproved ProductOffers introduced. All55canonical indexable routes remain eligible and sitemap/robots synchronized. Original source history and past dated decisions remain unchanged.

## Tests actually completed

PASS full build/parity, Python/JSsyntax, whitespacecheck; pricing-benefitssourceaudit/multiplefabricpertierfixture/all11FAQsubjects/sourceanchors; existingpolicyarithmetic/sitemap/guideimage+measurementchecks; approvedphotoassetprotection; selectedphoto27mappings/multi-designvalidation; commerce/publicCORSvalidation. Providers mocked, no messages/payment/inbox claims.

PASS Chromium320/360/375/390/430/768/1024/1440: all5tables/16ordinary+4tuxprices/benefits/headerrowcount/wrapping/nohorizontaloverflow, exacttop/bottomactions/headerShop, disclosurecontent, eightmainAxechecks. Announcementfixedlabel/nocontrol/nooverlap, eachmessageprogressessequentially, movementcontinuesaftertouchandhover, reducedmotion/noJSstatic. Guideimagesdecode andall8cardsnoindependentprices at320/390/1440. Hero/bottombuttondestinations at390/1440;FAQsubjectsearch/deeplinkopensanswer. Local320/390/1440screenshots inspected.

PASS existing full multi-designfabricquotation regression: selections/qty/add/remove/refresh/contactdraft/per-designfabricbrowsing/advice/own/cancel/return, exactimageURLreview/providerpayload, failedproviderpreservesinputs andpositiveacceptancealonemarksuccess;7responsivewidths/sharedFAQShopAboutGuideAxe. PASS all14FAQcategories/112accordions/10searchqueries/emptyclear/sourceanchors/9pages7widths/3Axe. No physical-deviceSafari or realinbox verification.

## Remaining limits and decisions

- Original named company handbooks are still unavailable; inspected repository references and latest explicit owner task are the actual sources, not claimed original verification.
- Exact follow-up booking/redemption process and gift allocations for multi-suit orders remain unspecified. Confirmed benefits are published on staging; no notice/proof/extension/transfer/quantity rules invented.
- Mixed family/bulk qualifying-item allocation edge cases are not further specified; no new automated rule/engine or stacking introduced. Human-reviewed quotation identifies applicable discounts.
- Continuous noninteractive announcement motion remains the accessibility limitation explained above, despite reduced-motion support.
- Actual deployed page browser verification must be attempted after push. Network restrictions have previously blocked pages.dev; report actual result separately from Cloudflare build/deploy status. No production change authorised.

Exact commit and Cloudflare-issued preview/check are recorded in final delivery after staging push. Complete changed-file list is PRICING_BENEFITS_FABRICS_FILES_2026-11-12.txt. Owner reviews staging before any separately authorised production release.
