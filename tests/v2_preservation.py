"""Protect approved homepage sections while permitting explicit R22 motion/payment changes."""
from pathlib import Path
import subprocess,re,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'))
def assert_home_protected():
 from build_homepage import SECTIONS,Section
 old=subprocess.check_output(['git','show','9bd678f:index.html'],cwd=ROOT,text=True);current=(ROOT/'index.html').read_text()
 for key,(_,tag,identifier) in SECTIONS.items():
  a=Section(old,tag,identifier);a.feed(old);b=Section(current,tag,identifier);b.feed(current)
  assert a.markup is not None and a.markup==b.markup,('Unexpected homepage section change',key)
 for pattern in [r'<title>.*?</title>',r'<meta name="description"[^>]+>',r'<script type="application/ld\+json">.*?</script>']:
  assert re.findall(pattern,old,re.S)==re.findall(pattern,current,re.S),'Unapproved homepage SEO change'
 old_js=subprocess.check_output(['git','show','9bd678f:assets/homepage.js'],cwd=ROOT,text=True);old_motion=subprocess.check_output(['git','show','9bd678f:_templates/homepage-galleries.js'],cwd=ROOT,text=True)
 new_js=(ROOT/'assets/homepage.js').read_text();new_motion=(ROOT/'_templates/homepage-galleries.js').read_text()
 assert old_js.removesuffix(old_motion)==new_js.removesuffix(new_motion),'Unrelated homepage interaction changed'
if __name__=='__main__':assert_home_protected();print('PASS unchanged approved homepage sections/SEO/non-gallery interactions;R22payment section/motion changes isolated')
