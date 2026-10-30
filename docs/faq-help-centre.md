# FAQ help centre and Coming Soon previews — staging review

Baseline: `40c18afc0e4094fd9e1616ad6fe48db1fd4df757`.
Authorized branch: `phase1/customer-journey-repairs`. This phase continues the
latest clean implementation. It does not reset earlier work, rewrite policies,
change the hero or launch the three proposed programs.

## Completed scope

`/faq/` is a welcoming help centre with a prominent search field and fourteen
service/customer-information cards. Cards are real links to dedicated clean
routes; the hub does not display the former mixed list of questions. Single-column
cards at narrow phone widths become two columns on tablet and three on desktop.
Small original inline-SVG icons and the established black/gold/ivory typography
avoid new image downloads, icon fonts or libraries. Counts come from published
questions; no popularity rankings, reviews or invented statistics are used.

Each topic has one H1, introductory guidance, breadcrumbs, All FAQ topics links,
native accessible disclosures, stable descriptive answer IDs/permalinks, a
relevant service/information link, related topics and one contextual WhatsApp
contact option. Messages identify the topic and production URL; opening a link
does not confirm an appointment or accepted production order.

Every FAQ page renders the exact canonical homepage header/footer through
`scripts/shared_components.py`, the same image/icon delivery helpers and shared
menu controller. No component markup was forked and no shared source was changed.
FAQ-specific CSS is scoped under `.faq-help`. Browser checks compare rendered
header/footer markup with the homepage, including the existing map/social links.

The three Coming Soon previews are restored between Services and the final
contact section. Their existing `home-programs`, `program-grid`, `home-program`
and photoshoot layout classes reuse the stylesheet already in place. The copy
matches the newly authorized meanings: programs/photography are in development;
details, conditions and relevant availability/eligibility will be announced when
ready. Every preview says Coming Soon, with no action, enrollment or data field.
No rewards, percentages, commissions, gifts, cleaning entitlements, qualifying
purchases, dates or guaranteed eligibility are offered. The separate historical
premium-cleaning-and-gifts claim is not restored.

## Routes and published content

The inventory below is generated from the maintained catalogue. Question counts
are actual published answers, not a required quota. Each answer has one canonical
owning topic; related guidance links to that destination instead of creating
parallel help centres.

| Topic | URL | Published answers |
| --- | --- | ---: |
| Custom Tailoring | `/faq/custom-tailoring/` | 6 |
| Wedding & Civil Wedding Tailoring | `/faq/wedding-tailoring/` | 5 |
| Graduation Tailoring | `/faq/graduation-tailoring/` | 5 |
| Mobile Fitting | `/faq/mobile-fitting/` | 5 |
| Alterations & Refinements | `/faq/alterations/` | 6 |
| Express Tailoring | `/faq/express-tailoring/` | 5 |
| Mr Sewing Garment Care | `/faq/garment-care/` | 6 |
| Collections & Design Requests | `/faq/collections-designs/` | 5 |
| Measurements & Fittings | `/faq/measurements-fittings/` | 5 |
| Prices, Suit Packages & Payments | `/faq/prices-packages-payments/` | 8 |
| Booking, Locations & Visiting | `/faq/booking-visiting/` | 5 |
| Production, Delivery & Collection | `/faq/production-delivery/` | 6 |
| Cancellations, Refunds & Order Changes | `/faq/cancellations-changes/` | 5 |
| Privacy & Customer Photographs | `/faq/privacy-photographs/` | 5 |

Total: 14 topics, 77 distinct published questions. Existing confirmed answers,
customer-information tokens and supported service descriptions are reused and
organized, with service-specific preparation/assessment guidance. No unfinished
program rules or invented service guarantees are added.

## One maintained data/build system

- `_data/customer-faqs.json` now contains topic records, canonical question IDs,
  answers, related topics, keywords, a small synonym list and legacy-fragment
  destinations. Published flags permit controlled publication; empty public
  topics and duplicate question ownership are rejected.
- `_data/customer-information.json`, `_data/policy-pages.json` and existing
  service content remain the factual baseline. Those files are unchanged.
- The existing `scripts/build_customer_information.py` delegates its FAQ portion
  to `scripts/faq_help.py`; there is no competing standalone help-centre builder.
  Three policy outputs remain byte-identical. Obsolete mixed-list rendering was
  removed rather than retained as a second FAQ experience.
- `_templates/faq.html`, `faq.css` and `faq-help.js` provide shared FAQ layout and
  enhancement. `assets/faq-help.js` is generated from the canonical menu script
  plus FAQ-only behavior. Fourteen topic directory pages and `faq.html` are
  generated, then the existing clean-URL builder creates `/faq/index.html`.
- Cards, counts, topic HTML, answer anchors, JSON-LD and the embedded search index
  all come from that same catalogue. Existing build and `--check` workflows remain.

## Search and compatibility

Search examines question titles, full expanded answer text, topic titles and
maintained keywords across all published topics. It is case-insensitive, folds
accents/punctuation and supports useful synonyms such as deposit/advance,
house-call/mobile-fitting and photo/photograph. Results show the actual question,
topic and a relevant excerpt, linking directly to the answer. The clear control
has an accessible name, restores cards and focuses the input. Empty results give
an honest message and contact option. Results/status use safe text construction;
no query is interpreted as HTML. There is no external search, tracking or new
runtime framework. Search state uses the hub's `?q=` URL for refresh/back behavior.

Without JavaScript all cards, service/related links, breadcrumbs and native
question disclosures work. A short noscript explanation directs visitors to the
topics; no broken search control is shown. With JavaScript, a direct answer hash
opens its disclosure. Existing `/faq.html` compatibility and server aliases are
unchanged. Meaningful old fragment mappings:

| Old fragment on `/faq/` or `/faq.html` | Destination |
| --- | --- |
| `#cat-visit`, `#cat-booking` | `/faq/booking-visiting/` |
| `#cat-ordering` | `/faq/production-delivery/` |
| `#cat-pricing` | `/faq/prices-packages-payments/` |
| `#cat-alterations` | `/faq/alterations/` |
| `#cat-policies` | `/faq/cancellations-changes/` |
| `#orderModal` | `/faq/custom-tailoring/#start-order` |

Fragments are not sent to HTTP servers, so topic mapping is client-side. With
scripts disabled, retained IDs land on the appropriate linked hub card. No old
modal, mixed question list or new permanent redirect chain is introduced.

## Confirmed facts and remaining decisions

The same confirmed facts remain: 70% advance; suit balance after tailoring and
before final cleaning/delivery; full payment before release; standalone service
balance on completion; actual unpaid balance after received payments; four Cotton
prices; standard jacket/trouser and waistcoat contents; quotation for skirts and
extras; included initial cleaning/Kigali delivery; customer-paid outside-Kigali
courier charges confirmed before dispatch; work-stage estimates distinguished
from total order timing; requests distinguished from confirmed arrangements.

No higher-collection figures, unapproved rewards/gifts/follow-up cleaning,
express/mobile surcharge rules, cancellation penalties, correction deadlines,
cleaning guarantees/claims conditions, courier liability or new privacy practices
are published. Supplier/maker costs, margins, budgets, owner pay, reserves and
sales targets are not exposed. Existing policy pages are linked and unchanged;
FAQs are informational and do not replace them.

Owner decisions remain those documented in the previous customer-information
review: final cancellation/refund/advance treatment, change approval, correction
conditions, storage, care availability/limitations/claims/timing publication,
courier responsibilities, privacy/photo/marketing arrangements and unapproved
express/mobile/higher-collection charges. Loyalty, referral and photography
program benefits/eligibility/conditions and launch readiness remain undecided.
These previews are not launched programs. No new legal verification or legal
compliance claim is made in this scope.

## FAQ-scoped SEO and protected configuration

The existing hub title/description and truthful author/location/social preview
metadata are retained. Its old FAQPage schema was replaced with a CollectionPage
and an ItemList matching the visible topic cards. New topics have unique metadata,
production canonicals, matching Open Graph/Twitter data, accurate visible-answer
FAQPage schema and breadcrumbs. No ratings or unsupported offers are marked up.
The one outdated FAQ description in `llms.txt` is corrected; its other content
and destinations are unchanged.

The existing sitemap builder adds only the 14 new canonical FAQ URLs: 160 total,
with all 146 earlier entries preserved. It excludes search queries and answer
fragments. No robots, staging noindex, redirects, Google verification, Search
Console, Maps, CNAME, DNS, hosting, credentials, account or dependency settings
are changed. No sitemap submission or indexing request is made, and no search
ranking outcome is promised.

## Evidence and delivery

Evidence directory: `/workspace/artifacts/faq-help-centre/`.
Final checks, screenshots, exact changed-file inventory, commit/push and staging
verification limitations are recorded with delivery. Screenshots cover the hub,
a topic page, search results and the restored previews at 390 and 1440 pixels.
Owner review is still required before any main merge or production publication.

## Final validation

- Full build and `python3 scripts/build_site.py --check`: passed, reproducible.
- 16 static/build/data suites: passed. The new scope guard checks literal homepage
  equality outside the preview block; byte-identical policy sources/outputs,
  hero code, shared components, media, registries and configuration; matching
  source/schema/search answers; truthful preserved hub metadata; and only new FAQ
  sitemap entries. Shared-component injection/parity checks cover FAQ output too.
- 18 browser/audit suites: passed after correcting an empty-result contact
  contrast issue. Existing Collections, About/Contact, image delivery, discovery,
  header, metadata, routing, customer journey and intercepted form suites passed.
  No real form submission or external message was sent.
- New FAQ browser suite: all 14 destinations and 77 answer anchors, 60 FAQ
  page/viewport combinations at 320/390/768/1440px, full-answer and keyword/synonym
  search, case handling, relevant results, empty/clear states, safe text rendering,
  back/refresh, old bookmarks, actual homepage component equality, keyboard and
  no-JavaScript navigation/disclosures passed. All three safe previews passed
  responsive and placement checks; no enrollment, benefit or redemption action.
- 37 axe scans passed with zero detected violations across all FAQ routes, open
  answers, search/empty/mobile menu states and homepage previews (WCAG 2 A/AA,
  WCAG 2.1 AA and best practices). Automated checks do not replace owner review.
- Complete sitemap inventory: 160 pages with unique title/description, one H1,
  production canonical/OG/parseable JSON-LD and 6,604 existing local link/resource
  destinations. No missing local responses or browser page errors in new flows.

Exact file inventory: [faq-help-centre-files.txt](faq-help-centre-files.txt).

Screenshot files in the evidence directory:
`hub-390.png`, `hub-1440.png`, `topic-390.png`, `topic-1440.png`,
`search-390.png`, `search-1440.png`, `programs-390.png`, `programs-1440.png`.

## Final local Lighthouse measurements

Lighthouse 13.6.0 / Chromium 154, local preview, one cold run for each preset.
External HTTPS was blocked. These are local laboratory measurements, not verified
staging field results, Google ranking evidence or real-user INP measurements.

| Page/state | Mobile performance | Desktop performance | Accessibility / Best practices / SEO, both |
| --- | ---: | ---: | --- |
| FAQ hub | 99 | 100 | 100 / 100 / 100 |
| Prices/packages topic | 100 | 99 | 100 / 100 / 100 |
| Search results | 100 | 100 | 100 / 100 / 100 |

All final mobile CLS values were zero; desktop values were zero except 0.00508
on the hub. An initial diagnostic found the search bar's late appearance moved
content. Rendering its space from the first JavaScript-enabled layout and preparing
the search index lazily fixed that shift without changing no-JavaScript topic
access. The affected functional/accessibility checks were repeated. Earlier
diagnostics are retained in `before-search-startup-fix/`; final JSON/HTML reports
remain outside the public site alongside screenshots and suite logs.

## Staging boundary

The commit/push result is supplied in the delivery response and external evidence
record. A successful Git push is distinct from verified Cloudflare deployment.
The managed proxy restricts the staging hostname; live verification is attempted
after pushing and no deployment success is claimed without evidence. No main
merge, production publication, DNS/hosting/account change or indexing action is
performed. The owner must review staging before approving production.
