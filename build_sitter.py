#!/usr/bin/env python3
"""Generates /pet-sitter-instructions/index.html — a free, printable pet-sitter
sheet people can fill in on the page and print, written for people searching
"printable pet sitter instructions" and similar.

The fields mirror Pawfolio's own Pet Sitter Info tab (owner contact, away dates,
emergency contact, regular and emergency vet, per-pet feeding / walks /
medications / supplements / notes, home notes), so the page is an honest preview
of the free app. What someone types is kept only in this browser's local storage,
never sent anywhere. Re-run after build.py; it writes only into
./pet-sitter-instructions/.
"""
import pathlib

ROOT = pathlib.Path(__file__).parent
OUT_DIR = ROOT / "pet-sitter-instructions"
URL = "https://cleartrackapps.com/pet-sitter-instructions/"
APP = "https://cleartrackapps.com/go/pawfolio-app/?src=sitter-page"
DEMO = "https://cleartrackapps.com/go/pawfolio-demo/?src=sitter-page"
TEXT_LINK = "https://cleartrackapps.com/go/pawfolio-app/?src=sitter-text"

CF_BEACON = (
    '<!-- Cloudflare Web Analytics: privacy-first, no cookies, no consent banner needed -->\n'
    '<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
    'data-cf-beacon=\'{"token": "5673e14274004df9a11f87d759a6b624"}\'></script>'
)

TITLE = "Free Printable Pet Sitter Instructions Sheet | Pawfolio"
DESC = ("A free pet sitter instructions sheet you can fill in and print: your contact info, "
        "emergency contacts, vet and emergency vet, plus feeding, walks and medications for "
        "each pet. No signup.")

CHECKLIST = [
    ("How to reach you", "Your phone and email, and the dates you'll be away."),
    ("A backup contact", "Someone nearby who can make decisions if you can't be reached."),
    ("Your vet and the emergency vet", "Clinic names, phone numbers and addresses, so the sitter isn't searching at 2 a.m."),
    ("Feeding", "When, how much, and what's off-limits. Treats count."),
    ("Walks and routines", "Times, leash habits, and anything your pet does that might worry a stranger."),
    ("Medications and supplements", "The name, the dose, the time, and how you usually give it."),
    ("The house", "Door codes, where the food and leash live, and which rooms are off-limits."),
]

FAQ = [
    ("Is this really free?",
     "Yes. No signup and no email. Fill it in, print it, and you're done."),
    ("Where does what I type go?",
     "Nowhere. It stays in this browser on this device so it's still here if you come back. "
     "Clear sheet erases it."),
    ("Can I print it blank and fill it in by hand?",
     "Yes. Tap Print without typing anything and you get a sheet with space to write."),
    ("Can I send it to my sitter instead of printing it?",
     "This page prints. Pawfolio Free builds the same sheet from your pet profiles and medications, "
     "keeps it for next time, and lets you text it to your sitter with tap-to-call numbers."),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def field(fid, label, ph="", area=False, rows=2, lines=1):
    if area:
        ctl = f'<textarea id="{fid}" data-k="{fid}" data-lines="{lines}" rows="{rows}" placeholder="{esc(ph)}"></textarea>'
    else:
        ctl = f'<input id="{fid}" data-k="{fid}" type="text" placeholder="{esc(ph)}" autocomplete="off">'
    return f'<label class="sf"><span>{label}</span>{ctl}</label>'


def pet_block(n):
    p = f"pet{n}"
    return f'''
      <section class="sheet-pet" data-pet="{n}"{' hidden' if n > 1 else ''}>
        <h3>Pet {n}</h3>
        <div class="sg">
          {field(p+"-name", "Name", "e.g., Bella")}
          {field(p+"-kind", "Type and breed", "e.g., Dog, golden retriever")}
        </div>
        <div class="sg">
          {field(p+"-when", "When to feed", "e.g., 7 a.m. and 5 p.m.")}
          {field(p+"-supp", "Supplements", "e.g., Fish oil, 1 pump on dinner")}
        </div>
        {field(p+"-food", "Feeding instructions", "e.g., 1 cup dry food, splash of warm water. No table scraps.", area=True)}
        {field(p+"-walk", "Walk schedule", "e.g., Morning and evening, 20 minutes. Pulls toward squirrels.", area=True)}
        {field(p+"-meds", "Medications", "e.g., Apoquel 16 mg, 1 tablet with breakfast", area=True)}
        {field(p+"-notes", "Additional notes", "e.g., Hides under the bed during storms", area=True, rows=3, lines=3)}
      </section>'''


def checklist():
    return "\n".join(
        f'        <li><strong>{t}.</strong> {d}</li>' for t, d in CHECKLIST)


def faq_items():
    return "\n".join(
        f'''      <details class="faq-item"><summary>{q}<span class="chev" aria-hidden="true">&#9662;</span></summary><p>{a}</p></details>'''
        for q, a in FAQ)


PAGE = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<meta name="theme-color" content="#faf6ef" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#181410" media="(prefers-color-scheme: dark)">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="CleartrackApps">
<meta property="og:url" content="{URL}">
<meta property="og:title" content="Free printable pet sitter instructions">
<meta property="og:description" content="{DESC}">
<meta property="og:image" content="https://cleartrackapps.com/assets/og-pawfolio.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="../assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="../assets/favicon-180.png" sizes="180x180">
<link rel="preconnect" href="https://api.fontshare.com" crossorigin>
<link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=general-sans@400,500,600&f[]=zodiak@600,700&display=swap">
<link rel="stylesheet" href="../base.css">
<link rel="stylesheet" href="../style.css">
<style>
  .ps-hero {{ padding: clamp(1.5rem, 4vw, 2.5rem) 0 1rem; text-align: center; }}
  .ps-hero h1 {{ font-family: Zodiak, Georgia, serif; font-weight: 700;
    font-size: clamp(1.85rem, 5.4vw, 3rem); letter-spacing: -.02em; max-width: 20ch; margin: .4rem auto 0; }}
  .ps-lede {{ max-width: 46ch; margin: .9rem auto 0; font-size: clamp(1rem, 2.2vw, 1.1rem); opacity: .82; }}
  .ps-sec {{ padding: clamp(2rem, 5vw, 3.5rem) 0; }}
  .ps-alt {{ background: var(--color-bg-alt, #f4eee3); }}
  .ps-h2 {{ font-family: Zodiak, Georgia, serif; font-weight: 700; letter-spacing: -.015em;
    font-size: clamp(1.5rem, 4vw, 2.2rem); max-width: 26ch; }}
  .ps-sub {{ max-width: 52ch; margin-top: .6rem; opacity: .78; }}
  .ps-actions {{ display: flex; flex-wrap: wrap; gap: .7rem; justify-content: center; margin-top: 1.4rem; }}
  .ps-note {{ margin-top: .8rem; font-size: .9rem; opacity: .62; text-align: center; }}

  .sheet {{ max-width: 46rem; margin: 1.5rem auto 0; background: var(--color-surface);
    border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: clamp(1rem, 4vw, 2rem); }}
  .sheet-title {{ font-family: Zodiak, Georgia, serif; font-weight: 700; font-size: 1.5rem; margin: 0; }}
  .sheet h3 {{ font-family: inherit; font-weight: 600; font-size: 1rem;
    color: var(--accent-pawfolio); border-bottom: 2px solid var(--accent-pawfolio);
    padding-bottom: .3rem; margin: 1.6rem 0 .8rem; }}
  .sg {{ display: grid; gap: 0 1rem; grid-template-columns: 1fr; }}
  @media (min-width: 560px) {{ .sg {{ grid-template-columns: 1fr 1fr; }} }}
  .sf {{ display: block; margin: 0 0 .8rem; min-width: 0; }}
  .sf span {{ display: block; font-size: .85rem; font-weight: 600; color: var(--color-text-muted); margin-bottom: .2rem; }}
  .sf input, .sf textarea {{ width: 100%; max-width: 100%; min-width: 0; box-sizing: border-box; font: inherit; font-size: 1rem;
    color: var(--color-text); background: transparent; border: 0; border-bottom: 1px solid var(--color-border);
    border-radius: 0; padding: .35rem 0; resize: none; overflow: hidden; -webkit-appearance: none; appearance: none; }}
  .sf input:focus, .sf textarea:focus {{ outline: none; border-bottom-color: var(--accent-pawfolio); }}
  .sf ::placeholder {{ color: var(--color-text-muted); opacity: .55; }}
  .sheet-tools {{ display: flex; flex-wrap: wrap; gap: .6rem; margin-top: 1rem; }}
  .linkbtn {{ background: none; border: 0; padding: .4rem 0; font: inherit; font-weight: 600;
    color: var(--color-primary); cursor: pointer; text-decoration: underline; text-underline-offset: 3px; }}

  .ps-text {{ margin-top: 1.4rem; padding: 1rem 1.1rem; border-radius: var(--radius);
    background: var(--accent-pawfolio-soft); border: 1px solid color-mix(in srgb, var(--accent-pawfolio) 25%, transparent); }}
  .ps-text p {{ margin: 0; }}
  .ps-text-h {{ font-weight: 600; font-size: 1.05rem; color: var(--color-text); }}
  .ps-text p + p {{ margin-top: .35rem; color: var(--color-text-muted); }}
  .ps-text-link {{ display: inline-block; margin-top: .6rem; font-weight: 600; color: var(--accent-pawfolio);
    text-decoration: underline; text-underline-offset: 3px; }}
  .ps-list {{ max-width: 52ch; margin: 1.2rem 0 0; padding-left: 1.2rem; display: grid; gap: .7rem; }}
  .ps-cta {{ max-width: 40rem; margin: 0 auto; text-align: center; }}
  .ps-cta .pf-tag {{ display: inline-block; vertical-align: .18em; margin-left: .1em; font-family: Satoshi, system-ui, sans-serif;
    font-weight: 700; font-size: .66em; letter-spacing: .04em; text-transform: uppercase; line-height: 1;
    padding: .3em .5em .26em; border-radius: 999px; background: var(--accent-pawfolio);
    color: var(--accent-pawfolio-soft); white-space: nowrap; }}

  .print-only, .pv {{ display: none; }}
  @media print {{
    @page {{ margin: 10mm; }}
    body {{ background: #fff !important; color: #000 !important; }}
    .site-head, .site-foot, .ps-hero, .ps-hide-print, .sheet-tools, .skip {{ display: none !important; }}
    .ps-sec {{ padding: 0 !important; background: none !important; }}
    .sheet {{ border: 0; padding: 0; margin: 0; max-width: none; background: none; }}
    .sheet h3 {{ color: #000; border-color: #000; break-after: avoid; }}
    .sheet {{ font-size: 10pt; }}
    .sheet-title {{ font-size: 15pt; }}
    .sheet h3 {{ font-size: 10.5pt; margin: .75rem 0 .35rem; }}
    .sg {{ grid-template-columns: 1fr 1fr; }}
    .sf span {{ font-size: 8.5pt; margin-bottom: 0; }}
    .sf input, .sf textarea {{ font-size: 10pt; padding: .2rem 0; }}
    .sf {{ break-inside: avoid; margin-bottom: .35rem; }}
    .sf span {{ color: #333; }}
    .sf input, .sf textarea {{ color: #000; border-bottom: 1px solid #999; resize: none; }}
    .sf ::placeholder {{ color: transparent; }}
    /* Text boxes print as plain text blocks that grow with what's written. */
    .sf textarea {{ display: none !important; }}
    .pv[data-lines] {{ min-height: calc(var(--n) * 1.8em); }}
    .pv .rl {{ height: 1.8em; border-bottom: 1px solid #999; }}
    .pv:has(.rl) {{ border-bottom: 0; padding: 0; }}
    .pv {{ display: block; min-height: 2.2em; padding: .2rem 0; border-bottom: 1px solid #999;
      white-space: pre-wrap; overflow-wrap: anywhere; font-size: 10pt; color: #000; }}
    .sheet-top {{ display: flex; justify-content: space-between; align-items: baseline; gap: 1rem; }}
    .print-only {{ display: block; font-size: 8pt; color: #555; margin: 0; }}
  }}
</style>
</head>
<body>
<a class="skip" href="#top">Skip to content</a>

<header class="site-head">
  <div class="wrap head-inner">
    <a class="brand" href="../" aria-label="Cleartrack Apps home">
      <span class="lockup logo-head"><img class="logo logo-on-light" src="../assets/logo.png" width="720" height="289" alt="Cleartrack Apps" decoding="async"><img class="logo logo-on-dark" src="../assets/logo-dark.png" width="720" height="289" alt="" aria-hidden="true" decoding="async"></span>
    </a>
  </div>
</header>

<main id="top">
  <section class="ps-hero">
    <div class="wrap">
      <h1>Free printable pet sitter instructions</h1>
      <p class="ps-lede">Everything your sitter needs in one place: how to reach you, the vet, and each
        pet's food, walks and medications. Fill it in here and print it, or print it blank.</p>
    </div>
  </section>

  <section class="ps-sec" aria-label="Pet sitter sheet">
    <div class="wrap">
      <form class="sheet" id="sheet" autocomplete="off" onsubmit="return false">
        <div class="sheet-top"><p class="sheet-title">Pet Sitter Instructions</p><p class="print-only">Free sheet from cleartrackapps.com/pet-sitter-instructions</p></div>

        <h3>Owner contact</h3>
        <div class="sg">
          {field("owner-name", "Owner name", "Your name")}
          {field("owner-phone", "Phone", "Your phone number")}
          {field("owner-email", "Email", "Your email")}
          {field("away", "Away dates", "e.g., Apr 10–15")}
        </div>

        <h3>Emergency contact</h3>
        <div class="sg">
          {field("emerg-name", "Name", "Someone nearby")}
          {field("emerg-phone", "Phone", "Their phone number")}
        </div>

        <div class="sg vets">
          <div>
            <h3>Veterinarian</h3>
            {field("vet-name", "Clinic", "e.g., Happy Paws Clinic")}
            {field("vet-phone", "Phone", "(555) 123-4567")}
            {field("vet-address", "Address", "123 Main St")}
          </div>
          <div>
            <h3>Emergency vet</h3>
            {field("evet-name", "Clinic", "e.g., 24-hour animal hospital")}
            {field("evet-phone", "Phone", "(555) 999-0000")}
            {field("evet-address", "Address", "Address")}
          </div>
        </div>
{pet_block(1)}{pet_block(2)}{pet_block(3)}{pet_block(4)}

        <div class="sheet-tools">
          <button type="button" class="linkbtn" id="add-pet">+ Add another pet</button>
        </div>

        <h3>The house</h3>
        {field("home", "Instructions and notes", "Door codes, where the food and leash are, rooms that are off-limits…", area=True, rows=4, lines=3)}

        <div class="sheet-tools">
          <button type="button" class="btn btn-primary" id="print">Print</button>
          <button type="button" class="linkbtn" id="clear">Clear sheet</button>
        </div>

        <div class="ps-text ps-hide-print">
          <p class="ps-text-h">Wouldn't it be easier to just text it?</p>
          <p>Pawfolio Free texts your sitter a link that opens this whole sheet on their phone, with
            tap-to-call numbers. It's ready again next trip.</p>
          <a class="ps-text-link" href="{TEXT_LINK}">Text it with Pawfolio&nbsp;Free&nbsp;&rarr;</a>
        </div>
      </form>
      <p class="ps-note ps-hide-print">What you type stays in this browser. Nothing is sent anywhere.</p>
    </div>
  </section>

  <section class="ps-sec ps-alt ps-hide-print" aria-labelledby="what-h">
    <div class="wrap">
      <h2 class="ps-h2" id="what-h">What to put in pet sitter instructions</h2>
      <ul class="ps-list">
{checklist()}
      </ul>
    </div>
  </section>

  <section class="ps-sec ps-hide-print" aria-labelledby="cta-h">
    <div class="wrap ps-cta">
      <h2 class="ps-h2" id="cta-h" style="margin-inline:auto">Keep it ready for next time</h2>
      <p class="ps-sub" style="margin-inline:auto">Pawfolio Free builds this same
        sheet from your pet profiles and medications, so it's ready the next time you travel. Text it to
        your sitter with tap-to-call numbers. No account, and your records stay on your phone.</p>
      <div class="ps-actions">
        <a class="btn btn-primary btn-lg" href="{APP}">Open Pawfolio Free</a>
        <a class="btn btn-ghost btn-lg" href="{DEMO}">Try the demo first</a>
      </div>
    </div>
  </section>

  <section class="faq ps-hide-print" aria-labelledby="faq-h">
    <div class="wrap faq-wrap">
      <h2 class="sec-title ps-h2" id="faq-h">Questions</h2>
      <div class="faq-list">
{faq_items()}
      </div>
    </div>
  </section>
</main>

<footer class="site-foot">
  <div class="wrap foot-inner">
    <div class="foot-brand">
      <div>
        <p class="foot-name">CleartrackApps</p>
        <p class="foot-note">Simple apps that work offline &mdash; no app store, no account. Granbury, Texas.</p>
      </div>
    </div>
    <nav class="foot-links" aria-label="Elsewhere">
      <a href="../pawfolio/">Pawfolio</a>
      <a href="https://instagram.com/cleartrackapps" target="_blank" rel="noopener noreferrer">Instagram</a>
      <a href="https://www.pinterest.com/cleartrackapps" target="_blank" rel="noopener noreferrer">Pinterest</a>
      <a href="mailto:cleartrackapps@gmail.com">cleartrackapps@gmail.com</a>
    </nav>
    <p class="foot-fine">&copy; 2026 CleartrackApps. Pawfolio&trade; is a trademark of CleartrackApps.</p>
  </div>
</footer>

<script src="../app.js" defer></script>
<script>
(function () {{
  var KEY = 'ct-sitter-sheet-v1';
  var form = document.getElementById('sheet');
  var fields = form.querySelectorAll('[data-k]');
  var pets = form.querySelectorAll('.sheet-pet');
  var addBtn = document.getElementById('add-pet');
  var data = {{}};
  try {{ data = JSON.parse(localStorage.getItem(KEY) || '{{}}') || {{}}; }} catch (e) {{ data = {{}}; }}

  function mirror(t) {{ if (t.tagName === 'TEXTAREA') {{ var v = t.nextElementSibling; if (!v || !v.classList.contains('pv')) {{ v = document.createElement('div'); v.className = 'pv'; var n = +t.dataset.lines || 1; if (n > 1) {{ v.dataset.lines = n; v.style.setProperty('--n', n); }} t.after(v); }} v.textContent = t.value; var n = +(v.dataset.lines || 0); if (n > 1 && !t.value) {{ for (var i = 0; i < n; i++) {{ var l = document.createElement('div'); l.className = 'rl'; v.appendChild(l); }} }} }} }}
  function grow(t) {{ if (t.tagName === 'TEXTAREA') {{ t.style.height = 'auto'; t.style.height = t.scrollHeight + 'px'; }} }}
  function shown() {{ var n = 0; pets.forEach(function (p) {{ if (!p.hidden) n++; }}); return n; }}
  function showPets(n) {{
    pets.forEach(function (p, i) {{ p.hidden = i >= n; }});
    addBtn.hidden = n >= pets.length;
  }}
  function save() {{
    try {{ data.pets = shown(); localStorage.setItem(KEY, JSON.stringify(data)); }} catch (e) {{}}
  }}

  fields.forEach(function (f) {{
    if (data[f.dataset.k]) f.value = data[f.dataset.k];
    mirror(f);
    f.addEventListener('input', function () {{ data[f.dataset.k] = f.value; grow(f); mirror(f); save(); }});
  }});
  // Show as many pet blocks as were in use last time.
  var used = 1;
  pets.forEach(function (p, i) {{
    p.querySelectorAll('[data-k]').forEach(function (f) {{ if (f.value) used = Math.max(used, i + 1); }});
  }});
  showPets(Math.max(used, data.pets || 1));
  requestAnimationFrame(function () {{ fields.forEach(grow); }});

  addBtn.addEventListener('click', function () {{
    var n = shown() + 1; showPets(n); save();
    var first = pets[n - 1] && pets[n - 1].querySelector('input'); if (first) first.focus();
  }});
  document.getElementById('print').addEventListener('click', function () {{ window.print(); }});
  document.getElementById('clear').addEventListener('click', function () {{
    if (!confirm('Erase everything on this sheet?')) return;
    data = {{}}; try {{ localStorage.removeItem(KEY); }} catch (e) {{}}
    fields.forEach(function (f) {{ f.value = ''; grow(f); mirror(f); }});
    showPets(1);
  }});
  // Blank pet blocks after the first don't need to print.
  window.addEventListener('beforeprint', function () {{
    pets.forEach(function (p, i) {{
      if (i === 0 || p.hidden) return;
      var any = false; p.querySelectorAll('[data-k]').forEach(function (f) {{ if (f.value) any = true; }});
      if (!any) p.dataset.printHide = '1', p.hidden = true;
    }});
    fields.forEach(mirror);
  }});
  window.addEventListener('afterprint', function () {{
    pets.forEach(function (p) {{ if (p.dataset.printHide) {{ delete p.dataset.printHide; p.hidden = false; }} }});
  }});
}})();
</script>
{CF_BEACON}
</body>
</html>
'''

if __name__ == "__main__":
    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / "index.html").write_text(PAGE, encoding="utf-8")
    print(f"wrote {OUT_DIR / 'index.html'}")
