# Staging review — 11 November 2026

These changes are for the development branch and Cloudflare staging only. Main remains at owner logo upload 4fefad3fb5fb1bbb5f5feb3af671035c6cec5628. The previous R31 customer-policy review is preserved and still requires owner approval before production publication.

## Changes for review

- Shop mobile navigation now has readable white/gold links against its black menu.
- Custom Tailoring supports Select This Design, Selected Designs, quantities, removal and continued browsing. Each design keeps its own fabric selection: choose a fabric, request help, or supply your own. One existing quotation form carries canonical photograph links and names for all selected designs. Add or Change Designs returns directly to browsing and retains the contact draft. The old change-design dropdown and redundant Enquire About Custom Tailoring link are removed.
- The email handler validates every design, photograph, project, fabric and quantity. Provider rejection preserves the request; only provider acceptance displays success. This does not create a Shop cart, reserve stock or activate payments. Technical request limits are 50 designs, total quantity 9,999 and the existing request size limit; these are not commercial entitlements.
- FAQs now provide a white Help Centre with search, Common Questions, 14 topic cards and actual question counts. Two columns on desktop, one on phones. There are 104 answers and 164 source-linked search entries. Added direct cost questions for suits, two/three-piece options, double-breasted suits, tuxedos, Express, after-hours, alterations, cleaning, mobile and VIP assistance, Shop enquiries and children's tailoring. Existing approved prices are used; missing standalone cleaning/alteration rates are not invented.
- Public branding uses Mr Sewing or Mr Sewing Fashion. The real official email address remains unchanged.
- Men's ordinary Tier 4 two-piece starting price is 250,000 RWF following the owner's correction. Men's three-piece 250,000 RWF and the other women's, fabric-tier and tuxedo schedules remain unchanged. Please review this precise scope. Price tables distinguish Two-Piece Starting Price and Three-Piece Starting Price.
- Children, including age two, can request assessed tailoring. The earlier child's individual 250,000 RWF quotation is not a universal child price. A 50% child-garment discount applies only when individually offered and confirmed; it is not an automatic permanent entitlement. Express guidance retains feasibility confirmation and the approved surcharge rules.
- About Us uses the owner's exact NLOGO.png artwork. The original is 1536 × 1024 RGB with an opaque black background, not transparent. Optimised derivatives are nexus-logo-480.webp (480 × 320) and nexus-logo-960.webp (960 × 640). No substitute logo, artificial 4K claim or modification of the global MS logo.
- A verified existing Google Maps directions link is included. No verified Google rating/review count was supplied, so no stars or fabricated rating are displayed.

## Policy and source limitations

Current repository customer reference records, policy facts, price schedules and implementation were reviewed alongside the latest owner instructions. Original company handbooks remain unavailable, as recorded in the R31 reconciliation. R31 unresolved refund/cancellation/privacy/legal clauses and standalone service advance-payment decisions remain for owner review. No new unsupported rates, shipping promises, blanket forfeiture rules or payment gateways have been introduced.

## Validation

PASS production build parity; 104-answer/14-topic FAQ generation; 55 canonical sitemap routes; policy consistency and arithmetic; 27 legacy selected-photo mappings; multi-design server validation including invalid IDs/photos/projects/fabrics/quantities/duplicates/consent; commerce server regression with mocked provider.

PASS browser checks at widths 320, 360, 390, 430, 768, 1024 and 1440; FAQ search/layout; Shop mobile menu and Services dropdown; About image decoding; multi-design refresh/add/remove/per-design fabrics/contact draft/review/provider failure and success. Axe checks passed for main content on FAQ, About, Shop and Fabric Guide. No real customer messages or payments were sent. Chromium emulation is not physical-device Safari verification.

Cloudflare deployment and direct URL verification are recorded separately after the staging push. A successful deployment notification alone is not proof of direct live browser verification.
