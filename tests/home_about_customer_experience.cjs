/* Local Home/About browser regression. External requests and submissions are blocked. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
function browserLibrary(){for(const name of ['playwright','playwright-core','/workspace/tools/phase1/node_modules/playwright-core']){try{return require(name)}catch(e){if(e.code!=='MODULE_NOT_FOUND')throw e}}throw Error('Install the existing Playwright dependency.');}
const {chromium}=browserLibrary();
const BASE=(process.env.REVIEW_BASE_URL||'http://127.0.0.1:8020').replace(/\/$/,''),OUT=process.env.REVIEW_ARTIFACTS||path.join(__dirname,'../artifacts/home-about-customer-experience');
const widths=[320,390,768,1440],results={layer:'Local Chromium; all external traffic blocked',widths,views:[],axe:[],errors:[],missing:[],realSubmissions:false};
const axeCandidates=[process.env.AXE_PATH,'/workspace/tools/homepage-qa/node_modules/axe-core/axe.min.js'].filter(Boolean);let axePath=axeCandidates.find(p=>fs.existsSync(p));
if(!axePath){try{axePath=require.resolve('axe-core/axe.min.js')}catch{}}
(async()=>{fs.mkdirSync(OUT,{recursive:true});const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_BINARY||(fs.existsSync('/usr/bin/chromium')?'/usr/bin/chromium':undefined),args:['--no-sandbox']});try{
 const context=await browser.newContext({reducedMotion:'reduce'});
 await context.route('**/*',r=>new URL(r.request().url()).origin===BASE?r.continue():r.abort());
 const page=await context.newPage();page.on('pageerror',e=>results.errors.push(e.message));page.on('response',r=>{if(r.url().startsWith(BASE)&&r.status()>=400)results.missing.push({url:r.url(),status:r.status()})});
 for(const width of widths){
  await page.setViewportSize({width,height:900});await page.goto(BASE+'/',{waitUntil:'domcontentloaded'});
  const feature=page.locator('.tailoring-feature-photo');await feature.scrollIntoViewIfNeeded();await feature.locator('img').evaluate(i=>i.decode());
  assert.equal(await feature.getAttribute('href'),'/services/custom-tailoring/');
  assert((await feature.locator('img').getAttribute('srcset')).includes('/r4.jpeg'),'original approved photograph remains available through responsive sources');
  assert(/light.*jacket.*trousers/i.test(await feature.locator('img').getAttribute('alt')),'approved library description replaces separately editable home alt');
  assert.equal(await feature.locator('img').evaluate(i=>getComputedStyle(i).objectFit),'contain','full original portrait must remain visible');
  if(width<=760){const box=await feature.locator('img').boundingBox();assert(Math.abs(box.width/box.height-1792/2400)<.02,'mobile uses original portrait proportions');}
  assert.equal(await page.locator('h1').count(),1);assert.equal(await page.locator('.tailoring-primary-card').count(),4);
  assert.equal(await page.locator('[data-moving-gallery]').count(),2);
  assert.equal(await page.locator('#tailoring-final a[href="/request/?general=1"]').innerText(),'Request a Quote');
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'home overflow '+width);
  if([390,1440].includes(width)){await feature.screenshot({path:path.join(OUT,'feature-'+width+'.png')});await page.screenshot({path:path.join(OUT,'homepage-'+width+'.png'),fullPage:true});}
  results.views.push({page:'Home',width,status:'PASS'});

  await page.goto(BASE+'/about/',{waitUntil:'domcontentloaded'});const text=await page.locator('main').innerText();
  assert.equal(await page.locator('h1').count(),1);for(const title of ['Our Story','Our Mission','Our Vision','What We Stand For','Our Services','Company Information'])assert(text.toLowerCase().includes(title.toLowerCase()),title);
  assert(text.includes('Mr Sewing Fashion')&&text.includes('NINKONIYUMUTWARE NEXUS LTD')&&text.includes('Kigali, Rwanda'));
  assert(!/CEO|Chief Executive|Founder|pending.owner|placeholder|test biography|2019|father/i.test(text),'no unsupported leadership/history/developer copy');
  assert.equal(await page.locator('.about-leadership').count(),0,'unapproved profile stays entirely absent');
  assert.equal(await page.locator('.about-values li').count(),5);assert.equal(await page.locator('.about-services article').count(),5);
  assert.deepEqual(await page.locator('.about-services a').evaluateAll(a=>a.map(x=>new URL(x.href).pathname)),['/services/custom-tailoring/','/services/alterations/','/services/garment-care/','/services/mobile-fitting/','/services/vip/']);
  assert.equal(await page.locator('link[rel=canonical]').getAttribute('href'),'https://mrsewingfashion.com/about/');
  const schema=JSON.parse(await page.locator('script[type="application/ld+json"]').first().textContent());assert(!JSON.stringify(schema).match(/foundingDate|"founder"|aggregateRating/));
  const logo=page.locator('.about-company-mark img');await logo.scrollIntoViewIfNeeded();await logo.evaluate(i=>i.decode());assert((await logo.boundingBox()).width<=141,'operating-company logo is subordinate');
  const picker=page.locator('[data-service-picker]');assert.equal(await picker.count(),1);await picker.locator('summary').focus();await page.keyboard.press('Enter');assert(await picker.evaluate(e=>e.open));
  assert.equal(await picker.locator('a').count(),5);await page.keyboard.press('ArrowDown');assert(await picker.locator('a').first().evaluate(e=>e===document.activeElement));await page.keyboard.press('Escape');assert(!(await picker.evaluate(e=>e.open)));
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'About overflow '+width);
  if([390,1440].includes(width)){await page.screenshot({path:path.join(OUT,'about-'+width+'.png'),fullPage:true});if(axePath){await page.addScriptTag({path:axePath});const violations=await page.evaluate(async()=>{const r=await axe.run(document.querySelector('main'),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}});return r.violations.map(v=>({id:v.id,targets:v.nodes.map(n=>n.target)}))});results.axe.push({page:'About',width,violations});assert.equal(violations.length,0,JSON.stringify(violations));}}
  results.views.push({page:'About',width,status:'PASS'});
 }
 assert.deepEqual(results.errors,[]);assert.deepEqual(results.missing,[]);
 results.axeStatus=axePath?'PASS':'NOT TESTED — axe-core unavailable';results.status='PASS';
}finally{await browser.close();fs.writeFileSync(path.join(OUT,'results.json'),JSON.stringify(results,null,2));}
console.log(JSON.stringify(results,null,2));})().catch(e=>{results.status='FAIL';results.failure=e.message;fs.mkdirSync(OUT,{recursive:true});fs.writeFileSync(path.join(OUT,'results.json'),JSON.stringify(results,null,2));console.error(e);process.exitCode=1});
