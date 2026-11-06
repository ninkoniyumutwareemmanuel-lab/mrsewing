/* Anonymous cart only. All purchase/quote requests are validated again by the Pages Function. */
(() => {
  "use strict";
  const data = document.getElementById("shopData"),
    products = data ? JSON.parse(data.textContent).products : [],
    byId = new Map(products.map((p) => [p.id, p])),
    key = "mrsewing-shop-cart-v1";
  let cart = [],
    storageWarning = false,
    quote = null;
  const $ = (s) => document.querySelector(s),
    money = (v) => "RWF " + v.toLocaleString("en-RW"),
    status = (el, text) => {
      if (el) el.textContent = text;
    };
  try {
    const saved = JSON.parse(localStorage.getItem(key) || "[]");
    if (Array.isArray(saved))
      cart = saved
        .filter(
          (x) =>
            x &&
            typeof x.productId === "string" &&
            typeof x.variationId === "string" &&
            Number.isSafeInteger(x.quantity) &&
            x.quantity > 0,
        )
        .slice(0, 50);
  } catch {
    storageWarning = true;
  }
  function save() {
    try {
      localStorage.setItem(key, JSON.stringify(cart));
    } catch {
      storageWarning = true;
    }
    document
      .querySelectorAll("[data-cart-count]")
      .forEach(
        (el) =>
          (el.textContent = String(cart.reduce((n, x) => n + x.quantity, 0))),
      );
  }
  function item(x) {
    const p = byId.get(x.productId),
      v = p?.variations.find((v) => v.id === x.variationId);
    return p && v ? { ...x, p, v } : null;
  }
  function checkedCart() {
    const clean = [],
      seen = new Set();
    let adjusted = false;
    for (const x of cart) {
      const i = item(x),
        id = x.productId + "|" + x.variationId;
      if (
        !i ||
        i.p.availability !== "Available in Stock" ||
        i.v.stockQuantity < 1 ||
        seen.has(id)
      ) {
        adjusted = true;
        continue;
      }
      seen.add(id);
      const quantity = Math.min(x.quantity, i.v.stockQuantity);
      if (quantity !== x.quantity) adjusted = true;
      clean.push({ ...x, quantity });
    }
    cart = clean;
    save();
    return adjusted;
  }
  function cartContext() {
    return cart.map((x) => ({
      productId: x.productId,
      variationId: x.variationId,
      quantity: x.quantity,
    }));
  }
  function context(kind) {
    return kind === "purchase"
      ? { items: cartContext() }
      : kind === "quote"
        ? { items: quote ? [quote] : [] }
        : {};
  }
  function summary(kind) {
    if (kind === "referral") return {};
    const rows = context(kind).items.map((x) => {
      const i = item(x);
      return i
        ? i.p.name +
            " (" +
            i.p.id +
            "), " +
            i.v.size +
            " / " +
            i.v.colour +
            ", quantity " +
            x.quantity
        : "";
    });
    return {
      "Selected Products": rows.join("\n"),
      ...(kind === "purchase"
        ? {
            "Catalogue Subtotal (RWF)":
              cart.reduce((n, x) => n + item(x).p.priceRwf * x.quantity, 0) +
              " — subject to confirmation; delivery not included",
          }
        : {}),
    };
  }
  function invalidate() {
    document
      .querySelectorAll('[data-commerce-form="purchase"]')
      .forEach((f) => {
        f.querySelector("[data-review-panel]").hidden = true;
        f.querySelector("[data-fields]").hidden = false;
      });
  }
  const grid = $("#shopGrid");
  if (grid) {
    const cards = [...grid.children];
    function filter() {
      const text = $("#shopSearch").value.trim().toLowerCase(),
        cat = ($("#shopCategory")?.value || grid.dataset.category || ""),
        availability = ($("#shopAvailability")?.value || ""),
        sort = ($("#shopSort")?.value || "name");
      cards
        .sort((a, b) =>
          sort === "name"
            ? a.dataset.name.localeCompare(b.dataset.name)
            : (a.dataset.price === "0") - (b.dataset.price === "0") ||
              (sort === "price-asc"
                ? Number(a.dataset.price) - Number(b.dataset.price)
                : Number(b.dataset.price) - Number(a.dataset.price)),
        )
        .forEach((c) => {
          c.hidden = !(
            c.dataset.name.includes(text) &&
            (!cat || c.dataset.category === cat) &&
            (!availability || c.dataset.availability === availability)
          );
          grid.append(c);
        });
      const count = cards.filter((c) => !c.hidden).length;
      $("#shopCount").textContent = count + " products";
      $("#shopEmpty").hidden = count > 0;
    }
    ["shopSearch", "shopCategory", "shopAvailability", "shopSort"].forEach(
      (id) => $("#" + id)?.addEventListener("input", filter),
    );
    filter();
  }
  const selection = $("#productSelection"),
    dialog = $("#quoteDialog");
  if (selection) {
    const p = byId.get(selection.dataset.productId),
      variation = $("#productVariation"),
      quantity = $("#productQuantity");
    variation.addEventListener("change", () => {
      const v = p.variations.find((v) => v.id === variation.value);
      if (p.availability === "Available in Stock" && v)
        quantity.max = String(v.stockQuantity);
      else quantity.removeAttribute("max");
    });
    selection.addEventListener("submit", (e) => {
      e.preventDefault();
      if (!selection.reportValidity()) return;
      const v = p.variations.find((v) => v.id === variation.value),
        q = Number(quantity.value);
      if (!v || !Number.isSafeInteger(q) || q < 1 || q > 1000)
        return status(
          $("#productStatus"),
          "Choose a valid variation and quantity.",
        );
      if (p.availability === "Out of Stock") return;
      if (p.availability === "Available on Orders") {
        quote = { productId: p.id, variationId: v.id, quantity: q };
        $("#quoteContext").textContent =
          p.name + " — " + v.size + " / " + v.colour + " — quantity " + q;
        const f = dialog.querySelector("form");
        f.querySelector("[data-fields]").hidden = false;
        f.querySelector("[data-review-panel]").hidden = true;
        f.querySelector("[data-success]").hidden = true;
        f.hidden = false;
        f.querySelector("[name=Consent]").checked = false;
        dialog.showModal();
        dialog.querySelector("[data-close]").focus();
        return;
      }
      const existing = cart.find(
          (x) => x.productId === p.id && x.variationId === v.id,
        ),
        total = (existing?.quantity || 0) + q;
      if (total > v.stockQuantity)
        return status(
          $("#productStatus"),
          "Only " +
            v.stockQuantity +
            " recorded for this variation. Check your cart quantity.",
        );
      if (existing) existing.quantity = total;
      else cart.push({ productId: p.id, variationId: v.id, quantity: q });
      save();
      status(
        $("#productStatus"),
        storageWarning
          ? "Added for this page. Browser storage is unavailable; your cart may not survive navigation."
          : "Added to cart. Review your cart when ready.",
      );
    });
  }
  if (dialog) {
    const close = () => {
      if (dialog.querySelector('form').dataset.sending === 'true') return;
      dialog.close();
      selection.querySelector("button").focus();
    };
    dialog.querySelector("[data-close]").addEventListener("click", close);
    dialog.addEventListener("cancel", (e) => {
      e.preventDefault();
      close();
    });
  }
  function renderCart() {
    const root = $("#cartItems");
    if (!root) return;
    const adjusted = checkedCart();
    root.replaceChildren();
    cart.forEach((x) => {
      const i = item(x),
        line = document.createElement("div");
      line.className = "cart-line";
      const desc = document.createElement("div"),
        link = document.createElement("a");
      link.href = "/shop/" + i.p.slug + "/";
      link.textContent = i.p.name;
      desc.append(
        link,
        document.createTextNode(
          i.v.size + " / " + i.v.colour + " — " + money(i.p.priceRwf),
        ),
      );
      const label = document.createElement("label");
      label.textContent = "Quantity";
      const input = document.createElement("input");
      input.type = "number";
      input.min = "1";
      input.max = String(i.v.stockQuantity);
      input.step = "1";
      input.value = x.quantity;
      input.setAttribute(
        "aria-label",
        "Quantity for " + i.p.name + " " + i.v.size + " " + i.v.colour,
      );
      input.addEventListener("change", () => {
        const q = Number(input.value);
        if (!Number.isSafeInteger(q) || q < 1 || q > i.v.stockQuantity) {
          input.setCustomValidity("Choose between 1 and " + i.v.stockQuantity);
          input.reportValidity();
          return;
        }
        input.setCustomValidity("");
        x.quantity = q;
        save();
        invalidate();
        renderCart();
      });
      label.append(input);
      const remove = document.createElement("button");
      remove.type = "button";
      remove.className = "home-button";
      remove.textContent = "Remove";
      remove.setAttribute(
        "aria-label",
        "Remove " + i.p.name + " " + i.v.size + " " + i.v.colour,
      );
      remove.addEventListener("click", () => {
        cart = cart.filter((y) => y !== x);
        save();
        invalidate();
        renderCart();
        $("#cartStatus").focus();
      });
      line.append(desc, label, remove);
      root.append(line);
    });
    $("#checkout").hidden = !cart.length;
    $("#cartTotal").textContent = cart.length
      ? "Catalogue subtotal: " +
        money(cart.reduce((n, x) => n + item(x).p.priceRwf * x.quantity, 0)) +
        " (delivery and final amount to be confirmed)"
      : "";
    status(
      $("#cartStatus"),
      !cart.length
        ? "Your cart is empty."
        : adjusted
          ? "Your cart was updated to match the latest catalogue. Please review the current quantities and prices."
          : storageWarning
            ? "Browser storage is unavailable; keep this page open until you finish."
            : "",
    );
    $("#cartStatus").tabIndex = -1;
  }
  if (data) {
    if ($("#cartItems")) renderCart();
    save();
  }
  window.addEventListener("storage", (event) => {
    if (event.key !== key) return;
    try {
      cart = JSON.parse(event.newValue || "[]");
      if (!Array.isArray(cart)) cart = [];
      cart = cart
        .filter(
          (x) =>
            x &&
            typeof x.productId === "string" &&
            typeof x.variationId === "string" &&
            Number.isSafeInteger(x.quantity) &&
            x.quantity > 0,
        )
        .slice(0, 50);
    } catch {
      cart = [];
    }
    invalidate();
    if ($("#cartItems")) renderCart();
  });
  document.querySelectorAll("[data-commerce-form]").forEach((form) => {
    const kind = form.dataset.commerceForm,
      fields = form.querySelector("[data-fields]"),
      review = form.querySelector("[data-review-panel]"),
      details = form.querySelector("[data-review-details]"),
      message = form.querySelector("[data-status]"),
      success = form.querySelector("[data-success]");
    let pending = false,
      fingerprint = "";
    form.querySelector('[data-review]').disabled = false;
    form.querySelector('[type=submit]').disabled = false;
    function values() {
      return Object.fromEntries(new FormData(form));
    }
    function valid() {
      for (const el of form.querySelectorAll("input,textarea"))
        el.setCustomValidity("");
      const name = form.elements["Full Name"],
        phone = form.elements["Phone / WhatsApp"];
      if (!name.value.trim()) name.setCustomValidity("Enter your full name.");
      if (
        !/^[+\d\s().-]{7,40}$/.test(phone.value) ||
        phone.value.replace(/\D/g, "").length < 7
      )
        phone.setCustomValidity("Enter a valid phone or WhatsApp number.");
      if (!form.reportValidity()) return false;
      if (kind !== "referral" && !context(kind).items.length) {
        status(message, "Choose a product before submitting.");
        return false;
      }
      return true;
    }
    function snapshot() {
      return JSON.stringify({ fields: values(), ...context(kind) });
    }
    form.querySelector("[data-review]").addEventListener("click", () => {
      if (!valid()) return;
      details.replaceChildren();
      for (const [k, v] of Object.entries({ ...values(), ...summary(kind) })) {
        if (k === "botcheck" || !v) continue;
        const dt = document.createElement("dt"),
          dd = document.createElement("dd");
        dt.textContent = k;
        dd.textContent = v;
        details.append(dt, dd);
      }
      fingerprint = snapshot();
      fields.hidden = true;
      review.hidden = false;
      status(message, "");
      review.querySelector("h3").focus();
    });
    form.querySelector("[data-edit]").addEventListener("click", () => {
      review.hidden = true;
      fields.hidden = false;
      form.elements["Full Name"].focus();
    });
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      if (pending) return;
      if (review.hidden || !fingerprint || fingerprint !== snapshot()) {
        status(message, "Review the current request before submitting.");
        return;
      }
      if (!valid()) return;
      if (form.elements.botcheck.value) {
        status(
          message,
          "We could not confirm your request. Please contact Customer Support.",
        );
        return;
      }
      pending = true;
      form.dataset.sending = 'true';
      const buttons = [...form.querySelectorAll("button")];
      buttons.forEach((b) => (b.disabled = true));
      status(message, "Submitting your request for review…");
      const controller = new AbortController(),
        timer = setTimeout(() => controller.abort(), 20000);
      try {
        const response = await fetch(window.MrPublicAPI?.url("/api/shop-request")||"/api/shop-request", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
          body: JSON.stringify({ kind, customer: values(), ...context(kind) }),
          signal: controller.signal,
        });
        const result = await response.json();
        if (!response.ok || result.success !== true)
          throw Error(
            result.error ||
              "We could not confirm your request. Your entries are preserved; please review and retry.",
          );
        fields.hidden = true;
        review.hidden = true;
        success.replaceChildren();
        const h = document.createElement("h2"),
          p = document.createElement("p"),
          note = document.createElement("p");
        h.textContent =
          kind === "quote"
            ? "Quotation Request Submitted"
            : kind === "purchase"
              ? "Purchase Request Submitted"
              : "Participation Request Submitted";
        p.textContent =
          kind === "quote"
            ? "Your quotation request was accepted by the submission service. Mr Sewing Fashion will review your product requirements and contact you on WhatsApp with availability and pricing information."
            : kind === "purchase"
              ? "Your purchase request was accepted by the submission service. Mr Sewing Fashion will review availability, confirm the final amount and contact you with payment instructions."
              : "Your participation enquiry was accepted by the submission service. Our team will review your details and contact you. This does not approve participation or commission.";
        note.textContent =
          kind === "quote"
            ? "This does not confirm an order or final price."
            : kind === "purchase"
              ? "Your order is not yet confirmed. Please do not make payment until you receive verified instructions from Mr Sewing Fashion."
              : "";
        success.append(h, p, note);
        success.hidden = false;
        status(message, "");
        success.focus();
        if (kind === "purchase") {
          cart = [];
          save();
          $("#cartItems").replaceChildren();
          $("#cartTotal").textContent = "";
        }
      } catch (error) {
        status(
          message,
          error.name === "AbortError"
            ? "Submission timed out. It may have arrived; contact Customer Support before retrying to avoid a duplicate request. Your entries are preserved."
            : error instanceof TypeError || error instanceof SyntaxError
              ? 'We could not confirm your request. Your entries are preserved; please retry or contact Customer Support.'
              : error.message,
        );
      } finally {
        clearTimeout(timer);
        pending = false;
        delete form.dataset.sending;
        buttons.forEach((b) => (b.disabled = false));
      }
    });
  });
})();
/* Manual product enquiries: no payment, stock reservation or automatic sending. */
(()=>{document.querySelectorAll('[data-shop-whatsapp-form]').forEach(form=>form.addEventListener('submit',event=>{event.preventDefault();if(!form.reportValidity())return;const error=form.querySelector('[data-shop-whatsapp-error]'),quantity=Number(form.elements.quantity.value);if(!Number.isSafeInteger(quantity)||quantity<1||quantity>999){error.textContent='Enter a whole quantity between 1 and 999.';return;}if(!window.MrSewingWhatsApp){error.textContent='WhatsApp enquiry is temporarily unavailable. Please try again or contact our team.';return;}error.textContent='';const text='Hello Mr Sewing Fashion, I would like to enquire about purchasing '+form.dataset.productName+' ('+form.dataset.productId+').\nProduct: '+form.dataset.productUrl+'\nRequested quantity: '+quantity+'\nPreferred payment: '+form.elements.payment.value+'\nPreferences: '+(form.elements.preferences.value.trim()||'Please advise')+'\nPlease confirm availability, options, final price and payment instructions.';window.MrSewingWhatsApp.open(text,form.querySelector('[type=submit]'));}));})();

(()=>{document.querySelectorAll('[data-share-product]').forEach(button=>button.addEventListener('click',async()=>{const status=document.querySelector('[data-share-status]');try{await navigator.clipboard.writeText(button.dataset.shareProduct);status.textContent='Product link copied.';}catch{status.textContent='Product link: '+button.dataset.shareProduct;}}));})();
