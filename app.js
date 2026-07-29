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
