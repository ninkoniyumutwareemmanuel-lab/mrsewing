# Priority technical SEO audit — 13 November 2026

Scope: Mr Sewing Fashion / Mr Sewing, Kigali, Rwanda. Production-source baseline `4d972f29417fa60366ebdb6348e1599208f6ae08`; staging implementation baseline `ce312f68b9ace4bd7d5df0334589007ff329a0e8`; branch `phase1/customer-journey-repairs`. **Staging only. Production publication requires separate owner approval.**

## Findings and limits

There is **no confirmed root cause for Google's indexing delays**. All eight priority pages pass committed-source and local rendering checks. Two safe technical repairs were established and implemented: conventional/square favicon support and an explicit static-host404 boundary. Neither establishes that Google will index a page, and neither proves a production-wide crawling block.

| Finding | Evidence | Remedy and current state |
| --- | --- | --- |
| Missing conventional root favicon | `/favicon.ico` absent in both inspected Git versions; existing declared PNG is192×124, not square | Added valid multi-size ICO and192×192 transparent-padded PNG from the existing approved logo. Original artwork/asset unchanged. Current ordinary favicon links use the square PNG with correct MIME declarations. Local retrieval passes. |
| Cloudflare unmatched paths fall back to homepage200 | No root404.html in baseline; official Cloudflare serving documentation and local Wrangler before/after reproduction | Added branded, noindex404.html with genuine navigation links and no canonical-to-home redirect. Complete repaired repository returns404 for unsupported historical/random paths,200 for all64 sitemap routes. This confirms local Pages behavior, **not the current production response**. |
| Priority services already discoverable/indexable in source | Eight pages have indexfollow, self-canonical HTTPSapex, unique titles/descriptions/H1, initialHTML content, valid JSON-LD syntax and present resources; seven non-home destinations linked directly from home | Preserve existing content, keywords, internal links and metadata. No artificial link or keyword rewrite justified. |
| Sitemap55 vs64 | Immutable main/staging XML comparison | Exactly nine additions: approved Men's Kaunda category and MS029–MS036 pages. No existing URL removed. Keep coherent staging64; production55 remains unchanged pending an appropriately scoped release. |
| Reported `/services/` sitemap/noindex mismatch | Neither inspected sitemap includes this URL. The directory's deliberate noindex follows the approved route allowlist; early page-map “Indexable” label is superseded | Preserve noindex and sitemap exclusion. Current live discrepancy remains unverified; obtain the actual served XML/headers before any live correction. |
| Historical URLs lack verified equivalents | No matching current internal references or proven replacement identities in available585-commit history | No new301 rules. Retain genuine404 for feeds/unknown detail/style paths; request exact upload filenames before assessing any image replacement. |

No sitemap, robots, `_headers`, redirect rules, canonical structure, public brand/location facts, service prices, images, business policies, selection/quotation code, providers, payments or private features were changed. Generated page changes concern favicon links only. The generated staging Shop HTML has the same favicon-only normalization; commercial restrictions are preserved.

## Owner-provided Search Console observations

The owner reported on13November:152 discovered/not-indexed;16 crawled/not-indexed;2 redirect URLs;1 alternate with proper canonical; sitemap successfully processed with55 discovered URLs; Custom Tailoring live test available/indexable;713 crawl requests;47ms mean response; host normal;83%200 and12%404;7% discovery/93% refresh.

These are owner-provided observations, not retrieved exports or a new Google test. They show crawling activity but do not identify which important pages are affected, establish response quality for every URL, prove all404s harmful, or justify removing security protections. Redirect and alternate-canonical states can be expected for legitimate aliases. The counts alone do not diagnose content quality, crawl scheduling, duplication or indexing demand.

## Production network verification

Attempted25 read-only endpoint checks covering all eight priorities, `/services/`, robots, sitemap, declared logo, favicon, style, exact historical examples, a random missing route, HTTPSwww and HTTPapex/www. The managed outbound proxy blocked HTTPS CONNECT with403; plainHTTP requests were likewise denied by the proxy. **No origin response was verified.** This is not a production HTTP403 finding or evidence Googlebot is blocked.

Consequently, production status, X-Robots-Tag, apex/www and HTTPS redirect chains, CDN/security/cache behavior, live missing-resource statuses, actual rendered mobile output and Googlebot responses remain unverified. Local tests and Git source do not replace these checks. Complete `/wp-content/uploads/2023/08/...` filenames were not supplied, so no exact asset request/mapping is claimed. Actual deployed staging access is attempted separately after release and distinguished from Cloudflare's deployment status.

Raw request evidence: `/workspace/review/technical-seo-2026-11-13/production-http.json` plus captured headers. Existing production-source metadata and each priority-page comparison are detailed in [source audit](SEO_SOURCE_AUDIT_2026-11-13.md). Historical dispositions and exact paths are in the [historical URL table](SEO_HISTORICAL_URL_AUDIT_2026-11-13.md). The [hosting audit](SEO_HOSTING_AUDIT_2026-11-13.md) contains official documentation and actual local Pages responses.

## Verification completed

- Build and generated-output consistency checks pass.
- Existing SEO/sitemap checks pass for64 unique canonical indexable routes, correct production domain, no transactional/private/draft entries, intentional directory exclusion and staging noindex source rules.
- New static guard preserves293 existing HTML pages except ordinary iconhref/MIME corrections and565 protected files with two narrow exceptions: one non-garment favicon inventory entry and the same icon normalization inside generated Shop HTML. No customer journey or provider logic changed.
- Local Pages server: all eight priorities and64 sitemap routes200; nine removed/random probes404 with real error body; faviconICO/PNG and real current resources200; all50 existing exact aliases remain one-hop301→200 with query preservation and no loops.
- Browser: eight priority pages at320,390,768,1440px (32 views), custom404 at four widths, image decoding, no horizontal overflow, working header navigation, three scoped axe checks and eight synthetic staging-host noindex checks. Synthetic host tests are not real HTTPSheader verification. Screenshots inspected at390/1440.
- Existing expiration, mixed-design sharing and selected-suit quotation regressions pass at all eight journey widths, including Back/Forward,60/121-second cases, two quotation flows, exact photographs/quantities/fabrics, validation and mocked provider failure/success. Legacy single-design quotation passes. No real WhatsApp messages, enquiries or payments.
- Structured data syntax and preserved schema values checked; no new LocalBusiness claims or external Google rich-result certification.

Evidence: `/workspace/review/technical-seo-2026-11-13/test-summary.json`, `technical-static.json`, `browser.json`, `hosting-repository.json`, `seo-after.json` and local test logs.

## Remaining evidence and next steps

Need exact affectedURLs from the16 crawled/not-indexed and152 discovered/not-indexed reports; actual inspected canonical choices/last-crawl dates; the2redirect and1alternate URLs; complete legacy upload filenames; live XML and production/wwwhost responses from an accessible network. Do not substitute guessed mappings, fabricated content or automatic homepage redirects.

Possible causes requiring this evidence include normal crawl/indexing scheduling, obsolete URLs mixed into reports, duplicate/reference-page relationships and page-specific indexing/content evaluations. No source evidence currently establishes these as causes or supports a universal ranking/ indexing guarantee.

Review the [production release proposal and Search Console plan](TECHNICAL_SEO_RELEASE_PLAN_2026-11-13.md). Exact changed paths are in [file manifest](TECHNICAL_SEO_CHANGED_FILES_2026-11-13.txt). The final owner report supplies the exact staging commit/deployment status and preview URL after the actual release check. Stop after staging; no main merge or production deployment.
