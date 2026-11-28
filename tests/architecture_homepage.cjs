/* Phase1 actual-browser contracts. External network and real submissions blocked. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
function library(){for(const name of ['playwright','playwright-core','/workspace/tools/phase1/node_modules/playwright-core']){try{return require(name)}catch(e){if(e.code!=='MODULE_NOT_FOUND')throw e}}throw Error('Install the existing browser test dependency.');}
const {chromium}=library(),ROOT=path.resolve(__dirname,'..'),BASE=(process.env.REVIEW_BASE_URL||'http://127.0.0.1:3170').replace(/\/$/,''),OUT=process.env.REVIEW_ARTIFACTS||'/tmp/mrsewing-architecture-homepage';
const result={layer:'Local Chromium, external traffic blocked, synthetic support-provider responses only',widths:[320,390,768,1440],views:[],checks:[],errors:[],missing:[],axe:[],realSubmissions:false,externalReceipt:'NOT TESTED'};
let browser,page;
(async()=>{fs.mkdirSync(OUT,{recursive:true});browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_BINARY||process.env.CHROMIUM_PATH||(fs.existsSync('/usr/bin/chromium')?'/usr/bin/chromium':undefined),args:['--no-sandbox']});try{
 const ctx=await browser.newContext({reducedMotion:'reduce',viewport:{width:390,height:900}});
 let supportCalls=0,accept=false,supportPayload;
 const handoffs=[];
 await ctx.route('**/*',async route=>{
  const request=route.request(),u=new URL(request.url());
  if(u.hostname==='api.web3forms.com'&&request.method()==='POST'){
   supportCalls++;supportPayload=JSON.parse(request.postData());
   return route.fulfill({status:200,contentType:'application/json',body:JSON.stringify({success:accept})});
  }
  if(u.origin===BASE){if(request.method()!=='GET')throw Error('Unexpected unmocked write request');return route.continue();}
  if(u.origin==='https://wa.me')handoffs.push(u.href);
  return route.abort();
 });
 page=await ctx.newPage();page.on('pageerror',e=>result.errors.push(e.message));
 page.on('response',r=>{if(r.url().startsWith(BASE)&&r.status()>=400)result.missing.push({url:r.url(),status:r.status()})});
 for(const width of result.widths){
  await page.setViewportSize({width,height:900});await page.goto(BASE+'/',{waitUntil:'load'});
  assert.equal(await page.locator('h1').count(),1);assert.equal(await page.locator('h1').innerText(),'Professional Tailoring & Custom-Made Clothing');
  assert.equal(await page.locator('link[rel=canonical]').getAttribute('href'),'https://mrsewingfashion.com/');
  assert.equal(await page.locator('.tailoring-primary-card').count(),4);
  assert.deepEqual(await page.locator('.tailoring-primary-card h3').allTextContents(),['Custom Tailoring','Alterations & Repairs','Garment Care','Garment Repair & Care']);
  const cards=await page.locator('.tailoring-primary-card').evaluateAll(a=>a.map(x=>x.href));
  assert.deepEqual(cards.slice(0,3).map(u=>new URL(u).pathname),['/services/custom-tailoring/','/services/alterations/','/services/garment-care/']);
  for(const href of cards.slice(0,3)){const response=await ctx.request.get(href);assert.equal(response.status(),200);}
  const combined=new URL(cards[3]);assert.equal(combined.origin,BASE);assert.equal(combined.pathname,'/whatsapp/');assert.equal(combined.searchParams.get('text'),'Hello Mr Sewing Fashion, I need both garment repairs and professional cleaning.');
  assert.equal(await page.locator('.home-suits-entry').getAttribute('href'),'/services/custom-tailoring/#tailoring-hub-categories');
  const suitLanding=await ctx.request.get(BASE+'/services/custom-tailoring/');assert((await suitLanding.text()).includes('id="tailoring-hub-categories"'));
  const primary=page.locator('#home-navigation>ul>li');
  assert.equal(await primary.count(),7);assert.deepEqual(await primary.evaluateAll(li=>li.map(x=>x.querySelector(':scope>a,:scope>details>summary').textContent.trim().replace(/\s*⌄$/,''))),['Home','Services','Suits','Showroom','Our Work','About Us','Contact Us']);
  assert.equal(await page.locator('#home-navigation .services-dropdown a').count(),4);
  assert.equal(await page.locator('#site-header a[href^="/shop"],#site-footer a[href^="/shop"]').count(),0);
  assert.equal(await page.locator('#site-footer a[aria-label="youtube" i]').getAttribute('href'),'https://youtube.com/@mr.sewingfashion');
  assert.equal(await page.locator('.tailor-options-grid>a').count(),6);
  for(const name of ['Standard Order','Express Order','VIP Order','On-Site Services','After-Hours Assistance','Collection & Delivery'])assert((await page.locator('.tailor-options-grid').innerText()).includes(name));
  assert.equal(await page.locator('.tailoring-photo-duo figure').count(),2);
  for(const video of await page.locator('.tailoring-photo-duo video').all()){assert(await video.evaluate(v=>v.muted&&v.paused&&v.preload==='none'));assert(await video.getAttribute('aria-label'));}
  assert.equal(await page.locator('[data-moving-gallery]').count(),2);
  assert.equal(await page.locator('.home-work-card').count(),2);assert.equal(await page.locator('#home-work-title').innerText(),'Made by Mr Sewing');
  for(const link of await page.locator('.home-work-card').all()){const href=await link.getAttribute('href');assert(href.startsWith('/our-work/'));assert.equal((await ctx.request.get(BASE+href)).status(),200);assert(await link.locator('img').getAttribute('alt'));}
  const motion=await page.locator('.moving-gallery-track').evaluateAll(tracks=>tracks.map(x=>getComputedStyle(x).animationName));assert(motion.every(x=>x==='none'));
  for(const selector of ['#supportForm','#supportSuccess','#supportStatus','#supportConsent'])assert.equal(await page.locator(selector).count(),1,selector);
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'no overflow '+width);
  if(width<1100){
   const toggle=page.locator('.home-menu-toggle');await toggle.click();assert.equal(await toggle.getAttribute('aria-expanded'),'true');assert(await page.locator('main').evaluate(x=>x.inert));
   if(width===390)await page.screenshot({path:path.join(OUT,'navigation-after-390.png')});
   await page.keyboard.press('Escape');assert.equal(await toggle.getAttribute('aria-expanded'),'false');assert(!(await page.locator('main').evaluate(x=>x.inert)));
  }
  if([390,1440].includes(width)){
   await page.screenshot({path:path.join(OUT,'first-screen-'+width+'.png')});
   await page.locator('#services').screenshot({path:path.join(OUT,'services-'+width+'.png')});
   await page.locator('.tailoring-feature-photo').screenshot({path:path.join(OUT,'feature-'+width+'.png')});
   await page.screenshot({path:path.join(OUT,'homepage-after-'+width+'.png'),fullPage:true});
   let axePath=process.env.AXE_PATH||'/workspace/tools/homepage-qa/node_modules/axe-core/axe.min.js';if(!fs.existsSync(axePath))axePath=require.resolve('axe-core/axe.min.js');await page.addScriptTag({path:axePath});
   const violations=await page.evaluate(async()=>(await axe.run('main',{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}})).violations.map(v=>({id:v.id,impact:v.impact,targets:v.nodes.map(n=>n.target)})));
   result.axe.push({width,scope:'main',violations});assert.deepEqual(violations,[]);
  }
  result.views.push({width,status:'PASS'});
 }
 await page.setViewportSize({width:390,height:900});await page.goto(BASE+'/',{waitUntil:'load'});
 await page.locator('#tailoring-final a[href="/request/?general=1"]').click();await page.locator('#mrCustomerFormPopup').waitFor({state:'visible'});await page.frameLocator('#mrCustomerFormFrame').locator('#customerRequestForm').waitFor({state:'visible'});assert.equal(await page.frameLocator('#mrCustomerFormFrame').locator('#requestConsent').isChecked(),false);
 await page.screenshot({path:path.join(OUT,'homepage-quote-dialog-390.png')});await page.locator('#mrCustomerFormPopup button').first().click();assert(await page.locator('#mrCustomerFormPopup').isHidden());
 result.checks.push({name:'Homepage general quotation opens existing reusable dialog and closes',status:'PASS'});
 await page.locator('.tailoring-primary-card').nth(3).click();
 await page.waitForTimeout(100);assert.equal(handoffs.length,1);assert.equal(new URL(handoffs[0]).searchParams.get('text'),combinedMessage());
 result.checks.push({name:'Combined service deliberately opens one official WhatsApp contact URL; no message sent',status:'PASS'});
 await page.goto(BASE+'/',{waitUntil:'load'});
 await page.locator('#supportName').fill('Synthetic Homepage Test');await page.locator('#supportPhone').fill('+250780000000');await page.locator('#supportMessage').fill('Synthetic non-customer test; do not contact.');
 await page.locator('#supportTopic').selectOption({index:1});await page.locator('#supportForm [type=submit]').click();assert.equal(supportCalls,0,'missing consent never submits');await page.locator('#supportConsent').check();await page.locator('#supportForm [type=submit]').click();await page.locator('#supportStatus').filter({hasText:/could not confirm/i}).waitFor();assert(await page.locator('#supportSuccess').isHidden());assert.equal(await page.locator('#supportName').inputValue(),'Synthetic Homepage Test');
 accept=true;await page.locator('#supportForm [type=submit]').evaluate(b=>{b.click();b.click()});await page.locator('#supportSuccess').waitFor({state:'visible'});assert.equal(supportCalls,2,'failed call plus one successful mocked retry; rapid duplicate prevented');assert.equal(supportPayload['Full Name'],'Synthetic Homepage Test');assert.equal(supportPayload['Terms Consent'],'Agreed');
 result.checks.push({name:'Support validates consent, preserves input on rejection, confirms only mocked positive provider response and prevents duplicate retry',status:'PASS',actualProviderReceipt:'NOT TESTED'});
 await page.emulateMedia({reducedMotion:'no-preference'});await page.goto(BASE+'/',{waitUntil:'load'});
 await page.waitForFunction(()=>document.documentElement.hasAttribute('data-galleries-ready'));
 const names=await page.locator('.moving-gallery-track').evaluateAll(tracks=>tracks.map(x=>getComputedStyle(x).animationName));assert.deepEqual(names,['gallery-drift','gallery-drift-right']);
 const pause=page.locator('[data-gallery-motion-control]').first();await pause.focus();await page.keyboard.press('Tab');await page.keyboard.press('Shift+Tab');await page.keyboard.press('Enter');assert.equal(await page.locator('.moving-gallery-track').first().evaluate(x=>getComputedStyle(x).animationPlayState),'paused');await page.keyboard.press('Escape');assert((await page.locator('.moving-gallery-track').evaluateAll(tracks=>tracks.map(x=>getComputedStyle(x).animationPlayState))).every(x=>x==='paused'));
 result.checks.push({name:'Opposite moving-row directions and accessible pause; DOM order preserved',status:'PASS'});
 assert.deepEqual(result.errors,[]);assert.deepEqual(result.missing,[]);result.status='PASS';
 }catch(e){result.status='FAIL';result.failure={message:e.message,stack:e.stack};if(page)try{await page.screenshot({path:path.join(OUT,'failure.png')})}catch{}process.exitCode=1;}finally{await browser?.close();fs.writeFileSync(path.join(OUT,'results.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));}})();
function combinedMessage(){return 'Hello Mr Sewing Fashion, I need both garment repairs and professional cleaning.';}
