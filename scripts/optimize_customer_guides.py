#!/usr/bin/env python3
"""Optional asset-preparation task; committed derivatives keep runtime builds dependency-free.
Requires Pillow only when regenerating. Originals are never modified.
"""
from pathlib import Path
from PIL import Image,ImageOps
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]
fabrics=[('super','Super / Super 100s'),('wool','Wool'),('polyester','Polyester'),('cotton','Cotton'),('americano','Americano'),('star','Star')]
measurements=[('belly','Belly','belly.webp','Tape shown around the stomach area'),('bicep','Bicep','bicep.webp','Tape shown around the upper arm'),('chest','Chest','chest.webp','Tape shown around the chest'),('hip','Hip','hip.webp','Tape shown around the hips'),('jacket-length','Jacket length','jacket length.webp','Front-view illustration of jacket length'),('neck','Neck','neck.webp','Tape shown around the neck at collar level'),('shoulder','Shoulder','shoulder.webp','Tape shown across the back of the shoulders'),('sleeve-length','Sleeve length','sleeve length.webp','Illustration of sleeve length along the arm'),('thigh','Thigh','thigh.webp','Tape shown around the upper thigh'),('trouser-length','Trouser length','trauser length.webp','Illustration of trouser length along the outer leg'),('waist','Waist','waist.webp','Tape shown around the trouser waistline')]
images={}
for key,path,alt in [(f'fabric-{k}',f'fabric-{k}.webp',f'Illustrative {name} fabric reference, not verified stock') for k,name in fabrics]+[(f'measure-{key}',path,alt) for key,_,path,alt in measurements]:
 p=ROOT/path;im=ImageOps.exif_transpose(Image.open(p)).convert('RGB');record={'src':'/'+path,'width':im.width,'height':im.height,'alt':alt,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'variants':[]}
 for w in [480,960]:
  if w>=im.width:continue
  scaled=im.resize((w,round(im.height*w/im.width)),Image.Resampling.LANCZOS);dest=ROOT/'assets/customer-guides'/f'{key}-{w}.webp';dest.parent.mkdir(parents=True,exist_ok=True);scaled.save(dest,'WEBP',quality=82,method=6)
  if dest.stat().st_size<p.stat().st_size:record['variants'].append({'src':'/'+str(dest.relative_to(ROOT)),'width':scaled.width,'height':scaled.height})
 images[key]=record
(ROOT/'_data/customer-guide-images.json').write_text(json.dumps({'source':'Owner R3 uploaded illustrative reference photographs; originals preserved','images':images},indent=2)+'\n')
items=[]
for category,mapping in [('men',[('super','Super / Super 100s'),('wool','Wool'),('polyester','Polyester'),('cotton','Cotton / Dubai')]),('women',[('americano','Americano'),('star','Star'),('polyester','Polyester'),('cotton','Cotton')])]:
 for tier,(key,name) in enumerate(mapping,1):items.append({'id':category+'-'+key,'category':category,'name':name,'tier':tier,'image':'fabric-'+key,'startingPriceRwf':None,'priceStatus':'Price on request','colourStatus':'Ask us about available colours.','description':f'Working local reference label: {name}. Ask the team to confirm the actual material and suitability for your garment.','availability':'Illustrative reference only. Fabric, colour availability and final quotation require business confirmation.'})
(ROOT/'_data/fabric-reference-catalogue.json').write_text(json.dumps({'source':'Owner R3 working categories; 5 November2026 addendum reports V5 labels, original Sources inaccessible','approvalStatus':'WORKING REFERENCE — source/stock/composition confirmation pending','fabrics':items},ensure_ascii=False,indent=2)+'\n')
(ROOT/'_data/measurement-guide-images.json').write_text(json.dumps({'source':'Owner R3 uploaded images, inspected 5 November2026','neckDecision':'neck.jepg.webp and neck.webp are byte-identical; use neck.webp','instructions':'Existing six guide sections preserved. Pictures are illustrative, not calibrated measurements or a new method.','measurements':[{'id':key,'title':name,'image':'measure-'+key,'caption':alt+'. Follow the garment-specific instructions confirmed with the team.'} for key,name,_,alt in measurements]},indent=2)+'\n')
print('Prepared',len(images),'source mappings and',sum(len(i['variants']) for i in images.values()),'smaller guide derivatives.')
