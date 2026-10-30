# Mr Sewing — Customer Journey V1

Implementation baseline: `08191fde2c1e984206ca40d53fbe99f69ce218da`.
Authorized branch: `phase1/customer-journey-repairs`. No production merge,
production deployment, DNS change or production account-setting change is part
of this work. This document follows the final consolidated owner specification.

## What changed

The homepage, Services, Our Work, Collections entry links and SEO now form one
customer journey. Existing shared components/builders remain the architecture;
no visitor framework, animation library, third-party font or new runtime API is
introduced. The pre-implementation findings are recorded in
[the audit](customer-journey-audit.md).

Homepage hero actions were replaced by **Crafted for Your Story** and three softly
fading phrases in a fixed typography slot. Only opacity and a small translation
animate; reduced motion shows a single readable phrase. The accessible static
text remains available. The original hero photograph and responsive derivatives
are unchanged. Customer-photo bytes and the three existing homepage photographs
are retained; their links safely lead to Our Work rather than invented stories.

## Navigation and canonical service inventory

Header and footer primary links now share six distinct destinations:

| Label | Destination |
| --- | --- |
| Home | `/` |
| Collections | `/collections/` |
| Our Work | `/our-work/` |
| Services | `/services/` |
| About Us | `/about/` |
| Contact Us | `/contact/` |

The same seven service destinations are linked directly from both the homepage
cards and the photographic Services overview. No extra overview step is required
from a homepage service card.

| Service | Canonical route |
| --- | --- |
| Custom Tailoring — men and women | `/services/custom-tailoring/` |
| Wedding & Civil Wedding Tailoring | `/services/wedding-tailoring/` |
| Graduation Tailoring | `/services/graduation-tailoring/` |
| Mobile Fitting | `/services/mobile-fitting/` |
| Premium Garment Care | `/services/garment-care/` |
| Alterations & Refinements | `/services/alterations/` |
| Express Tailoring | `/services/express-tailoring/` |

`_data/journey-services.json` contains the confirmed scope, evidence/source paths,
requirements, process, page-specific sections and illustrative assets. Custom
Tailoring covers garment categories for men and women, references/sketches,
own-fabric assessment, fabric options, measurements, fittings, ordering,
production and agreed collection/delivery. Mobile Fitting explains preparing for
a customer-location visit in Kigali and confirming coverage, charges and dates.
Express Tailoring asks for an exact deadline without promising capacity, fees or
a completion time. Alterations are subject to garment assessment. Wedding and
graduation pages link their relevant Collections filters without assigning new
occasion metadata.

Service images are existing garment inspiration or fitting/measurement
illustrations, explicitly distinguished from verified customer projects. No
identifiable customer photograph was introduced into a new service story. The
new garment-care still life is clearly labelled AI-generated. None of its objects
are represented as actual Mr Sewing equipment, premises or customer work.

## Premium Garment Care

The care section has its own warm ivory, dark olive and brass visual treatment,
editorial imagery, local navigation, care-information blocks, preparation guide,
quotes/timing explanation and one context-aware enquiry. It is a functional
**enquiry landing page**, not a claim that all candidate treatments are offered.

`_data/garment-care.json` defines six **unpublished, unconfirmed candidates**:
dry cleaning; laundry/garment washing; pressing/ironing; suit/formalwear care;
delicate care; pickup/delivery. There are **zero published care subservice pages**.
The landing page does not advertise these candidate names or show empty cards,
zero prices, sample rates, equipment, delivery coverage or turnaround promises.

`scripts/garment_care.py` validates the structured publication/pricing model:

- Availability confirmation, confirmation evidence reference and publication
  approval are required before a category page can be generated or enter the
  sitemap. Suitable garments, process, customer preparation and limitations are
  required for a complete public page.
- Pricing currency is RWF. Each row supports garment type, service type, a positive
  integer `standardPriceRwf`, optional additional charges and notes. Each published
  rate/charge needs explicit approval and a nonempty evidence reference.
- Standard turnaround has minimum/maximum, a unit (hours/days/business days), an
  approval flag and evidence reference. Express availability and any additional
  charge have separate approval fields. Unapproved values are not rendered.
- All real price rows are currently empty. Turnaround, express availability and
  operating-model details are unconfirmed. There are no fictional examples in
  public content. Test prices exist only in an in-memory test fixture.

After owner confirmation, edit the structured data and run the normal build.
Eligible categories automatically gain cards, navigation links, dedicated
`/services/garment-care/<slug>/` pages, unique metadata, breadcrumbs and sitemap
entries. Existing files for a newly unpublished care/project record cause a build
failure requiring explicit retirement review; they are not silently left public.

The conceptual source image is preserved at
`assets/journey/garment-care-illustration.png`. Responsive WebP variants are 480px
and 960px (approximately 13 KB and 41 KB); the 2 MB source is not loaded by the
website. `scripts/prepare_journey_media.py --check` reproduces the derivatives
without altering source media. `_data/journey-media.json` records dimensions,
size and provenance. Three support-asset inventory entries were appended; all
previous inventory rows and all design IDs/records remain unchanged.

### Competitor research limitation

A read-only search for Kigali dry-cleaning/laundry service organization, pricing
presentation and collection journeys was attempted through the configured proxy.
The Google HTTPS request was blocked with `Tunnel connection failed: 403
Forbidden`. No browsing/search connector is available here. **Competitor research
was not completed**, and no competitor facts, rates, text, photos or branding were
used. The architecture is original and follows the owner's requirements. Before
launching specific care treatments, the owner can provide public research links
or enable read access for a separate review of local customer journeys.

## Our Work and customer privacy

There is no `views.html` in the baseline repository. The existing archive is
`reviews.html`; its promotional captions are not evidence of completed work or
consent. A safe `views.html`/`views/` compatibility path now leads to `/our-work/`.

`/our-work/` is an honest editorial overview that explains why individual project
features need confirmed facts and permission and provides useful service/design/
contact destinations. It displays **zero invented projects** and no new customer
photographs. A completed-project photographic gallery is supported by the builder
but cannot be populated accurately from the available evidence.

`_data/customer-projects.json` currently has zero project records. The pending
homepage photo references are h2.jpeg, r7.jpeg and r4.jpeg; their project
associations and publication permissions are not documented. All three retain
safe `/our-work/` links. “View the full customer gallery” also links there.

The reusable project template and `assets/project-gallery.js` support:

- A stable `/our-work/<slug>/` URL, factual context, and optional documented design
  request/process sections.
- Multiple individually authorized photographs with responsive source support,
  complete-image links and a native full-screen viewer (keyboard/swipe/Escape,
  focus trapping/restoration and background scroll locking).
- An approved testimonial only when testimonial approval evidence is supplied.
- One enquiry containing the public project title and canonical/current-origin
  URL, without private customer information.

Publication requires completed-work evidence, approved publication permission,
an evidence reference, and per-image permission/project-association references.
Viewer payloads exclude these evidence references. Store actual consent documents,
contact data and private evidence **outside the public repository**; use nonsecret
references in content. A test-only intercepted story exercises the viewer in
memory; it is never written as a public project or included in a sitemap.

The legacy archive remains available without being promoted as verified work;
unsupported narrative claims and sale/stock structured data were removed or
neutralized. Existing photo assets and the legacy slider were retained. The
archive and its fragment are not indexable. Owner review of continued permission
for existing identifiable photographs is still needed before production approval.

## Collections V3 preservation and entry links

All 111 eligible garment pages, original images, stable registry/URLs, responsive
variants, full-screen viewing, enquiries, sharing and distinct recommendations
remain. The 27 excluded records stay excluded. Gallery CSS is byte-identical to
the Collections V3 baseline. Changes are limited to approved shared navigation,
page-specific SEO, small alternative-text accessibility corrections and reliable
occasion-filter entry/history behavior.

| Homepage category | Destination |
| --- | --- |
| Men's suits | `/mensuits/` |
| Women's suits | `/womensuits/` |
| Graduation outfits | `/collections/?occasion=graduation` |
| Wedding outfits | `/collections/?occasion=wedding` |
| Civil wedding outfits | `/collections/?occasion=civil-wedding` |
| All collections | `/collections/` |

The selected occasion is visible on direct load, refresh, Back and Forward.
Other filters remain usable. Graduation has three verified matches. Wedding and
civil wedding currently have **zero** verified assignments; their selected-filter
empty states say so and offer a contextual enquiry. No garments were reclassified.
V2 individual-design query/hash links continue to open V3 garment pages.

## SEO, sitemap and redirects

`site_seo.py` normalizes metadata/indexability consistently at builder write/check
boundaries; `build_source_seo.py` updates legacy source metadata. Every indexable
route has a unique title/description, one H1, production canonical, Open Graph
metadata, appropriate alternative text and internal links. Garment references
disambiguate metadata without becoming prominent captions/headings. Service and
breadcrumb structured data describe actual canonical services. Unsupported
Product/AggregateOffer stock claims were removed from legacy inspiration markup;
no customer ratings, testimonials or prices were fabricated.

`build_public_routes.py` generates a unified **137-URL production sitemap**, exact
redirects, robots.txt and staging headers. It validates actual output existence,
canonical identity, H1 and unique metadata. It includes 111 garment pages, seven
canonical service details, Services, Our Work and eligible existing information
pages. Forms, noindex archives, coming-soon category pages, aliases, unpublished
projects/care subservices, query URLs and staging origins are excluded. The old
collection-only sitemap remains a valid compatibility file but robots.txt points
to the complete sitemap.

`_headers` applies HTTP `X-Robots-Tag: noindex, nofollow, noarchive` to the staging
hostname and its preview subdomains only, not the production hostname. Generated
HTML also switches its robots meta on Pages staging hosts. This code is prepared
and locally tested; live header enforcement must be verified after deployment.

The exact `_redirects` rules avoid wildcard chains and preserve queries. Existing
HTML aliases and old service aliases target their final canonical route directly:

| Legacy route | Final destination |
| --- | --- |
| `/service-standard/`, `/service-sketches/`, `/service-cmt/` | `/services/custom-tailoring/` |
| `/service-housecall/`, `/service-workplace/` | `/services/mobile-fitting/` |
| `/service-express/` | `/services/express-tailoring/` |
| `/views.html`, `/views/`, legacy happy-customers fragment | `/our-work/` |

HTML versions and service paths without a slash have direct rules too. Static
fallback documents retain canonical content and query/hash-preserving browser
navigation where applicable. Python's ordinary file server does not implement
Cloudflare redirect rules. `tests/preview_server.py` explicitly simulates them
for local tests; it is not evidence of a real Cloudflare deployment.

### Google Search Console after production approval

Search Console was **not changed**, and no sitemap/URL was submitted.
After explicit owner approval and production release:

1. Rebuild/check the final production tree; verify sitemap and robots.txt return
   HTTP 200 with appropriate XML/text MIME types on the production hostname.
2. Confirm canonical URLs, live 301 targets/query preservation, no loops/chains,
   actual indexability, and staging/preview noindex headers.
3. Check that unpublished stories/care categories and form/alias pages are absent
   from the production sitemap. Confirm no accidental production noindex header.
4. In the verified production Search Console property, submit
   `https://mrsewingfashion.com/sitemap.xml`, then inspect the homepage, Services,
   Care, Our Work and representative garment/service URLs.
5. Monitor sitemap processing, redirects, indexing/coverage and canonical selection
   after launch. A submission is not a promise of indexing or ranking. Never submit
   staging URLs as production pages.

## Cleanup and compatibility

No original photos/videos, registry records, policies, shared templates or required
builders were deleted. Untracked interim men's/women's/measurement/graduation
service outputs from this task were removed when the consolidated specification
replaced them; these were never published or committed. The six previous public
service routes were retained as generated compatibility outputs and permanent
redirects, rather than independent duplicate service pages.

Unused hero actions, unavailable Shop controls, mismatched navigation targets,
unsupported archive story copy and service-page automatic video downloads were
removed from the active journey. Original media files remain. Legacy order-modal
bookmarks/consent flow, the old slider, component fragments, image preparation
scripts and the inert V2 JS compatibility filename remain because existing URLs
or tooling still reference them. No valuable asset was removed based on its name.

## Verification and artifacts

See `tests/README.md` for commands. The normal full build and read-only check
include Services, Our Work, page SEO, clean URLs, the complete sitemap and aliases.
New tests cover consent/publication/price/turnaround gates, 137 route metadata,
local links and unchanged media/registry; seven widths across homepage, overview,
Our Work and every service; occasion history and empty states; contextual enquiries;
project-viewer fixtures; 50 exact redirect rules and staging indexing protection.

The local redirect/header test is a simulation. The browser suites block external
requests or inspect/mock enquiry intent; no real WhatsApp message or form request
is sent. All final test/audit results, logs and screenshots are saved outside the
website checkout at `/workspace/artifacts/customer-journey-v1/`.

## Final verification results

- Full build and `--check`: passed, including 137 canonical sitemap URLs.
- Twelve static/build/calendar/media checks: all passed; original photos, V3
  styling, registry and prior inventory entries verified unchanged.
- Fourteen browser suites: all passed, including Customer Journey, the in-memory
  project viewer, all routing rules, Collections V3, phase1/phase2, homepage and
  delivery, page metadata, shared header, discovery, About and Contact.
- Seventy page/viewport combinations cover the homepage, Our Work, Services and
  all seven service details at 320/360/390/430/768/1024/1440px. Additional existing
  regression suites cover gallery and legacy route layouts.
- Axe 4.14.0: 26 mobile/desktop scans, zero violations for WCAG 2 A/AA, WCAG 2.1 AA
  and best-practice tags. This does not establish complete accessibility conformance.
- All 50 permanent redirect rules and staging/preview HTTP noindex behavior passed
  the local Pages simulation, including queries/fragments and no redirect chains.

Lighthouse 13.6.0, Chromium 154, one cold run per page/preset, standard mobile and
desktop presets, local static server and external HTTPS requests blocked:

| Page | Mobile performance | Desktop performance | Mobile LCP | Mobile TBT |
| --- | --- | --- | --- | --- |
| home | 91 | 100 | 1.7 s | 370 ms |
| services | 99 | 100 | 1.8 s | 70 ms |
| custom-tailoring | 100 | 100 | 1.2 s | 10 ms |
| garment-care | 100 | 100 | 1.5 s | 20 ms |
| our-work | 100 | 100 | 0.9 s | 10 ms |
| collections | 98 | 100 | 2.3 s | 30 ms |

Accessibility, best practices and SEO scored **100** for all 12 audits; CLS was
**0** throughout. Homepage mobile TBT was 370ms in this sample, the largest measured
remaining performance cost. These are real local diagnostics, not production
PageSpeed scores, field Core Web Vitals or real-user INP. Shared-machine scheduling,
local transport and deployment caching differ from production. Reports/logs are
available beside the screenshots; no production performance improvement is claimed
without a deployed comparison.

Screenshots cover all seven services, the homepage, Services overview and Our Work
at 390px and 1440px. Filenames include `home-390.png`, `services-1440.png`,
`services-garment-care-390.png`, `services-garment-care-1440.png`,
`services-custom-tailoring-390.png` and `our-work-1440.png`. Images are fully decoded
before full-page capture. No fake customer story screenshot is presented as real.

## Owner decisions needed

Required before publishing the corresponding content or claiming a complete
customer-project/garment-care offering:

1. **Care offerings and operation:** which candidate services actually exist,
   operating model (in-house/partner, where relevant), accepted garments, treatment
   options, exclusions, assessment requirements and permission to publish them.
2. **Care pricing and logistics:** approved garment/service RWF rates, additional
   charges, estimated standard timing, express eligibility/fees, and any confirmed
   collection/delivery area, charges and scheduling. Leave unconfirmed fields gated.
3. **Customer projects:** identify actual completed Mr Sewing work and map each photo
   to its project; supply publication permission, approved factual title/context,
   any documented request/process, and optional separately approved testimonial.
   Confirm continuing permission for the existing identifiable homepage/archive
   photographs. No invented customer details are needed or accepted.
4. **Current service arrangements:** confirm mobile-fitting coverage/visit fees and
   scheduling, express capacity/charges, and applicable garment-care eligibility.
   Current pages request direct confirmation rather than publishing guessed terms.
5. **Release verification:** inspect staging and verify the Cloudflare build for the
   delivered commit. Approve production separately. Terms, Privacy and final
   production-readiness review remain the owner's planned next phase.

Optional improvements that can follow launch: richer approved stories, additional
verified care categories, original authorized service photography, stronger
verified garment descriptions/occasion metadata, competitor customer-journey
research once network access is available, and ongoing search/performance review.
