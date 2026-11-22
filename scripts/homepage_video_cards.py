"""R61 owner-authorised suit media, SHA-verified originals, silent clips and matching posters."""
from pathlib import Path
from html import escape
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]
FALLBACK=[('r7.jpeg','Light suit styling reference'),('h2.jpeg','Tailoring styling reference')]
PUBLISHED=[('assets/videos/suit-light-silent.mp4','assets/videos/suit-light-poster.jpg'),('assets/videos/suit-black-silent.mp4','assets/videos/suit-black-poster.jpg')]
def eligible(v):
 if v.get('publicationStatus')!='published':return False
 rights=v.get('usageRights') or {};meta=v.get('metadataApproval') or {}
 if rights.get('approved') is not True or not rights.get('evidenceRef') or not rights.get('date'):return False
 if meta.get('approved') is not True or not meta.get('evidenceRef'):return False
 src=v.get('assetPath');sha=(v.get('technicalReview') or {}).get('sha256')
 if not isinstance(src,str) or not re.fullmatch(r'/[\w.-]+[.]mp4',src):return False
 if not isinstance(sha,str) or not re.fullmatch('[a-f0-9]{64}',sha):return False
 p=ROOT/src.lstrip('/')
 return p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==sha
def render():
 records=json.loads((ROOT/'_data/media-video-records.json').read_text())['videos']
 if len(records)!=2:raise ValueError('Owner review required for changed video count')
 cards=[]
 for record,(fallback,alt),(clip,poster) in zip(records,FALLBACK,PUBLISHED):
  if not (ROOT/fallback).is_file():raise ValueError('Missing reviewed fallback poster')
  if eligible(record):
   derived=(ROOT/clip).is_file() and (ROOT/poster).is_file()
   video_path='/'+clip if derived else record['assetPath']
   poster_path='/'+poster if derived else '/'+fallback
   label=record.get('alternativeText') or alt
   cards.append('<figure class="tailoring-video-card"><video controls muted playsinline preload="none" poster="'+escape(poster_path,quote=True)+'" aria-label="'+escape(label,quote=True)+'"><source src="'+escape(video_path,quote=True)+'" type="video/mp4">Your browser cannot play this video.</video><figcaption>'+escape(record.get('title') or 'Suit design reference')+'</figcaption></figure>')
  else:cards.append('<figure><img src="/'+escape(fallback,quote=True)+'" alt="'+escape(alt,quote=True)+'" loading="lazy" decoding="async"></figure>')
 return ''.join(cards)
