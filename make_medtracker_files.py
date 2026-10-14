#!/usr/bin/env python3
"""Makes the /medication-tracker/ downloads from the pet chart's ready-made
files: the chart itself is the same, so this covers the Pawfolio box and the
footer line and draws the MedRecords box (with its QR code) in their place.
Needs pypdf, reportlab, openpyxl and segno. Run after build_medtracker.py."""
import io, pathlib
import segno
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import ImageReader
import openpyxl

ROOT = pathlib.Path(__file__).parent
SRC, OUT = ROOT / "pet-medication-chart", ROOT / "medication-tracker"
QR_URL = "https://cleartrackapps.com/go/medrecords-app/?src=medtracker-print"
FONTS = pathlib.Path("/usr/share/fonts/truetype/lato")
for n in ("Lato-Regular", "Lato-Bold"):
    pdfmetrics.registerFont(TTFont(n, str(FONTS / f"{n}.ttf")))

def overlay():
    qr = io.BytesIO(); segno.make(QR_URL, error="m").save(qr, kind="png", scale=10, dark="#2b2723", border=1); qr.seek(0)
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(792, 612))
    c.setFillColorRGB(1, 1, 1); c.setStrokeColorRGB(1, 1, 1)
    c.rect(348, 60, 428, 84, stroke=0, fill=1)      # old Pawfolio box
    c.rect(18, 70, 300, 18, stroke=0, fill=1)       # old footer line
    c.setFillColorRGB(241/255, 247/255, 247/255); c.setStrokeColorRGB(164/255, 186/255, 189/255); c.setLineWidth(1)
    c.roundRect(355.5, 67.5, 412.5, 68.5, 5, stroke=1, fill=1)
    c.drawImage(ImageReader(qr), 362, 74, 56, 56)
    c.setFillColor("#12676e"); c.setFont("Lato-Bold", 10.5); c.drawString(426, 116, "Get dose reminders on your phone with MedRecords.")
    c.setFillColor("#4a4a4a"); c.setFont("Lato-Regular", 8.6); c.drawString(426, 101, "Tap Taken or Skip, keep a dose history, and bring it to the doctor.")
    c.setFillColor("#2b2723"); c.setFont("Lato-Bold", 8.6); c.drawString(426, 86, "Scan the code to try it free")
    c.setFillColor("#4a4a4a"); c.drawString(24, 76, "Free chart from cleartrackapps.com/medication-tracker")
    c.save(); buf.seek(0); return PdfReader(buf).pages[0]

DROP = ("Pawfolio", "pet-medication-chart", "Scan the code or visit")

def strip_old_text(w, page):
    """Remove the old Pawfolio box / footer text blocks, so it can't be copied or found."""
    from pypdf.generic import ContentStream, NameObject
    cs = ContentStream(page.get_contents(), w)
    out, block, keep = [], [], True
    for operands, op in cs.operations:
        if op == b"BT":
            block, keep = [(operands, op)], True; continue
        if block:
            block.append((operands, op))
            if op in (b"Tj", b"TJ"):
                raw = operands[0]
                txt = "".join(str(x) for x in raw) if op == b"TJ" else str(raw)
                if any(d in txt for d in DROP): keep = False
            if op == b"ET":
                if keep: out.extend(block)
                block = []
            continue
        out.append((operands, op))
    cs.operations = out
    page[NameObject("/Contents")] = w._add_object(cs)

def pdf(src, dst):
    w = PdfWriter(clone_from=str(SRC / src))
    strip_old_text(w, w.pages[0])
    w.pages[0].merge_page(overlay(), over=True)
    w.add_metadata({"/Title": "Weekly Medication Tracker", "/Author": "CleartrackApps"})
    with open(OUT / dst, "wb") as f: w.write(f)

def xlsx():
    wb = openpyxl.load_workbook(SRC / "pet-medication-chart.xlsx")
    for ws in wb:
        for row in ws.iter_rows():
            for c in row:
                v = c.value
                if not isinstance(v, str): continue
                if v.startswith("Get free dose reminders"):
                    c.value = "Get dose reminders on your phone with MedRecords. Tap Taken or Skip, keep a dose history, and bring it to the doctor."
                elif v == "cleartrackapps.com/pawfolio":
                    c.value = "cleartrackapps.com/go/medrecords-app"
                    c.hyperlink = "https://cleartrackapps.com/go/medrecords-app/?src=medtracker-xlsx"
                elif "pet-medication-chart" in v:
                    c.value = v.replace("pet-medication-chart", "medication-tracker")
    wb.properties.title = "Weekly Medication Tracker"
    wb.save(OUT / "medication-tracker.xlsx")

if __name__ == "__main__":
    pdf("pet-medication-chart.pdf", "medication-tracker.pdf")
    pdf("pet-medication-chart-fillable.pdf", "medication-tracker-fillable.pdf")
    xlsx()
    print("wrote downloads into", OUT)
