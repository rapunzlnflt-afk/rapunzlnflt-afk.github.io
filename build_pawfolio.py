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
ETSY = "https://cleartrackapps.com/go/pawfolio-etsy/"
PRICE = "$14.99"

CF_BEACON = (
    '<!-- Cloudflare Web Analytics: privacy-first, no cookies, no consent banner needed -->\n'
    '<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
    'data-cf-beacon=\'{"token": "5673e14274004df9a11f87d759a6b624"}\'></script>'
)

TITLE = "Pawfolio — your pet's whole life, on your phone"
DESC = ("Vet visits, medications, vaccination dates, weight and receipts for every pet you have — "
        "in one offline app. No account, no subscription, nothing leaves your phone. "
        "One-time $14.99 with a 30-day money-back guarantee.")

QUESTIONS = [
    ("When was the last vaccination?", "Every due date, with the next one already worked out."),
    ("Which medication, and what dose?", "Current medications and supplements per pet."),
    ("What was the weight at the last visit?", "A weight history you can actually see a trend in."),
    ("What was the diagnosis last time?", "Every visit, reason, diagnosis and what it cost."),
    ("When was the last flea and tick dose?", "Logged with the rest, not in your head."),
    ("What is the microchip number?", "On the profile, ready to read out."),
]

FEATURES = [
    ("Unlimited pets", "One dog or a full household — each pet gets its own profile."),
    ("Vet visit history", "Date, reason, diagnosis, weight and cost for every appointment."),
    ("Vaccination due dates", "See what's coming up before the reminder card arrives."),
    ("Medications &amp; supplements", "What each pet takes, and the dose."),
    ("Weight tracking", "Entries over time, per pet."),
    ("Expense history", "What you're actually spending, per pet."),
    ("Document vault", "Records, receipts, adoption papers, insurance details."),
    ("Pet-sitter sheet", "A printable page with tap-to-call vet numbers."),
]

FAQ = [
    ("Is this in the App Store?",
     "No, and that's deliberate. You open a link on your phone and add it to your home screen — "
     "about two minutes. After that it behaves like any other app icon, and it opens with no internet."),
    ("Does it work without signal?",
     "Yes. Everything runs on your device. That matters most in a vet's back room or a rural "
     "boarding kennel, which is exactly where you need it."),
    ("Where is my pet's information stored?",
     "On your phone, and nowhere else. There is no account to create and no server holding your "
     "records. Nothing is uploaded, so there is nothing of yours for anyone to lose."),
    ("Can I add more than one pet?",
     "As many as you want, each with a separate profile. It was built for multi-pet households "
     "because that's where remembering everything actually breaks down."),
    ("What if it isn't for me?",
     "Email cleartrackapps@gmail.com within 30 days and you get your money back. Try the demo "
     "first though — it's the whole app, free, with no email required."),
]


def q_cards():
    out = []
    for i, (q, a) in enumerate(QUESTIONS, 1):
        out.append(f'''        <li class="q-item">
          <span class="q-num">{i:02d}</span>
          <div>
            <p class="q-ask">{q}</p>
            <p class="q-ans">{a}</p>
          </div>
        </li>''')
    return "\n".join(out)


def f_cards():
    return "\n".join(
        f'''        <li class="f-item"><h3 class="f-title">{t}</h3><p class="f-body">{b}</p></li>'''
        for t, b in FEATURES)


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
<meta name="theme-color" content="#faf6ef" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#181410" media="(prefers-color-scheme: dark)">
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
<link rel="stylesheet" href="../base.css">
<link rel="stylesheet" href="../style.css">
<style>
  .pf-hero {{ padding: clamp(3rem, 8vw, 5.5rem) 0 clamp(2rem, 5vw, 3rem); text-align: center; }}
  .pf-hero h1 {{ font-family: Zodiak, Georgia, serif; font-weight: 700;
    font-size: clamp(2.1rem, 6.4vw, 3.6rem); letter-spacing: -.02em; max-width: 22ch;
    margin: .75rem auto 0; }}
  .pf-lede {{ max-width: 46ch; margin: 1.15rem auto 0; font-size: clamp(1.02rem, 2.4vw, 1.18rem);
    opacity: .82; }}
  .pf-actions {{ display: flex; flex-wrap: wrap; gap: .8rem; justify-content: center;
    margin-top: 2rem; }}
  .pf-micro {{ margin-top: 1rem; font-size: .92rem; opacity: .62; }}
  .pf-sec {{ padding: clamp(2.5rem, 6vw, 4rem) 0; }}
  .pf-sec-alt {{ background: var(--bg-alt, #f4eee3); }}
  .pf-h2 {{ font-family: Zodiak, Georgia, serif; font-weight: 700; letter-spacing: -.015em;
    font-size: clamp(1.6rem, 4.4vw, 2.4rem); max-width: 26ch; }}
  .pf-h2.center {{ margin-inline: auto; text-align: center; }}
  .pf-sub {{ max-width: 52ch; margin-top: .75rem; opacity: .78; }}
  .pf-sub.center {{ margin-inline: auto; text-align: center; }}
  .q-list {{ list-style: none; padding: 0; margin: 2rem 0 0; display: grid; gap: .9rem;
    grid-template-columns: repeat(auto-fit, minmax(19rem, 1fr)); }}
  .q-item {{ display: flex; gap: 1.1rem; align-items: flex-start; padding: 1.15rem 1.3rem;
    background: rgba(255,255,255,.55); border: 1px solid rgba(42,35,24,.09);
    border-radius: 16px; }}
  .q-num {{ font-family: Zodiak, Georgia, serif; font-weight: 700; font-size: 1.35rem;
    color: #464191; line-height: 1.2; flex: none; }}
  .q-ask {{ font-weight: 600; }}
  .q-ans {{ margin-top: .3rem; font-size: .95rem; opacity: .72; }}
  .pf-shots {{ display: flex; gap: clamp(1rem, 4vw, 2.5rem); justify-content: center;
    align-items: flex-start; margin-top: 2.5rem; flex-wrap: wrap; }}
  .pf-shot {{ max-width: 17rem; flex: 1 1 14rem; }}
  /* base.css sets max-width:100% on img but not height, so the intrinsic height
     attribute would stretch these vertically once the column narrows. */
  .pf-shot img {{ height: auto; width: 100%; }}
  .pf-frame {{ position: relative; border-radius: 20px; overflow: hidden;
    border: 1px solid rgba(42,35,24,.12);
    box-shadow: 0 24px 50px -26px rgba(20,16,10,.4); }}
  /* The source captures are scrolling screens, so the bottom edge lands mid-row.
     Fading it out reads as intentional instead of like a broken crop. */
  .pf-frame::after {{ content: ""; position: absolute; inset: auto 0 0 0; height: 18%;
    background: linear-gradient(to bottom, rgba(250,246,239,0), #faf6ef);
    pointer-events: none; }}
  .pf-cap {{ margin-top: .8rem; font-size: .9rem; opacity: .68; text-align: center; }}
  .f-list {{ list-style: none; padding: 0; margin: 2rem 0 0; display: grid; gap: 1.4rem 2rem;
    grid-template-columns: repeat(auto-fit, minmax(15rem, 1fr)); }}
  .f-title {{ font-size: 1.02rem; font-weight: 600; }}
  .f-body {{ margin-top: .3rem; font-size: .95rem; opacity: .75; }}
  .pf-buy {{ text-align: center; }}
  .pf-price {{ font-family: Zodiak, Georgia, serif; font-weight: 700;
    font-size: clamp(2.4rem, 7vw, 3.2rem); }}
  .pf-price small {{ display: block; font-family: inherit; font-size: .95rem;
    font-weight: 500; opacity: .66; margin-top: .3rem; }}
  .pf-faq {{ max-width: 44rem; margin-inline: auto; }}
  .pf-back {{ display: inline-block; margin-top: 2.5rem; font-size: .95rem; opacity: .7; }}
  @media (prefers-color-scheme: dark) {{
    .q-item {{ background: rgba(255,255,255,.05); border-color: rgba(255,255,255,.12); }}
    .pf-frame::after {{ background: linear-gradient(to bottom, rgba(24,20,16,0), #181410); }}
  }}
</style>
</head>
<body>
<a class="skip" href="#questions">Skip to the questions</a>

<header class="site-head">
  <div class="wrap head-inner">
    <a class="brand" href="../" aria-label="Cleartrack Apps home">
      <span class="lockup logo-head"><img class="logo logo-on-light" src="../assets/logo.png" width="720" height="289" alt="Cleartrack Apps" decoding="async"><img class="logo logo-on-dark" src="../assets/logo-dark.png" width="720" height="289" alt="" aria-hidden="true" decoding="async"></span>
    </a>
  </div>
</header>

<main id="top">

  <section class="pf-hero">
    <div class="wrap">
      <p class="eyebrow">Pawfolio &mdash; for pet owners</p>
      <h1>Could you answer these 6 questions about your pet?</h1>
      <p class="pf-lede">Your vet asks every one of them. Pawfolio keeps the answers
        on your phone, so you're not standing there scrolling your photos looking
        for a piece of paper.</p>
      <div class="pf-actions">
        <a class="btn btn-primary btn-lg" href="{DEMO}">Try the free demo</a>
        <a class="btn btn-ghost btn-lg" href="{BUY}">Buy now &mdash; {PRICE}</a>
      </div>
      <p class="pf-micro">The demo is the whole app. No email, no account, nothing to install.</p>
    </div>
  </section>

  <section class="pf-sec pf-sec-alt" id="questions" aria-labelledby="q-h">
    <div class="wrap">
      <h2 class="pf-h2 center" id="q-h">The six that catch everyone</h2>
      <p class="pf-sub center">Most people manage two. Here's where each answer lives.</p>
      <ul class="q-list">
{q_cards()}
      </ul>
    </div>
  </section>

  <section class="pf-sec" aria-labelledby="shot-h">
    <div class="wrap">
      <h2 class="pf-h2 center" id="shot-h">You shouldn't have to remember all of this</h2>
      <p class="pf-sub center">So it's all in one place, on the home screen, working offline.</p>
      <div class="pf-shots">
        <figure class="pf-shot">
          <div class="pf-frame"><img src="../assets/pawfolio-overview.png" width="780" height="1600" loading="lazy" decoding="async"
            alt="Pawfolio overview screen showing two pets with their latest weights and upcoming reminders."></div>
          <figcaption class="pf-cap">Everything due, at a glance.</figcaption>
        </figure>
        <figure class="pf-shot">
          <div class="pf-frame"><img src="../assets/pawfolio-pets.png" width="780" height="1600" loading="lazy" decoding="async"
            alt="Pawfolio pet profiles screen showing a dog and a cat with breed, age, microchip and allergy details."></div>
          <figcaption class="pf-cap">One profile per pet, however many you have.</figcaption>
        </figure>
      </div>
    </div>
  </section>

  <section class="pf-sec pf-sec-alt" aria-labelledby="f-h">
    <div class="wrap">
      <h2 class="pf-h2" id="f-h">What's in it</h2>
      <ul class="f-list">
{f_cards()}
      </ul>
    </div>
  </section>

  <section class="pf-sec" aria-labelledby="how-h">
    <div class="wrap">
      <h2 class="pf-h2 center" id="how-h">How a download becomes an app on your phone</h2>
      <p class="pf-sub center">Four steps, about two minutes. No app store involved.</p>
      <ol class="steps">
        <li class="step"><span class="step-num">1</span><div class="step-copy"><p class="step-title">Buy it</p><p>You get a link straight away.</p></div></li>
        <li class="step"><span class="step-num">2</span><div class="step-copy"><p class="step-title">Open the link on your phone</p><p>Safari on iPhone, Chrome on Android.</p></div></li>
        <li class="step"><span class="step-num">3</span><div class="step-copy"><p class="step-title">Add to Home Screen</p><p>From the share menu. Now it's an icon like any other app.</p></div></li>
        <li class="step"><span class="step-num">4</span><div class="step-copy"><p class="step-title">Use it offline, forever</p><p>No signal needed, no account, no subscription.</p></div></li>
      </ol>
    </div>
  </section>

  <section class="pf-sec pf-sec-alt" aria-labelledby="buy-h">
    <div class="wrap pf-buy">
      <h2 class="pf-h2 center" id="buy-h">One price, once</h2>
      <p class="pf-price">{PRICE}<small>One-time. No subscription, ever.</small></p>
      <div class="pf-actions">
        <a class="btn btn-primary btn-lg" href="{BUY}">Buy Pawfolio &mdash; {PRICE}</a>
        <a class="btn btn-ghost btn-lg" href="{DEMO}">Try the demo first</a>
      </div>
      <p class="pf-micro">30-day money-back guarantee &mdash; email cleartrackapps@gmail.com.<br>
        Prefer Etsy? <a href="{ETSY}">Buy it there instead</a> at Etsy's pricing.</p>
    </div>
  </section>

  <section class="pf-sec" aria-labelledby="faq-h">
    <div class="wrap pf-faq">
      <h2 class="pf-h2 center" id="faq-h">Questions people ask first</h2>
      <div class="faq-list" style="margin-top:1.75rem">
{faq_items()}
      </div>
      <p style="text-align:center"><a class="pf-back" href="../">See all five CleartrackApps &rarr;</a></p>
    </div>
  </section>

</main>

<footer class="site-foot">
  <div class="wrap foot-inner">
    <div class="foot-brand">
      <div>
        <p class="foot-name">CleartrackApps</p>
        <p class="foot-note">Simple offline apps &mdash; no app store, no subscription. Granbury, Texas.</p>
      </div>
    </div>
    <nav class="foot-links" aria-label="Elsewhere">
      <a href="https://instagram.com/cleartrackapps" target="_blank" rel="noopener noreferrer">Instagram</a>
      <a href="https://www.pinterest.com/cleartrackapps" target="_blank" rel="noopener noreferrer">Pinterest</a>
      <a href="https://cleartrackapps.com/go/etsy-shop/" target="_blank" rel="noopener noreferrer">Full Etsy shop</a>
      <a href="mailto:cleartrackapps@gmail.com">cleartrackapps@gmail.com</a>
    </nav>
    <p class="foot-fine">&copy; 2026 CleartrackApps. Pawfolio&trade; is a trademark of CleartrackApps.</p>
  </div>
</footer>

<script src="../app.js" defer></script>
{CF_BEACON}
</body>
</html>
'''

OUT_DIR.mkdir(exist_ok=True)
(OUT_DIR / "index.html").write_text(PAGE, encoding="utf-8")
print(f"wrote {OUT_DIR / 'index.html'} ({len(PAGE)} bytes)")
