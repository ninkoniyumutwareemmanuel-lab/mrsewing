/* Actual local browser navigation checks; all external requests blocked. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const base = process.env.BASE_URL || 'http://127.0.0.1:3000';
const out = path.resolve(process.env.REVIEW_ARTIFACTS || 'artifacts/customer-navigation');
fs.mkdirSync(out,{recursive:true});
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||process.env.CHROMIUM_BINARY||(fs.existsSync('/usr/bin/chromium')?'/usr/bin/chromium':undefined),args:['--no-sandbox']});
 const result={scope:'Local Chromium navigation only; external requests blocked; not deployed-origin verification',views:[]};
 try{
  for(const width of [320,390,768,1440]){
   const context=await browser.newContext({viewport:{width,height:900},reducedMotion:'reduce'});
   await context.route('**/*',route=>new URL(route.request().url()).origin===new URL(base).origin?route.continue():route.abort());
   const page=await context.newPage(),errors=[];page.on('pageerror',error=>errors.push(error.message));
   await page.goto(base+'/guides/fabrics/');
   const toggle=page.locator('.home-menu-toggle'),menu=page.locator('#home-navigation');
   if(width<1100){
    await toggle.click();assert.equal(await toggle.getAttribute('aria-expanded'),'true');
    assert.equal(await page.locator('main').evaluate(node=>node.inert),true);
    await page.keyboard.press('Tab');assert.equal(await menu.locator('a[href="/"]').evaluate(node=>node===document.activeElement),true);
   }
   const services=menu.locator('.services-dropdown>details');
   await services.locator('summary').click();
   assert.equal(await services.locator('a:visible').count(),5);
   assert.equal(await services.locator('a[href="/services/custom-tailoring/"]').textContent(),'Tailoring & Clothing Services');
   await page.keyboard.press('Escape');assert.equal(await services.evaluate(node=>node.open),false);
   const guides=menu.locator('.header-guides>details');
   await guides.locator('summary').click();assert.equal(await guides.locator('a:visible').count(),3);
   assert.equal(await guides.locator('a[aria-current="page"]').getAttribute('href'),'/guides/fabrics/');
   if(width<1100){
    await menu.locator('a[href="/contact/"]').focus();await page.keyboard.press('Tab');
    assert.equal(await toggle.evaluate(node=>node===document.activeElement),true);
    await page.keyboard.press('Escape');assert.equal(await toggle.getAttribute('aria-expanded'),'false');
    assert.equal(await page.locator('main').evaluate(node=>node.inert),false);
    await toggle.click();await page.mouse.click(2,898);assert.equal(await toggle.getAttribute('aria-expanded'),'false');
   }else{await page.keyboard.press('Escape');assert.equal(await guides.evaluate(node=>node.open),false);}
   assert.equal(await page.locator('.fg-grid').first().evaluate(node=>getComputedStyle(node).gridTemplateColumns.split(' ').length),width>1000?3:2);
   assert.equal(await page.locator('.fg-card').count(),7);
   assert.equal(await page.locator('.fg-card img,.fg-card canvas').count(),0);
   assert.equal(await page.locator('.fg-card a').allTextContents().then(labels=>labels.every(label=>label.includes('Explore Collection'))),true);
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),true);
   await page.screenshot({path:path.join(out,'fabric-navigation-'+width+'.png'),fullPage:true});
   assert.deepEqual(errors,[]);result.views.push({width,status:'PASS',mainInertAndFocusLoop:width<1100?'PASS':'not applicable',serviceAndGuideDisclosures:'PASS',compactFabricGrid:'PASS',errors});
   await context.close();
  }
  const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:900}});await nojs.route('https://**/*',route=>route.abort());
  const page=await nojs.newPage();await page.goto(base+'/guides/fabrics/');assert.equal(await page.locator('#home-navigation').isVisible(),true);
  await page.locator('#home-navigation .services-dropdown summary').click();assert.equal(await page.locator('#home-navigation .services-dropdown a:visible').count(),5);
  result.noJavaScript='PASS';await nojs.close();
  fs.writeFileSync(path.join(out,'results.json'),JSON.stringify(result,null,2));console.log('PASS shared navigation: 4widths, Services/Guides disclosure, mobile focus/inert/Escape/backdrop, active guide, noJS links and compact7collection grid.');
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exit(1);});
