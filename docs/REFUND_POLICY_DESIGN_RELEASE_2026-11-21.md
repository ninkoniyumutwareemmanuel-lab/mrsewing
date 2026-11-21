# Refund & Cancellation Policy page redesign — 21 November 2026

Owner approved the proposed black-and-gold responsive redesign and explicitly instructed immediate live publication.

What changed:
- A short hero with "Request a Review" and "Contact Support" actions.
- Desktop sticky section navigation and mobile "Jump to a section" menu.
- Readable numbered cards for the five approved sections, preserving all original refund/cancellation/workmanship wording and historic anchors.
- A three-step submit/review/response overview. This is guidance, not refund approval or a new service deadline.
- Improved form presentation and revised first-step button label: "Review Refund Request". No form field, consent, endpoint, validation, review or submit logic is changed.
- Anchor links use /refund-policy/#... to work correctly with the existing <base href="/">.
- The existing company header and footer and other policies remain unchanged.

Source of truth: _data/customer-release.json ("S-OWNER-2026-11-05 §§19–20"). Layout is maintained by scripts/refund_page.py and _data/refund-layout.json, applied by scripts/customer_site.py only on /refund-policy/. The two static outputs refund-policy.html and refund-policy/index.html are generated together.

No automatic refunds, new deductions, promised payment dates, or changes to customer legal rights were introduced. Live browser/form checks remain necessary.
