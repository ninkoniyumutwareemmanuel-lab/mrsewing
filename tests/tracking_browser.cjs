/* Offline official-host simulation: vendor SDKs are inert stubs, never downloads. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
function lib(){for(const n of['playwright','playwright-core','/workspace/tools/phase1/node_modules/playwright-core']){try{return require(n)}catch(e){if(e.code!=='MODULE_NOT_FOUND')throw e}}throw Error('Playwright required');}
const{chromium}=lib(),BASE=process.env.REVIEW_BASE_URL||'http://127.0.0.1:8020',OUT=process.env.REVIEW_ARTIFACTS||'/tmp/mrsewing-tracking-browser';
const result={scope:'Actual browser with local pages under synthetic official host; GTM/Meta inert stubs; no actual platform or provider traffic',checks:[],errors:[],realAdvertisingEvents:false,realSubmissions:false};
(async()=>{fs.mkdirSync(OUT,{recursive:true});const b=await chromium.launch({executablePath:process.env.CHROMIUM_BINARY||(fs.existsSync('/usr/bin/chromium')?'/usr/bin/chromium':undefined),args:['--no-sandbox']});try{
 const ctx=await b.newContext({viewport:{width:390,height:900},reducedMotion:'reduce'});const vendor=[];
 await ctx.addInitScript(()=>{window.__opened=[];window.open=u=>{__opened.push(String(u));return null;};});
 await ctx.route('**/*',async route=>{
  const req=route.request(),u=new URL(req.url());
  if(req.method()!=='GET')return route.abort();
  if(u.hostname==='www.googletagmanager.com'){vendor.push({kind:'google',url:u.href});return route.fulfill({contentType:'application/javascript',body:'window.__gtmStubLoaded=true;'});}
  if(u.hostname==='connect.facebook.net'){vendor.push({kind:'meta',url:u.href});return route.fulfill({contentType:'application/javascript',body:'window.__metaStubLoaded=true;'});}
  if(u.hostname==='mrsewingfashion.com'){const local=await ctx.request.get(BASE+u.pathname+u.search);return route.fulfill({response:local});}
  return route.abort();
 });
 const page=await ctx.newPage();page.on('pageerror',e=>result.errors.push(e.message));
 await page.goto('https://mrsewingfashion.com/',{waitUntil:'load'});assert.equal(vendor.length,0);
 await page.getByRole('button',{name:'Reject',exact:true}).click();assert.equal(vendor.length,0);result.checks.push({name:'fresh consent rejects without SDK and essential page remains',status:'PASS'});
 await page.getByRole('button',{name:'Cookie preferences',exact:true}).click();await page.getByRole('button',{name:'Accept',exact:true}).click();await page.waitForFunction(()=>__gtmStubLoaded&&__metaStubLoaded);
 assert.equal(vendor.filter(x=>x.kind==='google').length,1);assert.equal(vendor.filter(x=>x.kind==='meta').length,1);
 assert(vendor.some(x=>x.url.includes('GTM-WHR49M4D')));await page.screenshot({path:path.join(OUT,'consented-home-390.png')});
 await page.evaluate(()=>{document.addEventListener('click',e=>{if(e.target.closest('a[href^="tel:"],a[href*="maps.app.goo.gl"]'))e.preventDefault();});});
 const phone=page.locator('a[href^="tel:"]').first();await phone.click();
 await page.evaluate(()=>{const a=document.createElement('a');a.href='/whatsapp/?text=Synthetic%20enquiry';a.target='_blank';a.id='qa-wa';a.textContent='Synthetic contact';document.body.append(a);});await page.locator('#qa-wa').click();
 await page.evaluate(()=>{const form=document.createElement('form');form.id='customerRequestForm';form.dataset.kind='quotation';
  MrEnquiryMeasurement.support(form,'request_submission_failed');
  MrEnquiryMeasurement.providerAccepted(form,'quotation','custom-tailoring');
  MrEnquiryMeasurement.providerAccepted(form,'quotation','custom-tailoring');
  const other=document.createElement('form');other.id='customerRequestForm';MrEnquiryMeasurement.providerAccepted(other,'quotation','alterations');
  window.MrCustomerTracking.signal({eventName:'appointment_confirmed',eventId:'synthetic-appointment'});
 });
 const events=await page.evaluate(()=>dataLayer.filter(x=>x.event));
 assert.equal(events.filter(x=>x.event==='whatsapp_contact_click').length,1);assert.equal(events.filter(x=>x.event==='website_call_click').length,1);
 assert.equal(events.filter(x=>x.event==='quote_request_success').length,1);assert.equal(events.filter(x=>x.event==='lead_form_success').length,1);assert.equal(events.filter(x=>x.event==='appointment_confirmed').length,0);
 assert.equal(events.filter(x=>x.event==='request_submission_failed').length,1);
 assert.equal(await page.evaluate(()=>__opened.length),1,'WhatsApp opens without waiting for advertising');
 const meta=await page.evaluate(()=>fbq.queue.map(x=>Array.from(x)));
 assert.equal(meta.filter(x=>x[0]==='init').length,1);assert.equal(meta.filter(x=>x[1]==='Lead').length,2);assert(!meta.some(x=>x[1]==='Purchase'||x[1]==='Schedule'));
 result.checks.push({name:'single GTM/Pixel; deliberate contact, positive mutually exclusive enquiries and dedupe; appointment/Purchase inactive',status:'PASS'});
 await page.goto('https://mrsewingfashion.com/contact/',{waitUntil:'load'});
 await page.evaluate(()=>document.addEventListener('click',e=>{if(e.target.closest('a[href*="maps.app.goo.gl"]'))e.preventDefault();}));
 await page.locator('a[href*="maps.app.goo.gl/qz1GzkBunkmzVKXQ6"]').click();
 assert.equal(await page.evaluate(()=>dataLayer.filter(x=>x.event==='directions_click').length),1);
 result.checks.push({name:'approved actual directions link counts deliberate click, not map impression',status:'PASS'});
 const beforeBooking=vendor.length;await page.goto('https://mrsewingfashion.com/booking/',{waitUntil:'load'});
 await page.evaluate(()=>{for(const[id,value]of[['requestDate','2026-12-31'],['requestTime','12:00']]){const n=document.getElementById(id);if(n){n.value=value;n.dispatchEvent(new Event('change',{bubbles:true}));}}});
 assert.equal(vendor.length,beforeBooking);assert.equal(await page.evaluate(()=>dataLayer.filter(x=>['appointment_confirmed','quote_request_success','lead_form_success'].includes(x.event)).length),0);
 result.checks.push({name:'booking/date/time preferences are enquiries only; appointment conversion and SDKs remain inactive',status:'PASS'});
 await page.goto('https://mrsewingfashion.com/contact/',{waitUntil:'load'});
 await page.getByRole('button',{name:'Cookie preferences',exact:true}).click();const reloaded=page.waitForNavigation({waitUntil:'load'});await page.getByRole('button',{name:'Reject',exact:true}).click();await reloaded;const before=vendor.length;
 await page.reload({waitUntil:'load'});assert.equal(vendor.length,before);result.checks.push({name:'withdrawal and reload do not restart SDKs',status:'PASS'});
 const content=await page.locator('main').innerText();assert(content.length>20);
 await ctx.close();
 const stage=await b.newContext();let stageVendors=0;await stage.route('**/*',r=>{const u=new URL(r.request().url());if(u.origin===BASE)return r.continue();if(['www.googletagmanager.com','connect.facebook.net'].includes(u.hostname))stageVendors++;return r.abort();});const stagePage=await stage.newPage();await stagePage.goto(BASE+'/?tracking_preview=1');assert.equal(stageVendors,0);await stage.close();
 assert.deepEqual(result.errors,[]);result.status='PASS';
}catch(e){result.status='FAIL';result.failure={message:e.message,stack:e.stack};process.exitCode=1;}finally{await b.close();fs.writeFileSync(path.join(OUT,'results.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));}})();
