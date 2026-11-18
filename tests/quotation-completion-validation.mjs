/* R49: ordinary/Special tailoring use one secured provider pipeline. No live submissions. */
import assert from 'node:assert/strict';
import {handleSelected} from '../functions/_lib/selected-design-handler.js';
import {assessCompletion,validateQuotationDetails} from '../functions/_lib/quotation-details.js';
import {references} from '../scripts/edge/request-data.mjs';
import {colours} from '../functions/_lib/fabric-preferences.js';
const HOST='https://test.mrsewing-staging.pages.dev',NOW=Date.parse('2026-11-13T10:00:00Z'),DAY=86400000;
const at=ms=>{const stamp=new Date(ms+7200000).toISOString();return {date:stamp.slice(0,10),time:stamp.slice(11,16)};};
const deadline=at(NOW+12*DAY),appointment=at(NOW+2*DAY);
const men=Object.entries(references).find(([,v])=>v.audience==='men'),women=Object.entries(references).find(([,v])=>v.audience==='women');assert(men&&women);
const rows=[men,women].map(([design,r],i)=>({design,photo:r.images[0].url,quantity:i+1,fabricChoice:'advice',fabricRef:''}));
const fields={Service:'Custom Tailoring & Suits','Design Order Type':'Standard Order','Design Reference':rows[0].design,'Selected Photograph URL':rows[0].photo,Quantity:'1','Fabric Choice':'Help Me Choose Fabric','Full Name':'Fictional R49 Backend QA','Phone Number':'+250780000000','Email Address':'',Country:'Rwanda','Requested Completion Date':deadline.date,'Requested Completion Time':deadline.time,'Requested Completion Time Zone':'Africa/Kigali (UTC+02:00)','Additional Information':'Fictional requirements, not a real order'};
const details={version:2,mode:'suit',city:'Kigali',measurement:{method:'online'},delivery:{method:'delivery',address:''}};
const pref={choice:'advice',fabricRef:'',colour:'',colourDescription:''};
const base={fields,selections:rows,fabricPreference:pref,quotationDetails:details,termsAccepted:true,botcheck:''};
const specialBase={fields:{...fields,'Design Order Type':'Special Order','Design Reference':'','Selected Photograph URL':'','Garment Type':'shirt',Quantity:'3','Design Description':'A plain long-sleeved shirt, subject to review'},fabricPreference:pref,quotationDetails:{...details,mode:'special'},termsAccepted:true,botcheck:''};
const request=(body=base,headers={})=>new Request(HOST+'/api/selected-design-request',{method:'POST',headers:{'Content-Type':'application/json',Origin:HOST,...headers},body:JSON.stringify(body)});
let calls=0,sent;
const provider=async(url,options)=>{assert.equal(url,'https://api.web3forms.com/submit');calls++;sent=JSON.parse(options.body);return new Response('{"success":true}');};
const pass=async(body=base)=>{const response=await handleSelected(request(body),'synthetic-key',provider,NOW);assert.equal(response.status,200,await response.clone().text());return sent;};
const reject=async(body,status=400)=>{const before=calls,response=await handleSelected(request(body),'synthetic-key',provider,NOW);assert.equal(response.status,status,JSON.stringify(body));assert.equal(calls,before,'invalid input must not contact provider');return (await response.json()).error;};
const changed=(body,patch)=>({...body,quotationDetails:{...body.quotationDetails,...patch}});

// Inclusive ordinary planning boundary; requested deadline is never an accepted schedule.
for(const [offset,status]of[[8*DAY,'Standard'],[8*DAY-60000,'Express'],[DAY,'Express'],[60000,'Express']]){const d=at(NOW+offset);assert.equal(assessCompletion(d.date,d.time,'suit',NOW).status,status);await pass({...base,fields:{...fields,'Requested Completion Date':d.date,'Requested Completion Time':d.time}});assert.equal(sent['Provisional Service Assessment'],status);assert(sent['Deadline Status'].includes('confirmation'));assert(!('Order Priority'in sent));}
assert.equal(assessCompletion(...Object.values(at(NOW+DAY)),'special',NOW).status,'Human assessment required');
for(const d of[at(NOW),at(NOW-60000),{date:'2027-02-29',time:'14:30'},{date:'2026-13-01',time:'14:30'},{date:'2026-11-20',time:'24:00'}])await reject({...base,fields:{...fields,'Requested Completion Date':d.date,'Requested Completion Time':d.time}});

await pass();assert.equal(sent.City,'Kigali');assert.equal(sent.Country,'Rwanda');assert.equal(sent['Total Garments'],'3');assert.equal(sent['Selected Design Count'],'2');assert(!('Delivery Location / Address'in sent));assert.equal(sent['Calculated Delivery Charge RWF'],'0');assert(sent['Delivery Charge Status'].includes('confirm the full address'));assert.equal(sent['Measurement Preference'],'I Will Provide Measurements Online');assert.equal(sent['Additional Information'],fields['Additional Information']);assert(!('Customer Message'in sent));for(const row of rows)assert(sent['Selected Designs'].includes(row.photo));assert(sent.Consent.includes('Privacy Policy'));

// User-supplied output labels/charges cannot override server canonical values.
await pass({...base,fields:{...fields,City:'Forged city','Calculated Delivery Charge RWF':'999999','Provisional Service Assessment':'Express','Delivery Charge Status':'Already paid'}});assert.equal(sent.City,'Kigali');assert.equal(sent['Provisional Service Assessment'],'Standard');assert.equal(sent['Calculated Delivery Charge RWF'],'0');assert(!sent['Delivery Charge Status'].includes('Already paid'));
for(const count of[1,2,3]){await pass({...changed(base,{city:'Huye',delivery:{method:'delivery',address:'Fictional Huye address'}}),selections:[{...rows[0],quantity:count}]});assert.equal(sent['Calculated Delivery Charge RWF'],String(count*5000));assert(sent['Delivery Charge Status'].includes('not a final accepted quotation'));}
await reject(changed(base,{city:'Huye',delivery:{method:'delivery',address:''}}));
await pass({...changed(base,{city:'Nairobi',delivery:{method:'delivery',address:'Fictional Nairobi delivery address'}}),fields:{...fields,Country:'Kenya'}});assert(!('Calculated Delivery Charge RWF'in sent));assert(sent['Delivery Charge Status'].includes('individual quotation'));assert(!sent['Delivery Charge Status'].includes('5,000'));
await reject({...changed(base,{city:'Nairobi',delivery:{method:'delivery',address:''}}),fields:{...fields,Country:'Kenya'}});
await pass(changed(base,{delivery:{method:'collection',location:'downtown',address:'Stale address must not be forwarded'}}));assert(!('Delivery Location / Address'in sent));assert(!('Calculated Delivery Charge RWF'in sent));assert(sent['Preferred Collection Location'].includes('MIC Building, by appointment'));assert(sent['Collection Status'].includes('confirmation'));
await reject(changed(base,{delivery:{method:'collection',location:''}}));
await reject(changed(base,{delivery:{method:'delivery',address:'x',charge:0}}));

// Appointment fields are conditional; selecting a preference never makes payment due.
const workshop={method:'workshop',location:'workshop',...appointment};
await pass(changed(base,{measurement:workshop}));assert(sent['Preferred Measurement Location'].includes('KN 441 St, Norvège, Kigali'));assert.equal(sent['Measurement Time Zone'],'Africa/Kigali (UTC+02:00)');assert(!('Measurement Visit Address'in sent));assert(!('Measurement Visit Fee RWF'in sent));
await pass(changed(base,{measurement:{...workshop,location:'downtown'}}));assert(sent['Preferred Measurement Location'].includes('by appointment'));
for(const key of['location','date','time'])await reject(changed(base,{measurement:{...workshop,[key]:''}}));
const visit={method:'visit',purpose:'order-related',...appointment,address:'Fictional Kigali visit address',details:'Fictional location guidance'};
await pass(changed(base,{measurement:visit}));assert.equal(sent['Measurement Visit Address'],visit.address);assert.equal(sent['Measurement Visit City'],'Kigali');assert.equal(sent['Measurement Visit Purpose'],'Order-related measurement visit');assert(!sent['Measurement Visit Fee Guidance'].includes('35,000 RWF'));assert(sent['Measurement Visit Fee Guidance'].includes('10,000 RWF'));assert(sent['Measurement Visit Fee Guidance'].includes('after quotation acceptance'));assert(sent['Measurement Arrangement Status'].includes('does not require payment'));assert(!('Measurement Visit Fee RWF'in sent));
await pass(changed(base,{measurement:{...visit,purpose:'independent'}}));assert.equal(sent['Measurement Visit Purpose'],'Independent Consultation & Fitting');assert(sent['Measurement Visit Fee Guidance'].includes('35,000 RWF'));assert(!sent['Measurement Visit Fee Guidance'].includes('10,000 RWF'));
for(const key of['purpose','address','date','time'])await reject(changed(base,{measurement:{...visit,[key]:''}}));
await pass(changed(base,{measurement:{method:'online',date:'stale',address:'Stale private address'}}));assert(!('Measurement Visit Address'in sent));assert(!('Preferred Measurement Date'in sent));assert.equal(sent['Measurements Guide'],'https://mrsewingfashion.com/measurements/');

// Special Tailoring shares the existing endpoint/provider, without invented suit references.
await pass(specialBase);assert.equal(sent['Garment Type'],'Shirt');assert.equal(sent['Total Garments'],'3');assert.equal(sent['Selected Design Count'],'0');assert.equal(sent['Provisional Service Assessment'],'Human assessment required');assert(!('Calculated Delivery Charge RWF'in sent));assert(sent['Deadline Assessment'].includes('was not applied'));assert.equal(sent['Design Description'],specialBase.fields['Design Description']);assert(!('Selected Photograph URL'in sent));assert(sent['Picture Sharing'].includes('WhatsApp'));assert.equal(sent.subject,'Special Tailoring Quotation Request - Mr Sewing');
for(const garment of['shirt','trousers','dress','skirt','jacket','coat'])await pass({...specialBase,fields:{...specialBase.fields,'Garment Type':garment}});
await pass({...specialBase,fields:{...specialBase.fields,'Garment Type':'other','Other Garment':'Fictional custom waistcoat'}});assert.equal(sent['Other Garment'],'Fictional custom waistcoat');
await reject({...specialBase,fields:{...specialBase.fields,'Garment Type':'other','Other Garment':''}});
await reject({...specialBase,fields:{...specialBase.fields,'Garment Type':'unapproved-category'}});
await reject({...specialBase,fields:{...specialBase.fields,'Design Description':''}});
await reject({...specialBase,fields:{...specialBase.fields,Quantity:'0'}});
await reject({...specialBase,selections:rows});
await reject({...specialBase,fields:{...specialBase.fields,'Design Reference':rows[0].design}});
await pass({...specialBase,fabricPreference:undefined,fields:{...specialBase.fields,'Fabric Choice':'Customer fabric choice','Fabric Reference':'men-wool'}});assert.equal(sent['Selected Fabric'],'Wool');assert(!('Preferred Colour'in sent));
await pass({...specialBase,fabricPreference:undefined,fields:{...specialBase.fields,'Fabric Choice':'Customer fabric choice','Fabric Reference':''}});assert(!('Selected Fabric'in sent));
await pass(changed(specialBase,{city:'Musanze',delivery:{method:'delivery',address:'Fictional Musanze address'}}));assert.equal(sent['Calculated Delivery Charge RWF'],'15000');

// Optional Other description, strict valid supplied values and shared identity still apply.
await pass({...base,fabricPreference:{choice:'now',fabricRef:'men-wool',colour:'other',colourDescription:''}});assert.equal(sent['Preferred Colour'],colours.other.name);assert(!('Colour Description'in sent));
await reject({...base,fabricPreference:{choice:'now',fabricRef:'men-wool',colour:'other',colourDescription:'<script>'}});
for(const key of['Full Name','Phone Number','Country'])await reject({...base,fields:{...fields,[key]:''}});
await reject(changed(base,{city:''}));await reject({...base,termsAccepted:false});await reject({...base,botcheck:'spam'});
await reject({...base,quotationDetails:{...details,mode:'special'}});
await reject({...base,fields:{...fields,'Additional Information':'x'.repeat(4001)}});
await reject({...base,fields:{...fields,'Additional Information':'x'.repeat(31000)}},413);

// Legacy selected-suit formats keep their old contract and validation.
const legacy={...base,quotationDetails:undefined,fields:{...fields,'Delivery Location / Address':'Legacy fictional address','Customer Message':'Legacy request'}};await pass(legacy);assert(!('Provisional Service Assessment'in sent));assert.equal(sent['Delivery Location / Address'],'Legacy fictional address');
const before=calls;const origin=await handleSelected(request(base,{Origin:'https://foreign.invalid'}),'synthetic',provider,NOW);assert.equal(origin.status,403);assert.equal(calls,before);
for(const failure of[async()=>new Response('{"success":false}'),async()=>new Response('{"success":true}',{status:500}),async()=>{throw Error('Synthetic provider failure')}])assert.equal((await handleSelected(request(),'synthetic',failure,NOW)).status,502);
assert.equal((await handleSelected(request(),'')).status,503);
console.log('PASS V2ordinary+Special/commonprovider/futureKigalideadlines/StandardExpressboundary/conditionalmeasurements/deliveryfeesandaddresses/collection/optionalOther/completephotos+quantity/security+legacy/no real submissions');
