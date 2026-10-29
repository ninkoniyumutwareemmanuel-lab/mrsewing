# V2 shared header and footer

The homepage, Contact Us and About Us use this build-time architecture. Legacy pages
remain available with their current layouts; migrate them individually when their
V2 redesign is approved. No browser HTML fetching, framework or new dependency.

Single sources:

- `_templates/shared/header.html`: branding, navigation, Shop Coming Soon.
- `_templates/shared/footer.html`: five columns, hours, policies, contacts, social
  SVG icon placeholders and official destinations. YouTube uses the updated URL.
- `_templates/shared/site.css`: the approved stylesheet, moved intact to preserve
  homepage cascade/order. This includes common design tokens, typography, header,
  footer, responsiveness and homepage layouts. Contact's build selects the common
  rules instead of shipping unused homepage layout rules.
- `_templates/shared/navigation.js`: accessible disclosure-menu behavior.
- `scripts/shared_components.py`: page-aware rendering and shared style selection.

The homepage and Contact generators call these helpers, then replace existing
icon placeholders with the same local licensed SVG paths. Homepage-only gallery
and consent code is maintained in `_templates/homepage-interactions.js`; the build
appends the shared menu controller, producing `assets/homepage.js` unchanged.
Contact's smaller generated controller contains that same menu plus its legacy
order-bookmark compatibility handler. Never edit either generated JS file alone.

## Build and verify every migrated page

```sh
python3 scripts/build_site.py
python3 scripts/build_site.py --check
python3 tests/shared_components.py
```

This runs homepage, Contact, About, then clean-URL generation in dependency order. A
shared source change propagates to **all three V2 pages** when this command is run and
the generated outputs are committed. `--check` rejects stale outputs. Static
GitHub Pages does not run Python for visitors; run the build before pushing.
Legacy page layouts are not automatically migrated.

## Future page integration

1. Create/maintain the page's source template, metadata and body separately.
2. Import `shared_components.header('/about/')`, `footer()`, `component_css()`
   and `menu_script()` in that page's build script. Use root-qualified asset and
   navigation URLs. Header links to homepage sections are automatically qualified
   off the homepage; the matching page link gets `aria-current="page"`.
3. Keep common selectors under the existing header/footer/common CSS prefixes;
   put page-specific styles in that page's own template stylesheet. The common
   selector extraction is centralized in `shared_components.shared_css`.
4. Apply the existing optimized logo and local SVG `delivery()` helper to the
   rendered components, as Contact does. Do not add a second component copy or
   runtime component fetches.
5. Register the new builder before `build_clean_urls.py` in `build_site.py`.
6. Add generated-output, navigation, responsive and component-parity checks before
   migrating the page. Preserve its canonical and legacy URL compatibility.

The footer now retains the supplied main-workshop map destination and updated
social URLs. Invisible accessible clarifications scope its hours to the main
workshop and identify MIC consultations as appointment-only without changing the
approved visual layout. No policy, hours, SEO content or service terms changed.
