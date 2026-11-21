# R57 — Preserve the original homepage; make only requested additions
Date: 21 November 2026 | Staging only

## Owner clarification
The owner rejected the R56 homepage replacement because it deleted/reordered original content and changed how the existing homepage was built. The new instruction is: “take the existing homepage, add the changes that I asked you ... Do not remove anything or change anything on homepage the way it's built ... unless only unless what I asked.”

## Corrective implementation
Restore the exact earlier homepage template, header, footer, section builder and homepage source sections as they were at staging R55 commit 4d7c28261afe2a40aaba05b513b2d835071edd81, **then** apply only localized changes. All old information, service, customer/process, benefits, order-options, Our Work, programs, final CTA, Shop preview, payment details, footer and customer support remain in original order.

The changes are strictly:
1. Existing hero, same photo/background/layout: change heading to “Professional Tailor in Kigali, Rwanda”, supporting text to approved tailoring message, add three explicit customer actions while keeping the existing Request a Quote link and existing five service highlights.
2. Insert exactly two neutral portrait media spaces immediately after the hero. They use already owner-authorized reference images until separately approved silent videos/posters are genuinely eligible; no visible gender labels or captions.
3. Highlight the existing Tailoring & Clothing Services and VIP cards without removing, replacing, reordering or duplicating the five original service cards; first label changes.
4. Insert one standalone tailoring photo without long copy after the original Services section.
5. Keep the **existing men's and women's galleries**, with newly owner-approved R53 reference photos prepended in family groups using the verified 19 November 2026 upload timestamp. Original published Showroom/Shop status unchanged. Men's row moves right→left; women's moves left→right; explicit pause/resume, Escape pause and reduced-motion. The original Our Work gallery remains present as it was (third gallery). Do not invent missing dates or treat photo upload as garment production date.
6. Preserve existing quotation, customer support, WhatsApp consent, SEO, policy document, payment and navigation systems.

No wholesale redesign, deletion of sections, new framework, new supplier database, new payment or external integration.
Owner attested rights to the newer photos, with authorship and independent licence not inspected. Two R53 videos remain held and silent preparation remains private. The R55 PDF Terms are still a staging-review copy, while customer consent uses currently effective HTML Terms.

## Verification and deployment
Compare committed homepage source components to R55 historical SHA to verify original page structure restored. Run full builder/build --check, focused original-section preservation and media-gate tests, SEO, sitemap and Terms tests, browser widths 320/390/768/1440, reduced-motion and pause. Staging only; never touch production main.

**Staging noindex** remains preserved by the existing SEO build and `_headers` policy; it does not authorize main/production indexing changes.
