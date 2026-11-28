/* Staging-only advanced-mode Pages worker. Generated configuration is server-side.
 * Main/public request functions are never called by this review deployment.
 * The review key itself must never appear here: only its SHA256 verifier.
 */
const CONFIG = /*REBUILD_PREVIEW_CONFIG*/ null;
const COOKIE = '__Host-ms-preview';
const SESSION_PATH = '/__preview/session';
const KEY_PATTERN = /^[A-Za-z0-9_-]{43}$/;
const MAX_BODY = 512;
const INTERNAL = new Set([
  '_data', '_templates', '_media', 'scripts', 'tests', 'docs', 'functions',
  'staff', 'runtime', 'private', 'attachments', 'artifacts', 'node_modules',
  'mrsewing-rebuild-records', 'masters', 'registers',
]);
const CSP = [
  "default-src 'self'", "script-src 'self' 'unsafe-inline'",
  "style-src 'self' 'unsafe-inline'", "img-src 'self' data: blob:",
  "font-src 'self' data:", "media-src 'self' blob:", "connect-src 'self'",
  "frame-src 'self'", "frame-ancestors 'self'", "form-action 'none'",
  "object-src 'none'", "base-uri 'self'", "worker-src 'none'",
].join('; ');

function headers(extra) {
  const result = new Headers(extra);
  result.set('X-Robots-Tag', 'noindex, nofollow, noarchive, nosnippet');
  result.set('Cache-Control', 'private, no-store');
  result.set('Content-Security-Policy', CSP);
  result.set('X-Content-Type-Options', 'nosniff');
  result.set('Referrer-Policy', 'no-referrer');
  result.set('Permissions-Policy', 'camera=(), microphone=(), geolocation=(), payment=()');
  const vary = result.get('Vary');
  if (!vary || !vary.split(',').some(item => item.trim().toLowerCase() === 'cookie')) {
    result.set('Vary', vary ? vary + ', Cookie' : 'Cookie');
  }
  result.set('X-Mr-Sewing-Rebuild-Preview', '1');
  if (typeof CONFIG?.commit === 'string' && /^[a-f0-9]{40}$/i.test(CONFIG.commit)) {
    result.set('X-Mr-Sewing-Preview-Commit', CONFIG.commit);
  }
  return result;
}

function reply(request, status, body, type = 'text/plain; charset=utf-8', extra) {
  const out = headers(extra);
  out.set('Content-Type', type);
  return new Response(request.method === 'HEAD' ? null : body, { status, headers: out });
}

function json(request, status, value, extra) {
  return reply(request, status, JSON.stringify(value), 'application/json; charset=utf-8', extra);
}

function unavailable(request) {
  return json(request, 503, { success: false, preview: true, error: 'This private preview is unavailable or expired.' });
}

function disabled(request) {
  return json(request, 503, {
    success: false, preview: true,
    error: 'Website preview only: submissions are disabled. No request was submitted.',
  });
}

function configurationReady(url) {
  if (!CONFIG || CONFIG.version !== 1 || CONFIG.project !== 'mrsewing-staging' ||
      !CONFIG.assets || typeof CONFIG.assets !== 'object' || Array.isArray(CONFIG.assets) ||
      !/^[a-f0-9]{64}$/i.test(CONFIG.tokenSha256 || '') ||
      !Array.isArray(CONFIG.allowedHosts) || !Array.isArray(CONFIG.deniedHosts) ||
      CONFIG.allowedSuffix !== '.mrsewing-staging.pages.dev' ||
      url.protocol !== 'https:' || url.username || url.password) return false;
  const expiry = Date.parse(CONFIG.expiresAt);
  if (!Number.isFinite(expiry) || expiry <= Date.now()) return false;
  const host = url.hostname;
  // The existing Main deployment supplies live APIs. It is never a review host.
  if (host === 'main.mrsewing-staging.pages.dev' || host === 'mrsewingfashion.com' ||
      host === 'www.mrsewingfashion.com' || CONFIG.deniedHosts.includes(host)) return false;
  const prefix = host.endsWith(CONFIG.allowedSuffix) ? host.slice(0, -CONFIG.allowedSuffix.length) : '';
  return host === 'mrsewing-staging.pages.dev' && CONFIG.allowedHosts.includes(host) || /^[a-z0-9-]+$/.test(prefix);
}

function decodedPath(url) {
  let path = url.pathname;
  for (let i = 0; i < 8; i++) {
    const decoded = decodeURIComponent(path);
    if (decoded === path) break;
    path = decoded;
    if (i === 7) throw new Error('Too many encodings');
  }
  if (!path.startsWith('/') || path.includes('\\') || /[\x00-\x1f\x7f]/.test(path)) throw new Error('Invalid path');
  const parts = path.split('/').filter(Boolean);
  if (parts.some(part => part === '.' || part === '..')) throw new Error('Traversal');
  return path;
}

function privatePath(path) {
  const parts = path.split('/').filter(Boolean);
  return parts.some(part => part.startsWith('.') || part.startsWith('_') || INTERNAL.has(part.toLowerCase())) ||
    /\.(?:md|py|pyc|env|sqlite|db|map)$/i.test(path);
}

async function matchesKey(value) {
  if (typeof value !== 'string' || !KEY_PATTERN.test(value)) return false;
  const digest = new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(value)));
  const expected = CONFIG.tokenSha256.toLowerCase();
  let difference = 0;
  for (let i = 0; i < digest.length; i++) difference |= digest[i] ^ Number.parseInt(expected.slice(i * 2, i * 2 + 2), 16);
  return difference === 0;
}

async function authenticated(request) {
  const values = (request.headers.get('Cookie') || '').split(';').map(part => part.trim())
    .filter(part => part.startsWith(COOKIE + '='));
  if (values.length !== 1) return false;
  return matchesKey(values[0].slice(COOKIE.length + 1));
}

async function smallJson(request) {
  const length = request.headers.get('Content-Length');
  if (length !== null && (!/^\d+$/.test(length) || Number(length) > MAX_BODY)) throw new Error('Body limit');
  if (!/^application\/json(?:\s*;|$)/i.test(request.headers.get('Content-Type') || '')) throw new Error('Content type');
  if (!request.body) throw new Error('Missing body');
  const reader = request.body.getReader();
  const chunks = [];
  let count = 0;
  try {
    for (;;) {
      const { value, done } = await reader.read();
      if (done) break;
      count += value.byteLength;
      if (count > MAX_BODY) { await reader.cancel(); throw new Error('Body limit'); }
      chunks.push(value);
    }
  } finally { reader.releaseLock(); }
  const buffer = new Uint8Array(count);
  let offset = 0;
  for (const chunk of chunks) { buffer.set(chunk, offset); offset += chunk.byteLength; }
  return JSON.parse(new TextDecoder('utf-8', { fatal: true }).decode(buffer));
}

async function session(request, url) {
  if (request.method !== 'POST') return disabled(request);
  if (request.headers.get('Origin') !== url.origin) return json(request, 403, { authenticated: false, preview: true });
  let body;
  try { body = await smallJson(request); }
  catch { return json(request, 400, { authenticated: false, preview: true }); }
  if (!body || typeof body !== 'object' || Array.isArray(body) || Object.keys(body).length !== 1 || !await matchesKey(body.review)) {
    return json(request, 401, { authenticated: false, preview: true });
  }
  const remaining = Math.floor((Date.parse(CONFIG.expiresAt) - Date.now()) / 1000);
  const maxAge = Math.min(7 * 24 * 60 * 60, remaining);
  if (maxAge <= 0) return unavailable(request);
  return json(request, 200, { authenticated: true, preview: true }, {
    'Set-Cookie': COOKIE + '=' + body.review + '; Secure; HttpOnly; SameSite=Strict; Path=/; Max-Age=' + maxAge,
  });
}

function login(request) {
  return reply(request, 401, `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow,noarchive"><meta name="referrer" content="no-referrer"><link rel="icon" href="data:,"><title>Private Website Preview | Mr Sewing Fashion</title><style>html{color-scheme:dark}*{box-sizing:border-box}body{margin:0;min-height:100svh;display:grid;place-items:center;padding:24px;background:#10100f;color:#f5f0e8;font:16px/1.6 system-ui,sans-serif}main{width:min(100%,440px)}h1{font:400 clamp(28px,6vw,38px)/1.2 Georgia,serif;color:#e1bb65;margin:0 0 18px}p{margin:0 0 20px;color:#ddd5c8}label{display:block;margin:18px 0 6px;font-weight:600}input,button{font:inherit;min-height:48px;width:100%;padding:12px;border-radius:4px}input{border:1px solid #aa8c50;background:#1b1915;color:#fff}button{margin-top:14px;border:0;background:#d4a43b;color:#17130a;font-weight:600;cursor:pointer}button:disabled{opacity:.7;cursor:wait}:focus-visible{outline:3px solid #f4d48f;outline-offset:4px}#status{min-height:26px;margin-top:16px;color:#f0d48f;font-size:14px}</style></head><body><main><h1>Mr Sewing Fashion<br>Private Website Preview</h1><p>This preview is for review only. Customer submissions and advertising tracking are disabled.</p><form id="preview-login"><label for="review-key">Review key</label><input id="review-key" type="password" autocomplete="off" spellcheck="false" autocapitalize="none" maxlength="64" required><button type="submit">Open Preview</button></form><p id="status" role="status" aria-live="polite">Use the private review link supplied in this chat, or enter its review key.</p><noscript><p>JavaScript is required for private preview sign-in.</p></noscript></main><script>(()=>{'use strict';const form=document.getElementById('preview-login'),input=document.getElementById('review-key'),status=document.getElementById('status'),button=form.querySelector('button');let busy=false;async function open(review){if(busy)return;busy=true;button.disabled=true;status.textContent='Opening the private preview…';try{const response=await fetch('${SESSION_PATH}',{method:'POST',credentials:'same-origin',headers:{'Content-Type':'application/json'},body:JSON.stringify({review})});const result=await response.json();if(!response.ok||result.authenticated!==true)throw Error();location.replace(location.pathname+location.search);}catch{status.textContent='The review key is invalid or the preview has expired. Please use the latest private review link.';button.disabled=false;busy=false;input.focus();}}form.addEventListener('submit',event=>{event.preventDefault();open(input.value.trim());});const fragment=new URLSearchParams(location.hash.slice(1)),review=fragment.get('review');if(review){history.replaceState(null,'',location.pathname+location.search);open(review);}})();</script></body></html>`, 'text/html; charset=utf-8');
}

function assetKey(path) {
  const relative = path.replace(/^\/+/, '');
  const key = path.endsWith('/') ? relative + 'index.html' : relative;
  if (Object.hasOwn(CONFIG.assets, key)) return { key };
  if (!path.endsWith('/') && Object.hasOwn(CONFIG.assets, relative + '/index.html')) return { redirect: path + '/' };
  return null;
}

function safeRedirect(location, url) {
  try {
    const target = new URL(location, url);
    if (target.origin !== url.origin) return false;
    const path = decodedPath(target);
    return !privatePath(path) && !!assetKey(path);
  } catch { return false; }
}

function reviewHtml(source) {
  // A previously authenticated visitor may reopen the private fragment link.
  // Remove its key before any existing application script can read/share it.
  const cleanup = `<script data-ms-private-preview-cleanup>(()=>{'use strict';function clean(){try{const fragment=new URLSearchParams(location.hash.slice(1));if(fragment.has('review')){fragment.delete('review');const rest=fragment.toString();history.replaceState(history.state,'',location.pathname+location.search+(rest?'#'+rest:''));}}catch{}}clean();window.addEventListener('hashchange',clean);})();</script>`;
  const notice = '<p data-ms-private-preview-notice role="note" style="margin:0;padding:8px 16px;background:#272015;color:#f1d594;text-align:center;font:14px/1.5 system-ui,sans-serif">Private preview — enquiries and advertising tracking are disabled.</p>';
  if (!source.includes('data-ms-private-preview-cleanup')) {
    if (/<head\b[^>]*>/i.test(source)) source = source.replace(/<head\b[^>]*>/i, match => match + cleanup);
    else if (/^\s*<!doctype[^>]*>/i.test(source)) source = source.replace(/^\s*<!doctype[^>]*>/i, match => match + cleanup);
    else source = cleanup + source;
  }
  if (!source.includes('data-ms-private-preview-notice')) {
    if (/<body\b[^>]*>/i.test(source)) source = source.replace(/<body\b[^>]*>/i, match => match + notice);
    else source += notice;
  }
  return source;
}

async function handle(request, env) {
  const url = new URL(request.url);
  if (!configurationReady(url)) return unavailable(request);
  let path;
  try { path = decodedPath(url); }
  catch { return reply(request, 404, 'Not found.'); }
  if (path === SESSION_PATH) return session(request, url);
  if (!['GET', 'HEAD'].includes(request.method)) return disabled(request);
  if (path === '/api' || path.startsWith('/api/')) return disabled(request);
  if (privatePath(path)) return reply(request, 404, 'Not found.');
  if (path === '/robots.txt') return reply(request, 200, 'User-agent: *\nDisallow: /\n');
  if (!await authenticated(request)) return login(request);
  const selected = assetKey(path);
  if (!selected) return reply(request, 404, 'Not found.');
  if (selected.redirect) return reply(request, 301, '', 'text/plain; charset=utf-8', { Location: selected.redirect + url.search });
  const overrides = CONFIG.overrides || {};
  const type = CONFIG.assets[selected.key].type || 'application/octet-stream';
  const html = /^text\/html(?:;|$)/i.test(type);
  if (Object.hasOwn(overrides, selected.key)) {
    if (typeof overrides[selected.key] !== 'string') return unavailable(request);
    return reply(request, 200, html ? reviewHtml(overrides[selected.key]) : overrides[selected.key], type);
  }
  if (!env?.ASSETS || typeof env.ASSETS.fetch !== 'function') return unavailable(request);
  // A browser may have cached an older, public staging response. Force a fresh
  // asset body rather than accepting304 and reusing pre-review HTML or headers.
  // Range remains intact for native video playback/seek behavior.
  const requestHeaders = new Headers(request.headers);
  for (const name of ['If-None-Match', 'If-Modified-Since', 'If-Match', 'If-Unmodified-Since']) requestHeaders.delete(name);
  if (html) requestHeaders.set('Accept-Encoding', 'identity');
  const assetRequest = new Request(request, { headers: requestHeaders });
  const asset = await env.ASSETS.fetch(assetRequest);
  if (asset.status >= 300 && asset.status < 400) {
    const location = asset.headers.get('Location');
    if (!location || !safeRedirect(location, url)) return unavailable(request);
  }
  const out = headers(asset.headers);
  out.delete('Set-Cookie');
  out.set('Content-Type', type);
  let body = request.method === 'HEAD' ? null : asset.body;
  if (html && asset.status === 200) {
    out.delete('Content-Length'); out.delete('Content-Encoding');
    out.delete('ETag'); out.delete('Last-Modified');
    if (request.method !== 'HEAD') body = reviewHtml(await asset.text());
  }
  return new Response(body, { status: asset.status, statusText: asset.statusText, headers: out });
}

export default {
  async fetch(request, env) {
    try { return await handle(request, env); }
    catch { return unavailable(request); }
  },
};
