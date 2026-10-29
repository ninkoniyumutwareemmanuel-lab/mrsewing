/* Contact V2: local-only browser tests; external navigation and real submissions blocked. */
const {chromium}=require('playwright');
const assert=require('assert/strict');
const fs=require('fs');
const base=process.env.REVIEW_BASE_URL||'http://127.0.0.1:8000/';
(async()=>{const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});try{
const context=await browser.newContext();await context.route('**/*',r=>new URL(r.request().url()).origin===new URL(base).origin?r.continue():r.abort());
const page=await context.newPage();const errors=[];page.on('pageerror',e=>errors.push(e.message));
for(const width of [320,360,390,430,768,1024,1440]){
await page.setViewportSize({width,height:900});await page.goto(base+'contact/');
assert.equal(await page.locator('h1').count(),1);assert.equal(await page.locator('link[rel=canonical]').getAttribute('href'),'https://mrsewingfashion.com/contact/');
assert.equal(await page.locator('main a[href="/booking/"]').count(),3);assert.equal(await page.locator('form,iframe').count(),0);
assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`overflow ${width}`);
assert(await page.locator('img').evaluateAll(imgs=>imgs.every(i=>i.complete&&i.naturalWidth>0)));
for(const selector of ['a[href="tel:+250787411501"]','a[href="mailto:mrsewingfashiondesigner@gmail.com"]','a[href="https://youtube.com/@mr.sewingfashion"]','a[href="https://maps.app.goo.gl/qz1GzkBunkmzVKXQ6?g_st=ac"]']) assert(await page.locator(selector).count()>0,selector);
const schema=JSON.parse(await page.locator('script[type="application/ld+json"]').textContent());assert.equal(schema['@graph'].length,4);
if(width<1100){const toggle=page.locator('.home-menu-toggle');const nav=page.locator('#home-navigation');await toggle.click();assert.equal(await toggle.getAttribute('aria-expanded'),'true');await page.keyboard.press('Escape');assert.equal(await toggle.getAttribute('aria-expanded'),'false');assert(await toggle.evaluate(e=>document.activeElement===e));await toggle.click();await page.mouse.click(width-10,850);assert.equal(await toggle.getAttribute('aria-expanded'),'false');await toggle.click();await nav.locator('a[href="/contact/"]').click();assert.equal(await toggle.getAttribute('aria-expanded'),'false');}
if([390,1440].includes(width))await page.screenshot({path:`/workspace/phase1-review/contact-v2/contact-${width}.png`,fullPage:true});
}
// Each intentional booking action reaches actual controls, rather than checking HTTP alone.
for(let n=0;n<3;n++){await page.goto(base+'contact/');await page.locator('main a[href="/booking/"]').nth(n).click();await page.waitForURL('**/booking/');assert(await page.locator('form input[required]').count()>0);assert(await page.locator('form input[type="date"]').count()>0);assert(await page.locator('form input[type="checkbox"]').count()>0);assert.equal(await page.locator('form').first().evaluate(f=>f.checkValidity()),false);}
await page.goto(base+'contact.html?review=1#hours');await page.waitForURL('**/contact/?review=1#hours');
await page.goto(base+'contact/');for(const href of await page.locator('a[href]').evaluateAll(as=>as.map(a=>a.getAttribute('href')).filter(h=>h.startsWith('/')))){const target=new URL(href,base);const response=await context.request.get(target.href);assert.equal(response.status(),200,href);}
assert.deepEqual(errors,[]);await context.close();console.log('PASS: Contact V2 seven widths, three real booking entry points/required controls, menu Escape/outside/link closure and focus, local routes, legacy URL, images, contact URLs, SEO and JSON-LD. No real submissions or external messages.');
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exit(1)});
