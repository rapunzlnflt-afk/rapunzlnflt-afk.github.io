/* Meta (Facebook/Instagram) pixel — CleartrackApps
 * ---------------------------------------------------------------------------
 * PASTE YOUR PIXEL ID BELOW. Until you do, this file does nothing at all:
 * no network requests, no cookies, no tracking. It is safe to ship empty.
 *
 * Where to find the ID:
 *   business.facebook.com  ->  Events Manager  ->  Data sources
 *   The pixel ID is the 15-16 digit number under the dataset name.
 *   No pixel yet? "Connect data sources" -> Web -> Meta Pixel -> name it
 *   "CleartrackApps" -> it gives you the ID immediately.
 *
 * To use it on another page, add this one line before </body>:
 *   <script src="../meta-pixel.js" defer></script>
 * (use "./meta-pixel.js" for pages at the site root)
 * --------------------------------------------------------------------------- */

var CT_META_PIXEL_ID = '';

(function () {
  'use strict';

  // ---- a tracking helper that works whether or not the pixel is configured ----
  // Other scripts call window.ctTrack('EventName', {...}). It is always defined,
  // so quiz.js never has to check for the pixel's existence.
  var queued = [];
  window.ctTrack = function (name, params) {
    queued.push([name, params]);
    if (typeof window.fbq === 'function') {
      window.fbq('trackCustom', name, params || {});
    }
  };
  window.ctTrackStandard = function (name, params) {
    if (typeof window.fbq === 'function') {
      window.fbq('track', name, params || {});
    }
  };

  var id = String(CT_META_PIXEL_ID || '').trim();
  if (!/^[0-9]{10,20}$/.test(id)) return; // not configured — stay completely inert

  // Respect an explicit browser Do Not Track signal.
  if (navigator.doNotTrack === '1' || window.doNotTrack === '1') return;

  /* Standard Meta pixel bootstrap (unminified for readability). */
  (function (f, b, e, v, n, t, s) {
    if (f.fbq) return;
    n = f.fbq = function () {
      n.callMethod ? n.callMethod.apply(n, arguments) : n.queue.push(arguments);
    };
    if (!f._fbq) f._fbq = n;
    n.push = n; n.loaded = true; n.version = '2.0'; n.queue = [];
    t = b.createElement(e); t.async = true; t.src = v;
    s = b.getElementsByTagName(e)[0]; s.parentNode.insertBefore(t, s);
  })(window, document, 'script', 'https://connect.facebook.net/en_US/fbevents.js');

  window.fbq('init', id);
  window.fbq('track', 'PageView');

  // Flush anything that fired before the pixel finished booting.
  queued.forEach(function (ev) { window.fbq('trackCustom', ev[0], ev[1] || {}); });

  /* ---- InitiateCheckout on any buy link ----------------------------------
   * /go/pawfolio/ is a redirect interstitial, so the click is the last moment
   * we can measure. Fires on the outbound tap, not on page load. */
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[href*="/go/"]');
    if (!a) return;
    var href = a.getAttribute('href') || '';
    if (href.indexOf('/go/pawfolio') === -1) return;
    window.fbq('track', 'InitiateCheckout', {
      content_name: 'Pawfolio',
      content_ids: ['pawfolio'],
      value: 14.99,
      currency: 'USD'
    });
  }, true);

  /* ViewContent for the product page itself. */
  if (/\/pawfolio\/?$/.test(location.pathname)) {
    window.fbq('track', 'ViewContent', {
      content_name: 'Pawfolio',
      content_ids: ['pawfolio'],
      content_type: 'product',
      value: 14.99,
      currency: 'USD'
    });
  }
})();
