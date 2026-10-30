# Collections V3 — Luxury Minimalist Showroom

V3 release record. [Customer Journey V1](customer-journey-v1.md) subsequently
updates shared navigation, SEO/alternative text and occasion links, and appends
three non-collection care illustration assets. The V3 gallery design, images and
design registry remain protected.

Implemented for `phase1/customer-journey-repairs`, based on
`cf3d68b2cb1c04728c926ffccfe6a3acdd9d5df2`. This is a staging change;
production, DNS and hosting configuration are outside this implementation.

## Experience and architecture

The existing `/collections/`, `/mensuits/` and `/womensuits/` URLs now lead to
compact black-and-gold galleries: a short introduction, All Designs / Men / Women
navigation, discreet combined search/style/occasion filters, photographic cards
and explicit Load More. Two columns at mobile widths become three at 600px and
four at 1100px. Cards have consistent 4:5 frames with `object-fit: contain`:
photographs are neither stretched nor additionally cropped. Existing WebP/AVIF
candidates, intrinsic dimensions and lazy loading are retained. The first four
server-rendered gallery images load eagerly; the initial cards are enhanced in
place. Filter space is reserved before JavaScript loads to avoid layout shift.

There is no favourites/heart/saved-design/shortlist UI, storage listener, or
WhatsApp shortlist generator. The old JS filename remains as an inert compatibility
file; V3 uses `assets/collections-v3.js` and `assets/collection-design.js`.
Existing browser favourites data is not read, written or deleted.

One dependency-free Python builder, `scripts/build_collections.py`, validates the
original registry, creates the galleries and generates garment pages from
`_templates/collection-design.html`. Gallery styling is in
`_templates/collections.css`; shared header/footer sources remain unchanged.
`python3 scripts/build_site.py` and `--check` include all these outputs. Check mode
also rejects unexpected obsolete garment pages rather than silently retaining a
newly excluded design. Explicit retirement/removal needs review.

## Eligibility, names and original assets

The actual dataset contains **138 records**: **111 previously published designs**
and **27 excluded records**. V3 creates exactly **111** garment pages, one per
eligible record, at `/collections/designs/<stable-slug>/`. All current records
have one photo. No photographs were grouped or newly admitted, and no original
or optimized image bytes were changed. Existing publication-basis, rights,
provenance and grouping-evidence guards remain in force; a regression also rejects
multi-image grouping without evidence.

The ID registry, source dataset and image inventory are unchanged. The generated
migration CSV now points each published image to its static design page. Existing
rights-review documentation is retained verbatim. Existing public display is not
new evidence of ownership or a publication licence; the recorded owner review
requirements remain applicable before production approval.

Customer names derive only from verified V2 category metadata, for example
“Classic Tailored Suit”, “Double-Breasted Tailored Suit” and “Classic Women’s Suit”.
Unclassified records retain the neutral “Tailoring Design”. No colour, fabric,
construction or ownership details are invented. Reference numbers remain in the
registry, stable URLs, data and enquiries, without appearing in visible
card captions, garment headings or photo alternative text.

## Garment pages, enquiries and sharing

Warm-ivory garment content is framed by the unchanged dark shared header/footer.
Desktop places a large photo beside concise information; mobile places the photo
first. One **Request This Design** link targets `https://wa.me/250787411501` and
encodes the name, stable reference and direct URL. JavaScript uses the current
origin, so staging enquiries and shares link to staging. Without JavaScript, the
static enquiry retains its production canonical URL; the photograph remains an
ordinary full-size image link. No real messages are sent by tests.

Share Design uses native sharing, then Clipboard API, then a selectable Copy Link
field. Cancellation and duplicate clicks are handled. A native dialog displays
the complete original photograph, locks background scroll, supports Escape,
restores focus and traps keyboard focus. Arrow keys and swipe move only between
verified images of the same garment; a single-image garment stays on its own
photo, with disabled previous/next controls. Multi-photo behavior is exercised
with an intercepted test fixture, never by altering production records.

Recommendations use shared recorded styles, occasions or a known gender, with
at most four photographs in **Similar Styles You May Love**, and up to four
other photographs in **Discover More Designs**. The current garment and previous
recommendations are excluded. **54 designs** have no metadata-backed similarity
candidate; their similar section provides a short invitation to explore instead
of claiming a match. Every eligible design still has additional discoveries.

## URLs and discovery

V2 `?design=MS-...` links and `#design-MS-...` bookmarks resolve to the new static
page; legacy `.html` routes first preserve their query/hash during the existing
clean-URL redirect. Unknown IDs show an unavailable message, not an unsafe URL.
Legacy category pages and their content are retained.

Garment pages have their own canonical, Open Graph image/name/description and
WebPage/ImageObject metadata, without unsupported Product/offers schema. A
separate generated `/collections/designs/sitemap.xml` contains exactly the 111
eligible design URLs and is listed in `robots.txt`. The original 27-route sitemap
is unchanged.

## Validation and artifacts

Run the commands in `tests/README.md`, with the local static server on port 8000.
The existing browser regression suites and new V3 suite were executed, covering
approved pages, 111 static URLs, three galleries at seven widths, search/filter
combinations, complete Load More, old routes, sharing/WhatsApp, recommendation
uniqueness, viewer keyboard/focus/swipe, single/multiple photos, no-JavaScript
content, and zero missing resources/page errors. Enquiries are inspected or
mocked; external requests are blocked.

`tests/collections_pages.py` additionally compares approved homepage/About/Contact,
shared components, all original images/media, the registry and inventory against
the starting commit. `tests/collections_data.py` retains invalid-rights/provenance,
ID, retirement and grouping guard tests.

Axe 4.14.0 reported zero violations across gallery/category/design pages at 390px
and 1440px, including the open photo viewer, for WCAG 2 A/AA, WCAG 2.1 AA and
best-practice tags. This is an automated scan, not a complete conformance claim.

Lighthouse 13.6.0 used local Chromium 154, standard mobile/desktop presets, one
cold run per route/preset, and external HTTPS requests blocked. After the filter
layout correction, results were:

| Page | Preset | Performance | Accessibility | Best practices | SEO | LCP | CLS |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Collections | Mobile | 98 | 100 | 100 | 100 | 2.3 s | 0 |
| Collections | Desktop | 100 | 100 | 100 | 100 | 0.5 s | 0 |
| Garment (MS-009) | Mobile | 100 | 100 | 100 | 100 | 1.7 s | 0 |
| Garment (MS-009) | Desktop | 100 | 100 | 100 | 100 | 0.4 s | 0 |

These local diagnostics do not measure deployed cache headers, DNS/TLS/CDN,
production Core Web Vitals or real-user INP. Results vary with shared-machine
scheduling. Reports and screenshot artifacts are outside the website checkout at
`/workspace/artifacts/collections-v3/`, including gallery/category/design and
viewer screenshots at 390px and 1440px, Lighthouse HTML/JSON and axe JSON.
Audit tooling is pinned and installed under `/workspace/tools/collections-v3/`;
it is not a visitor dependency. See the delivery response for push/deployment
status; a local pass does not prove Cloudflare served the new commit.

## Homepage recommendation — not implemented

The approved homepage already has Collections in its main navigation and separate
Men’s/Women’s cards. A restrained **View All Designs →** text link immediately
below the existing four-card inspiration section would make the full showroom
easier to discover without adding a promotional block or changing the approved
hero. Keep its current typography/spacing and link to `/collections/`. This needs
separate authorization; no homepage or shared navigation edits were made here.
