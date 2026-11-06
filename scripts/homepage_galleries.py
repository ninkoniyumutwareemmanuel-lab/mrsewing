"""Homepage projections of the existing publication-gated collection/project loaders."""
from html import escape
import math,re

def collection_items(gender):
 from build_collections import load
 from suit_references import categories,references,model
 designs=load()[0];labels=model()['references'];items=[];seen=set()
 for category in categories():
  if category['gender']!=gender:continue
  for design in references(category,designs):
   for photo in design['images']:
    if photo['src'] in seen:continue
    seen.add(photo['src']);items.append({'id':design['id'],'photo':photo,'caption':labels.get(design['id'],{}).get('label') or design['name'],'category':category['title'],'kind':'design'})
 return items

def project_items():
 from build_journey import projects
 return [{'id':p['slug'],'photo':photo,'caption':p['title'],'category':'Completed Mr Sewing project','kind':'project'} for p in projects() for photo in p['images']]

def gallery(items,name):
 from build_collections import picture
 from build_journey import project_picture
 if not items:return '<p>Approved photographs are being prepared. Explore the page below or discuss your preferences with our team.</p>'
 # Each identical half covers even the narrowest card width across the content shell.
 copies=max(1,math.ceil(1440/(174*len(items))));tiles=items*copies;groups=[]
 for group in range(2):
  cards=[]
  for n,item in enumerate(tiles):
   duplicate=bool(group or n>=len(items));photo=item['photo'];html=picture(photo) if item['kind']=='design' else project_picture(photo,sizes='(max-width:600px) 174px,260px')
   html=re.sub(r'sizes="[^"]*"','sizes="(max-width:600px) 174px,260px"',html)
   cards.append('<figure class="moving-gallery-card" data-photo-source="'+escape(photo['src'],quote=True)+'" data-reference="'+escape(item['id'],quote=True)+'"'+(' aria-hidden="true"' if duplicate else '')+'>'+html+'<figcaption>'+escape(item['caption'])+'</figcaption></figure>')
  groups.append('<div class="moving-gallery-group"'+(' aria-hidden="true"' if group else '')+'>'+''.join(cards)+'</div>')
 return '<div class="moving-gallery" data-moving-gallery aria-label="'+escape(name,quote=True)+'"><div class="moving-gallery-track" style="--gallery-duration:'+str(len(tiles)*12)+'s">'+''.join(groups)+'</div></div>'

def suit_section():
 result='<section id="suit-collections" class="home-section suit-collections"><div class="home-shell"><div class="section-heading centered"><p class="home-eyebrow">Find your inspiration</p><h2>Explore Our <em>Suit Collections</em></h2><p>Discover men\'s and women\'s suit styles and find inspiration for your next outfit.</p></div><button type="button" class="gallery-motion-control" data-gallery-motion aria-pressed="false" hidden>Pause moving galleries</button>'
 for gender,title in [('men',"Men's Suits"),('women',"Women's Suits")]:
  text="Explore men's suits in Kigali, from single-breasted styles to three-piece tailoring and formalwear." if gender=='men' else "Find inspiration for women's suits in Kigali, including tailored trousers, skirt suits and three-piece styles."
  result+='<section class="collection-preview" aria-labelledby="'+gender+'-gallery-heading"><h3 id="'+gender+'-gallery-heading">'+escape(title)+'</h3><p>'+text+'</p>'+gallery(collection_items(gender),title)+'<div class="section-action"><a class="home-button home-button-gold" href="/'+('mensuits' if gender=='men' else 'womensuits')+'/">View All '+escape(title)+'</a></div></section>'
 return result+'</div></section>'
def moments_gallery():
 return gallery(project_items(),'Completed Mr Sewing tailoring projects')+'<div class="section-action"><a class="home-button home-button-gold" href="/our-work/">Explore Our Work</a></div>'
