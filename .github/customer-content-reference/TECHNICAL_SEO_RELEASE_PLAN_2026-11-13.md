# R47 production release proposal and Google Search Console follow-up

**Proposal only — production remains unchanged.** Owner technicalSEO instruction dated13November2026; safe changes implemented and tested on phase1/customer-journey-repairs. No indexing request or live setting change has been made.

## Ready for owner review

1. Square faviconPNG plus conventional rootICO derived from the unchanged approved logo; correct ordinary favicon references/MIME declarations. Keep the original PNG and Apple touch references intact.
2. Explicit noindex404 document, preventing Cloudflare's default root200 fallback on unsupported paths; no wildcard/home redirects. Retain actual404 responses for removed content without equivalent replacements.
3. Standard-library build validation, source image inventory entry and focused SEO/routing/preservation regressions.

**Release only this technical delta when authorized.** The staging branch also contains earlier, separately reviewed design/journey work. Approval of an SEO repair must not automatically merge all that work. Prepare an isolated main-based release, reapply these source/asset changes and regenerate HTML from production's approved content; do not overwrite production pages with generated staging content. Keep the production sitemap at its approved set unless the owner separately approves the Kaunda publication delta. The audit's64-entry staging sitemap is coherent and requires no arbitrary truncation or directory-indexing change.

No new301 mapping is ready: original legacy product/design identities are unverified. `/services/` remains deliberately noindex and excluded. Do not enable forms/private areas/draft merchandise for indexing, change security broadly, activate payments/databases, or rewrite approved service copy.

## Live release gate after authorization

- Confirm the actual production hosting/publishing path and immutable main baseline before applying the reviewed delta.
- Build/test the isolated production candidate and inspect its exact diff; verify ordinary service content, quotations and approved metadata remain intact.
- Deploy by the actual protected production process, then verify its served fingerprint rather than treating a Git commit as publication.
- Check HTTPSapex andwww plus HTTP redirects; all eight priorities200; intended indexfollow and self-canonicals; no production X-Robots-Tagnoindex leakage; actual faviconPNG/ICO MIME and retrieval; unknown paths404; no redirect loops/chains or missing required resources.
- Verify live robots/sitemap XML, exact intended URLset and `/services/` exclusion. Recheck staged root/preview noindex separately. Preserve security protections.

## Search Console monitoring — owner/manual actions

After the approved technical release has actually been verified:

- **Release day:** open Sitemaps and verify the canonical `https://mrsewingfashion.com/sitemap.xml` last-read date and success. Resubmit that existing sitemap if needed using the owner's authorized Search Console access. Confirm the discovered URLset reflects the actually approved production release, rather than assuming every staging URL is live.
- **Release day:** inspect the eight priority canonical URLs without query parameters. Compare live test, last crawl, robots/canonical and renderedHTML. If eligible and appropriate, the owner may manually request indexing of a small priority set. This task does not automatically request indexing or submit through unauthorized tools.
- **After3–7days:** review sitemap processing, crawl response codes and exact affectedURLs. Distinguish newly crawled pages from historical reports; watch specific required resources rather than trying to eliminate every legitimate404. A redirect URL or proper canonical alternate need not become independently indexed.
- **Weekly for2–4weeks, and longer if needed:** track indexed status for important services and approved collections, last-crawl dates and the exact16crawled/152discovered examples. Record before/after URL-level evidence; aggregate totals alone do not prove improvement or failure. Google may take longer and may choose not to index every eligible URL.
- For persistent priority-page exclusions, compare Google-selected vs declared canonical, rendered unique content, internal discovery and actual response data. Review page-specific quality/duplication only after seeing the exact affectedURLs. Do not keyword-stuff or mass-rewrite valuable content based on counts.
- Export the complete legacy upload paths and unknown detail URLs with referringpages/lastcrawl evidence. Add an exact301 only when an equivalent approved replacement is established; otherwise retain404/410.

No ranking positions, indexing date or universal inclusion are guaranteed. Owner review and separate production authorization remain required.
