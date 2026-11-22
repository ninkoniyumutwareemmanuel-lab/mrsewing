# R58: Restore staging homepage exactly from main
Date: 22 November 2026 | Owner-requested staging recovery

## Owner instruction
“Recover our homepage that we hade so ti can look the same as main then we will continue after !”

## Restoration
The eight files that directly determine the rendered homepage have been restored **byte-for-byte** from the current `main` commit `f07e3b3839b0faf133af77f3aca62779b3369be5`:
- `index.html`
- `assets/homepage.js`
- `_templates/homepage.html`
- `_templates/homepage-sections.html`
- `_templates/homepage-galleries.css`
- `_templates/homepage-galleries.js`
- `scripts/build_homepage.py`
- `scripts/homepage_galleries.py`

Existing homepage header, footer, common CSS, static imagery, metadata, resource pipeline, and other homepage components were already identical to main and have therefore not been modified. The generated `index.html` and `assets/homepage.js` are the original main blobs, not a re-created approximation.

This is a **homepage-only rollback of R56/R57**, not a reset of the entire staging branch. R54/R55 Terms PDF pop-up pages, the preserved currently effective HTML Terms, image-rights owner attestation and central media records, tests, all other staging pages and scripts remain on the staging branch. The unused R56/R57 homepage source helpers and historic tests are left in version control for traceability but are **not imported by the restored main homepage builder**.

The previous staging state is backed up in `backup/staging-before-main-homepage-recovery-2026-11-22` at `3bcf142ddb3ba1ef17b55566cb7d822dd142641b`. Production `main` is not updated. No declaration of PDF legal effectiveness, source image rights or customer data changes is made by this homepage restoration.

## Verification
The R58 read-only GitHub workflow compares all eight website homepage files byte-for-byte against pinned main and runs full-site `--check`, Terms, SEO and sitemap regression tests. Cloudflare deployment status is checked independently; device-specific rendering on the public staging domain may require owner visual review. Do not reinstate the rejected R56/R57 homepage-layout test suite as an R58 release gate because that suite explicitly demands new content the owner has now withdrawn.
