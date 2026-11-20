# R53 — Uploaded homepage video review

Owner corrective instruction and inspection:19November2026. Source upload commit `ce98ee3991a43483357304b5fe9f2f0a83f7ae27`. Branch `phase1/customer-journey-repairs`, staging only. This review completes technical registration; it does not establish rights that the owner did not provide. No original video was changed, re-encoded, moved or deleted.

## Scope, sources and action contract

Read root `AGENTS.md`, the current2026-11-19-02 customer reference/README and unresolved record, `docs/MEDIA_LIBRARY_WORKFLOW.md`, the media validator and existing homepage settings. The latest owner task authorizes inspection/preparation of both named files and explicitly requires usage-rights/publication gates. It does not claim the videos were made by Mr Sewing or provide creator/audio rights evidence. R51/R52's tailoring-first homepage, manual Terms-gated WhatsApp actions, quotation-first services, pricing/policy/consent/provider/SEO settings remain unchanged by this subtask.

The existing two-card showcase is the destination. Active cards continue to open the approved filtered Showroom; no new form or enquiry is created. A pending proposal is recorded in `homepage.pendingVideoShowcase` rather than replacing an active approved media ID with a held item. Actual activation must pass the existing separate rights/classification/poster gates. Existing video markup already uses native controls, muted audio, `preload="none"`, a separate-open fallback and no autoplay, so there is no automatic movement for reduced-motion users. Device-specific native playback/control accessibility is not established by file inspection alone.

## Actual files and technical checks

| File | Actual dimensions | Format | Container duration | File size | Fast start |
| --- | --- | --- | --- | --- | --- |
| `1024X768VIDEO.mp4` |720×1280,9:16portrait|H.264 High / yuv420p,30fps; HE-AAC stereo44.1kHz|22.845578s|3,017,971bytes|Yes; moov offset32 before mdat19895|
| `1024X768black.mp4` |720×1280,9:16portrait|H.264 High / yuv420p,30fps; HE-AAC stereo44.1kHz|21.94s|2,681,007bytes|Yes; moov offset32 before mdat19163|

The filenames' `1024X768` text is **not the actual resolution**. Both are short portrait videos, not landscape1024×768 assets. Container rates are approximately1.06Mbps and0.98Mbps. Existing `preload="none"` avoids fetching two complete videos merely to render the initial page. No heavy player/dependency or paid media service was introduced.

Both complete files were decoded by ffmpeg with no reported errors. Probe data, top-level ISO BMFF box offsets, SHA256 and sample frames are retained in `/workspace/review/r53-video-review/` for the owner/developer's review. ffmpeg success is not a claim that every mobile browser has independently played the deployed assets.

Original SHA256:

- `1024X768VIDEO.mp4`: `787bb40456b856e67995bd3444ffe21bc40ac465c0a0ed9ad671e4f21cb87756`
- `1024X768black.mp4`: `56dfbf5dc08bd27f6965eaa3a7ec6269419a8f107461161b63f2ab47a3a6763a`

## Visual content and truthful classification

Sampled frames from the beginning and at five-second intervals show a light ivory-coloured double-breasted suit on a mannequin in `1024X768VIDEO.mp4`; `1024X768black.mp4` shows a black double-breasted suit on a mannequin. A separate20-second frame confirms the black video's end content. Both are presented in a clothing-store interior with ties/pocket squares.

Both are reviewed as **men's suit reference-video candidates**. Neither may be labelled women's tailoring merely to fit the current men's/women's card layout. The visible store does not establish ownership, creator identity, stock, fabric composition or Mr Sewing manufacture. `sourceOrCreator` remains null and classification is proposed `reference-design`; `metadataApproval` remains false pending the required owner publication/classification review. Audio streams exist; their spoken/music content and rights are not established.

## Registration, posters and exact blockers

Two records now exist in `_data/media-video-records.json`, with actual paths, friendly titles, descriptive alternative text, duration, inspected technical metadata, original hashes and upload-source reference. Both are `publicationStatus: draft`, `usageRights.approved: false`, `metadataApproval.approved: false`. They do not enter the public media projection or Showroom.

Exact poster candidates were extracted at1second into review artifacts outside the public/deployed repository. Each is720×1280PNG; its hash is recorded in `posterPreparation`. `posterMediaId` stays null until the exact poster has real publication permission and a registered approved image record. No unapproved still was added to public assets. Existing approved photograph cards supply the active homepage fallback instead.

The remaining blockers for **each** video are:

1. Explicit usage-rights/publication evidence covering the video, any third-party imagery and its audio.
2. Owner approval of the reviewed reference-video description/classification and exact poster.
3. An approved exact poster media record; the existing published-video validator requires it.

Technical readiness is complete within the supplied permissions; these are publication blockers, not missing files. Do not set flags to true merely to activate the files. The latest corrective instruction explicitly permits holding assets whose rights are unestablished.

## Homepage settings

`_data/media-library-settings.json` retains the active approved men's and women's image IDs and the suitable large genuine-work suit photograph `MEDIA-e3f071d6aa9dd697dde84cd5`. The feature is already sourced from a verified Mr Sewing project, so there is no reason to replace it with an unapproved uploaded reference.

An explicit `homepage.pendingVideoShowcase` proposal names both files, their truthful men's audience and an approved men's image fallback. It does not silently occupy the existing women's slot or bypass validation. Before activation, select an owner-reviewed two-card composition that accurately reflects the two men's videos, or supply a separately approved women's video for a mixed-audience layout.

## Verification status

PASS: ffprobe metadata, full ffmpeg decode for both files, fast-start box inspection, visual frame sampling, hash preservation, JSON parsing and two draft records with explicit blockers. No public video or unapproved poster activation occurred.

Parent implementation performs the integrated build/check, media gates, homepage fallback and mobile/desktop regression tests. Actual rendered staging/provider results are reported separately. No production change is authorized.
