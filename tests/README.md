# Phase 1 browser checks

Start the existing static site from the repository root:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

With Playwright available to Node and Chromium installed:

```sh
node tests/phase1.spec.cjs
```

Optional environment variables: `REVIEW_BASE_URL` (default `http://127.0.0.1:8000/`) and `CHROMIUM_PATH` (default `/usr/bin/chromium`). In the prepared cloud environment Playwright is already installed; expose its module directory through `NODE_PATH=/opt/codex/runtimes/codex-primary-runtime/dependencies/node/node_modules` if needed.

The suite blocks all external requests. Form requests are intercepted and fulfilled with controlled responses; no live submission or customer message is sent. It checks all complete pages and rendered local links/assets, gallery keyboard interaction, responsive overflow, corrupted/unavailable storage, explicit form success, rejection, malformed/failed responses, duplicate submissions, consent toggling, measurement requirements, invalid phone numbers, and timeout recovery.

External icon styles/fonts are intentionally blocked. These checks do not establish live delivery, external account configuration, real appointment availability, Safari/Firefox compatibility, or full accessibility compliance.

## Static homepage generation and checks

The homepage reuses sections from the existing source pages at build time, so it
needs no runtime HTML fetches. After changing a shared header/footer, source
section, or `_templates/homepage.html`, regenerate and commit `index.html`:

```sh
python3 scripts/build_homepage.py
python3 scripts/build_homepage.py --check
node tests/homepage.spec.cjs
```

The script uses Python's standard library only and never edits standalone source
pages or image bytes. It copies section markup/styles, excludes document metadata
and component scripts, and adds intrinsic image dimensions. The generated HTML is
committed, so GitHub Pages and Cloudflare require no new build settings.

The homepage tests additionally check source synchronization, one H1/canonical,
metadata isolation, hero preloading, deferred scripts, image sizing/lazy loading,
absence of runtime component requests, navigation without JavaScript, slider
controls and WhatsApp consent. The WhatsApp destination is observed locally and
its navigation is prevented; no messages are sent.

## Business structured data

`_data/business.json` is the shared business identity, contacts and confirmed
working schedule. It reuses the existing contact-page branch addresses and phone;
no coordinates, reviews or ratings are invented. Weekend `00:00`/`00:00` entries
explicitly mean closed, not 24-hour opening. Legitimate about-page extra fields
and nonbusiness product/FAQ/navigation data remain separate.

After an authorized business-information change:

```sh
python3 scripts/sync_business_schema.py
python3 scripts/build_homepage.py
python3 tests/business_schema.py
```

The synchronizer updates static JSON-LD, not runtime scripts or form-service
account settings. Public email addresses/mailto links and visible hours must
also match the confirmed information. The static tests can additionally validate
all declared types, properties and domains against an official Schema.org
all-layer Turtle vocabulary downloaded separately:

```sh
python3 tests/business_schema.py --vocabulary /path/to/schemaorg-all-https.ttl
```

No network request or new package dependency is needed by either script. These
checks do not promise Google rich-result eligibility or verify mailbox delivery.
