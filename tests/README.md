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
