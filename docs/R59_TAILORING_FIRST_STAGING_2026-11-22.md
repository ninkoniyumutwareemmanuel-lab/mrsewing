# R59 Tailoring-first staging implementation, source map and release gates
Date: 22 November 2026 | Owner's explicit full redesign prompt | **Staging only**
Base: main/staging 33620fe4dc38ec81905fd2556a19db15f5c06db3; prior R53 historical reference cb245b573156ac7805e0d5ff10accba277222175.
 
## Approved page brief and scope
Routes: / (short, professionally focused homepage), /services/custom-tailoring/ (Tailoring & Clothing Services), /collections/ (universal Showroom, optional ?gender=men or ?gender=women), /shop/ (Shop discovery), existing /terms-and-conditions/ (approved PDF reviewer) and /terms-and-conditions/current/ (still-current effective legacy HTML). VIP /services/vip/, Special /services/custom-tailoring/special-order/, alterations /services/alterations/, care /services/garment-care/, mobile /services/mobile-fitting/ unchanged in their contractual operation. No new intake/checkout, system provider, discount, price, stock or personal-data collection.

Authority: owner’s 22 November 2026 message; historical approved R41 SEO; R49/R50 customer journeys; R53 source/rights audit; R55 Terms. Read AGENTS.md and customer-content-reference/versions/2026-11-22-01; original company policy source coverage still incomplete. The site's own historical content is comparison evidence, not new business approval. Distinguish independently accepted customer quotations and verified payments from website clicks and draft form state.

Page links/buttons: existing Terms-aware WhatsApp handoff; /collections/ for all designs and ?gender men/women for two category cards; relevant service overview links; /shop/ catalog and /services/vip/ independently. No design/photo becomes a Shop product from being a reference. Forms remain existing request/selection/fabric/quote APIs, with ordinary versus VIP, Special, Care, Alterations, Mobile all separate. The homepage new link is navigation only and does not imply message receipt.

## Source of truth and generated files
| Component | Authoritative sources | Generated outputs |
|---|---|---|
| Homepage | _templates/homepage-tailoring.html, _templates/homepage-tailoring.css, _templates/homepage.html, _templates/homepage-galleries.css/.js, scripts/build_homepage.py, scripts/homepage_galleries.py | index.html, assets/homepage.js |
| Central tailoring hub | scripts/tailoring_services_hub.py, scripts/customer_site.py, _templates/tailoring-services-hub.css, scripts/custom_tailoring_mobile.py, _data/customer-release.json | services/custom-tailoring/index.html |
| Clothing categories/Showroom | _data/clothing-category-config.json, scripts/clothing_categories.py, _data/collection-designs.json, _data/suit-reference-categories.json, scripts/build_collections.py, assets/collections-v3.js | collections/index.html, static design views; mensuits/womensuits legacy routes retained |
| Photography and dates | _data/collection-designs.json, _data/collection-image-inventory.json, scripts/media_sorting.py, scripts/homepage_galleries.py | published Showroom and homepage gallery selection; unknown dates stable |
| Held videos | _data/media-video-records.json, scripts/prepare_silent_homepage_videos.py | no public silent-video files until verified rights/posters |
| Shop | scripts/shop_catalog.py, scripts/build_commerce.py, _templates/commerce.js/.css, functions/_lib/shop-handler.js, _data/shop-products.json | shop/index.html and generated assets/server runtime; sale publication unchanged |
| Terms | _data/policy-documents.json, scripts/terms_reader.py, approved immutable PDF and pages | terms-and-conditions/index.html and original/current fallback |
| Site security, privacy and SEO | existing site_seo.py, _headers, existing customer consent/Meta Pixel, R41 preserved | no new production indexing or events |

## SEO, security and accessibility commitments
Preserve original canonical URLs, one meaningful H1/page, relevant local page SEO, shared contact facts, JSON-LD and image alt; retain staging noindex policy. No new Meta Pixel or external event tracking. Use reduced-motion preference, pause/keyboard Escape for gallery movement, touch scroll without forced capture, no audio autoload, native Terms reader with accessible toolbar. Real browser outcomes must be confirmed with staged QA, not inferred from source alone.

## Publication holds
R53 25 images and both videos remain held pending explicit rights, poster, metadata and publication evidence. 22 newly prepared design groups remain not-public. The approved Terms PDF remains awaiting official activation and payment/surcharge text reconciliation. Shop has no sale-published products; enquiry-only catalogue does not equate to sale stock. Any dates missing from old media records remain unknown with stable order. No production merge.

## Test/run record
Use GitHub Actions run logs for actual pass/fail: staging python scripts/build_site.py and --check, tests/seo_preservation.py, tests/sitemap_discovery.py, tests/terms_reader_main_base.py; additional R59 media_sorting, Shop status and browser QA. Avoid claiming obsolete tests are present if absent (R53-only tests/media_showroom.py and policy_documents.py are not in new main-derived baseline). Full browser/deployed checks require separate evidence and screenshots. Current report should cite the successful final staging SHA/deployment.

## Staging-only original media URL safety
The two held original R53 videos and 25 held R53 photographs were already present as raw repository root files. To avoid directly serving them through the publicly reachable staging hostname, scripts/build_public_routes.py now creates **temporary 302 redirects to /404.html** for their exact URLs from the authoritative media records, with no separate manually maintained image list. This controls future staging Pages static responses without blocking eligible published photographs. The production branch is not changed. An independent live HTTP confirmation of these redirect responses and historical caches is still needed; do not claim that old publicly accessible preview URLs or Git history are private.
