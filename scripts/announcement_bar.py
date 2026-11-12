"""Shared approved OFFER presentation; callers explicitly opt in by page scope."""
from html import escape
from pathlib import Path
import json,re

ROOT=Path(__file__).resolve().parents[1]

def decorate(source):
    """Keep the existing brand header and offer in one sticky, measured stack."""
    assert 'class="announcement-bar"' not in source, 'Do not duplicate OFFER bars'
    offer=json.loads((ROOT/'_data/custom-tailoring-page.json').read_text())['announcement']
    messages=''.join('<span class="announcement-message">'+escape(message)+'</span>' for message in offer['messages'])
    bar=(ROOT/'_templates/announcement-bar.html').read_text().replace('{{offer_messages}}',messages)
    if 'id="site-header"' in source:
        # Service/category frames already wrap the unmodified shared header.
        assert source.count('</div><main id="main-content"')==1
        source=source.replace('</div><main id="main-content"',bar+'</div><main id="main-content"',1)
    else:
        # Existing design details use the same header without its outer wrapper.
        source,count=re.subn(r'(<header\b[^>]*class="homepage-header"[^>]*>.*?</header>)',lambda m:'<div id="site-header">'+m[1]+bar+'</div>',source,count=1,flags=re.S)
        assert count==1, 'Expected exactly one shared brand header'
    styles=(ROOT/'_templates/announcement-bar.css').read_text()
    source=source.replace('</style>',styles+'</style>',1)
    return source.replace('</body>','<script>'+(ROOT/'_templates/announcement-bar.js').read_text()+'</script></body>',1)
