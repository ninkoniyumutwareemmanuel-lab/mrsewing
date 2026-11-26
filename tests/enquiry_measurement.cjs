/* Real first-party adapter, no vendor transport or network in any scenario. */
'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync('_templates/enquiry-measurement.js','utf8');
function scenario({iframe=false,crossOrigin=false,cryptoAvailable=true}={}){
 const local=[],parent=[];let nextId=0;
 class Event{constructor(type,options){this.type=type;this.detail=options.detail;}}
 const window={CustomEvent:Event,dispatchEvent:e=>local.push(e),location:{origin:'https://mrsewingfashion.com'}};
 const top=iframe?{CustomEvent:Event,dispatchEvent:e=>parent.push(e),location:{origin:'https://mrsewingfashion.com'}}:window;
 if(crossOrigin)Object.defineProperty(top,'location',{get(){throw Error('Cross-origin');}});
 window.top=top;
 const forbidden=()=>{throw Error('Signal adapter must never perform network or persistent storage');};
 const context={window,location:window.location,crypto:cryptoAvailable?{randomUUID:()=>`synthetic-${++nextId}`}:{},fetch:forbidden,localStorage:{getItem:forbidden,setItem:forbidden},sessionStorage:{getItem:forbidden,setItem:forbidden}};
 vm.runInNewContext(source,context);
 return{api:window.MrEnquiryMeasurement,local,parent,context};
}
const main=scenario(),form={id:'customerRequestForm'};
assert.equal(main.api.externalTracking,false);
assert.equal(main.api.providerAccepted(form,'quotation','custom-tailoring'),true);
assert.equal(main.api.providerAccepted(form,'quotation','custom-tailoring'),false,'same form cannot duplicate its accepted signal');
assert.equal(main.local.length,1);
assert.deepEqual(Object.keys(main.local[0].detail).sort(),['eventId','kind','outcome','service']);
assert.equal(main.local[0].type,'mrsewing:enquiry-accepted');
assert.equal(main.local[0].detail.outcome,'provider_accepted');
for(const [kind,service]of[['support','vip'],['refund','alterations'],['subscription','vip'],['quotation','unverified'],['purchase','custom-tailoring']])assert.equal(main.api.providerAccepted({id:'customerRequestForm'},kind,service),false);
assert.equal(main.api.providerAccepted({id:'supportForm'},'quotation','vip'),false);
assert.equal(main.api.providerAccepted(null,'quotation','vip'),false);
const event={};assert(main.api.whatsappClick(event));assert.equal(main.api.whatsappClick(event),false);assert(main.api.whatsappClick({}));
assert.equal(main.local.filter(e=>e.type==='mrsewing:whatsapp-click').length,2);
assert.deepEqual(Object.keys(main.local[1].detail).sort(),['eventId','interaction']);
const frame=scenario({iframe:true});assert(frame.api.providerAccepted({id:'customerRequestForm'},'consultation','alterations'));assert.equal(frame.local.length,0);assert.equal(frame.parent.length,1);
const cross=scenario({iframe:true,crossOrigin:true});assert(cross.api.whatsappClick({}));assert.equal(cross.parent.length,0);assert.equal(cross.local.length,1);
const noCrypto=scenario({cryptoAvailable:false});assert.equal(noCrypto.api.providerAccepted({id:'customerRequestForm'},'quotation','vip'),false);assert.equal(noCrypto.local.length,0);
const original=main.api;vm.runInNewContext(source,main.context);assert.equal(main.context.window.MrEnquiryMeasurement,original,'idempotent loader');
const config=JSON.parse(fs.readFileSync('_data/advertising-measurement.json'));
assert.equal(config.externalEventsEnabled,false);for(const name of['googleAds','ga4','gtm'])assert.equal(config[name].enabled,false);
assert.equal(config.googleAds.conversionId,null);assert.equal(config.googleAds.conversionLabel,null);
const request=fs.readFileSync('_templates/customer-site.js','utf8');
assert(request.indexOf('result.success!==true')<request.indexOf('MrEnquiryMeasurement?.providerAccepted'));
assert.equal((request.match(/MrEnquiryMeasurement\?\.providerAccepted/g)||[]).length,1);
assert(request.includes('if(!window.MrRequestUploads?.configured)window.MrEnquiryMeasurement?.providerAccepted'),'disabled/private storage never masquerades as verified public provider acceptance');
console.log('PASS first-party accepted-enquiry/secondary WhatsApp signals, in-memory deduplication, same-origin top-frame dispatch, allowlisted non-PII fields, no network/storage/vendor events, missing transport stays inactive. Actual Ads receipt NOT TESTED.');
