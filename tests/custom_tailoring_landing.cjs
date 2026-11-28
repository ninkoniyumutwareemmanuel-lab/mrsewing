/* S01 CTA -> existing Special form, real server validator, mocked provider only. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const {chromium}=(()=>{for(const name of ['playwright','playwright-core','/workspace/tools/phase1/node_modules/playwright-core'])try{return require(name)}catch(e){if(e.code!=='MODULE_NOT_FOUND')throw e}throw Error('Playwright unavailable')})();
const ROOT=path.resolve(__dirname,'..'),BASE=process.env.REVIEW_BASE_URL||'http://127.0.0.1:8020',OUT=process.env.REVIEW_ARTIFACTS||path.join(ROOT,'artifacts/custom-tailoring');
const NOW=Date.parse('2026-11-28T10:00:00Z');
const result={layer:'Local Chromium; actual Special form and server validator with mocked provider',views:[],checks:[],errors:[],missing:[],realProviderReceipt:'NOT TESTED',realSubmissions:false};
let browser,page,accept=false,calls=0,payload,forwarded;
(async()=>{fs.mkdirSync(OUT,{recursive:true});try{
 const {handleSelected}=await import(ROOT+'/functions/_lib/selected-design-handler.js');
 browser=await chromium.launch({executablePath:process.env.CHROMIUM_BINARY||(fs.existsSync('/usr/bin/chromium')?'/usr/bin/chromium':undefined),args:['--no-sandbox']});
 const ctx=await browser.newContext({viewport:{width:390,height:900},reducedMotion:'reduce'});
 await ctx.addInitScript(now=>{const Real=Date;window.Date=class extends Real{constructor(...a){super(...(a.length?a:[now]))}static now(){return now}};window.__accepted=[];window.addEventListener('mrsewing:enquiry-accepted',e=>window.__accepted.push(e.detail));},NOW);
 await ctx.route('**/*',async route=>{const req=route.request(),u=new URL(req.url());if(u.origin!==BASE)return route.abort();if(u.pathname==='/api/selected-design-request'){
   payload=JSON.parse(req.postData());const r=await handleSelected(new Request(req.url(),{method:'POST',headers:{'Content-Type':'application/json',Origin:BASE},body:req.postData()}),'synthetic-only',async(_u,options)=>{calls++;forwarded=JSON.parse(options.body);return new Response(JSON.stringify({success:accept}),{status:200})},NOW);
   return route.fulfill({status:r.status,headers:Object.fromEntries(r.headers),body:await r.text()});
 }assert.equal(req.method(),'GET','No real submission may escape the mock');return route.continue()});
 page=await ctx.newPage();page.on('pageerror',e=>result.errors.push(e.message));page.on('response',r=>{if(r.url().startsWith(BASE)&&r.status()>=400&&!r.url().includes('/api/'))result.missing.push({url:r.url(),status:r.status()})});
 for(const width of [320,390,768,1440]){
   await page.setViewportSize({width,height:900});const r=await page.goto(BASE+'/services/custom-tailoring/',{waitUntil:'load'});assert.equal(r.status(),200);
   assert.equal(await page.locator('h1').innerText(),'Custom Tailoring & Clothing Services');assert.equal(await page.locator('.s01-steps li').count(),4);assert.equal(await page.locator('.tailoring-hub-category').count(),2);
   assert.deepEqual(await page.locator('.tailoring-hub-category').evaluateAll(a=>a.map(x=>x.getAttribute('href'))),['/mensuits/','/womensuits/']);
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));result.views.push({width,status:'PASS'});
 }
 await page.setViewportSize({width:390,height:900});const trigger=page.locator('.service-hero-actions a').first();await trigger.click();await page.locator('#mrCustomerFormPopup').waitFor({state:'visible'});
 const f=page.frameLocator('#mrCustomerFormFrame');await f.locator('#customerRequestForm').waitFor();assert.equal(await f.locator('#customerRequestForm').getAttribute('data-special'),'true');assert.equal(await f.locator('#requestConsent').isChecked(),false);
 await f.locator('#reviewRequest').click();assert.equal(calls,0,'empty form never submits');assert(await f.locator('#requestReview').isHidden());
 await f.locator('#requestGarment').selectOption('other');assert(await f.locator('#requestOtherGarment').isVisible());await f.locator('#requestOtherGarment').fill('Synthetic garment for assessment');await f.locator('#requestGarment').selectOption('shirt');assert(await f.locator('#requestOtherGarment').isHidden());
 await f.locator('#requestQuantity').fill('2');await f.locator('#requestDesignDescription').fill('Synthetic plain shirt request; not a real customer order.');
 const choices=await f.locator('#requestFabricChoice option').evaluateAll(a=>a.map(x=>({value:x.value,text:x.textContent})));const own=choices.find(x=>/own/i.test(x.text));assert(own);await f.locator('#requestFabricChoice').selectOption(own.value);assert(await f.locator('#requestFabricSelection').isHidden());
 for(const[id,value]of Object.entries({requestName:'Synthetic S01 Test',requestPhone:'+250780000000',requestCountry:'Rwanda',requestCity:'Kigali',requestEmail:'synthetic@example.invalid',requestDate:'2026-12-15',requestCompletionTime:'12:00'}))await f.locator('#'+id).fill(value);
 await f.locator('#requestMeasurementMethod').selectOption('online');await f.locator('#requestDeliveryMethod').selectOption('collection');await f.locator('#requestCollectionLocation').selectOption('workshop');
 await f.locator('#requestConsent').check();await page.locator('.mr-customer-popup-close').click();assert(await page.locator('#mrCustomerFormPopup').isHidden());assert(await trigger.evaluate(x=>x===document.activeElement));
 await trigger.click();await f.locator('#requestName').waitFor();assert.equal(await f.locator('#requestName').inputValue(),'Synthetic S01 Test','existing draft restored');
 // Consent is an explicit current action, never inferred from draft storage.
 if(!await f.locator('#requestConsent').isChecked())await f.locator('#requestConsent').check();
 await f.locator('#reviewRequest').click();await f.locator('#requestReview').waitFor({state:'visible'});await page.screenshot({path:path.join(OUT,'special-review-390.png')});
 await f.locator('#sendRequest').click();await f.locator('#requestStatus').filter({hasText:/could not confirm|did not confirm/i}).waitFor();assert(await f.locator('#requestSuccess').isHidden());assert.equal(await f.locator('#requestName').inputValue(),'Synthetic S01 Test');assert.equal(await page.evaluate(()=>__accepted.length),0);
 accept=true;await f.locator('#sendRequest').evaluate(b=>{b.click();b.click()});await f.locator('#requestSuccess').waitFor({state:'visible'});assert.equal(calls,2,'failed attempt plus one accepted retry; no double submit');assert.equal(payload.quotationDetails.mode,'special');assert.equal(forwarded['Garment Type'],'Shirt');assert.equal(forwarded['Total Garments'],'2');assert.equal(forwarded['Selected Design Count'],'0');assert.equal(forwarded['Full Name'],'Synthetic S01 Test');assert.equal(await page.evaluate(()=>__accepted.length),1,'exactly one accepted signal');
 assert(!/inbox receipt|order confirmed|appointment confirmed/i.test(await f.locator('#requestSuccess').innerText()));
 result.checks.push({name:'S01 CTA, original Special conditional fields, draft close/reopen, consent/review, real validator failure/retry and duplicate prevention',status:'PASS'});
 assert.deepEqual(result.errors,[]);assert.deepEqual(result.missing,[]);result.status='PASS';
 }catch(e){result.status='FAIL';result.failure={message:e.message,stack:e.stack};if(page)try{await page.screenshot({path:path.join(OUT,'failure.png')})}catch{}process.exitCode=1}finally{await browser?.close();fs.writeFileSync(path.join(OUT,'results.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2))}})();
