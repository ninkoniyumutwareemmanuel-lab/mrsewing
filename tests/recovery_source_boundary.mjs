/* No network: exercise the real staging-only Pages middleware. */
import assert from 'node:assert/strict';
import {onRequest} from '../functions/_middleware.js';
let calls=0;
const next=()=>{calls++;return new Response('existing route',{status:200})};
for(const host of ['mrsewing-staging.pages.dev','preview.mrsewing-staging.pages.dev']){
 for(const path of ['/_data/suit-package-prices.json','/_templates/homepage-quotation.html','/scripts/customer_site.py','/tests/recovery_workflow.py','/docs/reconciliation/2026-11-25/history-audit.json','/.github/policy-documents/terms-and-conditions/1.0.pdf','/%5fdata/business.json','/%255fdata/business.json','/functions/_lib/shop-handler.js']){
  const before=calls,response=await onRequest({request:new Request('https://'+host+path),next});assert.equal(response.status,404,path);assert.equal(calls,before);assert.equal(response.headers.get('Cache-Control'),'no-store');assert.match(response.headers.get('X-Robots-Tag'),/noindex/);
 }
 for(const path of ['/','/assets/design-selections.js','/assets/policy-documents/terms-and-conditions/1.2.pdf','/guides/fabrics/','/shop/','/api/selected-design-request','/api/shop-request','/terms-and-conditions/current/']){
  const response=await onRequest({request:new Request('https://'+host+path),next});assert.equal(response.status,200,path);
 }
 const head=await onRequest({request:new Request('https://'+host+'/_data/business.json',{method:'HEAD'}),next});assert.equal(head.status,404);assert.equal(await head.text(),'');
}
for(const host of ['mrsewingfashion.com','www.mrsewingfashion.com','other.pages.dev','mrsewing-staging.pages.dev.evil.invalid']){
 const response=await onRequest({request:new Request('https://'+host+'/_data/business.json'),next});assert.equal(response.status,200,'unrelated/production host unchanged');
}
console.log('PASS real staging-only source boundary; internal selling/source records404; public assets/PDF/forms/Shop/API unchanged; no production-host behavior change');
