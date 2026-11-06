# R5 private requests and attachment readiness — 5 November 2026

Status: **BLOCKED — not operational.** This is an implementation dependency record, not a description of an existing backend.

Inspected repository: static Python-generated HTML/CSS/JavaScript, Web3Forms text submissions and official WhatsApp links. No Pages Functions/Workers, server, database schema/connection, private object-storage binding, staff login/roles, authenticated request-list API or attachment delivery integration was found. Current managed environment reports no credentials, runtime bindings or outbound cloud identities. Cloudflare account/project configuration cannot be inspected with the available access. Its absence from this workspace does not prove the owner's account has no resources.

Existing text forms remain available. A positive Web3Forms response means provider acceptance only; it does not prove email receipt, create a staff-visible database record, or attach photographs. Browser-tab drafts are temporary customer convenience, not business records. The upload input stays disabled and unnamed; no file bytes are submitted. No browser-only staff dashboard has been introduced.

## Required before end-to-end activation

1. An approved **staging-only** server endpoint and durable requests database; create request reference/time atomically, preserve structured selections/contact/message/consent, prevent accidental duplicate saves and return success only after durable persistence.
2. Private attachment storage with no public bucket URL or website asset path; upload limits, byte/signature and decoded-image validation, type/size/count limits, safe image processing, random object keys, malicious-file assessment, cleanup on partial failure and ownership checks. Browser `accept` is not server validation.
3. Real staff authentication and explicit authorisation for Customer Requests and each attachment. Require verified server-side identity/roles; prevent listing/reading another account's objects, public caching and unauthorised downloads. Never trust a client-only flag or a plaintext identity header.
4. Spam/rate/abuse controls and CSRF/origin protections appropriate to the selected architecture. No secrets in browser code or Git. Safe generic errors and operational monitoring without logging private payloads.
5. Owner-reviewed privacy/retention/deletion/access arrangements for contacts, measurements and photographs; actual processor arrangements and any applicable Rwanda legal checks. Do not assume an arbitrary company retention period.
6. An approved safe test recipient/delivery environment. Existing Web3Forms public integration key does not reveal its recipient settings. Owner/account access is required to verify those settings and actual receipt.
7. End-to-end tests: JPEG/PNG/WebP phone/computer selections, supported camera capture, previews/remove/replace, invalid/spoofed/oversized/too-many files, interrupted upload, duplicate submit, durable save, authorised staff retrieval and blocked unauthorised retrieval. Text-only requests must also appear in the real staff record.

## Architecture recommendation for review

Cloudflare Pages Functions plus a staging-only database and private object storage could fit the existing host, with server-verified staff identity. This is a proposed architecture, **not an installed/configured solution**. Obtain actual account capabilities/usage pricing and select authentication/spam protection before implementing and activating it. No service was purchased, no bucket/database/auth policy created, and no production/cloud-domain settings changed. Current prices/costs were not verified and are not quoted.

Suggested request statuses from the owner attachment remain proposals; no final staff workflow or business acceptance state was invented. A browser success screen must never substitute for staff persistence or production-order acceptance.
