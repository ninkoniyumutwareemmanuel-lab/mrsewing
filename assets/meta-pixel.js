/* Mr Sewing Fashion: optional Meta Pixel. Never load a third-party tracker before consent.
 * Staging demo: append ?meta_pixel_preview=1 to a Pages URL (no events sent).
 */
(function () {
  "use strict";
  var loader = document.querySelector("script[data-mr-meta-pixel]");
  if (!loader) return;
  var host = window.location.hostname.toLowerCase();
  var official = host === "mrsewingfashion.com" || host === "www.mrsewingfashion.com";
  var enabled = official && loader.dataset.productionEnabled === "true";
  var preview = host.endsWith(".pages.dev") &&
    new URLSearchParams(window.location.search).get("meta_pixel_preview") === "1";
  if (!enabled && !preview) return;

  var key = "mrsewing:meta-marketing-consent:v1";
  var choiceInMemory = null;
  var pixelStarted = false;
  var banner = null;
  // Legacy .html links and clean URLs share the same privacy boundary.
  var route = location.pathname.toLowerCase().replace(/\.html$/, "/");
  var unsafeRoute = /^\/(?:request|booking(?:-[a-z-]+)?|privacy-policy|terms-and-conditions|refund-policy|customer-support|measurement-submission|referral-program|staff|whatsapp)(?:\/|$)/.test(route) ||
    /\/(?:selected-designs|fabric|measurements)(?:\/|$)/.test(route) ||
    /^\/services\/(?:custom-tailoring\/(?:special-order|standard-order|design-choice)|vip\/subscription)(?:\/|$)/.test(route) ||
    /^\/shop\/cart(?:\/|$)/.test(route);
  // Fail closed for actual enquiry documents even when a future route is added.
  // Search forms and the homepage's ancillary support dialog do not redefine
  // the purpose of a public browsing page; they never emit conversion events.
  function hasRequestForm() {
    try {
      return !!document.querySelector("#customerRequestForm, #submissionForm, #bookingForm, form[data-commerce-form], form[data-shop-whatsapp-form], form[data-request-form], form[data-quotation-form]");
    } catch (_) { return true; }
  }
  // Don't pass query strings or sensitive journey pages to the browser Pixel.
  var canTrack = enabled && !unsafeRoute && !location.search;

  function getChoice() {
    try { return localStorage.getItem(key) || choiceInMemory; }
    catch (_) { return choiceInMemory; }
  }
  function setChoice(value) {
    choiceInMemory = value;
    try { localStorage.setItem(key, value); } catch (_) {}
  }
  function initPixel() {
    if (!canTrack || hasRequestForm() || pixelStarted || getChoice() !== "accepted") return;
    pixelStarted = true;
    // Base code supplied by the owner; run only after explicit opt-in.
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
    if (typeof window.fbq === "function") {
      window.fbq("init", loader.dataset.pixelId);
      window.fbq("track", "PageView");
    }
  }
  function closeBanner() {
    if (banner) banner.remove();
    banner = null;
  }
  function choose(value) {
    var before = getChoice();
    setChoice(value);
    closeBanner();
    if (value === "accepted") initPixel();
    if (value === "declined" && before === "accepted" && pixelStarted && enabled) {
      // Stop the active script by reloading; prior Meta processing cannot be undone.
      location.reload();
    }
  }
  function button(label, className, callback) {
    var el = document.createElement("button");
    el.type = "button";
    el.textContent = label;
    el.className = className;
    el.addEventListener("click", callback);
    return el;
  }
  function openBanner() {
    closeBanner();
    banner = document.createElement("section");
    banner.className = "ms-meta-consent";
    banner.setAttribute("role", "region");
    banner.setAttribute("aria-label", "Cookie consent preferences");
    var identity = document.createElement("div");
    identity.className = "ms-meta-identity";
    var icon = document.createElement("span");
    icon.className = "ms-meta-icon";
    icon.setAttribute("aria-hidden", "true");
    icon.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M20.5 13.3A8.7 8.7 0 0 1 10.7 3.5a8.7 8.7 0 1 0 9.8 9.8Z"/><circle cx="8" cy="12" r=".9" fill="currentColor" stroke="none"/><circle cx="13" cy="16" r=".9" fill="currentColor" stroke="none"/><circle cx="11" cy="8" r=".9" fill="currentColor" stroke="none"/></svg>';
    var title = document.createElement("h2");
    title.textContent = "Cookies & Privacy";
    identity.appendChild(icon);
    identity.appendChild(title);
    var description = document.createElement("p");
    description.className = "ms-meta-description";
    description.appendChild(document.createTextNode("This website uses optional cookies to improve your experience and measure our advertising. "));
    var policy = document.createElement("a");
    policy.href = "/privacy-policy/";
    policy.textContent = "Privacy Policy";
    description.appendChild(policy);
    var controls = document.createElement("div");
    controls.className = "ms-meta-actions";
    controls.appendChild(button("Reject", "ms-meta-no", function () { choose("declined"); }));
    controls.appendChild(button("Allow", "ms-meta-yes", function () { choose("accepted"); }));
    banner.appendChild(identity);
    banner.appendChild(description);
    if (preview) {
      var note = document.createElement("p");
      note.textContent = "Staging demonstration only. No tracking data is sent to Meta.";
      note.className = "ms-meta-preview";
      banner.appendChild(note);
    }
    banner.appendChild(controls);
    document.body.appendChild(banner);
  }
  function ready() {
    var style = document.createElement("style");
    style.textContent = ".ms-meta-consent{position:fixed;z-index:7000;left:50%;bottom:12px;transform:translateX(-50%);display:grid;grid-template-columns:max-content minmax(0,1fr) auto;align-items:center;column-gap:16px;row-gap:8px;box-sizing:border-box;width:calc(100% - 24px);max-width:1120px;padding:11px 15px;background:#111111;color:#f6f1e7;border:1px solid #c9a14e;border-radius:13px;box-shadow:0 8px 24px #0008;font:13px/1.4 system-ui,sans-serif}.ms-meta-identity{display:flex;align-items:center;gap:10px;padding-right:16px;border-right:1px solid #816a3d;white-space:nowrap;min-width:0}.ms-meta-icon{display:inline-flex;align-items:center;justify-content:center;color:#d8ad4c;flex-shrink:0}.ms-meta-consent h2{font:600 15px/1.35 system-ui,sans-serif;margin:0;color:#f6e6c5}.ms-meta-consent .ms-meta-description{margin:0;color:#f2ede4;font-size:13px;line-height:1.4}.ms-meta-consent a{color:#edc56d;text-decoration:underline;text-underline-offset:2px;white-space:nowrap}.ms-meta-actions{display:flex;align-items:center;gap:9px;min-width:188px}.ms-meta-actions button{min-width:83px;min-height:40px;border:1px solid #c9a14e;border-radius:7px;padding:8px 14px;font:600 13px/1.2 system-ui,sans-serif;cursor:pointer}.ms-meta-no{color:#fff;background:#111}.ms-meta-yes{color:#15120d;background:#e4b756}.ms-meta-consent button:focus-visible,.ms-meta-consent a:focus-visible,.ms-meta-manage:focus-visible{outline:3px solid #f0ce7e;outline-offset:3px}.ms-meta-consent button:hover{filter:brightness(1.09)}.ms-meta-consent .ms-meta-preview{grid-column:1/-1;margin:0;color:#edca7b;font-size:12px}.ms-meta-manage{display:inline-block;min-height:44px;border:0;background:transparent;color:inherit;cursor:pointer;text-decoration:underline;padding:9px;font:inherit}@media(max-width:780px){.ms-meta-consent{grid-template-columns:1fr auto;padding:11px 13px;column-gap:10px;row-gap:5px}.ms-meta-identity{border-right:0;padding-right:0}.ms-meta-consent .ms-meta-description{grid-column:1/-1;grid-row:2}.ms-meta-actions{grid-column:2;grid-row:1;min-width:0}.ms-meta-actions button{min-width:65px;padding:7px 12px;min-height:38px}.ms-meta-consent h2{font-size:14px}}@media(max-width:480px){.ms-meta-consent{bottom:8px;width:calc(100% - 16px);grid-template-columns:1fr;padding:10px 12px;row-gap:7px}.ms-meta-identity{grid-column:1;grid-row:1}.ms-meta-consent .ms-meta-description{grid-column:1;grid-row:2;font-size:12px}.ms-meta-actions{grid-column:1;grid-row:3;width:100%;gap:8px}.ms-meta-actions button{flex:1;min-height:40px}.ms-meta-consent .ms-meta-preview{grid-column:1}}";
    document.head.appendChild(style);
    var footer = document.querySelector("#site-footer, footer, .homepage-footer");
    (footer || document.body).appendChild(button("Cookie preferences", "ms-meta-manage", openBanner));
    if (getChoice() === null || preview) openBanner();
    if (getChoice() === "accepted") initPixel();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", ready, { once: true });
  else ready();
})();
