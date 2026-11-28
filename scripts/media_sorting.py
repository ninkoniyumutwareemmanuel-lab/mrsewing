"""Publication ordering, with the evidence-backed R59 migration fallback.

New records use timezone-aware ``published_at`` plus ``published_at_evidence``
for their first public publication. Equal timestamps use the stable ID/slug.
An ordinary caption/updated_at edit never changes this date. Do not infer dates
from filenames, array positions or the time of a website build.

Historical source-backed mediaDateAdded fields retain their established R59
migration order, including equal-day ties. They may describe an upload rather
than publication and are not represented as verified publication chronology.
Records without verified dates stay in their established input order, last.

Sort whole design/project records, never their individual views. Rights and
publication gating happen BEFORE this helper; pagination/slicing happen AFTER.
This helper deliberately does not replace service-specific publication gates.
"""
from datetime import date, datetime, timezone
import re


def verified_publication(record):
    """Return an aware UTC datetime only with explicit timestamp evidence."""
    value = record.get('published_at')
    evidence = record.get('published_at_evidence')
    if not isinstance(value, str) or not isinstance(evidence, str) or not evidence.strip():
        return None
    # Require a complete ISO date/time. Date-only or local time is ambiguous.
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})', value):
        return None
    try:
        parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return parsed.astimezone(timezone.utc) if parsed.utcoffset() is not None else None
    except (ValueError, OverflowError):
        return None

def verified_day(record):
    value=record.get('mediaDateAdded')
    evidence=record.get('mediaDateEvidence')
    basis=record.get('mediaDateBasis')
    if not isinstance(value,str) or not isinstance(evidence,str) or not evidence.strip():
        return None
    if basis not in ('verified-upload','verified-publication','verified-added'):
        return None
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}',value):
        return None
    try:return date.fromisoformat(value).toordinal()
    except ValueError:return None

def newest_first(items,evidence=None):
    """Verified publications first, then documented legacy dates/unknown order.

    Callers may pass authoritative raw records as ``evidence`` when their public
    projections omit the private date evidence. Return the original projections
    without adding evidence fields or flattening a family's image collection.
    """
    source=evidence or {}
    def key(item):
        record=source.get(item.get('id'),item) if isinstance(source,dict) else item
        publication = verified_publication(record)
        if publication is not None:
            ident = item.get('id') or item.get('slug') or record.get('id') or record.get('slug')
            # A timestamp with no stable identifier cannot meet the new contract.
            if isinstance(ident, str) and ident.strip():
                return (0, -publication.timestamp(), ident)
        ordinal=verified_day(record)
        return (1,-ordinal,'') if ordinal is not None else (2,0,'')
    return sorted(items,key=key)
