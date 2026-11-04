# Custom Tailoring & Suits — staging owner review

Date: 4 November 2026. Branch: `phase1/customer-journey-repairs`.

## Review URLs

- Landing: https://mrsewing-staging.pages.dev/services/custom-tailoring/
- Standard Order: https://mrsewing-staging.pages.dev/services/custom-tailoring/standard-order/
- Special Order: https://mrsewing-staging.pages.dev/services/custom-tailoring/special-order/

Staging publication is authorised; production publication is not. Exact pushed SHA and deployment visibility are supplied in the completion message. A successful GitHub push alone does not prove Cloudflare publication.

## Completed functionality

**PASS — landing page:** premium black/gold, mobile-first typography and spacing; exact requested H1, supporting headline and introduction; concise tailoring explanation; two equally sized Standard/Special cards with the requested descriptions/actions; one help section with one Customer Support link; six-step process consistent with the approved homepage and tailored to garment production/fittings. Choosing a pathway does not confirm an order or collect payment.

**PASS — Standard Order:** a separate chooser contains exactly Men's Suits and Women's Suits, using the two existing owner-approved representative tailoring photographs. It links to existing `/mensuits/` and `/womensuits/` galleries rather than inventing galleries or products. Existing publication data contains 46 men's and eight women's entries; no classification, photograph, product reference, price or stock claim was added. Gallery design requests already carry the selected reference and design URL into the existing WhatsApp enquiry. Tests observed references MS-045 and MS-129 without sending messages. Galleries contain design references, not a blanket claim of completed customer work. The landing/chooser introduce no new prices or stock availability claims; existing gallery content/pricing was not rewritten in this task.

**PASS — Special Order text enquiry:** its independent route opens directly, without requiring Men's/Women's browsing. Fields cover name, optional email, phone, country/location, garment/design description, quantity, optional fabric/date/additional requirements and three measurement-readiness choices. “Not sure yet” is the default; measurements are not a prerequisite. Existing form action/public integration is reused, with a distinct Special Order subject/pathway and a clear acknowledgement only after an HTTP-success response with explicit provider success. An enquiry never confirms feasibility, payment, a production order or completion date.

**PREPARED, NOT ACTIVE — online uploads:** owner explicitly confirmed no upload endpoint is approved. A labelled disabled file control is prepared outside the submission form, with no name or file-submission code. The page plainly says no files are attached. Reference sharing can be arranged using the existing WhatsApp link. No file selection or upload simulation occurred. Server file validation, limits, private storage, scanning, retention and actual uploads remain future work requiring approval. This is not represented as a working upload feature.

**NOT TESTED — real email delivery:** all automated form submissions were intercepted. Existing provider infrastructure is reused, but actual new-subject delivery/receipt and provider-admin settings were not tested. No real customer data, message or file was sent.

## Approved homepage protection

Approved visual baseline: **`c17639947d79f988bec3a72cd95a4bdb44a4fb74`**.

Recorded before service implementation in `docs/homepage-approved-baseline.json`, with 20 protected source/output/configuration hashes and screenshot references. Homepage output, all sections/copy, photographs, header/footer appearance, four categories, carousel and forms are unchanged. No homepage source or generated asset is included in this change set.

**PASS — source regression:** all 20 hashes match after the full production build. Homepage SEO data, business data, logo/media configuration, scripts and builder inputs remain unchanged. Shared site/header/footer/navigation source is unchanged. The SEO helper only adds noindex decisions for the two new service workflow URLs; it does not change homepage metadata.

**PASS — pixel comparison:** full-page 390px and 1440px screenshots have identical dimensions and zero differing pixels against the approved-baseline captures. Evidence: `homepage-visual-comparison.json`, `approved-homepage-*.png`, `homepage-after-*.png`.

The new service pages reuse the approved homepage header/footer **at build time**, with the current service marked active. They do not modify those components or execute homepage enquiry/carousel scripts. Their own stylesheet scopes the new layout to service-page classes.

## Build, functionality and accessibility tests

| Check | Result | Evidence / limitation |
| --- | --- | --- |
| Production build and full generated consistency check | PASS | `scripts/build_site.py` and `--check`; no new Python/runtime dependency. |
| Static Python suites | PASS | All 13 existing suites. |
| New service browser suite | PASS | Three pages × nine widths: 320, 360, 390, 430, 768, 1024, 1100, 1280, 1440px; no horizontal overflow, correct labels/routes, keyboard disclosures and responsive cards. |
| Existing gallery/design-reference handoff | PASS | Both populated galleries reached; valid reference and detail URL observed in the existing enquiry link. No order/payment action or real WhatsApp message. |
| Special form validation | PASS | Required fields, invalid phone, quantity minimum, trimmed design description and consent tested; sensible optional fields and undecided measurements allowed. |
| Special form success/error handling | PASS | Confirmed success, provider rejection, false success, malformed response, HTTP 500, network failure, duplicate submission, timeout and honeypot. Failed submissions retain entered text and never display success. |
| Upload controls | PASS for disabled state | Control disabled, unnamed and outside the text form; payload explicitly states no files attached. No actual or simulated uploads; file validation/storage/delivery NOT TESTED and not implemented. |
| No-JavaScript fallback | PASS | Landing/Standard navigation remains functional; Special submit remains disabled and the fallback directs to Customer Support. |
| Local links/anchors/schema | PASS | All three pages' local destinations and fragments resolve; JSON-LD parses and includes appropriate WebPage/BreadcrumbList/Service data. |
| Homepage browser regressions | PASS | Navigation/support corrections, support/quotation success and error paths, exact four-second carousel including Pixel 7/iPhone 13 Chromium touch emulation, and homepage structural/no-JS suite. |
| Cross-page regressions | PASS | Customer-journey and final-v2 suites. The old custom-service generic three-step/single-enquiry expectations were replaced with assertions for the authorised six-step, two-path service page. Other page expectations remain. |
| JavaScript syntax / whitespace | PASS | `node --check` on new source/generated scripts and tests; `git diff --check`. No configured TypeScript or ESLint task exists. |
| Automated WCAG 2/2.1/2.2 A/AA | PASS | Axe at 390/1440px on all three pages: zero reported violations. Incomplete/manual checks are saved in JSON; this is not a full accessibility certification. |
| Actual screen reader / Safari / Firefox / Edge / physical devices | NOT TESTED | Only installed Chromium 155 was available. Device-name results are emulation, not real Android/iOS or Safari. |
| Actual public staging rendering / TLS / mailbox receipt | NOT TESTED | Outbound staging/provider access restrictions prevent verification. Local screenshots are not claimed as deployed screenshots. |

Browser suites run: `custom-tailoring.spec.cjs`, `navigation-support-corrections.spec.cjs`, `support-refinements.spec.cjs`, `order-carousel.spec.cjs`, `homepage.spec.cjs`, `customer-journey.spec.cjs`, `final-v2.spec.cjs`.

## Performance

**PASS — measured landing-page laboratory runs**, Lighthouse 13.6.0 against localhost; default simulated mobile/desktop throttling. One final run per profile, not field data or a 75th-percentile result.

| Metric | Mobile lab | Desktop lab |
| --- | --- | --- |
| Performance / Accessibility / Best Practices / SEO | 100 / 100 / 100 / 100 | 100 / 100 / 100 / 100 |
| LCP | 1.05 s | 0.28 s |
| FCP | 1.05 s | 0.28 s |
| CLS | 0 | 0 |
| Total Blocking Time | 0 ms | 0 ms |
| Initial measured transfer | 113.3 KiB | 106.0 KiB |

INP and real-user Core Web Vitals are unavailable; TBT is not INP. Workflow pages have responsive/functional/axe coverage, not separate Lighthouse performance runs. No new remote font, icon library, tracking script or application framework is introduced. Existing imagery is responsive/lazy; the landing is primarily typography and has no oversized new hero image.

## SEO and routing

- Landing retains the existing canonical route `/services/custom-tailoring/`, now with unique title **Custom Tailoring & Suits in Kigali | Mr Sewing Fashion**, accurate unique description, one H1, Service/WebPage/BreadcrumbList JSON-LD, Open Graph/Twitter metadata and existing logo preview.
- Standard and Special workflows have unique metadata and self-referencing production canonicals. They are deliberately `noindex, follow` ordering/assessment utilities, avoiding competing thin search landing pages. They are discoverable through real HTML links, but are not added as indexable sitemap pages.
- Existing 160-route canonical sitemap, robots, redirects and staging noindex headers remain unchanged; the already-listed service landing stays discoverable. No search volume, ranking or traffic claim is made. Homepage metadata remains byte-identical.
- Existing CMT/sketch/standard legacy aliases already pointed to the same tailoring landing. Their six generated `.html`/directory copies regenerate to the new service content while retaining canonical/noindex/redirect handling; they are not new unrelated service pages.
- All other service, gallery, project and information page outputs remain unchanged.

## Policy and business accuracy

The owner supplied the Standard = website design / Special = customer reference distinction, and explicitly authorised the text-only fallback and disabled upload preparation. The page follows those instructions without changing the wider Special Orders policy.

**NEEDS OWNER VERIFICATION:** Master Operating Handbook V8, specifically its latest dated approved sections and applicable later approved addenda, is still absent from the accessible repository/attachments. Exact international/Special Order payment conditions, fabric/feasibility rules, delivery and refund terms cannot be independently reconciled against it. No percentages, deadlines, fabric availability, guarantees or shipping charges are invented. The new page asks customers to confirm applicable terms in their quotation. Existing policy pages are linked and untouched; their full current-handbook reconciliation remains pending.

## Upload investigation

See `docs/custom-tailoring-upload-options.md` for available options, official-source Cloudflare USD pricing references, security requirements, costs that remain unverified, and recommendation. Current text workflow has no new infrastructure purchase. No upload provider or storage account was purchased/configured, no customer files were exposed and no production settings were changed.

Recommended next decision: keep text enquiries active and uploads disabled for owner review. For later uploads, compare documented existing-provider attachment entitlement against a private R2/Worker design. File limits, retention, staff access, anti-abuse controls and a real end-to-end upload/delivery test require separate review before activation.

## Files changed

New source templates: `_templates/custom-tailoring-page.html`, `custom-tailoring-landing.html`, `custom-tailoring-standard.html`, `custom-tailoring-special.html`, `custom-tailoring.css`, `custom-tailoring.js`.

Builders: new `scripts/custom_tailoring.py`; targeted updates to `scripts/build_journey.py` and `scripts/site_seo.py`.

Generated service output: `services/custom-tailoring/index.html`, `services/custom-tailoring/standard-order/index.html`, `services/custom-tailoring/special-order/index.html`, `assets/custom-tailoring.css`, `assets/custom-tailoring.js`; existing `service-standard`, `service-sketches`, `service-cmt` `.html` and directory aliases.

Tests/docs: `tests/custom-tailoring.spec.cjs`, `tests/customer-journey.spec.cjs`, `docs/homepage-approved-baseline.json`, `docs/custom-tailoring-upload-options.md`, this review report.

## Evidence and stop point

Evidence: `/workspace/artifacts/custom-tailoring/` — `landing-390.png` / `landing-1440.png`, `standard-order-*`, `special-order-*`, approved and after-homepage screenshots, `test-evidence.json`, pixel comparison, Lighthouse HTML/JSON, official Cloudflare pricing source and `logs/`.

The corrected mobile process layout was inspected in actual screenshots; all six steps remain readable without the inherited homepage grid squeezing text. New page screenshots are ready for owner visual review, not declared approved on the owner's behalf.

Production/main/domain/hosting settings remain untouched. Stop after the authorised staging push and verification attempt; do not activate uploads, rebuild other pages or publish to production without further owner instruction.
