# Final release preparation — 26 November 2026

## Scope and sources

Owner's latest FINAL RELEASE PREPARATION instruction follows the reviewed candidate `7808a5a1d96389a40b925b87f4172974ba41704f`. Work only on `phase1/customer-journey-repairs`; Main read-back is `33620fe4dc38ec81905fd2556a19db15f5c06db3`. No Main merge, production deployment or advertising-account mutation. This is targeted preparation, not another redesign.

Read `AGENTS.md`, the current reference's information master/source matrix/unresolved register/page map, `SEO_PRESERVATION.md`, `_data/seo-search-intent.json`, the source map and previous pre-launch report. New reference `versions/2026-11-26-02` preserves previous snapshots as exact prefixes and records rules REL26-01–04. No price, payment, cancellation, refund, delivery, fabric claim, media permission or contractual effective date changes.

## Page and action brief

- **Audience/purpose:** visitors from Ads and normal navigation should find the existing tailoring/service/contact pages and safe enquiry actions; the unfinished Shop must not be prominently advertised.
- **Headers/homepage/services:** remove only prominent Shop links through shared source logic. Preserve the reviewed tailoring hero, logo, all unrelated service navigation and existing verified contact details. Do not hide a visible Shop button with CSS alone.
- **Shop:** central `_data/shop-release.json` temporarily disables public navigation/indexing. Existing direct staging URLs, source/product records/APIs/requests remain functional for development and noindex. Production export uses a temporary branded holding view at every existing Shop path; no fake stock/checkout, permanent move or reopening promise. Sitemap exclusion does not delete records. Returning Shop to release requires an explicit reviewed setting change and tests.
- **Six sitelinks:** preserve `/services/custom-tailoring/`, `/mensuits/`, `/womensuits/`, `/services/alterations/`, `/services/garment-care/`, `/contact/`. No new redirect is justified while these destinations exist. Verify clean self-canonicals, production sitemap inclusion and query behavior without copying private form data into URLs.
- **Enquiries/contacts:** keep existing provider/review/explicit submit, validation, positive acknowledgement, failure recovery, exact garment/photo/quantity/fabric/colour fields and consent. Provider acceptance is not inbox receipt, order confirmation, production start or a sale. WhatsApp opens a manually editable conversation; clicking is not a sent message.
- **Terms/policies/benefits:** current effective Terms and consent remain; actual received review PDF is not activated. New Flexible Advance Payment remains inactive. Existing approved commercial scope/benefits and exceptions preserved; no tariffs or financial records edited.
- **SEO:** stage remains noindex; intended production service pages retain independent indexability/canonicals. Shop's temporary exclusion is deliberate and reversible; do not use permanent redirects or robots blocking that prevents crawlers seeing noindex. No production indexing action.

## Advertising preparation and exact limits

Source audit found no Google Ads conversion ID/label, GA4 measurement ID or GTM container. Owner was asked for the actual Ads destination; never invent it. `_data/advertising-measurement.json` records missing configuration and disabled external transport. Existing Meta optional consent and PageView-only behavior are unchanged.

`_templates/enquiry-measurement.js` prepares **first-party DOM signals only**:

- `mrsewing:enquiry-accepted`: existing verified positive application/provider response for an eligible quotation/consultation; eventId, kind, allowlisted service, outcome only. In-memory per-form deduplication; dispatch once in the same-origin top document for dialog/iframe journeys.
- `mrsewing:whatsapp-click`: secondary contact-click interaction, never a conversation/lead/purchase; random eventId and fixed interaction label only. No message, destination query, contact or garment details.

No Google/Meta conversion, `dataLayer` transport, network request, cookie, persistent event/attribution store or account configuration is added by these signals. They do not make PMax conversion tracking operational. A later authorized transport must use the real destination, appropriate separate Google consent/privacy disclosure, safe URL/referrer and campaign handling, and receipt/deduplication tests. Choose one primary import/direct conversion route to avoid counting one request twice. No monetary value is fabricated.

Sensitive/query-route Meta protection remains. Do not simply remove it to make UTM/fbclid arrivals track: vendor SDKs can read URL/referrer independently of custom event parameters. Full private form text, photographs, contact details and addresses must never enter advertising events. Staging must never send production conversion events.

## Tests and evidence

Before release candidate commit: full build/check, SEO/sitemap, temporary Shop source/projection/navigation tests, existing Shop server/browser contracts, Meta privacy/contact tests, first-party signal/deduplication tests, actual guided form provider-failure/retry/iframe tests, other existing browser regressions and six-sitelink HTTP/rendered/query checks.

The internal review package is outside deployed assets at `/workspace/review/final-release-2026-11-26/`. Record each actual PASS/FAIL/BLOCKED outcome; source/mocks never prove deployed accessibility, provider/inbox receipt or advertising account receipt. Managed environment currently excludes Pages/production/provider/ad-account hosts and has no account connections/secrets. Continue independent staging work and provide minimal owner checks.

The previous305HTML inventory includes five without canonicals: `/404.html` and raw `/header.html`, `/footer.html`, `/hero.html`, `/why-mtm.html` fragments. These are not five missing customer landing pages. Header remains a required legacy Kaunda fetch dependency. The300canonical count and300previous production-artifact page count refer to different sets, not300indexable pages; the sitemap is the intended indexable set. Its temporary Shop exclusion reduces64entries to57 while preserving the six Ads destinations.

## Deployment and rollback — prepare only

Preserve the prior read-only Main baseline and known reviewed staging commits. Push normally only to the authorized branch. Inspect exact GitHub/Cloudflare result, deployment ID and preview; actual permanent served content must be checked separately. No successful receipt is described as independent browser verification.

After separate owner release authorization, verify actual hosting/branch/output, preserve production settings, publish only the public-only candidate, and deploy compatible existing Pages API runtime before/with the frontend. Keep private compiler inputs/source data out of static assets. Preserve current Terms and production indexability. Capture the actual known working production frontend/runtime deployment pair before release. Roll back to that pair on critical request/privacy/legal/indexability failure, using provider rollback or a normal reviewed corrective commit, never force-pushing/resetting Main or blindly rolling back databases.

Minimum external verification and exact release/campaign checklist are provided in the final internal report. Minor spacing, optional imagery/profile additions, Shop development and nonblocking performance improvements are deferred.
