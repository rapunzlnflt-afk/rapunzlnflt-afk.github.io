/* Theme toggle. No storage (sandboxed iframes block it) — in-memory only. */
(function () {
  var root = document.documentElement;
  var btn = document.getElementById('theme-toggle');
  if (!btn) return;
  var prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  var theme = prefersDark ? 'dark' : 'light';
  function apply() {
    root.setAttribute('data-theme', theme);
    btn.setAttribute('aria-label', theme === 'dark' ? 'Switch to light theme' : 'Switch to dark theme');
  }
  btn.addEventListener('click', function () {
    theme = theme === 'dark' ? 'light' : 'dark';
    apply();
  });
  apply();
})();


/* The header carries the logo at full size at the top of the page and shrinks it
   once you scroll, so it stays out of the way while you read. The class is flipped
   inside a requestAnimationFrame so scrolling stays smooth, and only when the state
   actually changes. The size change itself is a CSS transition, which the
   prefers-reduced-motion rule in style.css switches off for anyone who asks for it. */
(function () {
  var head = document.querySelector('.site-head');
  if (!head) return;
  var compact = false, queued = false;
  function apply() {
    queued = false;
    var want = window.scrollY > 56;
    if (want !== compact) { compact = want; head.classList.toggle('is-compact', want); }
  }
  window.addEventListener('scroll', function () {
    if (!queued) { queued = true; requestAnimationFrame(apply); }
  }, { passive: true });
  apply();
})();
