/* R57: verify the original page was preserved across four real browser widths. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const {chromium}=require('playwright');
const base='http://127.0.0.1:8020';
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 try{
  fs.mkdirSync('artifacts/r57-preserved-homepage',{recursive:true});
  for(const width of [320,390,768,1440]){
   const context=await browser.newContext({viewport:{width,height:width<=390?844:900},deviceScaleFactor:1,isMobile:width<=390,hasTouch:width<=390});
   const page=await context.newPage();const errors=[];
   page.on('pageerror',e=>errors.push(e.message));
   const response=await page.goto(base+'/',{waitUntil:'domcontentloaded'});
   assert.equal(response.status(),200);
   assert((await page.locator('#hero-title').innerText()).includes('Professional Tailor in Kigali, Rwanda'));
   assert.equal(await page.locator('a[data-whatsapp-modal]').count()>0,true);
   assert.equal(await page.locator('a[href="/collections/"]').count()>0,true);
   assert.equal(await page.locator('.r56-showcase-card img').count(),2);
   assert.equal(await page.locator('.home-r57-feature img').count(),1);
   assert.equal(await page.locator('.service-card').count(),5);
   assert.equal(await page.locator('.service-card-primary').count(),1);
   assert.equal(await page.locator('.service-card-vip').count(),1);
   assert.equal(await page.locator('#information-section').count(),1);
   assert.equal(await page.locator('#process-section').count(),1);
   assert.equal(await page.locator('#benefits-section').count(),1);
   assert.equal(await page.locator('#options-section').count(),1);
   assert.equal(await page.locator('#customers-section').count(),1);
   assert.equal(await page.locator('#programs-section').count(),1);
   assert.equal(await page.locator('#contact-section').count(),1);
   assert.equal(await page.locator('#supportForm').count(),1);
   assert.equal(await page.locator('.moving-gallery').count(),3);
   assert.equal(await page.locator('.moving-gallery[data-gallery-direction="left"]').count(),2);
   assert.equal(await page.locator('.moving-gallery[data-gallery-direction="right"]').count(),1);
   assert.equal(await page.locator('.gallery-motion-control').count(),3);
   const overshoot=await page.evaluate(()=>document.documentElement.scrollWidth-document.documentElement.clientWidth);
   assert(overshoot<=3,'No extra horizontal overflow at '+width+'px: '+overshoot);
   const motionButton=page.locator('.collection-preview .gallery-motion-control').first();
   await motionButton.scrollIntoViewIfNeeded();
   await motionButton.waitFor({state:'visible'});
   await motionButton.click();
   assert.equal(await motionButton.getAttribute('aria-pressed'),'true');
   await motionButton.click();
   assert.equal(await motionButton.getAttribute('aria-pressed'),'false');
   assert.deepEqual(errors,[],'No page JS exceptions at '+width+'px');
   if(width===390||width===1440){
    await page.screenshot({path:'artifacts/r57-preserved-homepage/home-'+width+'.png',fullPage:true});
    await page.locator('#hero-title').scrollIntoViewIfNeeded();
    await page.screenshot({path:'artifacts/r57-preserved-homepage/hero-'+width+'.png'});
   }
   console.log('PASS: R57 preserved all old homepage sections and requested additions at '+width+'px');
   await context.close();
  }
  const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,reducedMotion:'reduce'});
  const page=await context.newPage();
  await page.goto(base+'/',{waitUntil:'domcontentloaded'});
  await page.locator('.collection-preview').first().scrollIntoViewIfNeeded();
  const name=await page.locator('.collection-preview .moving-gallery-track').first().evaluate(node=>getComputedStyle(node).animationName);
  assert.equal(name,'none','Reduced-motion prevents gallery animation');
  console.log('PASS: reduced-motion fallback retains still galleries');
  await context.close();
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
