#!/usr/bin/env python3
"""Generate high-quality homepage-only AVIF and lossless logo candidates; keep originals."""
from pathlib import Path
from PIL import Image,ImageOps,ImageChops,ImageStat
import json,math,hashlib
ROOT=Path(__file__).resolve().parents[1];out=ROOT/'assets/homepage';out.mkdir(exist_ok=True)
for old in out.glob('*'):
 if old.suffix in ['.avif','.webp']:old.unlink()
sources=['The Executive Line.jpeg','MR LOGO.jpeg','h2.jpeg','h3.jpeg','r2.jpeg','r3.jpeg','r4.jpeg','r5.jpeg','r6.jpeg','r7.jpeg','r8.jpeg'];manifest={}
for name in sources:
 with Image.open(ROOT/name) as opened:
  image=ImageOps.exif_transpose(opened);logo=name=='MR LOGO.jpeg';hero=name=='The Executive Line.jpeg'
  widths=[96,192,320] if logo else [480,768,1024,1536] if hero else [160,240,320,480,640,960,1280] if name in ['h2.jpeg','h3.jpeg','r2.jpeg','r3.jpeg','r4.jpeg','r5.jpeg','r6.jpeg','r7.jpeg','r8.jpeg'] else [320,480,768,1024]
  variants=[]
  for width in sorted(set(min(w,image.width) for w in widths)):
   resized=image.resize((width,round(image.height*width/image.width)),Image.Resampling.LANCZOS)
   ext='webp' if logo else 'avif';target=out/(name[:-5].strip().replace(' ','-').lower()+f'-{width}.'+ext)
   if logo:resized.save(target,'WEBP',lossless=True,method=6)
   else:resized.save(target,'AVIF',quality=82,speed=6,max_threads=2,subsampling='4:2:0' if hero else '4:4:4')
   # Hashed immutable names help avoid stale replacements, without pretending
   # that GitHub Pages lets this repository set a long Cache-Control lifetime.
   digest=hashlib.sha256(target.read_bytes()).hexdigest()[:10];hashed=target.with_name(target.stem+'.'+digest+target.suffix);target.rename(hashed)
   a=resized.convert('RGBA');b=Image.open(hashed).convert('RGBA');errors=[]
   for color in ['black','white']:
    background=Image.new('RGBA',a.size,color);rms=ImageStat.Stat(ImageChops.difference(Image.alpha_composite(background,a).convert('RGB'),Image.alpha_composite(background,b).convert('RGB'))).rms;errors.append(sum(v*v for v in rms)/3)
   mse=max(errors);psnr=10*math.log10(255**2/mse) if mse else None
   variants.append({'width':width,'src':hashed.relative_to(ROOT).as_posix(),'bytes':hashed.stat().st_size,'psnr':psnr})
  manifest[name]={'width':image.width,'height':image.height,'variants':variants,'originalBytes':(ROOT/name).stat().st_size}
(ROOT/'_data/homepage-media.json').write_text(json.dumps(manifest,indent=2)+'\n');print('Homepage media derivatives:',sum(len(v['variants']) for v in manifest.values()));print('Non-logo min PSNR:',min(v['psnr'] for k,x in manifest.items() if k!='MR LOGO.jpeg' for v in x['variants'] if v['psnr'] is not None))
