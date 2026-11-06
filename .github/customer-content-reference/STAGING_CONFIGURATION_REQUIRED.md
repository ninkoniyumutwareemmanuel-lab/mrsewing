# Exact staging configuration and deployment investigation — 5 November 2026

## R7 verified deployment update (supersedes the earlier unknown-status diagnosis)

Public GitHub commit checks independently show successful Cloudflare deployment of433107ea259fcede6a2a7a057f752dd3151b3a32: deployment bfa64c37-cd6b-401b-90b5-eff27f766d77, preview https://bfa64c37.mrsewing-staging.pages.dev. They show **Build failed** for newer b83720b176a49190fb3583d24bf85fcee87a9f3c: deployment273632f8-eb91-4611-8d30-bfe98834dd16, check127431321571. Thus a successful GitHub push did not publish that repair; the older deployed code genuinely contained the Collections CTA. The precise failed-build error is account-protected and unavailable without an authorised Cloudflare account connection. Do not infer a particular failure cause without its log. The new R7 application uses generated plain ES-module allowlists instead of JSON import attributes for simpler Pages bundling; local Wrangler compilation passes, but this alone does not establish the old failure cause.

Read-only source: https://github.com/ninkoniyumutwareemmanuel-lab/mrsewing/commit/b83720b176a49190fb3583d24bf85fcee87a9f3c/checks . Detailed staging log: https://dash.cloudflare.com/?to=/ce4c727a75477b72168a3d2c4946c4b6/pages/view/mrsewing-staging/273632f8-eb91-4611-8d30-bfe98834dd16 . Do not change the live project. Direct staging origin access remains proxy-blocked. GitHub check success is deployment evidence, not a rendered-site or email-delivery test.

New release fingerprint: complete-repair-2026-11-05-r7. Use its exact commit and deployment check, not the earlierR6 fingerprint.

## Earlier investigation history (retained; unknown deployment status below is superseded)

## Confirmed evidence

GitHub remote development ref433107ea259fcede6a2a7a057f752dd3151b3a32 and unchanged remote mainba27bab0425a9df1948fe8f45dd3b941cb322f4c were read at task start. Full294-file change inventory is in the urgent review artefacts. The code contained real omissions independent of deployment (measurement CTA/lightbox, same-page FAQ modal, dedicated service forms, consultation header and portfolio-related section). These have been corrected locally.

An HTTPS request to https://mrsewing-staging.pages.dev/ failed at the environment's outbound proxy: CONNECT403, server envoy, before the Cloudflare origin was contacted. This is **not evidence of a Cloudflare build failure or an origin HTTP403**. No Cloudflare account/token/runtime bindings are connected. The configured project repository/production branch, deployed commit, deployment ID/build errors and cache state therefore remain unverified. Owner subsequently confirmed that433107e deployed successfully and the About Collections button was still present. That old button is also present in the inspected433107e source. Wrong branch, caching and failed builds are not established causes. The new revision still requires independent deployment verification.

A supported attempt to save network access for mrsewing-staging.pages.dev, api.cloudflare.com, api.github.com and developers.cloudflare.com returned `CONFLICT / draft_not_editable`. Saving/applying was NOT confirmed. Existing presets were not changed and no proxy bypass was attempted. Proposed network JSON is provided with the transferable review artefacts. In environment settings, allow those four hosts; if this chat's draft remains uneditable, open a new setup chat from environment settings. This concerns the Codex execution environment, **not publishing the website**. A read-only Cloudflare Pages account connection/token and the account ID are also needed to inspect deployments; do not paste credentials into conversation or Git.

## Owner/account deployment checks (staging project only)

1. Cloudflare dashboard → Workers & Pages → select **mrsewing-staging**, not the live-domain project.
2. Settings → Builds & deployments: verify the connected repository is ninkoniyumutwareemmanuel-lab/mrsewing and inspect its configured production branch. For this established root staging URL, the intended branch is phase1/customer-journey-repairs. Record the actual setting before changing anything. Never change main or the live project's settings/custom domains.
3. Deployments: locate the delivery SHA from the report, inspect its status, deployment ID, branch and build log. If absent, check automatic builds/branch filters and GitHub integration permissions. If it failed, share the specific error. If a different branch serves the root URL, correct **only this staging project** after confirming isolation. A successful Git push is not a deployment.
4. Verify build command `python3 scripts/build_site.py`, repository root, and output directory `.` for the existing generated-static architecture. Cloudflare should also compile root `functions/`; local Wrangler4.158.0 bundling has passed. No framework or paid service was installed into the website.
5. The new `/build-info.json` fingerprint contains release urgent-corrections-2026-11-05-r6. When the build command runs in Cloudflare CI, CF_PAGES_COMMIT_SHA and CF_PAGES_BRANCH populate the exact served revision. A null commit in this file means the static fallback was served without Cloudflare CI stamping; it does not prove which commit was deployed. Check the dashboard in that case.
6. Open the deployment's unique Pages URL and root staging URL, with a cache-busting query if needed; inspect build-info and the actual corrected pages. Only after those match can staging be marked verified. Do not purge/change live caches or domains.

## Private backend activation prerequisites (not currently configured)

The application code is implemented; it remains disabled in `_data/customer-request-backend.json` and fails closed without all server bindings. Local emulation is not a Cloudflare deployment.

Configure these on **mrsewing-staging only**, in the environment serving the authorised branch. Cloudflare may call that environment “Production” when the development branch serves this staging project's root URL; that name does not authorise any live-project change. If it is a preview branch, use its corresponding preview bindings.

| Binding/variable | Required configuration |
|---|---|
| REQUESTS_DB | Dedicated staging D1 database; apply additive migrations/0001_customer_requests.sql to that database only. No destructive migration |
| PRIVATE_REQUEST_FILES | Dedicated private R2 bucket binding. Disable public r2.dev access; no public/custom bucket domain. No static asset uploads |
| REQUESTS_ENABLED | String true only after prerequisites and tests are complete |
| TURNSTILE_SITE_KEY | Approved widget public site key restricted to intended staging host(s) |
| TURNSTILE_SECRET | Corresponding secret stored in Cloudflare encrypted environment settings; never in frontend/Git |
| REQUEST_EMAIL_ACCESS_KEY | Verified Web3Forms form integration for the approved business recipient. Existing browser form key does not prove recipient settings; verify in the provider account |
| REQUEST_RATE_SECRET | Independently generated random server-only secret, at least32characters, for hashed hourly rate-limit keys |
| STAFF_ACCESS_TEAM | Exact authorised team hostname, e.g. your-team.cloudflareaccess.com |
| STAFF_ACCESS_AUD | Exact Cloudflare Access application audience for this staff application |
| STAFF_ALLOWED_EMAILS | Explicit comma-separated approved staff email allowlist; application verifies signed JWT audience/issuer/expiry and this allowlist |

Create a Cloudflare Access application protecting /staff/customer-requests/* and /api/staff/* on staging, with explicit staff identity policy. Do not disable the in-application JWT checks. `/api/customer-requests` remains public intake with same-origin validation, Turnstile and rate limits. R9 now permits the exact approved production apex mrsewingfashion.com as well as staging;unknown hosts remain denied. All private prerequisites and the frontend feature gate still apply. Do not enable `LOCAL_TESTING` in Cloudflare; it exists only for the local test fixture.

Owner must confirm processor/privacy/retention/deletion arrangements, staff access, plan limits and costs before using real customer uploads. No cost or legal-compliance claim is made. PNG/JPEG/WebP validation checks type/signature/structure/dimensions, byte/count limits and still-image format; it is not a malware-scanning certification or a claim that all file content is harmless. Private responses use no-store/nosniff/sandbox and require staff auth.

After configuration, change the frontend feature flag enabled to true on the development branch and run the real staging men/women/Special/Standard/Express/authorised and unauthorised staff tests. Verify request and attachment persistence and real notifications. Until then file inputs stay disabled and only the existing text enquiry integration operates. Its acknowledgement is not proof of internal storage or email receipt. The staff shell contains no customer data; it fetches from authenticated server endpoints only.

## Email verification

Existing forms submit to https://api.web3forms.com/submit. The official contact address retained from the approved website is mrsewingfashiondesigner@gmail.com, but an access key does not reveal its actual configured recipient. In the provider account, inspect the form corresponding to the existing publishable integration key, confirm the authorised mailbox, domain restrictions and verified state. Do not change live settings for these tests. Use an owner-approved safe test recipient/environment, confirm actual inbox receipt and inspect provider logs if delivery fails. Current local tests mock responses and never send a real message. No account credentials or approved test mailbox access are exposed here.

## Pricing Sources

Required: Custom_Tailoring_Decision_Register_v5_2026-11-01.md, latest superseding approved price schedule/addenda and Mr_Sewing_Complete_Approved_Commercial_Policy_and_Open_Decisions_2026-11-01.md (or the original Mr_Sewing_Company_Sources.zip containing them). Need confirmation of current RWF complete two/three-piece packages by gender/tier, tuxedo distinctions/inclusions and publication clearance. Fabric-only rates require their own approved schedule. Earlier owner-reported amounts are preserved in the internal source matrix but explicitly were not new price/publication approval. No numbers were invented or silently reused as fabric-only prices. Current Source search found no originals. R8 later explicitly approved the exact ordinary-suit and men’s tuxedo amounts for staging;the old publication hold above is superseded for those supplied values.
