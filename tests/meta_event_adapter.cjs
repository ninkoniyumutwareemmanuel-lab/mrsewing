/* Synthetic Meta queue tests only. No SDK, network or account events run. */
'use strict';
const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const template=fs.readFileSync('_templates/meta-event-adapter.js','utf8');
const config={pixelId:'29683883327873735',productionEnabled:true};
function scenario({host='mrsewingfashion.com',granted=true,safe=true,iframe=false,existing=false,existingAlias=false,enabled=true,gateThrows=false}={}){
 const listeners={},scripts=[];let choice=granted,contextSafe=safe;
 const window={addEventListener:(name,callback)=>{(listeners[name]??=[]).push(callback);},MrCustomerTracking:{consentGranted:()=>choice,canTrack:()=>{if(gateThrows)throw Error('Synthetic gate failure');return contextSafe;}}};
 window.top=iframe?{}:window;
 if(existing)window.fbq=()=>{throw Error('Must not reuse unknown Pixel');};
 if(existingAlias)window._fbq=()=>{throw Error('Must not reuse unknown Pixel alias');};
 const document={head:{appendChild:node=>scripts.push(node)},createElement:tag=>({tag})};
 const context={window,location:{hostname:host},document};
 const source=template.replace('/*meta-event-config*/null',JSON.stringify({...config,productionEnabled:enabled}));
 vm.runInNewContext(source,context);
 function emit(eventName,eventId='synthetic-event',extra={}){for(const listener of listeners['mrsewing:customer-event']||[])listener({detail:{eventName,eventId,...extra}});}
 function consent(value){choice=value;for(const listener of listeners['mrsewing:tracking-consent']||[])listener({detail:{granted:value}});}
 return{window,scripts,emit,consent,setSafe:value=>{contextSafe=value;},queue:()=>Array.from(window.fbq?.queue||[],row=>Array.from(row)),reinstall:()=>vm.runInNewContext(source,context)};
}
for(const options of[{host:'mrsewing-staging.pages.dev'},{host:'preview.mrsewing-staging.pages.dev'},{host:'localhost'},{host:'unfamiliar.example'},{iframe:true},{granted:false},{safe:false},{enabled:false},{gateThrows:true}]){
 const s=scenario(options);s.emit('quote_request_success');assert.equal(s.scripts.length,0,JSON.stringify(options));assert.equal(s.queue().length,0);
}
const active=scenario();assert.equal(active.scripts.length,0,'adapter waits for unified consent/events');
active.consent(true);active.emit('page_view','page-one');active.emit('page_view','page-one');active.reinstall();active.emit('page_view','page-one');
assert.equal(active.scripts.length,1);assert.equal(active.scripts[0].src,'https://connect.facebook.net/en_US/fbevents.js');
const initial=active.queue();assert.deepEqual(initial.slice(0,3),[['set','autoConfig',false,config.pixelId],['consent','grant'],['init',config.pixelId]]);
assert.equal(initial.filter(row=>row[0]==='init').length,1);assert.equal(initial.filter(row=>row[0]==='track').length,1);
active.emit('design_view','design-one',{designId:'MS-031',name:'PRIVATE NAME',photo:'https://example.invalid/private.jpg'});
active.emit('whatsapp_contact_click','whatsapp-one',{message:'PRIVATE MESSAGE',phone:'+250780000000'});
active.emit('website_call_click','call-one');
active.emit('quote_request_success','enquiry-one',{service:'custom-tailoring',email:'private@example.invalid',measurements:'PRIVATE MEASUREMENTS',value:100});
active.emit('lead_form_success','enquiry-one',{service:'custom-tailoring'});
active.emit('lead_form_success','service-one',{service:'alterations'});
for(const name of['appointment_confirmed','Purchase','purchase','Schedule','request_submission_failed','request_started','directions_click'])active.emit(name,'unsupported-'+name);
const tracks=active.queue().filter(row=>row[0]==='track');
assert.deepEqual(tracks.map(row=>row[1]),['PageView','ViewContent','Contact','Contact','Lead','Lead']);
assert.deepEqual(JSON.parse(JSON.stringify(tracks[1].slice(2))),[{content_category:'garment_design'},{eventID:'design-one'}]);
assert.deepEqual(JSON.parse(JSON.stringify(tracks[2].slice(2))),[{intent_channel:'whatsapp'},{eventID:'whatsapp-one'}]);
assert.deepEqual(JSON.parse(JSON.stringify(tracks[3].slice(2))),[{intent_channel:'telephone'},{eventID:'call-one'}]);
assert.equal(tracks.filter(row=>row[3].eventID==='enquiry-one').length,1,'same success never counts quote and lead twice');
assert(!/PRIVATE|private@example|private\.jpg|MS-031|"value"|currency|user_data|external_id|fbp|fbc/.test(JSON.stringify(tracks)),'no arbitrary matching/PII/form fields');
const count=tracks.length;active.consent(false);active.emit('lead_form_success','withdrawn');assert.equal(active.queue().filter(row=>row[0]==='track').length,count);assert(active.queue().some(row=>row[0]==='consent'&&row[1]==='revoke'));
active.consent(true);active.emit('lead_form_success','after-regrant',{service:'garment-care'});assert.equal(active.scripts.length,1);assert.equal(active.queue().filter(row=>row[0]==='init').length,1);
active.setSafe(false);active.emit('lead_form_success','unsafe-after-load');assert.equal(active.queue().filter(row=>row[0]==='track').length,count+1,'safe context is rechecked for every event');
active.scripts[0].onerror();assert.equal(active.window.__mrMetaEventAdapter.scriptFailed,true);
const unknown=scenario({existing:true});unknown.consent(true);unknown.emit('page_view');assert.equal(unknown.scripts.length,0);assert.equal(unknown.window.__mrMetaEventAdapter.blockedExistingPixel,true);
const alias=scenario({existingAlias:true});alias.consent(true);assert.equal(alias.scripts.length,0);assert.equal(alias.window.__mrMetaEventAdapter.blockedExistingPixel,true);
const malformed=scenario();malformed.emit('Lead','x');malformed.emit('quote_request_success','private@example.invalid');assert.equal(malformed.scripts.length,0);
console.log('PASS Meta adapter: fresh unified consent/safe-context/official top gate, existing dataset, autoConfig off, no matching data, one SDK/init, supported PageView/ViewContent/Contact/Lead, eventID dedupe, revocation, malformed/unknown SDK failure handling. No actual Meta events or CAPI sent; platform receipt NOT TESTED.');
