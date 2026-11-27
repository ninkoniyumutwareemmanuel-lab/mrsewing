# Website history and branch reconciliation audit
Investigation25November2026. Read-only source/history audit; no Main or staging implementation changes made by this audit.

Initial Main: `33620fe4dc38ec81905fd2556a19db15f5c06db3`. Initial remote staging: `0acf34dc9c606c0fe283d48177c39ebc7a92b20f`. Original local staging: `cb245b573156ac7805e0d5ff10accba277222175` with saved uncommitted R54 work.

**766 reachable commits,26remote heads,7PR heads,3rollback tags.** Repository is not shallow. Main is the merge-base and ancestor of current staging; staging107commits ahead, Main0uniquecommits,400changed paths. The older local checkout was substantially stale.

## Recovery findings

- No missing Main-only commit needs merging. Source-level changes must still be checked; ancestry alone does not establish latest approval.
- R54–R58 branch ancestry is divergent because Terms-only reconciliation/main-copy work selected effects rather than merging whole old redesigns. R59–R67 are the current homepage/services successors. Do not blindly reapply R54, older rights holds, old WhatsAppTerms popup, or obsolete exactMain-homepage restoration.
- Later owner-approved repository media authorization R61 supersedes prior permission-pending status; actual deliberate publication/classification remains separate. Current two silent clips/posters must remain.
- CurrentMain-approved direct WhatsApp, optional production-only MetaPageView, Privacy, Refund and Contact designs are already inherited. Keep their latest scopes and test protections.
- Seven available PRheads are all public merged PRs. #6 is an open issue recording prior live/staging mismatch, not a missingPR. No published Releases found;three historicalrollback tags remain.
- No stash is present. One retained unreachable commit8bf7c118 is an older customer-reference creation, not a newer policy; reflogs and original bundled history preserve it. No explicit revert/reset commit subject exists, but source-reset effects are evidenced by divergent branches andR58/R59 source ancestry.
- Lost R51/R53 architecture/docs require selective source-map/authority recovery if still applicable; the successor UniversalShowroom is `/collections/`, not a second independent gallery.

## Branch inventory

| Source | Commit | Stage-only / source-only commits | Decision |
| --- | --- | ---: | --- |
| 1 | `f81072a3` | 638 / 0 | Already in staging ancestry; preserve current successors, do not merge an old tip. |
| 111 | `4471e414` | 554 / 0 | Already in staging ancestry; preserve current successors, do not merge an old tip. |
| 2 | `393035da` | 620 / 0 | Already in staging ancestry; preserve current successors, do not merge an old tip. |
| backup/main-before-terms-release-2026-11-22 | `f07e3b38` | 108 / 0 | Already in staging ancestry; preserve current successors, do not merge an old tip. |
| backup/staging-before-main-homepage-recovery-2026-11-22 | `3bcf142d` | 108 / 39 | Historical approved homepage/Terms iterations; compare effects, retain current R59–R67 successors and immutable history; no wholesale merge. |
| backup/staging-before-terms-2026-11-21 | `7f2bda86` | 121 / 5 | Historical media/Meta preparation; production-approved Meta and newer staging media supersede its disabled configuration. |
| backup/staging-before-terms-release-reset-2026-11-22 | `3e0c73b6` | 108 / 41 | Historical approved homepage/Terms iterations; compare effects, retain current R59–R67 successors and immutable history; no wholesale merge. |
| backup/staging-before-v2-stage-a-20261029 | `c58805e3` | 280 / 0 | Already in staging ancestry; preserve current successors, do not merge an old tip. |
| last-section | `25bd65bc` | 673 / 0 | Already in staging ancestry; preserve current successors, do not merge an old tip. |
| last-section2 | `c89a1b09` | 670 / 1 | Superseded October manual homepage HTML; no current-policy authority or missing independent feature identified. |
| last-section3 | `ded517ea` | 664 / 0 | Already in staging ancestry; preserve current successors, do not merge an old tip. |
| main | `33620fe4` | 107 / 0 | Already in staging ancestry; preserve current successors, do not merge an old tip. |
| modula-homepage | `85da5e0c` | 574 / 0 | Already in staging ancestry; preserve current successors, do not merge an old tip. |
| phase1/customer-journey-repairs | `0acf34dc` | 0 / 0 | Already in staging ancestry; preserve current successors, do not merge an old tip. |
| phase2/website-corrections | `2dbd5db9` | 281 / 0 | Already in staging ancestry; preserve current successors, do not merge an old tip. |
| release/terms-reader-only-2026-11-22 | `ce4632b9` | 108 / 4 | Terms effects were selectively released to Main and inherited by staging; branch ancestry differs because of scoped reconciliation. Preserve latest reader instead of merging. |
| review/customer-policy-2026-11-07 | `68bc9c98` | 143 / 0 | Already in staging ancestry; preserve current successors, do not merge an old tip. |
| save1 | `f4b1199c` | 654 / 0 | Already in staging ancestry; preserve current successors, do not merge an old tip. |
| section1 | `f601df16` | 687 / 4 | Superseded October manual homepage HTML; no current-policy authority or missing independent feature identified. |
| section2 | `35c108be` | 683 / 0 | Already in staging ancestry; preserve current successors, do not merge an old tip. |
| section4 | `26309ffb` | 682 / 1 | Superseded October manual homepage HTML; no current-policy authority or missing independent feature identified. |
| work/r55-terms-fullscreen-popup-2026-11-21 | `4d7c2826` | 108 / 20 | Terms effects were selectively released to Main and inherited by staging; branch ancestry differs because of scoped reconciliation. Preserve latest reader instead of merging. |
| work/r56-tailoring-first-homepage-2026-11-21 | `47b5966b` | 108 / 32 | Historical approved homepage/Terms iterations; compare effects, retain current R59–R67 successors and immutable history; no wholesale merge. |
| work/r57-preserve-existing-homepage-2026-11-21 | `3bcf142d` | 108 / 39 | Historical approved homepage/Terms iterations; compare effects, retain current R59–R67 successors and immutable history; no wholesale merge. |
| work/r58-restore-main-homepage-2026-11-22 | `3e0c73b6` | 108 / 41 | Historical approved homepage/Terms iterations; compare effects, retain current R59–R67 successors and immutable history; no wholesale merge. |
| work/terms-pdf-main-base-2026-11-21 | `c727540b` | 108 / 11 | Terms effects were selectively released to Main and inherited by staging; branch ancestry differs because of scoped reconciliation. Preserve latest reader instead of merging. |
| PR#1 | `db92d244` | 286 / 0 | Already in staging ancestry; preserve current successors, do not merge an old tip. |
| PR#2 | `2dbd5db9` | 281 / 0 | Already in staging ancestry; preserve current successors, do not merge an old tip. |
| PR#3 | `171ba92c` | 266 / 0 | Already in staging ancestry; preserve current successors, do not merge an old tip. |
| PR#4 | `81efee62` | 238 / 0 | Already in staging ancestry; preserve current successors, do not merge an old tip. |
| PR#5 | `501ccc16` | 156 / 0 | Already in staging ancestry; preserve current successors, do not merge an old tip. |
| PR#7 | `b6e4d1bc` | 154 / 0 | Already in staging ancestry; preserve current successors, do not merge an old tip. |
| PR#8 | `ce4632b9` | 108 / 4 | Historical branch; requires effect comparison rather than indiscriminate merge. |
| tag:rollback/production-before-parity-repair-2026-11-06 | `a2ae98f5` | 155 / 0 | Already in staging ancestry; preserve current successors, do not merge an old tip. |
| tag:rollback/production-before-photo-update-2026-11-07 | `7daf8466` | 148 / 0 | Already in staging ancestry; preserve current successors, do not merge an old tip. |
| tag:rollback/production-before-v2-2026-11-06 | `967401e4` | 176 / 0 | Already in staging ancestry; preserve current successors, do not merge an old tip. |

## Significant feature/decision register

| ID / area | Source commits | Status | Evidence and recovery decision |
| --- | --- | --- | --- |
| R01-R34 — Earlier navigation, service forms, FAQ, Shop preview, genuine work and policy system | `171ba92c` `81efee62` `501ccc16` `84b33d61` | Approved and implemented | Versioned references and merged PR1–5/7; current instruction preserves approved work. Present in both branch ancestry. Preserve forms, security and later scoped policies; no old branch merge. |
| R35-R49 — Suit pricing/benefits, Kaunda8,75s OFFER,category/detail,sharing,120s expiry,sharedfabric/colour,Suit/Special forms,24hExpress | `09fe4f70` `0a446ad2` `0ab19a14` `7707c0f6` `4c9dd3cd` `77855579` `3fd899e8` `ff750462` `ce312f68` `663c8f5d` `e4951002` | Approved and implemented | R35–R49 owner references and release records. Included on Main and staging. Current visible presentation and policies must be tested against later Fabric/Terms changes; preserve underlying identities and quantities. |
| R51-R53 — Single-source architecture, quotation-first public service pricing, universal Showroom, media registry, Terms workflow, new25photos | `749b21d9` `812aaca4` `ce98ee39` `cb245b57` | Approved but partly overwritten/superseded | R51/R52/R53 owner tasks and original checkout docs. Main-derived Terms-only branch discarded some architectural files. R59 implements successor /collections/ Showroom and hub; recover documentation/valid rules selectively rather than a second gallery database or old homepage. Audit any restored public prices against newer scope. |
| R54-LOCAL — Saved R54 redesign and derived-media/order/category/PDF safeguards | `cb245b57` | Approved but uncommitted/incomplete | Original uncommitted work plus R54 owner task; backup snapshot.json. 348 modified tracked paths and177untracked paths preserved in archive and original checkout. Later R59–R67 supersede most presentation/rights controls. Reuse tests/helpers only if current gaps justify them. |
| R54-TERMS — Main-based PDF reader with current-effective Terms consent split | `999ab477` `c4d2f9df` `c727540b` | Approved and implemented | Terms-only work branch and owner follow-up. Effects inherited via released Terms reader. Do not restore R54 separate conflicting Terms system. |
| R55 — Full-screen scrollable genuine PDF page images/zoom/open/download | `f0dcc2a0` `8d1c158c` `4d7c2826` | Approved and implemented | R55 branch notes/tests and PR8. Preserve latest renderer; current v1.1 verification audit controls upgrade. |
| R56 — Short homepage shell | `ff15e1ee` `a84660da` `47b5966b` | Superseded | R56 branch documents; later R57/R58/R59 instructions. Do not recover wholesale; later R59–R67 define current home. |
| R57 — Original homepage preservation with additive highlights | `042d9b8d` `f0e18453` `3bcf142d` | Superseded | R57 branch documentation. Preserve unique useful content via current R60 and current design, not entire old tree. |
| R58 — Restore exact Main homepage | `cf7cc49d` `3e0c73b6` | Superseded | R58 branch documentation then R59 redesign directive. Do not revert present staging homepage to Main; latest R59–R64 control. |
| MAIN-CONTACT — Compact Contact and page-specific Kigali tailoring SEO | `f07e3b38` | Approved and implemented | docs/CONTACT_US_DESIGN_AND_LOCAL_SEO_2026-11-21.md. Already inherited; preserve contacts, workshop, MIC appointment-only distinction and service-specific metadata. |
| MAIN-WHATSAPP — Direct WhatsApp without Terms popup | `ccf9bb12` `a74a5998` | Approved and implemented | docs/WHATSAPP_DIRECT_CHAT_FOOTER_TERMS_2026-11-21.md. Preserve direct WhatsApp manual-send; separate mandatory quotation/booking consent remains. Do not restore earlier R53/R54 WhatsApp Terms gating. |
| MAIN-PIXEL — Opt-in PageView-only Meta/compact cookie bar | `1e15ebc2` `8175509d` `ac4b6c40` `b507a2b5` | Approved and implemented | docs/META_PIXEL_ACTIVATION_2026-11-21.md and COOKIE_BAR_REVISION. Inherited config must remain. Exclude staging/sensitive/query URLs, no Lead/Purchase activation or real analytics calls during tests. |
| MAIN-PRIVACY — Responsive Privacy and correct same-page anchor numbering | `4b18462b` `ab53756c` `698e6a49` | Approved and implemented | docs/PRIVACY_POLICY_DESIGN_RELEASE_2026-11-21.md and CUSTOMER_FRIENDLY_REVISION. Preserve current presentation/disclosures; no unrelated legal rewrite. |
| MAIN-REFUND — Responsive refund review journey | `2a985a3a` | Approved and implemented | docs/REFUND_POLICY_DESIGN_RELEASE_2026-11-21.md. Preserve current UI/provider/consent; reconcile only approved v1.1 policy changes. |
| MAIN-TERMS-RELEASE — Scoped Terms reader release from staging to Main | `48022a6b` `ce4632b9` `33620fe4` | Approved and implemented | Merged PR8 body, 22Nov owner authority. Only Terms was released, not all divergent staging work. Main is ancestor of current stage; no current implementation changes to Main authorized. |
| R59 — Tailoring-first home,hub,exacttwo clothing cards,central /collections/,Backorder wording,ordering | `da803bca` `1e41473b` `b975cbf2` `c179c81a` `65f8d51f` | Approved and implemented | docs/R59_TAILORING_FIRST_STAGING_2026-11-22.md and dated owner directive. Current successor architecture; retain stable existing legacy routes. Missing date data stays unknown; do not fabricate newest dates. |
| R60 — Restored useful home steps/whychoose/order/payment/contact/support | `e7759910` | Approved and implemented | docs/R61_OWNER_MEDIA_AND_TAILORING_HOMEPAGE_2026-11-22.md. Keep unique useful sections and current tailoring-first presentation. |
| R61 — Owner authorization for repository media, two silent videos/posters | `88533130` | Approved and implemented | AGENTS.md R61 and docs/R61_OWNER_MEDIA_AND_TAILORING_HOMEPAGE_2026-11-22.md. Supersedes owner-permission-pending blocker. Does not invent third-party license audit or publish all uncategorized photos. Keep reference/work/shop distinctions. |
| R62 — Inventory generated posters and generate media before full build | `3a6b857c` | Approved and implemented | R61 document R62 correction and commit. Preserve exact technical derived-media inventories; confirm actual build passes. |
| R63 — H1 Professional Tailoring & Custom-Made Clothing,Shop gold header,stackedmobile loopingvisible videos | `866f86d3` `34723bb5` | Approved and implemented | docs/R63_STAGING_HOMEPAGE_PRESENTATION_2026-11-22.md. Current homepage H1 supersedes older R54 headline; keep Kigali in supporting SEO. Silent/offscreen/background/reducedmotion behavior must pass. |
| R64 — Remove visible gallerypause/video names and controls, tap+keyboard pause | `3f75b05b` | Approved and implemented | docs/R64_CLEAN_HOMEPAGE_MOTION_2026-11-22.md. Do not reintroduce R54 visible Pause buttons; retain keyboard/focus/reduced-motion behavior and report accessibility limits honestly. |
| R65 — Existing quotation/consultation forms in native dialog iframes | `a5ac3bdf` `99d731c1` | Approved and implemented | docs/R65_STAGING_FORMS_POPUP_2026-11-22.md. Preserve original route/validation/provider/data/consent and fallback; no duplicate forms. |
| NAV-ABOUT-PICKER — Remove redundant global Services but retain About service picker | `5a2edbbd` `612ad809` `bcaf7247` `2712b745` | Approved and implemented | Commit history and current approved navigation task reports. Keep standalone services-picker-source template; regenerating header must not empty About picker. |
| R66 — 31legacy canonical fallbacks/7core services crawlability/stagingnoindex | `c646a8b2` `cab4e035` `0087e525` `f8a85b03` `c75bb1ed` `6891ea24` | Approved but deployment/Google effect unverified | docs/R66_STAGING_INDEXING_REPAIR_2026-11-23.md. Preserve clean route no-refresh and legacy redirects; HTML refresh is not HTTP301, no indexing guarantee. |
| R67 — Concise services customer guide,quickfacts35%Express,fabricadvice and ownfabric,combinedRepairCareassessed | `4c827c04` `95b74713` `40b5dee8` `72eb3cbd` `68be8381` | Approved and implemented | docs/R67_TAILORING_HUB_CUSTOMER_GUIDE_2026-11-23.md. Keep exact2clothingcards and4servicejourneys, source-backed policy values, estimates not promises. Proposed ownfabricservice contract remains proposal. |
| FABRIC-PREMIUM — 7collections,26styles,17patterns,50colourpreferences | `291a1567` | Approved and implemented | Latest owner25Nov task and catalogue source. Retain central catalogue and collection routes; verify exact counts and quotations with current data. |
| FABRIC-TEXT-FIRST — Remove fabric photos/simulations, provide descriptive text/pattern/colour selection | `b4210fe2` `37049381` | Approved and implemented | Latest owner25Nov task explicitly confirms rejection of simulated previews. Do not recover rejected cloth imagery. Preserve actual supplier evidence privately/accurately without unverified collection assignments. |
| POLICY-V1.1 — 25Novpayment/refund/FAQ guidance | `55cef7cc` | Approved and implemented pending site-wide verification | docs/POLICY_V1_1_OWNER_APPROVAL_2026-11-25.md and latest owner task. Reconcile Standard-only exceptional lower advance,3calendar days,suspension/assessment,35%Express/noexception,no automatic10day cancellation/forfeiture; preserve agreed orders and legal rights. |
| ABOUT-UPDATE — Company identity/customer commitment/service navigation | `143fb019` `3248e01d` `f3b621c7` | Approved and implemented | Commit instructions and latest About source; no independent external registration evidence. Repeated equivalent commits must not duplicate UI; verify final details against approved records. |
| PDF-UPLOAD-RECOVERY — Owner v1.1 uploaded using v1filename, preserved separately then imported | `bc3c62cc` `a039e70a` `0acf34dc` | Approved; verification requires independent evidence | Latest owner25Nov task and exact uploaded/source/registry documents. Preserve1.0 and exactoriginalupload. Do not trust filename/pages/checksum alone; independently verify complete approved14sections/sixpages before reader activation; official effectiveness remains held. |
| BUILD-PATH-FIX — Python template path construction | `94064a1e` | Approved technical repair implemented | Commit and current generator. Verify full clean generation and --check; do not patch generated HTML only. |
| OLDER-MANUAL-HOME — October1page HTML variants | `c89a1b09` `f601df16` `26309ffb` | Superseded | Ancientbranch commits inspected; no current newpolicy approval. Do not merge; latest owner designs supersede these variants. |
| DANGLING-REFERENCE — Earlier customer-reference creation | `8bf7c118` | Superseded duplicate history | Reflog/fsck commit and current datedreference files. No unique newbusiness decision. Preserve recoverability in original repo/backup; do not promote it above later approvals. |

## Public GitHub records

| PR | State | Title | Head |
| --- | --- | --- | --- |
| [8](https://github.com/ninkoniyumutwareemmanuel-lab/mrsewing/pull/8) | merged | Release staging Terms & Conditions reader only (protect existing policies) | `ce4632b9` |
| [7](https://github.com/ninkoniyumutwareemmanuel-lab/mrsewing/pull/7) | merged | Merge pull request #5 from ninkoniyumutwareemmanuel-lab/phase1/custom… | `b6e4d1bc` |
| [5](https://github.com/ninkoniyumutwareemmanuel-lab/mrsewing/pull/5) | merged | Release Mr Sewing Fashion Version 2 to production | `501ccc16` |
| [4](https://github.com/ninkoniyumutwareemmanuel-lab/mrsewing/pull/4) | merged | Publish approved Mr Sewing Fashion Version 1 | `81efee62` |
| [3](https://github.com/ninkoniyumutwareemmanuel-lab/mrsewing/pull/3) | merged | Publish reviewed Mr Sewing website and FAQ help centre | `171ba92c` |
| [2](https://github.com/ninkoniyumutwareemmanuel-lab/mrsewing/pull/2) | merged | Publish Phase 2: site corrections, speed optimizations, AI discovery | `2dbd5db9` |
| [1](https://github.com/ninkoniyumutwareemmanuel-lab/mrsewing/pull/1) | merged | Publish verified SEO, performance and customer journey improvements | `db92d244` |

Issue6 remains open: historical production/staging mismatch is recorded; no currentconfiguration inference follows from thatoldissue. GitHubdiscussions and deployments/environments publicpages return404; no privateconfiguration inspection is claimed.

## Limits and deployment distinction

- Private/deleted remote branches with no available ref cannot be enumerated. Local reflogs/fsck and available PR heads only recover retained history.
- Public metadata is not access to private Actions artifacts/log archives,Cloudflare project settings,ChatGPTLibrary/conversations,private business originals or deleted workspaces.
- PermanentstagingandproductionactualHTTP/renderingblockedby currentenvironmentCONNECT403;nooriginhealthorcacheconclusion.
- Cloudflare publiccheck success on20c36335(stage0acf) andba58d9be(main3362) proves sameproject acceptedbothcommits, not whichproductionbranch/defaultaliasconfigurationisactive.
- Source/effectpresence does not prove currentfunctionalpass ordeployedcustomer visibility. Parent owns actual tests,deployment/settings audit and final register.

## Machine-readable evidence

`history-audit.json` contains all branchSHA/merge-base/counts, source-only commit lists,localrefs,fsck/reflog summary,PR/issue metadata and significantdecisionregister. `branch-inventory.json` and `all-commit-subjects.txt` preserve rawscope evidence. All are outside the publicdeploytree until parent selects sanitized technicaldocumentation.
