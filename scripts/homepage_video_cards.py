"""R59: neutral video cards with explicit publication, poster and silent-file gates."""
from pathlib import Path
from html import escape
import hashlib,json,re
ROOT=Path(__file__).resolve().parents[1]
FALLBACK=[
 ('r7.jpeg','Tailoring reference photograph featuring a light jacket and navy trousers',2048,2056),
 ('h2.jpeg','Tailoring reference photograph of an off-white outfit',750,938)
]
def permitted(path,sha):
 if not isinstance(path,str) or not path.startswith('/assets/') or '..' in path or '\\' in path or not re.fullmatch('[a-f0-9]{64}',str(sha)):return False
 target=ROOT/path.lstrip('/')
 return target.is_file() and hashlib.sha256(target.read_bytes()).hexdigest()==sha
def eligible(video,inventory):
 if video.get('publicationStatus')!='published':return None
 for name in ('usageRights','metadataApproval'):
  approval=video.get(name) or {}
  if approval.get('approved') is not True or not approval.get('evidenceRef') or not approval.get('date'):return None
 poster=video.get('posterApproval') or {};silent=video.get('silentDerivative') or {}
 if not video.get('posterMediaId') or poster.get('approved') is not True or not poster.get('evidenceRef') or not poster.get('date'):return None
 if silent.get('verifiedNoAudio') is not True or silent.get('publicationApproved') is not True:return None
 if not permitted(poster.get('assetPath'),poster.get('sha256')) or not permitted(silent.get('assetPath'),silent.get('sha256')):return None
 match=next((p for p in inventory['images'] if p.get('originalImagePath')==poster['assetPath'].lstrip('/')),None)
 if not match or match.get('rightsStatus')!='approved' or match.get('missing') is True:return None
 original=video.get('assetPath','')
 expected=(video.get('technicalReview') or {}).get('sha256')
 if not isinstance(original,str) or not original.startswith('/') or '..' in original or not re.fullmatch('[a-f0-9]{64}',str(expected)):return None
 candidate=ROOT/original.lstrip('/')
 if not candidate.is_file() or hashlib.sha256(candidate.read_bytes()).hexdigest()!=expected:return None
 return (silent['assetPath'],poster['assetPath'])
def render():
 records=json.loads((ROOT/'_data/media-video-records.json').read_text())['videos']
 inventory=json.loads((ROOT/'_data/collection-image-inventory.json').read_text())
 if len(records)!=2:raise ValueError('Owner review required for altered R53 video count')
 cards=[]
 for record,(src,alt,width,height) in zip(records,FALLBACK):
  permitted_media=eligible(record,inventory)
  if permitted_media:
   video_path,poster=permitted_media
   label=record.get('alternativeText')
   if not isinstance(label,str) or not label.strip():raise ValueError('Missing approved accessible description')
   cards.append('<figure><video controls muted playsinline preload="none" poster="'+escape(poster,quote=True)+'" aria-label="'+escape(label,quote=True)+'"><source src="'+escape(video_path,quote=True)+'" type="video/mp4">Silent video playback is unavailable in this browser.</video></figure>')
  else:
   cards.append('<figure><img src="'+escape(src,quote=True)+'" alt="'+escape(alt,quote=True)+'" width="'+str(width)+'" height="'+str(height)+'" loading="lazy" decoding="async"></figure>')
 return ''.join(cards)
