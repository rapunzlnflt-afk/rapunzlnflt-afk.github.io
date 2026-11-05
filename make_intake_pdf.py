#!/usr/bin/env python3
"""Makes pet-sitter-intake-form/pet-sitter-intake-form-blank.pdf: the two-page
fillable blank version of the sitter intake form (Bricolage Grotesque + DM Sans).
Fonts are downloaded from Google Fonts into ~/.cache/ct-fonts on first run and
cut to static weights there. Needs reportlab and fonttools.
"""
import pathlib, urllib.request
from fontTools.ttLib import TTFont as FTFont
from fontTools.varLib import instancer
CACHE = pathlib.Path.home() / ".cache/ct-fonts"; CACHE.mkdir(parents=True, exist_ok=True)
SRC = {"bric": "https://github.com/google/fonts/raw/main/ofl/bricolagegrotesque/BricolageGrotesque%5Bopsz,wdth,wght%5D.ttf",
       "dm": "https://github.com/google/fonts/raw/main/ofl/dmsans/DMSans%5Bopsz,wght%5D.ttf"}
CUTS = [("bric", "Bric-Bold", {"wght": 700, "opsz": 36, "wdth": 100}), ("bric", "Bric-Semi", {"wght": 600, "opsz": 14, "wdth": 100}),
        ("dm", "DM-Reg", {"wght": 400, "opsz": 11}), ("dm", "DM-Med", {"wght": 500, "opsz": 11}), ("dm", "DM-Semi", {"wght": 600, "opsz": 11})]
for src, name, axes in CUTS:
    out = CACHE / f"{name}.ttf"
    if out.exists(): continue
    vf = CACHE / f"{src}-vf.ttf"
    if not vf.exists(): urllib.request.urlretrieve(SRC[src], vf)
    f = FTFont(vf); instancer.instantiateVariableFont(f, axes, inplace=True); f.save(out)
OUT = str(pathlib.Path(__file__).parent / "pet-sitter-intake-form" / "pet-sitter-intake-form-blank.pdf")
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, white, Color
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF
F=str(CACHE)+"/"
for n in ["Bric-Bold","Bric-Semi","DM-Reg","DM-Med","DM-Semi"]:
    pdfmetrics.registerFont(TTFont(n,F+n+".ttf"))
CH=HexColor("#24272b"); MUT=HexColor("#6a7078"); SAGE=HexColor("#5e7c73"); SOFT=HexColor("#edf2ef"); LINE=HexColor("#b9c0c7"); FILL=HexColor("#f6f8f7")
W,H=letter; M=40; CW=W-2*M
URL="https://cleartrackapps.com/pawfolio/?src=intake-pdf"
c=canvas.Canvas(OUT,pagesize=letter)
c.setTitle("New Client Pet Care Intake Form"); c.setAuthor("CleartrackApps"); c.setSubject("Free fillable intake form for pet sitters")
form=c.acroForm
fid=[0]
def tf(name,x,y,w,h,size=9.5,multi=False,font="Helvetica",tip=""):
    fid[0]+=1
    form.textfield(name=f"{name}_{fid[0]}",tooltip=tip or name,x=x,y=y,width=w,height=h,borderWidth=0,
        fillColor=Color(1,1,1,alpha=0),textColor=CH,fontName=font,fontSize=size,
        fieldFlags="multiline" if multi else "",forceBorder=False)
def fld(label,x,y,w,lines=1,lh=20,size=9.5):
    """label at top y; returns bottom y"""
    c.setFont("DM-Semi",7.2); c.setFillColor(MUT); c.drawString(x,y-7,label.upper() if False else label)
    top=y-10
    c.setStrokeColor(LINE); c.setLineWidth(.6)
    for i in range(lines):
        ly=top-lh*(i+1); c.line(x,ly,x+w,ly)
    tf(label,x,top-lh*lines+1.5,w,lh*lines-2,size=size,multi=lines>1,tip=label)
    return top-lh*lines
def row(y,items,gap=12):
    """items: list of (label, weight[, lines])"""
    tot=sum(i[1] for i in items); avail=CW-gap*(len(items)-1); x=M; bot=y
    for it in items:
        w=avail*it[1]/tot; lines=it[2] if len(it)>2 else 1
        bot=min(bot,fld(it[0],x,y,w,lines)); x+=w+gap
    return bot-5
def head(t,y,sub=None):
    c.setFillColor(SAGE); c.setFont("Bric-Semi",11.5); c.drawString(M,y-11,t)
    if sub:
        tw=pdfmetrics.stringWidth(t,"Bric-Semi",11.5)
        c.setFont("DM-Reg",7.8); c.setFillColor(MUT); c.drawString(M+tw+8,y-10.5,sub)
    c.setStrokeColor(SAGE); c.setLineWidth(1.1); c.line(M,y-16,M+CW,y-16)
    return y-22
def header(page):
    c.setFillColor(SAGE); c.rect(0,H-8,W,8,stroke=0,fill=1)
    # business block (left)
    y=H-34
    c.setFont("DM-Semi",7.2); c.setFillColor(MUT); c.drawString(M,y,"Pet sitter / business name")
    c.setStrokeColor(LINE); c.setLineWidth(.6); c.line(M,y-26,M+300,y-26)
    tf("Business name",M,y-25,300,22,size=16,font="Helvetica-Bold",tip="Your business name")
    if page==1:
        yy=y-36; x=M
        for lab,w in [("Phone",110),("Email or website",178)]:
            c.setFont("DM-Semi",7.2); c.setFillColor(MUT); c.drawString(x,yy,lab)
            c.line(x,yy-17,x+w,yy-17); tf("Sitter "+lab,x,yy-16,w,14,size=9,tip="Your "+lab.lower()); x+=w+12
    # title (right)
    c.setFillColor(CH); c.setFont("Bric-Bold",22 if page==1 else 18)
    t="New Client Intake" if page==1 else "Pet Details"
    c.drawRightString(M+CW,H-46,t)
    c.setFont("DM-Reg",8.5); c.setFillColor(MUT)
    c.drawRightString(M+CW,H-60,"Pet care information form" if page==1 else "One section per pet. Use another page for more pets.")
    if page==1:
        c.setFont("DM-Med",8); c.drawRightString(M+CW,H-80,"Client start date  ________________")
        tf("Start date",M+CW-78,H-82,78,12,size=8.5)
    return H-(98 if page==1 else 78)
def footer(n):
    c.setFont("DM-Reg",7); c.setFillColor(MUT)
    c.drawString(M,22,"Free intake form from cleartrackapps.com/pet-sitter-intake-form  ·  Fill in on screen or print and write by hand")
    c.drawRightString(M+CW,22,f"Page {n} of 2")

# PAGE 1
y=header(1)
y=head("Client",y)
y=row(y,[("Name(s)",1.4),("Mobile phone",.8),("Email",1.1)])
y=row(y,[("Home address",2.2),("Other phone",.8)])
y=head("Emergency contact",y,"Someone nearby who can make decisions if you can't be reached")
y=row(y,[("Name",1.3),("Relationship",.8),("Phone",.9),("Has a key?  Yes / No",.6)])
y=head("Veterinary care",y)
half=(CW-14)/2
def vet(x,title,y0):
    c.setFont("DM-Semi",8.5); c.setFillColor(CH); c.drawString(x,y0-9,title)
    yy=y0-12
    yy=fld("Clinic",x,yy,half)-4
    b1=fld("Phone",x,yy,half*.42); fld("Address",x+half*.42+10,yy,half*.58-10)
    return b1-4
vet(M,"Regular vet",y); y=vet(M+half+14,"Emergency / 24-hour vet",y)
y=head("Home and visits",y)
y=row(y,[("How to get in (key, lockbox, code)",1.5),("Alarm code",.75),("Wi-Fi network / password",1)])
y=row(y,[("Where supplies are kept (food, leash, litter, meds)",2),("Parking",1)])
y=row(y,[("Rooms or areas that are off-limits",1),("Extra requests (mail, plants, trash, lights)",1)])
y=row(y,[("Anything else I should know about the home",1,2)])
y=head("Emergency care authorization",y)
c.setFont("DM-Reg",8.6); c.setFillColor(CH)
lines=["If my pet needs urgent care and I can't be reached, I authorize my pet sitter to take my pet to my vet",
       "or the nearest emergency vet and approve treatment up to the amount below. I agree to pay for that care."]
for i,l in enumerate(lines): c.drawString(M,y-10-i*11.5,l)
y-=30
y=row(y,[("Approved amount ($)",.6),("Client signature",1.6),("Date",.6)])
# Pawfolio box
bh=74; by=40
c.setFillColor(SOFT); c.setStrokeColor(HexColor("#c7d6cf")); c.setLineWidth(.8)
c.roundRect(M,by,CW,bh,8,stroke=1,fill=1)
qr=QrCodeWidget(URL); b=qr.getBounds(); s=58; d=Drawing(s,s,transform=[s/(b[2]-b[0]),0,0,s/(b[3]-b[1]),0,0]); d.add(qr)
c.setFillColor(white); c.roundRect(M+8,by+8,58,58,4,stroke=0,fill=1); renderPDF.draw(d,c,M+8,by+8)
tx=M+78
c.setFillColor(SAGE); c.setFont("Bric-Semi",11); c.drawString(tx,by+bh-18,"Does your pet take medication? Try Pawfolio.")
c.setFillColor(CH); c.setFont("DM-Reg",8.3)
for i,l in enumerate(["Pawfolio Free keeps your pet's profiles, medications and sitter info on your phone and reminds you when",
                      "doses are due. With Pawfolio Complete, you can share doses with your sitter, so you both see each dose given."]):
    c.drawString(tx,by+bh-32-i*11,l)
c.setFont("DM-Semi",8.3); c.drawString(tx,by+12,"Scan the code or visit cleartrackapps.com/pawfolio")
footer(1); c.showPage()

# PAGE 2
y=header(2)
def pet(y,n):
    y=head(f"Pet {n}",y)
    # photo circle
    r=33; cx=M+r; cy=y-r-4
    c.setStrokeColor(LINE); c.setDash(2,2); c.setLineWidth(.8); c.circle(cx,cy,r); c.setDash()
    c.setFont("DM-Reg",7); c.setFillColor(MUT); c.drawCentredString(cx,cy-2.5,"Photo (optional)")
    x0=M+2*r+14; w=CW-(x0-M)
    def subrow(y,items,gap=10):
        tot=sum(i[1] for i in items); avail=w-gap*(len(items)-1); x=x0; bot=y
        for lab,wt in items:
            ww=avail*wt/tot; bot=min(bot,fld(lab,x,y,ww)); x+=ww+gap
        return bot-4
    y=subrow(y,[("Name",1.1),("Species and breed",1.4),("Age",.5),("Weight",.5)])
    y=subrow(y,[("Sex / spayed or neutered",1),("Color and markings",1.4),("Microchip number",1.1)])
    y=min(y,cy-r-8)
    y=row(y,[("Feeding (food, amount, times)",1.6),("Treats allowed?",.6)])
    # med table
    c.setFont("DM-Semi",7.2); c.setFillColor(MUT); c.drawString(M,y-7,"Medications and supplements")
    cols=[("Name",1.3),("Dose",.7),("Time(s)",.8),("How it's given (with food, in a treat)",1.6)]
    tot=sum(x[1] for x in cols); gap=10; avail=CW-gap*3
    yy=y-12; x=M
    c.setFillColor(FILL); c.rect(M,yy-12,CW,12,stroke=0,fill=1)
    for lab,wt in cols:
        c.setFont("DM-Med",7); c.setFillColor(CH); c.drawString(x+2,yy-8.5,lab); x+=avail*wt/tot+gap
    yy-=12
    for r_ in range(3):
        x=M
        for lab,wt in cols:
            ww=avail*wt/tot
            c.setStrokeColor(LINE); c.setLineWidth(.6); c.line(x,yy-19,x+ww,yy-19)
            tf(f"Pet {n} med {r_+1} {lab}",x,yy-18,ww,16,size=8.5); x+=ww+gap
        yy-=19
    y=yy-6
    y=row(y,[("Allergies or health conditions",1,2),("Walks and exercise",1,2)])
    y=row(y,[("Behavior (strangers, other pets, escape risk, fears)",1,2),("Other notes and routines",1,2)])
    return y
y=pet(y,1); y-=2; y=pet(y,2)
footer(2)
c.save()
print("wrote", OUT)
