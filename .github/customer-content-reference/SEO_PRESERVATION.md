# Mandatory SEO workflow
Applies to every future website update. Owner authority:12November2026, R41.

## Before editing
Capture the affected page’s current title, meta description, H1 and supporting headings, canonical, image alt text, internal links, JSON-LD, sitemap membership and robots behavior. Consult the current approved company reference; preserve valuable content/URLs and verified business details. Record intentional changes in the task brief.

## Two levels of search intent
Shared identity: Mr Sewing Fashion, also searchable as Mr Sewing; verified Kigali, Rwanda location. The homepage targets broad local tailoring/tailor shop searches. Each indexable page has a distinct primary topic, documented in `_data/seo-search-intent.json`; secondary topics must match its content. Preserve existing useful phrases and avoid repetitive keyword lists. Use natural language for headings, descriptions, alt text and descriptive links. Never invent addresses, LocalBusiness facts, available services or guarantees.

Men’s Suits: men’s suits, custom suits, men’s tailoring in Kigali.
Women’s Suits: women’s suits, women’s tailoring in Kigali.
Kaunda: Kaunda suits, Kaunda suit tailoring in Kigali.
Special Tailoring: custom clothing, custom shirts, dresses, trousers, coats; preserve the enquiry route’s existing noindex.
Garment Care: garment cleaning and verified garment-care services.

## After editing
Run `python tests/seo_preservation.py` and `python tests/sitemap_discovery.py`, relevant builder checks and browser heading/link/responsiveness tests. Compare affected metadata with the pre-edit audit. Check local link targets, single nonempty title/description/H1, unique canonical/title across indexable pages, image alt attributes and JSON-LD syntax. Audit intentional heading/alt/link/schema changes, not just presence. Validate any new structured business facts against approved sources. Keep staging X-Robots-Tag and browser noindex protections intact; canonical production URLs do not authorise indexing staging. Do not infer staging response headers from local files alone.

## Required report
State what was preserved, what intentionally improved and what remains unverified. Distinguish syntax checks from Google rich-result eligibility and local files from live responses. No Google ranking guarantees, unapproved production changes or blanket metadata rewrites.
