"""Approved responsive refund policy presentation. Does not change refund policy or submission logic."""
from pathlib import Path
from html import escape
import json,re
ROOT=Path(__file__).resolve().parents[1]

def decorate(body):
    config=json.loads((ROOT/'_data/refund-layout.json').read_text())
    css=config['css']
    cut=body.index('</section>')+len('</section>')
    hero=body[:cut].replace('class="release-intro"','class="refund-hero-intro release-intro"',1)
    rest=body[cut:]
    rest,n=re.subn(r'<section class="release-section" id="([1-5])">',lambda m:'<section class="refund-card release-section" id="'+m[1]+'" data-number="'+m[1].zfill(2)+'">',rest)
    if n!=5:raise ValueError('Expected five approved refund sections')
    old_form='<section class="release-section" aria-labelledby="request-title">'
    form='<section class="refund-form-card release-section" id="refund-request" aria-labelledby="request-title">'
    if rest.count(old_form)!=1:raise ValueError('Unexpected refund form structure')
    rest=rest.replace(old_form,form,1)
    old_title='<h2 id="request-title">Refund Request</h2>'
    if rest.count(old_title)!=1:raise ValueError('Refund heading changed')
    rest=rest.replace(old_title,'<p class="refund-form-kicker">Step 1 of 2 · Tell us about the issue</p><h2 id="request-title">Refund Review Request</h2>',1)
    old_button='<button type="button" id="reviewRequest" class="home-button home-button-gold" disabled>Continue</button>'
    if rest.count(old_button)!=1:raise ValueError('Refund review button changed')
    rest=rest.replace(old_button,'<button type="button" id="reviewRequest" class="home-button home-button-gold" disabled>Review Refund Request</button>',1)
    note='<p class="refund-policy-help">If you prefer to speak to us first, please use our <a href="/contact/">Contact page</a>. For privacy, do not include payment PINs or complete card information in your request.</p>'
    rest=rest.replace(form,note+form,1)
    def toc():
        links=''.join('<a href="/refund-policy/#'+str(s['id'])+'"><span>'+str(i+1).zfill(2)+'</span>'+escape(s['title'])+'</a>' for i,s in enumerate(config['sections']))
        return links+'<a href="/refund-policy/#refund-request"><span>→</span>Refund review form</a>'
    sidebar='<aside class="refund-sidebar" aria-label="Refund policy sections"><nav class="refund-toc" aria-label="On this page"><p class="refund-toc-title">On this page</p>'+toc()+'</nav><div class="refund-sidebar-note">Need help with an order concern?<a href="/contact/">Contact Mr Sewing ↗</a></div></aside>'
    mobile='<details class="refund-mobile-toc"><summary>Jump to a section</summary><nav class="refund-mobile-links" aria-label="Jump to a refund policy section">'+toc()+'</nav></details>'
    actions='<div class="refund-hero-actions"><a class="refund-primary" href="/refund-policy/#refund-request">Request a Review ↗</a><a class="refund-secondary" href="/contact/">Contact Support</a></div><p class="refund-hero-note">Requests are reviewed by our team. A request is not an approved refund.</p>'
    return '<style id="refund-v2-css">'+css+'</style><div class="refund-hero-shell"><div class="refund-hero-inner">'+hero+actions+'</div></div><div class="refund-layout">'+sidebar+'<div class="refund-content">'+mobile+config['summary']+rest+'</div></div>'
