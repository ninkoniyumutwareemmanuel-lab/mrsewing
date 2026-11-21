# Meta Pixel — staging implementation (21 November 2026)

Pixel ID 29683883327873735 was provided directly by the owner. Implemented only on the phase1/customer-journey-repairs development branch.

## What the code does

The existing shared site builder injects one local first-party bootstrap into generated pages. It does not load Meta from the visitor's browser before optional marketing consent. The consent choices are Decline or Allow tracking, with a Privacy Policy link and a Tracking preferences control to revisit the choice.

Only the standard PageView event is prepared. Sensitive service/form/policy URLs and URLs carrying query strings are excluded. There is no unconditional noscript image, advanced matching, customer-data payload, purchase event or Conversions API integration.

The _data/meta-pixel.json productionEnabled flag is FALSE. No active tracking is authorised or sent on staging. To demonstrate the consent interface without sending events, append ?meta_pixel_preview=1 to a deployed Pages staging URL.

## What still needs approval

1. Owner review of the Privacy Policy disclosure, including Meta as an optional advertising measurement recipient.
2. Review the applicable Rwanda data protection obligations with the responsible adviser, including controller obligations and third-country data transfers. Official supervisory resources: https://dpo.gov.rw/.
3. Test actual browser-network consent behaviour and Meta Events Manager diagnostics. Source tests alone cannot establish successful Pixel delivery.
4. Separate owner authorisation for production activation and publication. Only then update the production flag and owner-approved status, rebuild and deploy.

Existing published Privacy Policy states no advertising tracker is introduced; that remains true while this proposed Pixel is disabled. No policy publication or live change was carried out as part of this staging integration.
