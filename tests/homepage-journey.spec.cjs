/* New homepage journey and accessible menu. No messages or real form submissions. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict');
const base=process.env.REVIEW_BASE_URL||'http://127.0.0.1:8000/';
const titles=["Have a Design in Mind? Let's Bring It to Life.",'Made for Real People. Worn for Special Moments.','Find Inspiration for Your Next Outfit.','From Your Idea to Your Perfect Fit.','More Than Tailoring. A Personalized Experience.','Tailoring Services for Every Occasion.','Your Next Special Outfit Starts Here.'];
(async()=>{const b=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',args:['--no-sandbox']});try{
  for(const width of [320,360,390,430,768,1024,1440]){
    const c=await b.newContext({viewport:{width,height:900}});
    await c.route('**/*',r=>new URL(r.request().url()).origin===new URL(base).origin?r.continue():r.abort());
    const p=await c.newPage();const errors=[],broken=[];p.on('pageerror',e=>errors.push(e.message));p.on('response',r=>{if(r.status()>=400)broken.push(r.url())});
    await p.goto(base);
    assert.deepEqual(await p.locator('main section').evaluateAll(es=>es.map(e=>e.querySelector('h1,h2').textContent)),titles);
    assert.equal(await p.locator('.brand-name').textContent(),'MR SEWING');
    assert((await p.locator('.hero-description').textContent()).includes('inspiration photo or describe'));
    assert((await p.locator('.hero-description').textContent()).includes('Mr Sewing creates'));
    assert(!/Mr Sewing Fashion Designer|FASHION DESIGNER/.test(await p.content()));
    assert((await p.locator('footer .footer-bottom-copy').textContent()).includes('Mr Sewing Fashion'));
    assert.equal(await p.locator('meta[property="og:site_name"]').getAttribute('content'),'Mr Sewing Fashion');
    assert.equal(await p.locator('meta[property="og:image:width"]').getAttribute('content'),'1536');
    assert.equal(await p.locator('meta[property="og:image:height"]').getAttribute('content'),'2752');
    if(width<768){assert(await p.locator('h1').evaluate(e=>parseFloat(getComputedStyle(e).fontSize)>=38));}
    assert.equal(await p.locator('h1').count(),1);assert.equal(await p.locator('header nav').count(),1);
    assert.equal(await p.locator('header').getByText('Book Consultation',{exact:true}).count(),0);
    const toggle=p.locator('.home-menu-toggle'),nav=p.locator('#home-navigation');
    if(width<1100){
      assert.equal(await toggle.getAttribute('aria-expanded'),'false');assert(!await nav.isVisible());
      const before=await p.locator('.hero-section').boundingBox();await toggle.focus();await p.keyboard.press('Enter');assert(await nav.isVisible());assert.equal(await toggle.getAttribute('aria-expanded'),'true');
      assert.equal((await p.locator('.hero-section').boundingBox()).y,before.y,'menu overlays without shifting content');
      const rows=await nav.locator('a').evaluateAll(es=>es.map(e=>{const r=e.getBoundingClientRect();return {x:r.x,y:r.y,height:r.height}}));
      assert(rows.every((r,i)=>Math.abs(r.x-rows[0].x)<1&&r.height>=44&&(!i||r.y>=rows[i-1].y+rows[i-1].height)),'one left-aligned vertical column with comfortable targets');
      const panel=await nav.boundingBox(),headerBox=await p.locator('header').boundingBox();
      assert(Math.abs(panel.y-headerBox.y-headerBox.height)<1);assert(panel.width<=280&&panel.height<=242,'compact panel beneath header');
      await p.keyboard.press('Tab');assert.equal(await p.evaluate(()=>document.activeElement.textContent),'Home');
      await p.keyboard.press('Escape');assert(!await nav.isVisible());assert(await toggle.evaluate(e=>e===document.activeElement));
      await toggle.click();await p.mouse.click(width-8,700);assert(!await nav.isVisible());
      await toggle.click();await p.mouse.click(10,30);assert(!await nav.isVisible(),'tapping elsewhere in the header closes the panel');
      await toggle.click();await nav.getByRole('link',{name:'Our Work',exact:true}).click();await p.waitForURL('**/#customers-section');assert(!await nav.isVisible());await p.waitForFunction(()=>document.activeElement.id==='customers-title');await p.goto(base);
      await toggle.click();await nav.getByRole('link',{name:'Contact Us',exact:true}).click();await p.waitForURL('**/contact/');await p.goto(base);
      const header=await p.locator('header').boundingBox();assert(header.height<=80,'single-row mobile header');
    }else{assert(await nav.isVisible());assert(!await toggle.isVisible());}
    assert.equal((await toggle.textContent()).trim(),'','icon-only menu, with no visible Menu word');
    assert.equal(await toggle.getAttribute('aria-label'),'Open navigation');
    assert.equal(await p.locator('header .header-order').isVisible(),width>=1100);
    const serviceNames=await p.locator('.service-card h3').allTextContents();
    assert.deepEqual(serviceNames,['Custom Men’s Tailoring','Custom Women’s Tailoring','Graduation Outfits','Wedding & Civil Wedding Outfits','Professional Alterations','VIP Mobile Fitting','Premium Garment Care']);
    assert(await p.locator('.service-card p').evaluateAll(es=>es.every(e=>e.textContent.length>20&&parseFloat(getComputedStyle(e).fontSize)>=14)));
    assert.equal(await p.locator('.customer-card-slide').count(),3);
    const portrait=await p.locator('.customer-card-slide').first().boundingBox();assert(portrait.width>=(width<600?width*.7:300),'generous editorial portraits');
    const footer=p.locator('footer');const footerHeight=(await footer.boundingBox()).height;assert(footerHeight<(width>=1100?420:800),'compact footer');
    if(width>=1100)assert.equal(await p.locator('.footer-top').evaluate(e=>getComputedStyle(e).gridTemplateColumns.split(' ').length),5);
    const hours=p.locator('.footer-hours-details');assert(!await hours.evaluate(e=>e.open));await hours.locator('summary').click();assert(await hours.evaluate(e=>e.open));assert((await hours.textContent()).includes('12:00 PM–5:00 PM, strictly by advance appointment'));assert((await hours.textContent()).includes('Ordinary Saturday visits do not require an appointment'));await hours.locator('summary').click();
    // Retained order consent has keyboard focus containment and returns focus.
    const order=p.locator('footer .order-btn');await order.click();await p.keyboard.press('Shift+Tab');assert(await p.locator('#orderModal').evaluate(e=>e.contains(document.activeElement)));await p.keyboard.press('Escape');assert(await order.evaluate(e=>e===document.activeElement));
    await p.locator('.hero-btn-secondary').click();await p.waitForURL('**/#customers-section');
    // Observe real anchors while preventing both navigation and external requests.
    await p.evaluate(()=>{window.designIntents=[];document.addEventListener('click',e=>{const a=e.target.closest('a[href^="https://wa.me/"]');if(a){e.preventDefault();window.designIntents.push(a.href)}},true)});
    const actions=p.locator('main a[href^="https://wa.me/"]');assert.equal(await actions.count(),2);
    for(const a of await actions.all()){await a.click();const u=new URL(await a.getAttribute('href'));assert.equal(u.pathname,'/250787411501');assert(u.searchParams.get('text').includes('inspiration photo'));assert((await a.boundingBox()).height>=44);}
    assert.equal(await p.evaluate(()=>window.designIntents.length),2);
    assert.equal(await p.locator('.home-collection-card').count(),4);assert.equal(await p.locator('.service-card').count(),7);
    assert((await p.locator('.home-benefits').textContent()).includes('subject to capacity'));
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
  console.log('PASS: seven ordered sections, two safe WhatsApp design intents, working existing destinations, decoded photographs, single-row disclosure menu with keyboard/Escape/outside close and no-JS fallback, no overflow/errors/missing assets at seven widths.');
}finally{await b.close()}})().catch(e=>{console.error(e);process.exitCode=1});
