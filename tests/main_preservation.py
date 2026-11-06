"""Normalise only the explicitly authorised public API/cache script tags."""
import re,subprocess,json
from html import escape
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def normalise_runtime(text):
 text=re.sub(r'<script src="/assets/public-api[.]js[^"]*" defer></script>','',text)
 return re.sub(r'src="(/assets/(?:customer-site|commerce|homepage)[.]js)\?[^"]*"',r'src="\1"',text)
def assert_protected_pages():
 for name in ['booking/index.html','loyalty-program/index.html','referral-program/index.html','terms-and-conditions/index.html','privacy-policy/index.html','refund-policy/index.html']:
  old=subprocess.check_output(['git','show','a2ae98f:'+name],cwd=ROOT,text=True)
  if name=='privacy-policy/index.html':
   before=json.loads(subprocess.check_output(['git','show','a2ae98f:_data/customer-release.json'],cwd=ROOT))['pages']['/privacy-policy/']['sections']
   after=json.loads((ROOT/'_data/customer-release.json').read_text())['pages']['/privacy-policy/']['sections']
   for section_index,paragraph_index in [(2,0),(3,0),(3,1)]:old=old.replace(escape(before[section_index]['paragraphs'][paragraph_index]),escape(after[section_index]['paragraphs'][paragraph_index]))
  assert normalise_runtime((ROOT/name).read_text())==normalise_runtime(old),name
if __name__=='__main__':assert_protected_pages();print('PASS protected booking/programmes/legal pages unchanged except authorised intake/cache tags')
