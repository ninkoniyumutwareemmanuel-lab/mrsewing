/* Actual local service navigation; every external handoff is intercepted. */
const fs = require('node:fs'), path = require('node:path'), assert = require('node:assert/strict');
function library() {
  for (const name of ['playwright', 'playwright-core', '/workspace/tools/phase1/node_modules/playwright-core']) {
    try { return require(name); } catch (e) { if (e.code !== 'MODULE_NOT_FOUND') throw e; }
  }
  throw Error('Install the existing Playwright browser test dependency.');
}
const {chromium} = library(), root = path.resolve(__dirname, '..');
const base = process.env.REVIEW_BASE_URL || 'http://127.0.0.1:8020';
const out = process.env.REVIEW_ARTIFACTS || '/tmp/mrsewing-service-landings';
const cfg = JSON.parse(fs.readFileSync(path.join(root, '_data/service-contact-actions.json')));
const business = JSON.parse(fs.readFileSync(path.join(root, '_data/business.json')));
const phone = business.telephone.replace(/\D/g, '');
const widths = [320, 390, 768, 1440];
const result = {layer: 'local Chromium, external handoffs mocked', widths, pages: [], errors: [], missing: [], handoffs: [], accessibility: [], realMessages: false, realSubmissions: false};
(async () => {
  fs.mkdirSync(out, {recursive:true});
  const launch = {args:['--no-sandbox']};
  const binary = process.env.CHROMIUM_BINARY || (fs.existsSync('/usr/bin/chromium') ? '/usr/bin/chromium' : null);
  if (binary) launch.executablePath = binary;
  const browser = await chromium.launch(launch);
  try {
    const context = await browser.newContext({viewport:{width:390, height:900}, reducedMotion:'reduce', timezoneId:'Africa/Kigali'});
    await context.route('**/*', async route => {
      const request = route.request(), url = new URL(request.url());
      if (url.hostname === 'wa.me') {
        result.handoffs.push(url.href);
        return route.fulfill({status:200, contentType:'text/html', body:'<!doctype html><title>Mock WhatsApp</title><p>External handoff intercepted; no message sent.</p>'});
      }
      if (url.origin !== new URL(base).origin || request.method() !== 'GET') return route.abort();
      return route.continue();
    });
    const page = await context.newPage();
    page.on('pageerror', e => result.errors.push({url:page.url(), message:e.message}));
    page.on('response', response => { if (response.url().startsWith(base) && response.status() >= 400) result.missing.push({url:response.url(), status:response.status()}); });
    const visit = async url => page.goto(new URL(url, base).href, {waitUntil:'load'});
    const overflow = async () => assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), 'horizontal overflow at ' + page.url());
    for (const width of widths) {
      await page.setViewportSize({width, height:900});
      for (const id of ['alterations', 'garment-care', 'mobile-fitting', 'vip']) {
        await visit('/services/' + id + '/');
        await page.locator('.service-overview').waitFor();
        await overflow();
        assert.equal(await page.locator('main h1').count(), 1);
        assert.equal(await page.locator('.service-hero-actions a').count(), 1);
        const hero = page.locator('.service-hero-actions a');
        assert.equal(await hero.innerText(), 'Contact Us on WhatsApp');
        assert.equal(await page.locator('.service-hero-photo img').evaluate(image => image.complete && image.naturalWidth > 0), true);
        assert(!/VIP Subscription|being developed/.test(await page.locator('.service-overview').innerText()));
        if (id === 'mobile-fitting') {
          assert.equal(await page.locator('.service-comparison article').count(), 3);
          for (const text of ['Order Measurement Visit', 'Consultation & Fitting', 'Independent Tailoring Assistance', 'five people and three hours']) assert((await page.locator('main').innerText()).includes(text), text);
        }
        if (id === 'alterations' || id === 'garment-care') {
          assert.equal(await page.locator('.service-combined a').innerText(), 'Contact Us on WhatsApp');
          assert((await page.locator('.service-combined').innerText()).includes('not charged twice'));
        }
        await page.screenshot({path:path.join(out, id + '-' + width + '.png'), fullPage:true});
        if (width === 390) {
          const axe = process.env.AXE_SCRIPT || '/workspace/tools/homepage-qa/node_modules/axe-core/axe.min.js';
          if (fs.existsSync(axe)) {
            await page.addScriptTag({path:axe});
            const findings = await page.evaluate(async () => (await axe.run('main', {runOnly:{type:'tag', values:['wcag2a','wcag2aa','wcag21a','wcag21aa']}})).violations);
            result.accessibility.push({id, violations:findings.map(v => ({id:v.id, impact:v.impact, nodes:v.nodes.map(n => n.target)}))});
          }
        }
        const opened = context.waitForEvent('request', {predicate:r=>new URL(r.url()).hostname==='wa.me'});
        if (width === 320) { await hero.focus(); await page.keyboard.press('Enter'); }
        else await hero.click();
        const whatsappRequest = await opened;
        // A request event precedes navigation commit. Let the intercepted
        // handoff settle before testing return navigation in the same tab.
        await page.waitForURL(url => url.hostname === 'wa.me', {waitUntil:'domcontentloaded'});
        const target = new URL(whatsappRequest.url());
        assert.equal(target.pathname, '/' + phone);
        assert.equal(target.searchParams.get('text'), cfg.messages[id]);
        await visit('/services/' + id + '/');
        const form = page.locator('.service-contact-actions a[href="/request/' + id + '/"]');
        await form.click();
        await page.locator('#mrCustomerFormPopup').waitFor({state:'visible'});
        const existingForm=page.frameLocator('#mrCustomerFormFrame');
        await existingForm.locator('#customerRequestForm').waitFor();
        assert.equal(await existingForm.locator('#customerRequestForm').count(), 1);
        assert(await existingForm.locator('body').evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'existing form overflow');
        await page.locator('.mr-customer-popup-close').click();
        await overflow();
        result.pages.push({id, width, status:'PASS', exactMessage:true, officialDestination:true, retainedForm:true, overflowing:false});
      }
      await visit('/services/custom-tailoring/');
      const card = page.locator('.tailoring-hub-combined');
      await card.scrollIntoViewIfNeeded();
      await overflow();
      await page.screenshot({path:path.join(out, 'combined-' + width + '.png'), fullPage:false});
      assert.equal(await card.locator('a').innerText(), 'Contact Us on WhatsApp');
      const openedCombined = context.waitForEvent('request', {predicate:r=>new URL(r.url()).hostname==='wa.me'});
      await card.locator('a').click();
      const combinedRequest = await openedCombined;
      await page.waitForURL(url => url.hostname === 'wa.me', {waitUntil:'domcontentloaded'});
      assert.equal(new URL(combinedRequest.url()).searchParams.get('text'), cfg.messages.combined);
      result.pages.push({id:'combined-hub', width, status:'PASS', exactMessage:true, officialDestination:true});
    }
    assert.equal(result.errors.length, 0, JSON.stringify(result.errors));
    assert.equal(result.missing.length, 0, JSON.stringify(result.missing));
    assert.equal(result.accessibility.flatMap(row => row.violations).length, 0, JSON.stringify(result.accessibility));
    result.status = 'PASS';
  } catch (error) {
    result.status = 'FAIL'; result.failure = {message:error.message, stack:error.stack}; process.exitCode = 1;
  } finally {
    await browser.close();
    fs.writeFileSync(path.join(out, 'results.json'), JSON.stringify(result, null, 2) + '\n');
    console.log(JSON.stringify(result, null, 2));
  }
})();
