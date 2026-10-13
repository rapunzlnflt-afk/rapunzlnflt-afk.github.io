#!/usr/bin/env python3
"""Generates /pet-medication-chart/index.html — a free weekly pet medication
chart builder (every 24, 12, 8, 6 or 4 hours, printed in the browser) plus the
ready-made printable PDF, fillable PDF and spreadsheet for people searching
"pet medication chart printable" and similar. Ends with Pawfolio Free, which
does the same job with reminders and Given / Skip check-offs. Re-run after
build.py; it writes only into ./pet-medication-chart/.
"""
import pathlib

from medchart_builder import BUILDER_HTML, BUILDER_CSS, BUILDER_JS

ROOT = pathlib.Path(__file__).parent
OUT_DIR = ROOT / "pet-medication-chart"
URL = "https://cleartrackapps.com/pet-medication-chart/"
APP = "https://cleartrackapps.com/go/pawfolio-app/?src=medchart-page"
DEMO = "https://cleartrackapps.com/go/pawfolio-demo/?src=medchart-page"
TIP_LINK = "https://cleartrackapps.com/go/pawfolio-app/?src=medchart-tip"

CF_BEACON = (
    '<!-- Cloudflare Web Analytics: privacy-first, no cookies, no consent banner needed -->\n'
    '<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
    'data-cf-beacon=\'{"token": "5673e14274004df9a11f87d759a6b624"}\'></script>'
)

TITLE = "Free Printable Pet Medication Chart (Weekly Dose Log) | Pawfolio"
DESC = ("Make a free weekly pet medication chart for dogs and cats. Pick medicines given every "
        "24, 12, 8, 6 or 4 hours, add the times, and print. Or download the ready-made PDF or "
        "spreadsheet. No signup.")

DOWNLOADS = [
    ("pet-medication-chart.pdf", "Printable PDF", "Print it and keep it by the pill bottles. Write in pen."),
    ("pet-medication-chart-fillable.pdf", "Fillable PDF", "Type the medicine names and times on your computer, then print."),
    ("pet-medication-chart.xlsx", "Spreadsheet", "Opens in Excel, Google Sheets or Numbers. Change anything you like."),
]

HOW = [
    ("Write the medicine and dose in the left column.",
     "One medicine per section, for example \u201cApoquel 16 mg, 1 tablet.\u201d"),
    ("Each medicine gets a section for its schedule.",
     "Once a day gets one box per day. Every 12 hours gets two (1 of 2 and 2 of 2), every 8 hours "
     "three, every 6 hours four, and every 4 hours six."),
    ("Fill in \u201cDue\u201d with the time the dose is scheduled.",
     "Each dose is due that many hours after the one before. In the builder, set the first dose "
     "of the day and the rest are filled in for you."),
    ("Fill in \u201cTaken\u201d with the time it was actually given.",
     "If it was late, the gap is right there on the page, and you can count 12 hours from when it was really given."),
    ("Follow the arrows.",
     "They point to the next box: down the day, then across to the next day."),
]

TIPS = [
    ("Write the time, not a checkmark.",
     "A checkmark tells you a dose happened. A time tells you when the next one is due."),
    ("Keep the chart where the medicine is.",
     "Taped inside the cabinet door or on the fridge, so nobody has to remember to go find it."),
    ("Everyone writes on the same sheet.",
     "When two people share the feeding and dosing, one chart is how you avoid a missed dose or a double dose."),
    ("Leave it out for the sitter.",
     "Fill in the Due times before you leave, and ask the sitter to write the Taken times."),
    ("Bring it to the vet.",
     "A week of real dose times answers \u201cIs she getting it on schedule?\u201d better than memory does."),
    ("Ask your vet about missed doses ahead of time.",
     "Whether to give a late dose or skip it depends on the medicine. Write their answer on the chart."),
]

FAQ = [
    ("Is this really free?",
     "Yes. No signup and no email. Download it, print it, and you're done."),
    ("Which version should I download?",
     "The printable PDF if you'll write on it by hand. The fillable PDF if you'd rather type the medicine "
     "names and times first. The spreadsheet if you want to add rows or change the layout."),
    ("Does it work for cats, or for more than one pet?",
     "Yes. Write the pet's name beside the medicine, or use the Name line at the top and print one sheet per pet."),
    ("Can I make a chart for every-8-hours, every-6-hours or every-4-hours medicines?",
     "Yes. Use Build your chart at the top of the page and choose how many medicines are on each schedule. "
     "The chart changes as you go, and Print gives you exactly what you see."),
    ("What if my pet takes a lot of medicines?",
     "The builder takes up to six on each schedule. A page holds up to 9 dose rows. Past that, the chart "
     "goes onto a second page, so the boxes stay big enough to write in."),
    ("What size does it print?",
     "Landscape, on US letter paper. One page covers a week. If the week starting date is set, each "
     "day shows its date."),
    ("Is there a version that reminds me?",
     "Pawfolio Free reminds you when each dose is due, lets you tap Given or Skip, and for every-few-hours "
     "medicines counts the next dose from when it was really given. It's free and needs no account. Pawfolio Complete adds sitter "
     "sharing, so your sitter can check off doses on their own phone and you see who gave each one."),
]


def lis(items):
    return "\n".join(f'        <li><strong>{t}</strong> {d}</li>' for t, d in items)


def faq_items():
    return "\n".join(
        f'''      <details class="faq-item"><summary>{q}<span class="chev" aria-hidden="true">&#9662;</span></summary><p>{a}</p></details>'''
        for q, a in FAQ)


def downloads():
    return "\n".join(
        f'''        <a class="dl" href="{f}" download>
          <span class="dl-k">{k}</span><span class="dl-d">{d}</span><span class="dl-go">Download &darr;</span>
        </a>''' for f, k, d in DOWNLOADS)


PAGE = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<meta name="theme-color" content="#f2f4f7" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#15181e" media="(prefers-color-scheme: dark)">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="CleartrackApps">
<meta property="og:url" content="{URL}">
<meta property="og:title" content="Free pet medication chart maker">
<meta property="og:description" content="{DESC}">
<meta property="og:image" content="https://cleartrackapps.com/pet-medication-chart/chart-preview.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="../assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="../assets/favicon-180.png" sizes="180x180">
<link rel="preconnect" href="https://api.fontshare.com" crossorigin>
<link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=general-sans@400,500,600&f[]=zodiak@600,700&display=swap">
<link rel="stylesheet" href="../base.css">
<link rel="stylesheet" href="../style.css">
<style>
  /* Same soft gray / slate blue as the sitter sheet page. */
  body.ps-page {{
    --color-bg: #f2f4f7; --color-bg-alt: #e8edf5; --color-surface: #ffffff; --color-surface-2: #f5f7fa;
    --color-border: #d6dce6; --color-border-strong: #c3cbd8; --color-text: #262b35; --color-text-muted: #5d6676;
    --color-primary: #4c5f8f; --color-primary-hover: #3d4d76; --color-focus: #4c5f8f;
    --accent-pawfolio: #4c5f8f; --accent-pawfolio-soft: #e7ecf6;
    background-color: var(--color-bg);
    background-image: url("paws.svg"); background-repeat: repeat; background-position: center top; background-size: 900px 1100px;
  }}
  [data-theme='dark'] body.ps-page {{
    --color-bg: #15181e; --color-bg-alt: #1b2029; --color-surface: #1e232c; --color-surface-2: #232934;
    --color-border: #333b49; --color-border-strong: #424b5b; --color-text: #dde2ea; --color-text-muted: #9aa3b2;
    --color-primary: #a3b4dc; --color-primary-hover: #bdcae8; --color-focus: #a3b4dc;
    --accent-pawfolio: #a3b4dc; --accent-pawfolio-soft: #252d3d; background-image: url("paws-dark.svg");
  }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme='light']) body.ps-page {{
      --color-bg: #15181e; --color-bg-alt: #1b2029; --color-surface: #1e232c; --color-surface-2: #232934;
      --color-border: #333b49; --color-border-strong: #424b5b; --color-text: #dde2ea; --color-text-muted: #9aa3b2;
      --color-primary: #a3b4dc; --color-primary-hover: #bdcae8; --color-focus: #a3b4dc;
      --accent-pawfolio: #a3b4dc; --accent-pawfolio-soft: #252d3d; background-image: url("paws-dark.svg");
    }}
  }}
  @media (max-width: 640px) {{ body.ps-page {{ background-size: 560px 684px; }} }}
  body.ps-page .site-head {{ background: color-mix(in srgb, var(--color-bg) 92%, transparent); }}
  body.ps-page .ps-alt, body.ps-page .faq {{ background: color-mix(in srgb, var(--color-bg-alt) 45%, transparent); }}
  .ps-hero {{ padding: clamp(1.5rem, 4vw, 2.5rem) 0 1rem; text-align: center; }}
  .ps-hero h1 {{ font-family: Zodiak, Georgia, serif; font-weight: 700;
    font-size: clamp(1.85rem, 5.4vw, 3rem); letter-spacing: -.02em; max-width: 20ch; margin: .4rem auto 0; }}
  .ps-lede {{ max-width: 48ch; margin: .9rem auto 0; font-size: clamp(1rem, 2.2vw, 1.1rem); opacity: .82; }}
  .ps-sec {{ padding: clamp(2rem, 5vw, 3.5rem) 0; }}
  .ps-h2 {{ font-family: Zodiak, Georgia, serif; font-weight: 700; letter-spacing: -.015em;
    font-size: clamp(1.5rem, 4vw, 2.2rem); max-width: 26ch; }}
  .ps-sub {{ max-width: 52ch; margin-top: .6rem; opacity: .78; }}
  .ps-actions {{ display: flex; flex-wrap: wrap; gap: .7rem; justify-content: center; margin-top: 1.4rem; }}
  .ps-note {{ margin-top: .8rem; font-size: .9rem; opacity: .62; text-align: center; }}
  .ps-list {{ max-width: 58ch; margin: 1.2rem 0 0; padding-left: 1.2rem; display: grid; gap: .7rem; }}
  ol.ps-list {{ padding-left: 1.4rem; }}
  .ps-cta {{ max-width: 40rem; margin: 0 auto; text-align: center; }}
  /* The chart preview */
  .chart-fig {{ max-width: 60rem; margin: 1.4rem auto 0; }}
  .chart-fig a {{ display: block; }}
  .chart-fig img {{ width: 100%; height: auto; display: block; background: #fff;
    border: 1px solid var(--color-border); border-radius: 6px; box-shadow: 0 6px 24px rgba(0,0,0,.08); }}
  .chart-fig figcaption {{ margin-top: .6rem; font-size: .85rem; color: var(--color-text-muted); text-align: center; }}
  /* Download cards */
  .dls {{ display: grid; gap: .8rem; max-width: 60rem; margin: 1.6rem auto 0; grid-template-columns: 1fr; }}
  @media (min-width: 720px) {{ .dls {{ grid-template-columns: repeat(3, minmax(0, 1fr)); }} }}
  .dl {{ display: flex; flex-direction: column; gap: .3rem; padding: 1rem 1.1rem; text-decoration: none;
    color: var(--color-text); background: var(--color-surface); border: 1px solid var(--color-border);
    border-radius: var(--radius-lg, 12px); transition: border-color .15s, transform .15s; }}
  .dl:hover {{ border-color: var(--accent-pawfolio); transform: translateY(-1px); }}
  .dl:focus-visible {{ outline: 2px solid var(--accent-pawfolio); outline-offset: 2px; }}
  .dl-k {{ font-weight: 600; font-size: 1.05rem; }}
  .dl-d {{ font-size: .92rem; color: var(--color-text-muted); }}
  .dl-go {{ margin-top: auto; padding-top: .3rem; font-weight: 600; color: var(--accent-pawfolio); }}
  /* Pawfolio nudge under the downloads */
  .ps-text {{ max-width: 60rem; margin: 1.4rem auto 0; padding: 1rem 1.1rem; border-radius: var(--radius, 8px);
    background: var(--accent-pawfolio-soft); border: 1px solid color-mix(in srgb, var(--accent-pawfolio) 25%, transparent); }}
  .ps-text p {{ margin: 0; }}
  .ps-text-h {{ font-weight: 600; font-size: 1.05rem; color: var(--color-text); }}
  .ps-text p + p {{ margin-top: .35rem; color: var(--color-text-muted); }}
  .ps-text-link {{ display: inline-block; margin-top: .6rem; font-weight: 600; color: var(--accent-pawfolio);
    text-decoration: underline; text-underline-offset: 3px; }}
 {BUILDER_CSS}
  .two {{ display: grid; gap: 2rem; }}
  @media (min-width: 880px) {{ .two {{ grid-template-columns: minmax(0, 1fr) minmax(0, 1fr); gap: 3rem; }} }}
</style>
</head>
<body class="ps-page">
<a class="skip" href="#top">Skip to content</a>
<header class="site-head">
  <div class="wrap head-inner">
    <a class="brand" href="../" aria-label="Cleartrack Apps home">
      <span class="lockup logo-head"><img class="logo logo-on-light" src="../assets/logo.png" width="720" height="289" alt="Cleartrack Apps" decoding="async"><img class="logo logo-on-dark" src="../assets/logo-dark.png" width="720" height="289" alt="" aria-hidden="true" decoding="async"></span>
    </a>
  </div>
</header>
<main id="top">
  <section class="ps-hero ps-hide-print">
    <div class="wrap">
      <h1>Free printable pet medication chart</h1>
      <p class="ps-lede">A weekly dose log for dogs and cats. Pick medicines given every 24, 12, 8, 6 or
        4 hours, then print. Write the time each dose is due and the time it was actually given.</p>
      <div class="ps-actions">
        <a class="btn btn-primary btn-lg" href="#builder">Build your chart</a>
        <a class="btn btn-ghost btn-lg" href="#downloads">Download a ready-made PDF</a>
      </div>
    </div>
  </section>
{BUILDER_HTML}
  <section class="ps-sec ps-alt ps-hide-print" aria-labelledby="dl-h">
    <div class="wrap">
      <h2 class="ps-h2" id="dl-h" style="margin-inline:auto;text-align:center">Or download the ready-made chart</h2>
      <p class="ps-sub" style="margin-inline:auto;text-align:center">Two once-a-day sections and two every-12-hours sections, Sunday through Saturday.</p>
      <figure class="chart-fig">
        <a href="pet-medication-chart.pdf" target="_blank" rel="noopener"><img src="chart-preview.png" width="1650" height="960" loading="lazy"
          alt="Weekly medication chart with two every-24-hours sections and two every-12-hours sections, Sunday through Saturday, with Due and Taken lines for each dose"></a>
      </figure>
      <div class="dls" id="downloads">
{downloads()}
      </div>
      <div class="ps-text">
        <p class="ps-text-h">Rather have your phone remind you?</p>
        <p>Pawfolio Free reminds you when each dose is due. Tap Given or Skip, and for every-few-hours
          medicines it counts the next dose from when it was really given. No account.</p>
        <a class="ps-text-link" href="{TIP_LINK}">Try Pawfolio&nbsp;Free&nbsp;&rarr;</a>
      </div>
      <p class="ps-note">Free. No signup, no email.</p>
    </div>
  </section>
  <section class="ps-sec ps-hide-print" aria-labelledby="how-h">
    <div class="wrap two">
      <div>
        <h2 class="ps-h2" id="how-h">How to use the chart</h2>
        <ol class="ps-list">
{lis(HOW)}
        </ol>
      </div>
      <div>
        <h2 class="ps-h2" id="tips-h">Tips for keeping doses on schedule</h2>
        <ul class="ps-list">
{lis(TIPS)}
        </ul>
      </div>
    </div>
  </section>
  <section class="ps-sec ps-alt ps-hide-print" aria-labelledby="cta-h">
    <div class="wrap ps-cta">
      <h2 class="ps-h2" id="cta-h" style="margin-inline:auto">Want reminders instead of paper?</h2>
      <p class="ps-sub" style="margin-inline:auto">Pawfolio Free keeps each pet's medications with a reminder
        when a dose or a refill is due. Tap Given or Skip, with Undo if you tap by mistake. No account,
        and your records stay on your phone. With Pawfolio Complete, your sitter can check off doses on
        their own phone, and you see who gave each one.</p>
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
      <a href="../pet-sitter-instructions/">Free pet sitter sheet</a>
      <a href="https://instagram.com/cleartrackapps" target="_blank" rel="noopener noreferrer">Instagram</a>
      <a href="https://www.pinterest.com/cleartrackapps" target="_blank" rel="noopener noreferrer">Pinterest</a>
      <a href="mailto:cleartrackapps@gmail.com">cleartrackapps@gmail.com</a>
    </nav>
    <p class="foot-fine">&copy; 2026 CleartrackApps. Pawfolio&trade; is a trademark of CleartrackApps.</p>
  </div>
</footer>
<script src="../app.js" defer></script>
{BUILDER_JS}
{CF_BEACON}
</body>
</html>
'''

if __name__ == "__main__":
    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / "index.html").write_text(PAGE, encoding="utf-8")
    print("wrote", OUT_DIR / "index.html")
