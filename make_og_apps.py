"""Generate per-app link-preview cards (1200x630) for the five CleartrackApps apps.

Same visual language as assets/og-image.png: cream ground, Zodiak headline,
General Sans body, pill chips, cleartrack logo top-left. Each app gets its own
background tint so the five cards are distinguishable at a glance.

Copy is taken verbatim from the APPS list in build.py -- nothing invented.

Run:  python3 make_og_apps.py
Out:  assets/og-pawfolio.png, og-medical-records.png, og-budget-tracker.png,
      og-puzzle-pig.png, og-cosmetic-surgery-planner.png
"""
import pathlib
from playwright.sync_api import sync_playwright

D = pathlib.Path(__file__).parent

APPS = [
    dict(slug="pawfolio", name="Pawfolio", tag="Pet care",
         who="For pet owners who want every vet detail in one place.",
         tint="#f3ead6", tint2="#e8f0e6"),
    dict(slug="medical-records", name="Medical Records Keeper", tag="Family health",
         who="For families and caregivers juggling more than one person's health.",
         tint="#e2eef6", tint2="#eef0f7"),
    dict(slug="budget-tracker", name="Budget Tracker", tag="Money",
         who="For anyone who wants a budget that stays on their own phone.",
         tint="#e3efe6", tint2="#f2eeda"),
    dict(slug="puzzle-pig", name="Puzzle Pig", tag="Kids &amp; chores",
         who="For parents teaching kids to earn, save, and give.",
         tint="#ece7f7", tint2="#f7e9ef"),
    dict(slug="cosmetic-surgery-planner", name="Cosmetic Surgery Planner", tag="Planning",
         who="For anyone planning a procedure and saving up for it.",
         tint="#f6e9f0", tint2="#eae9f6"),
]

TEMPLATE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<link rel="stylesheet" href="https://api.fontshare.com/v2/css?f[]=general-sans@400,500,600&f[]=zodiak@700&display=swap">
<style>
  * {{ margin:0; box-sizing:border-box; }}
  body {{ width:1200px; height:630px; background:#faf6ef; font-family:'General Sans',sans-serif;
         color:#2a2318; padding:74px 80px; display:flex; flex-direction:column;
         justify-content:space-between;
         background-image: radial-gradient(80% 60% at 100% 0%, {tint} 0%, transparent 60%),
                           radial-gradient(70% 70% at 0% 100%, {tint2} 0%, transparent 62%); }}
  .top {{ display:flex; align-items:center; gap:20px; }}
  .top img.logo {{ width:206px; height:auto; display:block; }}
  h1 {{ font-family:'Zodiak',serif; font-size:{size}px; line-height:1.06;
       letter-spacing:-.025em; max-width:17ch; font-weight:700; }}
  p.sub {{ margin-top:22px; font-size:26px; color:#6b6152; max-width:34ch; }}
  .row {{ display:flex; gap:14px; align-items:center; flex-wrap:wrap; }}
  .chip {{ font-size:21px; font-weight:500; padding:10px 20px; border-radius:999px;
          border:1.5px solid #d3c6b0; color:#4b4238; background:#fffdf9; }}
  .chip.lead {{ background:#1c574a; border-color:#1c574a; color:#faf6ef; font-weight:600; }}
</style></head>
<body>
  <div class="top">
    <img class="logo" src="./assets/logo.png" alt="Cleartrack Apps">
  </div>
  <div>
    <h1>{name}</h1>
    <p class="sub">{who}</p>
  </div>
  <div class="row">
    <div class="chip lead">{tag}</div>
    <div class="chip">No signal needed</div>
    <div class="chip">No app store</div>
    <div class="chip">Pay once</div>
  </div>
</body></html>
"""

tmp = D / "_og_app_tmp.html"
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
    for a in APPS:
        # Long names need a smaller headline so they stay on two lines.
        size = 66 if len(a["name"]) <= 14 else (58 if len(a["name"]) <= 24 else 54)
        tmp.write_text(TEMPLATE.format(size=size, **a), encoding="utf-8")
        pg.goto(tmp.as_uri())
        pg.wait_for_timeout(2500)
        out = D / f"assets/og-{a['slug']}.png"
        pg.screenshot(path=str(out))
        print(f"wrote {out.name}")
    b.close()
tmp.unlink(missing_ok=True)
print("done")
