# R47 — Technical SEO committed-source audit

Audit date: 13 November 2026. Read-only comparison of production-branch commit `4d972f29417fa60366ebdb6348e1599208f6ae08` and reviewed staging commit `ce312f68b9ace4bd7d5df0334589007ff329a0e8`.

**Scope distinction:** these findings describe Git snapshots and initial HTML, not current production HTTP status, X-Robots-Tag response headers, CDN caching, Googlebot responses, browser rendering or Google indexing. Actual endpoint verification and mobile browser evidence are separate parts of the parent task. No product code, indexing state or production settings were changed by this source audit.

## Priority pages

Every priority page in both snapshots has one nonempty title, one meta description, one H1, a production HTTPS apex self-canonical, and `index, follow`. Titles and descriptions distinguish each page's actual service intent and preserve Mr Sewing Fashion / Kigali identity. Main content and ordinary destination anchors are present in initial HTML; JavaScript is not required to discover the main services. Main text counts below document availability, not search-quality scores or ranking thresholds.

| Route | Local production-source indexing | Sitemap: main / staging | Initial main words: main / staging | HTML links from homepage | Missing local resources / internal destinations |
| --- | --- | --- | --- | --- | --- |
| `/` | `index, follow` / self-canonical | Yes / Yes | 1164 / 1164 | 0 | None / None |
| `/services/custom-tailoring/` | `index, follow` / self-canonical | Yes / Yes | 1056 / 1481 | 1 | None / None |
| `/services/alterations/` | `index, follow` / self-canonical | Yes / Yes | 424 / 424 | 1 | None / None |
| `/services/garment-care/` | `index, follow` / self-canonical | Yes / Yes | 352 / 352 | 1 | None / None |
| `/services/mobile-fitting/` | `index, follow` / self-canonical | Yes / Yes | 363 / 363 | 1 | None / None |
| `/services/vip/` | `index, follow` / self-canonical | Yes / Yes | 199 / 199 | 1 | None / None |
| `/mensuits/` | `index, follow` / self-canonical | Yes / Yes | 105 / 91 | 1 | None / None |
| `/womensuits/` | `index, follow` / self-canonical | Yes / Yes | 94 / 71 | 1 | None / None |

Resource checks resolve each page's actual `<base href>` and percent-encoded/Unicode file paths. All referenced local images/srcsets, scripts, stylesheets and declared icons exist in the corresponding Git snapshot. All local anchor destinations on these pages resolve to files. The root `/favicon.ico` fallback request is a separate historical-resource question: declaring an existing PNG icon does not establish the root ICO response.

The homepage links to Custom Tailoring, alterations, garment care, mobile tailoring, VIP, Men's Suits and Women's Suits using ordinary HTML anchors in existing customer navigation/content. Each is reachable in one click; no artificial discovery links or keyword repetition are justified by these checks. Every sitemap-listed route is reachable through the ordinary HTML link graph in each snapshot (55/55 main; 64/64 staging).

JSON-LD parses on all priority pages. Existing types are WebSite/SiteNavigationElement (home), WebPage/BreadcrumbList/Service (service pages), and CollectionPage/BreadcrumbList (men/women). This validates syntax and source presence only; it does not certify Google rich-result eligibility or add unsupported LocalBusiness facts. Existing heading hierarchy and image alt data should remain unchanged unless a separate verified defect is found.

## Exact sitemap difference: 55 to 64

All 55 main sitemap URLs remain in staging. The only nine additions are:

- `/collections/designs/ms-029/`
- `/collections/designs/ms-030/`
- `/collections/designs/ms-031/`
- `/collections/designs/ms-032/`
- `/collections/designs/ms-033/`
- `/collections/designs/ms-034/`
- `/collections/designs/ms-035/`
- `/collections/designs/ms-036/`
- `/mensuits/kaunda/`

These are the Men's Kaunda category and eight explicitly authorized historical references MS-029 through MS-036. Approval evidence: `KAUNDA_RESTORATION_BRIEF_2026-11-12.md`, `KAUNDA_PUBLICATION_APPROVAL_2026-11-12.json`, source-model memberships and R40. This difference reflects a scoped staging-approved collection addition, not nine arbitrary forms or unfinished products. Production publication still requires separate owner authorization. Preserve these staging entries and the existing 55; do not replace 64 with 55 blindly or infer production publication approval from sitemap eligibility.

No forms, Selected Designs review, fabric preference flow, Special Order enquiry, private/staff areas, held design references or unapproved merchandise are introduced into the sitemap. URLs use `https://mrsewingfashion.com`; no Pages staging hostname is in either XML document. Existing sitemap tests check XML, unique canonical routes, intended indexability and transactional exclusions.

## `/services/` discrepancy and approved purpose

**Neither inspected sitemap contains `/services/`.** Both Git snapshots have identical `/services/index.html`: a useful Our Services directory with five service links, canonical `https://mrsewingfashion.com/services/`, and deliberate `noindex, follow`.

Evidence:

- Commit `5df5a8a5267258e94d66df0b48c5d5a4484278e4` (6 November), “Limit SEO indexing to 14 owner-approved public routes,” introduced the explicit `INDEXABLE_ROUTES` allowlist excluding `/services/`.
- Commit `6550b88d32f702e7a80d03a4639dc89ea4355c0d` expanded the sitemap to 55 without adding `/services/`.
- Current `scripts/site_seo.py` still excludes the directory from its indexable-route allowlist while including the individual approved services.
- The early page-map row labeling `/services/` “Indexable” is historical documentation conflicting with the later scoped allowlist. Preserve historical records and record the current resolution; do not silently enable indexing based on that older row.

Safe recommendation: retain the hub's existing `noindex, follow` and sitemap exclusion. If actual live XML includes it, correct the live/deployment/generated-output mismatch after obtaining that response; the owner's reported discrepancy is not confirmed by the inspected Git versions. Indexing the directory itself would require explicit approval of a changed indexing purpose.

## Host, canonical and staging protection

`robots.txt` allows crawling and points to the production canonical sitemap. `CNAME` contains `mrsewingfashion.com`. Priority-page canonicals consistently use HTTPS apex; no www or Pages canonical is present in the inspected documents. Source alone does not establish apex/www redirect behavior, HTTP-to-HTTPS hops or Cloudflare security responses.

`_headers` scopes `X-Robots-Tag: noindex, nofollow, noarchive` to `https://mrsewing-staging.pages.dev/*` and preview subdomains using the existing host-qualified pattern. It does not contain an unqualified production-wide noindex rule. The shared inline staging guard changes robots to `noindex, nofollow` only on hostnames ending `.pages.dev`; it does not match `mrsewingfashion.com` or `www.mrsewingfashion.com`. Preserve both protections and verify actual host responses independently. No recommendation to disable security, change production settings or alter the enquiry backend follows from this audit.

## Conclusions and held questions

Confirmed source results: the priority routes have consistent local indexing/canonical/sitemap rules, crawlable service links, initial HTML content and present local resources; the 55-to-64 delta is entirely authorized Kaunda collection content; `/services/` is already excluded in both inspected sitemaps.

These checks establish **no root cause** for the owner's 152 “Discovered” or 16 “Crawled” indexing exclusions. URL-level Search Console exports, Google's selected canonical, latest crawl time/rendered HTML, and actual apex/www responses are still needed. Historical 404 requests can be legitimate removals; current source results do not justify homepage redirects, blanket indexing changes or speculative content rewrites. Preserve the approved design, forms, prices, benefits, photographs and two-level SEO strategy.

Machine-readable evidence: `/workspace/review/technical-seo-2026-11-13/source-audit.json` (both immutable snapshots, page metadata/headings/schema, initial HTML links/resources and exact sitemap delta). The parent release report supplies current mobile tests, actual network limitations and any narrow repairs.
