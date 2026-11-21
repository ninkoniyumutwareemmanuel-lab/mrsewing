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
    pat=r'(<section class="privacy-card release-section" id="5" data-number="05"><h2>Selections, cookies and analytics</h2>)(<p>[\s\S]*?</p>)(<p>[\s\S]*?</p>)(<p>[\s\S]*?</p>)(</section>)'
    def expand(m):
        h,p1,p2,p3,close=m.groups()
        return h+'<h3>Website selections and drafts</h3>'+p1+'<h3>Returning to an unfinished enquiry</h3>'+p2+'<h3>Advertising cookies and Meta Pixel</h3>'+p3+'<p class="privacy-cookie-help">You can change your advertising cookie choice using <strong>Cookie preferences</strong> in the website footer.</p>'+close
    rest,n=re.subn(pat,expand,rest,count=1)
    if n!=1:raise ValueError('Privacy cookies paragraph structure changed')
    def toc():
        return ''.join('<a href="#'+str(s['id'])+'"><span>'+str(i+1).zfill(2)+'</span>'+escape(s['title'])+'</a>' for i,s in enumerate(config['sections']))
    return '<style id="privacy-v2-css">'+css+'</style><div class="privacy-hero-shell"><div class="privacy-hero-inner">'+hero+'<p class="privacy-updated">Privacy information · Updated '+config['updated']+'</p></div></div><div class="privacy-layout"><aside class="privacy-sidebar" aria-label="Privacy Policy sections"><nav class="privacy-toc" aria-label="On this page"><p class="privacy-toc-title">On this page</p>'+toc()+'</nav><div class="privacy-sidebar-note">Need help with a privacy question?<a href="/contact/">Contact Mr Sewing ↗</a></div></aside><div class="privacy-content"><details class="privacy-mobile-toc"><summary>Jump to a section</summary><nav class="privacy-mobile-links" aria-label="Jump to a policy section">'+toc()+'</nav></details>'+config['summary']+rest+'<section class="privacy-contact-card" aria-labelledby="privacy-contact-heading"><div><h2 id="privacy-contact-heading">Questions about your privacy?</h2><p>Contact the Mr Sewing Fashion team using our official website contact channels.</p></div><a href="/contact/">Contact us ↗</a></section></div></div>'
