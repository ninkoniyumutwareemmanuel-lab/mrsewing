# Measurements Guide and future-page preparation

Staging-only work on `phase1/customer-journey-repairs`, based on `171ba92c9c872382010ceee9cb514473d7e69acf`. Main/production must not be merged or deployed without a later explicit owner instruction.

## Review destinations

| Page | Route | State |
| --- | --- | --- |
| Measurements Guide | `/measurements/` | Existing page restyled, original content retained |
| Shop | `/shop/` | Existing Coming Soon page, now links to two preparation pages |
| Shop Collections | `/shop/collections/` | New Coming Soon draft |
| Shop Ordering | `/shop/ordering/` | New Coming Soon draft |
| Loyalty Program | `/loyalty-program/` | New Coming Soon draft |
| Referral Program | `/referral-program/` | New Coming Soon draft |
| Garment Care | `/services/garment-care/` | Existing hub, now links to existing care subpages |
| Care options | `/services/garment-care/services/` | Existing guidance retained |
| Quotes and planning | `/services/garment-care/planning/` | Existing guidance retained |

The guide now uses the homepage's shared header/footer, responsive typography and an accessible native-dialog illustration viewer. All twelve original illustrations and individual measurement instructions, four existing answers, canonical URL, social metadata and structured data are preserved. The original image links remain usable without JavaScript.

A Measurements Guide link is added to shared navigation and footer. Header spacing is adjusted at smaller desktop widths to accommodate it. Regenerating these components necessarily updates the shells of existing collection, service, FAQ and project pages. Their unrelated content, metadata and photographs are preserved. Homepage Loyalty and Referral previews now link to their corresponding Coming Soon pages. The Complimentary Photoshoot preview remains unchanged.

Shop navigation establishes two neutral preparation destinations without creating products, checkout, ordering terms or availability. No reward benefits, enrollment, prices, eligibility rules or launch dates are introduced. Existing Garment Care pages are reused rather than duplicated; unpublished care categories remain gated.

## Publication and search boundaries

The guide's existing indexability and metadata are unchanged. Four new preparation pages use `noindex, follow`, and the existing staging-host safeguard applies `noindex, nofollow` on `*.pages.dev`. Draft pages are excluded from the sitemap. The existing sitemap remains byte-identical at 160 URLs. Robots, redirects, headers, business identity/Maps information, hero behavior, policy text, customer facts, form endpoints and media are unchanged.

The implementation follows the repository's static Python generation workflow. No production hosting, DNS, Search Console, payment integration or form-provider settings are changed.

## Validation

- `python3 scripts/build_site.py --check`: passed.
- All 14 applicable Python test suites: passed.
- `git diff --check`: passed.
- Browser review of ten page types at eight iframe viewport widths (320, 390, 600, 768, 1099, 1100, 1280, 1440): 80 combinations, no horizontal overflow; one H1 per page.
- Mobile navigation opens and exposes the guide link.
- Guide illustration viewer opens, closes with Escape and restores focus; scroll lock is released.
- Desktop and narrow guide layout and Shop hub visually reviewed.

Older phase-specific tests compared complete generated files byte-for-byte. Those assertions now allow the explicitly authorized shared shell regeneration while retaining unrelated content/metadata comparisons and exact media, policy, integration and source-data checks. The new `tests/measurements_preparation.py` verifies original guide evidence, exact shared guide-only link additions, draft indexing gates and protected configuration.

These checks do not establish browser coverage beyond the reviewed Chromium environment or guarantee Google indexing.

## Future editing

Guide data: `_data/measurements.json`; markup/style/viewer: `_templates/measurements.*`; generator: `scripts/build_measurements.py`.

Draft destinations and navigation: `scripts/preparation_pages.py`; draft styling: `_templates/preparation.css`; existing Shop and care information: `scripts/build_completion.py`; care hub: `scripts/build_journey.py`.

Business decisions, product details and program conditions should be added only when confirmed by the owner. Rebuild with `python3 scripts/build_site.py` and verify with `--check` after source edits. Do not edit generated outputs alone.
