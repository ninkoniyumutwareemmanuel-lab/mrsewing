# R65 — Owner-approved existing request forms in pop-up presentation
Date: 22 November 2026. Branch: phase1/customer-journey-repairs only.

Owner expressly chose separate, current forms for Request a Quotation and Book a Consultation. Preserve all existing form fields, current review/validation, privacy and terms consent, the existing Web3Forms destination and backend request integration. No synthetic customer submission and no main branch change.

Implementation: shared customer-interactions script (already included on generated public pages) progressively intercepts direct quotation/consultation form links on the same origin, opening a native <dialog> with the existing form route in a same-origin iframe. A scoped stylesheet is injected inside the iframe to conceal the form page's own header, breadcrumb, progress strip and footer while retaining the full form, review and success states. Links inside the form to non-request pages open in another tab. Close restores focus to the opener; Escape from within the form closes the popup. Original URLs continue to work as standalone pages if JavaScript is disabled.

A separate, injected footer Terms & Conditions quick link is also removed to fulfill the owner's earlier footer instruction. Terms remain in Policies and consent forms.

Test the 390px mobile request and consultation popups, original form fields and consent, and all existing homepage regressions; do not submit actual requests in tests.
