# Master website reconciliation register — 25 November 2026

**Status: recovery implemented, tested locally and pushed to staging; Cloudflare reports a successful deployment. Permanent staging verification remains blocked. The full task is not complete.** This register records evidence, not a claim that all requested work has been deployed. Final test/deployment fields are updated only after their actual checks.

## Authority, baseline and recovery protection

Owner instruction: complete accessible-source website recovery, investigation across branches, implementation and deployment on staging only. Follow-up: use newer applicable information/uploads, preserve older files. Main/official publication remains prohibited.

| Reference | Initial verified state |
|---|---|
| Repository | `ninkoniyumutwareemmanuel-lab/mrsewing` |
| Remote Main | `33620fe4dc38ec81905fd2556a19db15f5c06db3` |
| Remote staging branch | `phase1/customer-journey-repairs` at `0acf34dc9c606c0fe283d48177c39ebc7a92b20f` |
| Old local staging workspace | `/workspace/mrsewing`, HEAD `cb245b573156ac7805e0d5ff10accba277222175`, with 348 tracked edits and 177 untracked entries, including caches |
| Preserved old work | `/workspace/recovery/2026-11-25/uncommitted-work.tar.gz`, SHA256 `f862fa76fa79c8637286966d727ec345194ea41232979d777683ac0af76a7c20`; binary patch and all-ref Git bundle alongside it |
| Recovery implementation | `/workspace/mrsewing-recovery`, authorized branch, created from the current remote staging tip without overwriting the old workspace |
| Recoverable staging ref | Local `recovery/staging-before-reconciliation-2026-11-25` |
| Known Cloudflare project | `mrsewing-staging`; permanent intended URL `https://mrsewing-staging.pages.dev/` |
| Initial staging provider evidence | `0acf34dc` → deployment `20c36335-0705-4d1d-b863-34fd5f2dea22`, preview `https://20c36335.mrsewing-staging.pages.dev/`, GitHub check `139210850250` reports success |
| Initial Main provider evidence | `33620fe4` → deployment `ba58d9be-e6b8-4b9d-82a8-d84db57e798e` in the same staging project; not proof of official-domain content |

No force push, branch deletion, Main edit/merge or production setting change is authorized. The older workspace and historical documents remain recoverable.

## Sources investigated and limits

- All 26 remote heads, three rollback tags and seven available PR head refs were fetched into audit references. Full available reachable history, local branches, reflogs/stashes, dangling objects and linked production-repair checkout are investigated in the history audit.
- Main is an ancestor of remote staging: staging is 107 commits ahead; Main has zero unique commits relative to that starting staging tip. Ancestry does not establish feature correctness; Main-based resets intentionally superseded some prior designs and omitted other architecture.
- Public GitHub branch/PR/issue/release/Actions/check pages were read. The captured five Actions listing pages expose 125 run records, including failures and later corrections. Public metadata/step status is distinct from inaccessible full raw logs/artifact downloads.
- Branch-tip deployment checks were inspected at 24 unique branch commits (two branch names share one commit). Observed deployment IDs/previews and historical local deployment evidence are recorded separately. These checks do not enumerate account-protected Cloudflare projects/settings.
- Local `/workspace/mrsewing`, linked `/workspace/mrsewing-production-repair`, review reports, screenshots, generated artifacts, attachments, reflogs/stashes and backup evidence were inspected. Ten pasted-text attachments reduce to five unique payloads. `/workspace/library-files` is empty.
- Current instructions, reference snapshots, R59/R61/R63–R67 documents, policy approval note, actual uploaded PDFs, JSON, Python/template/browser/backend source and generated output are compared.
- **Unavailable:** private ChatGPT conversations/Project sources/Library and deleted remote refs not exposed by Git, named original company archives/handbooks not actually present, protected Cloudflare account configuration/security/cache/Workers/logs, full Actions logs/artifacts requiring access, Search Console and physical-device/Safari results. Do not describe these as inspected.

Raw fetched HTML can contain transient GitHub metadata and stays outside the public repository. Only sanitized evidence belongs here.

## Significant change register

| Change/source | Latest applicable evidence | Initial classification | Reconciliation decision |
|---|---|---|---|
| R35–R50 suits, pricing/benefits, selection/share, 120-second browsing/24-hour Express recovery, quotation framework | Historical owner directions; complete release history inherited by Main/staging | Approved and implemented; functional regressions require current tests | Preserve exact design/photo/quantity/state and service exceptions; no wholesale older-tree merge |
| R51–R54 universal Showroom, source map, quotation-first service presentation, media/PDF preparation | Older staging commits `749b21d`, `812aaca`, `cb245b5`; preserved dirty R54 | Some superseded, some architectural work omitted by later Main-based reset | Recover valid capabilities individually; use newer `/collections/` architecture and current designs, not an obsolete competing gallery |
| R55–R58 Terms/fullscreen/home preservation/restoration | Remote work/release/backup branches and decision docs | Terms improvements reintegrated; multiple homepage iterations superseded | Preserve latest Main-based R59–R67 presentation and current-effective Terms fallback |
| Direct WhatsApp, current Contact/Privacy/Refund design, opt-in Meta | Main commits/documents 21–22 Nov | Approved, inherited | Preserve direct handoff/manual send and mandatory form consent; do not reinstate old WhatsApp popup or alter live analytics |
| R59/R61/R63/R64 homepage/Showroom/media | Dated owner directives; two source videos, genuine posters/silent assets | Implemented; unsafe audible fallback found | Preserve actual latest appearance and owner-represented repository-media permission; enforce silent validated playback or photo fallback |
| R53 25 image uploads / 22 variant records / grouped families | Actual upload and catalogue, later R61 authorization, confirmed Burgundy image12 | Metadata prepared; placement held; obsolete rights/correction blockers | Preserve names/IDs/original files/grouping; correct superseded blockers without publishing every unplaced design |
| R65 quotation/booking modals | Latest dated owner approval | Implemented | Preserve existing shared forms and provider; test actual modal/iframe navigation |
| R66 SEO/canonicals/legacy redirects | Latest dated SEO repairs and standing preservation rule | Implemented | Preserve production canonical intent and staging noindex; verify entire current route set |
| R67 services hub | Approved 23 Nov quick facts, process/fabric cards, two categories/four services | Implemented; some facts independently duplicated | Preserve design and service scopes; centralize exact approved wording |
| Seven-collection text-first Fabric Guide | `291a1567`, `b4210fe2`, owner's latest specification | Approved, partially implemented | Repair quotation selection bypass of new catalogue/legacy hidden illustrations; preserve fabric/pattern/colour and all selected garments |
| About identity/customer commitment | `143fb019`, `3248e01d`, `f3b621c7` | Approved and implemented | New wording is also in template, so regeneration is not a lost design; preserve and test |
| Standard payment exception / refunds | `55cef7cc`, dated 25 Nov note and current explicit owner constraints | Approved operational wording already partially centralized | Preserve three-calendar-day individually approved Standard-only exception, verified receipt/suspension/reassessment; no automatic cancellation/forfeiture |
| Uploaded Terms filename versus actual document | `bc3c62cc`, `a039e70a`, `0acf34dc`; actual PDF full text/metadata | Conflicting identity; exact approved 1.1 cannot be verified | Newest upload is actual 1.2, six pages/20 sections; show only correctly labelled staging review under owner's latest-upload direction, preserve 1.0/current consent, no official activation |
| PDF importer CI | Workflow run `45615768626`, failed import step; actual normalized-text hash mismatch | Deployed preview exists while verification failed | Keep meaningful verification, separate deliberate document review/import from routine build, never fake an expected checksum |
| Generated-commit automation | Existing workflow checked out moving branch and pushed generated changes | Unsafe race/maintenance risk | Event-SHA checkout, contents-read, no persisted credentials or auto-commit/push; developer commits verified generated output |
| Permanent staging address | Preview success for both Main/development in one project | Unable to verify actual served commit/configuration | Requires direct HTTP/browser and Cloudflare settings access; preview URL alone is insufficient |

## Confirmed technical causes versus hypotheses

Confirmed: old local workspace was behind newer remote decisions; the latest routine CI attempted to import an incompatible PDF and failed; preview deployment success was independent of that failed CI; the new Fabric Guide's selected-design mode routed back to the legacy guide; original-audio video fallback could hide missing silent assets; multiple business facts were independently hardcoded. An auto-generated push over a moving branch was a verified risk in workflow code, not proof a particular customer change was overwritten.

Unconfirmed: the exact production branch/build-output setting or cached commit served at the permanent staging domain. Both Main and development previews in one Pages project make branch/promotion configuration an important check, but do not prove its value. Network CONNECT403 is an environment restriction, not a diagnosis of the origin server. Google indexing delays have no newly established cause.

## Tests, repairs and deployment evidence

Results and exact changed files are filled after the integrated build and browser checks. Initial local `python scripts/build_site.py` passed at `0acf34dc`; this did not validate new selection behavior or prove deployed content. Initial relevant backend tests found a clock-dependent test fixture and an obsolete 21-versus-26 enquiry count; scoped test fixes preserve current security/publication checks.

- Final staging implementation commit: pending.
- Final provider deployment ID/status: pending.
- Actual permanent staging served commit/content: **NOT VERIFIED — network/account access blocked**.
- Final Main recheck: pending; no Main changes made.
- Official website: no deployment/settings change performed; actual served content cannot currently be checked.

See [implementation brief](RECOVERY_IMPLEMENTATION_BRIEF_2026-11-25.md), [source map](WEBSITE_SOURCE_MAP.md), [staging workflow](STAGING_DEVELOPMENT_WORKFLOW.md) and scoped recovery reports. This register must be updated with actual outcomes before final reporting; do not convert “pending” into “pass” by inference.

## Detailed evidence files

[Full branch/feature audit](reconciliation/2026-11-25/history-audit.md), [machine-readable history register](reconciliation/2026-11-25/history-audit.json), [local workspace/source inventory](reconciliation/2026-11-25/workspace-audit.json), and [observed Cloudflare deployment references](reconciliation/2026-11-25/cloudflare-observed-deployments.json) preserve commit-by-commit evidence and limitations. New findings and final delivery evidence supplement rather than rewrite the initial baseline.

## Implemented recovery and final local test results

- Seven text-first fabric collections now work in the selected-design journey as well as standalone browsing. The central catalogue has 26 styles, 17 patterns and 50 illustrative colour preferences; supplier reports remain clearly unverified as stock/composition. Exact photographs, individual quantities, shared fabric/pattern/colour and contact drafts survive editing.
- The existing shared selection component now loads on the central Showroom and treats active Showroom browsing as part of the permitted area. The ordinary 120-second expiry and separate 24-hour Express recovery remain intact.
- Legacy Showroom, Why Choose and Happy Customers destinations are recovered through equivalent source-built pages/aliases; legacy design links preserve validated photograph/service context. No duplicate gallery or form was created.
- Homepage playback is silent-only, hash/track/poster validated, with approved-photo fallback. R61 owner-represented permission and R53 original photographs/IDs/families are preserved; 22 prepared designs remain unpublished until deliberate reviewed placement, rather than falsely awaiting repeated owner permission.
- Shared payment/refund/exception facts and FAQ/search/schema projections are reconciled. Quotation-first public tariff presentation is restored; approved surcharge/payment/benefit disclosure and internal prices/Shop/individual quotation calculations remain intact.
- The newest actual PDF is Version 1.2, six pages/20 sections, staged under its true review status per the owner's latest-upload direction. All old Version 1.0 bytes/pages and current contractual consent remain preserved. Exact 14-section approved Version 1.1 could not be independently retrieved; no fake equivalence or official effective date was recorded.
- CI now verifies the event commit without generated pushes or automatic PDF activation. Local QA/dependency output is explicitly excluded from website image inventory; every real website image still requires registration, proven in isolated fixtures.
- A staging-only Pages middleware denies internal source/data paths while preserving public assets/PDFs, Shop, forms and APIs. Its local mocked test does not establish deployed enforcement, and the public Git repository/history is not made private by this boundary.

Actual checks: full site generation and `--check`; Python compilation/JavaScript syntax/whitespace; 25 existing/recovery source, document, SEO, sitemap, media, Shop and mocked backend checks; additional staging-source-boundary and rendered-link/FAQ-anchor checks. The clock-sensitive missing-key test and obsolete 21-versus-26 Shop preview count were corrected without weakening validation. Early failures from post-test screenshots entering the image scan, an obsolete permission-hold count and a sandbox child-process restriction were diagnosed and rerun after appropriate scoped corrections. Final results must be read from the linked test evidence rather than the initial failed logs.

Local Chromium evidence covers 320/390/768/1440px. Fabric tests visit all seven collections, verify no fabric photos/simulated canvases, select Wool/Tweed/Herringbone/Navy and edit to Burgundy without losing designs/contact information. The existing home/hub and PDF suites pass at all four widths; the PDF suite verifies six pages, scroll/zoom/close and identical downloaded bytes. The journey suite passes all ten scenarios, including ten mixed designs/13 garments, actual image decoding, multipart/direct WhatsApp/native/copy fallbacks, mandatory fields/consent, provider failure/retry/duplicate protection, ordinary expiry/Back/Forward, 24-hour Express recovery, Special Tailoring, booking, refund review and FAQ search. No real messages, calls, payments or enquiries were sent.

Screenshots and actual JSON/log evidence are kept under `/workspace/recovery/2026-11-25/` and `/workspace/artifacts/recovery-2026-11-25/`; the final sanitized test index is also retained in `docs/reconciliation/2026-11-25/`. Browser checks are local Chromium, not physical-device, Safari, remote-origin performance or complete WCAG certification.

## Additional hosting and automation verification

Cloudflare's local Wrangler4.51 compiler successfully built the complete Pages Functions worker, including the staging source boundary. A local Pages server parsed51redirects and2host-specificheader rules. Eight synthetic-Host GET checks verified staging internal-price JSON404/noindex, publicPDF/service200/noindex and API405withoutsubmission, with production-host simulation unchanged. These are **local hosting tests**, not calls to the official website or proof of deployed behavior.

CI verifies committed silent video/poster assets instead of regenerating platform-dependent FFmpeg/JPEG bytes on every push. Explicit regeneration remains a reviewed operation with updated hashes. The build excludes only ignored local QA/dependency roots from media inventory; isolated fixtures prove an unregistered website image still fails. Existing workflow browser tests now use portable Playwright/system-browser selection and artifact paths, not this particular workspace's absolute tooling directories.

## Final accessibility and preservation checks

The broad sweep completed **212 page/width visits across 53 representative routes** at 320,390,768,1440px, with no horizontal overflow, JavaScript errors or missing local responses. Three explicit compatibility/design-context/PDF interactions passed. Four main-content axe scans (Home, hub, Fabric Guide, FAQ) are clear after fixing the four gold service-button labels' contrast in scoped hub CSS. A focused four-width hub recheck confirmed the fix. This is not a whole-site WCAG certification; the documented uninterrupted OFFER motion limitation remains.

The final source/output inventory has305HTML files and60forms, with zero missing local link/resource targets. Current approved suit/tuxedo internal price files, Shop product records and the production public-API routing configuration remain byte-unchanged from the initial remote staging commit. Main has not been edited or pushed. No new stock, fabric composition, paid service, private-recording feature or payment integration was activated.

## Fragment and legacy fallback repair

The final fragment audit also reconciled FAQ source destinations dropped by the R67 hub reorganization: fabric, timing and quotation guidance link to their current headings; cleaning/gift benefits to `/benefits/#6`; transport to `/delivery-and-collection/#1`. Answers and business rules are unchanged. The legacy Happy Customers root fallback now shares its source-built alias, preventing clean-URL generation from restoring the obsolete held placeholder. An unused legacy footer fragment's old modal link now opens the existing booking route. `tests/recovery_links.py` verifies actual rendered anchors and FAQ source mappings, rather than silently accepting missing fragments.

FAQ contractual source links now point explicitly to the preserved current Terms route, rather than anchors on the not-yet-effective PDF review reader. Fabric links use the text-first guide’s current collection anchors. No approved payment or benefit condition was changed by these link repairs.

## Staging publication checkpoint

The tested recovery implementation was committed and normally pushed to `phase1/customer-journey-repairs` as **800e23e4e5f64f368fb0f5e72dd3861d39b3f7de**. All314source/generated/document/test/evidence files are listed in the changed-file register. No force push or Main update occurred. A subsequent documentation/CI follow-up retains the same tested application and makes the checkout complete enough for preservation tests to read the recorded `0acf34dc` historical baseline; a default shallow checkout cannot supply that evidence. Deployment/provider results and permanent-domain verification are recorded separately after observation.

## Deployment result and final unresolved boundary

Reviewed staging revision **ea945d933855d0fc46d3929e1879e17d44d95ec2** was pushed normally. Cloudflare check [139408608160](https://github.com/ninkoniyumutwareemmanuel-lab/mrsewing/runs/139408608160) reports **Deploy successful** for project `mrsewing-staging`, deployment **90b6eb6c-1863-4957-ad5d-e00e56b0327f**, preview **https://90b6eb6c.mrsewing-staging.pages.dev/**. The application is the tested recovery from800e23e4; the later change makes its historical preservation baseline available to CI. A following documentation/CI-only commit records this receipt and avoids unnecessary package-index updates when FFmpeg/Poppler are already installed. The branch's final immutable tip is visible in Git and the owner handoff; a file cannot contain its own commit hash.

The separate Terms workflow at800e23e4 passed ([45671537411](https://github.com/ninkoniyumutwareemmanuel-lab/mrsewing/actions/runs/45671537411)). The first full recovery run was canceled by the newer same-branch run, not reported as passing. The newer full workflow was observed in progress at package setup; its final outcome must be checked separately. Local27checks, generation/check, browser suites and local Pages compilation are actual passes; they are not substituted for a remote CI result.

Fresh post-deployment HTTP attempts to the permanent staging root/Terms, exact preview and official root all failed at the managed proxy with CONNECT403. Actual Chromium390/1440attempts to permanent Home and deployed Terms failed with `ERR_TUNNEL_CONNECTION_FAILED`. **No deployed-origin rendering, final permanent served commit, cache behavior or branch/build-output setting is claimed verified.** These results establish an environment access limitation, not a Cloudflare origin failure or proof that the permanent site is stale.

Remote Main was re-read after staging publication and remains **33620fe4dc38ec81905fd2556a19db15f5c06db3**. No Main merge/push, production deployment, official-domain setting or production secret change occurred. The official website's actual served content could not be independently checked.

### To finish the infrastructure portion

Allow the required hostnames in this Cloud environment: `mrsewing-staging.pages.dev`, `*.mrsewing-staging.pages.dev`, `mrsewingfashion.com`, `www.mrsewingfashion.com`, `api.cloudflare.com`, `api.github.com`. Provide an authorized Cloudflare Pages account connection/read permission for `mrsewing-staging`, with staging-scoped edit permission only if a verified setting correction is necessary. Do not paste credentials into source or commands.

Inspect the staging project's connected repository, intended production branch `phase1/customer-journey-repairs`, latest production deployment and actual generated output/build command. Do not assume an incorrect value: current settings remain inaccessible. Preserve the existing `main.mrsewing-staging.pages.dev` production enquiry runtime and any official custom-domain dependency. Then open the permanent URL on mobile and desktop, compare exact deployed content/commit, verify host-specific noindex, all repaired journeys and source-boundary responses. The precise owner steps are in [the staging workflow](STAGING_DEVELOPMENT_WORKFLOW.md).

### Important review links

- Permanent intended staging: https://mrsewing-staging.pages.dev/
- Verified provider preview reference: https://90b6eb6c.mrsewing-staging.pages.dev/
- Main services hub: https://mrsewing-staging.pages.dev/services/custom-tailoring/
- Showroom: https://mrsewing-staging.pages.dev/collections/
- Fabric Guide: https://mrsewing-staging.pages.dev/guides/fabrics/
- PDF reader: https://mrsewing-staging.pages.dev/terms-and-conditions/
- Quotation: https://mrsewing-staging.pages.dev/request/

The links use real implemented routes. Their deployed rendering remains unverified here. Exact files, source/approval/branch matrix, tests and deployment JSON are in [the dated evidence directory](reconciliation/2026-11-25/). Continue development from the remote reconciled staging baseline, not the old dirty R54 tree. Production publication requires a new separate owner instruction.
