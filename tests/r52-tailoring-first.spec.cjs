/* R52 local browser checks. WhatsApp and provider interactions are mocked. */
function library(){for(const name of['playwright','playwright-core','/workspace/tools/phase1/node_modules/playwright-core']){try{return require(name);}catch(e){if(e.code!=='MODULE_NOT_FOUND')throw e;}}throw Error('Playwright is required; no installation occurs in this test.');}
const {chromium}=library();
const assert=require('node:assert/strict'),fs=require('node:fs');
const BASE=process.env.REVIEW_BASE_URL||'http://127.0.0.1:8020',OUT='/workspace/review/r52-tailoring-first-2026-11-19',SHOTS='/workspace/artifacts/r52-tailoring-first';
const WIDTHS=[320,360,375,390,430,768,1024,1440],NOW=Date.parse('2026-11-19T10:00:00Z');
const business=JSON.parse(fs.readFileSync('_data/business.json','utf8')),phone=business.telephone.replace(/\D/g,'');
const config=JSON.parse(fs.readFileSync('_data/tailoring-positioning.json','utf8'));
const identity=rows=>rows.map(({design,photo,quantity})=>({design,photo,quantity}));
(async()=>{
 fs.mkdirSync(OUT,{recursive:true});fs.mkdirSync(SHOTS,{recursive:true});
 const browser=await chromium.launch({executablePath:process.env.CHROMIUM_BINARY||'/usr/bin/chromium',args:['--no-sandbox']});
 const result={scope:'Local Chromium, external interactions mocked',widths:[],scenarios:{},errors:[],missing:[],axeChecks:0,realMessages:false,realCalls:false,realSubmissions:false,stagingRendered:false};let page;
 try{
  const context=await browser.newContext({viewport:{width:390,height:900},hasTouch:true,reducedMotion:'reduce',timezoneId:'Africa/Kigali'});
  await context.addInitScript(({now,eventName})=>{Date.now=()=>now;window.__opened=[];window.__events=[];window.open=(url)=>{window.__opened.push(url);return null;};document.addEventListener(eventName,e=>window.__events.push(e.detail));},{now:NOW,eventName:config.measurement.eventName});
  let providerCalls=0,submitted,sent;
  const references=JSON.parse(fs.readFileSync('_data/request-reference-allowlist.json','utf8'));
  const {handleSelected}=await import('../functions/_lib/selected-design-handler.js');
  await context.route('**/*',async route=>{
   const request=route.request(),url=new URL(request.url());if(url.origin!==BASE)return route.abort();
   if(url.searchParams.get('qa')==='r52-two-photo'){
    // Synthetic two-photo published-data fixture only; no company record changes.
    const response=await route.fetch();let html=await response.text(),fixture;
    html=html.replace(/(<script id="design-data" type="application\/json">)(.*?)(<\/script>)/s,(_all,start,json,end)=>{fixture=JSON.parse(json);const other=Object.values(references).find(r=>r.images[0].src!==fixture.design.images[0].src).images[0];fixture.design.images.push(other);return start+JSON.stringify(fixture).replace(/</g,'\\u003c')+end;});
    assert(fixture,'synthetic design data fixture exists');
    const thumbs=fixture.design.images.map((i,index)=>'<button type="button" data-photo="'+index+'" aria-label="View photograph '+(index+1)+'"><picture><img src="'+i.src+'" alt="'+i.alt+'" width="'+i.width+'" height="'+i.height+'"></picture></button>').join('');
    html=html.replace('<div class="design-thumbnails"></div>','<div class="design-thumbnails">'+thumbs+'</div>');
    return route.fulfill({status:200,contentType:'text/html',body:html});
   }
   if(url.pathname==='/api/selected-design-request'){
    submitted=JSON.parse(request.postData());
    const response=await handleSelected(new Request(request.url(),{method:'POST',headers:{'Content-Type':'application/json',Origin:BASE},body:request.postData()}),'synthetic-r52-key',async(_url,options)=>{providerCalls++;sent=JSON.parse(options.body);return new Response(JSON.stringify({success:true}));},NOW);
    return route.fulfill({status:response.status,headers:Object.fromEntries(response.headers),body:await response.text()});
   }
   if(request.method()==='POST')throw Error('Unexpected unmockedPOST '+url.href);
   return route.continue();
  });
  context.on('page',p=>{p.on('pageerror',e=>result.errors.push({url:p.url(),message:e.message}));p.on('response',r=>{if(r.url().startsWith(BASE)&&r.status()>=400&&!r.url().includes('/api/'))result.missing.push({url:r.url(),status:r.status()});});});
  page=await context.newPage();
  const at=async path=>{await page.goto(new URL(path,BASE).href);await page.waitForLoadState('domcontentloaded');};
  const screenshot=async name=>{await page.locator('img').evaluateAll(images=>images.forEach(i=>i.loading='eager'));await page.waitForFunction(()=>[...document.images].every(i=>i.complete),null,{timeout:15000});const imageFailures=await page.locator('img[src]').evaluateAll(images=>images.filter(i=>i.getAttribute('src')&&!i.naturalWidth).map(i=>i.src));assert.deepEqual(imageFailures,[]);await page.screenshot({path:SHOTS+'/'+name+'.png',fullPage:true});};
  const overflow=async()=>assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),page.url()+' overflow'+page.viewportSize().width);
  const axe=async selector=>{await page.addScriptTag({path:'/workspace/tools/homepage-qa/node_modules/axe-core/axe.min.js'});const violations=await page.evaluate(async sel=>(await window.axe.run(document.querySelector(sel),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})).violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)})),selector);assert.deepEqual(violations,[]);result.axeChecks++;};
  const consent=async selector=>{
   const previous=await page.evaluate(()=>window.__opened.length);await page.locator(selector).first().click();await page.locator('#serviceTermsDialog').waitFor({state:'visible'});
   assert(await page.locator('#serviceTermsDialog button[type=submit]').isDisabled());assert.equal(await page.evaluate(()=>window.__opened.length),previous);
   await page.locator('#serviceTermsDialog input[type=checkbox]').check();await page.locator('#serviceTermsDialog button[type=submit]').click();
   assert.equal(await page.evaluate(()=>window.__opened.length),previous+1,'single manual handoff');
   const url=new URL(await page.evaluate(()=>window.__opened.at(-1)));assert.equal(url.origin,'https://wa.me');assert.equal(url.pathname,'/'+phone);return url.searchParams.get('text')||'';
  };
  await at('/showroom/');const media=await page.locator('#showroomData').evaluate(n=>JSON.parse(n.textContent).items);assert.equal(media.length,28);
  const sample=media.find(x=>x.designId==='MS-031')||media[0];
  for(const width of WIDTHS){
   await page.setViewportSize({width,height:900});await at('/');
   assert.equal(await page.locator('h1').count(),1);assert.equal(await page.locator('h1').innerText(),'Professional Tailor in Kigali, Rwanda');
   assert.equal(await page.locator('.home-showcase-card').count(),2);assert.equal(await page.locator('.home-showcase-feature').count(),1);assert.equal(await page.locator('.home-fashion-showcase video').count(),0);
   assert(await page.locator('[data-tailoring-whatsapp="homepage-showcase"]').isVisible());assert(await page.locator('[data-tailoring-whatsapp="homepage-design-card"]').isVisible());
   assert.equal(await page.locator('.home-design-sharing').evaluate(n=>n.previousElementSibling?.className),'home-fashion-showcase');
   const action=page.locator('[data-tailoring-whatsapp="homepage-showcase"]');assert((await action.boundingBox()).height>=44);assert.equal(await action.innerText(),config.whatsapp.label);
   await overflow();if([390,1440].includes(width)){await axe('.home-fashion-showcase');await axe('.home-design-sharing');await screenshot('home-'+width);}
   await at('/services/custom-tailoring/');assert.equal(await page.locator('h1').innerText(),'Tailoring Services');assert.equal(await page.locator('.tailoring-category-card').count(),3);
   assert.deepEqual(await page.locator('.tailoring-category-card h3').allTextContents(),['Suit Tailoring','Special Tailoring','Alterations & Repairs']);
   for(const href of['/services/custom-tailoring/design-choice/','/services/custom-tailoring/special-order/','/services/alterations/'])assert(await page.locator('.tailoring-category-card a[href="'+href+'"]').count());
   assert(await page.locator('[data-tailoring-whatsapp="tailoring-services"]').isVisible());await overflow();if([390,1440].includes(width)){await axe('.tailoring-categories');await screenshot('service-'+width);}
   for(const path of['/mensuits/','/womensuits/','/services/custom-tailoring/special-order/','/showroom/',sample.detailUrl]){await at(path);await overflow();assert.equal(await page.locator('h1').count(),1);assert(await page.locator('[data-tailoring-whatsapp]').count(),path+' CTA');if(path===sample.detailUrl&&[390,1440].includes(width))await screenshot('detail-'+width);}
   result.widths.push(width);
  }
  result.scenarios.presentation='PASS8widths/tailorH1/2approvedcards+feature/designcardnormalflow/3servicegroups/existingroutes/nooverflow';
  await page.setViewportSize({width:390,height:900});await at('/');const generic=await consent('[data-tailoring-whatsapp="homepage-showcase"]');assert.equal(generic,config.whatsapp.message);assert((await page.locator('.home-design-sharing').innerText()).includes('Attach your photograph'));
  const hooks=await page.evaluate(()=>window.__events);assert.equal(hooks.length,1);assert.equal(hooks[0].context,'homepage-showcase');assert(!JSON.stringify(hooks).includes('customer'));
  await at(sample.detailUrl);await page.locator('[data-tailoring-whatsapp="design-detail"]').waitFor();
  const designMessage=await consent('[data-tailoring-whatsapp="design-detail"]');const detail=new URL(sample.detailUrl,BASE);assert(designMessage.includes(new URL(new URL(sample.photographUrl).pathname,BASE).href));assert(designMessage.includes(new URL(detail.pathname,BASE).href));assert(designMessage.includes(sample.title));assert(!/MS-\d{3}/.test(designMessage));assert(designMessage.includes(config.whatsapp.previewNotice));
  // Unapproved query photo must not become a WhatsApp reference.
  await at(new URL(detail.pathname,BASE).pathname+'?design='+sample.designId+'&photo='+encodeURIComponent('https://example.invalid/private-photo.jpeg'));
  const invalidMessage=await consent('[data-tailoring-whatsapp="design-detail"]');assert(!invalidMessage.includes('example.invalid'));assert(invalidMessage.includes(new URL(new URL(sample.photographUrl).pathname,BASE).href));
  await at(detail.pathname+'?qa=r52-two-photo');
  const synthetic=await page.locator('#design-data').evaluate(n=>JSON.parse(n.textContent).design);assert.equal(synthetic.images.length,2);
  await page.locator('[data-photo="1"]').click();await page.locator('#photo-viewer').waitFor({state:'visible'});await page.locator('#close-photo').click();
  const alternateMessage=await consent('[data-tailoring-whatsapp="design-detail"]');
  assert(alternateMessage.includes(new URL(synthetic.images[1].src,BASE).href),'synthetic approved thumbnail retains exact alternate image');
  assert(!alternateMessage.includes(new URL(synthetic.images[0].src,BASE).href),'old photograph is not retained after thumbnail change');
  result.scenarios.photoChange='PASS temporary intercepted two-photo design fixture using existing files; actual company allowlist has one approved photograph per design, no publication/data modified';
  result.scenarios.whatsapp='PASSconfiguredofficialnumber/genericandexactapproveddesignlinks/stagingnotice/uncheckedTerms/singlemockmanualhandoff/invalidphotorejected/localnonPIIeventonly';
  // Preserve mixed selections and the existing website quotation alternative.
  await at('/showroom/');await page.evaluate(()=>{sessionStorage.clear();localStorage.clear();});await page.reload();
  const chosen=[media.find(x=>x.audience==='men'),media.find(x=>x.audience==='women')];
  for(const item of chosen){await at(item.detailUrl);await page.locator('[data-select-design="'+item.designId+'"]').click();}
  await at('/showroom/');await page.locator('.selected-design-bar').click();await page.waitForURL(u=>u.pathname==='/services/custom-tailoring/selected-designs/');
  assert.equal(await page.locator('[data-selection-list] article').count(),2);await page.locator('[data-selection-list] article input').first().fill('2');await page.locator('[data-selection-list] article input').first().dispatchEvent('change');
  const selections=await page.evaluate(()=>MrDesignSelections.read());assert.equal(selections.reduce((sum,x)=>sum+x.quantity,0),3);
  await page.locator('#selection-share-whatsapp').click();await page.locator('#serviceTermsDialog').waitFor({state:'visible'});assert(await page.locator('#serviceTermsDialog button[type=submit]').isDisabled());await page.locator('#serviceTermsDialog input').check();await page.locator('#serviceTermsDialog button[type=submit]').click();
  const shared=new URL(await page.evaluate(()=>window.__opened.at(-1))).searchParams.get('text');for(const item of chosen)assert(shared.includes(new URL(new URL(item.photographUrl).pathname,BASE).href));
  await page.locator('[data-selected-continue]').click();await page.check('[name=sharedFabricChoice][value=advice]');await page.locator('#fabricChoiceForm [type=submit]').click();await page.waitForURL(u=>u.pathname==='/request/');await page.locator('#requestCity').waitFor();
  assert.deepEqual(identity(await page.evaluate(()=>MrDesignSelections.read())),identity(selections));
  for(const [id,value]of Object.entries({requestName:'Fictional R52 customer',requestPhone:'+250780000000',requestCountry:'Rwanda',requestCity:'Kigali',requestEmail:'r52@example.invalid',requestMessage:'Synthetic R52 design requirements'}))await page.fill('#'+id,value);
  await page.fill('#requestDate','2026-12-10');await page.fill('#requestCompletionTime','14:00');await page.selectOption('#requestMeasurementMethod','online');await page.selectOption('#requestDeliveryMethod','collection');await page.selectOption('#requestCollectionLocation',{index:1});await page.check('#requestConsent');
  await page.click('#reviewRequest');await page.locator('#requestReview').waitFor({state:'visible'});await page.click('#sendRequest');await page.locator('#requestSuccess').waitFor({state:'visible'});
  assert.equal(providerCalls,1);assert.deepEqual(identity(submitted.selections),identity(selections));assert.equal(submitted.fabricPreference.choice,'advice');assert.equal(sent['Total Garments'],'3');for(const item of chosen)assert(sent['Selected Designs'].includes(item.photographUrl));
  result.scenarios.quotation='PASSmixedmenwomen/exactphotos/quantities/reviewsharingTerms/fabricadvice/existingquote/review/actualvalidator/mockprovider/fullcanonicalpayload';
  assert.deepEqual(result.errors,[]);assert.deepEqual(result.missing,[]);result.providerCalls=providerCalls;fs.writeFileSync(OUT+'/browser.json',JSON.stringify(result,null,2)+'\n');console.log('PASS R52 local8widths/CTAconsent/approveddesignreferences/websitequotation; mockedexternalonly');
 }catch(error){result.failure={message:error.message,stack:error.stack};try{if(page)await page.screenshot({path:SHOTS+'/failure.png',fullPage:true});}catch{}fs.writeFileSync(OUT+'/browser-partial.json',JSON.stringify(result,null,2)+'\n');throw error;}finally{await browser.close();}
})().catch(error=>{console.error(error);process.exit(1)});
