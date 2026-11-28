/* Actual advanced-mode worker contract. Synthetic keys/assets only; no network. */
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { randomBytes, createHash, webcrypto } from 'node:crypto';

if (!globalThis.crypto) globalThis.crypto = webcrypto;
const template = readFileSync(new URL('../_templates/rebuild-preview-worker.js', import.meta.url), 'utf8');
const origin = 'https://mrsewing-staging.pages.dev';
const key = randomBytes(32).toString('base64url');
const verifier = createHash('sha256').update(key).digest('hex');
const base = {
  version: 1, project: 'mrsewing-staging',
  allowedHosts: ['mrsewing-staging.pages.dev'], allowedSuffix: '.mrsewing-staging.pages.dev',
  deniedHosts: ['main.mrsewing-staging.pages.dev', 'mrsewingfashion.com', 'www.mrsewingfashion.com'],
  tokenSha256: verifier, expiresAt: new Date(Date.now() + 30 * 86400000).toISOString(),
  commit: 'a'.repeat(40),
  assets: {
    'index.html': { type: 'text/html; charset=utf-8' },
    'contact/index.html': { type: 'text/html; charset=utf-8' },
    'assets/photo.jpg': { type: 'image/jpeg' },
    'assets/customer-tracking.js': { type: 'text/javascript; charset=utf-8' },
    'terms-and-conditions/index.html': { type: 'text/html; charset=utf-8' },
    'shop/index.html': { type: 'text/html; charset=utf-8' },
    'sitemap.xml': { type: 'application/xml' },
  },
  overrides: {
    'terms-and-conditions/index.html': '<h1>Current effective Terms</h1>',
    'shop/index.html': '<h1>The online Shop is temporarily unavailable.</h1>',
  },
};
let serial = 0;
async function worker(changes = {}) {
  const config = { ...base, ...changes };
  const source = template.replace('/*REBUILD_PREVIEW_CONFIG*/ null', JSON.stringify(config)) + '\n// fixture ' + serial++;
  assert(!source.includes(key), 'raw random review key is never in worker/config');
  return (await import('data:text/javascript;base64,' + Buffer.from(source).toString('base64'))).default;
}
function request(path = '/', options = {}) {
  const { authenticated = false, url, ...init } = options;
  const headers = new Headers(init.headers);
  if (authenticated) headers.set('Cookie', '__Host-ms-preview=' + key);
  return new Request(url || origin + path, { ...init, headers });
}
let assetCalls = 0;
const env = { ASSETS: { fetch: async req => {
  assetCalls++;
  assert.equal(req.method === 'GET' || req.method === 'HEAD', true);
  assert.equal(req.headers.get('If-None-Match'), null);
  assert.equal(req.headers.get('If-Modified-Since'), null);
  return new Response('<!doctype html><html><head><title>Source</title></head><body><h1>Approved source asset</h1></body></html>', { headers: { 'Set-Cookie': 'unsafe=source', 'Cache-Control': 'public,max-age=999999', 'Content-Type': 'text/plain', Vary: 'Accept-Encoding', ETag: 'stale-source-etag', 'Last-Modified': 'Mon, 01 Jan 2024 00:00:00 GMT' } });
} } };
const w = await worker();
function guard(response) {
  assert.match(response.headers.get('X-Robots-Tag'), /noindex.*noarchive/);
  assert.equal(response.headers.get('Cache-Control'), 'private, no-store');
  assert.equal(response.headers.get('Referrer-Policy'), 'no-referrer');
  assert.equal(response.headers.get('X-Content-Type-Options'), 'nosniff');
  assert.match(response.headers.get('Vary'), /Cookie/);
  const csp = response.headers.get('Content-Security-Policy');
  for (const directive of ["connect-src 'self'", "script-src 'self' 'unsafe-inline'", "frame-src 'self'", "form-action 'none'", "object-src 'none'"]) assert(csp.includes(directive));
  assert(!csp.includes('https:'));
}
const checks = [];
async function test(name, run) { await run(); checks.push(name); }

await test('Unauthenticated pages/assets return self-contained private login, no source fetch', async () => {
  for (const path of ['/', '/assets/photo.jpg', '/contact/']) {
    const r = await w.fetch(request(path), env); guard(r); assert.equal(r.status, 401);
    const html = await r.text();
    assert(html.includes('Private Website Preview'));
    assert(!html.includes(verifier)); assert(!html.includes(key));
    assert(!/<script[^>]+src=|<img\b|<iframe\b/.test(html));
    assert(html.includes("history.replaceState(null,'',location.pathname+location.search);open(review)"));
    assert(html.includes("fragment.get('review')"));
  }
  assert.equal(assetCalls, 0);
});

await test('Same-origin bounded JSON review-key exchange sets only secure private authentication', async () => {
  const r = await w.fetch(request('/__preview/session', { method: 'POST', headers: { Origin: origin, 'Content-Type': 'application/json' }, body: JSON.stringify({ review: key }) }), env);
  guard(r); assert.equal(r.status, 200); assert.deepEqual(await r.json(), { authenticated: true, preview: true });
  const cookie = r.headers.get('Set-Cookie');
  for (const part of ['__Host-ms-preview=' + key, 'Secure', 'HttpOnly', 'SameSite=Strict', 'Path=/', 'Max-Age=604800']) assert(cookie.includes(part));
  assert(!cookie.includes('Domain='));
  const r2 = await w.fetch(request('/', { authenticated: true, headers: { 'If-None-Match': 'old-public-page', 'If-Modified-Since': 'Mon, 01 Jan 2024 00:00:00 GMT' } }), env); guard(r2); assert.equal(r2.status, 200);
  const page = await r2.text();
  assert.match(page, /Approved source asset/);
  assert.match(page, /^<!doctype html>/);
  assert.match(page, /Private preview — enquiries and advertising tracking are disabled/);
  assert(page.indexOf('data-ms-private-preview-cleanup') < page.indexOf('<title>'));
  assert(!page.includes(key)); assert(!page.includes(verifier));
  assert.equal(r2.headers.get('ETag'), null); assert.equal(r2.headers.get('Last-Modified'), null);
  assert.equal(r2.headers.get('Set-Cookie'), null);
  assert.equal(r2.headers.get('Content-Type'), 'text/html; charset=utf-8');
  assert.match(r2.headers.get('Vary'), /Accept-Encoding, Cookie/);
});

await test('Wrong origin, malformed/oversized body, wrong/public-hash key and duplicate cookies never authenticate', async () => {
  const samples = [
    { origin: 'https://evil.invalid', body: JSON.stringify({ review: key }), status: 403 },
    { origin, body: JSON.stringify({ review: randomBytes(32).toString('base64url') }), status: 401 },
    { origin, body: JSON.stringify({ review: verifier }), status: 401 },
    { origin, body: JSON.stringify({ review: key, extra: 'not accepted' }), status: 401 },
    { origin, body: '{', status: 400 },
    { origin, body: 'x'.repeat(513), status: 400 },
    { origin, body: JSON.stringify({ review: key }), type: 'text/plain', status: 400 },
  ];
  for (const sample of samples) {
    const r = await w.fetch(request('/__preview/session', { method: 'POST', headers: { Origin: sample.origin, 'Content-Type': sample.type || 'application/json' }, body: sample.body }), env);
    guard(r); assert.equal(r.status, sample.status); assert.equal(r.headers.get('Set-Cookie'), null); assert.equal((await r.json()).authenticated, false);
  }
  for (const cookie of ['__Host-ms-preview=' + verifier, '__Host-ms-preview=' + key + '; __Host-ms-preview=' + key, '__Host-ms-preview=invalid']) {
    const r = await w.fetch(request('/', { headers: { Cookie: cookie } }), env); assert.equal(r.status, 401);
  }
});

await test('Main/live/foreign/HTTP hosts and expired/missing configuration fail closed without ASSETS', async () => {
  const before = assetCalls;
  for (const url of ['https://main.mrsewing-staging.pages.dev/', 'https://mrsewingfashion.com/', 'https://www.mrsewingfashion.com/', 'https://evil.invalid/', 'https://evil.mrsewing-staging.pages.dev.evil.invalid/', 'https://a.b.mrsewing-staging.pages.dev/', 'http://mrsewing-staging.pages.dev/']) {
    const r = await w.fetch(request('/', { url, authenticated: true }), env); guard(r); assert.equal(r.status, 503);
  }
  for (const changes of [{ expiresAt: new Date(Date.now() - 1000).toISOString() }, { tokenSha256: '' }, { assets: null }, { project: 'production' }, { allowedSuffix: '.evil.invalid' }]) {
    const broken = await worker(changes); const r = await broken.fetch(request('/', { authenticated: true }), env); guard(r); assert.equal(r.status, 503);
  }
  const missing = (await import('data:text/javascript;base64,' + Buffer.from(template).toString('base64'))).default;
  assert.equal((await missing.fetch(request('/'), env)).status, 503);
  assert.equal(assetCalls, before);
  const branch = await w.fetch(request('/', { url: 'https://phase1-customer-journey-repairs.mrsewing-staging.pages.dev/', authenticated: true }), env);
  assert.equal(branch.status, 200);
});

await test('Every public API or non-authentication write returns honest503, never provider or asset dispatch', async () => {
  const before = assetCalls;
  for (const method of ['GET', 'HEAD', 'POST', 'PUT', 'PATCH', 'DELETE', 'OPTIONS']) {
    for (const path of ['/api', '/api/selected-design-request', '/api/shop-request', '/%61pi/customer-requests']) {
      const r = await w.fetch(request(path, { method, authenticated: true }), env); guard(r); assert.equal(r.status, 503);
      if (method !== 'HEAD') { const data = await r.json(); assert.equal(data.success, false); assert.equal(data.preview, true); assert.match(data.error, /No request was submitted/); }
      else assert.equal(await r.text(), '');
    }
  }
  for (const path of ['/', '/contact/', '/request/']) {
    const r = await w.fetch(request(path, { method: 'POST', authenticated: true }), env); assert.equal(r.status, 503); assert.equal((await r.json()).success, false);
  }
  assert.equal(assetCalls, before);
});

await test('Private/hidden/encoded/traversal/source paths404 even with an accidentally allowlisted source', async () => {
  const before = assetCalls;
  const unsafe = await worker({ assets: { ...base.assets, '_data/business.json': { type: 'application/json' }, 'assets/private.map': { type: 'application/json' } } });
  for (const path of ['/_data/business.json', '/%5fdata/business.json', '/%255fdata/business.json', '/docs/test.html', '/%64ocs/test.html', '/staff/', '/.git/config', '/_worker.js', '/_headers', '/functions/api/shop-request.js', '/runtime/a.js', '/assets/private.map', '/%252e%252e/docs/private', '/assets/%255csecret', '/%00', '/%E0%A4%A']) {
    const r = await unsafe.fetch(request(path, { authenticated: true }), env); guard(r); assert.equal(r.status, 404, path);
  }
  assert.equal(assetCalls, before);
});

await test('Allowlist, query-preserving directory redirects, effective Terms and Shop hold protect source history', async () => {
  const redirect = await w.fetch(request('/contact?utm_source=google&gclid=synthetic', { authenticated: true }), env);
  guard(redirect); assert.equal(redirect.status, 301); assert.equal(redirect.headers.get('Location'), '/contact/?utm_source=google&gclid=synthetic');
  const before = assetCalls;
  for (const [path, expected] of [['/terms-and-conditions/', 'Current effective Terms'], ['/shop/', 'temporarily unavailable']]) {
    const r = await w.fetch(request(path, { authenticated: true }), env); guard(r); assert.equal(r.status, 200); assert((await r.text()).includes(expected));
  }
  assert.equal(assetCalls, before, 'overrides do not call existing PDF/Shop runtime');
  for (const path of ['/Mr_Sewing_Fashion_Terms_and_Conditions_v1_Approved.pdf', '/unpublished-photo.jpg', '/unknown/']) {
    const r = await w.fetch(request(path, { authenticated: true }), env); guard(r); assert.equal(r.status, 404);
  }
  const head = await w.fetch(request('/contact/', { method: 'HEAD', authenticated: true }), env); assert.equal(head.status, 200); assert.equal(await head.text(), '');
  const robots = await w.fetch(request('/robots.txt'), env); guard(robots); assert.equal(robots.status, 200); assert.match(await robots.text(), /Disallow: \/\n/);
});

await test('Asset errors cannot bypass isolation and redirects never leave the review origin', async () => {
  const external = { ASSETS: { fetch: async () => new Response(null, { status: 302, headers: { Location: 'https://mrsewingfashion.com/contact/', 'Set-Cookie': 'unsafe=1' } }) } };
  const r = await w.fetch(request('/', { authenticated: true }), external); guard(r); assert.equal(r.status, 503); assert.equal(r.headers.get('Location'), null); assert.equal(r.headers.get('Set-Cookie'), null);
  const internal = { ASSETS: { fetch: async () => new Response(null, { status: 302, headers: { Location: '/contact/?utm_source=synthetic' } }) } };
  const allowed = await w.fetch(request('/', { authenticated: true }), internal); guard(allowed); assert.equal(allowed.status, 302); assert.equal(allowed.headers.get('Location'), '/contact/?utm_source=synthetic');
  const denied = { ASSETS: { fetch: async () => new Response(null, { status: 302, headers: { Location: '/_data/business.json' } }) } };
  assert.equal((await w.fetch(request('/', { authenticated: true }), denied)).status, 503);
  assert.equal((await w.fetch(request('/', { authenticated: true }), {})).status, 503);
  const failure = { ASSETS: { fetch: async () => { throw Error('sensitive internal failure'); } } };
  const failed = await w.fetch(request('/', { authenticated: true }), failure); guard(failed); assert.equal(failed.status, 503); assert(!(await failed.text()).includes('sensitive'));
});

console.log('PASS ' + checks.length + ' advanced preview-worker groups: authenticated assets, fragment/session contract, source isolation, API503, policy/Shop overrides, exact hosts, expiry, redirects and tracking CSP. Synthetic keys only; no provider/vendor requests.');
