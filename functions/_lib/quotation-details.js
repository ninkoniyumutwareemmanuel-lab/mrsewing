/* R49: approved Custom Tailoring enquiry arrangements, not confirmed appointments/orders. */
import {operationalFacts} from './operational-facts.js';
export const KIGALI_TIME_ZONE='Africa/Kigali (UTC+02:00)';
const DAY=86400000;
const placeLabels={workshop:'Main Workshop: KN 441 St, Norvège, Kigali',downtown:'Downtown Consultation Location: MIC Building, by appointment'};
const methodLabels={workshop:'I Will Visit Mr Sewing',visit:'I Would Like Mr Sewing to Visit Me',online:'I Will Provide Measurements Online'};
const invalid=message=>{throw Error(message);};
function object(value,keys,message){if(!value||typeof value!=='object'||Array.isArray(value)||Object.keys(value).some(key=>!keys.includes(key)))invalid(message);return value;}
function text(value,max,label,required=false){if(value===undefined||value===null){if(required)invalid('Complete '+label+'.');return '';}if(typeof value!=='string'||value.length>max||/[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/.test(value))invalid('Review '+label+'.');const out=value.trim();if(required&&!out)invalid('Complete '+label+'.');return out;}
export function kigaliTimestamp(date,time,label='requested completion deadline'){
 if(typeof date!=='string'||typeof time!=='string'||!/^\d{4}-\d{2}-\d{2}$/.test(date)||!/^(?:[01]\d|2[0-3]):[0-5]\d$/.test(time))invalid('Enter a valid '+label+' in Kigali time.');
 const[y,m,d]=date.split('-').map(Number),leap=y%4===0&&(y%100!==0||y%400===0),days=[31,leap?29:28,31,30,31,30,31,31,30,31,30,31];
 if(y<1||m<1||m>12||d<1||d>days[m-1])invalid('Enter a valid '+label+' in Kigali time.');
 const stamp=Date.parse(date+'T'+time+':00+02:00');if(!Number.isFinite(stamp))invalid('Enter a valid '+label+' in Kigali time.');return stamp;
}
export function assessCompletion(date,time,mode,now=Date.now()){
 const deadline=kigaliTimestamp(date,time);if(!Number.isFinite(now)||deadline<=now)invalid('Choose a requested completion date and time in the future.');
 if(mode==='special')return {deadline,status:'Human assessment required',planningMs:null};
 const planningMs=deadline-now-DAY;return {deadline,status:planningMs>=7*DAY?'Standard':'Express',planningMs};
}
export function validateQuotationDetails(raw,fields,now=Date.now()){
 object(raw,['version','mode','city','measurement','delivery'],'Review the quotation arrangements.');
 if(raw.version!==2||!['suit','special'].includes(raw.mode))invalid('Review the quotation version and order type.');
 const city=text(raw.city,160,'city',true),country=text(fields.Country,160,'country',true);if(/[\r\n\t]/.test(city)||/[\r\n\t]/.test(country))invalid('Enter country and city on one line.');
 const measurement=object(raw.measurement,['method','purpose','location','date','time','address','details'],'Choose your measurement arrangements.');
 if(!Object.hasOwn(methodLabels,measurement.method))invalid('Choose how you would like your measurements taken.');
 const m={method:measurement.method,purpose:'',location:'',date:'',time:'',address:'',details:''};
 if(m.method!=='online'){
  m.date=text(measurement.date,10,'preferred measurement date',true);m.time=text(measurement.time,5,'preferred measurement time',true);kigaliTimestamp(m.date,m.time,'preferred measurement appointment');
  if(m.method==='workshop'){m.location=text(measurement.location,30,'preferred measurement location',true);if(!Object.hasOwn(placeLabels,m.location))invalid('Choose an approved measurement location.');}
  else{m.purpose=text(measurement.purpose,30,'measurement visit purpose',true);if(!['order-related','independent'].includes(m.purpose))invalid('Choose an order-related visit or independent consultation.');m.address=text(measurement.address,500,'measurement visit address',true);m.details=text(measurement.details,1000,'measurement location details');}
 }
 const delivery=object(raw.delivery,['method','location','address'],'Choose delivery or collection.');
 if(!['delivery','collection'].includes(delivery.method))invalid('Choose delivery or collection.');
 const domestic=['rwanda','rw','rwa','republic of rwanda'].includes(country.toLowerCase().replace(/\s+/g,' ')),kigali=domestic&&['kigali','kigali city','city of kigali'].includes(city.toLowerCase().replace(/\s+/g,' '));
 const d={method:delivery.method,location:'',address:''};
 if(d.method==='collection'){d.location=text(delivery.location,30,'preferred collection location',true);if(!Object.hasOwn(placeLabels,d.location))invalid('Choose an approved collection location.');}
 else d.address=text(delivery.address,500,'delivery address',!kigali);
 const assessment=assessCompletion(fields['Requested Completion Date'],fields['Requested Completion Time'],raw.mode,now);
 return {version:2,mode:raw.mode,city,country,measurement:m,delivery:d,domestic,kigali,assessment};
}
export function applyQuotationDetails(fields,value,quantity){
 const{measurement:m,delivery:d,assessment}=value;
 for(const key of ['Delivery Location / Address','Delivery Charge','Calculated Delivery Charge RWF','Delivery Charge Calculation','Collection Location','Measurement Visit Fee RWF','Provisional Service Assessment'])delete fields[key];
 fields.Country=value.country;fields.City=value.city;fields.Location=value.city+', '+value.country;
 fields['Provisional Service Assessment']=assessment.status;
 fields['Deadline Status']='Requested only; feasibility and completion date/time require business confirmation.';
 fields['Production Start']='The production period begins with the official production-start notification, not the initial enquiry.';
 if(value.mode==='suit')fields['Deadline Assessment']='Provisional screening: requested deadline minus current time minus 24 hours; at least seven days of planning time is Standard, otherwise Express. Availability and charges require assessment and customer agreement.';
 else fields['Deadline Assessment']='Special garments require human deadline assessment; the ordinary-suit seven-day threshold was not applied.';
 fields['Quotation Response Target']=assessment.status==='Express'?'Target quotation within 24 hours, subject to operating hours, sufficient information and assessment requirements.':assessment.status==='Standard'?'Target quotation within 24–48 hours, subject to operating hours, sufficient information and assessment requirements.':'The team will assess the service-specific deadline and applicable quotation target.';
 fields['Measurement Preference']=methodLabels[m.method];
 fields['Measurement Arrangement Status']='Requested only; appointment, scope and any applicable fee require confirmation. Selecting a preference does not require payment.';
 if(m.method==='online')fields['Measurements Guide']='https://mrsewingfashion.com/measurements/';
 else{
  fields['Preferred Measurement Date']=m.date;fields['Preferred Measurement Time']=m.time;fields['Measurement Time Zone']=KIGALI_TIME_ZONE;
  if(m.method==='workshop')fields['Preferred Measurement Location']=placeLabels[m.location];
  else{
   fields['Measurement Visit Address']=m.address;fields['Measurement Visit City']=value.city;fields['Measurement Visit Country']=value.country;if(m.details)fields['Measurement Location Details']=m.details;
   fields['Measurement Visit Purpose']=m.purpose==='independent'?'Independent Consultation & Fitting':'Order-related measurement visit';
   fields['Measurement Visit Fee Guidance']=m.purpose==='independent'?'Independent Consultation & Fitting: '+operationalFacts.consultationAndFittingRwf.toLocaleString('en-US')+' RWF. Location, scope and appointment require confirmation. Selecting a preference does not require payment.':'An eligible order-related Kigali measurement visit is '+operationalFacts.confirmedOrderMeasurementVisitRwf.toLocaleString('en-US')+' RWF after quotation acceptance and the required garment advance. Location, scope, eligibility and appointment require confirmation. Selecting a preference does not require payment.';
   fields['Measurement Fee Distinction']='Independent consultation and order-related measurement visits are distinct services; do not charge both fees for the same approved measurement service.';
  }
 }
 fields['Garment Receipt Preference']=d.method==='collection'?'I Will Collect':'Deliver to Me';
 if(d.method==='collection'){
  fields['Preferred Collection Location']=placeLabels[d.location];fields['Collection Status']='Requested location only; collection arrangements require team confirmation.';
 }else{
  fields['Delivery Country']=value.country;fields['Delivery City']=value.city;if(d.address)fields['Delivery Location / Address']=d.address;
  if(value.kigali&&value.mode==='suit'){
   fields['Calculated Delivery Charge RWF']='0';fields['Delivery Charge Status']='Initial eligible custom-suit delivery within Kigali is included. The team must confirm the full address before dispatch.';
  }else if(value.domestic&&!value.kigali){
   const fee=quantity*operationalFacts.outsideKigaliRwandaPerGarmentRwf;fields['Calculated Delivery Charge RWF']=String(fee);fields['Delivery Charge Calculation']=quantity+' garment'+(quantity===1?'':'s')+' × '+operationalFacts.outsideKigaliRwandaPerGarmentRwf.toLocaleString('en-US')+' RWF = '+fee.toLocaleString('en-US')+' RWF';fields['Delivery Charge Status']='Calculated domestic outside-Kigali delivery amount for an eligible Custom Tailoring order; not a final accepted quotation.';
  }else if(!value.domestic)fields['Delivery Charge Status']='International shipping and applicable charges require an individual quotation; no shipping rate or transit time is confirmed.';
  else fields['Delivery Charge Status']='Special Tailoring delivery arrangements and any applicable charge require quotation confirmation; included ordinary-suit delivery is not automatically extended.';
 }
 fields['Additional Information']=text(fields['Additional Information']??fields['Customer Message'],4000,'additional information');
 return fields;
}
export function specialOrderFields(raw){
 const garments={shirt:'Shirt',trousers:'Trousers',dress:'Dress',skirt:'Skirt',jacket:'Jacket',coat:'Coat',other:'Other custom clothing'};
 const garment=text(raw['Garment Type'],40,'garment type',true);if(!Object.hasOwn(garments,garment))invalid('Choose the garment you want made.');
 const other=garment==='other'?text(raw['Other Garment'],160,'other garment description',true):'';
 const quantity=text(raw.Quantity,4,'garment quantity',true);if(!/^[1-9]\d{0,3}$/.test(quantity))invalid('Enter a valid garment quantity.');
 return {garment,label:garments[garment],other,quantity,description:text(raw['Design Description'],4000,'design description',true),additional:text(raw['Additional Information']??raw['Customer Message'],4000,'additional information')};
}
