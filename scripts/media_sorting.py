"""R59 verified-date ordering: unknown dates remain in their established stable order.

Date belongs to a design/project group, not each image view; upload date is NOT
a garment manufacturing date. Rights/publication gating happens before sorting.
Only a source-backed YYYY-MM-DD date qualifies. Other date text is ignored.
"""
from datetime import date
import re

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
    """Stable, evidence-only descending dates. Undated records retain input order."""
    source=evidence or {}
    def key(item):
        record=source.get(item.get('id'),item) if isinstance(source,dict) else item
        ordinal=verified_day(record)
        return (0,-ordinal) if ordinal is not None else (1,0)
    return sorted(items,key=key)
