"""Responsive Privacy Policy presentation using the existing approved policy text."""
from pathlib import Path
from html import escape
import json,re
ROOT=Path(__file__).resolve().parents[1]
def decorate(body):
    config=json.loads((ROOT/'_data/privacy-layout.json').read_text())
    css=config['css'];cut=body.index('</section>')+len('</section>')
    hero=body[:cut].replace('class="release-intro"','class="privacy-hero-intro release-intro"',1)
    rest=body[cut:]
    rest,n=re.subn(r'<section class="release-section" id="([1-7])">',lambda m:'<section class="privacy-card release-section" id="'+m[1]+'" data-number="'+m[1].zfill(2)+'">',rest)
    if n!=7:raise ValueError('Expected seven privacy sections')
    # Add links to public privacy resources after escaping the source disclosure text.
    rest=rest.replace('https://www.facebook.com/privacy/policy/','<a href="https://www.facebook.com/privacy/policy/" target="_blank" rel="noopener noreferrer">Meta privacy policy</a>')
    rest=rest.replace('https://policies.google.com/privacy','<a href="https://policies.google.com/privacy" target="_blank" rel="noopener noreferrer">Google privacy policy</a>')
    rest=rest.replace('https://dpo.gov.rw/','<a href="https://dpo.gov.rw/" target="_blank" rel="noopener noreferrer">Rwanda Data Protection &amp; Privacy Office</a>')
    def toc():
        return ''.join('<a href="/privacy-policy/#'+str(s['id'])+'"><span>'+str(i+1).zfill(2)+'</span>'+escape(s['title'])+'</a>' for i,s in enumerate(config['sections']))
    return '<style id="privacy-v2-css">'+css+'</style><div class="privacy-hero-shell"><div class="privacy-hero-inner">'+hero+'<p class="privacy-updated">Privacy information · Updated '+config['updated']+'</p></div></div><div class="privacy-layout"><aside class="privacy-sidebar" aria-label="Privacy Policy sections"><nav class="privacy-toc" aria-label="On this page"><p class="privacy-toc-title">On this page</p>'+toc()+'</nav><div class="privacy-sidebar-note">Need help with a privacy question?<a href="/contact/">Contact Mr Sewing ↗</a></div></aside><div class="privacy-content"><details class="privacy-mobile-toc"><summary>Jump to a section</summary><nav class="privacy-mobile-links" aria-label="Jump to a policy section">'+toc()+'</nav></details>'+config['summary']+rest+'<section class="privacy-contact-card" aria-labelledby="privacy-contact-heading"><div><h2 id="privacy-contact-heading">Questions about your privacy?</h2><p>Contact the Mr Sewing Fashion team using our official website contact channels.</p></div><a href="/contact/">Contact us ↗</a></section></div></div>'
