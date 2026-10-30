# About Us V2 — staging review

Baseline staging commit: `1fce4f52b9b724a30f3647fee7169f10e0c73ec2`.
Branch: `phase1/customer-journey-repairs`.
Preview: https://mrsewing-staging.pages.dev/about/

## Implementation

Brand-focused editorial story using the owner-approved facts: family inspiration,
2019 establishment, small-workshop beginnings, locally made personalized clothing,
and the founder's present involvement. No biography, executive portrait, invented
milestones, growth figures, prices or financial promises. The page includes the
2019/present timeline, approved mission and vision, five values, seven services,
customer approach, subtle parent-company acknowledgment and exactly two final
CTAs to existing `/collections/` and `/contact/` destinations.

The portrait is the existing approved `r4.jpeg` customer photograph, used once.
It uses existing responsive AVIF/WebP derivatives, no new crop, explicit image
dimensions and eager/high-priority loading. No new or generated photography.
Future workshop photography can replace this editorial figure through the About
image/template block, with verified derivatives, dimensions and alt text; no
header/footer or overall page redesign is required.

`_templates/about.html` and `about.css` are maintained sources.
`scripts/build_about.py` renders them with the existing shared header, footer,
common CSS, local SVG icons and menu controller. It reads About-only metadata
from the existing SEO data. About now participates in the standard build:

```sh
python3 scripts/build_site.py
python3 scripts/build_site.py --check
```

Both the root legacy source and clean `/about/` output are generated, together
with a small About menu script. Legacy query strings/fragments and existing
order bookmarks remain compatible. No client-side component HTML fetching.

## Verification

- All nine established browser suites passed: homepage-journey, homepage, header,
  page-seo, homepage-optimization, phase1, phase2, image-delivery, agentic-discovery.
- Contact's existing browser suite and the new About-specific suite passed.
- About tests cover all seven widths (320, 360, 390, 430, 768, 1024, 1440), story,
  parent company, 2019, five values, seven services, CTA navigation, shared footer,
  responsive AVIF selection, menu keyboard/Escape/outside/link interactions, no
  horizontal overflow, no missing images/page errors, local links, legacy URLs,
  metadata/JSON-LD and content available without JavaScript.
- Build consistency, metadata synchronization, shared-component propagation,
  clean URLs, business/calendar checks and image/media checks passed.
- JSON-LD parses; 437 typed nodes site-wide validate against the supplied official
  Schema.org vocabulary and property domains. About uses AboutPage, Organization
  (founding year and parent organization) and BreadcrumbList, with no ratings,
  fabricated reviews or registration claims.
- One H1, production `/about/` canonical, Open Graph/Twitter metadata and an
  existing optimized social-preview photograph. Only About's SEO data changed.
- Homepage, Contact sources/generated pages, their JS and all shared components
  are byte-for-byte unchanged. Mobile (390px) and desktop (1440px) full-page
  before/after captures are pixel-identical for both approved pages.
- Sitemap, robots, business identity/hour data and policy pages are unchanged.

Local Lighthouse synthetic results (not field Core Web Vitals):

| Profile | Performance | Accessibility | Best practices | SEO | LCP | CLS | TBT |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Mobile | 100 | 100 | 100 | 100 | 1.4 s | 0 | 10 ms |
| Desktop | 100 | 100 | 100 | 100 | 0.3 s | 0 | 0 ms |

Screenshots, comparison captures, nine-suite logs and Lighthouse JSON are in
`/workspace/phase1-review/about-v2/`; About review captures are `about-390.png`
and `about-1440.png`. Automated checks do not replace owner visual approval or
establish full accessibility compliance on every browser/assistive technology.

## Limitations and safety

External staging access is blocked at the environment proxy (CONNECT 403).
Cloudflare's deployed revision and staging indexing protection cannot be
independently verified. Production indexing directives/canonicals were preserved;
no global noindex or hosting change was introduced. CTA navigation was exercised
locally; external services/real booking delivery are not proven by these tests.
All existing form regression submissions were intercepted, not sent to customers
or live services.

No main changes/merge/publication, branch creation, DNS/hosting changes, new
prices, policy changes or Collections V2 work. Owner visual approval is required
before the next stage or any production action.

## Exact changed files

- `_data/page-seo.json`
- `_templates/about.css`
- `_templates/about.html`
- `about.html`
- `about/index.html`
- `assets/about-navigation.js`
- `docs/about-v2-validation.md`
- `docs/shared-components.md`
- `scripts/build_about.py`
- `scripts/build_site.py`
- `tests/README.md`
- `tests/about-v2.spec.cjs`
- `tests/business_schema.py`
- `tests/header.spec.cjs`
- `tests/shared_components.py`
