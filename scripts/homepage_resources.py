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
            return re.sub(r'\bsizes="[^"]*"','sizes="(min-width: 1100px) 66px, 72px"',tag)
        if key not in ('customers','collections') or name=='h1.jpeg' or name not in media:return tag
        entry=media[name]
        # The editorial portraits are 3:4 crops; responsive candidates include
        # source pixels needed to preserve the centered garment at each width.
        cover=max(1,(4/3)*entry['width']/entry['height'])
        sizes=(f'(min-width: 1264px) {384*cover:.1f}px, (min-width: 1100px) calc((100vw - 112px) / 3 * {cover:.4f}), (min-width: 600px) calc((100vw - 64px) * {0.6*cover:.4f}), calc((100vw - 40px) * {0.86*cover:.4f})' if key=='customers'
               else '(min-width: 1264px) 258px, (min-width: 1100px) calc((100vw - 120px) * .225), (min-width: 600px) calc((100vw - 64px) * .45), calc((100vw - 40px) * .45)')
        tag=re.sub(r'\bsizes="[^"]*"',lambda _:f'sizes="{sizes}"',tag)
        return f'<picture class="homepage-picture"><source type="image/avif" srcset="{source_set(entry)}" sizes="{sizes}">{tag}</picture>'
    markup=re.sub(r'<img\b[^>]*>',image,markup)

    return markup


def hero_preloads():
    # Derive the hint from the source portrait so photo/layout edits have one
    # source of truth. Omit href to avoid unsupported responsive double-fetches.
    source=(ROOT/'_templates/homepage-sections.html').read_text()
    match=re.search(r'<img\b(?=[^>]*\bclass="[^"]*\bhero-lcp\b)[^>]*>',source)
    if not match:raise ValueError('Homepage needs an explicit hero portrait')
    attrs=dict(re.findall(r'([\w-]+)="([^"]*)"',match[0]))
    if not all(attrs.get(key) for key in ('srcset','sizes')):
        raise ValueError('Hero portrait needs srcset and sizes for matched preloading')
    candidates=escape(unescape(attrs['srcset']),quote=True)
    sizes=escape(unescape(attrs['sizes']),quote=True)
    return f'<link rel="preload" as="image" imagesrcset="{candidates}" imagesizes="{sizes}" fetchpriority="high">'


CSS='''
/* Original licensed SVG paths; no icon font or third-party stylesheet requests. */
.homepage-icon { display:inline-block; font-style:normal; line-height:1; }
.homepage-icon svg { height:1em; fill:currentColor; vertical-align:-.125em; overflow:visible; }
picture.homepage-picture { display:contents; }
'''
