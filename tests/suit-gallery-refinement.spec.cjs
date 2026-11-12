/* R42: all nine galleries, shared OFFER and preserved design-detail enquiry.
   Local Chromium; actual selected-design validator; email mocked, no real messages. */
const {chromium}=require('playwright');
const assert=require('node:assert/strict'),fs=require('node:fs');
const base=process.env.REVIEW_BASE_URL||'http://127.0.0.1:8020';
const model=JSON.parse(fs.readFileSync('_data/suit-reference-categories.json'));
const references=JSON.parse(fs.readFileSync('_data/request-reference-allowlist.json'));
const messages=JSON.parse(fs.readFileSync('_data/custom-tailoring-page.json')).announcement.messages;
const widths=[320,360,375,390,430,768,1024,1440];
const evidenceDir='/workspace/review/suit-gallery-refinement-2026-11-12';
const screenshotDir='/workspace/artifacts/suit-gallery-refinement';
(async()=>{
 fs.mkdirSync(evidenceDir,{recursive:true});fs.mkdirSync(screenshotDir,{recursive:true});
 const browser=await chromium.launch({executablePath:'/usr/bin/chromium',args:['--no-sandbox']});
 const evidence={widths,categories:model.categories.map(c=>c.route),galleryViews:0,decodedImages:0,detailNavigations:[],offerPages:[],axeChecks:0,errors:[],missing:[],realMessages:false};
 try{
  const context=await browser.newContext({viewport:{width:390,height:900},hasTouch:true,reducedMotion:'no-preference'});
  let sent,submitted,providerCalls=0;
  const {handleSelected}=await import('../functions/_lib/selected-design-handler.js');
  await context.route('**/*',async route=>{
   const req=route.request(),url=new URL(req.url());
   if(url.origin===base&&url.pathname==='/api/selected-design-request'){
    submitted=JSON.parse(req.postData());const result=await handleSelected(new Request(req.url(),{method:'POST',headers:{'content-type':'application/json',Origin:base},body:req.postData()}),'synthetic',async(_url,options)=>{sent=JSON.parse(options.body);providerCalls++;return new Response('{"success":true}')});
    return route.fulfill({status:result.status,headers:Object.fromEntries(result.headers),body:await result.text()});
   }
   return url.origin===base?route.continue():route.abort();
  });
  const page=await context.newPage();
  page.on('pageerror',e=>evidence.errors.push(e.message));
  page.on('response',r=>{if(r.url().startsWith(base)&&r.status()>=400)evidence.missing.push({url:r.url(),status:r.status()})});
  const noOverflow=async()=>assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),page.url()+' '+page.viewportSize().width+' overflow');
  async function offerCheck({scroll=true,reduced=false}={}){
   await page.waitForFunction(()=>document.documentElement.classList.contains('has-sticky-offer'));
   assert.equal(await page.locator('.announcement-bar').count(),1,'one shared announcement');
   assert.equal(await page.locator('#site-header>.announcement-bar').count(),1,'offer inside shared sticky stack');
   assert.equal(await page.locator('.announcement-label').innerText(),'OFFER');
   assert.deepEqual(await page.locator('.announcement-group:not([aria-hidden]) .announcement-message').allTextContents(),messages);
   assert.equal(await page.locator('.announcement-bar a,.announcement-bar button,.announcement-bar [tabindex]').count(),0);
   assert.equal(await page.locator('.announcement-track').evaluate(n=>getComputedStyle(n).animationDuration),'75s');
   const first=await page.locator('.announcement-label').boundingBox();
   if(!evidence.motionVerified){
    const before=await page.locator('.announcement-track').evaluate(n=>new DOMMatrixReadOnly(getComputedStyle(n).transform).m41);
    await page.waitForTimeout(120);await page.locator('.announcement-label').tap();await page.waitForTimeout(120);
    const motion=await page.locator('.announcement-track').evaluate(n=>({x:new DOMMatrixReadOnly(getComputedStyle(n).transform).m41,state:getComputedStyle(n).animationPlayState}));
    assert(motion.x<before,'right-to-left progress');assert.equal(motion.state,'running','touch must not freeze offer');evidence.motionVerified=true;
   }
   if(scroll)for(const y of[0,500,1600]){
    await page.evaluate(y=>scrollTo({top:y,behavior:'instant'}),y);
    const rect=await page.evaluate(()=>{const stack=document.getElementById('site-header').getBoundingClientRect(),head=document.querySelector('#site-header .homepage-header').getBoundingClientRect(),bar=document.querySelector('.announcement-bar').getBoundingClientRect(),label=document.querySelector('.announcement-label').getBoundingClientRect(),window=document.querySelector('.announcement-window').getBoundingClientRect();return {stackTop:stack.top,stackBottom:stack.bottom,headTop:head.top,headBottom:head.bottom,barTop:bar.top,barBottom:bar.bottom,labelLeft:label.left,labelTop:label.top,labelRight:label.right,windowLeft:window.left}});
    assert(Math.abs(rect.stackTop)<1&&Math.abs(rect.headTop)<1,'header remains visible');
    assert(Math.abs(rect.headBottom-rect.barTop)<1&&Math.abs(rect.barBottom-rect.stackBottom)<1,'offer flush below header');
    assert(rect.windowLeft>=rect.labelRight,'offer text cannot overlap fixed label');
    assert(Math.abs(rect.labelLeft-first.x)<1&&Math.abs(rect.labelTop-first.y)<1,'OFFER stationary');
   }
   if(reduced){
    await page.emulateMedia({reducedMotion:'reduce'});
    await page.waitForFunction(()=>!document.querySelector('.announcement-bar').hasAttribute('data-motion-ready'));
    assert.equal(await page.locator('.announcement-track').evaluate(n=>getComputedStyle(n).animationName),'none');
    assert.equal(await page.locator('.announcement-group[aria-hidden=true]').evaluate(n=>getComputedStyle(n).display),'none');
    for(const n of await page.locator('.announcement-group:not([aria-hidden]) .announcement-message').all())assert(await n.isVisible());
    const measured=await page.evaluate(()=>({header:Math.ceil(document.getElementById('site-header').getBoundingClientRect().height),offset:parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--offer-header-height'))}));
    assert(Math.abs(measured.header-measured.offset)<=1,'responsive anchor offset tracks combined header height');
    await noOverflow();await page.emulateMedia({reducedMotion:'no-preference'});
   }
   await noOverflow();
  }
  async function menuCheck(){
   await page.locator('.home-menu-toggle').tap();assert.equal(await page.locator('.home-menu-toggle').getAttribute('aria-expanded'),'true');assert(await page.locator('#home-navigation').isVisible());
   const geometry=await page.evaluate(()=>{const nav=document.getElementById('home-navigation').getBoundingClientRect(),header=document.getElementById('site-header').getBoundingClientRect();return{navTop:nav.top,navBottom:nav.bottom,headerBottom:header.bottom,viewport:innerHeight}});
   assert(geometry.navTop>=geometry.headerBottom-1,'mobile menu begins below entire header/OFFER stack');
   assert(geometry.navBottom<=geometry.viewport+1,'mobile menu remains inside viewport');
   await page.locator('.home-menu-toggle').tap();
  }
  for(const width of widths){
   await page.setViewportSize({width,height:900});
   for(const category of model.categories){
    await page.goto(base+category.route);await offerCheck({reduced:[320,390,1440].includes(width)});
    const cards=page.locator('.suit-design-card');assert.equal(await cards.count(),category.designIds.length);
    assert.equal(await page.locator('.suit-design-grid [data-select-design],.suit-design-grid button').count(),0);
    assert.deepEqual(await cards.evaluateAll(ns=>ns.map(n=>n.dataset.designId)),category.designIds);
    const intro=await page.locator('.suit-intro').innerText();assert(/design reference|design references/i.test(intro));assert(/stock|fabric availability/i.test(intro));
    const heading=page.locator('.suit-design-grid').locator('xpath=preceding-sibling::h2[1]');assert((await heading.innerText()).startsWith('Explore '));
    assert.equal((await page.locator('.suit-instructions').innerText()).trim(),'Tap a suit photograph to view its details.');
    for(let i=0;i<category.designIds.length;i++){
     const id=category.designIds[i],card=cards.nth(i),name=(await card.locator('h3').innerText()).trim();
     assert(name&&!/\bMS[-– ]?\d+\b/i.test(name),'human-readable suit name');
     assert.equal((await card.innerText()).trim(),name,'only name alongside photograph');
     assert(!/View Design|Select This Design|Reference MS-/i.test(await card.innerText()));
     assert.equal(await card.locator('p,button').count(),0,'no descriptions/reference labels/buttons');
     assert.equal(await card.evaluate(n=>n.tagName),'A');
     const target=new URL(await card.getAttribute('href'),base);assert.equal(target.pathname,references[id].route);assert.equal(target.searchParams.get('design'),id);
     await card.locator('img').evaluate(n=>{n.loading='eager';return n.decode()});evidence.decodedImages++;
    }
    await heading.evaluate(n=>n.scrollIntoView({block:'start',behavior:'instant'}));
    assert(await heading.evaluate(n=>n.getBoundingClientRect().top>=document.getElementById('site-header').getBoundingClientRect().bottom-1),'heading anchor not covered');
    if(width<700)await menuCheck();
    if([320,1440].includes(width)){
     await page.addScriptTag({path:'/workspace/tools/homepage-qa/node_modules/axe-core/axe.min.js'});
     assert.deepEqual(await page.evaluate(async()=>(await axe.run(document.querySelector('main'),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}})).violations.map(v=>v.id)),[]);evidence.axeChecks++;
    }
    if([390,1440].includes(width)&&['men-kaunda','women-single-breasted'].includes(category.id)){await page.evaluate(()=>scrollTo({top:0,behavior:'instant'}));await page.screenshot({path:screenshotDir+'/'+category.id+'-'+width+'.png',fullPage:true});}
    evidence.galleryViews++;
   }
  }
  // Every category photograph opens its original detail; keyboard activation included.
  for(const category of model.categories)for(const id of category.designIds){
   await page.goto(base+category.route);const card=page.locator('[data-design-id="'+id+'"]');await card.focus();assert.equal(await card.evaluate(n=>n===document.activeElement),true);await page.keyboard.press('Enter');await page.waitForURL(u=>u.pathname===references[id].route);
   const data=await page.locator('#design-data').evaluate(n=>JSON.parse(n.textContent).design);assert.equal(data.id,id);assert.equal(new URL(data.images[0].src,'https://mrsewingfashion.com').href,references[id].images[0].url);
   assert.equal(await page.locator('[data-select-design="'+id+'"]').count(),1);assert(await page.locator('.design-description').innerText());assert.equal(await page.locator('#open-photo').getAttribute('href'),references[id].image);
   assert(await page.locator('.design-related').count()>=1);await page.locator('#open-photo img').evaluate(n=>n.decode());await offerCheck({scroll:false});evidence.detailNavigations.push(id);
  }
  // Shared offer appears on both landing pages, main service and every published detail.
  for(const route of['/services/custom-tailoring/','/mensuits/','/womensuits/',...Object.values(references).map(x=>x.route)]){await page.goto(base+route);await offerCheck({scroll:false});evidence.offerPages.push(route);}
  for(const width of[320,390,768,1440]){await page.setViewportSize({width,height:900});for(const route of['/mensuits/','/womensuits/',references['MS-031'].route,references['MS-143'].route]){await page.goto(base+route);await offerCheck({reduced:true});}}
  for(const width of[320,390])for(const motion of['no-preference','reduce'])for(const route of['/mensuits/kaunda/','/womensuits/single-breasted/',references['MS-031'].route,references['MS-143'].route]){
   await page.setViewportSize({width,height:700});await page.emulateMedia({reducedMotion:motion});await page.goto(base+route);await page.waitForFunction(()=>document.documentElement.classList.contains('has-sticky-offer'));
   await page.waitForFunction(()=>Math.abs(Math.ceil(document.getElementById('site-header').getBoundingClientRect().height)-parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--offer-header-height')))<2);
   await menuCheck();evidence.menuGeometryChecks=(evidence.menuGeometryChecks||0)+1;
  }
  await page.emulateMedia({reducedMotion:'no-preference'});await page.setViewportSize({width:390,height:900});
  // Existing detail-only selection -> per-design fabric -> quote -> real validator/mock email.
  assert.equal(await page.evaluate(()=>MrDesignSelections.read().length),0);
  const selected=['MS-031','MS-143'];for(const id of selected){await page.goto(base+references[id].route);await page.locator('[data-select-design="'+id+'"]').click();}
  assert.equal(await page.evaluate(()=>MrDesignSelections.read().length),2);await page.locator('.selected-design-bar').click();await page.locator('[data-selection-list] article').first().waitFor();assert.equal(await page.locator('[data-selection-list] article').count(),2);await page.locator('[data-selected-continue]').click();
  await page.check('[name=fabric-0][value=now]');await page.locator('[data-fabric-choice-for="0"] a').click();await page.locator('[data-pick-fabric="men-wool"]').click();await page.waitForURL('**/services/custom-tailoring/fabric/**');await page.check('[name=fabric-1][value=own]');await page.locator('#fabricChoiceForm [type=submit]').click();await page.waitForURL('**/request/**');await page.waitForFunction(()=>!document.getElementById('reviewRequest').disabled);assert.equal(await page.locator('.batch-design-summary article').count(),2);
  for(const [id,value]of Object.entries({requestCountry:'Rwanda',requestDate:'2026-12-15',requestCompletionTime:'14:30',requestName:'Synthetic gallery QA',requestPhone:'+250780000000',requestLocation:'Kigali synthetic',requestMessage:'Synthetic mixed suit quote; do not send externally'}))await page.fill('#'+id,value);
  await page.check('#requestConsent');await page.click('#reviewRequest');for(const id of selected)assert.equal(await page.locator('#reviewDetails a').filter({hasText:'View selected photograph'}).evaluateAll((ns,url)=>ns.filter(n=>n.href===url).length,references[id].images[0].url),1);await page.click('#sendRequest');await page.locator('#requestSuccess').waitFor({state:'visible'});
  assert.equal(providerCalls,1);assert.deepEqual(submitted.selections.map(x=>x.design),selected);assert.equal(sent['Selected Design Count'],'2');for(const id of selected)assert(sent['Selected Designs'].includes(references[id].images[0].url));assert(sent['Selected Designs'].includes('Wool'));assert(sent['Selected Designs'].includes('Customer-Supplied Fabric'));
  evidence.quote='PASS detail-only selection preserves IDs/canonical originals through individual fabric/own-fabric choice, review and real server validator with mocked provider';
  assert.deepEqual(evidence.errors,[]);assert.deepEqual(evidence.missing,[]);
  fs.writeFileSync(evidenceDir+'/browser.json',JSON.stringify(evidence,null,2));console.log('PASS 9 galleries×8widths/27keyboard-detail mappings/28published detail+3landing OFFERs/75s/sticky+reducedmotion+menus/216decoded images/18Axe/detail-fabric-quote realvalidator mocked email; no real messages');
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exit(1)});
