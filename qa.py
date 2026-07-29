import sys, pathlib
from playwright.sync_api import sync_playwright

D = pathlib.Path(__file__).parent
URL = (D / "index.html").as_uri()

with sync_playwright() as p:
    b = p.chromium.launch()
    # og image
    if "og" in sys.argv:
        pg = b.new_page(viewport={"width": 1200, "height": 630}, device_scale_factor=1)
        pg.goto((D / "og-source.html").as_uri()); pg.wait_for_timeout(2500)
        pg.screenshot(path=str(D / "assets/og-image.png"))
        pg.close(); print("og-image written")

    for name, w, dark in [("mobile", 375, False), ("desktop", 1280, False), ("mobile-dark", 375, True)]:
        pg = b.new_page(viewport={"width": w, "height": 900},
                        color_scheme="dark" if dark else "light",
                        device_scale_factor=2 if w == 375 else 1)
        pg.goto(URL); pg.wait_for_timeout(2200)
        # expand all FAQ for QA shots
        pg.screenshot(path=str(D / f"../shots-{name}.png"), full_page=True)
        # overflow check
        ov = pg.evaluate("""() => {
          const bad = [];
          document.querySelectorAll('body *').forEach(el => {
            const r = el.getBoundingClientRect();
            if (r.width && (r.right > window.innerWidth + 1 || r.left < -1)) bad.push(el.tagName + '.' + el.className + ' ' + Math.round(r.left) + '..' + Math.round(r.right));
          });
          return {w: window.innerWidth, docW: document.documentElement.scrollWidth, bad: bad.slice(0,12)};
        }""")
        print(name, ov)
        pg.close()
    b.close()
