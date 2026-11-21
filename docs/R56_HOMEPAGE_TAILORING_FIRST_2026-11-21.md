# R56 — Tailoring-first homepage implementation brief
Date: 21 November 2026 | Staging-only owner authorisation

## Objective and scope
The homepage, not the rest of the website, becomes a short, visual tailoring-first arrival page. H1: "Professional Tailor in Kigali, Rwanda". The main actions use existing Terms-gated WhatsApp, Universal Showroom `/collections/`, and established `/services/custom-tailoring/`. The primary cards promote Tailoring & Clothing Services and separately verified VIP assistance; Shop remains a normal secondary link. Preserve existing standalone service/quotation/Shop/Terms implementation, API, customer-support form, SEO and live main. Earlier long homepage service/process/programme details remain available from linked service/information pages; original section source remains in Git history and templates, not copied into the new homepage.

## Authoritative media
R53 original 25 WebP reference photos from source commit ce98ee3 (19 Nov 2026 17:32:12 UTC) are restored as MS-152 through MS-173 and newly homepage-authorized by the owner's express statement. See `.github/customer-content-reference/HOMEPAGE_R56_OWNER_PHOTO_RIGHTS_2026-11-21.md`. The owner asserted commercial rights; no independent third-party licence was inspected. The photographs are **Reference Designs**, not established in-house work or Shop products. R53 image12 remains visually Burgundy despite its olive filename. Families are grouped (Sovereign, Admiral, Ivory Heritage) in the central registry, and none of the 22 records are automatically marked published in the Showroom or Shop.

Two prominent portrait media cards currently use those authorized photographs as fallbacks. The existing two R53 videos remain draft/held and are not emitted to public markup until explicit applicable video publication, visual metadata, poster and verified no-audio derivative gates pass. The sources and technical review record are preserved. Only if all gates pass will the renderer generate unlabelled, muted, native playback with `preload="none"`.

Two homepage photograph strips use the central approved design/portfolio loaders, not a second catalogue: first flows right→left; second left→right; each preserves DOM newest-upload-first from the **verified 19 Nov upload timestamp**. Older media without source timestamps use stable original published-loader order and are never assigned invented upload or manufacture dates. Multi-view garments and design families remain together. Each strip has explicit pause/resume, Escape pause, reduced-motion and JS-off static overflow fallbacks.

## Source files
`scripts/build_homepage.py` builds index.html from the shortened existing homepage template/hero/contact, the new `scripts/homepage_redesign.py` renderer, and `_templates/homepage-redesign.css/.js`. Existing homepage JS and footer customer support stay. Owner statement is in README and dated rights record; no new framework/provider/booking route.

## Hold / external checks
Do not mark video publication rights or poster approvals verified from the new **photograph-only** owner statement. Original video files exist in the repository but are not made visible by this page. Do not claim a WhatsApp click sends a message. The R55 PDF remains staging-review, so the homepage support consent link continues to point to the preserved currently effective HTML Terms. Staging noindex preserved; `main` not modified.

## QA
Run Python build + check, Python media/gallery tests, SEO/sitemap and noindex checks; desktop/mobile browser layout/link/gallery controls and Terms-gated WhatsApp checks; report any historical homepage tests superseded by this expressly authorised new owner design. Verify deployed Cloudflare provider status separately from independent remote browsing.

## Historical baseline-test conflict
The repository's legacy `tests/collections_data.py` test asserts **20** published designs (an old snapshot). R55 and current R56 full-site builds report **28** genuinely eligible Showroom designs. The stale legacy expectation fails on the unchanged eligible set, and is not a safe release gate for this homepage-only design. R56 instead asserts that the publication-gated loader remains at its existing 28-design baseline and that all 22 newly authorised homepage reference designs retain `published:false`. The old legacy test is recorded FAIL (obsolete fixed count); it is not misreported PASS.
