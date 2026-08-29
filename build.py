#!/usr/bin/env python3
"""Generates index.html plus the /go/ click-tracking redirect pages for the
CleartrackApps storefront. Static output, no runtime deps."""
import pathlib, html

ROOT = pathlib.Path(__file__).parent
OUT = ROOT / "index.html"
GO_DIR = ROOT / "go"

CF_BEACON = (
    '<!-- Cloudflare Web Analytics: privacy-first, no cookies, no consent banner needed -->\n'
    '<script defer id="cf-beacon" src="https://static.cloudflareinsights.com/beacon.min.js" '
    'data-cf-beacon=\'{"token": "5673e14274004df9a11f87d759a6b624"}\'></script>'
)

# --- Outbound click tracking -------------------------------------------------
# Every store link on the site points at /go/<slug>/ instead of straight at
# Etsy or Gumroad. Those tiny pages load the Cloudflare beacon, then forward the
# visitor on. Cloudflare has no event tracking, so this is what turns a buy-button
# click into something countable: each slug shows up as its own row under
# "Top pages" in the Cloudflare Web Analytics dashboard.
# To change where a button goes, edit the destination here and re-run build.py.
#
# The three Gumroad links carry ?wanted=true. Without it, a buy button drops the
# shopper on the Gumroad product page — a second listing that pitches the app all
# over again in Gumroad's layout, after they already read the pitch here. With
# it, Gumroad skips that page and opens the payment form directly, so the only
# thing they see is a checkout. See https://gumroad.com/help/article/270
#
# Gumroad's overlay widget (gumroad.js) was tried instead and rejected: reading
# its current bundle, an href containing wanted=true takes the plain-navigation
# branch and the overlay never fires, and dropping wanted=true to get the
# overlay renders the full Gumroad product page inside the modal — the same
# duplicate listing, just in an iframe. It also injects markup into the buttons
# and costs a third-party script on every pageview. The plain link below does
# more with less.
GO_LINKS = {
    "pawfolio":                 ("secure checkout", "https://cleartrackapps.gumroad.com/l/Pawfolio?wanted=true&ref=site"),
    "pawfolio-etsy":            ("Etsy",    "https://www.etsy.com/listing/4487742972"),
    "medical-records":          ("secure checkout", "https://cleartrackapps.gumroad.com/l/MedRecords?wanted=true&ref=site"),
    "medical-records-etsy":     ("Etsy",    "https://www.etsy.com/listing/4487743018"),
    "budget-tracker":           ("Etsy",    "https://www.etsy.com/listing/4489254039"),
    "puzzle-pig":               ("secure checkout", "https://cleartrackapps.gumroad.com/l/puzzlepig?wanted=true&ref=site"),
    "puzzle-pig-etsy":          ("Etsy",    "https://www.etsy.com/listing/4490566794"),
    "cosmetic-surgery-planner": ("Etsy",    "https://www.etsy.com/listing/4487732067"),
    "etsy-shop":                ("Etsy",    "https://cleartrackapps.etsy.com"),
    # Not a store link. This one is for the Instagram bio, so reel traffic lands on
    # the try-it-yourself demo instead of the storefront, and shows up as its own
    # row in Cloudflare separately from people who arrive via /pawfolio/.
    "pawfolio-demo":            ("the Pawfolio demo", "https://cleartrackapps.com/pet-care-planner-demo/?ref=reel"),
}


def go(slug):
    """Tracked link for a store destination."""
    assert slug in GO_LINKS, f"unknown go slug: {slug}"
    return f"https://cleartrackapps.com/go/{slug}/"

ICONS = {
    # each 24x24, stroke currentColor
    "pawfolio": '<circle cx="7" cy="8" r="2"/><circle cx="12" cy="6" r="2"/><circle cx="17" cy="8" r="2"/><path d="M12 11c-3 0-5.5 2.4-5.5 5 0 1.7 1.4 2.6 3 2.2 1.7-.4 3.3-.4 5 0 1.6.4 3-.5 3-2.2 0-2.6-2.5-5-5.5-5Z"/>',
    "medical": '<path d="M8 4.5H6.5A1.5 1.5 0 0 0 5 6v13a1.5 1.5 0 0 0 1.5 1.5h11A1.5 1.5 0 0 0 19 19V6a1.5 1.5 0 0 0-1.5-1.5H16"/><rect x="8" y="2.8" width="8" height="3.4" rx="1.2"/><path d="M12 10.5v5M9.5 13h5"/>',
    "budget": '<path d="M4 18V7M9 18v-6M14 18v-9M19 18V5"/><path d="M3 21h18"/>',
    "puzzlepig": '<path d="M4 13a6 6 0 0 1 6-6h4l3-2v3a6 6 0 0 1 2 4.5c0 3.6-3.4 6.5-7.5 6.5S4 16.6 4 13Z"/><circle cx="9" cy="12" r="1"/><path d="M7 19v2M15 19v2"/>',
    "beauty": '<path d="M12 3.5c2.5 3 4.5 5.2 4.5 8a4.5 4.5 0 0 1-9 0c0-2.8 2-5 4.5-8Z"/><path d="M12 21v-3.5"/>',
}

APPS = [
    dict(
        slug="pawfolio", key="pawfolio", name="Pawfolio",
        who="For pet owners who want every vet detail in one place.",
        blurb="Pawfolio keeps your pet's whole life on your phone \u2014 vet visits, medications, vaccine dates, weight, and receipts. Add as many pets as you like, from one dog to a full household of animals. When you travel, hand the sitter a printable sheet with tap-to-call vet numbers instead of a rushed text thread.",
        features=[
            "Vet visits, medications &amp; supplements, and vaccination due dates",
            "Weight tracking and expense history for each pet",
            "Document vault for records, receipts, and adoption papers",
            "Shareable, printable pet-sitter sheet with tap-to-call vet numbers",
            "Unlimited pets, each with its own profile",
        ],
        price="$14.99", audience="Pet owners",
        primary=("Buy now \u2014 $14.99", go("pawfolio")),
        secondary=("Prefer Etsy? Buy there instead", go("pawfolio-etsy")),
        demo="https://cleartrackapps.com/pet-care-planner-demo/",
        # Optional: a dedicated single-product page. When set, the card heading
        # links to it and a text link appears under the buttons. Without this,
        # /pawfolio/ is an orphan page — nothing on the site points at it, so
        # search engines never find it and homepage visitors can't reach it.
        # The other four apps simply omit the field until they have pages too.
        page="./pawfolio/",
        page_label="See the full Pawfolio page",
        tag="Pet care",
    ),
    dict(
        slug="medical-records", key="medical", name="Medical Records Keeper",
        who="For families and caregivers juggling more than one person's health.",
        blurb="Most apps that do this bill you every year, forever \u2014 and most of them show ads. This one is $24.99 once, with no ads and no renewals. It keeps what a doctor's office asks for in one private place on your phone: medications and doses, appointment notes, vitals, and pharmacy details. Track up to six family members, each with their own records, and print a clean summary for the next visit.",
        features=[
            "Doctors, pharmacies, and emergency contacts in one list",
            "Medications with doses plus phone reminders",
            "Appointments with visit notes you write afterwards",
            "Vitals history \u2014 blood pressure, weight, glucose, and more",
            "Up to 6 family members, with printable records for any visit",
        ],
        # Cost comparison. The point of this block is that a one-time price beats a
        # renewing one, so it names no competitor: naming them teaches a shopper the
        # name of a free-with-ads alternative, and any specific price we print goes
        # stale the moment they change it. A dated range says the same thing and
        # survives. Range spans the yearly plans verified 2026-08-14 across Dosecast
        # ($27.99), Capzule PHR ($29.99), Medisafe and CareClinic ($39.99), and
        # EveryDose ($59.99, $69.99 for Plus) \u2014 every one a subscription, most
        # carrying ads. Re-check before editing the numbers.
        compare=dict(
            head="Pay once, not every year",
            them=("Similar apps", "$30\u2013$70 every year"),
            us=("This app", "$24.99 once"),
            note="Typical yearly plans for comparable medication and health-record apps, checked August 2026. Most of them show ads. This one has none, and you never need a renewal.",
        ),
        price="$24.99", audience="Families &amp; caregivers",
        primary=("Buy now \u2014 $24.99", go("medical-records")),
        secondary=("Prefer Etsy? Buy there instead", go("medical-records-etsy")),
        demo="https://cleartrackapps.com/medical-records-demo/",
        tag="Family health",
    ),
    dict(
        slug="budget-tracker", key="budget", name="Budget Tracker",
        who="For anyone who wants a budget that stays on their own phone.",
        blurb="A full personal budget without a bank login or a monthly fee. Log income, bills, and spending by category, then watch savings goals and debt payoff move month to month. Already have statements? Import a CSV or OFX file from your bank instead of typing everything in.",
        features=[
            "Income, bills, and spending organised by category",
            "Savings goals and a debt payoff plan",
            "Net worth view and monthly reports",
            "Bank statement import (CSV / OFX)",
            "Bill tracker so nothing slips past a due date",
        ],
        price="$29.99", audience="Anyone budgeting",
        primary=("Buy on Etsy \u2014 $29.99", go("budget-tracker")),
        secondary=None,
        demo="https://cleartrackapps.com/budget-tracker-demo/",
        tag="Money",
    ),
    dict(
        slug="puzzle-pig", key="puzzlepig", name="Puzzle Pig",
        who="For parents teaching kids to earn, save, and give.",
        blurb="Kids do chores, earn money, and split it between Save, Spend, and Give jars. The thing they're saving for sits behind a hidden photo that reveals itself piece by piece as the jar fills, which is what keeps them checking in. Parents get a PIN-protected dashboard, and phones can sync between parent and child.",
        features=[
            "Chore chart kids can tick off themselves",
            "Save / Spend / Give jars for every payout",
            "Goal photo that reveals itself as savings grow",
            "PIN-protected parent dashboard",
            "Parent and child phone sync",
        ],
        price="$14.99", audience="Parents of kids",
        primary=("Buy now \u2014 $14.99", go("puzzle-pig")),
        secondary=("Prefer Etsy? Buy there instead", go("puzzle-pig-etsy")),
        demo="https://cleartrackapps.com/puzzle-pig-demo/",
        tag="Kids &amp; chores",
    ),
    dict(
        slug="cosmetic-surgery-planner", key="beauty", name="Cosmetic Surgery Planner",
        who="For anyone planning a procedure and saving up for it.",
        blurb="Plan the whole thing before you book: estimate the real cost, compare physicians, and save toward the total week by week. Twelve sections cover deposits, payments, travel, recovery notes, and a private photo log. It stays on your phone, so nothing about it lives in someone else's account.",
        features=[
            "Cost estimator covering surgeon, facility, and extras",
            "Savings tracker with weekly streaks",
            "Physician selection notes and comparisons",
            "Travel and recovery planning",
            "Receipts and a private photo log across 12 sections",
        ],
        price="$36.99", audience="Planning a procedure",
        primary=("Buy on Etsy \u2014 $36.99", go("cosmetic-surgery-planner")),
        secondary=None,
        demo="https://cleartrackapps.com/beauty-planner-demo/",
        tag="Planning",
    ),
]

FAQ = [
    ("Is this an app from the App Store or Google Play?",
     "No \u2014 and that's on purpose. You get a link (or a file) that opens in your phone's browser. Tap <strong>Add to Home Screen</strong> and it sits next to your other apps with its own icon, opens full screen, and works with no signal."),
    ("Do I need to create an account or sign in?",
     "No account, no password, no email verification. Open it and start using it."),
    ("Does my data leave my device?",
     "No. Everything you type stays on the device you typed it on. There is no server to send it to, no cloud sync, and no analytics collecting what you enter. That's why these apps work on a plane or in a basement with no signal."),
    ("Does it work on iPhone and Android?",
     "Yes \u2014 both, plus tablets and computers. Anything with a modern browser (Safari, Chrome, Edge, Firefox) works."),
    ("Is there a subscription?",
     "Never. You pay once and it's yours to keep. No renewals, no upgrade nags, no price creep. "
     "Apps that do similar jobs are usually subscriptions running roughly $30\u2013$70 a year \u2014 "
     "every year, for as long as you use them."),
    ("What if I buy it and it isn't right for me?",
     'Email <a href="mailto:cleartrackapps@gmail.com">cleartrackapps@gmail.com</a> within 30 days and you get your money back in full. No forms, no questions, no explanation needed. You can also try any app free before you buy \u2014 every one has a full demo with no email required.'),
    ("Can I get help if I get stuck?",
     'Yes. Email <a href="mailto:cleartrackapps@gmail.com">cleartrackapps@gmail.com</a> and Shauna will help you get set up. Every purchase also includes a short getting-started guide.'),
]

STEPS = [
    ("1", "Buy it", "Tap a buy button and you go straight to a checkout \u2014 no second product page to read. Your download link arrives right away, no waiting on shipping."),
    ("2", "Open the link on your phone", "Tap the file or link and the app opens in your phone's browser. Nothing to install, nothing to sign up for."),
    ("3", "Add to Home Screen", "Use your browser's share menu, then <strong>Add to Home Screen</strong>. Now it has its own icon and opens full screen, exactly like a normal app."),
    ("4", "Use it offline, forever", "Your data is saved on the device. No signal needed, no account, no monthly fee \u2014 it just keeps working."),
]

# Shauna's own logo, processed by make_logo.py into a transparent PNG plus a
# light-wordmark variant for the dark theme. Both are shipped; CSS shows one.
# Shauna's own logo, processed by make_logo.py into a transparent PNG plus a
# light-wordmark variant for the dark theme. Both are shipped; CSS shows one.
def logo(cls):
    return (f'<span class="lockup {cls}">'
            f'<img class="logo logo-on-light" src="./assets/logo.png" width="720" height="289" '
            f'alt="Cleartrack Apps" decoding="async">'
            f'<img class="logo logo-on-dark" src="./assets/logo-dark.png" width="720" height="289" '
            f'alt="" aria-hidden="true" decoding="async">'
            f'</span>')


LOGO = logo('logo-head')
LOGO_FOOT = logo('logo-foot')


def icon(key):
    return (f'<svg class="app-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" '
            f'focusable="false">{ICONS[key]}</svg>')


def cost_compare(c):
    """Optional two-row cost comparison. Only rendered for apps that define one."""
    if not c:
        return ""
    them_l, them_v = c["them"]
    us_l, us_v = c["us"]
    return f'''
      <div class="cost-compare">
        <p class="cc-head">{c['head']}</p>
        <ul class="cc-rows">
          <li><span class="cc-label">{them_l}</span> <span class="cc-val">{them_v}</span></li>
          <li class="cc-us"><span class="cc-label">{us_l}</span> <span class="cc-val">{us_v}</span></li>
        </ul>
        <p class="cc-note">{c['note']}</p>
      </div>'''


def card(a, i):
    feats = "\n".join(f"        <li>{f}</li>" for f in a["features"])
    # A dedicated page gets two links: the heading (a linked heading is a strong
    # signal to search engines about what that page covers) and a quiet text
    # link under the buttons. Deliberately not a fourth button — three already
    # ask a lot of one card, and a fourth would compete with Buy.
    page = a.get("page")
    title = a["name"] if not page else f'<a href="{page}">{a["name"]}</a>'
    more = "" if not page else (
        f'\n      <p class="card-alt"><a href="{page}">{a["page_label"]} &rarr;</a></p>')
    sec = ""
    if a["secondary"]:
        label, url = a["secondary"]
        sec = (f'\n      <p class="card-alt"><a href="{url}" target="_blank" rel="noopener noreferrer">'
               f'{label}<span class="sr-only"> ({a["name"]} on Etsy)</span></a></p>')
    plabel, purl = a["primary"]
    return f'''    <article class="card" id="{a['slug']}" style="--accent: var(--accent-{a['key']}); --accent-soft: var(--accent-{a['key']}-soft);">
      <header class="card-head">
        <span class="card-icon">{icon(a['key'])}</span>
        <div>
          <h3 class="card-title">{title}</h3>
          <p class="card-tag">{a['tag']}</p>
        </div>
      </header>
      <p class="card-who">{a['who']}</p>
      <p class="card-blurb">{a['blurb']}</p>
      <ul class="card-features">
{feats}
      </ul>{cost_compare(a.get("compare"))}
      <p class="card-price"><span class="price">{a['price']}</span> <span class="price-note">one-time</span></p>
      <div class="card-actions">
        <a class="btn btn-primary" href="{purl}" target="_blank" rel="noopener noreferrer">{plabel}</a>
        <a class="btn btn-ghost" href="{a['demo']}" target="_blank" rel="noopener noreferrer">Try the free demo</a>
      </div>{more}{sec}
    </article>'''


def table_row(a):
    return f'''        <tr>
          <th scope="row"><span class="t-dot" style="background: var(--accent-{a['key']})" aria-hidden="true"></span><a href="#{a['slug']}">{a['name']}</a></th>
          <td data-label="Who it's for">{a['audience']}</td>
          <td class="t-price" data-label="Price">{a['price']}</td>
          <td data-label="Try it"><a class="t-demo" href="{a['demo']}" target="_blank" rel="noopener noreferrer">Demo<span class="sr-only"> for {a['name']}</span> &rarr;</a></td>
        </tr>'''


cards = "\n\n".join(card(a, i) for i, a in enumerate(APPS))
rows = "\n".join(table_row(a) for a in APPS)
steps = "\n".join(
    f'''      <li class="step">
        <span class="step-num" aria-hidden="true">{n}</span>
        <h3 class="step-title">{t}</h3>
        <p class="step-copy">{c}</p>
      </li>''' for n, t, c in STEPS)
faq = "\n".join(
    f'''      <details class="faq-item"{' open' if i == 0 else ''}>
        <summary><span>{q}</span><svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg></summary>
        <p>{a}</p>
      </details>''' for i, (q, a) in enumerate(FAQ))

# QR tiles: a desktop visitor points their phone camera at a code and the demo
# opens on the phone, where the app actually lives. Hidden on narrow screens --
# you cannot scan the screen you are holding, and phone visitors already have a
# "Try the demo" button on every card.
qr_tiles = "\n".join(
    f'''        <li class="qr-tile">
          <img class="qr-img" src="./assets/qr-{a['slug']}.png" width="148" height="148" loading="lazy"
               alt="QR code that opens the {html.unescape(a['name'])} demo">
          <p class="qr-name">{a['name']}</p>
          <a class="qr-link" href="{a['demo']}">Open the demo</a>
        </li>''' for a in APPS)

DESC = ("Simple, private life-admin apps for your phone from CleartrackApps \u2014 pet records, family medical "
        "records, budgeting, kids' chores and savings, and procedure planning. Work offline, no app store, "
        "no accounts, no subscription. Pay once.")

HTML = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>CleartrackApps \u2014 Simple offline apps for real life admin</title>
<meta name="description" content="{DESC}">
<meta name="theme-color" content="#faf6ef" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#181410" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="CleartrackApps">
<link rel="canonical" href="https://cleartrackapps.com/">
<meta property="og:url" content="https://cleartrackapps.com/">
<meta property="og:title" content="CleartrackApps \u2014 Simple offline apps for real life admin">
<meta property="og:description" content="{DESC}">
<meta property="og:image" content="https://cleartrackapps.com/assets/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="CleartrackApps \u2014 five simple offline apps for pets, health, money, kids and planning.">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="CleartrackApps \u2014 Simple offline apps for real life admin">
<meta name="twitter:description" content="{DESC}">
<meta name="twitter:image" content="https://cleartrackapps.com/assets/og-image.png">
<link rel="icon" href="./assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="./assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="./assets/favicon-180.png" sizes="180x180">
<link rel="preconnect" href="https://api.fontshare.com" crossorigin>
<link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=general-sans@400,500,600&f[]=zodiak@600,700&display=swap">
<link rel="stylesheet" href="./base.css">
<link rel="stylesheet" href="./style.css">
</head>
<body>
<a class="skip" href="#apps">Skip to the apps</a>

<header class="site-head">
  <div class="wrap head-inner">
    <a class="brand" href="#top" aria-label="Cleartrack Apps home">
      {LOGO}
    </a>
    <button class="theme-toggle" type="button" id="theme-toggle" aria-label="Switch colour theme">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" aria-hidden="true">
        <circle class="t-sun" cx="12" cy="12" r="4.2"/>
        <g class="t-rays"><path d="M12 2.6v2.2M12 19.2v2.2M2.6 12h2.2M19.2 12h2.2M5.4 5.4l1.6 1.6M17 17l1.6 1.6M18.6 5.4L17 7M7 17l-1.6 1.6"/></g>
        <path class="t-moon" d="M20 13.4A8 8 0 1 1 10.6 4a6.4 6.4 0 0 0 9.4 9.4Z"/>
      </svg>
    </button>
  </div>
</header>

<main id="top">

  <section class="hero">
    <div class="wrap hero-inner">
      <p class="eyebrow">Made in Granbury, Texas by Shauna</p>
      <h1>Small apps that quietly keep your life in order &mdash; right on your phone.</h1>
      <p class="lede">Five simple planners for pets, family health, money, kids, and big-ticket plans. They work offline, live on your home screen, and keep your information on your device. <strong>No app store, no account, no subscription \u2014 pay once.</strong></p>
      <div class="hero-actions">
        <a class="btn btn-primary btn-lg" href="#apps">See the 5 apps</a>
        <a class="btn btn-ghost btn-lg" href="#how">How it works</a>
      </div>
      <ul class="promises">
        <li>Works offline</li>
        <li>No accounts</li>
        <li>Your data stays on your device</li>
        <li>One-time price</li>
        <li>30-day money-back guarantee</li>
      </ul>
    </div>
  </section>

  <section class="how" id="how" aria-labelledby="how-h">
    <div class="wrap">
      <h2 id="how-h" class="sec-title">How a download becomes an app on your phone</h2>
      <p class="sec-sub">It sounds too simple, so here it is, start to finish. Four steps, about two minutes.</p>
      <ol class="steps">
{steps}
      </ol>
    </div>
  </section>

  <section class="apps" id="apps" aria-labelledby="apps-h">
    <div class="wrap">
      <h2 id="apps-h" class="sec-title">The five apps</h2>
      <p class="sec-sub">Each one does a single job well. Try any demo free before you buy \u2014 no email required \u2014 and every purchase is covered by a 30-day money-back guarantee.</p>
      <div class="card-grid">

{cards}

      </div>
    </div>
  </section>

  <section class="scan" id="scan" aria-labelledby="scan-h">
    <div class="wrap">
      <h2 id="scan-h" class="sec-title">Try one on your phone right now</h2>
      <p class="sec-sub">Point your phone camera at a code. The free demo opens in your phone's browser \u2014 nothing to install, no signup.</p>
      <ul class="qr-grid">
{qr_tiles}
      </ul>
    </div>
  </section>

  <section class="compare" id="compare" aria-labelledby="compare-h">
    <div class="wrap">
      <h2 id="compare-h" class="sec-title">Not sure which one?</h2>
      <p class="sec-sub">A quick side-by-side of all five.</p>
      <div class="table-scroll">
        <table class="ctable">
          <caption class="sr-only">All five CleartrackApps apps, who each is for, the one-time price, and a link to the free demo.</caption>
          <thead>
            <tr><th scope="col">App</th><th scope="col">Who it's for</th><th scope="col">Price</th><th scope="col">Try it</th></tr>
          </thead>
          <tbody>
{rows}
          </tbody>
        </table>
      </div>
      <p class="table-note">Prices are one-time, and every app is covered by a 30-day money-back guarantee. Pawfolio, Medical Records Keeper, and Puzzle Pig are also available on Etsy at Etsy's own pricing.</p>
    </div>
  </section>

  <section class="faq" id="faq" aria-labelledby="faq-h">
    <div class="wrap faq-wrap">
      <h2 id="faq-h" class="sec-title">Questions people ask first</h2>
      <div class="faq-list">
{faq}
      </div>
    </div>
  </section>

</main>

<footer class="site-foot">
  <div class="wrap foot-inner">
    <div class="foot-brand">
      {LOGO_FOOT}
      <div>
        <p class="foot-name">CleartrackApps</p>
        <p class="foot-note">Simple offline apps \u2014 no app store, no subscription. Granbury, Texas.</p>
      </div>
    </div>
    <nav class="foot-links" aria-label="Elsewhere">
      <a href="https://instagram.com/cleartrackapps" target="_blank" rel="noopener noreferrer">Instagram</a>
      <a href="https://www.pinterest.com/cleartrackapps" target="_blank" rel="noopener noreferrer">Pinterest</a>
      <a href="https://cleartrackapps.com/go/etsy-shop/" target="_blank" rel="noopener noreferrer">Full Etsy shop</a>
      <a href="mailto:cleartrackapps@gmail.com">cleartrackapps@gmail.com</a>
    </nav>
    <p class="foot-fine">&copy; 2026 CleartrackApps. Pawfolio&trade; and Puzzle Pig&trade; are trademarks of CleartrackApps.</p>
  </div>
</footer>

<script src="./app.js" defer></script>
<!-- Cloudflare Web Analytics: privacy-first, no cookies, no consent banner needed -->
<script defer src="https://static.cloudflareinsights.com/beacon.min.js" data-cf-beacon='{{"token": "5673e14274004df9a11f87d759a6b624"}}'></script>
</body>
</html>
'''

OUT.write_text(HTML, encoding="utf-8")
print(f"wrote {OUT} ({len(HTML)} bytes)")


# --- /go/ click-tracking redirect pages --------------------------------------
# Each page: loads the Cloudflare beacon, waits for it to actually report, then
# replaces itself with the store URL (no back-button trap). A meta refresh and a
# plain link cover no-JS and slow-network cases.
#
# The redirect is chained off the beacon's own load event rather than a blind
# timeout. A fixed short delay races the beacon: fire too early and the click is
# never counted, which is the one thing these pages exist to do. Waiting on load
# (then 350ms to let it send) means a counted click is the normal path, an
# error listener covers a blocked beacon, and a 2.2s safety net means nobody is
# ever stranded here.
GO_TEMPLATE = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow">
<title>Opening {store}\u2026 \u2014 CleartrackApps</title>
<link rel="canonical" href="{dest}">
<meta http-equiv="refresh" content="3; url={dest}">
<style>
  :root {{ color-scheme: light dark; }}
  body {{ margin:0; min-height:100vh; display:grid; place-items:center;
         font:500 16px/1.5 -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif;
         background:#faf9f7; color:#484854; text-align:center; padding:24px; }}
  .wrap {{ max-width:22rem; }}
  .mark {{ font-weight:700; letter-spacing:-.01em; font-size:1.1rem; margin:0 0 1.25rem; }}
  .mark b {{ color:#F06C24; font-weight:700; }}
  .spin {{ width:30px; height:30px; margin:0 auto 1rem; border-radius:50%;
          border:3px solid rgba(72,72,84,.18); border-top-color:#F06C24;
          animation:sp .7s linear infinite; }}
  @keyframes sp {{ to {{ transform:rotate(360deg); }} }}
  p {{ margin:.4rem 0; }}
  .fine {{ font-size:.85rem; opacity:.65; }}
  a {{ color:#F06C24; }}
  @media (prefers-color-scheme: dark) {{
    body {{ background:#17171c; color:#e7e6ea; }}
  }}
  @media (prefers-reduced-motion: reduce) {{ .spin {{ animation:none; }} }}
</style>
</head>
<body>
  <div class="wrap">
    <p class="mark">cleartrack<b>apps</b></p>
    <div class="spin" aria-hidden="true"></div>
    <p role="status">Taking you to {store}\u2026</p>
    <p class="fine">Not moving? <a href="{dest}">Continue to {store}</a></p>
  </div>
{beacon}
<script>
  (function () {{
    var target = {dest_js};
    var sent = false;
    function go() {{ if (sent) return; sent = true; window.location.replace(target); }}
    var beacon = document.getElementById("cf-beacon");
    if (beacon) {{
      // Redirect once the analytics beacon has loaded and had a moment to report.
      beacon.addEventListener("load", function () {{ setTimeout(go, 350); }});
      // If the beacon is blocked or fails, don't make the buyer wait.
      beacon.addEventListener("error", go);
    }}
    // Safety net so nobody is ever stranded on this page.
    setTimeout(go, 2200);
  }})();
</script>
</body>
</html>
'''

import json as _json

GO_DIR.mkdir(exist_ok=True)
for slug, (store, dest) in GO_LINKS.items():
    page = GO_TEMPLATE.format(
        store=html.escape(store),
        dest=html.escape(dest, quote=True),
        dest_js=_json.dumps(dest),
        beacon=CF_BEACON,
    )
    d = GO_DIR / slug
    d.mkdir(exist_ok=True)
    (d / "index.html").write_text(page, encoding="utf-8")
print(f"wrote {len(GO_LINKS)} redirect pages under {GO_DIR}")
