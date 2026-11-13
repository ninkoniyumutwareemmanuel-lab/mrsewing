/* R48: one shared fabric/colour across the existing ordinary-suit enquiry.
   Local Chromium, real selected-design validator, mocked provider/apps only. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict'),fs=require('node:fs');
const base=process.env.REVIEW_BASE_URL||'http://127.0.0.1:8020';
const refs=JSON.parse(fs.readFileSync('_data/request-reference-allowlist.json'));
const model=JSON.parse(fs.readFileSync('_data/suit-reference-categories.json'));
const widths=[320,360,375,390,430,768,1024,1440];
const ids=[...model.categories.map(c=>c.coverDesignId),'MS-029'];
const reviewPath='/services/custom-tailoring/selected-designs/';
const fabricPath='/services/custom-tailoring/fabric/';
const out='/workspace/review/shared-fabric-journey-2026-11-13';
const shots='/workspace/artifacts/shared-fabric-journey';
const fictional={requestName:'Fictional shared-fabric customer',requestPhone:'+250780000000',requestCountry:'Rwanda',requestLocation:'Fictional Kigali delivery address',requestDate:'2026-12-20',requestCompletionTime:'14:30',requestMessage:'Fictional shared-fabric test; no actual customer submission.'};
const friendly=name=>String(name).replace(/\s*[—·-]\s*MS-\d+\b/g,'').trim();
(async()=>{
 fs.mkdirSync(out,{recursive:true});fs.mkdirSync(shots,{recursive:true});
 const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});
 const evidence={widths:[],scenarios:{},categories:model.categories.map(c=>c.id),errors:[],missing:[],axeChecks:0,providerCalls:0,realMessages:false,realSubmissions:false};
 try{
  const context=await browser.newContext({viewport:{width:390,height:900},hasTouch:true,reducedMotion:'reduce',timezoneId:'America/New_York'});
  await context.addInitScript(()=>{
   const now=Date.now.bind(Date);Date.now=()=>now()+Number(sessionStorage.getItem('__qa_time_offset')||0);
   window.__opened=[];window.open=(url,target,features)=>{window.__opened.push({url,target,features});return null;};
  });
  const {handleSelected}=await import('../functions/_lib/selected-design-handler.js');
  let submitted,sent,accept=false,providerCalls=0;
  await context.route('**/*',async route=>{
   const req=route.request(),u=new URL(req.url());
   if(u.origin!==base)return route.abort();
   if(u.pathname==='/api/selected-design-request'){
    submitted=JSON.parse(req.postData());
    const response=await handleSelected(new Request(req.url(),{method:'POST',headers:{'content-type':'application/json',Origin:base},body:req.postData()}),'synthetic',async(_url,options)=>{providerCalls++;sent=JSON.parse(options.body);return new Response(JSON.stringify({success:accept}),{status:200});});
    return route.fulfill({status:response.status,headers:Object.fromEntries(response.headers),body:await response.text()});
   }
   return route.continue();
  });
  const page=await context.newPage();
  page.on('pageerror',e=>evidence.errors.push(e.message));
  page.on('response',r=>{if(r.url().startsWith(base)&&r.status()>=400&&!r.url().includes('/api/'))evidence.missing.push({url:r.url(),status:r.status()});});
  const at=async path=>{await page.goto(new URL(path,base).href);await page.waitForLoadState('domcontentloaded');};
  const rows=()=>page.evaluate(()=>MrDesignSelections.read());
  const preference=()=>page.evaluate(()=>MrDesignSelections.fabricPreference());
  const identity=rows=>rows.map(({design,photo,quantity,project})=>({design,photo,quantity,project:project||null}));
  const bar=()=>page.locator('.selected-design-bar');
  async function noOverflow(){assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),page.url()+' overflow@'+page.viewportSize().width);}
  async function reset(){await at('/services/custom-tailoring/');await page.evaluate(()=>sessionStorage.clear());await page.reload();}
  async function select(id){await at(refs[id].route);await page.locator('[data-select-design="'+id+'"]').click();}
  async function review(){await bar().click();await page.waitForURL(u=>u.pathname===reviewPath);await page.locator('[data-selection-list] article').first().waitFor();assert.equal(await page.locator('.selected-design-bar:visible').count(),0);}
  async function toFabric(){await review();await page.locator('[data-selected-continue]').click();await page.waitForURL(u=>u.pathname===fabricPath);await page.locator('#fabricChoiceForm').waitFor();assert.equal(await page.locator('.selected-design-bar:visible').count(),0);}
  function prefRadio(choice){return page.locator('#fabricChoiceForm input[type=radio][value="'+choice+'"]');}
  function colourRadio(id){return page.locator('input[type=radio][value="'+id+'"]');}
  async function selectColour(id){const radio=colourRadio(id);await radio.locator('..').click();assert(await radio.isChecked());}
  function guideContinue(){return page.getByRole('link',{name:'Continue to Quotation',exact:true}).or(page.getByRole('button',{name:'Continue to Quotation',exact:true}));}
  async function fabricStep(count,total){
   assert.equal((await page.locator('main h1').innerText()).trim(),'Choose Your Fabric');
   assert.equal(await page.locator('#fabricChoiceForm input[type=radio]').count(),3,'one shared three-option question regardless of selection count');
   for(const choice of['now','advice','own'])assert.equal(await prefRadio(choice).count(),1);
   const text=await page.locator('main').innerText();assert(text.includes('Your Selected Designs'));assert(new RegExp(count+'\\s+design').test(text));assert(new RegExp(total+'\\s+garment').test(text));
   const details=page.locator('main details').first();assert.equal(await details.getAttribute('open'),null,'selected summary starts compact');await details.locator('summary').focus();await page.keyboard.press('Enter');assert.notEqual(await details.getAttribute('open'),null);assert(!/\bMS-\d+\b/.test(await details.innerText()));await details.locator('summary').focus();await page.keyboard.press('Enter');
   await noOverflow();if(page.viewportSize().width===320&&!evidence.fabricPreferenceAxe){await axeMain();evidence.fabricPreferenceAxe=true;}
  }
  async function choosePreference(choice){await prefRadio(choice).check();const label=choice==='now'?'Continue to Fabric Selection':'Continue to Quotation';const action=page.locator('#fabricChoiceForm').getByRole('button',{name:label,exact:true}).or(page.locator('#fabricChoiceForm').getByRole('link',{name:label,exact:true}));assert(await action.isVisible());await action.click();await page.waitForURL(u=>u.pathname===(choice==='now'?'/guides/fabrics/':'/request/'));}
  async function chooseFabric(id,colour='navy-blue'){
   const card=page.locator('[data-fabric-id="'+id+'"]');assert(await card.isVisible());await card.locator('[data-pick-fabric="'+id+'"]').click();
   const radio=colourRadio(colour);await radio.waitFor({state:'attached'});await selectColour(colour);if(page.viewportSize().width===320&&colour==='navy-blue'){await radio.focus();await page.keyboard.press('ArrowRight');assert(!(await radio.isChecked()),'native radio arrow navigation changes colour');await page.keyboard.press('ArrowLeft');assert(await radio.isChecked(),'native radio arrow navigation restores colour');}
   const label=page.locator('label').filter({has:radio});if(await label.count()){const box=await label.boundingBox();assert(box.width>=44&&box.height>=44,'swatch control has44px tap area');}
   const text=await page.locator('main').innerText();assert(/Selected Fabric:/i.test(text));assert(/Preferred Colour:/i.test(text));assert(/subject to availability|availability confirmation/i.test(text));assert(/illustrative|illustration|actual.*shade|shade.*differ/i.test(text));
   assert.equal(await page.locator('input[type=radio]:checked').count(),1,'one active preferred colour');
   const swatches=page.locator('.fabric-colour-swatch');assert.equal(await swatches.count(),23,'22 approved colours plus Other');for(const swatch of await swatches.all()){const size=await swatch.boundingBox();assert(size.width>=28&&size.width<=32&&size.height>=28&&size.height<=32,'compact illustrative30px swatch');}await noOverflow();if(page.viewportSize().width===320&&!evidence.colourSelectorAxe){await axeMain();evidence.colourSelectorAxe=true;}await guideContinue().click();await page.waitForURL(u=>u.pathname==='/request/');
  }
  async function checkQuote(count,total,{fabric,colour,label}={}){
   await page.locator('.selected-quote-summary').waitFor();assert.equal((await page.locator('main h1').innerText()).trim(),'Your Quotation Request');
   const details=page.locator('details.selected-quote-summary');assert.equal(await details.count(),1);assert.equal(await details.getAttribute('open'),null);assert(new RegExp(count+'\\s+design').test(await details.locator('summary').innerText()));assert(new RegExp(total+'\\s+garment').test(await details.locator('summary').innerText()));
   await details.locator('summary').click();assert.equal(await details.locator('.batch-design-summary article').count(),count);assert(!/\bMS-\d+\b/.test(await details.innerText()));await details.locator('summary').click();
   const text=await page.locator('main').innerText();if(fabric)assert(text.includes(fabric));if(colour)assert(text.includes(colour));if(label){if(label==='Help Me Choose Fabric')assert(/Help Me Choose (?:a )?Fabric/.test(text));else assert(text.includes(label));}
   assert.equal(await page.getByRole('link',{name:'Edit Fabric Preference',exact:true}).count(),1,'one shared preference edit action');
   assert.equal(await page.locator('#customerRequestForm input[type=radio]:visible').count(),0,'no repeated fabric or colour questions');
   for(const id of['requestPriority','requestAfterHours','requestGarment','requestFabric','requestFabricChoice','requestFabricSelection'])if(await page.locator('#'+id).count())assert(await page.locator('#'+id).isHidden()&&await page.locator('#'+id).isDisabled(),id+' hidden/disabled for selected suits');
   for(const id of['requestName','requestPhone','requestCountry','requestLocation','requestDate','requestCompletionTime'])assert.equal(await page.locator('#'+id).getAttribute('required'),'');
   assert.equal(await page.locator('#requestEmail').getAttribute('required'),null);assert.equal(await page.locator('#requestMessage').getAttribute('required'),null);
   assert(/Kigali/.test(text)&&/UTC\s*\+0?2/.test(text));assert(/confirm.*(?:possible|feasib)|(?:possible|feasib).*confirm/i.test(text));
   assert.equal(await page.locator('#reviewRequest').innerText(),'Review Quotation Request');
   assert.equal(await page.locator('.selected-design-bar:visible').count(),0);await noOverflow();
  }
  async function fillCustomer(){for(const[id,value]of Object.entries(fictional)){const input=page.locator('#'+id);if(await input.evaluate(n=>n.tagName)==='SELECT')await input.selectOption({label:value});else await input.fill(value);}await page.locator('#requestEmail').fill('');}
  async function axeMain(){await page.addScriptTag({path:'/workspace/tools/homepage-qa/node_modules/axe-core/axe.min.js'});const issues=await page.evaluate(async()=>(await axe.run(document.querySelector('main'),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})).violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)})));assert.deepEqual(issues,[]);evidence.axeChecks++;}
  // A/B/C: full existing route chain and all three preference paths at8widths.
  for(const width of widths){
   await page.setViewportSize({width,height:900});await reset();await at('/');const homeLink=page.locator('main a[href="/services/custom-tailoring/"]').first();await homeLink.click();await page.waitForURL(u=>u.pathname==='/services/custom-tailoring/');await page.getByRole('link',{name:/^Explore Men[’']s Suits$/}).first().click();await page.waitForURL(u=>u.pathname==='/mensuits/');
   const category=model.categories.find(c=>c.id==='men-double-breasted');await page.locator('.suit-category-card[href^="'+category.route+'"]').click();await page.locator('.suit-design-card').first().click();await page.locator('[data-select-design]').click();await select('MS-031');const selected=identity(await rows());await toFabric();await fabricStep(2,2);await choosePreference('now');await chooseFabric('men-wool');await checkQuote(2,2,{fabric:'Wool',colour:'Navy Blue'});assert.deepEqual(identity(await rows()),selected);assert.equal((await preference()).colour,'navy-blue');if([320,1440].includes(width))await axeMain();
   await reset();await select('MS-143');await toFabric();await fabricStep(1,1);await choosePreference('advice');await checkQuote(1,1,{label:'Help Me Choose Fabric'});assert.equal((await preference()).choice,'advice');
   await reset();await select('MS-031');await toFabric();await choosePreference('own');await checkQuote(1,1,{label:'I Have My Own Fabric'});assert.equal((await preference()).choice,'own');
   evidence.widths.push(width);console.log('PASS sharedfabric now/advice/own width '+width);
  }
  evidence.scenarios.ABC='PASSexistinghomepage-to-suit-category-detail-review-sharedfabric-guide-colour-quotation;advice+ownskipguide;all8widths';
  // D: ten mixed selections from every published category retain13garments.
  await page.setViewportSize({width:390,height:900});await reset();for(const id of ids)await select(id);assert.equal((await rows()).length,10);await review();const articles=page.locator('[data-selection-list] article');for(const[index,quantity]of[[0,'2'],[9,'3']]){await articles.nth(index).locator('input[type=number]').fill(quantity);await articles.nth(index).locator('input[type=number]').dispatchEvent('change');}const selected=identity(await rows());assert.equal(selected.reduce((n,r)=>n+r.quantity,0),13);
  await page.evaluate(()=>Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async value=>{window.__copied=value}}}));await page.locator('#selection-share-copy').click();const copied=await page.evaluate(()=>window.__copied);for(const row of selected)assert(copied.includes(new URL(refs[row.design].images[0].src,base).href));
  await page.locator('[data-selected-continue]').click();await page.waitForURL(u=>u.pathname===fabricPath);await fabricStep(10,13);await choosePreference('now');await chooseFabric('men-wool');await checkQuote(10,13,{fabric:'Wool',colour:'Navy Blue'});assert.deepEqual(identity(await rows()),selected);
  // The existing validated URL snapshot must recover every public selection and
  // shared preference when opened without the original session storage.
  const portableURL=page.url();for(const value of[fictional.requestName,fictional.requestPhone,fictional.requestLocation])assert(!decodeURIComponent(portableURL).includes(value),'quotation URL contains no private contact fields');
  const restoredContext=await browser.newContext({viewport:{width:390,height:900},reducedMotion:'reduce'});try{await restoredContext.route('**/*',r=>new URL(r.request().url()).origin===base?r.continue():r.abort());const restored=await restoredContext.newPage();await restored.goto(portableURL);await restored.locator('.selected-quote-summary').waitFor();assert.deepEqual(identity(await restored.evaluate(()=>MrDesignSelections.read())),selected);assert.deepEqual(await restored.evaluate(()=>MrDesignSelections.fabricPreference()),{choice:'now',fabricRef:'men-wool',colour:'navy-blue',colourDescription:''});}finally{await restoredContext.close();}
  await fillCustomer();
  // E: existing edit link retainsflow/designs/contactdraft and updates sharedchoice.
  await page.getByRole('link',{name:'Edit Fabric Preference',exact:true}).click();await page.waitForURL(u=>u.pathname===fabricPath);await fabricStep(10,13);await choosePreference('now');await chooseFabric('women-star','burgundy');await checkQuote(10,13,{fabric:'Star',colour:'Burgundy'});assert.deepEqual(identity(await rows()),selected);for(const[id,value]of Object.entries(fictional))assert.equal(await page.locator('#'+id).inputValue(),value,id+' restored after fabric edit');
  // Other colour is explicit, singular and requires a short safe description.
  await page.getByRole('link',{name:'Edit Fabric Preference',exact:true}).click();await choosePreference('now');await page.locator('[data-pick-fabric="men-wool"]').click();await selectColour('other');const custom=page.locator('[name="colourDescription"]');await custom.waitFor({state:'visible'});await guideContinue().click();assert.equal(new URL(page.url()).pathname,'/guides/fabrics/','missing custom colour blocks quotation');await custom.fill('<script>');await guideContinue().click();assert.equal(new URL(page.url()).pathname,'/guides/fabrics/','invalid custom colour blocks quotation');await custom.fill('Dusty mauve');await guideContinue().click();await page.waitForURL(u=>u.pathname==='/request/');await checkQuote(10,13,{fabric:'Wool',colour:'Dusty mauve'});assert.equal((await preference()).colourDescription,'Dusty mauve');
  // Return to the owner's NavyBlue scenario before payload verification.
  await page.getByRole('link',{name:'Edit Fabric Preference',exact:true}).click();await choosePreference('now');await chooseFabric('men-wool');await checkQuote(10,13,{fabric:'Wool',colour:'Navy Blue'});await fillCustomer();await page.check('#requestConsent');
  // F: eachrequiredfield andconsent preventsreview; optionalemail/messageallowed.
  for(const id of['requestName','requestPhone','requestCountry','requestLocation','requestDate','requestCompletionTime']){await page.locator('#'+id).fill('');await page.locator('#reviewRequest').click();assert(await page.locator('#customerRequestForm').isVisible());assert(await page.locator('#requestReview').isHidden());assert.equal(providerCalls,0);await page.locator('#'+id).fill(fictional[id]);}
  await page.locator('#requestConsent').uncheck();await page.locator('#reviewRequest').click();assert(await page.locator('#requestReview').isHidden());assert.equal(providerCalls,0);await page.locator('#requestConsent').check();await page.locator('#reviewRequest').click();await page.locator('#requestReview').waitFor({state:'visible'});const reviewText=await page.locator('#requestReview').innerText();assert(reviewText.includes('Wool')&&reviewText.includes('Navy Blue'));assert(!/\bMS-\d+\b/.test(reviewText));assert.equal(providerCalls,0);
  await page.locator('#sendRequest').click();await page.waitForFunction(()=>/did not confirm|could not confirm/i.test(document.getElementById('requestStatus').textContent));assert(await page.locator('#requestSuccess').isHidden());assert.equal(providerCalls,1);assert.deepEqual(identity(await rows()),selected);assert.equal((await preference()).colour,'navy-blue');
  await page.locator('#editRequest').click();for(const[id,value]of Object.entries(fictional))assert.equal(await page.locator('#'+id).inputValue(),value);await page.locator('#reviewRequest').click();accept=true;await page.locator('#sendRequest').click();await page.locator('#requestSuccess').waitFor({state:'visible'});assert.equal(providerCalls,2);assert.equal(submitted.selections.length,10);assert.deepEqual(identity(submitted.selections),selected);assert.deepEqual(submitted.fabricPreference,{choice:'now',fabricRef:'men-wool',colour:'navy-blue',colourDescription:''});assert.equal(sent['Total Garments'],'13');assert.equal(sent['Selected Design Count'],'10');assert(sent['Preferred Colour'].includes('Navy Blue'));for(const row of selected){assert(sent['Selected Designs'].includes(row.photo));assert(sent['Selected Designs'].includes('Quantity: '+row.quantity));assert(sent['Selected Design IDs'].includes(row.design));}assert.equal(sent['Requested Completion Time'],'14:30');assert.equal(sent['Requested Completion Time Zone'],'Africa/Kigali (UTC+02:00)');assert(!/inbox.*(?:received|delivered)|(?:received|delivered).*inbox/i.test(await page.locator('#requestSuccess').innerText()));
  const example={...sent};delete example.access_key;fs.writeFileSync(out+'/provider-example.json',JSON.stringify({request:{...submitted,fields:{...submitted.fields,access_key:undefined}},provider:example},null,2));evidence.scenarios.DEF='PASS10mixeddesigns/13garments/onequestion/onefabric-onecolour/Othercolour/editcontactpreservation/requiredcontacts+deadline+consent/completeexactpayload/falseproviderretry+mocksuccess';
  // G: standaloneguide remainsinformational without a broken selectorjourney.
  await reset();await at('/guides/fabrics/');assert.equal(await page.locator('[data-fabric-id]').count(),8);assert.equal(await page.locator('[data-pick-fabric]').count(),0);assert.equal(await page.locator('[data-own-fabric]').count(),0);assert.equal(await page.locator('.fabric-card a[href*="service-info-prices"]').count(),0);assert.equal(await page.getByText('View Fabric Details',{exact:true}).count(),8);assert(!/Express and children.s tailoring/i.test(await page.locator('main').innerText()));await noOverflow();await axeMain();
  evidence.scenarios.G='PASSstandalone8approvedfabriccards/details/photos/tiermapping;noquotationcontrols/noownfabricservicebutton/noirrelevantpromotions';
  // H: expiration and quotation isolation remain intact after shared preference.
  await reset();await select('MS-031');await select('MS-143');await at('/');await page.evaluate(()=>sessionStorage.setItem('__qa_time_offset','60000'));await at('/mensuits/');assert.equal((await rows()).length,2);await at('/');await page.evaluate(()=>sessionStorage.setItem('__qa_time_offset','181000'));await page.goBack();await page.waitForLoadState('domcontentloaded');assert.equal(await page.locator('.selected-design-bar:visible').count(),0);assert.equal((await rows()).length,0);
  await select('MS-031');await toFabric();await choosePreference('advice');const closedQuote=page.url();await page.goBack();await page.waitForLoadState('domcontentloaded');assert.equal(await page.locator('.selected-design-bar:visible').count(),0);await at(closedQuote);assert.equal((await preference()).choice,'advice');assert.equal((await rows()).length,1);
  // A fresh browsing/quotation flow must not overwrite a prior shared preference.
  await select('MS-143');assert.equal((await rows()).length,1);await toFabric();await choosePreference('own');const secondQuote=page.url();assert.equal((await preference()).choice,'own');await at(closedQuote);assert.equal((await preference()).choice,'advice');assert.equal((await rows())[0].design,'MS-031');await at(secondQuote);assert.equal((await preference()).choice,'own');assert.equal((await rows())[0].design,'MS-143');
  for(const path of['/services/custom-tailoring/special-order/','/request/alterations/','/request/garment-care/','/request/mobile-fitting/','/request/vip/']){await at(path);await page.locator('#customerRequestForm').waitFor();assert.equal(await page.locator('#requestCountry,#requestCompletionTime').count(),0,'selected-only fields absent on '+path);for(const id of['requestPriority','requestAfterHours','requestGarment'])assert(await page.locator('#'+id).count()>0,path+' preserves '+id);await noOverflow();}
  for(const path of['/faq/','/terms-and-conditions/','/shop/','/measurements/']){await at(path);await noOverflow();}
  evidence.scenarios.H='PASS60return/121expiry/Backclosedsession/twoindependentquotationpreferences/unrelatedSpecialAlterationsCareMobileVIPforms/FAQTermsShopMeasurementsnavigation';
  // Denied persistence must not break the immediate existing URL-based journey.
  const denied=await browser.newContext({viewport:{width:390,height:900},reducedMotion:'reduce'});try{
   await denied.addInitScript(()=>{for(const method of['getItem','setItem','removeItem']){const original=Storage.prototype[method];Storage.prototype[method]=function(key,...rest){if(String(key).startsWith('mrsewing-'))throw new DOMException('QA storage denied','SecurityError');return original.call(this,key,...rest);};}});
   await denied.route('**/*',r=>new URL(r.request().url()).origin===base?r.continue():r.abort());const p=await denied.newPage(),errors=[];p.on('pageerror',e=>errors.push(e.message));await p.goto(base+refs['MS-031'].route);await p.locator('[data-select-design]').click();await p.locator('.selected-design-bar').click();await p.locator('[data-selected-continue]').click();await p.waitForURL(u=>u.pathname===fabricPath);await p.locator('[name=sharedFabricChoice][value=own]').check();await p.locator('#fabricChoiceForm').getByRole('button',{name:'Continue to Quotation',exact:true}).click();await p.waitForURL(u=>u.pathname==='/request/');await p.locator('.selected-quote-summary').waitFor();assert.equal((await p.evaluate(()=>MrDesignSelections.fabricPreference())).choice,'own');assert.equal((await p.evaluate(()=>MrDesignSelections.read()))[0].design,'MS-031');assert.deepEqual(errors,[]);evidence.scenarios.storage='PASS immediate valid design/preference URL transport with browser storage denied; persisted cross-navigation expiry cannot be guaranteed without persistence';
  }finally{await denied.close();}
  // Capture honestlocalrendering evidence; reducedmotion intentionallykeepsOFFERstatic.
  await reset();await select('MS-031');await toFabric();for(const width of[390,1440]){await page.setViewportSize({width,height:900});await page.evaluate(()=>scrollTo({top:0,behavior:'instant'}));await page.screenshot({path:shots+'/shared-preference-'+width+'.png',fullPage:true});}await choosePreference('now');await page.locator('[data-pick-fabric="men-wool"]').click();await selectColour('navy-blue');for(const width of[390,1440]){await page.setViewportSize({width,height:900});await page.locator('img').evaluateAll(async ns=>{for(const n of ns){n.loading='eager';await n.decode().catch(()=>{});}});await page.evaluate(()=>scrollTo({top:0,behavior:'instant'}));await page.screenshot({path:shots+'/fabric-colour-'+width+'.png',fullPage:true});}await guideContinue().click();await page.waitForURL(u=>u.pathname==='/request/');await checkQuote(1,1,{fabric:'Wool',colour:'Navy Blue'});for(const width of[390,1440]){await page.setViewportSize({width,height:900});await page.evaluate(()=>scrollTo({top:0,behavior:'instant'}));await page.screenshot({path:shots+'/quotation-'+width+'.png',fullPage:true});}
  evidence.providerCalls=providerCalls;assert.deepEqual(evidence.errors,[]);assert.deepEqual(evidence.missing,[]);fs.writeFileSync(out+'/browser.json',JSON.stringify(evidence,null,2));console.log('PASSsharedfabric+colourall8widths/A-H/exact10designs13garments/realvalidator-mockprovider/requiredfields/edits/standaloneguide/selectionexpiry/unrelatedforms;no real messages');
 }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exit(1)});
