/* Phase 1 owner handoff: homepage journeys, SEO, keyboard access and delivery budget. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const base=process.env.REVIEW_BASE_URL||'http://127.0.0.1:8000/',origin=new URL(base).origin;
const out=process.env.REVIEW_ARTIFACTS||'/workspace/artifacts/phase1';
const seo=JSON.parse(fs.readFileSync('_data/page-seo.json'))['index.html'];
(async()=>{fs.mkdirSync(out,{recursive:true});const b=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',args:['--no-sandbox']});try{
const c=await b.newContext({reducedMotion:'reduce'});await c.route('**/*',r=>new URL(r.request().url()).origin===origin?r.continue():r.abort());
const p=await c.newPage(),errors=[],bad=[];p.on('pageerror',e=>errors.push(e.message));p.on('response',r=>{if(new URL(r.url()).origin===origin&&r.status()>=400)bad.push(r.url())});
for(const width of [320,360,390,430,768,1024,1100,1440]){
 await p.setViewportSize({width,height:900});await p.goto(base);await p.locator('.hero-lcp').evaluate(i=>i.decode());
 assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`overflow at ${width}`);
 assert.match(await p.locator('h1').innerText(),/Mr Sewing Fashion[\s\S]*Your Clothing\.[\s\S]*Our Craft\./);
 assert(await p.locator('.home-quote-action').isVisible());assert.equal(await p.locator('.home-step-grid li').count(),5);
 assert.deepEqual(await p.locator('main > div').evaluateAll(es=>es.map(e=>e.id)),['hero-section','services-section','information-section','benefits-section','process-section','options-section','customers-section','collections-section','programs-section','final-section']);
 assert.equal(await p.locator('.service-card').count(),6);
 assert(await p.locator('#programs-section').evaluate(e=>e.nextElementSibling?.id==='final-section'));
 for(const id of ['loyalty-program','referral-program','photoshoot-preview'])assert(await p.locator('#'+id).isVisible());
 assert.equal(await p.locator('#programs .program-status').filter({hasText:'Coming Soon'}).count(),3);
 assert.equal(await p.locator('#programs a,#programs button,#programs input,#programs form').count(),0);
 assert.match(await p.locator('#final-section .home-eyebrow').innerText(),/Let’s make it personal/i);
 assert.equal(await p.locator('#final-title').innerText(),'Your Next Special\nOutfit Starts Here.');
 assert.match(await p.locator('.service-card').last().innerText(),/workplace visit/);
 assert.match(await p.locator('.home-step-grid li').nth(1).innerText(),/required advance payment before production/);
 assert(await p.locator('#hero-pause').isHidden());await p.locator('[data-hero-step="1"]').click();assert.equal(await p.locator('[data-hero-slide].is-active').getAttribute('data-hero-slide'),'1');
 if(width<1100){const t=p.locator('.home-menu-toggle');await t.focus();await p.keyboard.press('Enter');assert(await p.locator('#home-navigation').isVisible());await p.keyboard.press('Escape');assert(await t.evaluate(e=>e===document.activeElement));await t.click();await p.locator('#home-navigation a[href="#services"]').click();await p.waitForFunction(()=>document.activeElement?.id==='services-title');assert.equal(await t.getAttribute('aria-expanded'),'false');}
 await p.locator('.home-quote-action').click();await p.waitForURL('**/#quotation');await p.waitForFunction(()=>{const r=document.getElementById('final-title').getBoundingClientRect();return r.top>=0&&r.top<innerHeight});
 for(const a of await p.locator('.quote-pathways a').all()){const u=new URL(await a.getAttribute('href'));assert.equal(u.origin,'https://wa.me');assert.equal(u.pathname,'/250787411501');assert(u.searchParams.get('text').startsWith('Hello Mr Sewing'));}
 if([390,768,1440].includes(width)){await p.locator('main img').evaluateAll(async es=>{for(const e of es)e.loading='eager';await Promise.all(es.map(e=>e.decode()))});await p.screenshot({path:path.join(out,`after-${width}.png`),fullPage:true});await p.locator('#programs-section').screenshot({path:path.join(out,`programs-${width}.png`)});await p.locator('#final-section').screenshot({path:path.join(out,`personal-${width}.png`)});}
}
await p.goto(base);assert.equal(await p.title(),seo.title);assert.equal(await p.locator('meta[name="description"]').getAttribute('content'),seo.description);
for(const tag of ['title','meta[name="description"]','meta[name="robots"]','link[rel="canonical"]','meta[property="og:title"]','meta[property="og:image"]','meta[name="twitter:image"]'])assert.equal(await p.locator(tag).count(),1,tag);
assert.equal(await p.locator('link[rel="canonical"]').getAttribute('href'),'https://mrsewingfashion.com/');
assert.equal(await p.locator('meta[property="og:title"]').getAttribute('content'),seo.title);
const image=await p.locator('meta[property="og:image"]').getAttribute('content');assert.equal(image,'https://mrsewingfashion.com/MR%20LOGO.jpeg');assert.equal(await p.locator('meta[name="twitter:image"]').getAttribute('content'),image);
const dimensions=await p.evaluate(async()=>{const i=new Image();i.src='/MR%20LOGO.jpeg';await i.decode();return [i.naturalWidth,i.naturalHeight]});assert.deepEqual(dimensions,[1244,802]);
const graph=JSON.parse(await p.locator('script[type="application/ld+json"]').textContent())['@graph'];assert.equal(graph[0].publisher.telephone,'+250787411501');assert.equal(graph[0].publisher.openingHoursSpecification[0].opens,'09:00');
const links=await p.locator('a[href]').evaluateAll(es=>es.map(e=>e.href));
for(const href of new Set(links)){const u=new URL(href);if(u.origin!==origin)continue;if(u.pathname==='/'&&u.hash){assert(await p.locator(`[id="${decodeURIComponent(u.hash.slice(1))}"]`).count(),href);continue;}const res=await c.request.get(href);assert.equal(res.status(),200,href);}
// No new form or success simulation is added to the homepage. Existing forms are tested separately.
assert.equal(await p.locator('main form').count(),0);
assert(await p.locator('.quote-privacy').innerText().then(t=>t.includes('No enquiry is submitted')));
const budget=await p.evaluate(()=>({htmlBytes:new TextEncoder().encode(document.documentElement.outerHTML).length,requests:performance.getEntriesByType('resource').length,hero:performance.getEntriesByType('resource').filter(e=>/\/(h1\.jpeg|h1-480\.webp)$/.test(e.name)).length}));
assert(budget.htmlBytes<100000,'HTML budget');assert.equal(budget.hero,1);console.log('Homepage delivery checks:',budget);
assert.deepEqual(errors,[]);assert.deepEqual(bad,[]);await c.close();
const n=await b.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});await n.route('https://**/*',r=>r.abort());const np=await n.newPage();await np.goto(base);assert(await np.locator('#home-navigation').isVisible());assert(await np.locator('.home-quote-action').isVisible());await np.locator('.home-quote-action').click();assert.equal(new URL(np.url()).hash,'#quotation');assert(await np.locator('.quote-pathways').isVisible());await n.close();
console.log('PASS: eight widths, homepage section order, keyboard disclosure/focus return, quotes, five-step advance gate, local links, social dimensions, metadata/schema, no-JS and delivery budget.');
}finally{await b.close()}})().catch(e=>{console.error(e);process.exit(1)});
