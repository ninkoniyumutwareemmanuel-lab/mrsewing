# Pre-launch audit and release preparation — 26 November 2026

## Authority and baseline

The owner's latest **FINAL PRE-LAUNCH AUDIT AND PRODUCTION READINESS** instruction authorizes focused launch corrections, testing and a staging release candidate. It explicitly prohibits Main changes, production deployment, external tracking configuration changes and real customer notifications. Preserve the reviewed design; defer cosmetic changes.

Repository `ninkoniyumutwareemmanuel-lab/mrsewing`; authorized branch `phase1/customer-journey-repairs`. Starting staging `5c394c6483564c6759b49c903631e7da72585847`; read-back Main `33620fe4dc38ec81905fd2556a19db15f5c06db3`. Backup `recovery/prelaunch-start-2026-11-26` preserves the starting staging commit. Main is a read-only comparison source, not an implementation target.

Read `AGENTS.md`, the current reference `versions/2026-11-26-01`, customer information master, source matrix, unresolved register, page map, SEO preservation reference and source map. This technical task changes no approved commercial or contractual rule. It therefore does not supersede that reference's rule approvals or historical records. R49 measurement/delivery scopes, later quotation-first presentation, R61 media authorization, exact-photo/quantity preservation and the separate inactive Flexible Advance Payment proposal remain intact.

## Page and component brief

- **Audience/purpose:** protect the existing public website and prepare a reproducible release artifact; no new service or visible customer flow.
- **Scope:** all generated routes/aliases, public asset dependencies, middleware boundary, production projection of the current effective Terms, browser/contact/SEO regression evidence and a prepare-only release/rollback plan.
- **Service and quotation semantics:** existing selected designs, fabric/pattern/colour, contact/deadline/measurement/delivery validation, review, explicit submission and positive-provider-only acknowledgement stay unchanged. No accepted order, appointment, inbox delivery or production-start claim follows from a click/provider response.
- **Payments/delivery/benefits:** no price, payment timing, surcharge, eligibility, refund, promotion or commercial record edited. The proposed flexible arrangement stays inactive; no automatic forfeiture or cancellation rule.
- **Contacts/actions:** official business data continues to supply telephone, email and WhatsApp. Existing links open manually editable conversations; testing intercepts handoffs and never sends messages. Existing form providers and consent are retained.
- **Terms/privacy:** received actual PDF Version1.2 remains a staging-review reader with no effective date. `/terms-and-conditions/current/` remains the effective consent fallback. Production export preserves that exact effective HTML body and anchors at the existing Terms route; it does not activate the PDF or invent approval of Version1.1.
- **SEO:** retain page-specific production canonicals, title/description/H1, structured data, image descriptions, sitemap, robots and intentional exclusions. Staging noindex remains host-specific. No production-wide noindex is introduced. Local target checks are not actual production HTTP or Google indexing verification.
- **Homepage/shared impact:** no reviewed homepage design/content/navigation edit. Legacy Kaunda still needs its dynamically fetched public `header.html`; release asset closure includes this dependency.
- **Missing evidence:** actual Cloudflare/production origins and settings, Search Console, analytics account receipt, isolated real provider destination and exact approved Library Version1.1 are unavailable. Report them as blocked, not failed origin behavior or verified receipt.

## Focused technical corrections

1. `functions/_middleware.js`: deny internal source/data paths on all runtime hosts, including decoded traversal. Public assets, forms, Shop and APIs pass through. This alone cannot protect a static host where Functions do not execute.
2. `scripts/prepare_release_candidate.py`: create a public-only artifact outside the checkout, resolving public HTML/CSS/JavaScript and legacy fragment dependencies. Keep private runtime compiler inputs separately. Refuse destructive overwrite; exact-byte `--check` validates public and runtime files. No deploy action exists.
3. `scripts/terms_reader.py:production_terms_html`: preserve the existing effective Terms body for a prospective production artifact; normalize only its canonical/social/schema route metadata. Fail closed if the registry is activated or the source is invalid. The staging reader is unchanged.
4. Add complete local HTTP/rendered canonical auditing, boundary/export tests, current synthetic Shop backend fixtures and contact/analytics safeguards to the existing staging-only CI. Historical frozen-design tests are not silently rewritten to pretend current approved changes never happened.

## Verification and evidence boundaries

The internal review package is outside deployed assets: `/workspace/review/prelaunch-2026-11-26/`. It contains the all-route inventory/canonical tables, actual local Chromium screenshots/results, lab performance, issue register, integration/security findings, test logs, release/rollback plan and immutable candidate receipt after commit. Do not upload that directory or `runtime/` as static assets.

Commands:

```sh
python scripts/build_site.py
python scripts/build_site.py --check
python tests/seo_preservation.py
python tests/sitemap_discovery.py
python tests/prelaunch_security_content.py
python tests/release_candidate.py
python tests/prelaunch_shop_contract.py
node tests/recovery_source_boundary.mjs
node tests/prelaunch_tracking_contacts.cjs
python scripts/run_customer_browser_checks.py
python scripts/prepare_release_candidate.py --output /tmp/mrsewing-candidate-unique
python scripts/prepare_release_candidate.py --output /tmp/mrsewing-candidate-unique --check
```

Browser tooling needs the installed Playwright/Chromium and an existing loopback preview, for example `CHROMIUM_BINARY=/usr/bin/chromium REVIEW_BASE_URL=http://127.0.0.1:3087 BASE_URL=http://127.0.0.1:3087` on this workstation. CI supplies its own browser and port8020. No real enquiries, external messages, purchases or tracking conversions are required.

## Release gate and future procedure

No Main merge or production upload is part of this assignment. After separate authorization, first verify real staging and production hosting/output settings and record a known working frontend/runtime rollback pair. Publish only the frozen candidate `public/`; separately compile/deploy compatible Pages API runtime with the existing approved public intake contract. A raw repository-root static deployment is unsafe. Preserve production-only settings, current consent and environment-specific indexing; do not enable private D1/R2/staff features.

The existing Meta integration is consented PageView-only. It excludes all queried landing URLs (including UTM/fbclid) and transactional flows, and has no persisted first-party campaign attribution or verified lead measurement. Keep privacy protections; do not silently activate conversions or claim event receipt. Resolve the advertising measurement design through authorized privacy/account review or obtain explicit owner acceptance before campaigns.

Actual origin/provider/account verification is still required. Green source tests, a normal Git push or a Cloudflare receipt do not establish those facts. Record local, CI, provider-reported deployment and actual deployed-browser outcomes separately in the final receipt. Minor spacing, seeded-request layout shift and image transfer optimizations may be deferred if enquiries remain usable.
