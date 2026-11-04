# Homepage-only visual review

Owner direction: finish the homepage first, then rebuild and reconnect one other page at a time. Work remains on `phase1/customer-journey-repairs`; staging only.

## What is disconnected

The generated homepage has no destination links, including service, booking, contact, social, policy, gallery and quotation actions. All destination anchors render with no href and with aria-disabled. The single remaining href is the accessible Skip to content control. The quotation form's fields and send action are disabled; submission credentials, endpoint, success state and legacy order popup are removed from the generated output. The preview JavaScript contains no fetch or enquiry controller and prevents form submission.

Presentation controls remain usable: mobile menu, Services disclosure, manual order-option selector and customer-gallery arrows. With JavaScript off, the navigation remains visible and all option descriptions can be reviewed; destination actions and enquiry fields remain disconnected.

The Looking Ahead programs retain exact approved wording and Coming Soon status directly before Let’s Make It Personal. Original photographs and visual design are retained.

Other pages are preserved on disk and remain directly accessible at their existing URLs; they are disconnected from the homepage, not deleted or unpublished. No new page redesign or production-routing change was made. This implements the owner's offered “exclude or disconnect” option while retaining valuable sources for later page-by-page rebuilding.

## Reconnection architecture

`HOMEPAGE_VISUAL_REVIEW = True` in `scripts/build_homepage.py` produces this disconnected version using `scripts/homepage_preview.py` and `_templates/homepage-preview.js`. The original destination URLs, form configuration and connected controller remain in their source files for future authorized work. Do not reconnect everything simply by disabling the flag: rebuild/review each destination first, then scope reconnection to the approved page.

## Search appearance

Homepage title: **Mr Sewing Fashion | Tailoring & Alterations in Kigali**.

Description: **Mr Sewing Fashion in Kigali, Rwanda: bespoke suits, custom tailoring, clothing alterations and garment care. Explore our work, designs and service information.**

Canonical remains `https://mrsewingfashion.com/`. Existing keyword metadata, official logo/social preview image, local-business identity and hours are preserved. Disconnected navigation is omitted from generated SiteNavigationElement structured data. Existing WebSite/business structured data stays present.

The exact brand is Mr Sewing Fashion, also identified as Mr Sewing—not the accidental transcription “Mr Selling.” The homepage uses relevant Kigali tailoring, alteration, bespoke-suit and garment-care wording without repeated typo keywords or ranking guarantees. Staging remains noindex, nofollow. Live metadata and the live website were not changed. Google chooses the final displayed title and snippet; the supplied example is illustrative, not evidence of a search ranking or indexed staging page.

## Validation

- Complete site build consistency check and all 14 Python static suites passed.
- Eight-width browser test passed at 320, 360, 390, 430, 768, 1024, 1280 and 1440px.
- Verified no destination hrefs, no form action, no access-key field, no active submit button, no enquiry POSTs, and no JavaScript errors.
- Menus/selector, exact program visibility/adjacency, no-JavaScript output, brand metadata and simulated staging noindex passed.
- Automated WCAG A/AA scans found zero violations at 390 and 1440px.
- Policy/program preservation, shared-component isolation, site inventory and customer-journey static checks passed. Existing connected-homepage submission/navigation browser suites describe the prior connected mode and are not the acceptance checks for this intentionally disconnected preview.

Artifacts: `/workspace/artifacts/homepage-only/homepage-390.png`, `homepage-1440.png`, `accessibility.json`, `search-preview.html` and `search-preview.png`.

No other page was deleted. No main-branch, live deployment, hosting setting, custom domain, sitemap or robots-policy change was made. A staging push and Cloudflare publication must be reported separately where network access blocks verification.
