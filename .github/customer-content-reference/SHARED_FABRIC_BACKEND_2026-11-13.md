# R48 shared fabric and colour — receiving-system contract

Owner source: Complete Custom Tailoring Customer Journey,13 November2026. Staging only, phase1/customer-journey-repairs. Read AGENTS and the current2026-11-13-02 master/matrix/register/map before this change. This implements one ordinary-suit enquiry preference; it changes no price, benefit, payment, stock or material guarantee. Existing Special Tailoring and unrelated service validators are unchanged.

## Request format

The existing selected-design endpoint accepts an optional top-level object:

```json
{
  "fabricPreference": {
    "choice": "now",
    "fabricRef": "men-wool",
    "colour": "navy-blue",
    "colourDescription": ""
  }
}
```

`choice` is `now`, `advice` or `own`. A specific choice requires an existing approved fabric identity and a centrally defined colour identity. `other` requires a short custom colour description (1–80 characters; Unicode letters/numbers and basic colour punctuation; no control characters, HTML or URLs). Advice/own reject stale selected-fabric/colour fields. Unknown preference properties and invalid types/lengths fail before provider contact.

The optional object is authoritative for the whole enquiry, not an inventory record or technical suitability guarantee. It does not infer composition from names. A catalogue fabric can be requested for a mixed men's/women's enquiry; professional assessment for each garment remains necessary. The legacy per-design audience restrictions are not incorrectly applied to this shared request.

## Validation and reconstruction

- Keep the existing textJSON endpoint, host/origin checks, consent, honeypot,30KB request-size ceiling, design/photo/project allowlists, integer per-design quantities and total9999-garment ceiling.
- Validate every reference/photograph/quantity using the existing selected-suit validator; the shared branch uses a neutral fabric placeholder during row validation, then independently reconstructs the shared preference from server-owned catalogue/colour records.
- Every exact original selected photograph URL, actual design identity, friendly name, quantity and detail link remains in the complete aggregate. Shared requests do not pretend to have separate per-design fabric decisions.
- Fabric/colour names are server-generated, not copied from customer fields. Raw injected `Shared Fabric Preference`, `Preferred Colour`, stock/material claims or legacy fabric labels cannot override them.
- Provider fields include `Shared Fabric Preference`, existing canonical `Fabric Choice`, `Fabric Preference Scope`, selected fabric identity/name/tier where relevant, and preferred colour identity/name/custom description where relevant. Scope and availability wording makes per-garment assessment explicit.
- Existing contacts, delivery location, requested completion date/time and Kigali timezone remain required and preserved. No automatic Standard/Express classification, production acceptance or delivery promise is introduced.
- Existing requests without `fabricPreference` keep their supported per-design validation. No generic unrelated-service validator change was required.

## Provider behavior

The existing Web3Forms provider path remains unchanged. Only positive HTTP/provider success acknowledges acceptance; errors retain the existing uncertainty wording. No private database, file upload, payment or automated WhatsApp action is introduced. Provider acceptance is not proof of business inbox delivery or an accepted order.

## Tests

`tests/shared-fabric-validation.mjs` uses mocked provider calls to check mixed10/28-design enquiries, complete photographs/IDs/quantities, the22 approved colour names plus Other, assistance/own-fabric branches, secure label reconstruction, malformed/stale/oversized inputs, required customer/deadline/consent fields, duplicate/invalid photographs and quantities, provider failures and legacy requests. Existing selected-suit/photo/multi-design validator tests remain regression requirements. No real messages or enquiries are sent.
