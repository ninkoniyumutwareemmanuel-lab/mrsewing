/* About V2: real local browser navigation; external services always blocked. */
const {chromium}=require('playwright'),assert=require('assert/strict');
const base=process.env.REVIEW_BASE_URL||'http://127.0.0.1:8000/';
(async()=>{const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});try{
const context=await browser.newContext({reducedMotion:'reduce'});await context.route('**/*',r=>new URL(r.request().url()).origin===new URL(base).origin?r.continue():r.abort());
const page=await context.newPage(),errors=[],missing=[],requests=[];page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.status()>=400&&r.url().startsWith(base))missing.push(r.url())});page.on('request',r=>requests.push(r.url()));
for(const width of [320,360,390,430,768,1024,1440]){
 await page.setViewportSize({width,height:900});await page.goto(base+'about/');await page.locator('.about-hero-image').evaluate(i=>i.decode());
 assert.equal(await page.locator('h1').count(),1);assert((await page.locator('h1').textContent()).includes('A Reflection of You.'));
 const body=await page.locator('main').textContent();for(const t of ['2019','father','small workshop','Our Mission','Our Vision','Made in Rwanda','NINKONIYUMUTWARE NEXUS LTD','Designed Around You'])assert(body.includes(t),t);
 assert(!/Mr Sewing Fashion Designer|NINKONIYUMUTWARE Emmanuel|Chief Executive|CEO/.test(body));
 assert.equal(await page.locator('.about-values li').count(),5);assert.equal(await page.locator('.about-services article').count(),7);assert.equal(await page.locator('.about-timeline li').count(),2);
 assert.equal(await page.locator('.about-final a').count(),2);assert.deepEqual(await page.locator('.about-final a').evaluateAll(es=>es.map(e=>e.getAttribute('href'))),['/collections/','/contact/']);
 assert.equal(await page.locator('link[rel=canonical]').count(),1);assert.equal(await page.locator('link[rel=canonical]').getAttribute('href'),'https://mrsewingfashion.com/about/');assert((await page.title()).includes('Mr Sewing Fashion'));
 const ld=JSON.parse(await page.locator('script[type="application/ld+json"]').textContent());const org=ld['@graph'].find(e=>e['@type']==='Organization');assert.equal(org.foundingDate,'2019');assert.equal(org.parentOrganization.name,'NINKONIYUMUTWARE NEXUS LTD');assert(!org.aggregateRating&&!org.review&&!org.founder);
 assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`overflow ${width}`);assert(await page.locator('img').evaluateAll(is=>is.every(i=>i.complete&&i.naturalWidth>0&&i.alt)));
 assert.equal(await page.locator('.about-hero-image').getAttribute('loading'),'eager');assert.equal(await page.locator('.about-hero-image').getAttribute('fetchpriority'),'high');assert((await page.locator('.about-hero-image').evaluate(i=>i.currentSrc)).endsWith('.avif'));
 assert.equal(await page.locator('footer .social-icons a').count(),4);assert.equal(await page.locator('footer a[href="https://youtube.com/@mr.sewingfashion"]').count(),1);
 if(width<1100){const toggle=page.locator('.home-menu-toggle');await toggle.focus();await page.keyboard.press('Enter');assert.equal(await toggle.getAttribute('aria-expanded'),'true');await page.keyboard.press('Escape');assert.equal(await toggle.getAttribute('aria-expanded'),'false');assert(await toggle.evaluate(e=>document.activeElement===e));await toggle.click();await page.mouse.click(width-10,850);assert.equal(await toggle.getAttribute('aria-expanded'),'false');await toggle.click();await page.locator('header a[href="/contact/"]').click();await page.waitForURL('**/contact/');await page.goto(base+'about/');}
 if([390,1440].includes(width))await page.screenshot({path:`/workspace/phase1-review/about-v2/about-${width}.png`,fullPage:true});
}
assert(!requests.some(u=>/cdnjs|\.woff2?$|\/(header|footer)\.html/.test(u)));
const footer=await page.locator('footer').innerHTML();await page.goto(base);assert.equal(await page.locator('footer').innerHTML(),footer);await page.goto(base+'contact/');assert.equal(await page.locator('footer').innerHTML(),footer);
await page.goto(base+'about/');for(const href of await page.locator('a[href]').evaluateAll(es=>[...new Set(es.map(e=>e.getAttribute('href')).filter(h=>h.startsWith('/')))])){assert((await context.request.get(new URL(href,base).href)).ok(),href)}
for(const [selector,path] of [['.about-final a[href="/collections/"]','collections/'],['.about-final a[href="/contact/"]','contact/']]){await page.goto(base+'about/');await page.locator(selector).click();await page.waitForURL(base+path);assert(await page.locator('h1').isVisible());}
await page.goto(base+'about.html?review=1#story-title');await page.waitForURL(base+'about/?review=1#story-title');
assert.deepEqual(errors,[]);assert.deepEqual(missing,[]);await context.close();
const nojs=await browser.newContext({javaScriptEnabled:false});await nojs.route('https://**/*',r=>r.abort());const fallback=await nojs.newPage();await fallback.goto(base+'about/');assert(await fallback.locator('#story-title').isVisible());assert.equal(await fallback.locator('.about-values li').count(),5);assert(await fallback.locator('header nav').isVisible());await nojs.close();
console.log('PASS: About V2 approved story/year/parent, five values, seven services, two CTAs, clean/legacy routes, shared footer, responsive AVIF, seven viewports, keyboard/menu interactions, SEO/JSON-LD, local links and no-JS content; no real messages/submissions.');
}finally{await browser.close()}})().catch(e=>{console.error(e);process.exit(1)});
