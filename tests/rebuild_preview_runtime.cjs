/* Workerd + Chromium review isolation. Synthetic key; no provider/vendor traffic.
 * Uses the actual compiled _worker.js and real approved static files. The only
 * substituted deployment input is the review-key verifier (never the real key).
 */
'use strict';
const fs = require('node:fs'), path = require('node:path'), assert = require('node:assert/strict');
const { randomBytes, createHash } = require('node:crypto');
const ROOT = path.resolve(__dirname, '..');
const ORIGIN = 'https://mrsewing-staging.pages.dev';
const OUT = process.env.REVIEW_ARTIFACTS || '/workspace/mrsewing-rebuild-records/2026-11-28/hosted-preview/runtime';
function dependency(names) {
  for (const name of names) {
    try { return require(name); }
    catch (error) { if (error.code !== 'MODULE_NOT_FOUND') throw error; }
  }
  throw Error('The existing local browser/runtime test dependency is unavailable.');
}
const { Miniflare, convertV4MiniflareOptions } = dependency([
  'miniflare', '/home/agent/.npm/_npx/32026684e21afda6/node_modules/miniflare',
]);
const { chromium } = dependency(['playwright', 'playwright-core', '/workspace/tools/phase1/node_modules/playwright-core']);
const compiled = fs.readFileSync(path.join(ROOT, '_worker.js'), 'utf8');
const match = compiled.match(/const CONFIG = ([\s\S]+?);\nconst COOKIE =/);
assert(match, 'Generate the isolated preview worker before running runtime QA.');
const configuration = JSON.parse(match[1]);
const syntheticKey = randomBytes(32).toString('base64url');
const syntheticVerifier = createHash('sha256').update(syntheticKey).digest('hex');
const script = compiled.replace(configuration.tokenSha256, syntheticVerifier);
assert(!script.includes(syntheticKey));
const report = {
  layer: 'Local native Workerd/Miniflare and intercepted Chromium HTTPS; actual compiled worker/static files, synthetic verifier only',
  sourceCommit: configuration.commit || null,
  tests: [], views: [], errors: [], unexpectedMissing: [], externalBrowserAttempts: [],
  outboundWorkerCalls: 0, realSubmissions: false, actualCloudflareDeployment: 'NOT TESTED', providerReceipt: 'NOT TESTED',
};
let runtime, browser, page, assetCalls = 0;
const dispatched = [];
function assetPath(raw) {
  const url = new URL(raw);
  let relative = decodeURIComponent(url.pathname).replace(/^\/+/, '');
  if (!relative || relative.endsWith('/')) relative += 'index.html';
  const target = path.resolve(ROOT, relative);
  assert(target.startsWith(ROOT + path.sep), 'Test ASSETS path escapes checkout.');
  assert(Object.hasOwn(configuration.assets, relative), 'Worker must reject source/unlisted files before ASSETS dispatch.');
  return { relative, target };
}
async function assets(request) {
  assetCalls++;
  assert(['GET', 'HEAD'].includes(request.method), 'Writes never reach ASSETS.');
  const { relative, target } = assetPath(request.url);
  if (!fs.existsSync(target) || !fs.statSync(target).isFile()) return new Response('Missing fixture asset', { status: 404 });
  return new Response(request.method === 'HEAD' ? null : fs.readFileSync(target), {
    headers: { 'Content-Type': configuration.assets[relative].type, 'Cache-Control': 'public,max-age=31536000' },
  });
}
async function dispatch(url, init = {}) {
  dispatched.push({ method: init.method || 'GET', path: new URL(url).pathname });
  return runtime.dispatchFetch(url, { ...init, redirect: 'manual' });
}
function guard(response) {
  assert.match(response.headers.get('x-robots-tag'), /noindex.*noarchive/);
  assert.match(response.headers.get('cache-control'), /no-store/);
  assert.equal(response.headers.get('referrer-policy'), 'no-referrer');
  assert.match(response.headers.get('content-security-policy'), /connect-src 'self'/);
  assert.match(response.headers.get('content-security-policy'), /form-action 'none'/);
}
async function check(name, run) {
  await run(); report.tests.push({ name, status: 'PASS' });
}
(async () => {
  fs.mkdirSync(OUT, { recursive: true });
  runtime = new Miniflare(convertV4MiniflareOptions({
    modules: true, script, compatibilityDate: '2026-11-01', host: '127.0.0.1', port: 0,
    serviceBindings: { ASSETS: assets },
    outboundService: async () => {
      report.outboundWorkerCalls++;
      return new Response('External requests are disabled in this isolated test.', { status: 503 });
    },
  }));
  await runtime.ready;
  try {
    await check('Native Workerd denies guests/private source and protects Main/live/foreign hosts', async () => {
      const before = assetCalls;
      const guest = await dispatch(ORIGIN + '/'); guard(guest); assert.equal(guest.status, 401);
      assert((await guest.text()).includes('Private Website Preview'));
      const image = Object.keys(configuration.assets).find(name => /\.(?:webp|jpe?g|png)$/.test(name));
      assert(image); const privateImage = await dispatch(ORIGIN + '/' + image); guard(privateImage); assert.equal(privateImage.status, 401);
      for (const suffix of ['/_data/business.json', '/%255fdata/business.json', '/docs/WEBSITE_SOURCE_MAP.md', '/_worker.js']) {
        const denied = await dispatch(ORIGIN + suffix); guard(denied); assert.equal(denied.status, 404);
      }
      const robots = await dispatch(ORIGIN + '/robots.txt'); guard(robots); assert.equal(robots.status, 200); assert.match(await robots.text(), /Disallow: \/\n/);
      for (const host of ['main.mrsewing-staging.pages.dev', 'mrsewingfashion.com', 'www.mrsewingfashion.com', 'foreign.invalid']) {
        const denied = await dispatch('https://' + host + '/'); guard(denied); assert.equal(denied.status, 503);
      }
      assert.equal(assetCalls, before);
    });
    browser = await chromium.launch({ executablePath: process.env.CHROMIUM_BINARY || '/usr/bin/chromium', args: ['--no-sandbox'] });
    const context = await browser.newContext({ viewport: { width: 390, height: 900 }, reducedMotion: 'reduce' });
    await context.route('**/*', async route => {
      const request = route.request(), url = new URL(request.url());
      if (url.origin !== ORIGIN) {
        report.externalBrowserAttempts.push({ origin: url.origin, path: url.pathname, method: request.method(), action: 'ABORTED BEFORE NETWORK' });
        return route.abort();
      }
      const headers = await request.allHeaders();
      const body = ['GET', 'HEAD'].includes(request.method()) ? undefined : request.postDataBuffer();
      const response = await dispatch(request.url(), { method: request.method(), headers, body });
      const outgoing = Object.fromEntries(response.headers);
      delete outgoing['transfer-encoding']; delete outgoing.connection;
      await route.fulfill({ status: response.status, headers: outgoing, body: Buffer.from(await response.arrayBuffer()) });
    });
    page = await context.newPage();
    page.on('pageerror', error => report.errors.push(error.message));
    page.on('response', response => {
      const url = new URL(response.url());
      if (url.origin === ORIGIN && response.status() >= 400 && !['/', '/__preview/session'].includes(url.pathname) && !url.pathname.startsWith('/api/')) {
        report.unexpectedMissing.push({ path: url.pathname, status: response.status() });
      }
    });
    await check('Phone fragment link authenticates through actual Worker, sets secure HttpOnly cookie and erases key', async () => {
      try { await page.goto(ORIGIN + '/#review=' + syntheticKey, { waitUntil: 'domcontentloaded' }); }
      catch (error) { if (!/ERR_ABORTED/.test(error.message)) throw error; }
      await page.locator('#hero-title').waitFor({ state: 'visible' });
      await page.waitForURL(url => url.pathname === '/' && !url.hash);
      const cookie = (await context.cookies(ORIGIN)).find(item => item.name === '__Host-ms-preview');
      assert(cookie); assert.equal(cookie.secure, true); assert.equal(cookie.httpOnly, true); assert.equal(cookie.sameSite, 'Strict');
      assert.equal(await page.evaluate(() => document.cookie.includes('__Host-ms-preview')), false);
      assert.equal(await page.locator('[data-ms-private-preview-notice]').count(), 1);
      assert.equal(await page.locator('[data-ms-private-preview-notice]').innerText(), 'Private preview — enquiries and advertising tracking are disabled.');
      await page.goto(ORIGIN + '/#review=' + syntheticKey, { waitUntil: 'domcontentloaded' });
      await page.waitForFunction(() => !location.hash);
      assert.equal(await page.locator('[data-ms-private-preview-notice]').count(), 1, 'Reopened authenticated link has one notice.');
    });
    await check('Authenticated mobile/desktop homepage and navigation stay usable under runtime security headers', async () => {
      for (const width of [390, 1440]) {
        await page.setViewportSize({ width, height: 900 });
        const response = await page.goto(ORIGIN + '/', { waitUntil: 'load' });
        assert.equal(response.status(), 200); assert.match(response.headers()['x-robots-tag'], /noindex/);
        assert.equal(await page.locator('.tailoring-primary-card').count(), 4);
        assert.equal(await page.locator('#home-navigation>ul>li').count(), 7);
        assert.equal(await page.locator('header a[href^="/shop/"],footer a[href^="/shop/"]').count(), 0);
        assert(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
        await page.locator('.tailoring-feature-photo').scrollIntoViewIfNeeded();
        await page.locator('.tailoring-feature-photo img').evaluate(image => image.decode());
        assert.equal(await page.locator('.tailoring-feature-photo img').evaluate(image => getComputedStyle(image).objectFit), 'contain');
        await page.evaluate(() => scrollTo(0, 0));
        await page.screenshot({ path: path.join(OUT, 'runtime-homepage-' + width + '.png') });
        if (width === 390) {
          await page.locator('.home-menu-toggle').click();
          assert.equal(await page.locator('.home-menu-toggle').getAttribute('aria-expanded'), 'true');
          await page.screenshot({ path: path.join(OUT, 'runtime-navigation-390.png') });
          await page.keyboard.press('Escape');
          assert.equal(await page.locator('.home-menu-toggle').getAttribute('aria-expanded'), 'false');
        }
        report.views.push({ width, status: 'PASS', httpStatus: 200, noindex: true });
      }
    });
    await check('General quotation and selected-design/fabric dialogs work without submission permissions', async () => {
      await page.setViewportSize({ width: 390, height: 900 }); await page.goto(ORIGIN + '/', { waitUntil: 'load' });
      await page.locator('#tailoring-final a[href="/request/?general=1"]').click();
      await page.locator('#mrCustomerFormPopup').waitFor({ state: 'visible' });
      await page.frameLocator('#mrCustomerFormFrame').locator('#customerRequestForm').waitFor({ state: 'visible' });
      await page.screenshot({ path: path.join(OUT, 'runtime-general-quote-390.png') });
      await page.locator('#mrCustomerFormPopup button').first().click();
      await page.goto(ORIGIN + '/collections/designs/ms-031/', { waitUntil: 'load' });
      await page.locator('[data-select-design]').click();
      const dialog = page.locator('.tailoring-request-dialog'); await dialog.waitFor({ state: 'visible' });
      const frame = page.frameLocator('.tailoring-dialog-frame');
      await frame.locator('[data-selection-list] article').waitFor({ state: 'visible' });
      await frame.locator('[aria-label^="Increase quantity"]').click();
      assert((await frame.locator('[data-selection-total]').innerText()).includes('2 garments'));
      await page.locator('.tailoring-dialog-close').click();
      await page.locator('.tailoring-resume-request').click();
      assert((await frame.locator('[data-selection-total]').innerText()).includes('2 garments'));
      await page.screenshot({ path: path.join(OUT, 'runtime-selected-resume-390.png') });
      await frame.locator('[data-selected-continue]').click();
      await frame.locator('[name=sharedFabricChoice]').first().waitFor({ state: 'visible' });
      assert.equal(await frame.locator('[name=sharedFabricChoice]').count(), 3);
      await frame.locator('[value=own]').check();
      await frame.locator('#fabricChoiceForm button').click();
      await frame.locator('#customerRequestForm').waitFor({ state: 'visible' });
      await page.screenshot({ path: path.join(OUT, 'runtime-own-fabric-390.png') });
      assert((await frame.locator('[data-quotation-section=order]').innerText()).includes('Use My Own Fabric'));
      assert.equal(await frame.locator('#requestConsent').count(), 1);
      assert.equal(await frame.locator('#requestConsent').isChecked(), false, 'Existing final-step consent remains unchecked, not forced into the first step.');
    });
    await check('Native APIs reject synthetic writes; current Terms and Shop overrides avoid old Functions', async () => {
      const accepted = await dispatch(ORIGIN + '/api/selected-design-request', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ synthetic: true }) });
      guard(accepted); assert.equal(accepted.status, 503); const data = await accepted.json();
      assert.equal(data.success, false); assert.equal(data.preview, true); assert.match(data.error, /No request was submitted/);
      const cookie = '__Host-ms-preview=' + syntheticKey;
      const before = assetCalls;
      for (const route of ['terms-and-conditions', 'shop']) {
        const result = await dispatch(ORIGIN + '/' + route + '/', { headers: { Cookie: cookie } }); guard(result); assert.equal(result.status, 200);
        const expected = configuration.overrides[route + '/index.html']; assert.equal(typeof expected, 'string');
        const main = expected.match(/<main\b[^>]*>[\s\S]*?<\/main>/i)?.[0]; assert(main);
        const html = await result.text(); assert(html.includes(main));
        if (route === 'shop') assert(!html.includes('data-shop-whatsapp-form'));
        if (route === 'terms-and-conditions') assert(!html.includes('termsPdfDialog'));
      }
      assert.equal(assetCalls, before, 'Policy and Shop use approved inline projections, not source runtime.');
    });
    assert.deepEqual(report.errors, []);
    assert.deepEqual(report.unexpectedMissing, []);
    assert.equal(report.outboundWorkerCalls, 0);
    assert(!report.externalBrowserAttempts.some(item => /google|facebook|web3forms|doubleclick|connect\.facebook/i.test(item.origin)), 'No advertising SDK/provider request even attempted by the staged app.');
    assert(dispatched.every(item => item.method === 'GET' || item.method === 'HEAD' || item.path === '/__preview/session' || item.path === '/api/selected-design-request'));
    report.assetsServed = assetCalls;
    report.status = 'PASS';
  } catch (error) {
    report.status = 'FAIL'; report.failure = { message: error.message, stack: error.stack };
    if (page) try { await page.screenshot({ path: path.join(OUT, 'failure.png') }); } catch {}
    process.exitCode = 1;
  } finally {
    await browser?.close(); await runtime?.dispose();
    fs.writeFileSync(path.join(OUT, 'results.json'), JSON.stringify(report, null, 2) + '\n');
    console.log(JSON.stringify(report, null, 2));
  }
})().catch(error => { console.error(error.message); process.exitCode = 1; });
