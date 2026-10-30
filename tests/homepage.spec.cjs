/* Homepage structure/interaction checks. Requires the same local server as phase1.spec.cjs. */
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const root = path.resolve(__dirname, '..');
const base = process.env.REVIEW_BASE_URL || 'http://127.0.0.1:8000/';
(async () => {
  execFileSync('python3', ['scripts/build_homepage.py', '--check'], { cwd:root, stdio:'inherit' });
  const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
  for (const section of ['hero-section','customers-section','services-section','collections-section','process-section','benefits-section','programs-section','final-section']) assert(html.includes(`id="${section}"`));
  assert(!html.includes('loadComponents'));
  assert(!/\bfetch\s*\(/.test(fs.readFileSync(path.join(root, 'assets/homepage.js'), 'utf8')));
  const browser = await chromium.launch({ executablePath:process.env.CHROMIUM_PATH || '/usr/bin/chromium', args:['--no-sandbox'] });
  try {
    const context = await browser.newContext();
    // Never reach WhatsApp, form providers, or any other external service.
    await context.route('**/*', route => new URL(route.request().url()).origin === new URL(base).origin ? route.continue() : route.abort());
    const page = await context.newPage();
    const errors = [], requests = [];
    page.on('pageerror', error => errors.push(error.message));
    page.on('request', request => requests.push({ url:request.url(), type:request.resourceType() }));
    await page.goto(base);
    assert.equal(await page.locator('html').count(), 1);
    assert.equal(await page.locator('head').count(), 1);
    assert.equal(await page.locator('title').count(), 1);
    assert.equal(await page.locator('main').count(), 1);
    assert.equal(await page.locator('h1').count(), 1);
    assert.equal(await page.locator('[data-hero-text="0"]').textContent(), "Crafted for Your Story.");
    assert.equal(await page.locator('link[rel="canonical"]').count(), 1);
    assert.equal(await page.locator('head link[rel="canonical"]').getAttribute('href'), 'https://mrsewingfashion.com/');
    assert.equal(await page.locator('meta[name="description"]').count(), 1);
    assert.equal(await page.locator('meta[property="og:url"]').count(), 1);
    assert.equal(await page.locator('meta[property="og:url"]').getAttribute('content'), 'https://mrsewingfashion.com/');
    assert.equal(await page.locator('body meta, body title, body link, body style, body script').count(), 0);
    assert.equal(await page.locator('script[type="application/ld+json"]').count(), 1);
    const schema = JSON.parse(await page.locator('script[type="application/ld+json"]').textContent());
    assert.equal(schema['@graph'][0]['@id'], 'https://mrsewingfashion.com/#website');
    assert.equal(await page.locator('.service-card').count(), 7);
    assert.equal(await page.locator('.home-collection-card').count(), 4);
    assert.equal(await page.locator('.customer-card-slide').count(), 3);
    assert.equal(await page.locator('header').count(), 1);
    assert.equal(await page.locator('footer').count(), 1);
    assert(await page.evaluate(() => [...document.querySelectorAll('script[src]')].every(script => script.defer)));
    const preload = page.locator('link[rel="preload"][as="image"]');
    assert.equal(await preload.getAttribute('imagesrcset'), await page.locator('.hero-lcp').getAttribute('srcset'));
    assert.equal(await preload.getAttribute('imagesizes'), await page.locator('.hero-lcp').getAttribute('sizes'));
    assert.equal(await preload.getAttribute('fetchpriority'), 'high');
    assert(await page.locator('img').evaluateAll(images => images.every(image => Number(image.getAttribute('width')) > 0 && Number(image.getAttribute('height')) > 0)));
    assert(await page.locator('main img:not([data-hero-slide])').evaluateAll(images => images.every(image => image.loading === 'lazy')));
    assert.equal(await page.locator('header img').getAttribute('loading'), null);
    assert.equal(await page.locator('.hero-lcp').getAttribute('loading'), 'eager');
    assert.equal(await page.locator('.hero-lcp').getAttribute('fetchpriority'), 'high');
    assert.equal(requests.filter(request => ['fetch','xhr'].includes(request.type)).length, 0);
    assert(!requests.some(request => /\/(?:services|collections|header|footer|hero|happy-customers|why-mtm|why-choose)\.html(?:$|\?)/.test(request.url)));
    console.log('PASS: one document/main/H1/canonical; homepage-only metadata; static content; hero preload; image dimensions; deferred scripts; zero runtime HTML fetches.');

    // Test both scroll directions and retain normal visual hover transitions.
    await page.setViewportSize({width:390,height:844});
    await page.locator('#slideRight').click();
    await page.waitForFunction(() => document.getElementById('customersSlider').scrollLeft > 0);
    await page.waitForTimeout(500);
    await page.locator('#slideLeft').click();
    await page.waitForFunction(() => document.getElementById('customersSlider').scrollLeft === 0);
    assert((await page.locator('.service-card').first().evaluate(card => getComputedStyle(card).transitionProperty)).includes('transform'));
    assert.equal(await page.locator('.hero-section a').count(),0);
    assert.equal(await page.locator('[data-hero-text]').count(),2);
    await page.locator('.home-booking-link').click();
    await page.waitForURL('**/booking/');
    await page.goto(base+'?legacy-order-test=1#orderModal');
    // Observe the intended WhatsApp action after the real handlers, then prevent navigation.
    await page.evaluate(() => document.getElementById('whatsappBtn').addEventListener('click', event => {
      window.whatsappIntent = { url:event.currentTarget.href, blockedByConsent:event.defaultPrevented };
      event.preventDefault();
    }));
    assert(await page.locator('#orderModal').evaluate(e=>e.classList.contains('open')));
    await page.locator('#whatsappBtn').click({ force:true });
    assert(await page.evaluate(() => window.whatsappIntent.blockedByConsent));
    await page.locator('#termsAgree').check();
    await page.locator('#whatsappBtn').click();
    const intent = await page.evaluate(() => window.whatsappIntent);
    assert(!intent.blockedByConsent);
    assert(intent.url.startsWith('https://wa.me/250787411501?text='));
    assert(!await page.locator('#orderModal').evaluate(modal => modal.classList.contains('open')));
    console.log('PASS: slider forward/back, hover transitions, booking navigation and WhatsApp consent/intent. No message was sent.');

    const noJS = await browser.newContext({ javaScriptEnabled:false });
    await noJS.route('**/*', route => new URL(route.request().url()).origin === new URL(base).origin ? route.continue() : route.abort());
    const native = await noJS.newPage();
    await native.goto(base);
    await native.locator('h1').waitFor({state:'visible'});
    assert.equal(await native.locator('.service-card').count(), 7);
    assert.equal(await native.locator('.home-collection-card').count(), 4);
    assert.equal(await native.locator('header nav a').count(), 9);
    await native.locator('.image-link').first().click();
    await native.waitForURL('**/collections/?occasion=graduation');
    await noJS.close();
    assert.deepEqual(errors, []);
    console.log('PASS: homepage content, navigation and category links work without JavaScript; no page errors.');
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
