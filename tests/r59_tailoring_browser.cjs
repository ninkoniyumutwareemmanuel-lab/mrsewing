/* R59 staging browser QA: no real customer enquiries or external requests. */
'use strict';
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const base='http://127.0.0.1:8020';
const dest='artifacts/r59-browser';
(async()=>{
 fs.mkdirSync(dest,{recursive:true});
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 try{
  for(const width of [320,390,768,1440]){
   const context=await browser.newContext({viewport:{width,height:900},reducedMotion:'no-preference',hasTouch:width<600,isMobile:width<600});
   await context.route('**/*',route=>new URL(route.request().url()).origin===base?route.continue():route.abort());
   const page=await context.newPage(),errors=[];
   page.on('pageerror',e=>errors.push(e.message));
   const home=await page.goto(base+'/',{waitUntil:'domcontentloaded'});
   assert.equal(home.status(),200);
   assert.equal((await page.locator('h1').innerText()).replace(/\s+/g,' ').trim(),'Professional Tailor in Kigali, Rwanda');
   assert.equal(await page.locator('.tailoring-photo-duo video').count(),2,'two authorized suit videos');
   assert.equal(await page.locator('.tailoring-photo-duo video[muted][controls][playsinline]').count(),2);
   for(const id of ['#tailor-essentials-title','#tailor-process-title','#tailor-benefits-title','#tailor-options-title','#tailor-programs-title','#tailor-final-title'])assert(await page.locator(id).isVisible(),id+' absent');
   assert(await page.locator('#payment-methods h2').isVisible());
   assert.equal(await page.locator('#customer-support form').count(),1);
   assert.equal(await page.locator('.tailoring-primary-card').count(),2);
   assert.equal(await page.locator('[data-moving-gallery]').count(),2);
   const motion=await page.locator('.moving-gallery-track').evaluateAll(x=>x.map(e=>getComputedStyle(e).animationName));
   assert.equal(motion[0],'gallery-drift','first moving row right to left');
   assert.equal(motion[1],'gallery-drift-right','second moving row left to right');
   const control=page.locator('[data-gallery-pause]').first();
   await control.click();
   assert.equal(await page.locator('[data-moving-gallery]').first().getAttribute('data-gallery-paused'),'true');
   assert.equal(await control.getAttribute('aria-pressed'),'true');
   await page.keyboard.press('Escape');
   assert.equal(await page.locator('[data-moving-gallery]').last().getAttribute('data-gallery-paused'),'true');
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'homepage horizontal overflow '+width);
   if(width===390||width===1440){
    await page.screenshot({path:path.join(dest,'homepage-'+width+'.png'),fullPage:true});
   }
   await page.goto(base+'/services/custom-tailoring/',{waitUntil:'domcontentloaded'});
   assert.equal((await page.locator('h1').innerText()).trim(),'Tailoring & Clothing Services');
   const categories=page.locator('.tailoring-hub-category');
   assert.equal(await categories.count(),2,'exactly two current clothing category cards');
   assert((await categories.nth(0).getAttribute('href')).includes('gender=men'));
   assert((await categories.nth(1).getAttribute('href')).includes('gender=women'));
   assert.equal(await page.locator('.tailoring-hub-service').count(),4);
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'hub horizontal overflow '+width);
   if(width===390||width===1440)await page.screenshot({path:path.join(dest,'tailoring-services-'+width+'.png'),fullPage:true});
   await page.goto(base+'/collections/?gender=men',{waitUntil:'domcontentloaded'});
   const available=await page.locator('#showroom-data').evaluate(x=>JSON.parse(x.textContent).designs);
   let expected=available.filter(d=>d.gender==='men');
   await page.waitForFunction(n=>document.querySelector('#gallery-status')?.textContent.startsWith(n+' designs'),expected.length);
   assert.equal(await page.locator('.show-card').count(),Math.min(12,expected.length));
   await page.goto(base+'/collections/?gender=women',{waitUntil:'domcontentloaded'});
   expected=available.filter(d=>d.gender==='women');
   await page.waitForFunction(n=>document.querySelector('#gallery-status')?.textContent.startsWith(n+' designs'),expected.length);
   assert.equal(await page.locator('.show-card').count(),Math.min(12,expected.length));
   await page.goto(base+'/collections/',{waitUntil:'domcontentloaded'});
   await page.waitForFunction(()=>document.querySelector('#gallery-status')?.textContent.includes(' designs'));
   assert.equal((await page.locator('h1').innerText()).trim(),'Showroom — Explore Clothing Designs');
   assert.equal(await page.locator('.show-collection-links a').count(),3);
   await page.goto(base+'/shop/',{waitUntil:'domcontentloaded'});
   assert(await page.locator('#shop-inspiration-title').isVisible());
   assert((await page.locator('.shop-tailoring-inspiration').innerText()).includes('Reference designs are not Shop stock'));
   if(width===390||width===1440)await page.screenshot({path:path.join(dest,'shop-'+width+'.png'),fullPage:true});
   if(width===390){
    await page.goto(base+'/terms-and-conditions/',{waitUntil:'domcontentloaded'});
    assert(await page.locator('#termsPdfDialog').isVisible(),'PDF reader stays present');
    assert.equal(await page.locator('.terms-popup-page').count(),5);
    await page.screenshot({path:path.join(dest,'terms-390.png')});
   }
   assert.deepEqual(errors,[],'Page JavaScript errors at '+width);
   await context.close();
   console.log('PASS R59 local Chromium '+width+'px: homepage, gallery directions/pause, hub, Showroom filters, Shop, '+(width===390?'Terms':'no Terms rerun'));
  }
  const reduced=await browser.newContext({viewport:{width:390,height:844},reducedMotion:'reduce'});
  const page=await reduced.newPage();await page.goto(base+'/',{waitUntil:'domcontentloaded'});
  const styles=await page.locator('.moving-gallery-track').evaluateAll(x=>x.map(e=>getComputedStyle(e).animationName));
  assert(styles.every(x=>x==='none'),'reduced-motion disables both moving galleries');
  await reduced.close();console.log('PASS: reduced-motion static photo fallback');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
