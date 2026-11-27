"""R61 owner-authorised suit media, SHA-verified originals, silent clips and matching posters."""
from pathlib import Path
from html import escape
import hashlib,json,re,struct
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
def _mp4_handlers(blob):
 """Read actual ISO BMFF track handlers, never infer silence from a filename."""
 handlers=[]
 def boxes(start,end):
  while start<end:
   if end-start<8:raise ValueError('Truncated MP4 box')
   size,kind=struct.unpack_from('>I4s',blob,start);header=8
   if size==1:
    if end-start<16:raise ValueError('Truncated extended MP4 box')
    size=struct.unpack_from('>Q',blob,start+8)[0];header=16
   elif size==0:size=end-start
   if size<header or start+size>end:raise ValueError('Invalid MP4 box')
   yield kind,start+header,start+size
   start+=size
 for kind,a,b in boxes(0,len(blob)):
  if kind!=b'moov':continue
  for kind,a,b in boxes(a,b):
   if kind!=b'trak':continue
   for kind,a,b in boxes(a,b):
    if kind!=b'mdia':continue
    for kind,a,b in boxes(a,b):
     if kind==b'hdlr':
      if b-a<12:raise ValueError('Truncated MP4 handler')
      handlers.append(blob[a+8:a+12])
 return handlers

def verified_playback(record,root=None):
 """Fail closed to approved photographs if playback metadata/assets differ.

 The original upload may retain audio. It is never a playback fallback.
 R61 owner rights remain independent of these technical integrity checks.
 """
 root=Path(root or ROOT).resolve();playback=record.get('playback') or {}
 if playback.get('sourceSha256')!=(record.get('technicalReview') or {}).get('sha256'):return None
 if playback.get('audioStreams')!=0:return None
 paths=[]
 for key,checksum in [('assetPath','sha256'),('posterPath','posterSha256')]:
  path=playback.get(key)
  if not isinstance(path,str) or not path.startswith('/assets/videos/') or '..' in path or '?' in path or '#' in path:return None
  source=(root/path.lstrip('/')).resolve()
  if not source.is_relative_to(root) or not source.is_file():return None
  data=source.read_bytes()
  if hashlib.sha256(data).hexdigest()!=playback.get(checksum):return None
  paths.append((path,data))
 try:
  if _mp4_handlers(paths[0][1])!=[b'vide']:return None
 except (ValueError,struct.error):return None
 if len(paths[0][1])!=playback.get('bytes'):return None
 return paths[0][0],paths[1][0]

def render():
 records=json.loads((ROOT/'_data/media-video-records.json').read_text())['videos']
 if len(records)!=2:raise ValueError('Owner review required for changed video count')
 cards=[]
 for record,(fallback,alt) in zip(records,FALLBACK):
  if not (ROOT/fallback).is_file():raise ValueError('Missing reviewed fallback poster')
  playback=verified_playback(record) if eligible(record) else None
  if playback:
   video_path,poster_path=playback
   label=record.get('alternativeText') or alt
   cards.append('<figure class="tailoring-video-card"><video data-tailoring-loop muted loop playsinline preload="none" tabindex="0" role="button" aria-pressed="false" poster="'+escape(poster_path,quote=True)+'" aria-label="'+escape(label+' video. Tap or press Enter to pause or resume.',quote=True)+'" data-video-title="'+escape(record.get('title') or 'suit video',quote=True)+'"><source src="'+escape(video_path,quote=True)+'" type="video/mp4"></video></figure>')
  else:cards.append('<figure><img src="/'+escape(fallback,quote=True)+'" alt="'+escape(alt,quote=True)+'" loading="lazy" decoding="async"></figure>')
 return ''.join(cards)
