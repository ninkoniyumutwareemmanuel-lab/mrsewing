import fs from "node:fs";
import assert from "node:assert/strict";
const { validate, handle } = await import(
    "data:text/javascript;base64," +
      fs.readFileSync("functions/_lib/shop-handler.js").toString("base64")
  ),
  products = JSON.parse(
    fs.readFileSync("/workspace/review/commerce/fixtures.json"),
  );
const customer = {
  "Full Name": "Synthetic QA",
  "Phone / WhatsApp": "+250780000000",
  "Email Address": "qa@example.invalid",
  Consent: "Accepted",
  "Delivery or Collection": "QA collection preference",
  "Preferred Payment Method": "Bank Transfer",
};
const body = {
  kind: "purchase",
  customer,
  items: [{ productId: "QA_0", variationId: "qa-a", quantity: 2 }],
  total: 1,
};
const payload = validate(body, products);
for(const method of ["Mobile Money","Bank Transfer","Cryptocurrency"])assert.equal(validate({...body,customer:{...customer,"Preferred Payment Method":method}},products)["Preferred Payment Method"],method);
assert.equal(payload["Catalogue Subtotal RWF"], 24690);
assert.equal(JSON.parse(payload.Products)[0].catalogueUnitPriceRwf, 12345);
for (const bad of [
  { ...body, items: [{ productId: "QA_0", variationId: "qa-a", quantity: 3 }] },
  { ...body, items: [{ productId: "QA_2", variationId: "qa-a", quantity: 1 }] },
  { ...body, items: [{ productId: "bad", variationId: "qa-a", quantity: 1 }] },
  { ...body, items: [{ productId: "QA_0", variationId: "bad", quantity: 1 }] },
  { ...body, items: [...body.items, ...body.items] },
  { ...body, customer: { ...customer, Consent: "" } },
  {
    ...body,
    customer: { ...customer, "Preferred Payment Method": "Unsupported payment" },
  },
  { ...body, customer: { ...customer, botcheck: "spam" } },
])
  assert.throws(() => validate(bad, products));
assert.equal(
  validate(
    {
      kind: "quote",
      customer,
      items: [{ productId: "QA_1", variationId: "qa-a", quantity: 4 }],
    },
    products,
  )["Request Type"],
  "Shop product quotation request",
);
assert.equal(
  validate(
    { kind: "referral", customer: { ...customer, "Existing Customer": "No" } },
    [],
  )["Existing Customer"],
  "No",
);
let count = 0,
  sent;
const req = (data = body, extra = {}) =>
  new Request("https://preview.mrsewing-staging.pages.dev/api/shop-request", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Origin: "https://preview.mrsewing-staging.pages.dev",
      ...extra,
    },
    body: typeof data === "string" ? data : JSON.stringify(data),
  });
const fetcher = async (url, options) => {
  count++;
  sent = JSON.parse(options.body);
  return new Response(JSON.stringify({ success: true }), { status: 200 });
};
let r = await handle(req(), products, "synthetic-provider-key", fetcher);
assert.equal(r.status, 200);
assert.equal((await r.json()).success, true);
assert.equal(sent["Catalogue Subtotal RWF"], 24690);
assert.equal(sent.access_key, "synthetic-provider-key");
assert(!("total" in sent));
for (const fetcher of [
  async () => new Response('{"success":false}', { status: 200 }),
  async () => new Response('{"success":true}', { status: 500 }),
  async () => new Response("not json"),
  async () => {
    throw Error("Network");
  },
]) {
  r = await handle(req(), products, "synthetic-provider-key", fetcher);
  assert.equal(r.status, 502);
  assert.equal((await r.json()).success, false);
}
assert.equal((await handle(req(), products, "", fetcher)).status, 503);
assert.equal(
  (
    await handle(
      req(body, { Origin: "https://evil.invalid" }),
      products,
      "k",
      fetcher,
    )
  ).status,
  403,
);
assert.equal(
  (await handle(req("invalid json"), products, "k", fetcher)).status,
  400,
);
assert.equal(
  (await handle(req("x".repeat(30001)), products, "k", fetcher)).status,
  413,
);
assert.equal(
  (
    await handle(
      new Request("https://evil.invalid/api/shop-request"),
      products,
      "k",
      fetcher,
    )
  ).status,
  403,
);
assert.equal(
  (
    await handle(
      new Request("https://mrsewing-staging.pages.dev/api/shop-request"),
      products,
      "k",
      fetcher,
    )
  ).status,
  405,
);
console.log(
  "PASS authoritative stock/variation/status/price/consent/payment validation, referral/quote payloads, provider positive-only acknowledgement, 4 provider failures, host/origin/method/size/malformed/config handling; no real email",
);

// The deployed entrypoint imports its generated empty catalogue and existing provider configuration.
const {onRequest}=await import('../functions/api/shop-request.js');
const originalFetch=globalThis.fetch;let entryCalls=0;
try {globalThis.fetch=async()=>{entryCalls++;return new Response(JSON.stringify({success:true}),{status:200})};const response=await onRequest({request:new Request('https://mrsewing-staging.pages.dev/api/shop-request',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({kind:'referral',customer:{...customer,'Existing Customer':'No'}})})});assert.equal(response.status,200);assert.equal(entryCalls,1);}finally{globalThis.fetch=originalFetch;}
console.log('PASS deployed entrypoint imports and email-only referral path with mocked provider; existing key not printed');
