/* No network: source files stay denied on every deployment host; public routes keep their behavior. */
import assert from 'node:assert/strict';
import {onRequest} from '../functions/_middleware.js';
let calls=0;
const next=()=>{calls++;return new Response('existing route',{status:200})};
for(const host of ['mrsewing-staging.pages.dev','preview.mrsewing-staging.pages.dev','mrsewingfashion.com','www.mrsewingfashion.com','other.pages.dev']){
 for(const path of ['/_data/suit-package-prices.json','/_templates/homepage-quotation.html','/scripts/customer_site.py','/tests/recovery_workflow.py','/docs/reconciliation/2026-11-25/history-audit.json','/.github/policy-documents/terms-and-conditions/1.0.pdf','/%5fdata/business.json','/%255fdata/business.json','/assets/%252e%252e/%255fdata/business.json','/functions/_lib/shop-handler.js']){
  const before=calls,response=await onRequest({request:new Request('https://'+host+path),next});assert.equal(response.status,404,path);assert.equal(calls,before);assert.equal(response.headers.get('Cache-Control'),'no-store');assert.match(response.headers.get('X-Robots-Tag'),/noindex/);
 }
 for(const path of ['/','/assets/design-selections.js','/assets/policy-documents/terms-and-conditions/1.2.pdf','/guides/fabrics/','/shop/','/api/selected-design-request','/api/shop-request','/terms-and-conditions/current/']){
  const response=await onRequest({request:new Request('https://'+host+path),next});assert.equal(response.status,200,path);
 }
 const head=await onRequest({request:new Request('https://'+host+'/_data/business.json',{method:'HEAD'}),next});assert.equal(head.status,404);assert.equal(await head.text(),'');
}
console.log('PASS actual middleware on staging/production/other host simulations: internal source/data404, encoded traversal denied, public assets/PDF/forms/Shop/API unchanged; no global production noindex');
