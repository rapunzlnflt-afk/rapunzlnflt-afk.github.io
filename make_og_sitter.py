"""Generate assets/og-pawfolio-sitter-sharing.png (1200x630), the link preview for
/pawfolio/sitter-sharing/. Cloud gray gradient, sage button, cocoa badge; the phones
are a frame captured from the walkthrough itself (pass the PNG path as argv[1])."""
import pathlib, sys, base64
from playwright.sync_api import sync_playwright
D = pathlib.Path(__file__).parent
phones = base64.b64encode(pathlib.Path(sys.argv[1]).read_bytes()).decode()
icon = base64.b64encode((D / "pawfolio/sitter-sharing/icon-192.png").read_bytes()).decode()
HTML = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@700;800&family=Karla:wght@500;700&display=swap" rel="stylesheet">
<style>
 *{{margin:0;box-sizing:border-box}}
 body{{width:1200px;height:630px;overflow:hidden;font-family:'Karla',sans-serif;color:#24272b;
   background:linear-gradient(160deg,#fafbfc 0%,#f5f6f8 40%,#eceff3 75%,#e6e9ee 100%);
   display:flex;align-items:center;padding:0 0 0 64px;gap:28px}}
 .l{{width:440px;flex:none}}
 .brand{{display:flex;align-items:center;gap:14px;font-family:'Montserrat';font-weight:800;font-size:30px}}
 .brand img{{width:58px;height:58px;border-radius:14px;box-shadow:0 3px 10px rgba(36,39,43,.18)}}
 .badge{{display:inline-block;margin-top:30px;font-family:'Montserrat';font-weight:800;font-size:15px;letter-spacing:.08em;
   color:#6b5b50;background:#ece7e3;border:1px solid rgba(107,91,80,.25);padding:6px 14px;border-radius:999px}}
 h1{{font-family:'Montserrat';font-weight:800;font-size:56px;line-height:1.08;letter-spacing:-.01em;margin-top:16px}}
 p{{margin-top:18px;font-size:26px;line-height:1.35;color:#5d636c}}
 .btn{{display:inline-block;margin-top:34px;font-weight:700;font-size:24px;color:#fff;padding:14px 30px;border-radius:999px;
   background:linear-gradient(135deg,#7f9d94,#5e7c73 55%,#4f6b63);box-shadow:0 6px 16px rgba(79,107,99,.28)}}
 .r{{flex:1;height:630px;display:flex;align-items:flex-start;justify-content:center;padding-top:22px}}
 .r img{{height:640px}}
</style></head><body>
 <div class="l">
  <div class="brand"><img src="data:image/png;base64,{icon}">Pawfolio</div>
  <span class="badge">PAWFOLIO COMPLETE</span>
  <h1>Share doses with your sitter</h1>
  <p>Text one link. Your sitter taps Given, and you see who gave it.</p>
  <span class="btn">Watch how it works</span>
 </div>
 <div class="r"><img src="data:image/png;base64,{phones}"></div>
</body></html>"""
tmp = D / "_og_sitter_tmp.html"; tmp.write_text(HTML, encoding="utf-8")
with sync_playwright() as pw:
    b = pw.chromium.launch(); pg = b.new_page(viewport={"width": 1200, "height": 630})
    pg.goto(tmp.as_uri()); pg.wait_for_timeout(2500)
    pg.screenshot(path=str(D / "assets/og-pawfolio-sitter-sharing.png")); b.close()
tmp.unlink()
print("wrote og-pawfolio-sitter-sharing.png")
