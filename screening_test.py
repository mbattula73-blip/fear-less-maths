"""
Fear Less Maths — FLM Screening Test Assembler.

Builds a class-readiness diagnostic worksheet by pulling REAL, already-verified
questions from specific FLM sublevels (not new content) and assembling them
into a single screening paper, using the exact same rendering engine, header,
and format as every other FLM worksheet.

This directly answers "does this student need FLM, and if so where" for a
given class, by testing the exact prerequisite sublevels that class's
students should already have secured (per the Class-By-Class Support Schema).
"""
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

import pdf_engine as pe
from content import get_questions


def _screening_header(c, ws_id, tier, topic):
    """Same visual header as a normal worksheet, but the subtitle line
    reads the screening topic directly instead of 'Level N - <name>',
    since a screening test deliberately spans multiple FLM levels."""
    from reportlab.lib.units import mm
    hx = pe.ML; hy = pe.PH - pe.MT - pe.HDR_H; hw = pe.BW
    c.setFillColor(pe.WHITE); c.setStrokeColor(pe.BLACK); c.setLineWidth(0.6)
    c.rect(hx, hy, hw + pe.SW, pe.HDR_H, fill=1, stroke=1)
    c.setLineWidth(0.8); c.line(pe.ML, hy, pe.ML + pe.BW + pe.SW, hy)
    c.setFont("Helvetica", 7.5); c.setFillColor(pe.BLACK)
    c.drawRightString(pe.ML + pe.BW - 2*mm, pe.PH - pe.MT - 3.5*mm,
                       "Date: _________ / _________ / _________")
    if __import__("os").path.exists(pe.LOGO):
        try:
            c.drawImage(pe.LOGO, pe.ML + 2*mm, hy + pe.HDR_H - 4.5*mm - 10*mm,
                        width=22*mm, height=10*mm, preserveAspectRatio=True, mask='auto')
        except Exception:
            pass
    cx = pe.ML + pe.BW / 2
    c.setFont("Helvetica-Bold", 12); c.setFillColor(pe.BLACK)
    c.drawCentredString(cx, pe.PH - pe.MT - 9*mm, "LA Excellence SCHOOLS  /  IDPS ORCHARDS")
    c.setFont("Helvetica", 7); c.setFillColor(pe.MGRAY)
    c.drawCentredString(cx, pe.PH - pe.MT - 14*mm, f"{topic}  |  {tier}")
    c.setFont("Helvetica-Bold", 10); c.setFillColor(pe.BLACK)
    c.drawCentredString(cx, pe.PH - pe.MT - 19.5*mm, f"Screening Test:  {ws_id}")
    c.setFont("Helvetica", 8.5); c.setFillColor(pe.BLACK)
    c.drawString(pe.ML + 2*mm, pe.PH - pe.MT - 25.5*mm,
                 "Name of the Student:  _____________________________   Class: ___________")
    c.drawString(pe.ML + 2*mm, pe.PH - pe.MT - 31*mm,
                 "Name of the Mentor:    _____________________________   Group: ___________")


def _has_real_content(sublevel_code, sheet_num, level_num):
    """Guards against silently including a 'Coming Soon' placeholder
    question in a screening test -- returns False if this sublevel/sheet
    has no real hand-crafted content yet."""
    try:
        items = get_questions(sublevel_code, sheet_num, level_num)
    except Exception:
        return False
    if not items:
        return False
    first = items[0]
    return not str(first.get("section_title", "")).endswith("(Coming Soon)")


def build_screening_pdf(class_label: str, sources: list, title_suffix: str = "") -> BytesIO:
    """
    sources: list of (sublevel_code, sheet_num, level_num, n_questions) tuples
             specifying exactly which real questions to pull for this screen.
    Any source whose content isn't built yet is silently skipped (never
    renders a placeholder), and the caller can inspect .skipped afterward
    via build_screening_pdf_with_report() for an honest coverage log.
    Returns a BytesIO PDF, same visual format as a normal FLM worksheet.
    """
    return build_screening_pdf_with_report(class_label, sources, title_suffix)[0]


def build_screening_pdf_with_report(class_label: str, sources: list, title_suffix: str = ""):
    """Same as build_screening_pdf, but also returns a coverage report:
    (pdf_bytes, {"used": [...], "skipped": [...], "total_questions": n})."""
    ws_id = f"SCREEN-{class_label}{title_suffix}"
    topic = f"Class {class_label} — FLM Readiness Screening (Comprehensive)"
    tier = "Diagnostic"

    questions = []
    used, skipped = [], []
    for sublevel_code, sheet_num, level_num, n in sources:
        if not _has_real_content(sublevel_code, sheet_num, level_num):
            skipped.append(sublevel_code)
            continue
        raw = get_questions(sublevel_code, sheet_num, level_num)
        picked = [it for it in raw if it.get("type") not in ("concept_box", "tips_box")][:n]
        questions.extend(picked)
        used.append(sublevel_code)

    n = 0
    for item in questions:
        n += 1
        item["_num"] = n

    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)

    def _new_page(first):
        pe._outer(c)
        if first:
            _screening_header(c, ws_id, tier, topic)
            top = pe.P1_TOP
        else:
            top = pe.P2_TOP
            from reportlab.lib.units import mm as _mm
            c.setFont("Helvetica-Bold", 9); c.setFillColor(pe.MGRAY)
            c.drawCentredString(pe.PW/2, pe.PH - pe.MT - 4*_mm, f"Screening Test {ws_id} (continued)")
        pe._sidebar(c, top, pe.P1_BOT if first else pe.P2_BOT, page=1 if first else 2)
        pe._divider(c, top, pe.P1_BOT if first else pe.P2_BOT)
        bot = pe.P1_BOT if first else pe.P2_BOT
        return pe.Col(c, pe.LX, pe.CW, top, bot), pe.Col(c, pe.RX, pe.CW, top, bot)

    rl, rr = _new_page(True)
    remaining = list(questions)
    page_num = 1
    while remaining:
        leftover = []
        for item in remaining:
            if not rl.render(item):
                leftover.append(item)
        remaining2 = []
        for item in leftover:
            if not rr.render(item):
                remaining2.append(item)
        remaining = remaining2
        if remaining:
            c.showPage()
            page_num += 1
            rl, rr = _new_page(False)
        else:
            if page_num == 1:
                c.showPage()
                pe._outer(c)
                pe._sidebar(c, pe.P2_TOP, pe.P2_BOT, page=2)
                pe._divider(c, pe.P2_TOP, pe.P2_BOT)
                pe._footer_p2(c)
                rl2 = pe.Col(c, pe.LX, pe.CW, pe.P2_TOP, pe.P2_BOT)
                rr2 = pe.Col(c, pe.RX, pe.CW, pe.P2_TOP, pe.P2_BOT)
                pe._rough_work(c, rl2); pe._rough_work(c, rr2)
            else:
                pe._footer_p2(c)
                pe._rough_work(c, rl); pe._rough_work(c, rr)
    c.save()
    pe._clean()
    buf.seek(0)
    report = {"used": used, "skipped": skipped, "total_questions": n}
    return buf, report


# ─────────────────────────────────────────────────────────────────────────
# COMPREHENSIVE screening blueprints — sample EVERY prerequisite sublevel
# band a student should have completed by the end of the PREVIOUS class,
# per the Class-By-Class Support Schema. 2 questions per band.
#
# NOTE: Level 20 (Statistics, Probability & AP) has no real question
# content built in the app yet -- any Level 20 source below will be
# automatically skipped and reported, never silently faked.
# ─────────────────────────────────────────────────────────────────────────
def _band(level_num, codes, n=2, sheet="1"):
    return [(code, sheet, level_num, n) for code in codes]

SCREENING_BLUEPRINTS = {
    "3": (
        _band(1, ["1A","1B","1C","1D","1E"]) +
        _band(3, ["3A","3B","3C","3D","3E"])
    ),
    "4": (
        _band(1, ["1D","1E","1F"]) +
        _band(3, ["3F","3G","3H","3I","3J"]) +
        _band(4, ["4A","4B","4C","4D"])
    ),
    "5": (
        _band(1, ["1D","1E"]) +
        _band(3, ["3K","3L","3M","3N"]) +
        _band(4, ["4E","4F","4G","4H","4I","4J"]) +
        _band(5, ["5A","5B","5C"]) +
        _band(6, ["6A"])
    ),
    "6": (
        _band(3, ["3O","3P","3Q","3R"]) +
        _band(4, ["4K","4L","4M","4N","4O","4P","4Q"]) +
        _band(5, ["5G","5H","5I"]) +
        _band(6, ["6A","6B","6C","6D","6E","6F"]) +
        _band(7, ["7A","7B","7C"]) +
        _band(18, ["18A"])
    ),
    "7": (
        _band(1, ["1G","1H","1I","1J"]) +
        _band(9, ["9A","9B","9C","9D","9E"]) +
        _band(8, ["8A","8B","8C","8D"]) +
        _band(6, ["6G","6H","6I","6J","6K","6L"]) +
        _band(7, ["7D","7E","7F"]) +
        _band(11, ["11A","11B","11C"]) +
        _band(10, ["10A","10B","10C","10D","10E"]) +
        _band(18, ["18B","18C"])
    ),
    "8": (
        _band(8, ["8E","8F","8G","8H","8I","8J"]) +
        _band(6, ["6M","6N","6O","6P"]) +
        _band(7, ["7G","7H","7I"]) +
        _band(12, ["12A","12B","12C"]) +
        _band(16, ["16A","16B","16C"]) +
        _band(11, ["11D","11E","11F","11G"]) +
        _band(13, ["13A","13B"]) +
        _band(18, ["18D"])
    ),
    "9": (
        _band(12, ["12D","12E","12F","12G","12H","12I","12J"]) +
        _band(16, ["16D","16E","16F","16G","16H","16I","16J"]) +
        _band(13, ["13C","13D","13E","13F"]) +
        _band(10, ["10F","10G","10H","10I","10J"]) +
        _band(14, ["14A","14B","14C"]) +
        _band(18, ["18E","18F","18G","18H","18I"])
    ),
    "10": (
        _band(14, ["14D","14E","14F","14G","14H"]) +
        _band(15, ["15A","15B","15C"]) +
        _band(16, ["16D","16E","16F","16G","16H","16I","16J"]) +
        _band(17, ["17A","17B","17C"]) +
        _band(18, ["18E","18F","18G","18H","18I"]) +
        _band(20, ["20A","20B","20C"])  # will auto-skip -- flagged below
    ),
}
