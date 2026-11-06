/* Email-only shop/referral intake. No database, upload, payment or stock reservation. */
const reply = (status, body) =>
  new Response(JSON.stringify(body), {
    status,
    headers: {
      "Content-Type": "application/json",
      "Cache-Control": "no-store",
      "X-Content-Type-Options": "nosniff",
      "X-Robots-Tag": "noindex, nofollow",
    },
  });
function text(customer, key, max = 2000, required = false) {
  const value = customer[key];
  if (value === undefined && !required) return "";
  if (
    typeof value !== "string" ||
    value.length > max ||
    (required && !value.trim())
  )
    throw Error("Check " + key + ".");
  return value.trim();
}
export function validate(body, products) {
  if (!body || !["referral", "quote", "purchase"].includes(body.kind))
    throw Error("Invalid request type.");
  const c = body.customer;
  if (!c || typeof c !== "object" || Array.isArray(c))
    throw Error("Customer details required.");
  if (c.botcheck) throw Error("Request could not be confirmed.");
  const customer = {
    "Full Name": text(c, "Full Name", 160, true),
    "Phone / WhatsApp": text(c, "Phone / WhatsApp", 40, true),
    "Email Address": text(c, "Email Address", 254),
    Consent: text(c, "Consent", 50, true),
  };
  if (customer.Consent !== "Accepted")
    throw Error("Terms and privacy acceptance required.");
  if (
    !/^[+\d\s().-]{7,40}$/.test(customer["Phone / WhatsApp"]) ||
    customer["Phone / WhatsApp"].replace(/\D/g, "").length < 7
  )
    throw Error("Check Phone / WhatsApp.");
  if (
    customer["Email Address"] &&
    !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(customer["Email Address"])
  )
    throw Error("Check Email Address.");
  if (body.kind === "referral") {
    customer["Existing Customer"] = text(c, "Existing Customer", 10, true);
    if (!["Yes", "No"].includes(customer["Existing Customer"]))
      throw Error("Select whether you are an existing customer.");
    return {
      ...customer,
      "Request Type": "Referral participation enquiry",
      Important:
        "Human review only. No automatic participation, referral code, commission or payment approval.",
    };
  }
  const list = body.items;
  if (
    !Array.isArray(list) ||
    !list.length ||
    list.length > 50 ||
    (body.kind === "quote" && list.length !== 1)
  )
    throw Error("Choose valid products.");
  const seen = new Set();
  let total = 0;
  const rows = list.map((x) => {
    if (
      !x ||
      typeof x !== "object" ||
      typeof x.productId !== "string" ||
      typeof x.variationId !== "string"
    )
      throw Error("Choose valid products and variations.");
    const p = products.find((p) => p.id === x.productId),
      v = p?.variations.find((v) => v.id === x.variationId);
    if (!p || !v)
      throw Error(
        "A product or variation is no longer available. Review your selections.",
      );
    const id = p.id + "|" + v.id;
    if (seen.has(id)) throw Error("Duplicate product variation.");
    seen.add(id);
    if (
      !Number.isSafeInteger(x.quantity) ||
      x.quantity < 1 ||
      x.quantity > 1000
    )
      throw Error("Choose a valid quantity.");
    if (body.kind === "purchase") {
      if (
        p.availability !== "Available in Stock" ||
        x.quantity > v.stockQuantity ||
        !Number.isSafeInteger(p.priceRwf)
      )
        throw Error(
          "Recorded stock has changed. Review your cart before submitting.",
        );
      total += p.priceRwf * x.quantity;
    } else if (p.availability !== "Available on Orders")
      throw Error("This product is not available for a quotation request.");
    return {
      productId: p.id,
      name: p.name,
      url: "https://mrsewingfashion.com/shop/" + p.slug + "/",
      size: v.size,
      colour: v.colour,
      quantity: x.quantity,
      ...(body.kind === "purchase"
        ? { catalogueUnitPriceRwf: p.priceRwf }
        : {}),
    };
  });
  if (body.kind === "purchase") {
    customer["Delivery or Collection"] = text(
      c,
      "Delivery or Collection",
      1000,
      true,
    );
    customer["Preferred Payment Method"] = text(
      c,
      "Preferred Payment Method",
      40,
      true,
    );
    if (
      !["Bank Transfer", "Mobile Money"].includes(
        customer["Preferred Payment Method"],
      )
    )
      throw Error("Select an available payment preference.");
    customer["Additional Information"] = text(c, "Additional Information");
  } else
    customer["Additional Requirements"] = text(c, "Additional Requirements");
  return {
    ...customer,
    "Request Type":
      body.kind === "purchase"
        ? "Shop purchase request"
        : "Shop product quotation request",
    Products: JSON.stringify(rows, null, 2),
    ...(body.kind === "purchase" ? { "Catalogue Subtotal RWF": total } : {}),
    Important:
      "Enquiry only. No order, payment or inventory reservation. Verify current catalogue and final amount before acceptance; delivery charges are not included in the catalogue subtotal.",
  };
}
export async function handle(request, products, providerKey, fetcher = fetch) {
  const host = new URL(request.url).hostname;
  if (
    host !== "mrsewingfashion.com" &&
    host !== "mrsewing-staging.pages.dev" &&
    !host.endsWith(".mrsewing-staging.pages.dev") &&
    host !== "localhost" &&
    host !== "127.0.0.1"
  )
    return reply(403, { success: false, error: "Unrecognised website." });
  if (request.method !== "POST")
    return reply(405, { success: false, error: "POST required." });
  const origin = request.headers.get("Origin");
  if (origin && origin !== new URL(request.url).origin)
    return reply(403, { success: false, error: "Submit from this website." });
  if (!request.headers.get("Content-Type")?.startsWith("application/json"))
    return reply(415, { success: false, error: "JSON required." });
  if (Number(request.headers.get("Content-Length")) > 30000)
    return reply(413, { success: false, error: "Request too large." });
  let fields;
  try {
    const reader = request.body?.getReader();
    if (!reader) throw Error("Request body required.");
    const chunks = [];
    let size = 0;
    while (true) {
      const chunk = await reader.read();
      if (chunk.done) break;
      size += chunk.value.byteLength;
      if (size > 30000) {
        await reader.cancel();
        return reply(413, { success: false, error: "Request too large." });
      }
      chunks.push(chunk.value);
    }
    const bytes = new Uint8Array(size);
    let offset = 0;
    for (const chunk of chunks) {
      bytes.set(chunk, offset);
      offset += chunk.byteLength;
    }
    fields = validate(JSON.parse(new TextDecoder().decode(bytes)), products);
  } catch (error) {
    return reply(400, {
      success: false,
      error: error instanceof SyntaxError ? "Invalid request." : error.message,
    });
  }
  if (!providerKey)
    return reply(503, {
      success: false,
      error:
        "Email submission is not configured. Your request has not been sent.",
    });
  const controller = new AbortController(),
    timer = setTimeout(() => controller.abort(), 15000);
  try {
    const response = await fetcher("https://api.web3forms.com/submit", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({
        access_key: providerKey,
        subject: "Mr Sewing Fashion — " + fields["Request Type"],
        from_name: "Mr Sewing Fashion website",
        ...fields,
        botcheck: "",
      }),
      signal: controller.signal,
    });
    const result = await response.json();
    if (!response.ok || result.success !== true)
      return reply(502, {
        success: false,
        error:
          "The submission service did not confirm acceptance. Your entries are preserved; please retry or contact Customer Support.",
      });
    return reply(200, { success: true });
  } catch (error) {
    return reply(502, {
      success: false,
      error:
        error.name === "AbortError"
          ? "Submission timed out and may have arrived. Contact Customer Support before retrying."
          : "We could not confirm submission. Your entries are preserved; please retry or contact Customer Support.",
    });
  } finally {
    clearTimeout(timer);
  }
}
