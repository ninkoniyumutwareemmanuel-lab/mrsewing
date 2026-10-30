# Contact Us V2.1 validation

Implementation baseline: `5a872d1e2d8ab596d0415a29df5ec740322110f2`.
Working branch: `phase1/customer-journey-repairs`.

## Scope and architecture

Removed both Contact hero links and their unused layout styles, preserving the
headline/copy and compacting the bottom paragraph margin. Main content retains
MIC appointment booking and final consultation booking, direct WhatsApp/phone/
email, owner-provided workshop directions and the existing booking workflow.

Homepage and Contact now render the same shared header/footer, including the
original footer SVG social icons, sizes, spacing, hover/focus styling and layout.
Contact's separate social row and footer substitutions were removed. Social
URLs are the official destinations, including updated YouTube. The shared
footer uses the owner's workshop map URL; invisible labels clarify main-workshop
hours and MIC appointment-only consultations without changing the approved look.

See [shared-components.md](shared-components.md) for exact sources, registration
of future pages and build commands. No client-side component fetching or new
runtime dependency was added. Legacy layouts were not migrated.

## Verified results

- `python3 scripts/build_site.py --check`: both V2 outputs and 31 clean URLs match.
- `python3 tests/shared_components.py`: identical rendered footer on both pages;
  in-memory header/footer/CSS edits propagate to both generators; two main booking
  links and no Contact hero actions.
- All nine existing browser suites passed: homepage-journey, homepage, header,
  page-seo, homepage-optimization, phase1, phase2, image-delivery, agentic-discovery.
- Contact V2 browser suite passed: seven viewports, menu Escape/focus/outside/link
  closure, two booking entry points and required controls, canonical, JSON-LD,
  images, clean/legacy URLs and local destinations. No browser page errors.
- Existing booking tests use intercepted responses, exercise success/error/
  duplicate handling and weekend dates; no real messages or forms were sent.
- JSON-LD: 25 blocks parse; 462 typed nodes pass the supplied official Schema.org
  vocabulary/property-domain checks. Confirmed hours/calendar tests pass.
- Clean URL, metadata synchronization, JavaScript syntax and git whitespace checks
  pass. No changes to SEO data, business schema data, sitemap or robots.
- Homepage main markup, complete inline styles and generated JavaScript remain
  byte-for-byte identical. Before/after full-page Chromium captures at 320, 360,
  390, 430, 768, 1024 and 1440px are pixel-identical. Contact has no horizontal
  overflow at those widths; footer markup and computed social styles equal home.
- Generated gzip sizes: homepage 15,157 -> 15,128 bytes; Contact clean page
  9,260 -> 9,069 bytes (local gzip comparison, not measured transfer savings).

Local Lighthouse synthetic results (not field Core Web Vitals):

| Page / profile | Performance | Accessibility | Best practices | SEO | LCP | CLS |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Contact mobile | 100 | 100 | 100 | 100 | 1.1 s | 0 |
| Contact desktop | 100 | 100 | 100 | 100 | 0.3 s | 0 |
| Homepage mobile | 100 | 100 | 100 | 100 | 1.4 s | 0 |
| Homepage desktop | 100 | 100 | 100 | 100 | 0.3 s | 0 |

Screenshots and raw reports are in the review workspace:
`/workspace/phase1-review/contact-v21/`. Homepage captures have before/after
variants for all seven widths. Contact full-page and footer captures include
390px and 1440px. Automated equality is technical evidence; owner visual approval
remains required.

## Limits and safety

Cloudflare staging HTTP requests fail at the environment proxy (CONNECT 403),
so the deployed revision and staging indexing protection cannot be verified here.
External social/Maps links are constructed/checked locally; live external-service
behavior is not established. MIC directions remain unverified and intentionally
have no directions link. Mock form tests do not prove real message delivery.

No production merge/publication, DNS/hosting changes, policy changes, legacy-page
redesigns or About Us V2 work were performed. Remote main before work:
`8419a616ee3450fc46f6bd3f1d477a034d0de07c`.

## Exact changed files

- `_templates/contact.css`
- `_templates/contact.html`
- `_templates/homepage-interactions.js` (extracted unchanged homepage-only JS)
- `_templates/homepage-sections.html` (header moved out; body content unchanged)
- `_templates/shared/header.html`
- `_templates/shared/footer.html` (moved from `_templates/homepage-footer.html`)
- `_templates/shared/site.css` (moved unchanged from `_templates/homepage.css`)
- `_templates/shared/navigation.js`
- `assets/contact-navigation.js` (generated)
- `contact.html` (generated)
- `contact/index.html` (generated)
- `index.html` (generated; only intended footer integration changes)
- `scripts/build_contact.py`
- `scripts/build_homepage.py`
- `scripts/build_site.py`
- `scripts/shared_components.py`
- `tests/README.md`
- `tests/contact-v2.spec.cjs`
- `tests/shared_components.py`
- `docs/shared-components.md`
- `docs/contact-v21-validation.md`
