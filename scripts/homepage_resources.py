"""Homepage-only static resource substitutions. Other standalone pages keep their assets."""
from html import escape, unescape
import json
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parents[1]

def source_set(entry):
    return ', '.join(f'{v["src"]} {v["width"]}w' for v in entry['variants'])

def delivery(markup, key):
    media=json.loads((ROOT/'_data/homepage-media.json').read_text())
    icons=json.loads((ROOT/'_data/homepage-icons.json').read_text())
    def icon(match):
        classes=match[1];name=next(c[3:] for c in classes.split() if c.startswith('fa-'))
        name={'pencil-ruler':'pen-ruler','map-marker-alt':'location-dot'}.get(name,name)
        svg=icons[name]
        dims=re.search(r'viewBox="0 0 (\d+) (\d+)"',svg);width=int(dims[1])/int(dims[2])
        svg=svg.replace('<svg ',f'<svg aria-hidden="true" focusable="false" style="width:{width:g}em" ',1)
        return f'<i class="{classes} homepage-icon" aria-hidden="true">{svg}</i>'
    markup=re.sub(r'<i class="([^"]*\b(?:fas|fab)\b[^"]*)"></i>',icon,markup)
    def image(match):
        tag=match[0];m=re.search(r'\bsrc="([^"]+)"',tag)
        if not m:return tag
        name=unescape(m[1])
        if name=='MR LOGO.jpeg':
            tag=re.sub(r'\bsrcset="[^"]*"',lambda _:f'srcset="{source_set(media[name])}"',tag)
            return re.sub(r'\bsizes="[^"]*"','sizes="(max-width: 600px) 64px, 70px"',tag)
        if key not in ('customers','collections') or name=='h1.jpeg' or name not in media:return tag
        # Slider cards retain the existing 4:5 crop; collection cards contain
        # the full garment and need no extra source pixels for cover cropping.
        entry=media[name]
        cover=max(1,1.25*entry['width']/entry['height'])
        sizes=(f'(max-width: 900px) {158*cover:.1f}px, {218*cover:.1f}px' if key=='customers'
               else '(max-width: 600px) calc(46vw - 6px), (max-width: 1000px) calc(46vw - 9px), (max-width: 1217px) calc(23vw - 13.5px), 266.5px')
        tag=re.sub(r'\bsizes="[^"]*"',lambda _:f'sizes="{sizes}"',tag)
        return f'<picture class="homepage-picture"><source type="image/avif" srcset="{source_set(entry)}" sizes="{sizes}">{tag}</picture>'
    markup=re.sub(r'<img\b[^>]*>',image,markup)
    if key=='hero':
        entry=media['The Executive Line.jpeg']
        picture=f'<picture class="homepage-hero-media"><source media="(max-width: 1024px)" type="image/avif" srcset="{source_set(entry)}" sizes="100vw"><img class="hero-lcp" src="The Executive Line.jpeg" alt="" width="1536" height="2752" loading="eager" fetchpriority="high" decoding="async"></picture>'
        markup=markup.replace('<section class="hero-section">','<section class="hero-section">\n'+picture,1)
    return markup


def hero_preloads():
    media=json.loads((ROOT/'_data/homepage-media.json').read_text())['The Executive Line.jpeg']
    # Match the picture's candidates exactly. Omit href on the responsive hint:
    # browsers without imagesrcset-preload support must not preload the largest
    # AVIF and then download a second, smaller picture candidate.
    return (f'<link rel="preload" as="image" imagesrcset="{source_set(media)}" imagesizes="100vw" media="(max-width: 1024px)" type="image/avif" fetchpriority="high">\n'
            '  <link rel="preload" as="image" href="The%20Executive%20Line.jpeg" media="(min-width: 1025px)" fetchpriority="high">')


CSS='''
/* Homepage-only SVGs use the same Font Awesome 6.4.0 paths; no icon font request. */
.homepage-icon { display:inline-block; font-style:normal; font-variant:normal; line-height:1; }
.homepage-icon svg { height:1em; fill:currentColor; vertical-align:-.125em; overflow:visible; }
picture.homepage-picture { display:contents; }
.hero-section { background:#0b0b0b; isolation:isolate; }
.homepage-hero-media { position:absolute; inset:0; z-index:-2; pointer-events:none; }
.homepage-hero-media img { width:100%; height:100%; object-fit:cover; object-position:center; display:block; }
.hero-section::before { content:""; position:absolute; inset:0; z-index:-1; pointer-events:none; background:linear-gradient(rgba(11,11,11,.75),rgba(11,11,11,.85)); }
footer .footer-bottom-copy p { color:#888888; }
'''
