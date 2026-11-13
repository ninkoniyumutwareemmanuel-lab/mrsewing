# R48 fabric reference facts and research record

Date:13November2026. Scope:Fabric Guide comparison cards only, on `phase1/customer-journey-repairs` for staging. The latest owner instruction and current repository reference were read before editing. No production or commercial-policy change is authorized.

## Verified company reference information

The owner's “COMPLETE CUSTOM TAILORING CUSTOMER JOURNEY” instruction dated13November2026 explicitly preserves these labels and associations:

| Collection | Reference label | Tier / Quality | Approved photograph key |
| --- | --- | --- | --- |
| Men | Super | 1 / 1 | fabric-super |
| Men | Wool | 2 / 2 | fabric-wool |
| Men | Polyester | 3 / 3 | fabric-polyester |
| Men | Cotton / Dubai | 4 / 4 | fabric-cotton |
| Women | Americano | 1 / 1 | fabric-americano |
| Women | Star | 2 / 2 | fabric-star |
| Women | Polyester | 3 / 3 | fabric-polyester |
| Women | Cotton | 4 / 4 | fabric-cotton |

Inspected implementation sources: `_data/fabric-reference-catalogue.json`, `_data/customer-guide-images.json`, `scripts/customer_guides.py`, the current2026-11-13-02 customer master/matrix/register/page map, and `SHARED_FABRIC_JOURNEY_BRIEF_2026-11-13.md`. Existing photographs remain reference illustrations, not evidence of a stocked fabric lot or certified fibre composition. No image, ID, name, category or tier association was changed. Several fabric IDs can still share a tier.

Published short descriptions say only that each entry is a reference for its approved suit collection and tier. Expanded details identify the reference collection and state that exact fibre composition, texture, weight and care requirements need confirmation. Cotton and Polyester entries additionally contain one short, independently paraphrased general fact from inspected OpenStax textbooks, under General textile background, followed by “This does not verify the composition of this fabric reference.” No fibre percentage, certification, breathability, durability, wrinkle resistance, origin, stock or fabric-specific colour availability is inferred from a name.

“Super”, “Americano”, “Star” and “Dubai” are treated as the supplied reference labels. “Wool”, “Cotton” and “Polyester” labels likewise do not establish exact composition or a100% claim for Mr Sewing's particular fabric.

## General textile research attempted

| Source | Intended verification | Actual access/result | Use in public content |
| --- | --- | --- | --- |
| [US Federal Trade Commission: Threading Your Way Through the Labeling Requirements Under the Textile and Wool Acts](https://www.ftc.gov/business-guidance/resources/threading-your-way-through-labeling-requirements-under-textile-wool-acts) | General guidance on evidence for fibre-content descriptions | Managed proxy denied HTTPS CONNECT403 before the origin; document contents were **not read**. Captured headers `/tmp/r48-ftc-textile.headers`. | No claim or quotation attributed to this unread source. |
| [US Federal Trade Commission: Clothes Captioning — Complying with the Care Labeling Rule](https://www.ftc.gov/business-guidance/resources/clothes-captioning-complying-care-labeling-rule) | General care-label information | Managed proxy denied HTTPS CONNECT403 before the origin; document contents were **not read**. Captured headers `/tmp/r48-ftc-care.headers`. | No care recommendation or legal-compliance claim attributed to this unread source. |
| [Official USGPO CFR XML User Guide](https://raw.githubusercontent.com/usgpo/bulk-data/main/CFR-XML_User-Guide.md) | Possible accessible route to original textile/care regulatory text | Successfully fetched and read; it explains XML structure and contains no relevant textile facts. Local evidence `/tmp/r48-usgpo-cfr-guide.md`. | Not used as a textile citation. |

The FTC links above record research attempts and future verification targets; listing them does not establish that their contents were inspected. Original company handbooks and supplier specifications remain unavailable. Additional original academic sources were subsequently retrieved successfully:

| Source / central sourceRef | Inspected passage and source revision | Independent factual paraphrase used |
| --- | --- | --- |
| `openstax-cotton-cellulose`: [OpenStax Organic Chemistry, Polysaccharides and Their Synthesis — Cellulose](https://github.com/openstax/osbooks-organic-chemistry/blob/72cb625c8ffd62c4eecf04fbe2389ae4e8db2f14/modules/m00307/index.cnxml#L18) | Official OpenStax source, revision `72cb625c8ffd62c4eecf04fbe2389ae4e8db2f14`; section Cellulose, paragraph `para-00003`, identifies cotton as primarily cellulosic material. Entire relevant section read. | Cotton fibre is made mainly of cellulose. Used only as general background on `men-cotton` and `women-cotton`. |
| `openstax-polyester-polymers`: [OpenStax Organic Chemistry, Polyamides and Polyesters: Step-Growth Polymers](https://github.com/openstax/osbooks-organic-chemistry/blob/72cb625c8ffd62c4eecf04fbe2389ae4e8db2f14/modules/m00247/index.cnxml) and [chapter summary passage identifying polyester in clothing](https://github.com/openstax/osbooks-organic-chemistry/blob/72cb625c8ffd62c4eecf04fbe2389ae4e8db2f14/modules/m00255/index.cnxml#L445) | Same original source/revision; paragraphs `para-00001`–`para-00002`, step-growth polymer table and chapter-summary paragraph `para-00071` read. These describe polyester polymers and an example used for clothing fibres. | Polyesters are polymers that can be manufactured into clothing fibres. Used only as general background on `men-polyester` and `women-polyester`. |
| Supplementary confirmation: [OpenStax Chemistry textbook module on liquids and solids](https://github.com/openstax/osbooks-chemistry-bundle/blob/78b742a7fed1379705c5d882cee1ebfab7f58dc9/modules/m68764/index.cnxml#L152) | Official OpenStax Chemistry bundle revision `78b742a7fed1379705c5d882cee1ebfab7f58dc9`; paragraph `fs-idm57496496` discusses cellulose molecules in cotton. Relevant passage read. | Corroborates the general cellulose relationship. Its water-interaction discussion is **not** presented as a performance or care claim about any Mr Sewing fabric. |

The repositories' README files explicitly identify OpenStax as part of Rice University and link the original textbooks. Source material was read directly from the original publisher repositories, not a third-party mirror. Local read-only evidence is in `/tmp/r48-openstax-organic` and `/tmp/r48-openstax-chemistry`; no textbook files were added to the website repository. Access checked13November2026. The books' repository licensing is Attribution-NonCommercial-ShareAlike4.0; this implementation uses only independently worded basic scientific facts, with no copied instructional prose, diagrams or photographs.

These limited general definitions establish neither the blend nor the technical performance of the company's actual reference fabrics. No general care, breathability, durability or skin-feel claim is published. Wool, Super, Americano, Star and Dubai remain without an inferred technical composition. A customer still sees the specific confirmation notice for every reference.

## Deliberately unpublished details

Exact fibre composition/percentages, fabric weight and weave, texture/feel measurements, performance characteristics, detailed care instructions, additional product photographs and confirmed colours by fabric are unverified. Publish such information only after the specific supplied fabric has supporting evidence. General illustrative colour preferences are a separate enquiry feature and must not imply availability for every reference.

Future customer-garment examples remain unpublished pending the image permissions and fabric identification required by the owner. This update does not import internet photographs or invent company inventory.

## Implementation boundaries and checks

Only `cards()` and `fabric_guide()` changed in `scripts/customer_guides.py`; `measurements()`, `options()`, `script()` and `fabric_request_notes()` remain byte-identical to baselinec1428b9. The old policy-note function remains available to legitimate existing consumers, but the Fabric Guide no longer invokes it. Existing commercial facts remain on their service, FAQ and Terms pages.

`_data/fabric-reference-catalogue.json` changes only customer descriptions, a specification-confirmation note, and the four short general-background entries with their sourceRef citations. `_templates/fabric-guide.css` is scoped to `.fabric-guide-page`; it provides compact cards, native keyboard-operable details and44px-minimum details/selection targets. Parent integration attaches Select This Fabric only in an active quotation-selection context.

Completed local checks: Python syntax compilation; eight cards and eight native details controls; exactly four general-background passages each separated from company specifications by an explicit confirmation notice; unchanged approved ID/name/tier/category/image mappings; exact preservation of the measurement/options/script/policy-note function tail; no price links, Express or children's promotion content in the guide renderer. End-to-end generated-page, mobile, selection and backend validation are performed by the parent task after integration.
