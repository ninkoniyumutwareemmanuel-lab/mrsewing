#!/usr/bin/env python3
"""Validate the centralized design registry and build three static V2 showrooms."""
import argparse,csv,io,json,re
from html import escape
from pathlib import Path
from urllib.parse import quote
import shared_components as shared
from build_homepage import reserve_image_space
from build_clean_urls import legacy_script
from homepage_resources import delivery,CSS as ICON_CSS
ROOT=Path(__file__).resolve().parents[1]
PAGES={'collections.html':('all','Discover Your Signature Style.'),'mensuits.html':('men','Tailoring with Your Signature.'),'womensuits.html':('women','An Expression of Your Style.')}
SIZES='(min-width: 1100px) 280px, (min-width: 600px) 30vw, calc((100vw - 52px) / 2)'

def load():
    content=json.loads((ROOT/'_data/collection-designs.json').read_text());registry=json.loads((ROOT/'_data/collection-id-registry.json').read_text())
    ids=set(); slugs=set(); originals=set();published=[]
    assert content["schemaVersion"]==1
    optim=json.loads((ROOT/'_data/image-delivery.json').read_text());avif=json.loads((ROOT/'_data/homepage-media.json').read_text())
    for record in content['designs']:
        ident=record['id'];assert re.fullmatch(r'MS-\d{3,}',ident) and ident not in ids,ident;ids.add(ident)
        assert record['slug'] not in slugs and re.fullmatch(r'[a-z0-9-]+',record['slug']);slugs.add(record['slug'])
        assert isinstance(record['name'],str) and record['name'].strip()
        for key in ['styles','occasions','colors']:
            assert isinstance(record[key],list) and all(isinstance(v,str) and v for v in record[key])
        assert record['gender'] in ['men','women','unclassified']
        assert record['provenance'] in ['made_by_mr_sewing','design_inspiration','unverified']
        assert record['rightsStatus'] in ['review_required','approved','restricted']
        assert isinstance(record['published'],bool) and record['images']
        assert not record['published'] or record['rightsStatus']=='approved' or (record['rightsStatus']=='review_required' and record['publicationBasis']=='existing_public_display' and record['sources']),ident
        assert registry[ident]==record['sourceAnchor'],ident
        if record['provenance']!='unverified':assert record.get('provenanceEvidence'),ident
        if record['styles'] or record['occasions'] or record['colors']:assert record['metadataEvidence'],ident
        if len(record['images'])>1:assert record.get('groupingEvidence'),'Multi-image grouping needs evidence'
        images=[]
        for image in record['images']:
            path=ROOT/image['src'].lstrip('/');assert path.resolve().is_relative_to(ROOT) and path.is_file() and image['alt'] and image['width']>0 and image['height']>0,(ident,path)
            assert re.fullmatch(r'(?:center|top|bottom|left|right|\d{1,3}% \d{1,3}%)',image['position'])
            if '%' in image['position']:assert all(0<=int(v.rstrip('%'))<=100 for v in image['position'].split())
            original=image['originalPath'];originals.add(original)
            variants=optim.get(original,{}).get('variants',[])
            fallback=[v for v in variants if v['src'].endswith('.webp') and v['width']<=960]
            # Original fallback remains available; browser selects smaller candidates.
            candidates=[{'src':'/'+v['src'],'width':v['width']} for v in fallback]
            candidates.append({'src':image['src'],'width':image['width']})
            avifs=[{'src':'/'+v['src'],'width':v['width']} for v in avif.get(original,{}).get('variants',[]) if v['width']<=960]
            for v in candidates+avifs:assert (ROOT/v['src'].lstrip('/')).is_file(),v
            images.append({**{k:image[k] for k in ['alt','position','width','height']},'src':quote(image['src'],safe='/'),'thumb':quote(candidates[0]['src'],safe='/'),'srcset':', '.join(quote(v['src'],safe='/')+' '+str(v['width'])+'w' for v in candidates),'avif':', '.join(quote(v['src'],safe='/')+' '+str(v['width'])+'w' for v in avifs)})
        if record['published']:published.append({k:record[k] for k in ['id','slug','name','gender','styles','occasions','colors','garmentType','description','provenance']}|{'images':images})
    assert not ids.intersection(content['retiredIds'])
    assert set(registry)==ids|set(content['retiredIds']),'Registry entries must remain present or explicitly retired'
    assert content['nextId']>max(int(i.split('-')[1]) for i in registry)
    inventory=json.loads((ROOT/'_data/collection-image-inventory.json').read_text())
    source_records={r['id']:r for r in content['designs']}
    for row in inventory['images']:
        record=source_records.get(row['designId'])
        if record:
            row['provenance']=record['provenance'];row['rightsStatus']=record['rightsStatus']
            row['galleryLocation']='/collections/?design='+record['id'] if record['published'] else None
            row['groupedWithOtherPhotographs']=len(record['images'])>1
        elif row['designId'] in content['retiredIds']:
            row['galleryLocation']=None;row['excludedReason']='Design retired; source asset retained.'
    known={r['originalImagePath'] for r in inventory['images']}
    for path in ROOT.rglob('*'):
        if path.is_file() and '.git' not in path.parts and path.suffix.lower() in ['.jpeg','.jpg','.png','.webp','.avif','.gif','.svg']:
            assert str(path.relative_to(ROOT)) in known, 'Uninventoried asset: '+str(path)
    assert all((ROOT/r['originalImagePath']).is_file() for r in inventory['images'])
    # Preserve deterministic existing display order without coupling stable IDs to order.
    priorities={'m1.jpeg':0,'w-classicsuittwo1.jpeg':1,'r4.jpeg':2,'r7.jpeg':3,'h1.jpeg':4}
    path_by_id=registry
    published.sort(key=lambda d:(priorities.get(path_by_id[d['id']],10),d['id']))
    return published,inventory

def picture(image,eager=False):
    attrs=f'width="{image["width"]}" height="{image["height"]}" alt="{escape(image["alt"],quote=True)}" decoding="async" loading="'+('eager" fetchpriority="high"' if eager else 'lazy"')
    src=f'<img src="{image["thumb"]}" srcset="{image["srcset"]}" sizes="{SIZES if not eager else "(min-width: 768px) 340px, 50vw"}" {attrs} style="object-position:{image["position"]}">'
    return ('<picture><source type="image/avif" srcset="'+image['avif']+'" sizes="'+(SIZES if not eager else '(min-width: 768px) 340px, 50vw')+'">'+src+'</picture>') if image['avif'] else src

def card(design):
    return f'<article class="show-card" data-id="{design["id"]}"><a class="design-preview view-details-btn" href="/collections/?design={design["id"]}#design-{design["id"]}" data-open="{design["id"]}">{picture(design["images"][0])}<span class="show-card-copy"><span>{escape(design["name"])}</span><small>{design["id"]}</small></span></a><button class="save-design" data-save="{design["id"]}" aria-label="Save {design["id"]} to favourites" aria-pressed="false">♡</button></article>'

def render(name,gender,title,designs):
    seo=json.loads((ROOT/'_data/page-seo.json').read_text())[name];route='/'+name[:-5]+'/'
    selected=[d for d in designs if gender=='all' or d['gender']==gender]
    hero=next(d for d in designs if d['images'][0]['src']=='/r4.jpeg') if gender=='all' else next(d for d in designs if d['gender']==gender)
    men=[d for d in designs if d['gender']=='men'][1];women=[d for d in designs if d['gender']=='women'][1]
    data=json.dumps({'designs':designs,'defaultGender':gender},ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')
    styles=sorted({s for d in designs for s in d['styles']});occasions=sorted({s for d in designs for s in d['occasions']})
    opts=lambda values:''.join('<option value="'+escape(s,quote=True)+'">'+escape(s.replace('-',' ').title())+'</option>' for s in values)
    header=delivery(re.sub(r'<img\b[^>]*>',reserve_image_space,shared.header(route)),'header')
    values={'header':header,'footer':delivery(shared.footer(),'footer'),'title':escape(title),'page_title':escape(seo['title'],quote=True),'description':escape(seo['description'],quote=True),'route':route,'legacy_redirect':legacy_script(name),'styles':shared.component_css()+'\n'+ICON_CSS+'\n'+(ROOT/'_templates/collections.css').read_text(),'men_card':picture(men['images'][0]),'women_card':picture(women['images'][0]),'hero':picture(hero['images'][0],True),'cards':''.join(card(d) for d in selected[:12]),'styles_options':opts(styles),'occasions_options':opts(occasions),'occasion_links':''.join('<button type="button" data-occasion="'+s+'">'+escape(s.title())+' <span aria-hidden="true">↗</span></button>' for s in occasions),'data':data,'fallback':''.join('<li id="design-'+d['id']+'"><a href="'+d['images'][0]['src']+'">'+escape(d['name'])+' · '+d['id']+'</a></li>' for d in designs),'count':str(len(selected))}
    schema={'@context':'https://schema.org','@type':'CollectionPage','@id':'https://mrsewingfashion.com'+route+'#webpage','url':'https://mrsewingfashion.com'+route,'name':seo['title'],'description':seo['description'],'about':{'@id':'https://mrsewingfashion.com/#organization'},'mainEntity':{'@type':'ItemList','numberOfItems':len(selected),'itemListElement':[{'@type':'ListItem','position':i+1,'name':d['name']+' '+d['id'],'url':'https://mrsewingfashion.com'+route+'?design='+d['id']+'#design-'+d['id']} for i,d in enumerate(selected[:12])]}}
    values['schema']=json.dumps(schema,ensure_ascii=False)
    source=(ROOT/'_templates/collections.html').read_text()
    for key,value in values.items():source=source.replace('{{'+key+'}}',value)
    assert not re.search(r'{{\w+}}',source),'Unexpanded showroom placeholder'
    return '<!-- Generated by scripts/build_collections.py; edit centralized collection data/templates. -->\n'+source

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--check',action='store_true');args=parser.parse_args()
    designs,inventory=load();outputs={ROOT/name:render(name,*config,designs) for name,config in PAGES.items()}
    outputs[ROOT/'assets/collections-navigation.js']='/* Generated from the approved shared menu controller. */\n'+shared.menu_script()+'\nfunction legacyOrderBookmark(){if(location.hash===\"#orderModal\")location.replace(\"/#orderModal\");}\naddEventListener(\"hashchange\",legacyOrderBookmark);legacyOrderBookmark();\n'
    out=io.StringIO();fields=['originalImagePath','sourceOriginal','designId','galleryLocation','groupedWithOtherPhotographs','provenance','rightsStatus','missing','excludedReason','legacyReferences'];writer=csv.DictWriter(out,fields,lineterminator="\n");writer.writeheader()
    for r in inventory['images']:writer.writerow({**r,'legacyReferences':'; '.join(r['legacyReferences'])})
    outputs[ROOT/'docs/collection-image-migration.csv']=out.getvalue()
    records=json.loads((ROOT/'_data/collection-designs.json').read_text())['designs']
    outputs[ROOT/'docs/collection-rights-review.md']='# Collection image rights review\n\nNo publication licence or provenance proof is inferred from repository presence.\nExisting-public photographs are carried into staging pending owner rights review.\nUnreferenced originals are inventoried but excluded from showroom publication.\nNo different photographs have been grouped by visual similarity.\n\n'+f'{len(designs)} existing-public designs; {len(records)} original garment records; {len(inventory["images"])} total image assets inventoried.\n\n| ID | Original | Showroom | Provenance | Rights |\n| --- | --- | --- | --- | --- |\n'+'\n'.join('| '+r['id']+' | `'+r['sourceAnchor']+'` | '+('existing public display preserved' if r['published'] else 'excluded pending review')+' | '+r['provenance']+' | '+r['rightsStatus']+' |' for r in records)+'\n'
    for path,output in outputs.items():
        if args.check:
            if not path.exists() or path.read_text()!=output:raise SystemExit('Stale collection output: '+str(path.relative_to(ROOT)))
        else:path.write_text(output)
    print(f'PASS: {len(designs)} published designs validated; 3 showroom sources and migration/rights reports '+('synchronized.' if args.check else 'generated.'))
if __name__=='__main__':main()
