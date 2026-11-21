# Compact cookie banner — approved visual revision, 21 November 2026

Owner inspected live opt-in consent and rejected the oversized marketing-tracker dialog. Owner then approved the compact black/gold cookie-bar preview and expressly authorised implementation on the live website.

Updated ONLY the cookie consent component and the related Privacy Policy explanation, preserving the existing Meta Pixel ID, owner-authorised production flag, lawful opt-in gate and PageView-only scope.

## Visual result

Desktop: compact horizontal banner centred at bottom, black background, subtle gold border, cookie icon, "Cookies & Privacy", concise optional-cookie/advertising description, inline Privacy Policy link, and two equal-height actions: **Reject** and **Allow**.

Mobile: small responsive bar with clear legible text, actions full-width in a row, above browser safe-area where possible. Original site content remains scrollable. A footer "Cookie preferences" control allows reopening.

## Tracking safety

- "Reject" stores declined and does not initialise Meta Pixel.
- "Allow" stores accepted and initialises the existing PageView Pixel only on eligible live URLs.
- Existing saved choices are respected (the banner is not forced back on every visit).
- Separate, persisted Terms-consent flow remains untouched.
- No new Contact/Lead/Purchase events; no customer form contents collected as event fields.
- Privacy Policy explains optional Meta advertising cookies, the purpose, processing and withdrawal; no claim that all technical or essential site storage is exclusively for advertising.
- Meta delivery cannot be proven from a successful GitHub build alone: verify Events Manager Test Events separately.

Source: owner screenshot and approved visual mockup in this conversation.
