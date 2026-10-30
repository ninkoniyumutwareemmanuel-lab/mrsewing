"""Allow shared-shell regeneration while preserving unrelated page content and metadata."""
import re

def without_shared_shell(html):
    # Layout CSS is regenerated from separately tested shared/page sources.
    html=re.sub(r'<style\b[^>]*>.*?</style>', '', html, flags=re.S)
    html=re.sub(r'<header\b[^>]*class="homepage-header"[^>]*>.*?</header>', '', html, flags=re.S)
    html=re.sub(r'<footer\b[^>]*class="homepage-footer"[^>]*>.*?</footer>', '', html, flags=re.S)
    return html
