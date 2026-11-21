/* R56 actual Chromium browser checks at common mobile/desktop widths. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {chromium}=require('playwright');
const base='http://127.0.0.1:8020';
(async()=>{
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
try{
 fs.mkdirSync('artifacts/r56-homepage',{recursive:true});
 for(const width of [320,390,768,1440]){
  const height=width<=390?844:900;
  const context=await browser.newContext({viewport:{width,height},deviceScaleFactor:1,isMobile:width<=390,hasTouch:width<=390});
  const page=await context.newPage();
  const errors=[];page.on('pageerror',e=>errors.push(e.message));
  const response=await page.goto(base+'/',{waitUntil:'domcontentloaded'});
  assert.equal(response.status(),200);
  const h1=page.locator('h1#hero-title');assert.equal(await h1.count(),1);
  assert((await h1.innerText()).includes('Professional Tailor in Kigali, Rwanda'));
  assert.equal(await page.locator('.r56-showcase-card').count(),2);
  assert.equal(await page.locator('.r56-showcase-card video').count(),0);
  const imgs=page.locator('.r56-showcase-card img');
  assert.equal(await imgs.count(),2);
  const main=page.locator('a.r56-primary-card[href="/services/custom-tailoring/"]');
  const vip=page.locator('a.r56-primary-card[href="/services/vip/"]');
  assert.equal(await main.count(),1);assert.equal(await vip.count(),1);
  assert.equal(await page.locator('.r56-gallery[data-direction="left"]').count(),1);
  assert.equal(await page.locator('.r56-gallery[data-direction="right"]').count(),1);
  assert.equal(await page.locator('.r56-gallery-group[aria-hidden="true"]').count(),2);
  assert.equal(await page.locator('.r56-gallery-panel').count(),2);
  assert.equal(await page.locator('#supportForm').count(),1);
  assert.equal(await page.locator('a[data-whatsapp-modal]').count()>0,true);
  assert.equal(await page.locator('.r56-hero-actions a[href="/collections/"]').count(),1);
  const bodyOverflow=await page.evaluate(()=>document.documentElement.scrollWidth-document.documentElement.clientWidth);
  assert(bodyOverflow<=2,'No horizontal viewport overflow '+width+'px: '+bodyOverflow);
  await page.locator('.r56-galleries-section').scrollIntoViewIfNeeded();
  const pause=page.locator('[data-r56-pause]').first();
  await pause.waitFor({state:'visible'});
  await pause.click();
  assert.equal(await pause.getAttribute('aria-pressed'),'true');
  assert.equal(await page.locator('.r56-gallery').first().getAttribute('data-paused'),'true');
  await pause.click();
  assert.equal(await pause.getAttribute('aria-pressed'),'false');
  assert.deepEqual(errors,[],'no client JS exceptions '+width+'px');
  if(width===390||width===1440){
    await page.screenshot({path:path.join('artifacts/r56-homepage','home-'+width+'.png'),fullPage:true});
    await h1.scrollIntoViewIfNeeded();
    await page.screenshot({path:path.join('artifacts/r56-homepage','hero-'+width+'.png')});
  }
  console.log('PASS: tailoring homepage '+width+'px — H1, media fallback, service/VIP cards, galleries, pausing and consent links');
  await context.close();
 }
 const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true,reducedMotion:'reduce'});
 const page=await context.newPage();
 await page.goto(base+'/',{waitUntil:'domcontentloaded'});
 await page.locator('.r56-galleries-section').scrollIntoViewIfNeeded();
 const motion=await page.locator('.r56-gallery-track').first().evaluate(e=>getComputedStyle(e).animationName);
 assert.equal(motion,'none','reduced motion stops both moving galleries');
 const state=await page.locator('.r56-gallery').first().evaluate(e=>getComputedStyle(e).overflowX);
 assert(state==='auto'||state==='scroll','reduced motion provides static horizontal photo scroll');
 console.log('PASS: reduced-motion static photo fallback on mobile');
 await context.close();
}finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
