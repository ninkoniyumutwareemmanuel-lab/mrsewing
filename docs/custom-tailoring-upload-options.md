# Special Order attachments — options and recommendation

Research date: 4 November 2026. No upload service, purchase, bucket, endpoint or deployment setting has been approved or activated.

## Current verified state

The website repository is static HTML/CSS/JavaScript with Python builders. There is no existing upload handler, private file store, upload credential binding or Pages Function in the project. The runtime exposes no approved Cloudflare storage identity. Existing enquiry forms use Web3Forms JSON submission; the new Special Order text form reuses that same configuration. An existing text integration does not prove attachment support or entitlement.

The owner explicitly approved text-only Special Order enquiries and a disabled upload interface while a secure solution is reviewed. The displayed file control is disabled, has no submission name, is outside the text form, and cannot attach files. No file selection/upload simulation was performed. JPEG/PNG/WebP `accept` values are preparation only, not a supported-upload or server-validation claim. Actual file-type, size, count, scanning and failure-handling tests must happen after a backend and limits are approved.

No customer files have been uploaded, made public or stored in this work. No service was purchased. Current incremental infrastructure purchase cost: **$0**; existing account bills were not inspected.

## Options

| Option | Feasibility / cost | Security and operational considerations |
| --- | --- | --- |
| Existing text enquiry plus customer-controlled WhatsApp sharing | Available now; no new website upload backend or purchase. Existing messaging/data charges remain outside this project. | Customers arrange image sharing directly with the business using its existing link. Website does not accept files. Staff should link references to the relevant enquiry and follow approved handling rules. |
| Attachments through the existing Web3Forms provider | Candidate only. Current plan entitlement, supported attachment API, file limits, retention and price **not verified**. May require a plan change; no plan/price assumption is made. | Could minimise integration work and avoid another form processor, but requires documented private handling, delivery, access, retention and deletion guarantees. Never infer support by adding an HTML file field to the current JSON endpoint. Test actual receipt and all rejection/timeout paths before activation. |
| Cloudflare Pages Function/Worker with **private R2** storage | Technically compatible with the established Cloudflare staging platform, but not implemented/configured. Compute, storage, operations, notification and scanning costs must be budgeted. Official published rate examples below; actual account plan is unknown. | Strong control over private access and retention, but needs server validation, authentication/abuse protection, malware/image processing, staff-only access, deletion and error monitoring. Requires engineering and owner-approved data handling, not just a new input field. |
| Another managed private-upload vendor | Possible later; provider selection, subscription/quota/transfer costs and contract remain unverified. | Adds a data processor and access/retention obligations. Do not adopt one simply to make the interface look finished. |

## Verified Cloudflare published pricing reference

Official Cloudflare documentation website requests were proxy-blocked. Its official public documentation **source** was accessible on GitHub and retrieved successfully. Rates below are USD public documentation references, not a quote for this account, a purchase authorisation or a promise that this implementation will be free. Taxes, account-wide existing usage, billing activation, rounding and changed vendor terms may affect cost.

- R2 **Standard** storage: **$0.015 per GB-month**; Class A operations **$4.50 per million**; Class B operations **$0.36 per million**; Internet egress is listed as free. Standard free tier lists **10 GB-month storage, 1 million Class A and 10 million Class B operations per month**. Allowances are shared with other account usage, not reserved for this page; billable usage is rounded as documented.
- Workers/Pages Functions: Free lists **100,000 requests/day** with limited CPU. Workers Paid has a **$5/month account minimum**, including **10 million requests/month** and **30 million CPU milliseconds/month**, then **$0.30/additional million requests** and **$0.02/additional million CPU milliseconds**. Pages Functions are billed as Workers. Heavy scanning/image processing may need other services or paid compute; do not assume the free CPU budget is sufficient.
- Private storage access, email notifications, malware scanning and ongoing maintenance are separate design/cost considerations. A small storage volume may fit free allowances, but this does not establish a zero-cost secure service.

Sources retrieved 4 November 2026:

- https://github.com/cloudflare/cloudflare-docs/blob/production/src/content/docs/r2/pricing.mdx
- https://github.com/cloudflare/cloudflare-docs/blob/production/src/content/docs/workers/platform/pricing.mdx

Evidence copies: `/workspace/artifacts/custom-tailoring/cloudflare-r2-pricing.mdx` and `cloudflare-workers-pricing.mdx`.

For Web3Forms, the live attachment documentation was blocked by the outbound proxy. The official organisation/documentation repository could be inspected, but the retrieved repository navigation did not establish current attachment capability or pricing. Obtain current provider documentation/account entitlement before comparing a concrete subscription quote. No unverified dollar price is supplied.

## Recommendation

Keep the implemented **text enquiry + arranged WhatsApp reference sharing** now. Keep website file selection disabled until owner review and backend approval.

For eventual on-site attachments, prefer a small Cloudflare Worker/Pages Function and **private R2** if the owner wants direct control over staff access, deletion and retention. Before committing to that engineering, ask the existing form provider for its attachment capability, privacy/retention details and exact account price; a verified equivalent may be simpler. Neither candidate is approved or currently working as an upload integration.

Minimum acceptance criteria for any chosen solution:

1. Agree permitted image formats, maximum per-file/total size and file count with the owner. Initial candidates are JPEG/PNG/WebP; these are not activated upload limits. Validate extension, MIME **and decoded content** on the server; reject executable/SVG/HTML payloads, oversized files, excessive dimensions and malformed images. Client `accept` alone is insufficient.
2. Rate-limit and verify requests, constrain origins, prevent unlimited storage abuse, use unguessable server-generated object names and prevent path traversal. Treat user text as data.
3. Store objects privately; disable public bucket/r2.dev access. Keep credentials server-side. Do not place customer files or public download links in Git, static assets, browser logs or email notifications. Staff access must be authenticated, narrowly authorised and time-limited.
4. Define malware scanning/quarantine, safe image decoding, metadata/EXIF handling and what happens when a scan fails. Reference pictures may contain personal/location information.
5. Agree consent, processor arrangements, retention/deletion periods and enquiry-to-file association. Do not invent those policies in homepage or service copy.
6. Confirm all files and the text enquiry are durably accepted before showing success. Handle partial uploads, duplicates, cancellations, quota failures, timeouts, orphan cleanup and retry without false success or duplicate orders. No upload creates a confirmed production order.
7. Test real authorised non-customer receipt and staff access; test invalid files, limits, private-access denial, retries, deletion and mobile use. Require owner review before enabling the control.

No production or staging Cloudflare settings were changed to investigate these options.
