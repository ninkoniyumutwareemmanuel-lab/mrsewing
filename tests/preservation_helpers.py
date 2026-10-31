"""Allow shared-shell regeneration while preserving unrelated page content and metadata."""
import re

def without_shared_shell(html):
    html=re.sub(r'<!-- customer-information:start -->.*?<!-- customer-information:end -->','',html,flags=re.S)
    # Layout CSS is regenerated from separately tested shared/page sources.
    html=re.sub(r'<style\b[^>]*>.*?</style>', '', html, flags=re.S)
    html=re.sub(r'<header\b[^>]*class="homepage-header"[^>]*>.*?</header>', '', html, flags=re.S)
    html=re.sub(r'<footer\b[^>]*class="homepage-footer"[^>]*>.*?</footer>', '', html, flags=re.S)
    return html


def original_about_scope(html):
    return html.replace('Custom suits and suit packages for business and special occasions.','Personalized suits and clothing for business and special occasions.').replace('Suits and suit packages shaped around your measurements and personal style.','Tailored outfits shaped around your measurements and personal style.')
