#!/usr/bin/env python3
"""Generates /pet-sitter-intake-form/index.html: a free new-client intake form
for pet sitters.

Two ways in:
  * A sitter opens the plain page, types their business name, phone and email
    once, and gets a personal link (…/pet-sitter-intake-form/?b=Name&p=Phone&e=Email).
  * A client opens that link. The sitter's business name is at the top of the
    form. They fill it in, add pet photos, and print it or save it as a PDF to
    send back.

Like the owner sheet at /pet-sitter-instructions/, what anyone types stays in
that browser's local storage. The link itself holds only the sitter's business
name and contact info.

Send to a sitter: a link made by Pawfolio's Sitter mode also carries
#s=<inboxId>.<publicKey> in the fragment (never sent to any server). Then the
form shows "Send to <Business>": the answers are encrypted on the client's phone
with intake-crypto.js (shared with Pawfolio, copied verbatim) and only that
encrypted envelope is uploaded. Without #s= the page is print / PDF only.

Re-run after build.py; it writes only into ./pet-sitter-intake-form/.
The blank fillable PDF comes from make_intake_pdf.py.
"""
import pathlib

ROOT = pathlib.Path(__file__).parent
OUT_DIR = ROOT / "pet-sitter-intake-form"
URL = "https://cleartrackapps.com/pet-sitter-intake-form/"
APP = "https://cleartrackapps.com/go/pawfolio-app/?src=intake-page"
DEMO = "https://cleartrackapps.com/go/pawfolio-demo/?src=intake-page"
PDF = "pet-sitter-intake-form-blank.pdf"

CF_BEACON = (
    '<!-- Cloudflare Web Analytics: privacy-first, no cookies, no consent banner needed -->\n'
    '<script defer src="https://static.cloudflareinsights.com/beacon.min.js" '
    'data-cf-beacon=\'{"token": "5673e14274004df9a11f87d759a6b624"}\'></script>'
)

TITLE = "Free Pet Sitter Client Intake Form, With Your Business Name | Pawfolio"
DESC = ("A free new-client intake form for pet sitters. Get a link with your business name "
        "at the top, and clients fill it in on their phone, add pet photos, and send it back. "
        "Vet, home access, emergency authorization and medications. Blank PDF too.")

COVERS = [
    ("Client and emergency contacts", "Phones, email, address, and someone nearby who has a key."),
    ("Both vets", "The regular vet and the 24-hour emergency vet, with phone numbers and addresses."),
    ("Getting in", "Key, lockbox or door code, alarm code, Wi-Fi, parking, and where supplies are kept."),
    ("Emergency care authorization", "The client approves a dollar amount for urgent care if they can't be reached, and signs."),
    ("Each pet, with a photo", "Breed, age, weight, markings and microchip number, so you can describe a pet that slips out."),
    ("Medications", "Name, dose, times and how each one is given, plus allergies and health conditions."),
    ("Behavior and routines", "Strangers, other pets, escape risk, fears, walks and feeding."),
]

FAQ = [
    ("Is this really free?",
     "Yes. No signup, no account and no email for you or your clients."),
    ("How do I give clients my link?",
     "Make your link above, then text it, email it, add it to your booking confirmation or put it in your "
     "Instagram bio. Every client who opens it sees your business name at the top of the form."),
    ("Do my clients' answers come to me automatically?",
     "Not with a link made on this page. Nothing is sent anywhere, which keeps door codes and alarm codes "
     "private. When your client is done, they tap Print or save as PDF and text or email the PDF to you. "
     "If you'd rather get forms in an app, turn on Sitter mode in Pawfolio. It's free, and its link adds a "
     "Send button. The form is encrypted on your client's phone, and only your phone can open it."),
    ("Can clients add photos of their pets?",
     "Yes. Each pet has an Add photo circle. The photo stays on the client's phone with the rest of the form "
     "and prints in that pet's section."),
    ("What if a client would rather write it by hand?",
     "Download the blank PDF. You can type your business name into it once, then print copies or send the file."),
    ("How do clients save it as a PDF on an iPhone?",
     "Tap Print or save as PDF, then tap the Share button at the top of the print screen and choose Save to "
     "Files, or send it straight to you in Messages or Mail."),
]


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def field(fid, label, ph="", area=False, rows=2, lines=1, cls="", typ="text"):
    if area:
        ctl = f'<textarea id="{fid}" data-k="{fid}" data-lines="{lines}" rows="{rows}" placeholder="{esc(ph)}"></textarea>'
    else:
        ctl = f'<input id="{fid}" data-k="{fid}" type="{typ}" placeholder="{esc(ph)}" autocomplete="off">'
    c = f' class="sf {cls}"' if cls else ' class="sf"'
    return f'<label{c}><span>{label}</span>{ctl}</label>'


def med_rows(p):
    out = []
    for i in range(1, 4):
        out.append(f'''          <div class="med-row">
            {field(f"{p}-med{i}-name", "Medication or supplement", "e.g., Apoquel" if i == 1 else "", cls="m-name")}
            {field(f"{p}-med{i}-dose", "Dose", "16 mg, 1 tablet" if i == 1 else "", cls="m-dose")}
            {field(f"{p}-med{i}-time", "Time(s)", "7 a.m." if i == 1 else "", cls="m-time")}
            {field(f"{p}-med{i}-how", "How it's given", "Hidden in cheese, with breakfast" if i == 1 else "", cls="m-how")}
          </div>''')
    return "\n".join(out)


def pet_block(n):
    p = f"pet{n}"
    return f'''
      <section class="sheet-pet" data-pet="{n}"{' hidden' if n > 1 else ''}>
        <h3>Pet {n}</h3>
        <div class="pet-id">
          <div class="pet-photo" data-photo="{p}-photo">
            <label class="pet-photo-btn" for="{p}-photo-in"><img alt="" hidden><span class="ps-hide-print">Add photo</span><span class="print-only">Photo</span></label>
            <input type="file" id="{p}-photo-in" accept="image/*" class="ps-hide-print">
            <button type="button" class="linkbtn pet-photo-rm ps-hide-print" hidden>Remove</button>
          </div>
          <div class="pet-id-fields">
            {field(p+"-name", "Name", "e.g., Bella")}
            {field(p+"-kind", "Species and breed", "e.g., Dog, yellow Lab")}
            {field(p+"-age", "Age", "e.g., 4 years")}
            {field(p+"-weight", "Weight", "e.g., 70 lb")}
            {field(p+"-sex", "Sex / spayed or neutered", "e.g., Female, spayed")}
            {field(p+"-chip", "Microchip number", "e.g., 985 112 004 567 890")}
            <div class="pet-desc">{field(p+"-desc", "Color and markings", "e.g., Pale yellow, white patch on chest")}</div>
          </div>
        </div>
        <div class="sg">
          {field(p+"-food", "Feeding (food, amount, times)", "e.g., 1 cup dry food at 7 a.m. and 5 p.m.", area=True)}
          {field(p+"-treats", "Treats allowed?", "e.g., Yes, 2 a day. No rawhide.", area=True)}
        </div>
        <p class="sf-group">Medications and supplements</p>
        <div class="meds">
{med_rows(p)}
        </div>
        <div class="sg">
          {field(p+"-health", "Allergies or health conditions", "e.g., Chicken allergy, arthritis", area=True, lines=2)}
          {field(p+"-walk", "Walks and exercise", "e.g., 20 minutes, morning and evening", area=True, lines=2)}
          {field(p+"-behave", "Behavior (strangers, other pets, escape risk, fears)", "e.g., Friendly, but slips out the front door", area=True, lines=2)}
          {field(p+"-notes", "Other notes and routines", "e.g., Hides under the bed during storms", area=True, lines=2)}
        </div>
      </section>'''


def covers():
    return "\n".join(f'        <li><strong>{t}.</strong> {d}</li>' for t, d in COVERS)


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
<meta name="theme-color" content="#f5f6f5" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#151917" media="(prefers-color-scheme: dark)">
<link rel="canonical" href="{URL}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="CleartrackApps">
<meta property="og:url" content="{URL}">
<meta property="og:title" content="Free pet sitter client intake form">
<meta property="og:description" content="Send new clients one link. They fill it in, add pet photos, and send it back.">
<meta property="og:image" content="https://cleartrackapps.com/assets/og-pawfolio.png?v=2">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="../assets/favicon.svg" type="image/svg+xml">
<link rel="icon" href="../assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="../assets/favicon-180.png" sizes="180x180">
<link rel="preconnect" href="https://api.fontshare.com" crossorigin>
<link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=general-sans@400,500,600&display=swap">
<link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=zodiak@700&display=swap">
<link rel="stylesheet" href="../base.css?v=20261014g">
<link rel="stylesheet" href="../style.css?v=20261105a">
<style>
  /* Page colors: soft gray with a sage accent (this page only). */
  body.ps-page {{
    --color-bg: #f5f6f5; --color-bg-alt: #ecefed; --color-surface: #ffffff; --color-surface-2: #f7f8f7;
    --color-border: #e1e5e2; --color-border-strong: #cfd5d1; --color-text: #24272b; --color-text-muted: #5d636c;
    --color-primary: #5e7c73; --color-primary-hover: #4f6b63; --color-focus: #5e7c73;
    --accent-pawfolio: #5e7c73; --accent-pawfolio-soft: #e9efec;
    background-color: var(--color-bg);
    background-image: url("paws.svg"); background-repeat: repeat; background-position: center top; background-size: 900px 1100px;
  }}
  [data-theme='dark'] body.ps-page {{
    --color-bg: #151917; --color-bg-alt: #1b201d; --color-surface: #1e2420; --color-surface-2: #232a26;
    --color-border: #333c37; --color-border-strong: #424c46; --color-text: #dde2df; --color-text-muted: #9aa49f;
    --color-primary: #9dbcb2; --color-primary-hover: #b4cfc6; --color-focus: #9dbcb2;
    --accent-pawfolio: #9dbcb2; --accent-pawfolio-soft: #22302c; background-image: url("paws-dark.svg");
  }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme='light']) body.ps-page {{
      --color-bg: #151917; --color-bg-alt: #1b201d; --color-surface: #1e2420; --color-surface-2: #232a26;
      --color-border: #333c37; --color-border-strong: #424c46; --color-text: #dde2df; --color-text-muted: #9aa49f;
      --color-primary: #9dbcb2; --color-primary-hover: #b4cfc6; --color-focus: #9dbcb2;
      --accent-pawfolio: #9dbcb2; --accent-pawfolio-soft: #22302c; background-image: url("paws-dark.svg");
    }}
  }}
  @media (max-width: 640px) {{ body.ps-page {{ background-size: 560px 684px; }} }}
  body.ps-page .site-head {{ background: color-mix(in srgb, var(--color-bg) 92%, transparent); }}
  body.ps-page .ps-alt, body.ps-page .faq {{ background: color-mix(in srgb, var(--color-bg-alt) 45%, transparent); }}
  [hidden] {{ display: none !important; }}
  .ps-hero {{ padding: clamp(1.5rem, 4vw, 2.5rem) 0 1rem; text-align: center; }}
  .ps-eyebrow {{ font-size: .85rem; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; color: var(--accent-pawfolio); margin: 0; }}
  .ps-hero h1 {{ font-family: Zodiak, Georgia, serif; font-weight: 700;
    font-size: clamp(1.85rem, 5.4vw, 3rem); letter-spacing: -.02em; max-width: 20ch; margin: .4rem auto 0; overflow-wrap: anywhere; }}
  .ps-lede {{ max-width: 48ch; margin: .9rem auto 0; font-size: clamp(1rem, 2.2vw, 1.1rem); opacity: .82; }}
  .ps-contact {{ margin: .6rem auto 0; display: flex; flex-wrap: wrap; justify-content: center; gap: .3rem 1.2rem; font-weight: 600; }}
  .ps-contact a {{ color: var(--accent-pawfolio); text-decoration: underline; text-underline-offset: 3px; overflow-wrap: anywhere; }}
  .ps-sec {{ padding: clamp(2rem, 5vw, 3.5rem) 0; }}
  .ps-h2 {{ font-family: Zodiak, Georgia, serif; font-weight: 700; letter-spacing: -.015em;
    font-size: clamp(1.5rem, 4vw, 2.2rem); max-width: 26ch; }}
  .ps-sub {{ max-width: 52ch; margin-top: .6rem; opacity: .78; }}
  .ps-actions {{ display: flex; flex-wrap: wrap; gap: .7rem; justify-content: center; margin-top: 1.4rem; }}
  .ps-note {{ margin-top: .8rem; font-size: .9rem; opacity: .62; text-align: center; }}
  .ps-links {{ margin: 1rem auto 0; display: flex; flex-wrap: wrap; justify-content: center; gap: .4rem 1.2rem; }}
  .ps-links a {{ font-weight: 600; color: var(--accent-pawfolio); text-decoration: underline; text-underline-offset: 3px; }}
  .ps-list {{ max-width: 52ch; margin: 1.2rem 0 0; padding-left: 1.2rem; display: grid; gap: .7rem; }}
  .ps-cta {{ max-width: 40rem; margin: 0 auto; text-align: center; }}
  .linkbtn {{ display: inline-flex; align-items: center; line-height: 1.3; background: none; border: 0; padding: .4rem 0; font: inherit; font-weight: 600;
    color: var(--color-primary); cursor: pointer; text-decoration: underline; text-underline-offset: 3px; }}

  /* Link maker (sitters) */
  .maker {{ max-width: 46rem; margin: 1.2rem auto 0; background: var(--color-surface); border: 1px solid var(--color-border);
    border-radius: var(--radius-lg); padding: clamp(1rem, 4vw, 1.6rem); box-shadow: var(--shadow-sm); }}
  .maker h2 {{ font-family: Zodiak, Georgia, serif; font-weight: 700; font-size: 1.35rem; margin: 0; }}
  .maker > p {{ margin: .35rem 0 1rem; color: var(--color-text-muted); }}
  .maker-out {{ margin-top: .4rem; padding: .9rem 1rem; border-radius: var(--radius); background: var(--accent-pawfolio-soft);
    border: 1px solid color-mix(in srgb, var(--accent-pawfolio) 25%, transparent); }}
  .maker-out p {{ margin: 0; font-size: .85rem; font-weight: 600; color: var(--color-text-muted); }}
  .maker-url {{ display: block; margin: .3rem 0 .7rem; font-size: .95rem; font-weight: 600; color: var(--color-text); overflow-wrap: anywhere; }}
  .maker-btns {{ display: flex; flex-wrap: wrap; gap: .6rem 1.2rem; align-items: center; }}
  .maker-hint {{ margin-top: .8rem; font-size: .85rem; color: var(--color-text-muted); }}
  .maker-hint a {{ font-weight: 600; color: var(--accent-pawfolio); text-decoration: underline; text-underline-offset: 3px; }}

  /* The form */
  .sheet {{ max-width: 46rem; margin: 1.5rem auto 0; background: var(--color-surface);
    border: 1px solid var(--color-border); border-radius: var(--radius-lg); padding: clamp(1rem, 4vw, 2rem); }}
  .sheet-top {{ display: flex; flex-wrap: wrap; justify-content: space-between; align-items: flex-start; gap: .6rem 1.4rem;
    padding-bottom: .9rem; border-bottom: 3px solid var(--accent-pawfolio); }}
  .biz {{ flex: 1 1 16rem; min-width: 0; }}
  #biz-name {{ font-size: 1.35rem; font-weight: 700; }}
  .biz-line {{ display: grid; grid-template-columns: 1fr 1.4fr; gap: 0 1rem; }}
  .biz-show .biz-edit {{ display: none; }}
  .biz-static {{ display: none; }}
  .biz-show .biz-static {{ display: block; }}
  .biz-static .bs-name {{ font-size: 1.35rem; font-weight: 700; margin: 0; overflow-wrap: anywhere; }}
  .biz-static .bs-line {{ margin: .15rem 0 0; color: var(--color-text-muted); font-size: .95rem; overflow-wrap: anywhere; }}
  .sheet-titles {{ text-align: right; flex: 0 0 auto; }}
  .sheet-title {{ font-family: Zodiak, Georgia, serif; font-weight: 700; font-size: 1.5rem; margin: 0; }}
  .sheet-sub {{ margin: 0; font-size: .85rem; color: var(--color-text-muted); }}
  @media (max-width: 559px) {{ .sheet-titles {{ text-align: left; order: -1; }} }}
  .sheet h3 {{ font-family: inherit; font-weight: 600; font-size: 1rem;
    color: var(--accent-pawfolio); border-bottom: 2px solid var(--accent-pawfolio);
    padding-bottom: .3rem; margin: 1.6rem 0 .8rem; }}
  .sheet h3 small {{ font-weight: 400; color: var(--color-text-muted); font-size: .8rem; margin-left: .4rem; }}
  .sheet h4 {{ font-size: .9rem; font-weight: 600; margin: 0 0 .3rem; }}
  .sg {{ display: grid; gap: 0 1rem; grid-template-columns: 1fr; }}
  .sg3 {{ display: grid; gap: 0 1rem; grid-template-columns: 1fr; }}
  @media (min-width: 560px) {{ .sg {{ grid-template-columns: 1fr 1fr; }} .sg3 {{ grid-template-columns: 1.3fr 1fr 1fr; }}
    .wide {{ grid-column: 1 / -1; }} }}
  .sf {{ display: block; margin: 0 0 .8rem; min-width: 0; }}
  .sf span {{ display: block; font-size: .85rem; font-weight: 600; color: var(--color-text-muted); margin-bottom: .2rem; }}
  .sf input, .sf textarea {{ width: 100%; max-width: 100%; min-width: 0; box-sizing: border-box; font: inherit; font-size: 1rem;
    color: var(--color-text); background: transparent; border: 0; border-bottom: 1px solid var(--color-border-strong);
    border-radius: 0; padding: .35rem 0; resize: none; overflow: hidden; -webkit-appearance: none; appearance: none; }}
  .sf input:focus, .sf textarea:focus {{ outline: none; border-bottom-color: var(--accent-pawfolio); }}
  .sf ::placeholder {{ color: var(--color-text-muted); opacity: .55; }}
  .sf-group {{ font-size: .85rem; font-weight: 600; color: var(--color-text-muted); margin: .4rem 0 .4rem; }}
  .auth-text {{ margin: 0 0 .8rem; font-size: .95rem; }}
  .sheet-tools {{ display: flex; flex-wrap: wrap; align-items: center; gap: .6rem 1.4rem; margin-top: 1rem; }}
  .print-tip {{ margin-top: .6rem; font-size: .85rem; color: var(--color-text-muted); }}

  /* Send to a sitter (only with #s= in the link). */
  .send-box {{ margin-top: .2rem; }}
  .send-privacy {{ flex: 0 0 100%; margin: -.2rem 0 .3rem; font-size: .9rem; color: var(--color-text-muted); }}
  @media (max-width: 559px) {{ .sheet-tools #send {{ flex: 1 1 100%; justify-content: center; }} }}
  @media (min-width: 560px) {{ .send-privacy {{ order: 10; margin: -.1rem 0 0; }} }}
  .send-msg {{ margin: .6rem 0 0; padding: .7rem .9rem; border-radius: var(--radius); font-size: .95rem; max-width: 52ch;
    background: var(--color-surface-2); border: 1px solid var(--color-border); color: var(--color-text); }}
  .send-msg:empty {{ display: none; }}
  .send-msg.ok {{ background: var(--accent-pawfolio-soft); border-color: color-mix(in srgb, var(--accent-pawfolio) 35%, transparent); }}
  .send-msg.err {{ background: color-mix(in srgb, #b4533a 9%, var(--color-surface)); border-color: color-mix(in srgb, #b4533a 40%, transparent); }}
  .sf.need span {{ color: #a3452f; }}
  .sf.need input {{ border-bottom: 2px solid #a3452f; }}
  [data-theme='dark'] .sf.need span {{ color: #e59a85; }}
  [data-theme='dark'] .sf.need input {{ border-bottom-color: #e59a85; }}
  @media (prefers-color-scheme: dark) {{
    :root:not([data-theme='light']) .sf.need span {{ color: #e59a85; }}
    :root:not([data-theme='light']) .sf.need input {{ border-bottom-color: #e59a85; }}
  }}
  .btn[disabled] {{ opacity: .65; cursor: progress; }}

  /* Medication rows: four across on wider screens, two by two on phones. */
  .meds {{ display: grid; gap: .2rem; }}
  .med-row {{ display: grid; gap: 0 1rem; grid-template-columns: 1fr 1fr; padding: .5rem .6rem .1rem;
    background: var(--color-surface-2); border-radius: var(--radius); }}
  .med-row .m-name, .med-row .m-how {{ grid-column: 1 / -1; }}
  @media (min-width: 640px) {{
    .med-row {{ grid-template-columns: 1.3fr .8fr .8fr 1.5fr; background: none; padding: 0; }}
    .med-row .m-name, .med-row .m-how {{ grid-column: auto; }}
    .med-row + .med-row .sf span {{ position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0 0 0 0); }}
  }}

  .ps-text {{ margin-top: 1.4rem; padding: 1rem 1.1rem; border-radius: var(--radius);
    background: var(--accent-pawfolio-soft); border: 1px solid color-mix(in srgb, var(--accent-pawfolio) 25%, transparent); }}
  .ps-text p {{ margin: 0; }}
  .ps-text-h {{ font-weight: 600; font-size: 1.05rem; color: var(--color-text); }}
  .ps-text p + p {{ margin-top: .35rem; color: var(--color-text-muted); }}
  .ps-text-link {{ display: inline-block; margin-top: .6rem; font-weight: 600; color: var(--accent-pawfolio);
    text-decoration: underline; text-underline-offset: 3px; }}

  /* Pet photo (round, like Pawfolio). */
  .pet-id {{ display: flex; gap: 1rem; align-items: flex-start; width: 100%; }}
  .pet-id-fields {{ flex: 1; min-width: 0; display: grid; gap: 0 1rem; grid-template-columns: 1fr; }}
  @media (min-width: 560px) {{ .pet-id-fields {{ grid-template-columns: 1fr 1fr; }} }}
  @media screen and (max-width: 559px) {{
    .pet-id {{ display: grid; grid-template-columns: 88px minmax(0, 1fr); gap: 0 1rem; }}
    .pet-id-fields {{ display: contents; }}
    .pet-photo {{ grid-row: span 2; }}
    .pet-id-fields > :nth-child(n+3) {{ grid-column: 1 / -1; }}
  }}
  .pet-desc {{ grid-column: 1 / -1; }}
  .pet-photo {{ flex: 0 0 auto; display: flex; flex-direction: column; align-items: center; }}
  .pet-photo input {{ position: absolute; width: 1px; height: 1px; opacity: 0; pointer-events: none; }}
  .pet-photo-btn {{ width: 88px; height: 88px; border-radius: 50%; overflow: hidden; cursor: pointer;
    display: flex; align-items: center; justify-content: center; text-align: center;
    border: 1.5px dashed var(--color-border-strong); background: var(--accent-pawfolio-soft);
    font-size: .8rem; font-weight: 600; color: var(--accent-pawfolio); }}
  .pet-photo-btn img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
  .pet-photo.has .pet-photo-btn {{ border-style: solid; }}
  .pet-photo.has .pet-photo-btn span {{ display: none; }}
  .pet-photo-btn:focus-within {{ outline: 2px solid var(--accent-pawfolio); }}
  .pet-photo-rm {{ font-size: .8rem; padding: .2rem 0; }}

  .print-only, .pv {{ display: none; }}
  @media print {{
    @page {{ size: letter; margin: 11mm 12mm; }}
    html, body {{ background: #fff !important; color: #000 !important; }}
    body.ps-page {{ background-image: none !important; }}
    .site-head, .site-foot, .ps-hero, .ps-hide-print, .sheet-tools, .skip, .print-tip, .maker {{ display: none !important; }}
    .ps-sec {{ padding: 0 !important; background: none !important; }}
    .wrap {{ padding: 0 !important; max-width: none !important; }}
    .sheet {{ border: 0; padding: 0; margin: 0; max-width: none; background: none; font-size: 9.5pt; }}
    .sheet-top {{ border-bottom-color: #5e7c73; padding-bottom: 6pt; flex-wrap: nowrap;
      -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
    .sheet-titles {{ text-align: right; order: 0; }}
    .sheet-title {{ font-size: 17pt; color: #24272b; }}
    .sheet-sub {{ font-size: 8.5pt; color: #555; }}
    #biz-name {{ font-size: 14pt; }}
    .biz-static .bs-name {{ font-size: 14pt; color: #000; }}
    .biz-static .bs-line {{ font-size: 9pt; color: #333; }}
    .sheet h3 {{ color: #4f6b63; border-color: #8fa89f; font-size: 10.5pt; margin: 8pt 0 3pt; break-after: avoid; }}
    .sheet h3 small {{ font-size: 7.5pt; color: #555; }}
    .sheet h4 {{ font-size: 9pt; margin: 0 0 1pt; }}
    .sg {{ grid-template-columns: 1fr 1fr; }}
    .sg3 {{ grid-template-columns: 1.3fr 1fr 1fr; }}
    .wide {{ grid-column: 1 / -1; }}
    .biz-line {{ grid-template-columns: 1fr 1.4fr; }}
    .sf {{ break-inside: avoid; margin-bottom: 3pt; }}
    .sf span {{ font-size: 7.5pt; margin-bottom: 0; color: #444; }}
    .sf input, .sf textarea {{ font-size: 9.5pt; padding: 1pt 0; color: #000; border-bottom: 1px solid #999; }}
    .sf ::placeholder {{ color: transparent; }}
    .sf-group {{ font-size: 7.5pt; color: #444; margin: 2pt 0 1pt; }}
    .auth-text {{ font-size: 9pt; margin-bottom: 3pt; }}
    .sf textarea {{ display: none !important; }}
    .pv {{ display: block; min-height: 1.9em; padding: 1pt 0; border-bottom: 1px solid #999;
      white-space: pre-wrap; overflow-wrap: anywhere; font-size: 9.5pt; color: #000; }}
    .pv[data-lines]:has(.rl) {{ min-height: calc(var(--n) * 1.7em); }}
    .pv .rl {{ height: 1.7em; border-bottom: 1px solid #999; }}
    .pv:has(.rl) {{ border-bottom: 0; padding: 0; }}
    .meds {{ gap: 0; }}
    .med-row {{ grid-template-columns: 1.3fr .8fr .8fr 1.5fr; background: none; padding: 0; }}
    .med-row .m-name, .med-row .m-how {{ grid-column: auto; }}
    .med-row + .med-row .sf span {{ display: none; }}
    .sheet-pet {{ break-inside: avoid; }}
    .pets-start {{ break-before: page; }}
    .pet-id-fields {{ grid-template-columns: 1.2fr 1.4fr .6fr .6fr; }}
    .pet-id-fields > :nth-child(5) {{ grid-column: span 2; }}
    .pet-id-fields > :nth-child(6) {{ grid-column: span 2; }}
    .pet-desc {{ grid-column: 1 / -1; }}
    .pet-photo-btn {{ width: 0.95in; height: 0.95in; border: 1px dashed #999; background: none; color: #999; font-size: 8pt; }}
    .pet-photo.has .pet-photo-btn {{ border: 0; }}
    .pet-photo[data-print-hide] {{ display: none; }}
    .print-only {{ display: block; }}
    .ps-plug.print-only {{ display: flex; align-items: center; gap: 10pt; margin-top: 10pt; padding: 6pt 10pt 6pt 6pt;
      border: 1px solid #b9cdc5; border-radius: 6pt; background: #edf2ef; break-inside: avoid;
      -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
    .ps-plug img {{ width: 0.62in; height: 0.62in; flex: 0 0 auto; background: #fff; }}
    .ps-plug p {{ margin: 0; font-size: 8pt; color: #333; line-height: 1.35; }}
    .ps-plug .ps-plug-h {{ font-size: 9.5pt; font-weight: 700; color: #4f6b63; }}
    .ps-plug .ps-plug-u {{ font-weight: 700; color: #24272b; }}
    .print-foot {{ margin-top: 6pt; font-size: 7pt; color: #666; }}
  }}
</style>
</head>
<body class="ps-page">
<a class="skip" href="#top">Skip to content</a>

<header class="site-head"></header>

<main id="top">
  <section class="ps-hero" id="hero-sitter">
    <div class="wrap">
      <p class="ps-eyebrow">For pet sitters and dog walkers</p>
      <h1>Free pet sitter client intake form</h1>
      <p class="ps-lede">Send new clients one link with your business name at the top. They fill it in on
        their phone, add photos of their pets, and send it back to you as a PDF.</p>
      <p class="ps-links"><a href="#make">Make your link</a><a href="{PDF}" download>Download the blank PDF</a></p>
    </div>
  </section>

  <section class="ps-hero" id="hero-client" hidden>
    <div class="wrap">
      <p class="ps-eyebrow">New client form for</p>
      <h1 id="hc-name"></h1>
      <p class="ps-contact" id="hc-contact"></p>
      <p class="ps-lede" id="hc-lede">Fill this in and add a photo of each pet. When you're done, tap
        <strong>Print or save as PDF</strong> and send it to <span id="hc-name2"></span>.</p>
    </div>
  </section>

  <section class="ps-sec" aria-label="Make your link" id="make" style="padding-bottom:0">
    <div class="wrap">
      <div class="maker">
        <h2>Make your link</h2>
        <p>Type your business info once. Your clients will see it at the top of the form.</p>
        <div class="sg">
          <label class="sf wide"><span>Business name</span><input id="mk-b" type="text" maxlength="60" placeholder="e.g., Happy Tails Pet Care" autocomplete="organization"></label>
          <label class="sf"><span>Phone</span><input id="mk-p" type="tel" maxlength="30" placeholder="(555) 010-2233" autocomplete="tel"></label>
          <label class="sf"><span>Email or website</span><input id="mk-e" type="text" maxlength="80" placeholder="hello@happytails.com" autocomplete="email"></label>
        </div>
        <div class="maker-out" id="mk-out" hidden>
          <p>Your link</p>
          <a class="maker-url" id="mk-url" href="#" target="_blank" rel="noopener"></a>
          <div class="maker-btns">
            <button type="button" class="btn btn-primary" id="mk-copy">Copy link</button>
            <button type="button" class="linkbtn" id="mk-share" hidden>Share</button>
            <a class="linkbtn" id="mk-preview" href="#" target="_blank" rel="noopener">See what clients see</a>
          </div>
        </div>
        <p class="maker-hint">Text it to new clients, add it to your booking confirmation, or put it in your bio.
          The link holds only your business info. Your clients' answers stay on their own phones.</p>
        <p class="maker-hint" id="mk-app">With a link made here, clients send the form back to you as a PDF. To get
          forms in an app instead, turn on <a href="../pawfolio/">Sitter mode in Pawfolio</a>. It's free.</p>
      </div>
    </div>
  </section>

  <section class="ps-sec" aria-label="Client intake form" id="form">
    <div class="wrap">
      <form class="sheet" id="sheet" autocomplete="off" onsubmit="return false">
        <div class="sheet-top">
          <div class="biz" id="biz">
            <div class="biz-edit">
              {field("biz-name", "Pet sitter / business name", "Your business name", cls="biz-n")}
              <div class="biz-line">
                {field("biz-phone", "Phone", "Sitter's phone")}
                {field("biz-email", "Email or website", "Sitter's email")}
              </div>
            </div>
            <div class="biz-static" aria-live="polite">
              <p class="bs-name" id="bs-name"></p>
              <p class="bs-line" id="bs-line"></p>
            </div>
          </div>
          <div class="sheet-titles">
            <p class="sheet-title">New Client Intake</p>
            <p class="sheet-sub">Pet care information form</p>
          </div>
        </div>

        <h3>Client</h3>
        <div class="sg3">
          {field("c-name", "Name(s)", "e.g., Sam and Alex Taylor")}
          {field("c-phone", "Mobile phone", "(555) 010-9911", typ="tel")}
          {field("c-email", "Email", "sam@example.com", typ="email")}
        </div>
        <div class="sg">
          {field("c-address", "Home address", "123 Oak St, Granbury", cls="")}
          {field("c-phone2", "Other phone", "Work or partner's phone", typ="tel")}
        </div>

        <h3>Emergency contact <small>Someone nearby who can make decisions if you can't be reached</small></h3>
        <div class="sg">
          {field("e-name", "Name", "e.g., Jordan Lee")}
          {field("e-rel", "Relationship", "e.g., Neighbor")}
          {field("e-phone", "Phone", "(555) 010-4477", typ="tel")}
          {field("e-key", "Has a key?", "Yes / No")}
        </div>

        <h3>Veterinary care</h3>
        <div class="sg">
          <div>
            <h4>Regular vet</h4>
            {field("v-name", "Clinic", "e.g., Happy Paws Clinic")}
            {field("v-phone", "Phone", "(555) 123-4567", typ="tel")}
            {field("v-address", "Address", "123 Main St")}
          </div>
          <div>
            <h4>Emergency / 24-hour vet</h4>
            {field("ev-name", "Clinic", "e.g., County 24-Hour Animal Hospital")}
            {field("ev-phone", "Phone", "(555) 999-0000", typ="tel")}
            {field("ev-address", "Address", "800 Hwy 377")}
          </div>
        </div>

        <h3>Home and visits</h3>
        <div class="sg">
          {field("h-entry", "How to get in (key, lockbox, door code)", "e.g., Lockbox on back gate, code 4821")}
          {field("h-alarm", "Alarm code", "None")}
          {field("h-wifi", "Wi-Fi network / password", "Optional")}
          {field("h-park", "Parking", "e.g., Driveway is fine")}
          {field("h-supplies", "Where supplies are kept (food, leash, litter, meds)", "e.g., Hall closet", cls="wide")}
          {field("h-off", "Rooms or areas that are off-limits", "e.g., Keep the office door closed")}
          {field("h-extra", "Extra requests (mail, plants, trash, lights)", "e.g., Bring in the mail")}
          {field("h-notes", "Anything else I should know about the home", "", area=True, lines=2, cls="wide")}
        </div>

        <h3>Emergency care authorization</h3>
        <p class="auth-text">If my pet needs urgent care and I can't be reached, I authorize my pet sitter to take
          my pet to my vet or the nearest emergency vet and approve treatment up to the amount below.
          I agree to pay for that care.</p>
        <div class="sg3">
          {field("a-amount", "Approved amount ($)", "e.g., 500")}
          {field("a-sign", "Client signature (or type your full name)", "")}
          {field("a-date", "Date", "")}
        </div>

        <div class="pets-start">
{pet_block(1)}{pet_block(2)}{pet_block(3)}{pet_block(4)}
        </div>

        <div class="sheet-tools">
          <button type="button" class="linkbtn" id="add-pet">+ Add another pet</button>
        </div>

        <div class="sheet-tools">
          <button type="button" class="btn btn-primary" id="send" hidden>Send</button>
          <p class="send-privacy ps-hide-print" id="send-privacy" hidden></p>
          <button type="button" class="btn btn-primary" id="print">Print or save as PDF</button>
          <a class="linkbtn" href="{PDF}" download>Blank PDF</a>
          <button type="button" class="linkbtn" id="clear">Clear form</button>
        </div>
        <div class="send-box ps-hide-print" id="send-box" hidden>
          <p class="send-msg" id="send-msg" role="status" aria-live="polite"></p>
        </div>
        <p class="print-tip">To save a PDF, choose Save as PDF in the print screen. On an iPhone, tap the Share
          button at the top of the print screen, then Save to Files, Messages or Mail.</p>

        <div class="ps-plug print-only">
          <img src="qr-pawfolio.svg" width="58" height="58" alt="">
          <div>
            <p class="ps-plug-h">Does your pet take medication? Try Pawfolio.</p>
            <p>Pawfolio Free keeps your pet's profiles, medications and sitter info on your phone and reminds you when
              doses are due. With Pawfolio Complete, you can share doses with your sitter, so you both see each dose given.</p>
            <p class="ps-plug-u">Scan the code or visit cleartrackapps.com/pawfolio</p>
          </div>
        </div>
        <p class="print-only print-foot">Free intake form from cleartrackapps.com/pet-sitter-intake-form</p>

        <div class="ps-text ps-hide-print">
          <p class="ps-text-h">Does your pet take medication?</p>
          <p>Pawfolio Free keeps your pet's profiles, medications and sitter info on your phone and reminds you
            when doses are due. With Pawfolio Complete, you can share doses with your sitter, so you both see
            each dose given.</p>
          <a class="ps-text-link" href="{APP}">Open Pawfolio&nbsp;Free&nbsp;&rarr;</a>
        </div>
      </form>
      <p class="ps-note ps-hide-print" id="ps-note">What you type stays in this browser. Nothing is sent anywhere.</p>
    </div>
  </section>

  <section class="ps-sec ps-alt ps-hide-print" aria-labelledby="what-h" id="covers">
    <div class="wrap">
      <h2 class="ps-h2" id="what-h">What the intake form covers</h2>
      <ul class="ps-list">
{covers()}
      </ul>
    </div>
  </section>

  <section class="ps-sec ps-hide-print" aria-labelledby="cta-h">
    <div class="wrap ps-cta">
      <h2 class="ps-h2" id="cta-h" style="margin-inline:auto">Pets on medication?</h2>
      <p class="ps-sub" style="margin-inline:auto">With Pawfolio Complete, your clients share their pets' doses
        with you. You get a private link with today's doses and tap Given, and the owner sees it right away.
        You don't need an account. Your clients can start with Pawfolio Free.</p>
      <div class="ps-actions">
        <a class="btn btn-primary btn-lg" href="../pawfolio/sitter-sharing/">See how sitter sharing works</a>
        <a class="btn btn-ghost btn-lg" href="{DEMO}">Try the demo</a>
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

<footer class="site-foot"></footer>

<script src="../app.js?v=20261014g" defer></script>
<script src="intake-crypto.js?v=1"></script>
<script>
(function () {{
  var KEY = 'ct-sitter-intake-v1', BIZ = 'ct-sitter-intake-biz';
  var BASE = location.origin + location.pathname;
  var form = document.getElementById('sheet');
  var fields = form.querySelectorAll('[data-k]');
  var pets = form.querySelectorAll('.sheet-pet');
  var addBtn = document.getElementById('add-pet');
  function load(k) {{ try {{ return JSON.parse(localStorage.getItem(k) || '{{}}') || {{}}; }} catch (e) {{ return {{}}; }} }}
  function store(k, v) {{ try {{ localStorage.setItem(k, JSON.stringify(v)); }} catch (e) {{}} }}
  var data = load(KEY);

  // ---- Which mode: a client opening a sitter's link, or a sitter. ----
  var q = new URLSearchParams(location.search);
  function clip(s, n) {{ return (s || '').replace(/[\\u0000-\\u001f]/g, '').trim().slice(0, n); }}
  var link = {{ b: clip(q.get('b'), 60), p: clip(q.get('p'), 30), e: clip(q.get('e'), 80) }};
  var client = !!link.b;
  // A Pawfolio Sitter mode link adds #s=<inboxId>.<publicKey>. It lives only in the
  // fragment (browsers never send it to a server), and we read it once here.
  var PI = window.PawfolioIntake;
  var target = PI ? PI.parseSendTarget(location.hash) : null;
  var sendName = link.b || 'your sitter';

  var bizIn = {{ b: document.getElementById('biz-name'), p: document.getElementById('biz-phone'), e: document.getElementById('biz-email') }};
  function contactHref(v) {{
    if (/^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/.test(v)) return 'mailto:' + v;
    if (/^(https?:\\/\\/)?[\\w-]+(\\.[\\w-]+)+(\\/\\S*)?$/i.test(v)) return /^https?:/i.test(v) ? v : 'https://' + v;
    return '';
  }}
  if (client) {{
    document.getElementById('hero-sitter').hidden = true;
    document.getElementById('make').hidden = true;
    document.getElementById('hero-client').hidden = false;
    document.getElementById('hc-name').textContent = link.b;
    document.getElementById('hc-name2').textContent = link.b;
    var hc = document.getElementById('hc-contact');
    if (link.p) {{ var a = document.createElement('a'); a.href = 'tel:' + link.p.replace(/[^\\d+]/g, ''); a.textContent = link.p; hc.appendChild(a); }}
    if (link.e) {{ var h = contactHref(link.e), el = document.createElement(h ? 'a' : 'span'); if (h) el.href = h; el.textContent = link.e; hc.appendChild(el); }}
    document.getElementById('biz').classList.add('biz-show');
    document.getElementById('bs-name').textContent = link.b;
    document.getElementById('bs-line').textContent = [link.p, link.e].filter(Boolean).join('  ·  ');
    document.title = 'New client form for ' + link.b;
  }}

  if (target) {{
    document.addEventListener('click', function (ev) {{
      var a = ev.target.closest && ev.target.closest('a[href^="#"]');
      if (!a || ev.defaultPrevented) return;
      var id = a.getAttribute('href').slice(1), el = id && document.getElementById(id);
      if (!el) return;
      ev.preventDefault();
      el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
      if (!el.hasAttribute('tabindex')) el.setAttribute('tabindex', '-1');
      el.focus({{ preventScroll: true }});
    }});
  }}

  // ---- Link maker (sitters). Also fills the form's header. ----
  var mk = {{ b: document.getElementById('mk-b'), p: document.getElementById('mk-p'), e: document.getElementById('mk-e') }};
  var biz = load(BIZ);
  function linkFor(v) {{
    function enc(x) {{ return encodeURIComponent(x).replace(/%20/g, '+').replace(/%40/g, '@').replace(/%28/g, '(').replace(/%29/g, ')').replace(/%2C/g, ','); }}
    var u = 'b=' + enc(v.b); if (v.p) u += '&p=' + enc(v.p); if (v.e) u += '&e=' + enc(v.e);
    return BASE + '?' + u + (target ? PI.sendFragment(target.inboxId, target.publicKey) : '');
  }}
  function renderLink() {{
    var v = {{ b: clip(mk.b.value, 60), p: clip(mk.p.value, 30), e: clip(mk.e.value, 80) }};
    var out = document.getElementById('mk-out');
    out.hidden = !v.b;
    if (!v.b) return;
    var u = linkFor(v);
    var a = document.getElementById('mk-url'); a.textContent = u; a.href = u;
    document.getElementById('mk-preview').href = u;
  }}
  if (!client) {{
    ['b', 'p', 'e'].forEach(function (k) {{
      mk[k].value = biz[k] || '';
      if (!bizIn[k].value && biz[k] && !data['biz-' + ({{b: 'name', p: 'phone', e: 'email'}})[k]]) data['biz-' + ({{b: 'name', p: 'phone', e: 'email'}})[k]] = biz[k];
      mk[k].addEventListener('input', function () {{
        biz[k] = mk[k].value; store(BIZ, biz); renderLink();
        var f = bizIn[k]; f.value = mk[k].value; data[f.dataset.k] = f.value; save();
      }});
    }});
    renderLink();
    var share = document.getElementById('mk-share');
    if (navigator.share) share.hidden = false;
    share.addEventListener('click', function () {{
      var u = document.getElementById('mk-url').href;
      navigator.share({{ title: 'New client form', text: 'Please fill in my new client form for your pets:', url: u }}).catch(function () {{}});
    }});
    var copy = document.getElementById('mk-copy');
    copy.addEventListener('click', function () {{
      var u = document.getElementById('mk-url').href;
      function done() {{ copy.textContent = 'Copied'; setTimeout(function () {{ copy.textContent = 'Copy link'; }}, 1600); }}
      if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(u).then(done, fallback); else fallback();
      function fallback() {{ var t = document.createElement('textarea'); t.value = u; document.body.appendChild(t); t.select();
        try {{ document.execCommand('copy'); done(); }} catch (e) {{}} t.remove(); }}
    }});
  }}

  // ---- The form ----
  function mirror(t) {{ if (t.tagName === 'TEXTAREA') {{ var v = t.nextElementSibling; if (!v || !v.classList.contains('pv')) {{ v = document.createElement('div'); v.className = 'pv'; var n = +t.dataset.lines || 1; if (n > 1) {{ v.dataset.lines = n; v.style.setProperty('--n', n); }} t.after(v); }} v.textContent = t.value; var n = +(v.dataset.lines || 0); if (n > 1 && !t.value) {{ for (var i = 0; i < n; i++) {{ var l = document.createElement('div'); l.className = 'rl'; v.appendChild(l); }} }} }} }}
  function grow(t) {{ if (t.tagName === 'TEXTAREA') {{ t.style.height = 'auto'; t.style.height = t.scrollHeight + 'px'; }} }}
  function shown() {{ var n = 0; pets.forEach(function (p) {{ if (!p.hidden) n++; }}); return n; }}
  function showPets(n) {{ pets.forEach(function (p, i) {{ p.hidden = i >= n; }}); addBtn.hidden = n >= pets.length; }}
  function save() {{ data.pets = shown(); store(KEY, data); }}

  fields.forEach(function (f) {{
    if (data[f.dataset.k]) f.value = data[f.dataset.k];
    mirror(f);
    f.addEventListener('input', function () {{ data[f.dataset.k] = f.value; grow(f); mirror(f); save(); }});
  }});
  var used = 1;
  pets.forEach(function (p, i) {{
    p.querySelectorAll('[data-k]').forEach(function (f) {{ if (f.value) used = Math.max(used, i + 1); }});
    if (data['pet' + (i + 1) + '-photo']) used = Math.max(used, i + 1);
  }});
  showPets(Math.max(used, data.pets || 1));
  requestAnimationFrame(function () {{ fields.forEach(grow); }});

  // Pet photos: center-cropped, shrunk to 360px and kept with the form.
  var photos = form.querySelectorAll('.pet-photo');
  function setPhoto(box, url) {{
    var img = box.querySelector('img'), rm = box.querySelector('.pet-photo-rm');
    if (url) {{ img.src = url; img.hidden = false; box.classList.add('has'); rm.hidden = false; }}
    else {{ img.removeAttribute('src'); img.hidden = true; box.classList.remove('has'); rm.hidden = true; }}
  }}
  function shrink(file, done) {{
    var r = new FileReader();
    r.onload = function () {{
      var im = new Image();
      im.onload = function () {{
        var S = 360, c = document.createElement('canvas'); c.width = c.height = S;
        var side = Math.min(im.width, im.height);
        c.getContext('2d').drawImage(im, (im.width - side) / 2, (im.height - side) / 2, side, side, 0, 0, S, S);
        done(c.toDataURL('image/jpeg', 0.82));
      }};
      im.src = r.result;
    }};
    r.readAsDataURL(file);
  }}
  photos.forEach(function (box) {{
    var k = box.dataset.photo, inp = box.querySelector('input'), rm = box.querySelector('.pet-photo-rm');
    if (data[k]) setPhoto(box, data[k]);
    inp.addEventListener('change', function () {{
      var f = inp.files && inp.files[0]; if (!f) return;
      shrink(f, function (url) {{ data[k] = url; setPhoto(box, url); save(); inp.value = ''; }});
    }});
    rm.addEventListener('click', function () {{ delete data[k]; setPhoto(box, ''); save(); }});
  }});

  addBtn.addEventListener('click', function () {{
    var n = shown() + 1; showPets(n); save();
    var first = pets[n - 1] && pets[n - 1].querySelector('input:not([type=file])'); if (first) first.focus();
  }});
  document.getElementById('print').addEventListener('click', function () {{ window.print(); }});
  document.getElementById('clear').addEventListener('click', function () {{
    if (!confirm('Erase everything on this form?')) return;
    var keep = {{}};
    if (!client) ['biz-name', 'biz-phone', 'biz-email'].forEach(function (k) {{ if (data[k]) keep[k] = data[k]; }});
    data = keep; store(KEY, data);
    fields.forEach(function (f) {{ f.value = data[f.dataset.k] || ''; grow(f); mirror(f); }});
    photos.forEach(function (box) {{ setPhoto(box, ''); }});
    showPets(1);
  }});
  // Blank pet sections after the first don't print; a filled pet with no photo skips the empty circle.
  window.addEventListener('beforeprint', function () {{
    pets.forEach(function (p, i) {{
      var any = !!data['pet' + (i + 1) + '-photo'];
      p.querySelectorAll('[data-k]').forEach(function (f) {{ if (f.value) any = true; }});
      if (i > 0 && !p.hidden && !any) {{ p.dataset.printHide = '1'; p.hidden = true; }}
      var box = p.querySelector('.pet-photo');
      if (any && !data['pet' + (i + 1) + '-photo']) box.dataset.printHide = '1';
    }});
    fields.forEach(mirror);
  }});
  window.addEventListener('afterprint', function () {{
    pets.forEach(function (p) {{ if (p.dataset.printHide) {{ delete p.dataset.printHide; p.hidden = false; }} }});
    photos.forEach(function (b) {{ delete b.dataset.printHide; }});
  }});

  // ---- Send to the sitter (only when the link has #s=). ----
  // The answers are encrypted on this phone with the sitter's public key, and only
  // that encrypted envelope is uploaded. Nothing else ever leaves the browser.
  if (!target) return;
  var CID = 'ct-sitter-intake-cid', SENT = 'ct-sitter-intake-sent';
  var AUTH = "If my pet needs urgent care and I can't be reached, I authorize my pet sitter to take my pet to my vet or the nearest emergency vet and approve treatment up to the amount below. I agree to pay for that care.";
  var sendBtn = document.getElementById('send'), msg = document.getElementById('send-msg');
  var label = 'Send to ' + sendName;
  sendBtn.textContent = label; sendBtn.hidden = false;
  document.getElementById('print').className = 'btn btn-ghost';
  document.getElementById('send-box').hidden = false;
  document.getElementById('send-privacy').hidden = false;
  document.getElementById('send-privacy').textContent = "Encrypted on your phone before it's sent. Only " +
    (link.b ? link.b + "'s" : "your sitter's") + " phone can open it, and I can't read it.";
  document.getElementById('ps-note').textContent = "What you type is saved in this browser. It's only sent when you tap " + label + ", and it's encrypted first.";
  if (client) {{
    var lede = document.getElementById('hc-lede');
    lede.textContent = "Fill this in and add a photo of each pet. When you're done, tap ";
    var st = document.createElement('strong'); st.textContent = label; lede.appendChild(st);
    lede.appendChild(document.createTextNode(' at the bottom. You can also print it or save a PDF.'));
  }}
  function day(iso) {{ try {{ return new Date(iso).toLocaleDateString(undefined, {{ month: 'long', day: 'numeric', year: 'numeric' }}); }} catch (e) {{ return ''; }} }}
  function say(text, kind) {{ msg.textContent = text; msg.className = 'send-msg' + (kind ? ' ' + kind : ''); }}
  function sentText(iso) {{ return 'Sent to ' + sendName + ' on ' + day(iso) + '. You can send it again if anything changes.'; }}
  var sent = load(SENT);
  if (sent[target.inboxId]) say(sentText(sent[target.inboxId]), 'ok');

  function val(k) {{ var f = form.querySelector('[data-k="' + k + '"]'); return f ? String(f.value || '').trim() : ''; }}
  function clientId() {{
    var m = load(CID);
    if (typeof m !== 'object' || Array.isArray(m)) m = {{}};
    if (!m[target.inboxId]) {{ m[target.inboxId] = PI.b64u(crypto.getRandomValues(new Uint8Array(16))); store(CID, m); }}
    return m[target.inboxId];
  }}
  async function buildPayload() {{
    var out = [];
    for (var n = 1; n <= pets.length; n++) {{
      var p = 'pet' + n, photo = data[p + '-photo'] || '';
      if (!val(p + '-name') && !photo) continue;
      var meds = [];
      for (var m = 1; m <= 3; m++) {{
        var mk = p + '-med' + m + '-';
        if (val(mk + 'name')) meds.push({{ name: val(mk + 'name'), dose: val(mk + 'dose'), time: val(mk + 'time'), how: val(mk + 'how') }});
      }}
      if (photo) {{ try {{ photo = await PI.shrinkPhoto(photo, 720, 0.78); }} catch (e) {{ photo = ''; }} }}
      var pet = {{}};
      ['name', 'kind', 'age', 'weight', 'sex', 'chip', 'desc', 'food', 'treats', 'health', 'walk', 'behave', 'notes']
        .forEach(function (k) {{ pet[k] = val(p + '-' + k); }});
      pet.rabies = ''; pet.insurance = ''; pet.meds = meds; pet.photo = photo;
      out.push(pet);
    }}
    return {{
      kind: 'pawfolio-intake', v: 1, sentAt: new Date().toISOString(), source: 'web', clientId: clientId(),
      sitter: {{ name: link.b || val('biz-name'), phone: link.p || val('biz-phone'), email: link.e || val('biz-email') }},
      client: {{ name: val('c-name'), phone: val('c-phone'), email: val('c-email'), address: val('c-address'), phone2: val('c-phone2') }},
      emergency: {{ name: val('e-name'), rel: val('e-rel'), phone: val('e-phone'), hasKey: val('e-key') }},
      vet: {{ name: val('v-name'), phone: val('v-phone'), address: val('v-address') }},
      emergencyVet: {{ name: val('ev-name'), phone: val('ev-phone'), address: val('ev-address') }},
      home: {{ entry: val('h-entry'), alarm: val('h-alarm'), wifi: val('h-wifi'), parking: val('h-park'), supplies: val('h-supplies'),
        offLimits: val('h-off'), extra: val('h-extra'), notes: val('h-notes') }},
      authorization: {{ amount: val('a-amount'), signature: val('a-sign'), date: val('a-date'), text: AUTH }},
      pets: out
    }};
  }}
  function mark(k, on) {{ var f = form.querySelector('[data-k="' + k + '"]'); if (f) f.closest('.sf').classList.toggle('need', on); return f; }}
  fields.forEach(function (f) {{ f.addEventListener('input', function () {{ var l = f.closest('.sf'); if (l) l.classList.remove('need'); }}); }});
  function check() {{
    var miss = [], first = null;
    function need(k, what) {{ var bad = !val(k), f = mark(k, bad); if (bad) {{ miss.push(what); first = first || f; }} }}
    need('c-name', 'your name'); need('c-phone', 'your mobile phone');
    var anyPet = false;
    for (var n = 1; n <= pets.length; n++) if (val('pet' + n + '-name')) anyPet = true;
    mark('pet1-name', !anyPet);
    if (!anyPet) {{ miss.push("your pet's name"); first = first || form.querySelector('[data-k="pet1-name"]'); }}
    if (!miss.length) return true;
    var list = miss.length === 1 ? miss[0] : miss.slice(0, -1).join(', ') + ' and ' + miss[miss.length - 1];
    say('Please add ' + list + ' before sending.', 'err');
    if (first) first.focus();
    return false;
  }}
  var busy = false;
  sendBtn.addEventListener('click', async function () {{
    if (busy || !check()) return;
    if (navigator.onLine === false) {{ say("You seem to be offline. Your answers are still here. Try again when you're connected.", 'err'); return; }}
    busy = true; sendBtn.disabled = true; sendBtn.textContent = 'Sending...'; say('Encrypting and sending...');
    try {{
      await PI.submit(target, await buildPayload());
      var now = new Date().toISOString();
      sent[target.inboxId] = now; store(SENT, sent);
      say(sentText(now), 'ok');
    }} catch (e) {{
      var code = (e && (e.code || e.message)) || '';
      if (code === 'too_large' || (e && e.status === 413)) say('This form is too large to send with these photos. Try fewer or smaller photos, then send again.', 'err');
      else if (code === 'not_found' || (e && e.status === 404)) say("This link isn't active anymore. Ask your sitter for a new one.", 'err');
      else if (code === 'inbox_full' || (e && e.status === 429)) say("This sitter's inbox is full right now. Please let them know.", 'err');
      else if (navigator.onLine === false || (e && e.name === 'TypeError')) say("You seem to be offline, so it wasn't sent. Your answers are still here. Try again when you're connected.", 'err');
      else say("Something went wrong and it wasn't sent. Please try again, or print or save a PDF instead.", 'err');
    }} finally {{
      busy = false; sendBtn.disabled = false; sendBtn.textContent = label;
    }}
  }});
}})();
</script>
{CF_BEACON}
</body>
</html>
'''


if __name__ == "__main__":
    OUT_DIR.mkdir(exist_ok=True)
    import build_sitter, chrome
    (OUT_DIR / "paws.svg").write_text(build_sitter.paws_svg("#5e7c73", 0.13), encoding="utf-8")
    (OUT_DIR / "paws-dark.svg").write_text(build_sitter.paws_svg("#9dbcb2", 0.10), encoding="utf-8")
    page = chrome.apply(PAGE, "../", "&copy; 2026 CleartrackApps. Pawfolio&trade; is a trademark of CleartrackApps.", extra="")
    (OUT_DIR / "index.html").write_text(page, encoding="utf-8")
    print(f"wrote {OUT_DIR / 'index.html'}")
