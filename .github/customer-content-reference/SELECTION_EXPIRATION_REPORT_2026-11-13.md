# R46 — Selection expiration validation report

Owner decision: 12 November 2026. Implementation resumed 13 November 2026.
Baseline: `ff7504621306976888a69076eed38538219102ec`.
Branch: `phase1/customer-journey-repairs`. Target: **Cloudflare mrsewing-staging only**.
Protected main baseline: `4d972f29417fa60366ebdb6348e1599208f6ae08`.

## Implemented behavior

- Existing floating action and its black-and-gold design are preserved. It appears only with selections in the main Custom Tailoring browsing area, all five men's and four women's categories (including Kaunda), and approved design-detail pages. Other pages hide it.
- `mrsewing-design-session-v1` records a non-personal session ID, status, first `leftAt` and absolute `expiresAt`. The deadline is exactly **120,000 ms** after departure. Outside refresh does not renew it; active permitted browsing does not expire. Entry, reads, continuation, visibility return and history restoration validate persisted state. Expired browsing rows are removed and a tombstone prevents stale URL resurrection.
- Existing browsing rows remain in `mrsewing-design-selections-v1`. Continuing from review to the existing fabric route closes browsing and transfers complete validated rows into a flow in `mrsewing-quotation-selections-v1`. `selectionFlow` identifies quotation snapshots in existing routes; `selectionSession` identifies browsing; explicit `selectionEdit` creates an editable copy without overwriting the original quotation.
- Back/Forward and refresh do not reopen closed browsing. A newly selected design starts a clean browsing session. Different quotation flows and newer browsing remain independent, including after completing a mocked quotation. Closed review history retains its quotation identity. Restored fabric/guide pages reload the same flow snapshot to avoid cached controls contradicting saved preferences.
- Exact photographs, internal identities, quantities and existing per-design fabrics are retained. No new form, provider, fields, pricing, fabric options or customer journey. The complete existing fabric controls/rendering block is byte-identical.
- Sharing retains selections with the existing Terms consent and manual WhatsApp Send. No actual messages or enquiries were sent. Review is outside the browsing area and uses the same grace until continuation.
- Storage denial/quota failures are caught; current-page memory and existing validated packed URLs keep the immediate journey usable. Lifecycle storage contains no names, addresses, phone numbers or enquiry details. Existing separate contact-draft handling is unchanged.

## Tests

PASS: simulated 60-second return, 121-second expiration, exact 120,000-ms deadline, five-minute active browsing, outside/review refresh, stale URLs, Back/Forward and BFCache checks, late continuation rejection, new selection after expiry, mixed categories and sharing return.

PASS: three selected designs/four garments with exact photographs/quantities/own-fabric preferences reach the real existing validator and a mocked provider. Two independent quotation flows and a newer browsing selection survive each other's changes and completion. All nine categories participate in the same selection component.

PASS: mobile/desktop widths **320, 360, 375, 390, 430, 768, 1024 and 1440 px**; floating action fits, remains tappable, has reserved lower-page spacing and introduces no horizontal overflow. Two scoped axe checks pass. Screenshots inspected at 390/1440. No browser errors or missing local responses in the new lifecycle suite.

PASS: malformed storage, complete storage denial and quota-only write failure; no uncaught exceptions. Browser persistence limitations remain below.

PASS: existing R45 selected-suit browser suite, single-design legacy suite, sharing suite and explicit Add/Change/fabric round-trip regression. Mocked server regressions cover single/10/28-design payloads, consent, required contact/deadline fields, exact identities/photos/quantities/fabrics and unrelated forms.

PASS: full static preservation of **293 existing HTML pages** apart from generated asset cache queries and **566 protected files**, including all CSS, photographs, price/benefit data, sharing and provider modules. The generated selection bundle consists of the lifecycle helper, existing selection module and unchanged quotation UI module. Existing detail/gallery/selection/price/benefit guards pass.

PASS: **64 canonical indexable routes** retain titles, descriptions, headings, canonical destinations, image alt attributes, internal-link targets and valid structured data. Sitemap, robots and staging noindex protections are unchanged. No production SEO changes or ranking claims.

Build and generated-output consistency checks pass. The older detail visibility test now uses the general quotation entry during its unrelated-page tour; selected-design continuation is tested separately under the new closed-session contract. The full updated detail suite passes: 27 categorized detail pages at all eight widths, plus scoped floating visibility, sharing and quotation.

## Files and preservation

See [complete changed-file list](SELECTION_EXPIRATION_CHANGED_FILES_2026-11-13.txt). Runtime changes are confined to the lifecycle helper, shared selection integration, generated bundle, generator prefix and asset cache reference. Existing HTML changes only the selection JavaScript version (`staging-r45` to `staging-r46`); CSS stays unchanged. Dated source reference, manifest, changelog, brief, report and regression tests record the owner decision. Earlier snapshots remain untouched.

## Deployment and limitations

This report records local implementation and validation before release. The final owner response supplies the exact pushed commit, Cloudflare deployment status and preview URL after the actual deployment check. Git push/build success alone is not treated as rendered-site verification.

- When browser persistence is unavailable, a persisted cross-navigation expiration/closed-session guarantee cannot be established; no fingerprinting or private tracking fallback is introduced. An immediate quotation can still transport validated selections in its existing URL snapshot.
- WhatsApp, clipboard/native sharing and provider calls are mocked. No actual app delivery or business inbox receipt is claimed.
- The environment's network policy has previously blocked pages.dev access. Attempt the new deployed URL and distinguish provider status from rendered staging verification.
- Existing OFFER motion/accessibility limitations are unchanged and outside this lifetime-only task.
- Main/production settings, code and deployment are outside authorization. Stop after staging for owner review.
