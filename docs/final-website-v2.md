# Mr Sewing — Final Website Completion V2

Baseline: `ce32d5ff67eacecf03804bf6608222c5f13e3cd1` (Customer Journey V1).
Authorized delivery: `phase1/customer-journey-repairs` only. This report supersedes
V1's pending-photo-permission status: the owner's final V2 instructions confirm
publication permission and genuine completed-work status for the existing hero,
reviews/gallery, Happy Customers and men's Wedding card photographs. No customer
names, quotations, consultation histories or testimonials have been added.

## Homepage and navigation

The borderless hero presents the existing women's `h1.jpeg` and men's `r7.jpeg`
photographs, using their existing optimized derivatives. The first is the
original off-white graduation suit; the second is the light-grey jacket/navy
trousers photograph already used for the Wedding card. Originals are retained.
Photo and heading change together after exactly **25,000 ms of active time**, with
a gentle crossfade. Explicit pause, hidden-page suspension and reduced-motion
manual controls prevent unwanted motion. The fixed image/text slots avoid layout
shifts. No removed hero enquiry buttons were restored. The supporting statement
includes bespoke fashion and premium garment care in Kigali.

Shared header/footer destinations:

| Entry | Canonical destination |
| --- | --- |
| Home | `/` |
| Collections | `/collections/` |
| Our Work | `/our-work/` |
| Services | `/services/` |
| Garment Care | `/services/garment-care/` |
| About Us | `/about/` |
| Existing FAQs | `/faq/` |
| Shop — Coming Soon | `/shop/` |
| Contact Us | `/contact/` |

Shop is a real informational destination, explicitly unavailable for online
shopping, with no checkout, fake products or launch date. It is intentionally
`noindex,follow` and omitted from the sitemap while temporary.

Homepage service links retain their direct destinations:
`/services/custom-tailoring/`, `/services/wedding-tailoring/`,
`/services/graduation-tailoring/`, `/services/mobile-fitting/`,
`/services/garment-care/`, `/services/alterations/`,
`/services/express-tailoring/`. Service-specific FAQ additions are deferred.
Ask About Premium Care and Care Beyond the Occasion lead directly to Garment
Care. Timeline information leads to `/our-process/`; measurements information
leads to `/made-to-measure/`. These two reusable information pages explain the
stages and fitting preparations without promising dates or duplicating services.

Collections entry points remain `/mensuits/`, `/womensuits/`, `/collections/`,
and `/collections/?occasion=graduation|wedding|civil-wedding`. Verified metadata,
empty states, URL/back-forward behavior, 111 garment pages, stable references,
sharing, viewers and image optimization are preserved. Generated garment HTML
changes are shared navigation/footer updates, not a Collections redesign.

## Mr Sewing Garment Care

The section retains the existing disclosed AI still-life illustration and uses
**Mr Sewing Garment Care** / **Premium Clothing Care — Kigali, Rwanda**. The
illustration is not represented as actual premises, equipment or customer work.
Dry Cleaning is not promoted because no owner confirmation was supplied.

| Route | Purpose |
| --- | --- |
| `/services/garment-care/` | Specialized care homepage, basic statuses, enquiry process |
| `/services/garment-care/services/` | How to identify a suitable, currently available care option |
| `/services/garment-care/planning/` | One useful planning page with `#prices`, `#turnaround`, `#pickup-delivery` sections |

The local care navigation makes these destinations immediately available.
Pricing, timing and handover status are visible on the care homepage; customers
are not forced through several pages for basic information. No duplicate large
homepage care section was added.

`_data/care-information.json` manages business identity and truthful public
statuses. `_data/garment-care.json` and `scripts/garment_care.py` retain the
validated, reusable service/pricing architecture: garment/service type, RWF
standard price, optional approved charges, availability, turnaround range/unit,
express availability and notes. Service publication requires confirmation,
evidence and complete content. Rates/timings have separate approval gates.

**Zero candidate treatment pages or price tables are published.** The six draft
categories remain private source records. No fabricated zero/sample prices,
equipment, methods, same-day promises or delivery coverage are shown.

Competitor research was attempted through the available network; the search
request was blocked by the environment proxy (`Tunnel connection failed: 403
Forbidden`). No competitor findings, prices or copied content are claimed.

## Our Work: five projects, seven original photographs

| Project route suffix under `/our-work/` | Existing sources |
| --- | --- |
| `off-white-graduation-suit/` | `h1.jpeg`, `h2.jpeg`, `h3.jpeg` |
| `light-grey-and-navy/` | `r7.jpeg` |
| `soft-ivory-tailoring/` | `r4.jpeg` |
| `cobalt-blue-suit/` | `r2.jpeg` |
| `blue-jacket-black-trousers/` | `r3.jpeg` |

The graduation views are grouped by the matching garment and original archive
association. Other projects remain distinct. Editorial descriptions cover
visible colour, silhouette, layers and garment details. No identity inference or
invented personal story is used. Each page has responsive photographs, access to
original full images, keyboard/swipe viewing and a contextual WhatsApp enquiry
to `+250787411501`. Existing project templates remain reusable.

The three Happy Customers originals (`h2`, `r7`, `r4`) now lead to their verified
matching project pages. View Full Customer Gallery leads to `/our-work/`.
`views.html` and existing archive aliases retain their direct permanent redirect.

## FAQ and legal work — deferred by owner

The latest resume instruction supersedes the earlier FAQ requirement. No updated
FAQ categories, answers, FAQ schema, new FAQ redirects or FAQ content source are
in this delivery. The uncommitted draft is preserved outside the website at
`/workspace/artifacts/deferred-faq-v2/`. Existing `/faq/` content and legal pages
remain unchanged. Navigation continues to the existing FAQ destination. New
Terms & Conditions, Refund Policy and Privacy Policy are not implemented.

## About, SEO, redirects and cleanup

About now displays the existing official logo at its original proportions in a
dark, generously spaced presentation. Its written story/template main content
remains unchanged. No logo was generated or redesigned.

New pages have distinct titles/descriptions, one H1, production canonicals,
Open Graph information, semantic links and suitable breadcrumb/service data.
Project social images use the actual authorized photographs. Homepage social
imagery now uses `h1.jpeg`. No invented reviews, prices or ratings are marked up.
Discovery metadata and `llms.txt` now link current canonical destinations.

The generated sitemap contains **146 canonical indexable URLs**. It excludes
Shop, redirect-only aliases, unpublished care treatments and other noncanonical
or temporary routes. There are **50 existing generated redirect rules**, preserved without new FAQ
redirects. Existing FAQ URLs remain unchanged. Existing service/archive aliases
remain compatible without chains.
Staging noindex headers/client hostname guard remain in place; actual live
headers require deployment verification.

No original assets or valuable records were deleted. The replaced independent
hero-text animation and obsolete disabled Shop behavior were removed from their
existing components. Existing FAQ implementation is retained. The builder still owns
reproducible output; no new runtime framework or animation library was added.

## Verification and evidence

Build and deterministic checks: `python3 scripts/build_site.py` and
`python3 scripts/build_site.py --check` passed. Fourteen static/data/build suites
passed. Fifteen browser regression suites passed after correcting one stale
canonical discovery link. Exact-clock tests verify the 25,000-ms dwell, synced
text/photos, hidden-page remaining time, manual pause and reduced motion.
Responsive coverage includes 45 new-page/viewport combinations at 320, 390, 768,
1100 and 1440 px, plus the existing Services/Collections regression suites.
The checks exercise nine-link mobile navigation,
project viewers, contextual WhatsApp encoding, legacy routes, metadata,
collections filters, pagination/sharing and no-JavaScript content.

A complete inventory audit also passed for all 146 sitemap pages: unique titles
and descriptions, one H1, production canonicals, Open Graph metadata, parseable
JSON-LD and 5,979 existing local links/resources.

**33 axe page/state scans passed with zero violations** for WCAG 2 A/AA, WCAG
2.1 AA and best-practice checks. Automated checks do not replace owner review.

Evidence is outside the public site at `/workspace/artifacts/final-v2/`:
`static-results.json`, `browser-results.json`, `accessibility.json`, per-suite
logs, mobile/desktop PNGs, and Lighthouse JSON/HTML reports. Screenshots cover the
homepage, care landing page, Our Work and About at 390 and 1440 px.
Final Lighthouse measurements and delivery limitations follow below.
The complete changed-file inventory is [final-website-v2-files.txt](final-website-v2-files.txt).
Primary source changes are the existing homepage/About/shared templates,
`_data/customer-projects.json`, `_data/care-information.json`, the journey/care
builders and new `scripts/build_completion.py`; remaining HTML is reproducible
generated output. Existing FAQ/legal source files are absent from that inventory.

## Owner decisions and production checklist

Required before advertising specific care treatments: confirm offered categories,
operating model, suitable/excluded garments, process/preparation/limitations and
publication approval. Then supply approved RWF rates/additional charges,
turnaround/express conditions, and pickup/delivery availability, coverage and
fees. Current site explicitly communicates their unconfirmed status.

Before production: complete/review official Terms, Privacy and other policies;
confirm payment/deposit/cancellation and service operational details; review
staging visually; verify actual Cloudflare response headers/redirects; approve
production separately. No production deployment or hosting/DNS change is part of
this task. Customer names, approved genuine testimonials and further photographs
are optional later additions; photo permission already received is not requested
again.

After owner-authorized production deployment: rebuild/check the final sitemap;
verify production sitemap/robots accessibility, canonicals, redirects and
indexability; submit only the production sitemap in Google Search Console;
inspect key changed URLs; monitor indexing/coverage and search performance.
**No Search Console submission or reindexing action has been performed.**

## Final Lighthouse measurements

Lighthouse 13.6.0 with local Chromium 154, one cold run for each mobile/desktop
preset. HTTPS third-party requests were blocked. These are local laboratory
measurements, not staging field data or measured real-user INP.

| Page | Mobile performance | Desktop performance | Accessibility / Best practices / SEO (both) |
| --- | ---: | ---: | --- |
| Homepage | 100 | 98 | 100 / 100 / 100 |
| Garment Care | 100 | 100 | 100 / 100 / 100 |
| Our Work | 100 | 100 | 100 / 100 / 100 |
| Graduation project | 100 | 100 | 100 / 100 / 100 |
| About | 99 | 100 | 100 / 100 / 100 |
| Collections | 98 | 100 | 100 / 100 / 100 |

LCP ranged from 0.34 to 2.33 seconds; CLS was zero except a 0.00048 project-desktop
measurement. No Lighthouse runtime errors were reported. Full JSON/HTML reports
are in the evidence directory.

## Staging delivery limitations

Only the authorized staging branch may be pushed. No main merge, production
deployment or production/DNS/account setting change was performed. The commit
and verified Git push status are supplied in the delivery response and the
external evidence record. Access to `https://mrsewing-staging.pages.dev/` is
blocked by this environment's proxy (CONNECT tunnel HTTP 403). A successful
Cloudflare deployment therefore cannot be claimed from these local tests. The
owner must verify the live staging commit and pages before production approval.
