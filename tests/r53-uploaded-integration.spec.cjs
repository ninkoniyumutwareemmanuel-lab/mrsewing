/* R53 local browser checks; temporary fixtures and mocked external handoffs only. */
function library(){for(const name of['playwright','playwright-core','/workspace/tools/phase1/node_modules/playwright-core']){try{return require(name);}catch(e){if(e.code!=='MODULE_NOT_FOUND')throw e;}}throw Error('Playwright unavailable');}
const{chromium}=library(),assert=require('node:assert/strict'),fs=require('node:fs');
const BASE=process.env.REVIEW_BASE_URL||'http://127.0.0.1:8020',OUT='/workspace/review/r53-uploaded-integration-2026-11-19',SHOTS='/workspace/artifacts/r53-uploaded-integration';
const WIDTHS=[320,360,375,390,430,768,1024,1440],NOW=Date.parse('2026-11-19T10:00:00Z');
const raw=JSON.parse(fs.readFileSync('_data/collection-designs.json','utf8')).designs,ivory=raw.find(d=>d.id==='MS-169');
const company=JSON.parse(fs.readFileSync('_data/business.json','utf8')),phone=company.telephone.replace(/\D/g,'');
const record=JSON.parse(fs.readFileSync('_data/policy-documents.json','utf8')).documents['terms-and-conditions'].receivedVersions[0];
const fixtureImages=ivory.images.map(i=>({...i,url:'https://mrsewingfashion.com'+i.src}));
(async()=>{
 fs.mkdirSync(OUT,{recursive:true});fs.mkdirSync(SHOTS,{recursive:true});
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM_BINARY||'/usr/bin/chromium',args:['--no-sandbox']});
 const result={scope:'Local Chromium; company uploads remain held; temporary fixtures; external handoffs mocked',widths:[],scenarios:{},axeChecks:0,providerCalls:0,errors:[],missing:[],realMessages:false,realCalls:false,realSubmissions:false,stagingRendered:false};let page,fixtureFlow=false,sample,submitted,sent,providerCalls=0;
 try{
  const context=await browser.newContext({viewport:{width:390,height:900},reducedMotion:'reduce',timezoneId:'Africa/Kigali',hasTouch:true});
  await context.addInitScript(now=>{Date.now=()=>now;window.__opened=[];window.open=u=>{window.__opened.push(u);return null;};},NOW);
  const{handleSelected}=await import('../functions/_lib/selected-design-handler.js');
  const fixturePatch=html=>{
   html=html.replace(/(<script id="designSelectionData" type="application\/json">)(.*?)(<\/script>)/s,(_all,start,value,end)=>{const data=JSON.parse(value);if(data.designs[sample.designId])data.designs[sample.designId].images=fixtureImages;return start+JSON.stringify(data).replace(/</g,'\\u003c')+end;});
   html=html.replace(/(<script id="requestDesignMedia" type="application\/json">)(.*?)(<\/script>)/s,(_all,start,value,end)=>{const data=JSON.parse(value);if(data[sample.designId]){data[sample.designId].images=fixtureImages;data[sample.designId].image=fixtureImages[0].src;}return start+JSON.stringify(data).replace(/</g,'\\u003c')+end;});
   html=html.replace(/(<script id="design-data" type="application\/json">)(.*?)(<\/script>)/s,(_all,start,value,end)=>{const data=JSON.parse(value);data.design.images=fixtureImages;return start+JSON.stringify(data).replace(/</g,'\\u003c')+end;});
   const thumbs=fixtureImages.map((image,index)=>'<button type="button" data-photo="'+index+'" aria-label="View photograph '+(index+1)+'"><picture><img src="'+image.src+'" alt="Synthetic three-view fixture" width="'+image.width+'" height="'+image.height+'"></picture></button>').join('');
   return html.replace('<div class="design-thumbnails"></div>','<div class="design-thumbnails">'+thumbs+'</div>');
  };
  await context.route('**/*',async route=>{
   const request=route.request(),url=new URL(request.url());if(url.origin!==BASE)return route.abort();
   if(url.pathname==='/__r53-family-fixture/')return route.fulfill({status:200,contentType:'text/html',body:fs.readFileSync(OUT+'/family-fixture.html','utf8')});
   if(url.pathname==='/api/selected-design-request'){
    submitted=JSON.parse(request.postData());const response=await handleSelected(new Request(request.url(),{method:'POST',headers:{'Content-Type':'application/json',Origin:BASE},body:request.postData()}),'synthetic-r53-only',async(_url,options)=>{providerCalls++;sent=JSON.parse(options.body);return new Response('{"success":true}');},NOW);
    return route.fulfill({status:response.status,headers:Object.fromEntries(response.headers),body:await response.text()});
   }
   if(request.method()==='POST')throw Error('Unexpected unmockedPOST '+url.href);
   if(fixtureFlow&&url.pathname==='/assets/request-context.js'){
    const response=await route.fetch();let body=await response.text();
    let patched=0;body=body.replace(/(const enums=\{photo:)(\[[^\]]*\])/,(_all,prefix,encoded)=>{patched++;return prefix+JSON.stringify([...new Set([...JSON.parse(encoded),...fixtureImages.map(i=>i.url)])]);});assert.equal(patched,1,'patch the actual generated client whitelist only in the temporary fixture');
    return route.fulfill({response,body});
   }
   if(fixtureFlow&&request.resourceType()==='document'){const response=await route.fetch();return route.fulfill({response,body:fixturePatch(await response.text())});}
   return route.continue();
  });
  context.on('page',p=>{p.on('pageerror',e=>result.errors.push({url:p.url(),message:e.message}));p.on('response',r=>{if(r.url().startsWith(BASE)&&r.status()>=400&&!r.url().includes('/api/'))result.missing.push({url:r.url(),status:r.status()});});});
  page=await context.newPage();const at=async path=>{await page.goto(new URL(path,BASE).href);await page.waitForLoadState('domcontentloaded');};
  const overflow=async()=>assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),page.url()+' overflow'+page.viewportSize().width);
  const axe=async selector=>{await page.addScriptTag({path:'/workspace/tools/homepage-qa/node_modules/axe-core/axe.min.js'});const violations=await page.evaluate(async sel=>(await axe.run(document.querySelector(sel),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})).violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)})),selector);assert.deepEqual(violations,[]);result.axeChecks++;};
  const shot=async name=>{await page.locator('img[src]').evaluateAll(images=>images.forEach(i=>i.loading='eager'));await page.evaluate(async()=>Promise.all([...document.images].filter(i=>i.getAttribute('src')).map(i=>i.decode().catch(()=>{}))));await page.screenshot({path:SHOTS+'/'+name+'.png',fullPage:false});};
  for(const width of WIDTHS){
   await page.setViewportSize({width,height:900});await at('/');assert.equal(await page.locator('h1').innerText(),'Professional Tailor in Kigali, Rwanda');assert.equal(await page.locator('.home-showcase-card').count(),2);assert.equal(await page.locator('.home-fashion-showcase video').count(),0);assert(await page.locator('[data-tailoring-whatsapp="homepage-showcase"]').isVisible());await overflow();
   if([390,1440].includes(width)){await axe('.home-fashion-showcase');await shot('home-'+width);}
   await at('/showroom/');const media=await page.locator('#showroomData').evaluate(n=>JSON.parse(n.textContent).items);assert.equal(media.length,28);assert(!media.some(m=>Number(m.designId?.split('-')[1])>=152));sample=media.find(m=>m.designId==='MS-031')||media[0];assert.equal(await page.locator('.showroom-card').count(),28);await overflow();
   await at('/terms-and-conditions/');assert.equal(await page.locator('h1').count(),1);assert.equal(await page.locator('[data-policy-document-review="1.0"]').count(),1);assert.equal(await page.locator('[data-policy-document-current]').count(),0);
   const panel=page.locator('[data-policy-document-review="1.0"]');assert.equal(await panel.locator('object[type="application/pdf"]').getAttribute('data'),record.publishedPath+'#view=FitH');assert(await panel.locator('a[download]').count());assert(await panel.locator('a[target="_blank"]').count());
   const text=await page.locator('main').innerText();assert(text.includes('current online Terms'));assert(text.includes('official'));assert(!text.includes('registered on 19 November 2026'));await overflow();
   if([390,1440].includes(width)){await axe('[data-policy-document-review]');await shot('terms-'+width);}
   await at('/__r53-family-fixture/');assert.equal(await page.locator('.design-family-variant').count(),2);await page.locator('.design-family-variant').first().focus();await page.keyboard.press('Tab');assert.equal(await page.evaluate(()=>document.activeElement.className),'design-family-variant');await overflow();if([390,1440].includes(width)){await axe('main');await shot('family-fixture-'+width);}
   result.widths.push(width);
  }
  result.scenarios.presentation='PASS8widths/approved28only/heldvideosfallback/tailoringCTA/realPDFreviewandHTMLfallback/syntheticfamilykeyboard/nooverflow';
  await at('/terms-and-conditions/');const pdf=await page.evaluate(async path=>{const r=await fetch(path);return{status:r.status,type:r.headers.get('content-type'),prefix:(await r.text()).slice(0,8)};},record.publishedPath);assert.equal(pdf.status,200);assert(pdf.type.includes('application/pdf'));assert(pdf.prefix.startsWith('%PDF-1.7'));result.scenarios.pdf='PASSactualapproved5pagePDFHTTP200/object/open/download/effectivedatepending/currentHTMLretained;nativePDFzoomandassistivetechnologyarenotcertified';
  // Existing eligible selection/quotation remains usable with actual validation.
  await at('/showroom/');await page.evaluate(()=>{sessionStorage.clear();localStorage.clear();});await page.reload();await at(sample.detailUrl);await page.locator('[data-select-design="'+sample.designId+'"]').click();await page.locator('.selected-design-bar').click();await page.locator('[data-selected-continue]').click();await page.check('[name=sharedFabricChoice][value=advice]');await page.locator('#fabricChoiceForm [type=submit]').click();await page.locator('#requestCity').waitFor();
  async function fillForm(){for(const[id,value]of Object.entries({requestName:'Fictional R53 customer',requestPhone:'+250780000000',requestCountry:'Rwanda',requestCity:'Kigali',requestEmail:'r53@example.invalid',requestMessage:'Synthetic R53 no real enquiry'}))await page.fill('#'+id,value);await page.fill('#requestDate','2026-12-10');await page.fill('#requestCompletionTime','14:00');await page.selectOption('#requestMeasurementMethod','online');await page.selectOption('#requestDeliveryMethod','collection');await page.selectOption('#requestCollectionLocation',{index:1});await page.check('#requestConsent');}
  await fillForm();await page.click('#reviewRequest');await page.locator('#requestReview').waitFor({state:'visible'});await page.click('#sendRequest');await page.locator('#requestSuccess').waitFor({state:'visible'});assert.equal(providerCalls,1);assert.equal(submitted.selections[0].photo,sample.photographUrl);assert(sent['Selected Designs'].includes(sample.photographUrl));result.scenarios.existingQuotation='PASSexistingeligiblephotoselection/fabricadvice/completeactualvalidator/mockedprovider;noactualsubmission';
  // Conditional future-approved multi-view fixture: never add held company IDs
  // or photos to the actual backend allowlist or live page output.
  fixtureFlow=true;await at('/showroom/');await page.evaluate(()=>{sessionStorage.clear();localStorage.clear();});await page.reload();
  await at(new URL(sample.detailUrl,BASE).pathname+'?qa=r53-three-view');assert.equal(await page.locator('[data-photo]').count(),3);
  for(const index of[1,2]){await page.locator('[data-photo="'+index+'"]').click();await page.locator('#photo-viewer').waitFor({state:'visible'});await page.locator('#close-photo').click();await page.locator('[data-select-design="'+sample.designId+'"]').click();}
  const selected=await page.evaluate(()=>MrDesignSelections.read());assert.equal(selected.length,2);assert.deepEqual(selected.map(x=>x.photo),[fixtureImages[1].url,fixtureImages[2].url]);
  await page.locator('.selected-design-bar').click();await page.locator('[data-selection-list] article').first().waitFor({state:'visible'});assert.equal(await page.locator('[data-selection-list] article').count(),2);await page.locator('#selection-share-whatsapp').click();assert(await page.locator('#serviceTermsDialog [type=submit]').isDisabled());assert.equal(await page.evaluate(()=>window.__opened.length),0);await page.locator('#serviceTermsDialog input').check();await page.locator('#serviceTermsDialog [type=submit]').click();const shared=new URL(await page.evaluate(()=>window.__opened.at(-1)));assert.equal(shared.pathname,'/'+phone);for(const image of fixtureImages.slice(1))assert(shared.searchParams.get('text').includes(new URL(image.src,BASE).href));
  await page.locator('[data-selected-continue]').click();await page.check('[name=sharedFabricChoice][value=advice]');await page.locator('#fabricChoiceForm [type=submit]').click();await page.locator('#requestCity').waitFor();assert.deepEqual((await page.evaluate(()=>MrDesignSelections.read())).map(x=>x.photo),[fixtureImages[1].url,fixtureImages[2].url]);await fillForm();await page.click('#reviewRequest');await page.locator('#requestReview').waitFor({state:'visible'});
  const before=providerCalls;await page.click('#sendRequest');await page.waitForFunction(()=>{const status=document.getElementById('requestStatus');return status&&status.textContent.trim()&&!status.textContent.includes('Sending');});assert.equal(providerCalls,before,'unapproved fixture photos rejected before provider');assert.equal(await page.locator('#requestName').inputValue(),'Fictional R53 customer');assert.equal((await page.evaluate(()=>MrDesignSelections.read())).length,2);
  result.scenarios.threeViews='PASStemporarythreeIvoryviewclientfixture/exactphotographselection+sharing+fabric+review;actualbackendrejectsheldphotosbeforeproviderandpreservesdata;notcompanypublication';
  assert.deepEqual(result.errors,[]);assert.deepEqual(result.missing,[]);result.providerCalls=providerCalls;fs.writeFileSync(OUT+'/browser.json',JSON.stringify(result,null,2)+'\n');console.log('PASS R53local8widths/approvedPDFreview/familyfixture/heldgates/exact3viewfixture/existingmockquotation');
 }catch(error){result.failure={message:error.message,stack:error.stack};try{if(page)await page.screenshot({path:SHOTS+'/failure.png',fullPage:true});}catch{}fs.writeFileSync(OUT+'/browser-partial.json',JSON.stringify(result,null,2)+'\n');throw error;}finally{await browser.close();}
})().catch(error=>{console.error(error);process.exit(1)});
