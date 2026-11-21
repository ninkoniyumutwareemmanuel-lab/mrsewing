# Homepage hero Request a Quote — WhatsApp handoff
Date: 21 November 2026
Owner instruction: connect the homepage hero's existing Request a Quote button to WhatsApp.

Updated the original homepage section template and its generated `index.html` output only.
Old destination: `/booking/`.
New destination: `/whatsapp/?text=Hello%20Mr%20Sewing%20Fashion%2C%20I%20would%20like%20to%20request%20a%20quotation.%20Please%20help%20me%20with%20the%20next%20steps.`, carrying an editable quotation enquiry.

The existing `data-whatsapp-modal` handler opens the established Terms confirmation dialog and only then opens the already verified WhatsApp number (+250 787 411 501). No message is automatically sent, no request is automatically logged, no booking is confirmed. Without JavaScript, the `/whatsapp/` page remains the fall-back consent journey.

Only the hero button changes. Existing booking links/forms elsewhere and all customer terms/consent controls remain untouched.
