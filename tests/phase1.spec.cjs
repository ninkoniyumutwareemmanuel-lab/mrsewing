/* Run with a local server on port 8000 and Playwright available to Node. */
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const base = process.env.REVIEW_BASE_URL || 'http://127.0.0.1:8000/';
(async () => {
  const browser = await chromium.launch({ executablePath:process.env.CHROMIUM_PATH || '/usr/bin/chromium', args:['--no-sandbox'] });
  try {
    const context = await browser.newContext();
    // Every external request is intercepted. No real forms or messages are sent.
    await context.route('**/*', route => new URL(route.request().url()).origin === new URL(base).origin ? route.continue() : route.abort());
    const page = await context.newPage();
    const errors = [], missing = [];
    page.on('pageerror', error => errors.push(error.message));
    page.on('response', response => { if (response.url().startsWith(base) && response.status() >= 400) missing.push(response.url()); });
    const fullPages = fs.readdirSync(root).filter(file => file.endsWith('.html') && /<html\b/i.test(fs.readFileSync(path.join(root, file), 'utf8')));
    let references = 0;
    for (const file of fullPages) {
      await page.goto(base + file);
      await page.waitForFunction(() => document.querySelector('header nav a'));
      await page.waitForTimeout(100);
      const urls = await page.locator('a[href], img[src], source[src], video[poster], script[src], link[rel="stylesheet"]').evaluateAll(nodes => nodes.flatMap(node => {
        const attr = node.tagName === 'A' ? 'href' : node.tagName === 'VIDEO' ? 'poster' : node.tagName === 'LINK' ? 'href' : 'src';
        const raw = node.getAttribute(attr);
        if (!raw || raw.startsWith('#')) return [];
        return [new URL(raw, document.baseURI).href];
      }));
      for (const url of urls) {
        if (new URL(url).origin !== new URL(base).origin) continue;
        const response = await context.request.get(url);
        assert(response.ok(), `${file}: ${url}: ${response.status()}`); references++;
      }
      assert.equal(await page.locator('.customer-actions').count(), 0, file + ' has no extra navigation row');
      const missingAnchors = await page.locator('a[href]').evaluateAll(links => links.flatMap(a => {
        const url = new URL(a.href);
        if (url.origin !== location.origin || url.pathname !== location.pathname || !url.hash || url.hash === '#') return [];
        return document.getElementById(decodeURIComponent(url.hash.slice(1))) ? [] : [url.href];
      }));
      assert.deepEqual(missingAnchors, [], file + ' in-page anchors');
    }
    console.log(`PASS: ${fullPages.length} complete pages; ${references} rendered local references resolve.`);
    const sitemap = fs.readFileSync(path.join(root, 'sitemap.xml'), 'utf8');
    assert.equal((sitemap.match(/<loc>https:\/\/mrsewingfashion\.com\/<\/loc>/g) || []).length, 1);
    assert(!sitemap.includes('https://mrsewingfashion.com/index.html'));
    for (const pathname of ['', 'index.html']) {
      await page.goto(base + pathname);
      const home = page.locator('header nav a[href="/"]');
      await home.waitFor();
      assert.equal(await home.getAttribute('aria-current'), 'page');
      assert.equal(await page.locator('head link[rel="canonical"]').count(), 1);
      assert.equal(await page.locator('head link[rel="canonical"]').getAttribute('href'), 'https://mrsewingfashion.com/');
    }
    await page.goto(base + 'mensuits.html');
    await page.locator('header nav a[href="/"]').click();
    await page.waitForURL(base);
    await page.goto(base + 'mensuits.html');
    await page.goto(base + 'mensuits/#orderModal');
    await page.waitForURL(base + '#orderModal');
    assert(await page.locator('#orderModal').evaluate(el => el.classList.contains('open')));
    console.log('PASS: root-only sitemap homepage, root Home navigation, active states for / and /index.html, and order-modal fallback.');
    for (const file of ['suits.html','mensuits.html','womensuits.html','reviews.html']) {
      await page.goto(base + file);
      const trigger = page.locator('.design-preview').first(); await trigger.click();
      const dialog = page.locator('.design-dialog');
      assert(await dialog.evaluate(d => d.open));
      await dialog.locator('img').evaluate(img => img.decode());
      assert(await dialog.locator('img').evaluate(img => img.complete && img.naturalWidth > 0));
      assert((await dialog.locator('.design-enquiry').getAttribute('href')).startsWith('https://wa.me/250787411501?text='));
      await page.keyboard.press('Shift+Tab');
      assert(await dialog.evaluate(d => d.contains(document.activeElement)), 'modal focus stays inside');
      await page.keyboard.press('Escape');
      assert(await trigger.evaluate(el => document.activeElement === el));
    }
    await page.goto(base + 'reviews.html');
    await page.locator('[data-design-image=" r24.jpeg"]').first().click();
    await page.locator('.design-photo').evaluate(img => img.decode());
    assert(await page.locator('.design-photo').evaluate(img => img.complete && img.naturalWidth > 0));
    console.log('PASS: four galleries, modal focus, Escape, return focus, and leading-space photograph.');
    await page.keyboard.press('Escape');
    await page.goto(base + 'mensuits.html');
    await page.locator('.view-details-btn').first().click();
    await page.locator('#design-details summary').click();
    await page.locator('.design-booking').click();
    assert((await page.locator('input[name="Selected Design"]').inputValue()).includes('MS-'));
    assert.equal(await page.locator('input[name="Selected Photograph"]').inputValue(),'/m1.jpeg');
    console.log('PASS: selected design is retained when booking a consultation.');
    await page.setViewportSize({width:390,height:844});
    for (const file of ['index.html','happy-customers.html']) {
      await page.goto(base + file);
      await page.locator('#slideRight').click();
      await page.waitForFunction(() => document.getElementById('customersSlider').scrollLeft > 0);
    }
    console.log('PASS: customer slider works on the homepage and standalone customer gallery.');
    const responsive = ['index.html','suits.html','mensuits.html','womensuits.html','reviews.html','collections.html','booking.html','measurement-submission.html'];
    for (const width of [320,375,390,768,1024,1440]) {
      await page.setViewportSize({width,height:900});
      for (const file of responsive) {
        await page.goto(base + file);await page.waitForFunction(() => document.querySelector('header nav a'));
        assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), `${file} overflow at ${width}`);
      }
    }
    console.log('PASS: 48 page/viewport combinations without horizontal page overflow.');
    await page.goto(base + 'suits.html');
    await page.evaluate(() => { localStorage.setItem('featuredSuits_date',new Date().toLocaleDateString('en-CA',{timeZone:'Africa/Kigali'}));localStorage.setItem('featuredSuits_arr','invalid JSON'); });
    await page.reload();assert.equal(await page.locator('.gallery-card').count(),30);
    await page.addInitScript(() => { Object.defineProperty(window,'localStorage',{get(){throw new Error('Storage unavailable');}}); });
    await page.reload();assert.equal(await page.locator('.gallery-card').count(),30);
    console.log('PASS: gallery survives corrupted and unavailable storage.');
    await page.close();
    const forms = await context.newPage();
    forms.on('pageerror', error => errors.push(error.message));
    async function prepare(file) {
      await forms.goto(base + file);
      await forms.locator('#fullName').fill('Phase 1 QA — mock only');
      await forms.locator('#phone').fill('+250780000000');
      for (const input of await forms.locator('input[required]:not([type="checkbox"])').all()) {
        const type = await input.getAttribute('type');
        if (type === 'date') await input.fill(await input.getAttribute('min'));
        else if (!(await input.inputValue())) await input.fill(type === 'email' ? 'qa@example.invalid' : 'Mock validation');
      }
      for (const select of await forms.locator('select[required]').all()) {
        const value = await select.locator('option').evaluateAll(options => options.find(option => option.value && !option.disabled)?.value);
        if (value) await select.selectOption(value);
      }
      if (file === 'measurement-submission.html') await forms.locator('#standardSize').selectOption({index:1});
      await forms.locator('#agreeTerms, #formTermsAgree').check();
    }
    for (const file of ['booking.html','booking-adjustment.html','booking-housecall.html','booking-workplace.html','measurement-submission.html']) {
      for (const scenario of ['success','rejection','missing-success','http-error','malformed','network']) {
        let count=0;
        await forms.route('https://api.web3forms.com/submit',async route => {
          count++;
          const data=route.request().postDataJSON();assert(data.access_key);assert(!data.apikey);
          if (scenario==='network') return route.abort();
          await route.fulfill({status:scenario==='http-error'?500:200,contentType:'application/json',body:scenario==='malformed'?'not JSON':JSON.stringify(scenario==='missing-success'?{}:{success:scenario!=='rejection'})});
        });
        await prepare(file);
        const submit=forms.locator('button[type="submit"]');await submit.click();
        if(scenario==='success') await forms.locator('#successBox').waitFor({state:'visible'});
        else { await forms.getByRole('status').filter({hasText:'We could not confirm'}).waitFor();assert(await submit.isEnabled());assert.equal(await forms.locator('#fullName').inputValue(),'Phase 1 QA — mock only'); }
        assert.equal(count,1);await forms.unroute('https://api.web3forms.com/submit');
      }
      let count=0,release;
      const held=new Promise(resolve=>release=resolve);
      await forms.route('https://api.web3forms.com/submit',async route=>{count++;await held;await route.fulfill({contentType:'application/json',body:'{"success":true}'});});
      await prepare(file);await forms.locator('button[type="submit"]').click();
      await forms.waitForFunction(()=>document.querySelector('form').getAttribute('aria-busy')==='true');
      await forms.locator('#agreeTerms, #formTermsAgree').uncheck();await forms.locator('#agreeTerms, #formTermsAgree').check();
      assert(await forms.locator('button[type="submit"]').isDisabled());
      await forms.locator('form').evaluate(form=>form.dispatchEvent(new Event('submit',{bubbles:true,cancelable:true})));
      release();await forms.locator('#successBox').waitFor({state:'visible'});assert.equal(count,1);await forms.unroute('https://api.web3forms.com/submit');
    }
    console.log('PASS: 30 mocked submission outcomes and duplicate-request/consent protection on all five forms.');
    await prepare('measurement-submission.html');await forms.locator('#standardSize').selectOption({index:0});
    await forms.locator('button[type="submit"]').click();await forms.getByRole('status').filter({hasText:'Please provide a standard size'}).waitFor();
    assert(await forms.locator('#standardSize').evaluate(el=>document.activeElement===el));
    await prepare('booking.html');await forms.locator('#phone').fill('letters');
    assert.equal(await forms.locator('#phone').evaluate(el=>el.validity.valid),false);
    await forms.clock.install();
    await forms.locator('#phone').fill('+250780000000');
    await forms.evaluate(()=>{window.fetch=(url,options)=>new Promise((resolve,reject)=>options.signal.addEventListener('abort',()=>reject(new DOMException('Aborted','AbortError'))));});
    await forms.locator('button[type="submit"]').click();await forms.clock.fastForward(21000);
    await forms.getByRole('status').filter({hasText:'timed out'}).waitFor();
    assert(await forms.locator('button[type="submit"]').isEnabled());
    console.log('PASS: measurement minimum, invalid phone rejection and timeout recovery.');
    assert.deepEqual(errors,[]);assert.deepEqual(missing,[]);
    console.log('PASS: no JavaScript page errors or local missing-resource responses. External services were blocked/mocked.');
  } finally {await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
