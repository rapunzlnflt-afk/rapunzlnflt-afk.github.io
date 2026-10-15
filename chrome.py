"""One header and one footer for every page on cleartrackapps.com.

Each page builder makes its own HTML, then passes it through apply(), which
swaps in this header and footer. Before this, every builder carried its own
copy, and the copies drifted (different footer links on every page).

prefix: "./" on the homepage, "../" on pages one folder down.
"""
import re

TOGGLE = '''    <button class="theme-toggle" type="button" id="theme-toggle" aria-label="Switch colour theme">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">
        <circle class="t-sun" cx="12" cy="12" r="4.2"/>
        <g class="t-rays"><path d="M12 2.6v2.2M12 19.2v2.2M2.6 12h2.2M19.2 12h2.2M5.4 5.4l1.6 1.6M17 17l1.6 1.6M18.6 5.4L17 7M7 17l-1.6 1.6"/></g>
        <path class="t-moon" d="M20 13.4A8 8 0 1 1 10.6 4a6.4 6.4 0 0 0 9.4 9.4Z"/>
      </svg>
    </button>'''


def _logo(prefix, cls):
    return (f'<span class="lockup {cls}">'
            f'<img class="logo logo-on-light" src="{prefix}assets/logo.png?v=2" width="720" height="289" '
            f'alt="Cleartrack Apps" decoding="async">'
            f'<img class="logo logo-on-dark" src="{prefix}assets/logo-dark.png?v=2" width="720" height="289" '
            f'alt="" aria-hidden="true" decoding="async">'
            f'</span>')


def header(prefix, toggle=False):
    home = "" if prefix == "./" else prefix  # on the homepage, plain #anchors
    brand_href = "#top" if prefix == "./" else prefix
    links = [
        ("Apps", f"{home}#apps"),
        ("Free printables", f"{home}#free"),
        ("How it works", f"{home}#how"),
        ("FAQ", f"{home}#faq"),
    ]
    nav = "\n".join(f'      <a href="{u}">{t}</a>' for t, u in links)
    return f'''<header class="site-head">
  <div class="wrap head-inner">
    <a class="brand" href="{brand_href}" aria-label="Cleartrack Apps home">
      {_logo(prefix, "logo-head")}
    </a>
    <nav class="head-nav" aria-label="Main">
{nav}
    </nav>
{TOGGLE if toggle else ""}
  </div>
</header>'''


def footer(prefix, fine, extra=""):
    p = prefix
    return f'''<footer class="site-foot">
  <div class="wrap foot-inner">
    <div class="foot-brand">
      {_logo(p, "logo-foot")}
      <p class="foot-note">Simple apps that work offline. No app store, no account. Made in Granbury, Texas.</p>
    </div>
    <nav class="foot-cols" aria-label="Footer">
      <div class="foot-col">
        <p class="foot-h">Apps</p>
        <a href="{p}pawfolio/">Pawfolio</a>
        <a href="{p}medrecords/">MedRecords</a>
        <a href="{p}#apps">All five apps</a>
      </div>
      <div class="foot-col">
        <p class="foot-h">Free printables</p>
        <a href="{p}medication-tracker/">Medication tracker</a>
        <a href="{p}pet-medication-chart/">Pet medication chart</a>
        <a href="{p}pet-sitter-instructions/">Pet sitter sheet</a>
      </div>
      <div class="foot-col">
        <p class="foot-h">Follow</p>
        <a href="https://instagram.com/cleartrackapps" target="_blank" rel="noopener noreferrer">Instagram</a>
        <a href="https://www.pinterest.com/cleartrackapps" target="_blank" rel="noopener noreferrer">Pinterest</a>
        <a href="https://cleartrackapps.com/go/etsy-shop/" target="_blank" rel="noopener noreferrer">Etsy shop</a>
      </div>
      <div class="foot-col">
        <p class="foot-h">Contact</p>
        <a href="mailto:cleartrackapps@gmail.com">cleartrackapps@gmail.com</a>
      </div>
    </nav>{extra}
    <p class="foot-fine">{fine}</p>
  </div>
</footer>'''


_HEAD_RE = re.compile(r'<header class="site-head">.*?</header>', re.S)
_FOOT_RE = re.compile(r'<footer class="site-foot">.*?</footer>', re.S)


def apply(page, prefix, fine, extra="", toggle=False):
    assert _HEAD_RE.search(page) and _FOOT_RE.search(page), "page has no site header/footer"
    page = _HEAD_RE.sub(lambda m: header(prefix, toggle), page, count=1)
    page = _FOOT_RE.sub(lambda m: footer(prefix, fine, extra), page, count=1)
    return page
