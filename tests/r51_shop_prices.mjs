/* R51 Shop exception: trusted synthetic catalogue only, no real publication/payment/provider. */
import assert from 'node:assert/strict';
import {validate,handle} from '../functions/_lib/shop-handler.js';
const p={id:'R51_SYNTHETIC',name:'Fictional stock garment',slug:'r51-synthetic-garment',availability:'Available in Stock',priceRwf:173000,variations:[{id:'R51_SIZE',size:'M',colour:'Navy',stockQuantity:3}]};
const body={kind:'purchase',customer:{'Full Name':'Fictional R51 QA','Phone / WhatsApp':'+250780000000','Email Address':'qa@example.invalid',Consent:'Accepted','Delivery or Collection':'Fictional collection request','Preferred Payment Method':'Bank Transfer'},items:[{productId:p.id,variationId:p.variations[0].id,quantity:2,priceRwf:1}]};
const result=validate(body,[p]);assert.equal(result['Catalogue Subtotal RWF'],346000);assert.equal(JSON.parse(result.Products)[0].catalogueUnitPriceRwf,173000);assert.equal(JSON.parse(result.Products)[0].quantity,2);
assert.throws(()=>validate({...body,items:[{...body.items[0],quantity:4}]},[p]),/stock/i);
assert.throws(()=>validate(body,[{...p,availability:'Out of Stock'}]),/stock/i);
assert.throws(()=>validate(body,[]),/no longer available/i);
let sent,calls=0;const host='https://preview.mrsewing-staging.pages.dev';const req=new Request(host+'/api/shop-request',{method:'POST',headers:{'Content-Type':'application/json',Origin:host},body:JSON.stringify(body)});
const response=await handle(req,[p],'synthetic-key',async(url,options)=>{calls++;sent=JSON.parse(options.body);assert.equal(url,'https://api.web3forms.com/submit');return new Response('{"success":true}');});assert.equal(response.status,200);assert.equal(calls,1);assert.equal(sent['Catalogue Subtotal RWF'],346000);
console.log('PASS R51 Shop canonical unit price/subtotal/stock rejection/positive mocked provider; no actual order/payment/publication');
