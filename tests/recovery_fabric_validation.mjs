/* Recovery25Nov2026: canonical collection/style/pattern survives the real
   request handler. Provider and all customer details are synthetic. */
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {handleSelected} from '../functions/_lib/selected-design-handler.js';
import {references,fabrics} from '../scripts/edge/request-data.mjs';
import {patterns,colours} from '../functions/_lib/fabric-preferences.js';
const catalogue=JSON.parse(fs.readFileSync('_data/fabric-collections.json'));
assert.equal(catalogue.collections.length,7);
assert.equal(catalogue.collections.flatMap(c=>c.styles).length,26);
assert.equal(Object.keys(patterns).length,17);
assert.equal(Object.keys(colours).length,50);
const refs=Object.entries(references),men=refs.find(([,r])=>r.audience==='men'),women=refs.find(([,r])=>r.audience==='women');
const selections=[men,women].map(([design,r],i)=>({design,photo:r.images[0].url,quantity:i+2,project:null}));
const fields={Service:'Custom Tailoring & Suits','Design Order Type':'Standard Order','Design Reference':selections[0].design,'Selected Photograph URL':selections[0].photo,Quantity:'1','Fabric Choice':'Help Me Choose Fabric','Full Name':'Fictional Fabric Recovery QA','Phone Number':'+250780000000',Country:'Rwanda','Delivery Location / Address':'Fictional Kigali test address','Requested Completion Date':'2026-12-29','Requested Completion Time':'14:30','Requested Completion Time Zone':'Africa/Kigali (UTC+02:00)','Customer Message':'Mock only'};
let calls=0,sent;
const provider=async(_url,options)=>{calls++;sent=JSON.parse(options.body);return new Response('{"success":true}');};
async function submit(pref){return handleSelected(new Request('https://mrsewing-staging.pages.dev/api/selected-design-request',{method:'POST',headers:{'Content-Type':'application/json',Origin:'https://mrsewing-staging.pages.dev'},body:JSON.stringify({fields,selections,fabricPreference:pref,termsAccepted:true,botcheck:''})}),'fictional-key',provider);}
for(const collection of catalogue.collections)for(const style of collection.styles){
 const response=await submit({choice:'now',fabricRef:style.id,pattern:'windowpane',colour:'navy-blue',colourDescription:''});
 assert.equal(response.status,200,await response.clone().text());
 assert.equal(sent['Selected Fabric'],style.name);assert.equal(sent['Fabric Collection'],collection.name);assert.equal(sent['Pattern & Texture'],'Windowpane');assert.equal(sent['Pattern Reference'],'windowpane');assert.equal(sent['Preferred Colour'],'Navy Blue');assert.equal(sent['Total Garments'],'5');assert.equal(sent['Selected Design Count'],'2');assert.equal(sent['Fabric Tier'],undefined,'Collection grouping must not invent a pricing tier');
 for(const row of selections){assert(sent['Selected Designs'].includes(row.photo));assert(sent['Selected Designs'].includes('Quantity: '+row.quantity));}
}
for(const pattern of Object.keys(patterns)){
 assert.equal((await submit({choice:'now',fabricRef:'super-1',pattern,colour:'black',colourDescription:''})).status,200);
 assert.equal(sent['Pattern & Texture'],patterns[pattern].name);
}
for(const bad of [{choice:'now',fabricRef:'unapproved-style',pattern:'plain',colour:'black'},{choice:'now',fabricRef:'super-1',pattern:'invented-pattern',colour:'black'},{choice:'now',fabricRef:'super-1',pattern:'plain',colour:'invented-colour'},{choice:'advice',fabricRef:'',pattern:'plain',colour:''}]){
 const before=calls;assert.equal((await submit(bad)).status,400);assert.equal(calls,before);
}
const context={window:{}};vm.runInNewContext(fs.readFileSync('_templates/shared-fabric.js','utf8'),context);
const preferences=context.window.MrFabricPreferences({fabrics,patterns,colours});
const chosen={choice:'now',fabricRef:'wool-2',pattern:'herringbone',colour:'navy-blue',colourDescription:''};
assert.equal(preferences.unpack(preferences.pack(chosen)).pattern,'herringbone');assert.equal(preferences.details(chosen).collectionName,'Wool Collection');assert.equal(preferences.details(chosen).patternName,'Herringbone');
assert.equal(preferences.unpack(JSON.stringify(['now','men-wool','black',''])).fabricRef,'men-wool','Supported old four-part links stay usable');
assert.equal(preferences.valid(chosen),true);assert.equal(preferences.valid({choice:'now',fabricRef:'fake',colour:'black'}),false);
console.log('PASS7collections/26styles/17patterns/50colours; realvalidator with mockedprovider; exactmixedphotos+quantities; canonicalnames/patterns; no inventedtier; invalidrejection; legacy4/new5partstorage');
