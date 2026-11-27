# Reliable staging workflow

25 November 2026. Authorized implementation branch: `phase1/customer-journey-repairs`. Owner's permanent review URL: **https://mrsewing-staging.pages.dev/**. Repository: `ninkoniyumutwareemmanuel-lab/mrsewing`. Known Pages project: `mrsewing-staging`.

## Evidence and remaining infrastructure boundary

Read the current dated reconciliation register before relying on any old deployment report. GitHub checks establish that both Main and development commits have produced deployment-specific previews in this same project. That alone does **not** establish the project production branch or the commit served at the permanent address. The permanent `project.pages.dev` address serves the project's production deployment; other branches commonly receive previews/branch aliases.

At recovery start, GitHub reported a successful staging preview for `0acf34dc` (`20c36335-0705-4d1d-b863-34fd5f2dea22`) while its R59 verification workflow failed. Main `33620fe4` also has a successful preview in the staging project. These are separate facts from actual served-content verification. The current environment's enforced HTTP policy denies `mrsewing-staging.pages.dev`, its preview subdomains, `mrsewingfashion.com`, `www.mrsewingfashion.com`, `api.cloudflare.com` and `api.github.com`; no Cloudflare account credential is configured. No production-branch setting has been independently verified or changed.

## Settings the project owner must inspect

In Cloudflare Workers & Pages → **mrsewing-staging** → Settings → Builds & deployments (the interface may call it Build or Branch control):

1. Confirm the connected repository is `ninkoniyumutwareemmanuel-lab/mrsewing`.
2. For this **staging project**, the intended production branch is `phase1/customer-journey-repairs`, because its production deployment owns the permanent staging URL. This does not mean changing GitHub Main. Inspect existing custom domains and integrations first.
3. Confirm branch build controls allow that branch and automatic Git deployments.
4. Confirm the build command runs the synchronized generators and checks, and the output directory is the actual generated website root. Do not assume a framework `dist/` directory exists. Current architecture generates HTML at repository root.
5. Inspect the latest deployment's branch, exact commit, output and build log. Verify those against GitHub, not just a green badge.
6. Ensure staging-only noindex responses remain active, then inspect Home, Fabric Guide, Terms and quotation journey at the permanent address. Compare `build-info.json`/commit evidence and the actual expected content.

**Production dependency warning:** `_data/public-api.json` and `functions/_lib/public-api-config.js` record that the live static site's public enquiry pipeline uses `https://main.mrsewing-staging.pages.dev`. Preserve that existing Main branch alias/runtime, production-origin allowlist and API validators. Do not disable Main preview builds, delete the alias, change global API settings or repoint custom domains as part of a staging repair. If a proposed setting can affect that live dependency, inspect it with authorized account access and get the necessary scoped authorization. No such configuration change was made here.

To perform these settings checks directly, this task needs read access to the Cloudflare Pages project and domain grants in the running Cloud environment. Staging-scoped edit permission is needed only for a verified required setting correction. Do not paste tokens into source, chat commands or Git. A public GitHub repository connection is not Cloudflare account access.

## Developer sequence

1. Read `AGENTS.md`, the latest reference pointer, source map and master register. Record remote Main and development SHA, branch, dirty files and owner authority.
2. Preserve dirty/local-only work and a recoverable baseline. Fetch all relevant history as read-only evidence; do not indiscriminately merge branches.
3. Edit authoritative source/data/templates. Keep historical documents and unrelated staged work. Update the dated decision/reference records when approval changes.
4. Prepare exact silent media and verified PDF-derived assets through their scripts; never invent permission, document version or effective date. Pending verification is an explicit state, not a reason to bypass checks.
5. Build, run `--check`, appropriate source/SEO/sitemap/media/document/backend tests and browser mocks. Verify all generated outputs are committed and there are no unexpected template placeholders.
6. Commit and push **only** `HEAD:phase1/customer-journey-repairs`, without force. If the branch advanced meanwhile, inspect and reconcile the new changes first.
7. CI checks the exact event commit with read-only repository permission. It never commits generated outputs or silently imports an arbitrary new PDF. A failure blocks a claim of verified release.
8. Verify the Cloudflare deployment for that SHA, then open the **permanent** staging site. Inspect its content, mobile layouts, assets, headers and customer journeys with safe mocks. A preview deployment is not a replacement for this final verification.
9. Record the final commit, deployment ID, tested URLs/screenshots, actual results and unavailable checks. Leave Main protected and stop for owner review.

## Production publication

A separate explicit owner instruction is required. Prepare a reviewed reconciliation against then-current Main, preserve production-only configuration/SEO/consent/customer agreements, exclude unfinished policies/products and verify actual live deployment separately. Do not infer release authority from an earlier unrelated task.
