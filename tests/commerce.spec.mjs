import fs from "node:fs";
import assert from "node:assert/strict";
import { createRequire } from "node:module";
const require = createRequire(import.meta.url),
  { chromium } = require("playwright");
const { handle } = await import(
    "data:text/javascript;base64," +
      fs.readFileSync("functions/_lib/shop-handler.js").toString("base64")
  ),
  products = JSON.parse(
    fs.readFileSync("/workspace/review/commerce/fixtures.json"),
  ),
  pages = JSON.parse(
    fs.readFileSync("/workspace/review/commerce/fixture-pages.json"),
  );
const browser = await chromium.launch({
  executablePath: "/usr/bin/chromium",
  args: ["--no-sandbox"],
});
let mode = "ok",
  calls = 0,
  payload,
  last;
const evidence = {
  viewports: [],
  axe: [],
  cases: [],
  errors: [],
  scope:
    "Local Chromium; synthetic product fixtures served only by interception; provider mocked, no real customer messages",
};
try {
  const ctx = await browser.newContext({ reducedMotion: "reduce" });
  let fixtures = false;
  await ctx.route("**/*", async (route) => {
    const url = new URL(route.request().url());
    if (url.origin !== "http://127.0.0.1:8000") return route.abort();
    if (url.pathname === "/api/shop-request") {
      if (mode === 'client-network') return route.abort();
      if (mode === 'client-malformed') return route.fulfill({status:200,contentType:'application/json',body:'not json'});
      calls++;
      payload = route.request().postDataJSON();
      const request = new Request("http://127.0.0.1:8000/api/shop-request", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Origin: "http://127.0.0.1:8000",
        },
        body: JSON.stringify(payload),
      });
      const response = await handle(
        request,
        products,
        "synthetic-provider-key",
        async (u, o) => {
          last = JSON.parse(o.body);
          if (mode === "slow") await new Promise((r) => setTimeout(r, 300));
          if (mode === "network") throw Error("synthetic network");
          return new Response(
            mode === "malformed"
              ? "not json"
              : JSON.stringify({ success: mode !== "reject" }),
            { status: mode === "http" ? 500 : 200 },
          );
        },
      );
      return route.fulfill({
        status: response.status,
        contentType: "application/json",
        body: await response.text(),
      });
    }
    const key = url.pathname.slice(1) + "index.html";
    if (fixtures && pages[key])
      return route.fulfill({ contentType: "text/html", body: pages[key] });
    return route.continue();
  });
  const p = await ctx.newPage();
  p.on("pageerror", (e) => evidence.errors.push(e.message));
  for (const width of [320, 360, 390, 430, 768, 1024, 1440]) {
    await p.setViewportSize({ width, height: 900 });
    for (const path of [
      "/loyalty-program/",
      "/referral-program/",
      "/shop/",
      "/shop/cart/",
    ]) {
      await p.goto("http://127.0.0.1:8000" + path);
      assert(
        await p.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth + 1,
        ),
        path + " overflow " + width,
      );
      assert.equal(await p.locator("h1").count(), 1);
    }
    evidence.viewports.push(width);
  }
  await p.goto("http://127.0.0.1:8000/shop/");
  assert.equal(await p.locator("[data-product-card]").count(), 0);
  assert(
    await p
      .getByRole("heading", { name: "Our catalogue is being prepared" })
      .isVisible(),
  );
  assert.equal(
    await p.locator("meta[name=robots]").getAttribute("content"),
    "index, follow",
  );
  async function fillCommon() {
    await p.locator('[name="Full Name"]').fill("Synthetic QA");
    await p.locator('[name="Phone / WhatsApp"]').fill("+250780000000");
    await p.locator('[name="Email Address"]').fill("qa@example.invalid");
    await p.locator("[name=Consent]").check();
  }
  await p.goto("http://127.0.0.1:8000/referral-program/");
  assert.equal(await p.locator('[data-commerce-form]').getAttribute('method'),'post');
  const before = calls;
  await p.getByRole("button", { name: "Continue", exact: true }).click();
  assert.equal(calls, before);
  await fillCommon();
  await p.locator("#existingCustomer").selectOption("No");
  await p.locator("[data-review]").click();
  assert.match(
    await p.locator("[data-review-details]").innerText(),
    /Existing Customer\s+No/,
  );
  await p.locator("[data-edit]").click();
  assert.equal(
    await p.locator('[name="Full Name"]').inputValue(),
    "Synthetic QA",
  );
  await p.locator("[data-review]").click();
  mode = "reject";
  await p.getByRole("button", { name: "Submit Participation Request" }).click();
  await p.waitForFunction(() =>
    document
      .querySelector("[data-status]")
      .textContent.includes("did not confirm"),
  );
  assert(await p.locator("[data-success]").isHidden());
  mode = "ok";
  await p.getByRole("button", { name: "Submit Participation Request" }).click();
  await p.waitForFunction(
    () => !document.querySelector("[data-success]").hidden,
  );
  assert.equal(last["Existing Customer"], "No");
  evidence.cases.push(
    "Referral required fields, non-customer participation, review/edit, rejection, retry and positive provider success",
  );
  fixtures = true;
  await p.goto("http://127.0.0.1:8000/shop/");
  assert.equal(await p.locator("[data-product-card]").count(), 3);
  await p.locator("#shopSearch").fill("Synthetic QA 1");
  assert.equal(await p.locator("[data-product-card]:visible").count(), 1);
  await p.locator("#shopSearch").fill("");
  await p.locator("#shopAvailability").selectOption("Out of Stock");
  assert.equal(await p.locator("[data-product-card]:visible").count(), 1);
  await p.locator("#shopAvailability").selectOption("");
  await p.locator("#shopSort").selectOption("price-desc");
  assert.equal(
    await p.locator("[data-product-card]").first().getAttribute("data-price"),
    "12345",
  );
  await p.goto("http://127.0.0.1:8000/shop/qa-only-2/");
  assert(
    await p
      .getByRole("button", { name: "Out of Stock", exact: true })
      .isDisabled(),
  );
  await p.goto("http://127.0.0.1:8000/shop/qa-only-0/");
  await p.locator("#productVariation").selectOption("qa-a");
  await p.locator("#productQuantity").fill("3");
  await p.getByRole("button", { name: "Add to Cart" }).click();
  assert.equal(await p.evaluate(()=>JSON.parse(localStorage.getItem("mrsewing-shop-cart-v1")||"[]").reduce((n,item)=>n+item.quantity,0)),0);
  await p.locator("#productQuantity").fill("2");
  await p.getByRole("button", { name: "Add to Cart" }).click();
  assert.equal(await p.evaluate(()=>JSON.parse(localStorage.getItem("mrsewing-shop-cart-v1"))[0].quantity),2);
  await p.reload();
  assert.equal(await p.evaluate(()=>JSON.parse(localStorage.getItem("mrsewing-shop-cart-v1"))[0].quantity),2);
  await p.goto("http://127.0.0.1:8000/shop/cart/");
  assert.equal(await p.locator(".cart-line input").inputValue(), "2");
  await p.locator(".cart-line input").fill("1");
  await p.locator(".cart-line input").dispatchEvent("change");
  assert.match(await p.locator("#cartTotal").innerText(), /12,345/);
  await fillCommon();
  await p.locator("#deliveryAddress").fill("Synthetic collection preference");
  await p.locator("#paymentMethod").selectOption("Mobile Money");
  assert(!(await p.locator("#paymentMethod option").last().isDisabled()));
  await p.locator("[data-review]").click();
  assert.match(
    await p.locator("[data-review-details]").innerText(),
    /Synthetic QA 0/,
  );
  mode = "slow";
  const oldCalls = calls;
  await p
    .getByRole("button", { name: "Submit Purchase Request" })
    .dblclick({ force: true });
  await p.waitForFunction(
    () => !document.querySelector("[data-success]").hidden,
  );
  assert.equal(calls, oldCalls + 1);
  assert.equal(last["Catalogue Subtotal RWF"], 12345);
  assert.equal(payload.customer["Preferred Payment Method"], "Mobile Money");
  assert.deepEqual(
    await p.evaluate(() =>
      JSON.parse(localStorage.getItem("mrsewing-shop-cart-v1")),
    ),
    [],
  );
  evidence.cases.push(
    "Listing search/filter/sort, out-of-stock disabled, stock limit, cart refresh/navigation/edit, purchase review, duplicate prevention, server-authoritative subtotal, positive acknowledgement and cart clear",
  );
  await p.goto("http://127.0.0.1:8000/shop/qa-only-1/");
  await p.locator("#productVariation").selectOption("qa-a");
  await p.locator("#productQuantity").fill("4");
  await p.getByRole("button", { name: "Request a Quote", exact: true }).click();
  assert(await p.locator("#quoteDialog").isVisible());
  await p.keyboard.press("Escape");
  assert(
    await p
      .getByRole("button", { name: "Request a Quote", exact: true })
      .evaluate((n) => n === document.activeElement),
  );
  await p.getByRole("button", { name: "Request a Quote", exact: true }).click();
  await fillCommon();
  await p.locator("#quoteRequirements").fill("Synthetic requirements");
  await p.locator("[data-review]").click();
  for (const failure of ["http", "malformed", "network", "client-network", "client-malformed"]) {
    mode = failure;
    await p.getByRole("button", { name: "Submit Quotation Request" }).click();
    await p.waitForFunction(
      () =>
        document
          .querySelector("[data-status]")
          .textContent.includes("could not confirm") ||
        document
          .querySelector("[data-status]")
          .textContent.includes("did not confirm"),
    );
    assert(await p.locator("[data-success]").isHidden());
    assert.equal(
      await p.locator('[name="Full Name"]').inputValue(),
      "Synthetic QA",
    );
  }
  mode = "ok";
  await p.getByRole("button", { name: "Submit Quotation Request" }).click();
  await p.waitForFunction(
    () => !document.querySelector("[data-success]").hidden,
  );
  assert.match(last.Products, /QA_1/);
  assert.match(last.Products, /"quantity": 4/);
  assert(!("Catalogue Subtotal RWF" in last));
  evidence.cases.push(
    "Quote dialog keyboard/focus, context, 3 provider failures, preserved entries, retry and exact positive-only quote acknowledgement",
  );
  for (const width of [320, 390, 768, 1440]) {
    await p.setViewportSize({ width, height: 900 });
    for (const path of [
      "/shop/qa-only-0/",
      "/shop/qa-only-1/",
      "/shop/qa-only-2/",
    ]) {
      await p.goto("http://127.0.0.1:8000" + path);
      assert(
        await p.evaluate(
          () => document.documentElement.scrollWidth <= innerWidth + 1,
        ),
      );
    }
  }
  await p.goto("http://127.0.0.1:8000/shop/cart/");
  await p.evaluate(() =>
    localStorage.setItem(
      "mrsewing-shop-cart-v1",
      JSON.stringify([
        { productId: "QA_0", variationId: "qa-a", quantity: 900 },
        { productId: "QA_2", variationId: "qa-a", quantity: 1 },
        { productId: "bad", variationId: "bad", quantity: 1 },
      ]),
    ),
  );
  await p.reload();
  assert.equal(await p.locator(".cart-line").count(), 1);
  assert.equal(await p.locator(".cart-line input").inputValue(), "2");
  assert.match(await p.locator("#cartStatus").innerText(), /updated/);
  await p.getByRole("button", { name: /Remove Synthetic/ }).click();
  assert(await p.locator("#checkout").isHidden());
  evidence.cases.push(
    "Stale/unavailable/unknown cart records removed, quantity capped and remove action",
  );
  // Audit the functional form states using unpublished product fixtures as well.
  for (const scenario of ['cart','quote']) {
    await p.setViewportSize({width:390,height:900});
    if(scenario==='cart') {
      await p.goto('http://127.0.0.1:8000/shop/qa-only-0/');await p.locator('#productVariation').selectOption('qa-a');await p.getByRole('button',{name:'Add to Cart'}).click();await p.goto('http://127.0.0.1:8000/shop/cart/');
    } else {
      await p.goto('http://127.0.0.1:8000/shop/qa-only-1/');await p.locator('#productVariation').selectOption('qa-a');await p.getByRole('button',{name:'Request a Quote',exact:true}).click();
    }
    await p.addScriptTag({path:'/workspace/tools/homepage-qa/node_modules/axe-core/axe.min.js'});
    const violations=await p.evaluate(async()=> (await axe.run(document.querySelector('main'),{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa']}})).violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)})));
    assert.deepEqual(violations,[]);evidence.axe.push({fixtureScenario:scenario,width:390,violations});
  }
  fixtures = false;
  for (const width of [390, 1440]) {
    await p.setViewportSize({ width, height: 900 });
    for (const [path, name] of [
      ["/loyalty-program/", "loyalty"],
      ["/referral-program/", "referral"],
      ["/shop/", "shop"],
    ]) {
      await p.goto("http://127.0.0.1:8000" + path);
      await p.screenshot({
        path: "/workspace/artifacts/commerce/" + name + "-" + width + ".png",
        fullPage: true,
      });
      await p.addScriptTag({
        path: "/workspace/tools/homepage-qa/node_modules/axe-core/axe.min.js",
      });
      const result = await p.evaluate(async () => {
        const r = await axe.run(document.querySelector("main"), {
          runOnly: {
            type: "tag",
            values: ["wcag2a", "wcag2aa", "wcag21aa", "wcag22aa"],
          },
        });
        return r.violations.map((v) => ({
          id: v.id,
          nodes: v.nodes.map((n) => n.target),
        }));
      });
      evidence.axe.push({ path, width, violations: result });
      assert.deepEqual(result, []);
    }
  }
  await p.goto("http://127.0.0.1:8000/");
  assert.equal(
    await p.locator("#loyalty-title a").getAttribute("href"),
    "/loyalty-program/",
  );
  assert.equal(
    await p.locator("#referral-title a").getAttribute("href"),
    "/referral-program/",
  );
  assert.equal(await p.locator(".header-shop").getAttribute("href"), "/shop/");
  assert.equal(
    await p.locator(".header-shop").getAttribute("aria-label"),
    "Online Shop",
  );
  assert.equal(await p.locator("[data-moving-gallery]").count(), 3);
  for (const width of [390,1440]) {
    await p.setViewportSize({width,height:900});
    for (const [selector,destination] of [['#loyalty-title a','/loyalty-program/'],['#referral-title a','/referral-program/'],['.header-shop','/shop/']]) {
      await p.goto('http://127.0.0.1:8000/'); await p.locator(selector).click(); await p.waitForURL('**'+destination); assert.equal(new URL(p.url()).pathname,destination);
    }
  }
  evidence.cases.push('Actual homepage programme and shared Shop navigation clicks at mobile and desktop widths');
  assert.deepEqual(evidence.errors, []);
  const nojs=await browser.newContext({javaScriptEnabled:false});
  await nojs.route('**/*',r=>new URL(r.request().url()).origin==='http://127.0.0.1:8000'?r.continue():r.abort());
  const fallback=await nojs.newPage();await fallback.goto('http://127.0.0.1:8000/referral-program/');
  assert.equal(await fallback.locator('form').getAttribute('method'),'post');
  assert(await fallback.locator('[data-review]').isDisabled());
  assert(await fallback.locator('noscript').isVisible());
  await nojs.close();evidence.cases.push('No-JavaScript form fails closed with POST method, disabled submit controls and explanatory fallback');
  fs.writeFileSync(
    "/workspace/review/commerce/browser.json",
    JSON.stringify(evidence, null, 2),
  );
  console.log(
    "PASS commerce: 7 widths; catalogue/product/cart/quote/referral/mock-provider flows, 8 Axe scans, homepage connections; fixtures never published; no real email",
  );
} finally {
  await browser.close();
}
