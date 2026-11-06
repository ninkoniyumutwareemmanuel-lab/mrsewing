# Maintaining the Shop through GitHub

The single source is `_data/shop-products.json` (`schemaVersion: 1`, `products: []`). The blank `_data/shop-product-template.json` is a **draft schema template**, not merchandise. Copy a record into `products`, supply verified values and keep it `draft` until approved. Do not convert suit reference designs into ready stock.

Required publication evidence: stable ID/SKU, unique permanent lowercase slug, name/category/description, owner approval source/date, approved local image paths with real pixel dimensions/alt/permission evidence, specifications/care/ordering notes, unique SEO title/description and an approved image as `socialImage`. Optional image `responsiveSources` entries contain approved local derivative `src` and pixel `width`; they generate srcset/sizes. Images keep intrinsic dimensions and lazy loading below the main product photograph. Never include supplier costs, contact lists or private records.

Exactly three availability labels:

- **Available in Stock**: positive approved integer `priceRwf`, `priceApproved: true`, stock > 0, explicitly defined size/colour variation IDs and nonnegative integer quantities. Variation quantities must sum to `stockQuantity`. Price applies to the product's variations; different-price variants must be separate approved product records until variable pricing is explicitly implemented.
- **Available on Orders**: `priceRwf: null`, stock 0, variations defined with stock 0. Opens product quotation; no fixed/starting price is published.
- **Out of Stock**: stock 0; approved price may be retained if applicable. Details remain accessible, purchase action disabled.

Use genuine “Not applicable” values only when the product is truly unsized/has no colour choice. Do not invent options. All published records validate at build; draft/archived records produce no product page. Keep published IDs/slugs stable for shared links. Withdrawing a record removes its generated page/listing/sitemap entry on build; no redirect is invented. Add an explicit redirect only when a verified replacement exists.

Run `python3 scripts/build_site.py`, `python3 scripts/build_site.py --check`, `python3 tests/commerce_catalog.py`, `node tests/commerce-server.mjs`, then browser regression checks. The normal build regenerates `/shop/`, `/shop/{slug}/`, product schema/sharing metadata, server catalogue module and sitemap from the same data. Commit sources **and generated outputs** on the development branch; staging review before production.

## Request architecture and limitations

Cart local storage contains only public product/variation IDs and quantities. Customer names, addresses, email and payment preferences are not persisted there. Storage may be unavailable; the interface warns accordingly. Stock is a manually maintained snapshot; no real-time reservation or deduction occurs. Server validates current published catalogue, rejects unavailable/invalid/duplicate variations and reconstructs prices/subtotals. Customer totals, titles, routes, recipient and subject are never trusted. Final amount, delivery charges and payment instructions require staff verification.

`functions/api/shop-request.js` uses `functions/_lib/shop-handler.js` and build-generated `shop-runtime.js`. The latter reuses the existing site's Web3Forms publishable access key without changing provider/recipient configuration. It is not a private storage credential. No new key/account/payment service is introduced. Forms use same-origin JSON POST, origin/host checks, payload bounds, honeypot, schema validation, timeout, disabled pending controls and positive provider-response success only. Provider spam/abuse handling and inbox delivery must be verified live; no new CAPTCHA configuration is assumed. Public intake is not authenticated and is not an internal request-record system. No personal records/files/database/staff feature is enabled.

Bank Transfer and Mobile Money are preferences only; no accounts/numbers/instructions are shown. Cryptocurrency is disabled and server-rejected pending legal/operational approval. Nothing is charged, reserved, automatically approved or sent to WhatsApp. All requests use existing business email provider; acceptance does not prove inbox receipt. A timeout may mean delivery occurred; customers are told to contact Support before resubmitting.

## Before enabling real products

Owner must supply authorised merchandise/image rights, precise variations/current inventory, prices/publication approval, specifications/care and ordering conditions. Confirm applicable Shop fulfilment, delivery charges, returns/cancellation/customer rights and privacy treatment before owner publication approval. Verify the deployed email-only endpoint and real business inbox with controlled test data. Existing general Terms/Privacy are linked; no new Shop-specific refund/shipping/crypto promises are inferred. No paid services.
