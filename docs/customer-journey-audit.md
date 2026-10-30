# Customer Journey V1 — pre-implementation audit

Baseline: 08191fde2c1e984206ca40d53fbe99f69ce218da, staging branch only.

- Reusable components: shared header/footer/navigation/CSS, Python static builders,
  Collections V3 registry, optimized picture delivery, clean-URL generator.
- No views.html or views/ exists in this checkout. reviews.html is the photo
  archive; its narrative descriptions are promotional copy, not project evidence.
- No completed-work evidence, per-photo publication permission, approved customer
  identities or approved testimonials are recorded. Collection provenance is
  explicitly unverified. Reusing a published image does not prove consent.
- Preserve existing homepage/legacy photo uses and original bytes; do not expand
  identifiable images into new galleries or stories. Our Work will explain the
  editorial/permission policy and link useful existing destinations. A gated
  project registry/template can publish only after actual evidence is provided.
- The three homepage customer images are h2.jpeg, r7.jpeg and r4.jpeg. No verified
  same-project association or publication-consent record exists for these.
- Hero actions duplicate later actions. Replace only hero buttons with lightweight
  CSS typography; retain hero photo and legacy order-modal compatibility.
- Shared header uses in-page anchors and an unavailable Shop. Legacy header has
  eight different links. Footer omits Our Work/Services. Consolidate six destinations.
- Homepage service cards currently lead to collections, generic galleries or forms.
  Existing services.html has six service routes, with inconsistent/unqualified
  promises. Existing homepage, About, booking-adjustment and measurement guidance
  support men's/women's tailoring, wedding/civil wedding, graduation, alterations,
  fittings and express enquiries. Keep customization/timing subject to confirmation.
- Collection metadata has graduation assignments, no wedding/civil-wedding
  assignments. Do not infer occasions from photographs or review marketing copy.
- V3 galleries still advertise favourites in meta descriptions. Many garment pages
  have duplicate metadata. Root sitemap is manually maintained (27 routes), separate
  from the 111-design sitemap. No unified indexability/redirect generator exists.
- Preserve all existing category/service/photo URLs and images. Add exact permanent
  redirect rules for HTML aliases and views aliases, without wildcard chains.
- No hosting/DNS configuration changes or Search Console submissions are authorized.
  Prepare hostname-specific noindex HTTP headers in static _headers for staging;
  production metadata/sitemaps use only the production origin.


## Final consolidated implementation decisions

The later consolidated owner specification superseded the preliminary category
proposal: there are seven canonical service destinations, with one combined
Custom Tailoring page, a specialized Garment Care section and direct legacy
service redirects. See the current implementation report. Six care candidates
remain unpublished; zero customer stories have sufficient consent/completion
records to publish. No original photos, videos or stable design IDs were deleted.
Competitor browsing was attempted but the Google request was blocked by the
configured outbound proxy (403); no competitor content or prices were used.
