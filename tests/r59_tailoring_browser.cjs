/* R59 staging browser QA: no real customer enquiries or external requests. */
'use strict';
const {chromium}=(()=>{try{return require('playwright');}catch(e){if(e.code!=='MODULE_NOT_FOUND')throw e;return require('playwright-core');}})();
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const base='http://127.0.0.1:8020';
const dest='artifacts/r59-browser';
(async()=>{
 fs.mkdirSync(dest,{recursive:true});
 const browser=await chromium.launch({headless:true,...(process.env.CHROMIUM_BINARY?{executablePath:process.env.CHROMIUM_BINARY}:{}),args:['--no-sandbox']});
 try{
  for(const width of [320,390,768,1440]){
   const context=await browser.newContext({viewport:{width,height:900},reducedMotion:'no-preference',hasTouch:width<600,isMobile:width<600});
   await context.route('**/*',route=>new URL(route.request().url()).origin===base?route.continue():route.abort());
   const page=await context.newPage(),errors=[];
   page.on('pageerror',e=>errors.push(e.message));
   const home=await page.goto(base+'/',{waitUntil:'domcontentloaded'});
   assert.equal(home.status(),200);
   assert.equal((await page.locator('h1').innerText()).replace(/\s+/g,' ').trim(),'Professional Tailoring & Custom-Made Clothing');
   assert.equal(await page.locator('.tailoring-photo-duo video').count(),2,'two authorized suit videos');
   assert.equal(await page.locator('.tailoring-photo-duo video[muted][loop][playsinline]').count(),2);
   assert.equal(await page.locator('.tailoring-photo-duo [data-video-toggle]').count(),0,'no video pause buttons');
   assert.equal(await page.locator('.tailoring-photo-duo figcaption').count(),0,'no video captions visible');
   assert.equal(await page.locator('.tailoring-photo-duo video[controls]').count(),0,'no native video controls');
   assert.equal(await page.locator('.tailoring-photo-duo video[role="button"][tabindex="0"]').count(),2,'videos remain tap/keyboard controllable');

   if(width===390){
     const quoteLink=page.locator('#tailoring-final a[href^="/request/"]').first();
     assert.equal(await quoteLink.count(),1,'quotation CTA remains on homepage');
     await quoteLink.click();
     const modal=page.locator('#mrCustomerFormPopup');
     await modal.waitFor({state:'visible'});
     const quote=page.frameLocator('#mrCustomerFormFrame');
     await quote.locator('form#customerRequestForm').waitFor();
     assert.equal(await quote.locator('form#customerRequestForm').getAttribute('data-kind'),'quotation','existing quotation form loaded');
     assert.equal(await quote.locator('#site-header').evaluate(el=>getComputedStyle(el).display),'none','no inner page header');
     assert.equal(await quote.locator('footer').first().evaluate(el=>getComputedStyle(el).display),'none','no inner footer');
     assert(await quote.locator('#requestReview').count()===1,'existing review step preserved');
     assert(await quote.locator('#requestConsent').count()===1,'existing consent preserved');
     await page.screenshot({path:path.join(dest,'quotation-popup-390.png')});
     await page.locator('.mr-customer-popup-close').click();
     assert.equal(await modal.isVisible(),false,'quotation popup closed');
     await page.goto(base+'/contact/',{waitUntil:'domcontentloaded'});
     await page.getByRole('link',{name:/Book a Consultation/}).click();
     const consultationPopup=page.locator('#mrCustomerFormPopup');
     await consultationPopup.waitFor({state:'visible'});
     const consult=page.frameLocator('#mrCustomerFormFrame');
     await consult.locator('form#customerRequestForm').waitFor();
     assert.equal(await consult.locator('form#customerRequestForm').getAttribute('data-kind'),'consultation');
     assert.equal(await consult.locator('#site-header').evaluate(el=>getComputedStyle(el).display),'none','no consultation header');
     assert.equal(await consult.locator('footer').first().evaluate(el=>getComputedStyle(el).display),'none','no consultation footer');
     assert(await consult.locator('#consultationMethod').count()===1,'existing visit/phone methods intact');
     assert(await consult.locator('#requestDate').count()===1,'existing date selection intact');
     assert(await consult.locator('#requestTime').count()===1,'existing time selection intact');
     await page.screenshot({path:path.join(dest,'consultation-popup-390.png')});
     await page.locator('.mr-customer-popup-close').click();
     // Return to the homepage before the existing gallery and layout assertions.
     await page.goto(base+'/',{waitUntil:'domcontentloaded'});
   }
   assert.equal(await page.locator('#home-navigation > ul > li.services-dropdown').count(),0,'redundant Services item fully removed');
   assert.equal(await page.locator('.tailoring-primary-card[href="/services/custom-tailoring/"]').count(),1,'Tailoring & Clothing Services remains available from home');
   assert.equal(await page.locator('.homepage-header .header-shop').innerText(),'Shop');
   assert.equal(await page.locator('.homepage-header .header-shop').getAttribute('href'),'/shop/');
   assert.equal(await page.locator('.homepage-footer a[href="/terms-and-conditions/"]').count(),1);
   assert.equal(await page.locator('.footer-bottom a[href="/terms-and-conditions/"]').count(),0,'no extra Terms after copyright');
   const videoGridColumns=await page.locator('.tailoring-photo-duo').evaluate(el=>getComputedStyle(el).gridTemplateColumns.split(' ').filter(Boolean).length);
   assert.equal(videoGridColumns,width<=760?1:2,'video grid width '+width);
   for(const id of ['#tailor-essentials-title','#tailor-process-title','#tailor-benefits-title','#tailor-options-title','#tailor-programs-title','#tailor-final-title'])assert(await page.locator(id).isVisible(),id+' absent');
   assert(await page.locator('#payment-methods h2').isVisible());
   assert.equal(await page.locator('#customer-support form').count(),1);
   assert.equal(await page.locator('.tailoring-primary-card').count(),2);
   assert.equal(await page.locator('[data-moving-gallery]').count(),2);
   const motion=await page.locator('.moving-gallery-track').evaluateAll(x=>x.map(e=>getComputedStyle(e).animationName));
   assert.equal(motion[0],'gallery-drift','first moving row right to left');
   assert.equal(motion[1],'gallery-drift-right','second moving row left to right');
   assert.equal(await page.locator('[data-gallery-pause]').count(),0,'gallery pause buttons removed');
   assert.equal(await page.locator('.gallery-motion-note').count(),0,'technical motion instructions removed');
   const gallery=page.locator('[data-moving-gallery]').first();
   await gallery.click();
   assert.equal(await gallery.getAttribute('data-gallery-paused'),'true','tap pauses gallery');
   assert.equal(await gallery.getAttribute('aria-pressed'),'true','accessible gallery state');
   await gallery.focus();
   await page.keyboard.press('Enter');
   assert.equal(await gallery.getAttribute('data-gallery-paused'),'false','keyboard resumes gallery');
   await page.keyboard.press('Escape');
   assert.equal(await page.locator('[data-moving-gallery]').last().getAttribute('data-gallery-paused'),'true','Escape pauses both galleries');
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
   assert.equal(await page.locator('.tailoring-hub-fact').count(),4,'four customer policy facts');
   assert.equal(await page.locator('.tailoring-hub-steps li').count(),4,'four actual customer journey steps');
   assert.equal(await page.locator('.tailoring-hub-fabric-card').count(),2,'fabric supplied by us or customer');
   assert.equal(await page.locator('.tailoring-hub-faq-list details').count(),3,'three customer questions');
   assert(await page.locator('.tailoring-hub-essentials').innerText().then(t=>t.includes('1–3 weeks')&&t.includes('2–3 days')&&t.includes('70%')&&t.includes('35%')),'approved tailoring estimates and deposit are visible');
   for(const href of ['/guides/fabrics/','/measurements/','/customer-information/','/services/custom-tailoring/special-order/','/services/alterations/','/services/garment-care/','/services/mobile-fitting/']){
    assert(await page.locator('a[href="'+href+'"]').count()>0,'missing customer guidance/service route '+href);
   }
   const factsColumns=await page.locator('.tailoring-hub-fact-grid').evaluate(el=>getComputedStyle(el).gridTemplateColumns.split(' ').filter(Boolean).length);
   assert.equal(factsColumns,width<=320?1:2,'policy card layout '+width);
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
    assert.equal(await page.locator('.terms-popup-page').count(),require('../_data/policy-documents.json').documents['terms-and-conditions'].receivedVersions.at(-1).technicalInspection.pages);
    await page.screenshot({path:path.join(dest,'terms-390.png')});
   }
   assert.deepEqual(errors,[],'Page JavaScript errors at '+width);
   await context.close();
   console.log('PASS R59 local Chromium '+width+'px: homepage, gallery tap-to-pause, clean autoplay videos, hub, Showroom filters, Shop, '+(width===390?'Terms':'no Terms rerun'));
  }
  const reduced=await browser.newContext({viewport:{width:390,height:844},reducedMotion:'reduce'});
  const page=await reduced.newPage();await page.goto(base+'/',{waitUntil:'domcontentloaded'});
  const styles=await page.locator('.moving-gallery-track').evaluateAll(x=>x.map(e=>getComputedStyle(e).animationName));
  assert(styles.every(x=>x==='none'),'reduced-motion disables both moving galleries');
  assert(await page.locator('.tailoring-video-card video').evaluateAll(v=>v.length===2&&v.every(video=>video.paused)),'reduced motion prevents video autoplay');
  await reduced.close();console.log('PASS: reduced-motion static photo fallback');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
