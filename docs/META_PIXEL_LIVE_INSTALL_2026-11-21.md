# Live-site Meta Pixel code placement — 21 November 2026

Owner requested direct deployment to main on 21 November 2026. Source staging preparation commit 7f2bda869fab476775206049adf22535354ced54. The requested ID is 29683883327873735.

Only the Pixel integration support is copied to main, without merging incomplete R51–R53 site redesign or staging content:
- _data/meta-pixel.json: productionEnabled remains false.
- _templates/customer-interactions.js: optional first-party loader, guarded by explicit owner-approved-production status.
- scripts/customer_site.py: source-driven synchronisation of the generated browser asset from the approved config.
- assets/customer-interactions.js: generated browser asset.
- assets/meta-pixel.js: consent-gated implementation prepared on staging, does not execute while productionEnabled=false.

The existing live HTML already references /assets/customer-interactions.js on the homepage and current canonical pages. No existing customer journey or page content is changed. Meta Pixel requests are **not active** and no marketing-consent panel appears until the follow-up activation.

Before activation:
1. Present updated privacy disclosure to owner for approval, then publish approved policy text.
2. Verify legal requirements under Rwanda Law 058/2021, particularly consent, registration and international transfers, with appropriate responsible authority/adviser.
3. Run browser/network tests for accept/decline/withdrawal, Meta Test Events, correct Pixel ID, duplicate requests, and sensitive URL exclusion.
4. Obtain explicit activation approval. Update status to owner-approved-production and productionEnabled=true, rebuild and release through normal approved production controls.

Do not claim Meta Events Manager is receiving data from this disabled installation.
