# Meta Pixel activation — 21 November 2026

Owner explicitly instructed: "activate it now !" after staged integration and installation on main.

## Active scope

Pixel: 29683883327873735. Main branch. Only browser PageView is enabled on eligible public pages for visitors who click Allow tracking or have previously saved that choice. Marketing tracking is not enabled without opt-in. The user can decline and can revoke locally through Tracking preferences. No extra Contact, Lead, Purchase, Advanced Matching or CAPI events are enabled.

The linked legal Privacy Policy has been updated in the canonical source and both generated root and clean-url pages to disclose Meta, categories of data, optional consent, withdrawal and possible external processing. The consent banner text was updated to match. This change does not claim completion of an independent legal review.

No unrelated customer journeys, service policy rules, Shop, video permissions or website redesign are included in this release.

## Checks/limits

- Main configuration: productionEnabled true and status owner-approved-production.
- First-party script requires both flags, matching official host, and user opt-in before fetching Meta's fbevents.js or transmitting PageView.
- Pixel does not fire on sensitive forms, policy routes or pages with query parameters (including the staging preview query).
- No noscript image that bypasses consent.
- Live real-event delivery must be confirmed via Meta Events Manager Test Events with a clean homepage URL and explicit consent, and browser-network inspection; repository tests alone cannot prove receipt.
- Verify business compliance and lawful processing/transfer requirements independently with the Rwanda DPO; do not infer legal authorisation from technical release.

## Reversal

For emergency disablement only: change _data/meta-pixel.json productionEnabled to false and status to a non-approved value, regenerate assets/customer-interactions.js from the source builder and deploy. Do not deactivate by silently altering consent preference.
