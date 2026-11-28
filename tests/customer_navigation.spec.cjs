/* Actual local browser navigation checks; all external requests blocked. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const base = process.env.BASE_URL || 'http://127.0.0.1:3000';
const shell=require('../_data/site-shell.json'),labels=require('../_data/customer-interface-labels.json');
const guides=require('../_data/homepage-guides.json').filter(item=>item.href);
const messages=require('../_data/service-contact-actions.json').messages;
const serviceNames=shell.serviceNavigation.map(key=>{const item=shell.destinations[key];return item.navLabel||labels.services[item.serviceId]||item.label;});
assert.deepEqual(shell.serviceNavigation,['custom-tailoring','alterations','garment-care','combined'],'Phase1 approved primary service projection');
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
   assert.equal(await services.locator('a:visible').count(),shell.serviceNavigation.length);
   assert.deepEqual(await services.locator('a:visible').allTextContents(),serviceNames);
   for(const key of shell.serviceNavigation){
    const item=shell.destinations[key],link=services.locator('a').nth(shell.serviceNavigation.indexOf(key));
    const url=new URL(await link.getAttribute('href'),base);
    if(item.whatsappMessageId){assert.equal(url.pathname,'/whatsapp/');assert.equal(url.searchParams.get('text'),messages[item.whatsappMessageId]);}
    else assert.equal(url.pathname,item.href);
   }
   await page.keyboard.press('Escape');assert.equal(await services.evaluate(node=>node.open),false);
   assert.equal(await menu.locator('.header-guides').count(),0,'guides belong in the footer under the Phase1 navigation');
   for(const guide of guides){const link=page.locator('.homepage-footer a[href="'+guide.href+'"]');assert.equal(await link.count(),1);assert.equal(await link.textContent(),guide.label);}
   assert.equal(await page.locator('.homepage-footer a[href="/faq/"]').count(),1);
   assert.equal(await page.locator('h1').innerText(),'Fabric Guide','current independent guide remains clearly identified');
   if(width<1100){
    await menu.locator('a[href="/contact/"]').focus();await page.keyboard.press('Tab');
    assert.equal(await toggle.evaluate(node=>node===document.activeElement),true);
    await page.keyboard.press('Escape');assert.equal(await toggle.getAttribute('aria-expanded'),'false');
    assert.equal(await page.locator('main').evaluate(node=>node.inert),false);
    await toggle.click();await page.mouse.click(2,898);assert.equal(await toggle.getAttribute('aria-expanded'),'false');
   }
   assert.equal(await page.locator('.fg-grid').first().evaluate(node=>getComputedStyle(node).gridTemplateColumns.split(' ').length),width>1000?3:2);
   assert.equal(await page.locator('.fg-card').count(),7);
   assert.equal(await page.locator('.fg-card img,.fg-card canvas').count(),0);
   assert.equal(await page.locator('.fg-card a').allTextContents().then(labels=>labels.every(label=>label.includes('Explore Collection'))),true);
   assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),true);
   await page.screenshot({path:path.join(out,'fabric-navigation-'+width+'.png'),fullPage:true});
   assert.deepEqual(errors,[]);result.views.push({width,status:'PASS',mainInertAndFocusLoop:width<1100?'PASS':'not applicable',servicesDisclosureAndFooterGuides:'PASS',compactFabricGrid:'PASS',errors});
   await context.close();
  }
  const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:900}});await nojs.route('https://**/*',route=>route.abort());
  const page=await nojs.newPage();await page.goto(base+'/guides/fabrics/');assert.equal(await page.locator('#home-navigation').isVisible(),true);
  await page.locator('#home-navigation .services-dropdown summary').click();assert.equal(await page.locator('#home-navigation .services-dropdown a:visible').count(),shell.serviceNavigation.length);
  for(const guide of guides)assert(await page.locator('.homepage-footer a[href="'+guide.href+'"]').isVisible(),'guide remains usable without JavaScript');
  result.noJavaScript='PASS';await nojs.close();
  fs.writeFileSync(path.join(out,'results.json'),JSON.stringify(result,null,2));console.log('PASS shared navigation: 4widths, source-backed four-service disclosure/footer guides, mobile focus/inert/Escape/backdrop, current guide identification, noJS links and compact7collection grid.');
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exit(1);});
