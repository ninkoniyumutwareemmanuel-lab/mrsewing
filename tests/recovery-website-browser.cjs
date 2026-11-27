/* 25Nov recovery: broad local browser sweep. External requests and POSTs blocked. */
'use strict';
const fs=require('node:fs'),assert=require('node:assert/strict'),path=require('node:path');
let pw;for(const name of ['playwright','playwright-core','/workspace/tools/phase1/node_modules/playwright-core']){try{pw=require(name);break;}catch{}}
if(!pw)throw Error('Playwright unavailable');
const BASE=process.env.REVIEW_BASE_URL||'http://127.0.0.1:8020';
const OUT=process.env.RECOVERY_EVIDENCE_DIR||(fs.existsSync('/workspace/recovery')?'/workspace/recovery/2026-11-25':'artifacts/recovery-evidence'),SHOTS=process.env.REVIEW_ARTIFACTS||(fs.existsSync('/workspace/artifacts')?'/workspace/artifacts/recovery-2026-11-25':'artifacts/recovery-browser');
const ROUTES=['/','/about/','/contact/','/services/','/services/custom-tailoring/','/mensuits/','/womensuits/','/collections/','/showroom/?audience=women&service=custom-tailoring','/services/alterations/','/services/garment-care/','/services/mobile-fitting/','/services/vip/','/services/express-tailoring/','/services/wedding-tailoring/','/services/graduation-tailoring/','/our-work/','/guides/fabrics/','/guides/fabrics/super/','/guides/fabrics/linen/','/measurements/','/services/custom-tailoring/special-order/','/services/custom-tailoring/selected-designs/','/services/custom-tailoring/fabric/','/request/','/request/alterations/','/request/garment-care/','/request/mobile-fitting/','/request/vip/','/booking/','/shop/','/shop/sky-blue-elegance-suit/','/customer-information/','/our-process/','/delivery-and-collection/','/refund-policy/','/privacy-policy/','/faq/','/faq/prices-packages-payments/','/faq/cancellations-changes/','/terms-and-conditions/','/terms-and-conditions/current/','/why-choose/','/happy-customers/','/mensuits/single-breasted/','/mensuits/double-breasted/','/mensuits/three-piece/','/mensuits/tuxedos-formalwear/','/mensuits/kaunda/','/womensuits/single-breasted/','/womensuits/double-breasted/','/womensuits/skirt-suits/','/womensuits/three-piece/'];
(async()=>{
 fs.mkdirSync(OUT,{recursive:true});fs.mkdirSync(SHOTS,{recursive:true});
 const result={scope:'Local Chromium, all external interactions blocked; not deployed verification',widths:[320,390,768,1440],pages:[],errors:[],missing:[],violations:[],interactions:{},screenshots:[],externalPosts:0};
 const executable=process.env.CHROMIUM_PATH||(fs.existsSync('/usr/bin/chromium')?'/usr/bin/chromium':undefined);
 const browser=await pw.chromium.launch({executablePath:executable,args:['--no-sandbox']});
 try{
  const context=await browser.newContext({viewport:{width:390,height:900},hasTouch:true,reducedMotion:'reduce'});
  await context.addInitScript(()=>{window.__recoveryOpened=[];window.open=(...args)=>{window.__recoveryOpened.push(args);return null;};});
  await context.route('**/*',route=>{const req=route.request();if(req.method()==='POST'){result.externalPosts++;return route.abort();}return new URL(req.url()).origin===BASE?route.continue():route.abort();});
  const page=await context.newPage();page.on('pageerror',e=>result.errors.push({page:page.url(),error:e.message}));page.on('response',r=>{if(r.url().startsWith(BASE)&&r.status()>=400)result.missing.push({page:page.url(),url:r.url(),status:r.status()});});
  for(const width of result.widths){
   await page.setViewportSize({width,height:900});
   for(const route of ROUTES){
    try{
     const response=await page.goto(BASE+route,{waitUntil:'load',timeout:25000});
     const entry={width,route,final:new URL(page.url()).pathname+new URL(page.url()).search,status:response.status()};
     entry.h1=await page.locator('h1').count();entry.overflow=await page.evaluate(()=>({viewport:innerWidth,width:document.documentElement.scrollWidth}));
     entry.jsRobots=await page.locator('meta[name=robots]').getAttribute('content').catch(()=>null);
     if(entry.status!==200||entry.h1!==1||entry.overflow.width>width+1)entry.issue=true;
     result.pages.push(entry);
     if((width===390||width===1440)&&['/','/services/custom-tailoring/','/guides/fabrics/','/refund-policy/','/terms-and-conditions/','/about/','/collections/'].includes(route)){
      const filename=route==='/'?'home':route.replace(/\W+/g,'-').replace(/^-|-$/g,'');
      await page.locator('main img').evaluateAll(images=>images.forEach(i=>i.loading='eager'));
      await page.evaluate(async()=>Promise.all([...document.images].filter(i=>i.getAttribute('src')).map(i=>i.decode().catch(()=>{}))));
      const dest=path.join(SHOTS,filename+'-'+width+'.png');await page.screenshot({path:dest,fullPage:false});result.screenshots.push(dest);
     }
    }catch(e){result.pages.push({width,route,error:e.message,issue:true});}
   }
  }
  await page.setViewportSize({width:390,height:900});
  await page.goto(BASE+'/showroom/?audience=women&service=custom-tailoring&selectionFlow=synthetic-recovery#designs');
  await page.waitForURL(u=>u.pathname==='/collections/');
  const parsed=new URL(page.url());assert.equal(parsed.searchParams.get('gender'),'women');assert.equal(parsed.searchParams.get('service'),'custom-tailoring');assert.equal(parsed.searchParams.get('selectionFlow'),'synthetic-recovery');assert.equal(parsed.hash,'#designs');
  result.interactions.showroomCompatibility='PASS oldaudience translated; service/selectioncontext/hash preserved';
  const refs=JSON.parse(fs.readFileSync('_data/request-reference-allowlist.json','utf8')),exactPhoto=refs['MS-143'].images[0].url;
  await page.goto(BASE+'/showroom/?'+new URLSearchParams({audience:'women',design:'MS-143',service:'custom-tailoring',photo:exactPhoto})+'#designs');
  await page.waitForURL(u=>u.pathname.startsWith('/collections/designs/'));
  const detailContext=await page.evaluate(()=>mrRequestContext.read());assert.equal(detailContext.design,'MS-143');assert.equal(detailContext.service,'custom-tailoring');assert.equal(detailContext.photo,exactPhoto);assert.equal(new URL(page.url()).hash,'#designs');result.interactions.legacyDesignContext='PASS existingexactdetailredirect preservesvaliddesign/photo/servicecontext; normalpublicURLcleaningretained';
  await page.goto(BASE+'/terms-and-conditions/');const dialog=page.locator('#termsPdfDialog');await dialog.waitFor({state:'visible'});
  const open=page.getByRole('link',{name:'Open the staging-review PDF in a new tab'}),download=page.getByRole('link',{name:'Download the original staging-review PDF'});assert.equal(await open.getAttribute('href'),await download.getAttribute('href'));
  const before=await page.locator('[data-terms-scroll]').evaluate(n=>n.scrollTop);await page.locator('[data-terms-scroll]').evaluate(n=>n.scrollTop=500);assert((await page.locator('[data-terms-scroll]').evaluate(n=>n.scrollTop))>before);
  await Promise.all([page.waitForURL(u=>u.pathname!=='/terms-and-conditions/',{waitUntil:'load'}),page.keyboard.press('Escape')]);assert.equal(await page.locator('#termsPdfDialog:visible').count(),0);result.interactions.termsReader='PASS scrolling/directPDF/downloadidentity/keyboardcloseandnavigation';
  // Scan actual principal content; this records violations without claiming full conformance.
  const axe='/workspace/tools/homepage-qa/node_modules/axe-core/axe.min.js';
  if(fs.existsSync(axe))for(const route of ['/','/services/custom-tailoring/','/guides/fabrics/','/faq/']){
   await page.goto(BASE+route);await page.addScriptTag({path:axe});const violations=await page.evaluate(async()=>(await axe.run(document.querySelector('main')||document.body,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})).violations.map(v=>({id:v.id,impact:v.impact,targets:v.nodes.map(n=>n.target)})));result.violations.push({route,violations});
  }
  assert.equal(result.externalPosts,0,'No real requests submitted');
 }catch(error){result.interactionError=error.message;throw error;}finally{await browser.close();result.status=result.pages.some(p=>p.issue)||result.errors.length||result.missing.length||result.interactionError||result.violations.some(v=>v.violations.length)?'FAIL':'PASS';fs.writeFileSync(OUT+'/technical-browser.json',JSON.stringify(result,null,2)+'\n');}
 const summary={status:result.status,visits:result.pages.length,issues:result.pages.filter(p=>p.issue),jsErrors:result.errors,missing:result.missing,axe:result.violations,interactions:result.interactions,screenshots:result.screenshots.length};
 console.log(JSON.stringify(summary,null,2));if(result.status!=='PASS')process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1;});
