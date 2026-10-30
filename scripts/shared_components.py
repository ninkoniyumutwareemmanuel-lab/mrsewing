"""Build-time V2 components: no browser HTML fetching or framework.

Only pages registered with build_site.py use these components. Legacy pages are
intentionally not migrated. site.css preserves the approved stylesheet verbatim;
component_css selects common rules for lighter non-homepage delivery.
"""
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parents[1]
SHARED = ROOT / '_templates/shared'

def header(page='/'):
    markup = (SHARED/'header.html').read_text().rstrip()
    if page != '/':
        markup = markup.replace('href="#customers-section"', 'href="/#customers-section"').replace('href="#services"', 'href="/#services"')
    return markup.replace(f'<a href="{page}">', f'<a href="{page}" aria-current="page">', 1)

def footer():
    return (SHARED/'footer.html').read_text().rstrip()

def site_css():
    return (SHARED/'site.css').read_text()

def menu_script():
    return (SHARED/'navigation.js').read_text()

def component_css():
    return shared_css(site_css())

def shared_css(source):
    """Select common design rules without shipping homepage gallery/hero styles.

The approved stylesheet uses ordinary rules and nested @media only. Unknown
at-rules fail explicitly so a future design change cannot silently corrupt CSS.
"""
    source = re.sub(r'/\*.*?\*/', '', source, flags=re.S)
    common = re.compile(r'^(?::root|\*|html|body|img|a(?=\s|$)|button|figure|h[123]|p(?=\s|$)|ul|ol|dl|dd|:focus-visible|\.home-shell|\.home-section|\.home-eyebrow|\.section-heading|\.home-button|\.home-text-link|\.home-arrow|\.visually-hidden|\.skip-link|#site-header|\.homepage-header|\.header-|\.home-brand|\.brand-name|\.home-menu-toggle|\.coming-soon|\.shop-nav|\.mobile-shop|\.js |\.home-final|\.final-|\.homepage-footer|\.footer-|\.social-icons)')
    output = []
    pos = 0
    while pos < len(source):
        start = source.find('{', pos)
        if start == -1:
            if source[pos:].strip():raise ValueError('Unexpected trailing design CSS')
            break
        selector = source[pos:start].strip()
        depth, end, quote = 1, start + 1, None
        while end < len(source) and depth:
            char = source[end]
            if quote:
                if char == quote and source[end-1] != '\\':quote = None
            elif char in "\"'":quote = char
            elif char == '{':depth += 1
            elif char == '}':depth -= 1
            end += 1
        if depth:raise ValueError('Unbalanced approved CSS')
        body = source[start+1:end-1]
        if selector.startswith('@media'):
            nested = shared_css(body)
            if nested.strip():output.append(selector + ' {\n' + nested + '\n}')
        elif selector.startswith('@'):
            raise ValueError('Unsupported design at-rule: ' + selector)
        else:
            selectors = [s.strip() for s in selector.split(',') if common.match(s.strip())]
            if selectors:output.append(', '.join(selectors) + ' {' + body + '}')
        pos = end
    return '\n'.join(output)
