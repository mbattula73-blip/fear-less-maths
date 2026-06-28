"""Fear Less Maths — PDF Engine (B&W, 2 pages, footer on p2 only)"""
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.pdfbase.pdfmetrics import stringWidth
import os, tempfile
from io import BytesIO
from content import get_questions

def _wrap(text, font, size, maxw):
    """Greedy word-wrap text to fit maxw, using stringWidth (no canvas needed)."""
    words=text.split(); lines=[]; line=""
    for w in words:
        test=(line+" "+w).strip()
        if stringWidth(test,font,size)<=maxw or not line:
            line=test
        else:
            lines.append(line); line=w
    if line: lines.append(line)
    return lines or [""]


# Re-import level metadata
from levels_data import get_tier, LEVELS, SUBLEVELS

LOGO = os.path.join(os.path.dirname(__file__), "assets", "logo.jpeg")
PW,PH=A4; ML=12*mm; MR=12*mm; MT=10*mm; MB=10*mm
SW=36*mm; BW=PW-ML-MR-SW; CW=BW/2
LX=ML; RX=ML+CW; SX=ML+BW
HDR_H=36*mm; FTR_H=10*mm
P1_TOP=PH-MT-HDR_H-1*mm; P1_BOT=MB+2*mm
P2_TOP=PH-MT-2*mm;        P2_BOT=MB+FTR_H+1*mm
BLACK=colors.black; WHITE=colors.white
LGRAY=colors.HexColor("#AAAAAA"); MGRAY=colors.HexColor("#555555")
_TEMP=[]

def _diag(dtype,dpar):
    if not dtype: return None
    try:
        from diagram_engine import generate_diagram
        buf=generate_diagram(dtype,dpar)
        if not buf: return None
        buf.seek(0)
        f=tempfile.NamedTemporaryFile(suffix='.png',delete=False)
        f.write(buf.read()); f.close(); _TEMP.append(f.name); return f.name
    except: return None

def _clean():
    for p in _TEMP:
        try: os.unlink(p)
        except: pass
    _TEMP.clear()

def _outer(c):
    c.setStrokeColor(BLACK); c.setLineWidth(1.2)
    c.rect(ML,MB,PW-ML-MR,PH-MT-MB)

def _header(c,ws_id,tier,topic,lvl):
    hx=ML; hy=PH-MT-HDR_H; hw=BW
    c.setFillColor(WHITE); c.setStrokeColor(BLACK); c.setLineWidth(0.6)
    c.rect(hx,hy,hw+SW,HDR_H,fill=1,stroke=1)
    c.setLineWidth(0.8); c.line(ML,hy,ML+BW+SW,hy)
    # Date
    c.setFont("Helvetica",7.5); c.setFillColor(BLACK)
    c.drawRightString(ML+BW-2*mm,PH-MT-3.5*mm,"Date: _________ / _________ / _________")
    # Logo
    if os.path.exists(LOGO):
        try: c.drawImage(LOGO,ML+2*mm,hy+HDR_H-4.5*mm-10*mm,width=22*mm,height=10*mm,preserveAspectRatio=True,mask='auto')
        except: pass
    cx=ML+BW/2
    c.setFont("Helvetica-Bold",12); c.setFillColor(BLACK)
    c.drawCentredString(cx,PH-MT-9*mm,"LA Excellence SCHOOLS  /  IDPS ORCHARDS")
    c.setFont("Helvetica",7); c.setFillColor(MGRAY)
    c.drawCentredString(cx,PH-MT-14*mm,f"Level {lvl} — {LEVELS.get(lvl,{}).get('name','')}  |  {topic}  |  {tier}")
    c.setFont("Helvetica-Bold",10); c.setFillColor(BLACK)
    c.drawCentredString(cx,PH-MT-19.5*mm,f"Worksheet  No:  {ws_id}")
    c.setFont("Helvetica",8.5); c.setFillColor(BLACK)
    c.drawString(ML+2*mm,PH-MT-25.5*mm,"Name of the Student:  _____________________________   Class: ___________")
    c.drawString(ML+2*mm,PH-MT-31*mm,  "Name of the Mentor:    _____________________________   Group: ___________")

def _sidebar(c,top_y,bot_y,page=1):
    c.setFillColor(WHITE); c.setStrokeColor(BLACK); c.setLineWidth(0.6)
    c.rect(SX,bot_y,SW,top_y-bot_y,fill=1,stroke=1)
    y=top_y-3.5*mm
    if page==1:
        c.setFont("Helvetica-Bold",9); c.setFillColor(BLACK)
        c.drawCentredString(SX+SW/2,y,"GRADE"); y-=3.5*mm
        c.setStrokeColor(BLACK); c.setLineWidth(0.4)
        c.line(SX+2*mm,y,SX+SW-2*mm,y); y-=1.5*mm
        bw=(SW-7*mm)/2; bh=6.5*mm
        for i,ltr in enumerate(["A","B","C","D"]):
            col_=i%2; row_=i//2
            bx=SX+2*mm+col_*(bw+1.5*mm); by=y-row_*(bh+2*mm)-bh
            c.setFillColor(WHITE); c.setStrokeColor(BLACK); c.setLineWidth(0.5)
            c.rect(bx,by,bw,bh,fill=1,stroke=1)
            c.setFont("Helvetica-Bold",10); c.setFillColor(BLACK)
            c.drawCentredString(bx+bw/2,by+1.5*mm,ltr)
        y-=2*(bh+2*mm)+5*mm
        c.setStrokeColor(BLACK); c.setLineWidth(0.3)
        c.line(SX+2*mm,y,SX+SW-2*mm,y); y-=5*mm
    ms_top=y; ms_bot=bot_y+2*mm
    c.setFillColor(WHITE); c.setStrokeColor(BLACK); c.setLineWidth(0.5)
    c.rect(SX+2*mm,ms_bot,SW-4*mm,ms_top-ms_bot,fill=1,stroke=1)
    lbl_y=ms_top-(ms_top-ms_bot)/2-2*mm
    c.setFont("Helvetica-Bold",8); c.setFillColor(BLACK)
    c.drawCentredString(SX+SW/2,lbl_y+4*mm,"MENTOR")
    c.drawCentredString(SX+SW/2,lbl_y,"SPACE")

def _divider(c,top_y,bot_y):
    c.setStrokeColor(LGRAY); c.setLineWidth(0.3); c.setDash(3,3)
    c.line(RX,bot_y,RX,top_y); c.setDash()

def _rough_work(c,col,min_space=14*mm):
    """Fill remaining space in a column with a 'rough work' ruled box, if enough room."""
    avail=col.y-col.bot
    if avail<min_space: return
    x=col.x; cw=col.cw
    c.setStrokeColor(LGRAY); c.setLineWidth(0.5)
    c.line(x-1*mm,col.y,x-1*mm+cw+1*mm,col.y)
    col.y-=5*mm
    c.setFont("Helvetica-Oblique",10); c.setFillColor(MGRAY)
    c.drawString(x,col.y,"Use this space for rough work")
    col.y-=6*mm
    c.setDash(1,2); c.setStrokeColor(LGRAY); c.setLineWidth(0.4)
    while col.y-4.5*mm>=col.bot:
        c.line(x,col.y,x+cw-2*mm,col.y)
        col.y-=4.5*mm
    c.setDash()

def _footer_p2(c):
    c.setFillColor(WHITE); c.setStrokeColor(BLACK); c.setLineWidth(0.5)
    c.rect(ML,MB,BW,FTR_H,fill=1,stroke=1)
    c.setFont("Helvetica-Bold",8); c.setFillColor(BLACK)
    c.drawString(ML+3*mm,MB+3.5*mm,"Teacher's Comment: _________________________________________________")
    c.setFillColor(WHITE); c.rect(SX,MB,SW,FTR_H,fill=1,stroke=1)
    c.setFont("Helvetica-Bold",7); c.setFillColor(BLACK)
    c.drawCentredString(SX+SW/2,MB+5*mm,"Parent")
    c.drawCentredString(SX+SW/2,MB+1.5*mm,"Signature:")

def _est(item, cw=None):
    if item.get("type")=="concept_box":
        title=item.get("section_title",""); bullets=item.get("section_bullets",[]); example=item.get("example","")
        avail=(cw or 60*mm)-4*mm
        n_lines=0
        for b in bullets:
            n_lines+=len(_wrap(f"\u2022 {b}","Helvetica",12,avail))
        ex_lines=0
        if example:
            ex_lines=len(_wrap(f"e.g. {example}","Helvetica-Oblique",12,avail))
        h=4*mm+n_lines*4.5*mm+ex_lines*4.5*mm+5*mm
        if item.get("icon_diagram"):
            h=max(h, 24*mm)
        return h
    if item.get("type")=="tips_box":
        tips=item.get("tips",[])
        avail=(cw or 60*mm)-4*mm
        n_lines=0
        for t in tips:
            n_lines+=len(_wrap(f"\u27a4 {t}","Helvetica",12,avail))
        return 6*mm+n_lines*4.5*mm+4*mm
    big_diag = item.get("diagram_type") in ("base10_blocks", "compare_blocks",
                                             "vertical_numberline_blank", "vertical_numberline_example")
    diag_h = (34*mm if big_diag else 20*mm) if item.get("diagram_type") else 0
    text = item.get("text", "")
    avail_text = max((cw or 60*mm) - 10*mm, 20*mm)
    n_lines = max(2, len(_wrap(text, "Helvetica", 12, avail_text))) if text else 2
    text_h = n_lines * 4.5*mm
    return 2*mm+text_h+diag_h+4.5*mm+(3.5*mm if item.get("diagram_type") else 10.5*mm)

class Col:
    def __init__(self,c,x,cw,top,bot):
        self.c=c; self.x=x+1*mm; self.cw=cw-3*mm; self.y=top; self.bot=bot
    def fits(self,item): return self.y-_est(item,self.cw)>=self.bot
    def render(self,item):
        if not self.fits(item): return False
        if item.get("type")=="concept_box": self._cb(item)
        elif item.get("type")=="tips_box": self._tb(item)
        else: self._q(item)
        return True
    def _cb(self,item):
        c=self.c; x=self.x; cw=self.cw
        title=item.get("section_title",""); bullets=item.get("section_bullets",[]); example=item.get("example","")
        icon_dtype=item.get("icon_diagram"); icon_dparm=item.get("icon_params",{})
        self.y-=3.5*mm
        bh=_est(item,cw)-3.5*mm
        c.setFillColor(colors.HexColor("#F5F5F5")); c.setStrokeColor(BLACK); c.setLineWidth(0)
        c.rect(x-1*mm,self.y-bh+1*mm,cw+1*mm,bh,fill=1,stroke=0)
        c.setStrokeColor(BLACK); c.setLineWidth(1.5)
        c.line(x-1*mm,self.y-bh+1*mm,x-1*mm,self.y+1*mm); c.setLineWidth(0.3)
        icon_w = 0
        if icon_dtype:
            path=_diag(icon_dtype,icon_dparm)
            if path:
                try:
                    ih=20*mm; iw=ih*1.45
                    c.drawImage(path,x+cw-iw,self.y-ih+2*mm,width=iw,height=ih,preserveAspectRatio=True,mask='auto')
                    icon_w = iw + 2*mm
                except: pass
        c.setFont("Helvetica-Bold",12); c.setFillColor(BLACK)
        c.drawString(x,self.y,title[:52]); self.y-=4.5*mm
        avail=cw-4*mm-icon_w
        for b in bullets:
            c.setFont("Helvetica",12); c.setFillColor(BLACK)
            for ln in _wrap(f"\u2022 {b}","Helvetica",12,avail):
                c.drawString(x+1.5*mm,self.y,ln); self.y-=4.5*mm
        if example:
            c.setFont("Helvetica-Oblique",12); c.setFillColor(MGRAY)
            for ln in _wrap(f"e.g. {example}","Helvetica-Oblique",12,avail):
                c.drawString(x+2*mm,self.y,ln); self.y-=4.5*mm
        self.y-=2*mm
    def _tb(self,item):
        """Render a tips box — compact, with lightblue background."""
        c=self.c; x=self.x; cw=self.cw
        title=item.get("section_title","Tips"); tips=item.get("tips",[])
        self.y-=3*mm
        bh=_est(item,cw)-3*mm
        c.setFillColor(colors.HexColor("#E8F4FD")); c.setStrokeColor(colors.HexColor("#2196F3")); c.setLineWidth(1.2)
        c.rect(x-1*mm,self.y-bh+1*mm,cw+1*mm,bh,fill=1,stroke=1)
        c.setFont("Helvetica-Bold",12); c.setFillColor(colors.HexColor("#1565C0"))
        c.drawString(x+1*mm,self.y,f"\u2605 {title}"); self.y-=4.5*mm
        avail=cw-4*mm
        for tip in tips:
            c.setFont("Helvetica",12); c.setFillColor(BLACK)
            for ln in _wrap(f"\u27a4 {tip}","Helvetica",12,avail):
                c.drawString(x+2*mm,self.y,ln); self.y-=4.5*mm
        self.y-=2*mm

    def _q(self,item):
        c=self.c; x=self.x; cw=self.cw
        num=item.get("_num","?"); text=item.get("text",""); bph=item.get("bold_phrase","")
        albl=item.get("answer_label","Answer = ____"); dtype=item.get("diagram_type"); dparm=item.get("diagram_params",{})
        if len(text)>220: text=text[:215]+"..."
        self.y-=2.5*mm
        sz=12; c.setFont("Helvetica-Bold",sz); c.setFillColor(BLACK)
        ns=f"{num}."; nw=c.stringWidth(ns,"Helvetica-Bold",sz)+1.5*mm; c.drawString(x,self.y,ns)
        tx=x+nw; avail=cw-nw; lh=sz*1.45
        if bph and bph in text:
            bef,_,aft=text.partition(bph)
            c.setFont("Helvetica",sz); bw=c.stringWidth(bef,"Helvetica",sz); c.drawString(tx,self.y,bef); tx+=bw
            c.setFont("Helvetica-Bold",sz); pw_=c.stringWidth(bph,"Helvetica-Bold",sz)
            if tx+pw_>x+cw: self.y-=lh; tx=x+nw
            c.drawString(tx,self.y,bph); tx+=pw_
            c.setFont("Helvetica",sz)
            if tx+c.stringWidth(aft,"Helvetica",sz)>x+cw: self.y-=lh; tx=x+nw
            c.drawString(tx,self.y,aft[:55])
        else:
            words=text.split(); line=""; c.setFont("Helvetica",sz); c.setFillColor(BLACK); tx2=tx
            for w in words:
                test=(line+" "+w).strip()
                if c.stringWidth(test,"Helvetica",sz)<=avail: line=test
                else:
                    if line: c.drawString(tx2,self.y,line)
                    self.y-=lh; line=w; tx2=x+nw
            if line: c.drawString(tx2,self.y,line)
        self.y-=lh+1.5*mm
        if dtype:
            path=_diag(dtype,dparm)
            if path:
                try:
                    big_diag = dtype in ("base10_blocks", "compare_blocks",
                                          "vertical_numberline_blank", "vertical_numberline_example")
                    iw=min(cw-3*mm, 78*mm if big_diag else 68*mm)
                    ih=32*mm if big_diag else 18*mm
                    c.drawImage(path,x+1.5*mm,self.y-ih,width=iw,height=ih,preserveAspectRatio=True,mask='auto')
                    self.y-=ih+1.5*mm
                except: pass
        c.setFont("Helvetica-Bold",12); c.setFillColor(BLACK); c.drawString(x+1.5*mm,self.y,albl); self.y-=4*mm
        n_lines=1 if dtype else 3; c.setFont("Helvetica",4.5); c.setFillColor(LGRAY)
        du=c.stringWidth(". ","Helvetica",4.5); ds=". "*int(cw/max(du,0.1))
        for _ in range(n_lines): c.drawString(x,self.y,ds); self.y-=3.5*mm

def _concept_page(c, concept_items, ws_id, tier, topic, level_num, sublevel_code_for_enrich=None):
    """Render Page 3: concept boxes and tips as a reference/answer guide page."""
    _outer(c)
    # Simplified header for concept page
    hx=ML; hy=PH-MT-HDR_H; hw=BW
    c.setFillColor(WHITE); c.setStrokeColor(BLACK); c.setLineWidth(0.6)
    c.rect(hx,hy,hw+SW,HDR_H,fill=1,stroke=1)
    c.setLineWidth(0.8); c.line(ML,hy,ML+BW+SW,hy)
    if os.path.exists(LOGO):
        try: c.drawImage(LOGO,ML+2*mm,hy+HDR_H-4.5*mm-10*mm,width=22*mm,height=10*mm,preserveAspectRatio=True,mask='auto')
        except: pass
    cx=ML+BW/2
    c.setFont("Helvetica-Bold",12); c.setFillColor(BLACK)
    c.drawCentredString(cx,PH-MT-9*mm,"LA Excellence SCHOOLS  /  IDPS ORCHARDS")
    c.setFont("Helvetica",7); c.setFillColor(MGRAY)
    c.drawCentredString(cx,PH-MT-14*mm,f"Level {level_num}  |  {topic}  |  {tier}")
    c.setFont("Helvetica-Bold",10); c.setFillColor(BLACK)
    c.drawCentredString(cx,PH-MT-19.5*mm,f"Worksheet  {ws_id}  —  Concept & Tips")
    c.setFont("Helvetica-Oblique",8); c.setFillColor(MGRAY)
    c.drawCentredString(cx,PH-MT-26*mm,"Read and understand — then attempt the worksheet questions without looking here.")
    _sidebar(c,P1_TOP,P1_BOT,page=1)
    _divider(c,P1_TOP,P1_BOT)
    rl=Col(c,LX,CW,P1_TOP,P1_BOT); rr=Col(c,RX,CW,P1_TOP,P1_BOT)
    overflow=[]
    for item in concept_items:
        if not rl.render(item): overflow.append(item)
    for item in overflow: rr.render(item)
    # --- Enrichment blocks (worked example, formula card, reference table) ---
    try:
        from tips_enrichment import get_enrichment
        blocks=get_enrichment(sublevel_code_for_enrich, level_num, topic)
        if blocks:
            # First block(s) fill the right column top; remaining stack in left
            # column under the tips box. This balances both columns.
            lx=LX; rx=RX; ew=CW
            ly=rl.y-2*mm           # below tips (left column)
            ry=P1_TOP-2*mm         # right column top
            # Heuristic: put the reference table (last block) on the right,
            # the visual cards on the left under the tips.
            *left_blocks, table_block = blocks if len(blocks)>1 else (blocks+[None])
            for blk in left_blocks:
                if blk and ly > P1_BOT+22*mm:
                    ly=blk(c,lx,ly,ew)
            if table_block and ry > P1_BOT+30*mm:
                ry=table_block(c,rx,ry,ew)
    except Exception:
        pass

def build_pdf(level_num:int, sublevel_code:str, sheet_num:str)->BytesIO:
    ws_id=f"{sublevel_code}-{sheet_num}"; tier=get_tier(sheet_num)
    topic=dict(SUBLEVELS.get(level_num,[])).get(sublevel_code,"")
    raw=get_questions(sublevel_code,sheet_num,level_num)

    # Decide whether a RICH concept page will be added (sheet 1 + spec exists)
    # BEFORE deciding what to do with inline concept/tips boxes, so we only
    # ever pull them off the worksheet when something is actually replacing
    # them -- otherwise every worked-example/instructions box stays inline
    # on the worksheet itself, exactly like Levels 1-6.
    rich_spec = None
    if str(sheet_num) == "1":
        try:
            from concept_pages import get_concept_page
            rich_spec = get_concept_page(sublevel_code, level_num, topic)
        except Exception:
            rich_spec = None

    # Worked-example/instructions boxes ALWAYS stay inline on the worksheet
    # itself, on every sheet -- never pulled onto a separate page. The rich
    # "Concept & Tips" page (sheet 1 only, when an existing spec is found)
    # is an ADDITIONAL bonus page, not a replacement for the inline boxes.
    concept_items = []
    questions     = raw

    n=0
    for item in questions:
        if item.get("type") not in ("concept_box", "tips_box"):
            n+=1; item["_num"]=n

    buf=BytesIO(); c=canvas.Canvas(buf,pagesize=A4)
    # Page 1 — questions only (when rich page will replace concept) or mixed
    _outer(c); _header(c,ws_id,tier,topic,level_num)
    _sidebar(c,P1_TOP,P1_BOT,page=1); _divider(c,P1_TOP,P1_BOT)
    rl=Col(c,LX,CW,P1_TOP,P1_BOT); rr=Col(c,RX,CW,P1_TOP,P1_BOT)
    p2=[]
    for item in questions:
        if not rl.render(item): p2.append(item)
    p3=[]
    for item in p2:
        if not rr.render(item): p3.append(item)
    c.showPage()
    # Page 2
    _outer(c); _sidebar(c,P2_TOP,P2_BOT,page=2); _divider(c,P2_TOP,P2_BOT); _footer_p2(c)
    rl2=Col(c,LX,CW,P2_TOP,P2_BOT); rr2=Col(c,RX,CW,P2_TOP,P2_BOT)
    p4=[]
    for item in p3:
        if not rl2.render(item): p4.append(item)
    for item in p4: rr2.render(item)
    _rough_work(c,rl2); _rough_work(c,rr2)

    # Page 3 — concept & tips (Level 7+). Skipped when the rich concept page
    # will be shown (it replaces this), to avoid a redundant page.
    if level_num >= 7 and concept_items and rich_spec is None:
        c.showPage()
        _concept_page(c, concept_items, ws_id, tier, topic, level_num,
                      sublevel_code_for_enrich=(sublevel_code if str(sheet_num)=="3" else None))

    # RICH concept page — only on sheet 1 of a sublevel (becomes page 3).
    if rich_spec is not None:
        try:
            from concept_pages import render_rich_concept_page
            spec = rich_spec
            c.showPage()
            _outer(c)
            # Clean concept-page header (no grade sidebar; full width)
            cx=ML+(PW-ML-MR)/2
            c.setFont("Helvetica-Bold",12); c.setFillColor(BLACK)
            c.drawCentredString(cx,PH-MT-7*mm,"LA Excellence SCHOOLS  /  IDPS ORCHARDS")
            c.setFont("Helvetica",7.5); c.setFillColor(MGRAY)
            c.drawCentredString(cx,PH-MT-11.5*mm,
                f"Level {level_num} — {LEVELS.get(level_num,{}).get('name','')}  |  {topic}")
            c.setFont("Helvetica-Bold",12); c.setFillColor(colors.HexColor('#1565C0'))
            c.drawCentredString(cx,PH-MT-17.5*mm,"CONCEPT  &  TIPS  \u2014  Study Sheet")
            # Worksheet / sublevel number (so it's clear which sublevel this belongs to)
            c.setFont("Helvetica-Bold",9); c.setFillColor(BLACK)
            c.drawRightString(PW-MR-1*mm,PH-MT-7*mm,f"Worksheet:  {ws_id}")
            c.setStrokeColor(BLACK); c.setLineWidth(0.8)
            c.line(ML,PH-MT-20*mm,PW-MR,PH-MT-20*mm)
            frame = {
                "ML":ML,"MR":MR,"MT":MT,"MB":MB,"PW":PW,"PH":PH,
                "BW":PW-ML-MR,"CW":(PW-ML-MR)/2-2*mm,
                "LX":ML,"RX":ML+(PW-ML-MR)/2+2*mm,"SX":SX,"SW":SW,
                "P_TOP":PH-MT-22*mm,"P_BOT":MB+2*mm,
            }
            render_rich_concept_page(c, spec, frame)
        except Exception:
            pass
    c.save(); _clean(); buf.seek(0); return buf
