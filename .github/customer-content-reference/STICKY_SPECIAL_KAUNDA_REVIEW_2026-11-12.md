# R38 — Sticky offer, Special Tailoring and Kaunda review

## Result and scope

Three UI refinements implemented and tested on phase1/customer-journey-repairs. Kaunda restoration remains blocked by missing image publication approval; no empty category, invented reference, unrelated photograph or permission bypass was added. Baseline0ab19a14eb0880b17cd7f8fe803b65af6bd515f6; main4d972f29417fa60366ebdb6348e1599208f6ae08 protected. Staging only; no mainpush/merge, production deployment/settings or payment changes.

## Implemented

- Existing OFFER bar now lives inside the same sticky #site-header wrapper, directly after the unchanged brand header. Both remain together on scroll. ResizeObserver tracks actual combined height and updates page-scoped anchor offsets for responsive/reduced-motion changes. Initial document flow reserves the stack; no duplicate bar. Homepage has no existing announcement and remains byte-identical; no new homepage bar was added.
- Animation90seconds->75seconds, giving20%faster linear right-to-left movement. Same3approved messages, fixedgoldOFFER, no links/buttons/Pause/touch-freeze; reducedmotion/staticfallback and knowncontinuousmotionwithoutuserstopaccessibilitylimitation retained. No full motion-conformance claim.
- Special Tailoring added as third button in hero and bottom navigation, both to /services/custom-tailoring/special-order/. Men's and women's destinations unchanged. Exact owner description under Special Tailoring & Custom Garments near hero. Existing Special Order form remains byte-identical: free-text garment type supports non-suits; standard existing fabric/priority/review/provider/Terms/manualWhatsApp-picture arrangements, no photo uploads/newform/provider path.

## Kaunda source and approval audit — not restored yet

Current collection loader explicitly states: “Existing-public display is not publication permission (owner5Nov§28).” It admits approved-rights records or project-linked photograph permission evidence only. Every historical Kaunda-tagged record fails that permission test. Root owner restriction requires approved photographs and forbids empty or fabricated categories; no unrelated approved western-suit pictures were substituted.

Original historical men sources, all rightsStatusreview_required/provenanceunverified:
- MS029..MS036: /m-kaundasuits1.jpeg through /m-kaundasuits8.jpeg. Files and earlier m-kaundasuits.html association exist; these eight are available for owner image review, not newly approved by this implementation.
- MS120..MS124: /s1.jpeg through /s5.jpeg were historically cross-tagged Kaunda/modern. Visual review shows s1/s2/s4/s5 as western-style/unrelated references; do not use them to fill Kaunda. s3/MS122 is a potential women’s stand-collar garment reference, but currently men-labelled and unapproved. Owner classification and publication confirmation are needed.

No currently approved women's Kaunda design/reference found. Existing approved pool remains20; all existing4men+4women categories and destinations remain unchanged. No empty customer-facing Kaunda category was created. Exact record audit: KAUNDA_ASSET_REVIEW_2026-11-12.json. Local contact sheet /workspace/review/sticky-special-kaunda-2026-11-12/kaunda-source-review.jpg supports concrete owner review; originals unchanged. Owner must identify/approve the images to admit before category restoration can complete. This is an approval/classification dependency, not a missing source file or fabricated product opportunity.

## Preservation

Exact prior ordinary/tuxedo prices, tier benefits, FAQ/payment/family/bulk facts, Fabric Guide, category registry/rights/design records, men's/women's landing files, Special Order generated form, form/selection scripts, Shop/homepage and source images remain unchanged. Brand header/footer markup, hero photograph, title/meta/canonical/page schema unchanged. Target Custom Tailoring and its three existing root/directory redirect aliases are the only customer-page outputs regenerated. Shared-component CSS is inlined only where announcement already rendered; no global style or gallery redesign.

## Tests completed

PASS Chromium320/360/375/390/430/768/1024/1440: header/bar geometry at scroll0/600/1800/3600; bar immediatelybelowbrandheader, stacktop0, room forcontent/nohorizontaloverflow; no overlap offixedOFFERandmessagewindow. Anchor targetsclearcombinedstack, includingreducedmotionheightchanges.75scomputedanimation; nointeractivepromo. Three top and bottomdestinations, mobilemenu, eightmaincontentAxechecks andno pageerrors.

PASS390/1440top+bottomSpecialTailoring->existingSpecialOrder form; fourmockedprovideracceptednon-suitrequests withDress,shirtandcoat freetext, ownfabric andcustomerrequirements. No websitephoto/fileinput, no selectedwebsitephotorequired, preservedSpecialOrderpayload, no realmessages/payments. Existing8collectioncategories/destinations verifiedunchanged; noemptyKaunda.

PASS R37 eightwidth pricing/benefits/guide/FAQ/button/promotion regression afterupdatingintentional3-button/75stestexpectations; all16ordinary+4tuxedoamounts, sourceconsistency/multiplefabricpertier,55-routesitemap,policyarithmetic,27selectedphotomappings/multi-designservervalidation. Full existing selected-design/fabric/quotation browser regression passed: add/remove/qty/refresh/contactdraft, per-designfabrics/return/cancel, exactphotolinks/review/providerfailure+success,7width/shared-pageAxe. No inbox/physicaldeviceSafari claim.

PASS normal fullbuild/parity/PythonJSsyntax/whitespace. Actualdeployedbrowserverification mustbeattempted afterpush and distinguished fromCloudflareproviderstatus. Prior environmentproxyCONNECT403 isnot a website403.

## Remaining limits

- Kaunda approval/classification dependency described above prevents the fourth requested area from being completed safely.
- Continuous noninteractive promotional motion still lacks an on-page user stop mechanism. Reduced-motion supported; full WCAG2.2.2conformance not claimed.
- Original company handbooks remain unavailable; inspected current repository references, image metadata/history and latest owner task.
- Physicalphones/Safari/realinbox/directdeployedvisualchecks are not established by local Chromium/mocked tests; final delivery records network result, exactcommit and CloudflareissuedstagingURL.

No production publication requested; owner reviews staging and supplies specific Kaunda image approval before restoration.
