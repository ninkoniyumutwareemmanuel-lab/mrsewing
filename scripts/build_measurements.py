#!/usr/bin/env python3
"""Render the existing measurement guide with the canonical shared components."""
import argparse,json,re
from html import escape
from site_seo import ROOT,finalize
from sync_page_seo import apply
from shared_components import header,footer,component_css
from homepage_resources import delivery,CSS as ICON_CSS
from build_homepage import reserve_image_space

def outputs():
    data=json.loads((ROOT/'_data/measurements.json').read_text())
    assert len(data['measurements'])==12 and len(data['questions'])==4
    content='<section class="measure-intro"><p class="home-eyebrow">Made to your measurements</p><h1>Suit Measurement &amp; Sizing Guide</h1><p>Prepare for your fitting or share your measurements with the team. Explore the twelve-point guide below.</p><nav class="measure-actions" aria-label="Measurement options"><a class="home-button home-button-gold" href="/measurement-submission/">Submit your measurements <span class="home-arrow" aria-hidden="true"></span></a><a class="home-text-link" href="/booking/">Request a fitting</a></nav></section>'
    content+='<section class="measure-methods"><h2>Choose how to get measured.</h2><div class="measure-method-grid">'
    methods=[('Workshop or mobile fitting','Arrange professional measurements at the workshop or discuss a mobile fitting with the team.'),('Professional tailor','Have an experienced local tailor measure you using this twelve-point guide if you cannot visit.'),('Assisted home measurements','Ask a trusted family member or friend to help hold the tape. Do not take your measurements alone.'),('Standard size reference','Share a size from an unadjusted garment that fits you, and discuss it with the team.')]
    for title,text in methods:content+='<section><h3>'+title+'</h3><p>'+text+'</p></section>'
    content+='</div></section><section class="measure-guide" id="measurement-guide"><h2>The twelve-point guide.</h2><p>Use the illustrations and instructions below. Provide direct body measurements without adding extra room, and state whether you used centimetres or inches.</p><div class="measurement-grid">'
    for n,m in enumerate(data['measurements'],1):
        assert (ROOT/m['image'].lstrip('/')).is_file()
        content+='<article class="measurement-card"><a class="measure-image-link" data-measure-image="'+escape(m['title'],quote=True)+'" href="'+m['image']+'" aria-label="Enlarge '+escape(m['title'],quote=True)+' measurement illustration"><img src="'+m['image']+'" width="'+str(m['width'])+'" height="'+str(m['height'])+'" alt="'+escape(m['alt'],quote=True)+'" loading="'+('eager' if n==1 else 'lazy')+'" decoding="async"><span>View illustration <span aria-hidden="true">↗</span></span></a><h3><span class="measurement-number">'+str(n).zfill(2)+'</span>'+escape(m['title'])+'</h3><p>'+escape(m['description'])+'</p></article>'
    content+='</div></section><section class="measure-faq"><h2>Before you send your measurements.</h2>'
    for q in data['questions']:content+='<details><summary>'+escape(q['question'])+'</summary><p>'+escape(q['answer'])+'</p></details>'
    content+='</section><nav class="measure-next" aria-label="Continue with your measurements"><a class="home-button home-button-gold" href="/measurement-submission/">Submit your measurements <span class="home-arrow" aria-hidden="true"></span></a><a class="home-text-link" href="/faq/measurements-fittings/">Measurements &amp; fittings FAQs</a><a class="home-text-link" href="/services/mobile-fitting/">Mobile fitting</a></nav><dialog class="measure-viewer" id="measurement-viewer" aria-label="Measurement illustration"><button type="button">Close illustration</button><img alt=""><p></p></dialog>'
    source=(ROOT/'_templates/measurements.html').read_text()
    values={'styles':component_css()+'\n'+ICON_CSS+'\n'+(ROOT/'_templates/measurements.css').read_text(),'header':delivery(re.sub(r'<img\b[^>]*>',reserve_image_space,header('/measurements/')),'header'),'footer':delivery(footer(),'footer'),'content':content}
    for key,value in values.items():source=source.replace('{{'+key+'}}',value)
    assert not re.search(r'{{\w+}}',source)
    metadata=json.loads((ROOT/'_data/page-seo.json').read_text())['measurements.html']
    source=finalize(apply(source,metadata),ROOT/'measurements.html')
    return {ROOT/'measurements.html':source,ROOT/'assets/measurements.js':(ROOT/'_templates/measurements.js').read_text()}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    for path,value in outputs().items():
        if args.check:
            if not path.exists() or path.read_text()!=value:raise SystemExit('Stale measurement output: '+str(path.relative_to(ROOT)))
        else:path.write_text(value)
    print('PASS: shared measurement guide, twelve preserved illustrations/instructions and image viewer '+('synchronized.' if args.check else 'generated.'))
if __name__=='__main__':main()
