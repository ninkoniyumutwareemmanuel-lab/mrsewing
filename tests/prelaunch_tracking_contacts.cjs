/* Pre-launch contact and attribution contracts. Synthetic DOM only; no network,
 * customer records, Meta event delivery or external-account claims. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict'),{execFileSync}=require('node:child_process');
const ROOT=path.resolve(__dirname,'..');
const OUT=process.env.REVIEW_ARTIFACTS||'/tmp/mrsewing-prelaunch-tracking';
const business=JSON.parse(fs.readFileSync(path.join(ROOT,'_data/business.json'))),officialPhone=business.telephone.replace(/\D/g,''),officialEmail=business.email.toLowerCase();
const result={scope:'Generated HTML plus synthetic DOM/VM. No third-party requests, messages or receipt claims.',checks:[],issues:[],realMessages:false,realEvents:false};
fs.mkdirSync(OUT,{recursive:true});
function checked(name,fn){try{const detail=fn();result.checks.push({name,status:'PASS',detail});}catch(error){result.checks.push({name,status:'FAIL',error:error.message});process.exitCode=1;}}
checked('All generated contact destinations match approved business configuration',()=>{
 const python=String.raw`from pathlib import Path
from html.parser import HTMLParser
import json
root=Path('.')
skip={'_templates','docs','tests','artifacts','node_modules','.git','.wrangler','.github'}
class Parser(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.links=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag=='a' and a.get('href'):self.links.append(a['href'])
rows=[];pages=0
for p in root.rglob('*.html'):
 if any(part in skip for part in p.relative_to(root).parts):continue
 pages+=1;doc=Parser();doc.feed(p.read_text())
 rows.extend({'file':str(p),'href':href} for href in doc.links)
print(json.dumps({'pages':pages,'links':rows}))`;
 const data=JSON.parse(execFileSync('python3',['-c',python],{cwd:ROOT,encoding:'utf8'}));
 const counts={telephone:0,email:0,whatsappHelper:0,whatsappDirect:0};
 for(const row of data.links){const u=new URL(row.href,'https://mrsewingfashion.com');
  if(u.protocol==='tel:'){assert.equal(decodeURIComponent(u.pathname).replace(/\D/g,''),officialPhone,row.file);counts.telephone++;}
  if(u.protocol==='mailto:'){assert.equal(decodeURIComponent(u.pathname).toLowerCase(),officialEmail,row.file);counts.email++;}
  if(u.hostname==='wa.me'){assert.equal(u.pathname.replace(/\D/g,''),officialPhone,row.file);counts.whatsappDirect++;}
  if(['api.whatsapp.com','web.whatsapp.com'].includes(u.hostname)){assert.equal((u.searchParams.get('phone')||'').replace(/\D/g,''),officialPhone,row.file);counts.whatsappDirect++;}
  if(u.hostname==='mrsewingfashion.com'&&u.pathname.replace(/\/+$/,'')==='/whatsapp'){counts.whatsappHelper++;}
 }
 assert(data.pages>=300);assert(counts.telephone&&counts.email&&counts.whatsappHelper);return{pages:data.pages,counts};
});
function handoff(raw,{host='mrsewingfashion.com',target='',modifier=false}={}){
 const callbacks={},opened=[],assigned=[];const location={origin:'https://'+host,href:'https://'+host+'/services/alterations/',pathname:'/services/alterations/',assign:url=>assigned.push(url),replace:url=>assigned.push(url)};
 const window={location,open:url=>opened.push(url)},document={addEventListener:(kind,fn)=>callbacks[kind]=fn};
 vm.runInNewContext(fs.readFileSync(path.join(ROOT,'_templates/whatsapp-consent.js'),'utf8'),{document,window,location,URL});
 const link={href:new URL(raw,location.href).href,target,getAttribute:()=>null};let prevented=false;
 callbacks.click({target:{closest:()=>link},ctrlKey:modifier,metaKey:false,shiftKey:false,preventDefault(){prevented=true},stopImmediatePropagation(){}});
 return{opened,assigned,prevented};
}
checked('WhatsApp helper preserves exact prepared message with manual handoff only',()=>{
 const message="Hello Mr Sewing Fashion. Design: Navy & Ivory — 50% reference.\nPlease assess the quotation.";
 for(const host of ['mrsewingfashion.com','mrsewing-staging.pages.dev'])for(const target of ['','_blank']){
  const out=handoff('/whatsapp/?text='+encodeURIComponent(message),{host,target});assert(out.prevented);assert.equal(out.opened.length+out.assigned.length,1);const u=new URL(out.opened[0]||out.assigned[0]);assert.equal(u.hostname,'wa.me');assert.equal(u.pathname,'/'+officialPhone);assert.equal(u.searchParams.get('text'),message);
 }
 for(const raw of ['https://wa.me/250000000000?text=test','https://wa.me.evil.invalid/'+officialPhone]){const out=handoff(raw);assert.equal(out.prevented,false);assert.equal(out.opened.length+out.assigned.length,0);}
 return{officialConfigurationUsed:true,desktopMobileHelperEncoding:true,manualSendRequired:true};
});
function contextScenario(start,href){
 const storage=new Map(),events={},replacements=[];const u=new URL(start),location={origin:u.origin,pathname:u.pathname,search:u.search,href:u.href,hash:u.hash};
 const document={getElementById:()=>null,querySelector:()=>null,addEventListener(k,fn){(events[k]||=[]).push(fn);}},history={replaceState(_s,_t,url){replacements.push(url);}};
 const window={};vm.runInNewContext(fs.readFileSync(path.join(ROOT,'assets/request-context.js'),'utf8'),{window,document,location,history,URL,URLSearchParams,sessionStorage:{getItem:k=>storage.get(k)??null,setItem:(k,v)=>storage.set(k,v),removeItem:k=>storage.delete(k)}});
 const link={href:new URL(href,location.href).href,hasAttribute:()=>false,classList:{contains:()=>false}};
 for(const fn of events.click||[])fn({target:{closest:()=>link}});
 return{href:link.href,stored:[...storage.values()].join('\n'),replacements};
}
checked('Explicit campaign link query survives context decoration; private input is not invented',()=>{
 const out=contextScenario('https://mrsewingfashion.com/collections/?utm_source=facebook','/mensuits/?utm_source=facebook&utm_medium=paid_social&utm_campaign=synthetic-launch&fbclid=synthetic-click');
 const u=new URL(out.href,'https://mrsewingfashion.com');assert.equal(u.searchParams.get('utm_source'),'facebook');assert.equal(u.searchParams.get('utm_campaign'),'synthetic-launch');assert.equal(u.searchParams.get('fbclid'),'synthetic-click');assert(!/Full Name|Phone Number|Email Address/.test(out.stored));return{explicitCampaignQueryPreserved:true};
});
checked('Attribution persistence limitation is verified rather than claimed implemented',()=>{
 const out=contextScenario('https://mrsewingfashion.com/collections/?utm_source=facebook&utm_campaign=synthetic-launch','/mensuits/');const u=new URL(out.href,'https://mrsewingfashion.com');assert.equal(u.searchParams.has('utm_source'),false);assert(!out.stored.includes('utm_source'));result.issues.push({id:'TRACK-P1-01',priority:'P1',scope:'Campaign attribution/measurement readiness',finding:'No first-party campaign attribution is persisted across ordinary clean internal links; current Meta suppresses every queried landing URL, including UTM/fbclid. This is a measurement limitation, not evidence that customer enquiries fail.',requiredDecision:'Owner acceptance for click/manual-enquiry campaigns, or separately reviewed safe attribution design. Do not weaken query/privacy suppression or add conversion events silently.'});return{limitationConfirmed:true};
});
checked('Current Meta privacy regression remains green, including no conversion events',()=>execFileSync(process.execPath,['tests/analytics_privacy.cjs'],{cwd:ROOT,encoding:'utf8'}).trim());
const meta=JSON.parse(fs.readFileSync(path.join(ROOT,'_data/meta-pixel.json'))),pixel=fs.readFileSync(path.join(ROOT,'assets/meta-pixel.js'),'utf8');
checked('Meta is PageView-only with deliberate fail-closed campaign-query behavior',()=>{
 assert(meta.productionEnabled&&meta.status==='owner-approved-production');assert(/^\d+$/.test(meta.pixelId));assert(pixel.includes('&& !location.search'));assert.equal((pixel.match(/fbq\("init"/g)||[]).length,1);assert.equal((pixel.match(/fbq\("track", "PageView"/g)||[]).length,1);assert(!/fbq\(["']track["'],\s*["'](?:Lead|Purchase|ViewContent)/.test(pixel));return{configuredPixelPresent:true,configuredIdentifierNotRepeatedInReport:true,onlyPageViewInstalled:true,querySuppressionVerified:true,actualReceipt:'BLOCKED: no Events Manager access'};
});
result.status=result.checks.some(x=>x.status==='FAIL')?'FAIL':'PASS';
fs.writeFileSync(path.join(OUT,'tracking-contact-tests.json'),JSON.stringify(result,null,2)+'\n');console.log(JSON.stringify(result,null,2));
