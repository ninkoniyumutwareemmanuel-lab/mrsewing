# Recovery customer-journey browser results — 25 November 2026

**PASS: 10 current-baseline scenarios.** Local Chromium; selected-design review, quotation, booking, refund and FAQ layouts tested at 320, 390, 768 and 1440 pixels. Session lifecycle was exercised at390; Express recovery popup/standalone at1440. Synthetic data only. This is local rendered verification, not a claim of deployed content, WhatsApp delivery, inbox receipt or accepted orders.

Command actually run: `node /workspace/recovery/2026-11-25/journey-browser/harness.cjs` against the localhost8020 server rooted at `/workspace/mrsewing-recovery` (outer executor required because sandbox localhost cannot reach the server). The portable regression is saved in `tests/recovery_journeys.cjs`; it was also actually run as `REVIEW_ARTIFACTS=/workspace/recovery/2026-11-25/journey-browser/portable-run node tests/recovery_journeys.cjs` and passed all10scenarios with zero JavaScript errors or missing local assets. It uses the same assertions, normal repository paths and configurable output/base variables. Launch selects CHROMIUM_BINARY, an existing system Chromium, or the bundled Playwright browser; the no-system-browser branch requires actual CI verification.

| Scenario | Result / evidence |
| --- | --- |
| Ordinary browsing expiration | PASS: mixed selections survive active five-minute browsing, exact120000ms persisted outside timeout,60second return and refresh without renewal,121second expiry,Back/Forward,BFCache event,stale packed URL and fresh selection. |
| Current Universal Showroom | PASS after actual repair: `/collections/` and filtered women’s Showroom retain floating review and active selections after five minutes. First run exposed missing shared selection assets, not just a CSS problem. |
| Quotation handoff | PASS: three exact designs/four garments retained independently; browsing session closes,Back does not restore old floating bar,new browsing selection does not overwrite active quotation. |
| Ten-design sharing | PASS: ten designs across nine men/women categories (including Kaunda),13garments; all ten actual original photographs decoded; exact names/photos/quantities in copy/native/WhatsApp parts; long messages preserve every photo; direct official WhatsApp,manual-send only,no obsolete Terms popup; clipboard/native unavailable/failure fallbacks. |
| Ten-design quotation | PASS: one compact summary,one shared advice preference,no repeated priority/after-hours fields; required contact/date/time/consent validation; actual server validator plus mocked provider failure/retry; all ten exact photo links and quantities/13total in complete payload; duplicate-click suppression; accurate unconfirmed-order acknowledgement. |
| Express24hour recovery | PASS: provisional Express assessment; prepared exact-photo message and mocked official WhatsApp/call;86400000ms expiry; recovery excludes name/phone/email/AdditionalInformation; recover through approved R65 quotation popup and standalone route; empty personal contact fields on recovery; expired recovery unavailable after24hours. |
| Special Tailoring | PASS: independent shirt/quantity/design-description/own-fabric request,no uploads,no suit selections forced,human deadline assessment,same existing selected-request validator/provider pipeline with mocked positive response. |
| Consultation booking | PASS: current alterations/workplace-visit fields,requested date/time,Kigali zone,required consent,review/edit preservation; mocked failure and subsequent positive provider response; duplicate suppression; no automatic appointment confirmation. |
| Refund review | PASS: current review form,reference/requirements/consent,review/edit,data preserved on mocked provider failure,positive mock remains request-for-review rather than refund approval. |
| FAQ | PASS: search at four widths,matching direct answers,anchors visible after click and refresh,empty-search fallback/clear,escaped injection-like input. |

**Zero JavaScript errors and zero missing local assets** in this suite. Three mocked selected-provider calls (two mixed-design attempts plus one Special); four mocked generic-provider calls (booking/refund failure then positive responses). No real external provider request, WhatsApp message, call, order or payment was made.

## First run versus final run

The first run correctly failed the centralShowroom floating action because `/collections/` lacked the shared selection data/controller entirely. The parent fixed the existing renderer/finalizer, then the full suite passed. The first Express assertion expected top-level navigation, while the owner-approved R65 design opens the existing form in an iframe popup. The test was updated to verify that real popup, exact restored selections and the standalone route, retaining24hour/privacy assertions. No application workaround was made for that obsolete test expectation. `first-run-results.json` and `first-run.log` retain the original evidence; final `results.json` and `run.log` show all passes.

## Screenshots and complete fictional payload

Files in this evidence directory: `selected-designs-390.png`, `selected-designs-1440.png`, `quotation-390.png`, `quotation-1440.png`, `booking-390.png`, `booking-1440.png`, `refund-390.png`, `refund-1440.png`, `faq-search-390.png`, `faq-search-1440.png`. `fictional-complete-payload.json` contains the complete synthetic ten-design request and reconstructed provider payload; public form access-key fields were removed from the saved example.

Remaining limits: Chromium only for this focused suite. New Fabric collection/pattern/colour end-to-end testing belongs to the parallel fabric suite. Whole-page visual/accessibility/video/navigation inventory belongs to the technical suite. Physical devices, actual deployed headers/pages,provider inbox delivery and external messaging are not claimed.
