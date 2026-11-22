"""R61: two published silent suit videos have matching frame posters in generated staging."""
import sys,json,subprocess
from pathlib import Path
R=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(R/'scripts'))
from homepage_video_cards import render
html=render()
assert html.count('<figure')==2 and html.count('<video')==2
assert html.count('data-tailoring-loop muted loop playsinline preload="none"')==2
assert html.count('role="button"')==2 and html.count('tabindex="0"')==2
assert '<figcaption>' not in html and 'data-video-toggle' not in html
assert ' controls ' not in html
for name in ('suit-light','suit-black'):
 clip=R/'assets/videos'/(name+'-silent.mp4')
 poster=R/'assets/videos'/(name+'-poster.jpg')
 assert clip.is_file() and poster.is_file() and clip.stat().st_size>1000 and poster.stat().st_size>1000
 assert '/assets/videos/'+name+'-silent.mp4' in html and '/assets/videos/'+name+'-poster.jpg' in html
 probe=subprocess.run(['ffprobe','-v','error','-show_streams','-of','json',str(clip)],capture_output=True,text=True,check=True)
 streams=json.loads(probe.stdout)['streams']
 assert len([s for s in streams if s.get('codec_type')=='video'])==1
 assert not [s for s in streams if s.get('codec_type')=='audio']
print('PASS: both matching video posters and playable video streams without audio')
