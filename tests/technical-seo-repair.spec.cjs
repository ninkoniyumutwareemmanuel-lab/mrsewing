/* R47: local mobile/desktop rendering and synthetic-host indexing boundaries.
   No production response or Googlebot indexing claim; no real submissions. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const root=path.resolve(__dirname,'..'),base=process.env.REVIEW_BASE_URL||'http://127.0.0.1:8020';
const routes=['/','/services/custom-tailoring/','/services/alterations/','/services/garment-care/','/services/mobile-fitting/','/services/vip/','/mensuits/','/womensuits/'];
const widths=[320,390,768,1440],out='/workspace/review/technical-seo-2026-11-13';
(async()=>{
 fs.mkdirSync(out,{recursive:true});
 const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});
 const report={scope:'Local generated HTML and synthetic hostname behavior only; live response headers/production rendering are separate evidence.',widths,pages:[],errors:[],missing:[],axe:[],nativeExternalInteractions:false};
 try{
  const context=await browser.newContext({viewport:{width:390,height:900},reducedMotion:'reduce'});
  await context.route('**/*',r=>new URL(r.request().url()).origin===new URL(base).origin?r.continue():r.abort());
  const page=await context.newPage();
  page.on('pageerror',e=>report.errors.push(e.message));
  page.on('response',r=>{if(r.url().startsWith(base)&&r.status()>=400)report.missing.push({url:r.url(),status:r.status()});});
  for(const width of widths){
   await page.setViewportSize({width,height:900});
   for(const route of routes){
    const response=await page.goto(base+route,{waitUntil:'domcontentloaded'});assert.equal(response.status(),200,route);
    assert.equal(await page.locator('h1').count(),1,route+' unique H1');
    assert.equal(await page.locator('meta[name="robots"]').getAttribute('content'),'index, follow',route+' localhost source directive');
    assert.equal(await page.locator('link[rel="canonical"]').getAttribute('href'),'https://mrsewingfashion.com'+route);
    assert(await page.locator('main').innerText().then(s=>s.trim().length>=150),route+' visible main information');
    assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),route+' horizontal overflow at'+width);
    await page.locator('img').evaluateAll(async ns=>{for(const image of ns){image.loading='eager';await image.decode().catch(()=>{});}});
    const broken=await page.locator('img').evaluateAll(ns=>ns.filter(n=>!n.complete||n.naturalWidth===0).map(n=>n.getAttribute('src')));assert.deepEqual(broken,[],route+' image decoding');
    const scripts=await page.locator('script[type="application/ld+json"]').allTextContents();for(const script of scripts)JSON.parse(script);
    const links=await page.locator('a[href]').evaluateAll(ns=>ns.map(n=>({text:n.textContent.trim(),href:n.getAttribute('href')})));
    assert(links.some(a=>a.href==='/services/custom-tailoring/'),route+' ordinary header/footer custom-tailoring link');
    if(width<768){const toggle=page.locator('.home-menu-toggle');if(await toggle.isVisible()){await toggle.click();assert.equal(await toggle.getAttribute('aria-expanded'),'true');const nav=page.locator('#home-navigation');assert(await nav.isVisible());await toggle.click();assert.equal(await toggle.getAttribute('aria-expanded'),'false');}}
    report.pages.push({route,width,status:response.status(),imagesDecoded:await page.locator('img').count(),schemas:scripts.length,canonical:'https://mrsewingfashion.com'+route});
   }
   console.log('PASS priority8 mobile/desktop SEO rendering width'+width);
  }
  // Local favicon retrieval; browsers can request the conventional root resource.
  const icon=await context.request.get(base+'/favicon.ico');assert.equal(icon.status(),200);const bytes=await icon.body();assert.equal(bytes.readUInt16LE(0),0);assert.equal(bytes.readUInt16LE(2),1);report.favicon={localStatus:icon.status(),bytes:bytes.length};
  report.notFound=[];
  for(const width of widths){
   await page.setViewportSize({width,height:900});await page.goto(base+'/404.html');assert.equal(await page.locator('meta[name=robots]').getAttribute('content'),'noindex, follow');assert.equal(await page.locator('h1').innerText(),'Page not found');assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
   for(const link of await page.locator('main nav a').all()){const rect=await link.boundingBox();assert(rect.height>=44&&rect.width>=44);}
   const links=await page.locator('main nav a').evaluateAll(ns=>ns.map(n=>n.getAttribute('href')));assert.deepEqual(links,['/','/services/']);report.notFound.push({width,templateNoindex:true,navigation:links});
  }
  const unknown=await context.request.get(base+'/r47-nonexistent-resource-checked');assert.equal(unknown.status(),404);report.localUnknownStatus=unknown.status();
  // The static server does not implement Cloudflare routing; separate Wrangler
  // or deployed HTTP evidence must establish the actual custom404 status/body.

  // Exercise actual existing noindex script against generated HTML in a synthetic
  // pages.dev document. This is explicitly not an HTTP header/origin verification.
  const staging=await browser.newContext({viewport:{width:390,height:900},reducedMotion:'reduce'});
  try{
   const fake='https://r47-audit.mrsewing-staging.pages.dev';
   await staging.route('**/*',async r=>{const u=new URL(r.request().url());if(u.origin!==fake)return r.abort();const local=await context.request.get(base+u.pathname+u.search);await r.fulfill({status:local.status(),headers:{'content-type':local.headers()['content-type']||'text/plain'},body:await local.body()});});
   const staged=await staging.newPage();report.syntheticStagingNoindex=[];
   for(const route of routes){await staged.goto(fake+route,{waitUntil:'domcontentloaded'});assert.equal(await staged.locator('meta[name="robots"]').getAttribute('content'),'noindex, nofollow');report.syntheticStagingNoindex.push(route);}
  }finally{await staging.close();}
  // Representative main-content checks; existing continuous OFFER motion is
  // suppressed by reduced-motion, without making a full WCAG claim.
  const axePath='/workspace/tools/homepage-qa/node_modules/axe-core/axe.min.js';
  if(fs.existsSync(axePath))for(const route of['/services/custom-tailoring/','/services/alterations/','/404.html']){
   await page.setViewportSize({width:390,height:900});await page.goto(base+route);await page.addScriptTag({path:axePath});
   const violations=await page.evaluate(async()=>(await axe.run(document.querySelector('main'),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})).violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>n.target)})));
   assert.deepEqual(violations,[],route+' scoped axe main content');report.axe.push({route,violations});
  }
  // Capture representative fully decoded mobile and desktop views.
  for(const width of[390,1440]){await page.setViewportSize({width,height:900});await page.goto(base+'/services/custom-tailoring/');await page.locator('img').evaluateAll(async ns=>{for(const n of ns){n.loading='eager';await n.decode().catch(()=>{});}});await page.screenshot({path:out+'/custom-tailoring-'+width+'.png',fullPage:true});}
  assert.deepEqual(report.errors,[]);assert.deepEqual(report.missing,[]);fs.writeFileSync(out+'/browser.json',JSON.stringify(report,null,2)+'\n');console.log('PASS priority8×4widths/initial+renderedcontent/resources/canonical/schema/headernavigation/localfavicon/syntheticstagingnoindex/scopedaxe; no production or indexing claim');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
