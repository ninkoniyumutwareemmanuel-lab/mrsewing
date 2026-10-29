/* New homepage journey and accessible menu. No messages or real form submissions. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const base=process.env.REVIEW_BASE_URL||'http://127.0.0.1:8000/';
const titles=["Have a Design in Mind? Let's Bring It to Life.",'Made for Real People. Worn for Special Moments.','Find Inspiration for Your Next Outfit.','From Your Idea to Your Perfect Fit.','More Than Tailoring. A Personalized Experience.','Tailoring Services for Every Occasion.','Your Next Special Outfit Starts Here.'];
(async()=>{const b=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',args:['--no-sandbox']});try{
  for(const width of [320,360,390,430,768,1440]){
    const c=await b.newContext({viewport:{width,height:900}});
    await c.route('**/*',r=>new URL(r.request().url()).origin===new URL(base).origin?r.continue():r.abort());
    const p=await c.newPage();const errors=[],broken=[];p.on('pageerror',e=>errors.push(e.message));p.on('response',r=>{if(r.status()>=400)broken.push(r.url())});
    await p.goto(base);
    assert.deepEqual(await p.locator('main section').evaluateAll(es=>es.map(e=>e.querySelector('h1,h2').textContent)),titles);
    assert.equal(await p.locator('h1').count(),1);assert.equal(await p.locator('header nav').count(),1);
    assert.equal(await p.locator('header').getByText('Book Consultation',{exact:true}).count(),0);
    const toggle=p.locator('.home-menu-toggle'),nav=p.locator('#home-navigation');
    if(width<=1100){
      assert.equal(await toggle.getAttribute('aria-expanded'),'false');assert(!await nav.isVisible());
      const before=await p.locator('.hero-section').boundingBox();await toggle.focus();await p.keyboard.press('Enter');assert(await nav.isVisible());assert.equal(await toggle.getAttribute('aria-expanded'),'true');
      assert.equal((await p.locator('.hero-section').boundingBox()).y,before.y,'menu overlays without shifting content');
      await p.keyboard.press('Tab');assert.equal(await p.evaluate(()=>document.activeElement.textContent),'Home');
      await p.keyboard.press('Escape');assert(!await nav.isVisible());assert(await toggle.evaluate(e=>e===document.activeElement));
      await toggle.click();await p.mouse.click(width-8,700);assert(!await nav.isVisible());
      await toggle.click();await nav.getByRole('link',{name:'Contact Us',exact:true}).click();await p.waitForURL('**/contact/');await p.goto(base);
      const header=await p.locator('header').boundingBox();assert(header.height<=80,'single-row mobile header');
    }else{assert(await nav.isVisible());assert(!await toggle.isVisible());}
    await p.locator('.hero-btn-secondary').click();await p.waitForURL('**/#customers-section');
    // Observe real anchors while preventing both navigation and external requests.
    await p.evaluate(()=>{window.designIntents=[];document.addEventListener('click',e=>{const a=e.target.closest('a[href^="https://wa.me/"]');if(a){e.preventDefault();window.designIntents.push(a.href)}},true)});
    const actions=p.locator('main a[href^="https://wa.me/"]');assert.equal(await actions.count(),3);
    for(const a of await actions.all()){await a.click();const u=new URL(await a.getAttribute('href'));assert.equal(u.pathname,'/250787411501');assert(u.searchParams.get('text').includes('inspiration photo'));assert((await a.boundingBox()).height>=44);}
    assert.equal(await p.evaluate(()=>window.designIntents.length),3);
    assert.equal(await p.locator('.home-collection-card').count(),4);assert.equal(await p.locator('.service-card').count(),6);
    assert((await p.locator('.home-benefits').textContent()).includes('subject to availability confirmation'));
    assert((await p.locator('.home-benefits').textContent()).includes('Selected premium orders'));
    assert(!/loyalty|referral commission/i.test(await p.locator('main').textContent()));
    // Scroll all photographs into view and verify actual image decoding and reserved space.
    for(const img of await p.locator('main img').all()){await img.scrollIntoViewIfNeeded();await img.evaluate(i=>i.decode());assert(await img.evaluate(i=>i.naturalWidth>0&&i.width>0&&i.height>0));}
    assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
    for(const a of await p.locator('main a[href^="/"]').all()){
      const href=await a.getAttribute('href');const u=new URL(href,base),response=await c.request.get(u.origin+u.pathname);assert.equal(response.status(),200,href);
      if(u.hash){const html=await response.text();assert(html.includes(`id="${u.hash.slice(1)}"`),href);}
    }
    assert.deepEqual(errors,[]);assert.deepEqual(broken,[]);
    await c.close();
  }
  const nojs=await b.newContext({viewport:{width:320,height:900},javaScriptEnabled:false});await nojs.route('https://**/*',r=>r.abort());const p=await nojs.newPage();await p.goto(base);for(const link of await p.locator('header nav a').all())assert(await link.isVisible());assert(!await p.locator('.home-menu-toggle').isVisible());assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));await nojs.close();
  console.log('PASS: seven ordered sections, three safe WhatsApp design intents, working existing destinations, decoded photographs, single-row disclosure menu with keyboard/Escape/outside close and no-JS fallback, no overflow/errors/missing assets at six widths.');
}finally{await b.close()}})().catch(e=>{console.error(e);process.exitCode=1});
