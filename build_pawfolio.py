#!/usr/bin/env python3
"""Generates /pawfolio/index.html — a single-product landing page for traffic
arriving from Instagram.

Why this page exists: the storefront index sells five apps at once. Someone who
clicks through from a Reel about vet paperwork lands there and has to work out
which of the five is the pet one before anything else happens. Most don't. This
page opens on the exact question the Reel asked, so the arrival is continuous,
and it offers one decision instead of five.

Buy links reuse the existing /go/pawfolio/ tracked redirect so clicks stay
countable in Cloudflare alongside the rest of the site. Re-run this after
build.py; it writes only into ./pawfolio/.
"""
import pathlib

ROOT = pathlib.Path(__file__).parent
OUT_DIR = ROOT / "pawfolio"
DEMO = "https://cleartrackapps.com/pet-care-planner-demo/"
BUY = "https://cleartrackapps.com/go/pawfolio/"
# The Etsy listing is paused while the subscription launches. The /go/ redirect still
# exists, so putting this link back is a one-line change if a one-time Etsy licence
# ever ships.
ETSY = "https://cleartrackapps.com/go/pawfolio-etsy/"
APP = "https://cleartrackapps.com/pet-care-planner/"   # the free app itself
PRICE_YEAR = "$29.99"
PRICE_MONTH = "$4.99"

CF_BEACON = (
    '<!-- Cloudflare Web Analytics: privacy-first, no cookies, no consent banner needed -->\n'
    '<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
    'data-cf-beacon=\'{"token": "5673e14274004df9a11f87d759a6b624"}\'></script>'
)

TITLE = "Pawfolio — your pet's whole life, on your phone"
DESC = ("Vet visits, medications, vaccination dates, weight and receipts for every pet you have — "
        "in one offline app. No account needed and your records stay on your phone. "
        "Free to use. Pawfolio Complete is $4.99 a month or $29.99 a year.")

FREE_FEATURES = [
    ("Unlimited pets", "One dog or a full household &mdash; each pet gets its own profile."),
    ("Everything due, at a glance", "The home screen shows what's coming up."),
    ("Medications &amp; supplements", "What each pet takes, the dose, and a reminder when a refill or a dose is due."),
    ("Dose tracking", "Tap Given or Skip for each dose, with Undo if you tap by mistake. Set times, or every few hours from the last dose, plus what to do if one is missed."),
    ("Microchip, rabies date and insurance", "On the profile, ready to read out."),
    ("Your vet's details", "Tap to call, straight from the app."),
    ("Pet-sitter sheet", "A printable page with tap-to-call numbers &mdash; and you can text it to a sitter. Always free."),
    ("Notes and useful links", "Insurance providers, pet pharmacies, airline pet policies."),
    ("Print, back up and export", "Your records, any time."),
]

PAID_FEATURES = [
    ("Share doses with a sitter", "Send your sitter a link to the medications you choose. They check off each dose and get reminders, and you see who gave it. <a href=\"sitter-sharing/\">Watch how it works</a>"),
    ("Vet visit history", "Date, reason, what the vet found, the cost and the weight for every appointment, with a photo of the receipt attached to the visit it belongs to."),
    ("Vaccination due dates", "What was given, when, and what's next &mdash; with a reminder before it expires."),
    ("Weight tracking", "Drawn as a chart, so a slow gain or loss is easy to see."),
    ("Expense history", "What you're actually spending per pet, by category."),
    ("Timeline", "All of a pet's records in one history, newest first."),
    ("Document vault", "Certificates, receipts, adoption papers and lab results, filed under the right pet."),
]

FAQ = [
    ("Is this in the App Store?",
     "No, and that's deliberate. You open a link on your phone and add it to your home screen — "
     "about two minutes. After that it behaves like any other app icon, and it opens with no internet."),
    ("Does it work without signal?",
     "Yes. Everything runs on your device. That matters most in a vet's back room or a rural "
     "boarding kennel, which is exactly where you need it. Phone reminders and checking off "
     "doses need a connection."),
    ("Where is my pet's information stored?",
     "On your phone. There's no account and no server holding your records. If you send the "
     "sitter sheet, it's scrambled on your phone first and I can't read it. If you turn on "
     "reminders or share doses with a sitter, only the item name, your pet's name and the times "
     "go to Pawfolio's reminder service."),
    ("Can I add more than one pet?",
     "As many as you want, each with a separate profile. It was built for multi-pet households "
     "because that's where remembering everything actually breaks down."),
    ("What do I actually get for free?",
     "Unlimited pets, medications with refill and dose reminders, dose tracking, your vet's tap-to-call details, "
     "the microchip and rabies dates, the printable pet-sitter sheet, notes, the useful-links "
     "directory, and printing and backups. Most people can run their household on that."),
    ("Can I upgrade now?",
     "Yes. Pawfolio Complete is $4.99 a month or $29.99 a year. Your license key arrives by "
     "email: tap Open Pawfolio in the receipt, or open the app, tap any locked tab and enter "
     "the key. Everything described as free still needs no card."),
    ("Can my pet sitter see the doses?",
     "With Pawfolio Complete, yes. Send your sitter a link to the medications you choose. They "
     "check off each dose and get reminders on their own phone, and you see who gave it and when. "
     "The printable sitter sheet stays free."),
    ("What happens if I cancel?",
     "Your records stay. Vet visits, vaccinations, weights, expenses, the timeline and the vault "
     "all go read-only — still there, still printable, still exportable. You just can't add new "
     "entries until you subscribe again, and sharing doses with a sitter stops. Nothing is "
     "deleted and nothing is held hostage."),
    ("I already bought Pawfolio. Am I losing anything?",
     "No. Pawfolio unlocks itself for anyone who was already using it, free and permanently, "
     "including anyone who previously purchased the app. You don't need a code and you don't "
     "need to contact me."),
    ("What if it isn't for me?",
     "Start with Pawfolio Free — there's nothing to lose and no card involved. If you upgrade "
     "to Pawfolio Complete and change your mind, cancel any time. On the yearly plan, email "
     "cleartrackapps@gmail.com within 30 days for a full refund. Pawfolio Complete then switches "
     "off, and your records stay in Pawfolio Free."),
]


def free_list():
    return "\n".join(f"            <li>{t}</li>" for t, _ in FREE_FEATURES)


def paid_list():
    return "\n".join(f"            <li>{t}</li>" for t, _ in PAID_FEATURES)


def faq_items():
    return "\n".join(
        f'''      <details class="faq-item">
        <summary>{q}</summary>
        <p>{a}</p>
      </details>''' for q, a in FAQ)


PAGE = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<meta name="description" content="{DESC}">
<meta name="theme-color" content="#f5f6f8" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#15181e" media="(prefers-color-scheme: dark)">
<link rel="canonical" href="https://cleartrackapps.com/pawfolio/">
<meta property="og:type" content="product">
<meta property="og:site_name" content="CleartrackApps">
<meta property="og:url" content="https://cleartrackapps.com/pawfolio/">
<meta property="og:title" content="{TITLE}">
<meta property="og:description" content="{DESC}">
<meta property="og:image" content="https://cleartrackapps.com/assets/og-pawfolio.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="Pawfolio — pet records that work offline.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{TITLE}">
<meta name="twitter:description" content="{DESC}">
<meta name="twitter:image" content="https://cleartrackapps.com/assets/og-pawfolio.png">
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="../assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="../assets/favicon-180.png" sizes="180x180">
<link rel="preconnect" href="https://api.fontshare.com" crossorigin>
<link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=general-sans@400,500,600&f[]=zodiak@600,700&display=swap">
<link rel="stylesheet" href="../base.css?v=20261014f">
<link rel="stylesheet" href="../style.css?v=20261014f">
<style>
  /* Pawfolio page: a short product page. Hero with the app, one side-by-side
     Free / Complete comparison, three pictures, then questions. The six-question
     quiz that used to be the hero is gone; its ?from=daisy arrivals now land on
     the Timeline picture (see the script at the bottom). */
  .pf-hero {{ padding: clamp(2rem, 5vw, 3.5rem) 0 clamp(2.5rem, 6vw, 4rem); }}
  .pf-hero-grid {{ display: grid; gap: 2.5rem; align-items: center; }}
  .pf-hero h1 {{ font-family: Zodiak, Georgia, serif; font-weight: 700;
    font-size: clamp(1.9rem, 5vw, 3rem); letter-spacing: -.02em; max-width: 18ch; margin-top: .6rem; }}
  .pf-lede {{ max-width: 42ch; margin-top: 1rem; font-size: clamp(1rem, 2.2vw, 1.1rem);
    color: var(--color-text-muted); }}
  .pf-actions {{ display: flex; flex-wrap: wrap; gap: .8rem; margin-top: 1.8rem; }}
  .pf-ticks {{ display: flex; flex-wrap: wrap; gap: .4rem 1.1rem; margin-top: 1.4rem;
    font-size: var(--text-xs); color: var(--color-text-muted); }}
  .pf-ticks li::before {{ content: "\\2713"; color: var(--accent-pawfolio); font-weight: 700; margin-right: .4rem; }}
  .pf-shots {{ display: flex; gap: 1rem; justify-content: center; }}
  .pf-shot {{ flex: 1 1 0; max-width: 15rem; margin: 0; }}
  .pf-shot:nth-child(2) {{ margin-top: 2.5rem; }}
  .pf-frame {{ position: relative; border-radius: 22px; overflow: hidden; aspect-ratio: 780 / 1280;
    border: 1px solid var(--color-border); background: var(--color-surface); box-shadow: var(--shadow-md); }}
  .pf-frame img {{ width: 100%; height: auto; display: block; }}
  .pf-frame::after {{ content: ""; position: absolute; inset: auto 0 0 0; height: 16%;
    background: linear-gradient(to bottom, transparent, var(--color-surface)); pointer-events: none; }}

  .pf-sec {{ padding: clamp(2.5rem, 6vw, 4rem) 0; }}
  .pf-sec-alt {{ background: transparent; }}
  .pf-h2 {{ font-family: Zodiak, Georgia, serif; font-weight: 700; letter-spacing: -.015em;
    font-size: clamp(1.5rem, 4vw, 2.2rem); }}
  .pf-sub {{ max-width: 52ch; margin-top: .6rem; color: var(--color-text-muted); font-size: var(--text-sm); }}

  .plans {{ display: grid; gap: 1.25rem; margin-top: 2rem; }}
  .plan {{ background: var(--color-surface); border: 1px solid var(--color-border);
    border-radius: var(--radius-lg); padding: 1.5rem 1.4rem; box-shadow: var(--shadow-sm);
    display: flex; flex-direction: column; }}
  .plan-top {{ border-top: 3px solid var(--accent-pawfolio); }}
  .plan-name {{ font-weight: 600; font-size: 1.05rem; }}
  .plan-price {{ font-family: Zodiak, Georgia, serif; font-weight: 700; font-size: 2rem; margin-top: .35rem; }}
  .plan-price small {{ font-family: var(--font-body); font-size: .9rem; font-weight: 500; color: var(--color-text-muted); margin-left: .3rem; }}
  .plan-note {{ font-size: var(--text-sm); color: var(--color-text-muted); margin-top: .2rem; }}
  .plan ul {{ margin: 1.2rem 0 1.4rem; display: grid; gap: .55rem; font-size: var(--text-sm); }}
  .plan li {{ display: grid; grid-template-columns: 1.1rem 1fr; gap: .45rem; }}
  .plan li::before {{ content: "\\2713"; color: var(--accent-pawfolio); font-weight: 700; }}
  .plan li.plus::before {{ content: "+"; }}
  .plan .btn {{ margin-top: auto; }}
  .plan-fine {{ font-size: var(--text-xs); color: var(--color-text-muted); margin-top: .8rem; }}
  .plan-fine a {{ color: var(--accent-pawfolio); font-weight: 600; }}
  /* "Pawfolio COMPLETE": the tier's name mark. */
  .pf-tag {{ display: inline-block; vertical-align: .14em; margin-left: .15em;
    font-weight: 700; font-size: .66em; letter-spacing: .04em; text-transform: uppercase; line-height: 1;
    padding: .3em .5em .26em; border-radius: 999px;
    background: var(--accent-pawfolio); color: var(--accent-pawfolio-soft); white-space: nowrap; }}

  .looks {{ list-style: none; padding: 0; margin: 2rem 0 0; display: grid; gap: 1.25rem; }}
  .look {{ display: grid; grid-template-rows: auto 1fr; background: var(--color-surface);
    border: 1px solid var(--color-border); border-radius: var(--radius-lg); overflow: hidden;
    box-shadow: var(--shadow-sm); text-decoration: none; color: inherit; height: 100%;
    transition: box-shadow .22s var(--ease), border-color .22s var(--ease); }}
  a.look:hover {{ box-shadow: var(--shadow-md); border-color: var(--accent-pawfolio); }}
  .look-img {{ aspect-ratio: 4 / 3; overflow: hidden; background: var(--color-surface-2); }}
  .look-img img {{ width: 100%; height: 100%; object-fit: cover; }}
  .look-img.top img {{ object-position: top; }}
  .look-body {{ padding: 1rem 1.1rem 1.15rem; }}
  .look-title {{ font-weight: 600; display: block; }}
  .look-title span {{ color: var(--accent-pawfolio); }}
  .look-copy {{ margin-top: .25rem; font-size: var(--text-sm); color: var(--color-text-muted); }}
  .look-tag {{ display: block; margin-bottom: .2rem; font-size: .68rem; font-weight: 700; letter-spacing: .05em;
    text-transform: uppercase; color: var(--accent-pawfolio); vertical-align: .1em; }}

  .pf-faq {{ max-width: 44rem; }}
  .foot-verse {{ font-family: Zodiak, Georgia, serif; font-size: .9rem; font-style: italic;
    line-height: 1.5; color: var(--color-text-muted); }}
  .foot-verse cite {{ font-style: normal; font-size: .82em; opacity: .8; white-space: nowrap; }}

  @media (min-width: 46rem) {{
    .plans {{ grid-template-columns: 1fr 1fr; align-items: stretch; }}
    .looks {{ grid-template-columns: repeat(3, 1fr); }}
  }}
  @media (min-width: 62rem) {{
    .pf-hero-grid {{ grid-template-columns: 1.1fr 1fr; gap: 3rem; }}
  }}
</style>
</head>
<body>
<a class="skip" href="#top">Skip to content</a>

<header class="site-head"></header>

<main id="top">

  <section class="pf-hero" aria-labelledby="pf-h">
    <div class="wrap pf-hero-grid">
      <div>
        <p class="eyebrow">Pawfolio &mdash; for pet owners</p>
        <h1 id="pf-h">Every vet detail for every pet, on your phone.</h1>
        <p class="pf-lede">Medications, dose reminders, vet numbers and a sitter sheet, free for as many pets as you have. It works offline, with no account.</p>
        <div class="pf-actions">
          <a class="btn btn-primary btn-lg js-free-cta" href="{APP}">Open Pawfolio Free</a>
          <a class="btn btn-ghost btn-lg" href="{DEMO}">Try the demo</a>
        </div>
        <ul class="pf-ticks">
          <li>Unlimited pets</li>
          <li>Works offline</li>
          <li>No account</li>
          <li>Records stay on your phone</li>
        </ul>
      </div>
      <div class="pf-shots">
        <figure class="pf-shot">
          <div class="pf-frame"><img src="../assets/pawfolio-overview.png" width="780" height="1600" decoding="async"
            alt="Pawfolio overview screen: two pets, Bella and Milo, with upcoming medications and vaccinations."></div>
        </figure>
        <figure class="pf-shot">
          <div class="pf-frame"><img src="../assets/pawfolio-pets.png" width="780" height="1600" decoding="async"
            alt="Pawfolio pet profiles screen with Bella's breed, microchip and vet details."></div>
        </figure>
      </div>
    </div>
  </section>

  <section class="pf-sec pf-sec-alt" id="plans" aria-labelledby="plans-h">
    <div class="wrap">
      <h2 class="pf-h2" id="plans-h">Free, or Complete</h2>
      <p class="pf-sub">Free isn't a trial. Complete adds the long-term records and live dose sharing with your sitter.</p>
      <div class="plans">
        <div class="plan">
          <p class="plan-name">Pawfolio <span class="pf-tag">Free</span></p>
          <p class="plan-price">$0<small>forever</small></p>
          <p class="plan-note">No card, ever.</p>
          <ul>
{free_list()}
          </ul>
          <a class="btn btn-ghost btn-lg js-free-cta" href="{APP}">Open Pawfolio Free</a>
        </div>
        <div class="plan plan-top">
          <p class="plan-name">Pawfolio <span class="pf-tag">Complete</span></p>
          <p class="plan-price">{PRICE_MONTH}<small>a month</small></p>
          <p class="plan-note">or {PRICE_YEAR} a year. Cancel any time.</p>
          <ul>
            <li class="plus">Everything in Free</li>
{paid_list()}
          </ul>
          <a class="btn btn-primary btn-lg js-upgrade-cta" href="{BUY}">Get Pawfolio Complete</a>
          <p class="plan-fine">If you stop paying, your records stay visible, printable and exportable. Already using Pawfolio? You keep everything free.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="pf-sec" aria-labelledby="looks-h">
    <div class="wrap">
      <h2 class="pf-h2" id="looks-h">A closer look</h2>
      <ul class="looks">
        <li>
          <a class="look" href="sitter-sharing/">
            <span class="look-img"><img src="sitter-sharing/give-pill.jpg" alt="Hands giving a pill in a treat to a golden retriever in a kitchen." loading="lazy" decoding="async"></span>
            <span class="look-body">
              <span class="look-tag">Complete</span><span class="look-title">Share doses with a sitter</span>
              <span class="look-copy" style="display:block">They tap Given on their phone, and you see who gave each dose. <span style="color:var(--accent-pawfolio);font-weight:600">Watch how &rarr;</span></span>
            </span>
          </a>
        </li>
        <li id="timeline">
          <div class="look">
            <span class="look-img top"><img src="../assets/daisy-timeline.png" width="780" height="660" alt="A Pawfolio timeline card: Daisy, Emergency, 08/16/2026 at 4:15 AM at a 24-hour emergency vet. The vet tried to lance the abscess and found that it is instead a mast cell tumor." loading="lazy" decoding="async"></span>
            <span class="look-body">
              <span class="look-tag">Complete</span><span class="look-title">Every visit, in one timeline</span>
              <span class="look-copy" style="display:block">Reasons, findings and costs, newest first. Ready when the next vet asks.</span>
            </span>
          </div>
        </li>
        <li>
          <a class="look" href="../pet-sitter-instructions/">
            <span class="look-img top"><img src="../pet-sitter-instructions/example-sheet.png" alt="A filled-in pet sitter instructions sheet with owner and emergency contacts." loading="lazy" decoding="async"></span>
            <span class="look-body">
              <span class="look-tag">Free</span><span class="look-title">A sitter sheet to print or text</span>
              <span class="look-copy" style="display:block">Feeding, meds and tap-to-call vet numbers on one page. <span style="color:var(--accent-pawfolio);font-weight:600">Get the free sheet &rarr;</span></span>
            </span>
          </a>
        </li>
      </ul>
    </div>
  </section>

  <section class="pf-sec pf-sec-alt" id="faq" aria-labelledby="faq-h">
    <div class="wrap pf-faq">
      <h2 class="pf-h2" id="faq-h">Questions</h2>
      <div class="faq-list" style="margin-top:1.5rem">
{faq_items()}
      </div>
    </div>
  </section>

</main>

<footer class="site-foot"></footer>

<script src="../app.js?v=20261014f" defer></script>
<script src="../meta-pixel.js" defer></script>
<script>
(function () {{
  // Visitors from the Daisy reel (?from=daisy) were promised her timeline:
  // bring that picture into view instead of the top of the page.
  if (/(^|[?&])from=daisy(&|$)/.test(location.search)) {{
    window.addEventListener('load', function () {{
      var t = document.getElementById('timeline');
      if (t) t.scrollIntoView({{ block: 'center' }});
    }});
  }}
  function track(name, params) {{ if (typeof window.ctTrack === 'function') window.ctTrack(name, params || {{}}); }}
  // Same event names the quiz used, so Meta reporting carries on.
  if (/(^|[?&])from=daisy(&|$)/.test(location.search)) track('DaisyLanding');
  else if (/(^|[?&])utm_medium=paid(&|$)/.test(location.search)) track('PaidLanding');
  document.addEventListener('click', function (e) {{
    var a = e.target.closest && e.target.closest('a');
    if (!a) return;
    if (a.classList.contains('js-upgrade-cta')) track('CtaClick', {{ cta: 'complete' }});
    else if (a.classList.contains('js-free-cta')) track('CtaClick', {{ cta: 'free' }});
  }});
}})();
</script>
{CF_BEACON}
</body>
</html>
'''

OUT_DIR.mkdir(exist_ok=True)
import chrome
PAGE = chrome.apply(PAGE, "../", "&copy; 2026 CleartrackApps. Pawfolio&trade; is a trademark of CleartrackApps.", extra='\n    <p class="foot-verse">&ldquo;The righteous care for the needs of their animals.&rdquo;\n      <cite>&mdash; Proverbs 12:10</cite></p>')
(OUT_DIR / "index.html").write_text(PAGE, encoding="utf-8")
print(f"wrote {OUT_DIR / 'index.html'} ({len(PAGE)} bytes)")

# ---------------------------------------------------------------------------
# Quiz step stubs.
#
# quiz.js pushes a real path as the visitor advances (/pawfolio/q2/ ... /q6/,
# then /pawfolio/score/) so Cloudflare Web Analytics reports quiz drop-off in
# the Paths list. pushState never fetches those URLs, but a refresh, a shared
# link or a crawler would, so each one gets a real file that bounces back to
# the landing page.
#
# Deliberately no Cloudflare beacon on these: a direct hit on a stub is not a
# real funnel step and must not inflate the counts it exists to measure.
# noindex keeps them out of search results.
# ---------------------------------------------------------------------------
STEP_STUBS = {
    "q2": "Question 2",
    "q3": "Question 3",
    "q4": "Question 4",
    "q5": "Question 5",
    "q6": "Question 6",
    "score": "Your score",
    # Paid traffic skips the quiz and lands straight on the answers, so that
    # view gets a countable path of its own.
    "where": "Where each answer lives",
    # The Daisy reel tells a story rather than asking the six questions, so
    # its arrivals land on their own panel and get their own countable path.
    "daisy": "Daisy's timeline",
}

STUB = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, follow">
<title>{label} &mdash; Pawfolio</title>
<link rel="canonical" href="https://cleartrackapps.com/pawfolio/">
<meta http-equiv="refresh" content="0; url=/pawfolio/">
<script>location.replace('/pawfolio/' + location.search);</script>
</head>
<body>
<p>Taking you to <a href="/pawfolio/">Pawfolio</a>&hellip;</p>
</body>
</html>
'''

for seg, label in STEP_STUBS.items():
    d = OUT_DIR / seg
    d.mkdir(exist_ok=True)
    (d / "index.html").write_text(STUB.format(label=label), encoding="utf-8")
print(f"wrote {len(STEP_STUBS)} quiz step stubs: {', '.join(STEP_STUBS)}")
