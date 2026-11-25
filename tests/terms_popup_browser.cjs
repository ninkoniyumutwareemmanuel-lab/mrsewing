/* R55 real Chromium smoke checks for the Android-safe full-screen PDF popup. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {chromium}=require('playwright');
const base='http://127.0.0.1:8020';
const expected=require('../_data/policy-documents.json').documents['terms-and-conditions'].receivedVersions.at(-1).technicalInspection.pages;
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 try{
  fs.mkdirSync('artifacts/r55-terms',{recursive:true});
  for(const width of [320,390,768,1440]){
   const height=width<600?844:900;
   const context=await browser.newContext({viewport:{width,height},isMobile:width<600,hasTouch:width<600,deviceScaleFactor:1,reducedMotion:'reduce'});
   const page=await context.newPage();
   const errors=[];
   page.on('pageerror',e=>errors.push(e.message));
   const response=await page.goto(base+'/terms-and-conditions/',{waitUntil:'networkidle'});
   assert.equal(response.status(),200,'Terms route HTTP 200');
   const modal=page.locator('#termsPdfDialog');
   await modal.waitFor({state:'visible'});
   const bounds=await modal.boundingBox();
   assert(bounds&&Math.abs(bounds.width-width)<=2,'Popup fills mobile/desktop width: '+width);
   assert(Math.abs(bounds.height-height)<=3,'Popup fills mobile/desktop height: '+width);
   assert.equal(await page.locator('.terms-popup-page').count(),expected,'all original PDF pages are present');
   assert.equal(await page.locator('object[type="application/pdf"]').count(),0,'does not rely on unsupported native PDF');
   assert.equal(await page.locator('.terms-document-state').count(),0,'old brochure header has been removed');
   await page.locator('.terms-popup-page img').first().waitFor({state:'visible'});
   const ready=await page.locator('.terms-popup-page img').first().evaluate(img=>img.complete&&img.naturalWidth===1360);
   assert(ready,'real PDF page 1 loaded and decoded');
   const ui=await page.evaluate(()=>{
    const scroller=document.querySelector('[data-terms-scroll]'),modal=document.querySelector('#termsPdfDialog');
    return {active:modal.open,scrollHeight:scroller.scrollHeight,clientHeight:scroller.clientHeight,bodyLocked:getComputedStyle(document.body).overflow};
   });
   assert(ui.active,'modal stays open');
   assert(ui.scrollHeight>ui.clientHeight*2,'all PDF pages are scrollable');
   assert.equal(ui.bodyLocked,'hidden','background page does not scroll');
   if(width===390||width===1440){await page.screenshot({path:path.join('artifacts/r55-terms','terms-'+width+'.png'),fullPage:false});}
   await page.evaluate(()=>{const s=document.querySelector('[data-terms-scroll]');s.scrollTop=s.scrollHeight;});
   await page.waitForTimeout(250);
   assert.equal(await page.locator('[data-terms-page-number]').textContent(),String(expected),'scroll reaches final PDF page');
   await page.locator('[data-terms-zoom-in]').click();
   const widthIn=await page.locator('[data-terms-pages]').evaluate(n=>n.clientWidth);
   await page.locator('[data-terms-zoom-out]').click();
   const widthOut=await page.locator('[data-terms-pages]').evaluate(n=>n.clientWidth);
   assert(widthIn>widthOut,'zoom controls enlarge actual PDF pages');
   assert.deepEqual(errors,[],'no page JS errors');
   await page.locator('[data-terms-close]').click();
   await page.waitForURL(base+'/',{timeout:15000});
   console.log('PASS: R55 Chromium popup at '+width+'px, '+expected+' pages, scroll/zoom/close, no plug-in');
   await context.close();
  }
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1;});
