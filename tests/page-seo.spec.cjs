/* On-page metadata and heading checks; uses the existing local test server. */
const { chromium } = require('playwright');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const root = path.resolve(__dirname, '..');
const base = process.env.REVIEW_BASE_URL || 'http://127.0.0.1:8000/';
(async () => {
  execFileSync('python3',['scripts/sync_page_seo.py','--check'],{cwd:root,stdio:'inherit'});
  execFileSync('python3',['scripts/build_homepage.py','--check'],{cwd:root,stdio:'inherit'});
  const aliases=JSON.parse(fs.readFileSync(path.join(root,'_data/route-aliases.json'),'utf8'));
  const pages=JSON.parse(fs.readFileSync(path.join(root,'_data/page-seo.json'),'utf8'));
  const full=fs.readdirSync(root).filter(file=>file.endsWith('.html')&&/<html\b/i.test(fs.readFileSync(path.join(root,file),'utf8')));
  assert.deepEqual(Object.keys(pages).sort(),full.sort());
  assert.equal(new Set(Object.values(pages).map(page=>page.title.toLowerCase())).size,32);
  assert.equal(new Set(Object.values(pages).map(page=>page.description.toLowerCase())).size,32);
  for(const data of Object.values(pages)){
    assert(data.title.includes('Mr Sewing Fashion'));
    assert(data.title.length>0);
    assert(data.description.length>0);
  }
  const browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH||'/usr/bin/chromium',args:['--no-sandbox']});
  try{
    const context=await browser.newContext();
    await context.route('**/*',route=>new URL(route.request().url()).origin===new URL(base).origin?route.continue():route.abort());
    const page=await context.newPage();const errors=[];
    page.on('pageerror',error=>errors.push(error.message));
    for(const [file,data]of Object.entries(pages)){
      if(aliases[file])continue;
      await page.goto(base+file);await page.locator('header nav').waitFor({state:'attached'});
      assert.equal(await page.title(),data.title,file);
      assert.equal(await page.locator('head title').count(),1,file);
      const description=page.locator('meta[name="description"]');
      assert.equal(await description.count(),1,file);
      assert.equal(await description.getAttribute('content'),data.description,file);
      assert.equal(await page.locator('h1').count(),1,file);
      assert((await page.locator('h1').innerText()).trim(),file);
      for(const [key,value]of [['og:title',data.title],['twitter:title',data.title],['og:description',data.description],['twitter:description',data.description]]){
        const tags=page.locator(`meta[property="${key}"], meta[name="${key}"]`);
        for(const tag of await tags.all())assert.equal(await tag.getAttribute('content'),value,file+' '+key);
      }
      const outline=await page.locator('body h1,body h2,body h3,body h4').evaluateAll(nodes=>nodes.filter(node=>!node.closest('header,footer,[role="dialog"],#successBox')&&node.getClientRects().length).map(node=>({level:Number(node.tagName.slice(1)),text:node.textContent.trim()})));
      let previous=0;
      for(const heading of outline){assert(heading.level<=previous+1,`${file}: H${previous} to H${heading.level}: ${heading.text}`);previous=heading.level;}
      for(const width of [390,1440]){
        await page.setViewportSize({width,height:900});
        assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`${file} overflow at ${width}`);
      }
    }
    await page.goto(base+'services.html');assert.equal(await page.locator('.journey-intro h1').count(),1);assert.equal(await page.locator('.journey-card h2').count(),7);
    await page.goto(base+'reviews.html');assert.equal(await page.locator('main h2').count(),1);assert.equal(await page.locator('.work-title').first().evaluate(node=>node.tagName),'H3');
    await page.goto(base);assert.equal(await page.locator('h1').count(),1);assert.equal(await page.locator('.services-header h2').count(),1);assert.equal(await page.locator('.home-collection-card h3').count(),4);assert.equal(await page.locator('.home-step-grid h3').count(),4);assert.equal(await page.locator('.home-benefit-grid h3').count(),4);
    assert.deepEqual(errors,[]);
    console.log('PASS: 32 unique titles/descriptions, matching social metadata, single descriptive H1s and logical H1–H4 content outlines.');
    console.log('PASS: all 32 pages fit desktop/mobile viewports; services/reviews/homepage hierarchy verified; no JavaScript errors or live submissions.');
  }finally{await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
