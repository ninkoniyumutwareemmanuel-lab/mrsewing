# R47 — Local Cloudflare Pages routing verification

Date: 13 November 2026. Baseline: `ce312f68b9ace4bd7d5df0334589007ff329a0e8`. These experiments used read-only GET requests against a local Wrangler 4.46.0 Pages development server. They do **not** establish the responses currently received from production, deployed staging or Googlebot.

## Confirmed hosting behavior

Cloudflare's official [Serving Pages documentation](https://developers.cloudflare.com/pages/configuration/serving-pages/) states that a site without a top-level `404.html` is treated as a single-page application and unmatched paths serve the root document. The [official source inspected for this audit](https://raw.githubusercontent.com/cloudflare/cloudflare-docs/production/src/content/docs/pages/configuration/serving-pages.mdx) also documents how an explicit `404.html` handles missing files.

The baseline repository has no top-level 404 document. Its Pages Functions match `/api/*` and `/shop/*`; no global middleware or arbitrary-path catch-all overrides the historical URLs in this test.

An isolated fixture copied 14 files directly from the baseline commit: the actual homepage and priority service/collection HTML, `/services/` directory, real `_headers` and `_redirects`, robots, sitemap and the original logo PNG. No product files were changed by the fixture experiment.

| Local fixture request | Before: no root 404 document | After: only a temporary root 404 document added |
| --- | --- | --- |
| Eight priority service/collection URLs | 200, their actual HTML | 200, byte-identical HTML |
| Nine supplied obsolete URLs plus one deliberately nonexistent URL, including the then-missing root favicon | 200 with the exact homepage body | Genuine 404 with the error document |
| `/services/` | 200 | 200 |
| Two representative existing exact aliases | 301 to existing destination, query preserved | Same single-hop 301 and query |

This confirms the soft-200 fallback in the **local Pages static-serving implementation** and verifies the explicit-404 repair. Production's `CNAME` identifies `mrsewingfashion.com`, and its hosting behavior may differ; production might already return legitimate 404 responses. The experiment does not prove that production currently has a soft-404 problem or that this explains Search Console indexing delays.

## Repaired repository verification

The complete repaired repository was then served with `wrangler pages dev . --local --port 8031 --ip 127.0.0.1 --compatibility-date=2026-11-13`. Its actual Pages Functions compiled successfully. No customer submission, message, payment, database binding or private feature was activated.

| Check | Local result |
| --- | --- |
| All eight priority pages | 200 |
| All 64 canonical sitemap destinations | 200 |
| `/product-category/sewing-for-you/`, both supplied historical product-feed paths, `/feed/`, `/comments/feed/`, both unknown detail filenames, `/style.css`, and a random nonexistent route | 404, actual Page Not Found body, `noindex, follow` meta |
| `/favicon.ico` | 200, valid icon MIME type |
| `/assets/images/favicon-192.png` | 200, `image/png` |
| Original `/assets/images/logo-icon.png` | 200 |
| `/robots.txt`, `/sitemap.xml`, selection JavaScript and Custom Tailoring stylesheet | 200 |
| All 50 existing exact redirect rules | 301 followed by destination 200 in one hop; test query preserved; no loops |
| `/services/` | 200 with existing `noindex, follow`; no indexing-status change |

The new favicon correctly replaces the missing-icon request, so it is no longer expected to remain 404. No redirect was created for unsupported historical content. Existing approved service and collection URLs continue to resolve.

## Evidence and limits

Local evidence in the shared review workspace:

- `/workspace/review/technical-seo-2026-11-13/hosting-before.json`
- `/workspace/review/technical-seo-2026-11-13/hosting-after.json`
- `/workspace/review/technical-seo-2026-11-13/hosting-experiment.json`
- `/workspace/review/technical-seo-2026-11-13/hosting-repository.json`

The temporary fixture server ran on port 8030; the repaired repository server ran on 8031. Wrangler parsed the existing 50 redirect rules and two header rules. Its optional `Request.cf` bootstrap fetch was blocked and used a default placeholder; the actual static requests and local Functions compilation succeeded.

These were local HTTP requests. Host-qualified HTTPS `X-Robots-Tag` behavior on apex, www, the staging root domain and preview domains still requires actual network verification. The source rules were preserved, but no claim about deployed response headers, security challenges, caches, Googlebot or indexing is inferred from this test.

Production publication remains held for owner approval. This audit did not merge into main, change production settings or deploy production.
