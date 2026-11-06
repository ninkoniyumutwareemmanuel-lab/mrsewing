import fs from 'node:fs';import assert from 'node:assert/strict';
const imp=p=>import('data:text/javascript;base64,'+fs.readFileSync(p).toString('base64'));
const{pages}=await imp('functions/_lib/shop-preview-pages.js'),{handlePreview}=await imp('functions/_lib/shop-preview-handler.js');
const next=()=>new Response('normal published-only shop',{status:404});
for(const host of ['mrsewing-staging.pages.dev','abc.mrsewing-staging.pages.dev']){
 const r=await handlePreview({request:new Request('https://'+host+'/shop/'),next},pages);assert.equal(r.status,200);const text=await r.text();assert.equal((text.match(/class="product-card draft-card"/g)||[]).length,21);assert.match(r.headers.get('X-Robots-Tag'),/noindex/);assert.equal(r.headers.get('Cache-Control'),'no-store');
 for(const route of Object.keys(pages)){const q=await handlePreview({request:new Request('https://'+host+route),next},pages);assert.equal(q.status,200);}
}
for(const host of ['mrsewingfashion.com','www.mrsewingfashion.com','evil-mrsewing-staging.pages.dev','mrsewing-staging.pages.dev.evil.com','other.pages.dev']){const r=await handlePreview({request:new Request('https://'+host+'/shop/'),next},pages);assert.equal(await r.text(),'normal published-only shop');}
assert.equal((await handlePreview({request:new Request('https://mrsewing-staging.pages.dev/shop/cart/'),next},pages)).status,404);
assert.equal((await handlePreview({request:new Request('https://mrsewing-staging.pages.dev/shop/',{method:'POST'}),next},pages)).status,404);
console.log('PASS server route:21draft cards,28preview routes,2staging hosts;5nonstaginghosts fall through;cart/POST unchanged;noindex/no-store');
