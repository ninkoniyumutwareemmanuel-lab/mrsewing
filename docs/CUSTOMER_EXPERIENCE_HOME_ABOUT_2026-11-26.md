# Homepage and About customer-experience refinement — 26 November 2026

## Pre-writing brief and baseline

- Branch: `phase1/customer-journey-repairs`; starting commit `b388644796fcb24b747bb6818dd211422fab9cff`.
- Authority: owner's 26 November comprehensive website assignment §§5–8 and16; current customer reference `2026-11-25-01`, master/matrix/unresolved/page map; retained R61 media authorization, R63/R64 homepage, R65 modal routes and R67 service hub. No production authorization.
- Pages: `/` introduces professional tailoring and existing service/Showroom/contact journeys; `/about/` explains brand, values, services and operating-company relationship. Public page titles, descriptions, canonical URLs, existing image paths and schema are preserved.
- No new prices, benefits, manufacturing claims, operating conditions, biography or contact destination is introduced. Existing quotation/provider/consent and Shop behavior are outside this scoped edit.
- Homepage primary links retain the existing design-sharing, `/collections/` and `/services/custom-tailoring/` destinations. The bottom quotation action uses the same `/request/?general=1` destination with the standardized `Request a Quote` label. Browsing is not a submission, purchase or automatically accepted request.
- About retains its exact five-service disclosure built from the shared header. Individual service links and Contact Us remain ordinary crawlable links. Policy information links to the current effective Terms route, not the separate review PDF as contractual authority.
- Leadership public name/title/biography and an approved portrait remain missing. The owner identifies a person in the assignment but explicitly requires approval of their public profile; no unfinished content should be displayed.
- Before evidence: local Chromium390/1440 screenshots under `/workspace/review/2026-11-26/before/`, including decoded feature photographs. These are local snapshots, not independently verified Cloudflare-origin pages.

## Changes

- The original `r4.jpeg` light ivory outfit remains at the same path and same service destination. The feature now presents the full portrait with `object-fit: contain`, rather than cutting off the person's head and garment in a shallow landscape crop. On mobile the image has its original portrait ratio, with the caption below rather than covering the garment. Desktop uses a balanced image/text split.
- Its alt text describes the visible jacket/trousers rather than calling it generically approved imagery. No assertion that Mr Sewing manufactured this reference is added.
- Homepage sections have shorter vertical spacing, fewer decorative panels and a compact two-column process at suitable phone widths. Duplicate supporting explanations beneath three headings are removed. Existing silent videos, main tailoring/VIP cards, opposite-direction media rows, unique customer information, programme links, Shop and all customer journeys are retained.
- About has one clear brand introduction, a shorter customer-centred story, the existing approved mission and vision, all five values, five service summaries, one concise process/policy section, company information and contact/service actions. Repeated approach/commitment explanations are consolidated.
- The legal operating-company logo is a small supporting mark in Company Information instead of dominating the first screen. The global Mr Sewing logo is unchanged.
- `_data/about-leadership.json` and `_templates/about-leadership.html` provide the optional profile. `published:false` produces no customer markup. Deliberate publication additionally requires approved content, name/title/biography, permitted local portrait, descriptive alt and intrinsic dimensions. The renderer escapes every plain-text field and rejects invalid/incomplete publication.

## Ownership and tests

Sources: `_templates/homepage-tailoring.html`, `_templates/homepage-tailoring.css`, `_templates/about.html`, `_templates/about.css`, `scripts/build_about.py`, `_data/about-leadership.json`, `_templates/about-leadership.html`.

`tests/about_leadership.py` verifies the inactive record, approval gate, required fields, photo permission/path/dimension checks and HTML escaping. Integrated builds, browser/axe checks and generated output are handled in the full task's final review package, with actual outcomes recorded there. Historic About tests expecting an unsupported founding year/family history are obsolete and are not treated as current approved requirements.

Owner decisions still needed: approved public leadership name/title, concise biography/personal statements and portrait with publication permission. Until then the entire leadership component remains absent from public pages.
