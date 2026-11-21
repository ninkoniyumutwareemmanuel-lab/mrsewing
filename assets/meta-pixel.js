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
  var unsafeRoute = /^\/(?:request|booking|privacy-policy|terms-and-conditions|refund-policy)(?:\/|$)/.test(location.pathname) ||
    /\/(?:selected-designs|fabric|measurements)(?:\/|$)/.test(location.pathname);
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
    if (!canTrack || pixelStarted || getChoice() !== "accepted") return;
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
    banner.setAttribute("aria-label", "Optional marketing tracking preferences");
    var title = document.createElement("h2");
    title.textContent = "Optional website tracking";
    var description = document.createElement("p");
    description.textContent = "May we use Meta Pixel to measure website visits after Facebook and Instagram advertising? You can decline or change your choice later.";
    var policy = document.createElement("a");
    policy.href = "/privacy-policy/";
    policy.textContent = "Read our Privacy Policy";
    var controls = document.createElement("div");
    controls.className = "ms-meta-actions";
    controls.appendChild(button("Decline", "ms-meta-no", function () { choose("declined"); }));
    controls.appendChild(button("Allow tracking", "ms-meta-yes", function () { choose("accepted"); }));
    banner.appendChild(title);
    banner.appendChild(description);
    banner.appendChild(policy);
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
    style.textContent = ".ms-meta-consent{position:fixed;z-index:7000;left:12px;right:12px;bottom:12px;max-width:440px;margin-left:auto;background:#191815;color:#f7f4ed;padding:18px;border:1px solid #c9a14e;border-radius:12px;box-shadow:0 10px 30px #0009;font:15px/1.5 system-ui,sans-serif}.ms-meta-consent h2{font:600 19px/1.3 system-ui,sans-serif;color:#fff;margin:0 0 9px}.ms-meta-consent p{color:#f0eee9;margin:0 0 9px}.ms-meta-consent a{color:#f1ce7b;text-decoration:underline}.ms-meta-actions{display:flex;gap:10px;margin-top:14px}.ms-meta-actions button{flex:1;min-height:44px;border:1px solid #c9a14e;border-radius:6px;padding:9px 10px;font:600 14px system-ui;cursor:pointer}.ms-meta-no{color:#fff;background:#191815}.ms-meta-yes{color:#111;background:#d7a83a}.ms-meta-consent .ms-meta-preview{font-size:13px;color:#edca7b;margin-top:9px}.ms-meta-manage{display:inline-block;min-height:44px;border:0;background:transparent;color:inherit;cursor:pointer;text-decoration:underline;padding:9px;font:inherit}";
    document.head.appendChild(style);
    var footer = document.querySelector("#site-footer, footer, .homepage-footer");
    (footer || document.body).appendChild(button("Tracking preferences", "ms-meta-manage", openBanner));
    if (getChoice() === null || preview) openBanner();
    if (getChoice() === "accepted") initPixel();
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", ready, { once: true });
  else ready();
})();
