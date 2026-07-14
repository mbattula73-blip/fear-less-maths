"""
Fear Less Maths — Bulk Worksheet Export.

Generates every worksheet (4 main sheets + 4 remedial sheets, per sublevel)
for a whole level, or for a 5-level range, and packages them into a single
ZIP file organised by sublevel folder. Reuses pdf_engine.build_pdf() as-is —
no changes to worksheet generation logic, only batching + zipping.
"""
import zipfile
from io import BytesIO

from pypdf import PdfWriter

import levels_data
from pdf_engine import build_pdf

ALL_SHEETS = ["1", "2", "3", "4", "1R", "2R", "3R", "4R"]

# Used only by the single-PDF, level-wise export (build_level_single_pdf /
# build_multi_level_single_pdfs below). Remedial sheets are deliberately
# excluded — they're printed separately and rarely, so bundling them into
# the main printing PDF would just add clutter.
MAIN_SHEETS = ["1", "2", "3", "4"]

# The five preset ranges offered in the app, covering every level 1-25
# (Level 0 / Pre-Levels are offered as their own range since they're a
# different track from the main 1-20 academic ladder).
FIVE_LEVEL_RANGES = {
    "Pre-Levels (0, 21-25)": [0, 21, 22, 23, 24, 25],
    "Levels 1-5":  [1, 2, 3, 4, 5],
    "Levels 6-10": [6, 7, 8, 9, 10],
    "Levels 11-15": [11, 12, 13, 14, 15],
    "Levels 16-20": [16, 17, 18, 19, 20],
}


def count_pdfs_for_levels(level_nums: list) -> int:
    """Total PDF count for a list of levels -- used to show an honest
    'this will generate N files' estimate before the user commits."""
    total = 0
    for lvl in level_nums:
        subs = levels_data.SUBLEVELS.get(lvl, [])
        total += len(subs) * len(ALL_SHEETS)
    return total


def build_level_zip(level_num: int, progress_cb=None):
    """Generates every worksheet for a single level. Returns (zip_bytesio,
    failures_list). progress_cb(done, total) is called after each PDF."""
    return build_multi_level_zip([level_num], progress_cb=progress_cb)


def build_multi_level_zip(level_nums: list, progress_cb=None) -> BytesIO:
    """Generates every worksheet across multiple levels and returns one ZIP,
    with files organised as Level<N>/<sublevel>-<sheet>.pdf inside.
    Any sublevel/sheet that fails to render is skipped and recorded in a
    MANIFEST.txt inside the zip, rather than aborting the whole export."""
    total = count_pdfs_for_levels(level_nums)
    done = 0
    failures = []

    zip_buf = BytesIO()
    with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for lvl in level_nums:
            subs = levels_data.SUBLEVELS.get(lvl, [])
            level_name = levels_data.LEVELS.get(lvl, {}).get("name", f"Level {lvl}")
            folder = f"Level{lvl:02d} - {level_name}".replace("/", "-")
            for sublevel_code, _topic in subs:
                for sheet in ALL_SHEETS:
                    ws_id = f"{sublevel_code}-{sheet}"
                    try:
                        pdf_bytes = build_pdf(lvl, sublevel_code, sheet).read()
                        zf.writestr(f"{folder}/{ws_id}.pdf", pdf_bytes)
                    except Exception as e:
                        failures.append(f"{ws_id}: {e}")
                    done += 1
                    if progress_cb:
                        progress_cb(done, total)
        manifest = (
            f"Fear Less Maths -- Bulk Export Manifest\n"
            f"Levels included: {level_nums}\n"
            f"Total worksheets: {total}\n"
            f"Successful: {total - len(failures)}\n"
            f"Failed: {len(failures)}\n\n"
        )
        if failures:
            manifest += "Failed worksheets (skipped, not included in this zip):\n"
            manifest += "\n".join(failures)
        zf.writestr("MANIFEST.txt", manifest)

    zip_buf.seek(0)
    return zip_buf, failures


# ─── Single PDF, level-wise (main sheets only, no remedials) ────────────────
# Separate from the ZIP functions above so existing behaviour is untouched.

def count_main_pdfs_for_levels(level_nums: list) -> int:
    """Same as count_pdfs_for_levels but counts only the 4 main sheets per
    sublevel (no remedials) — used for the single-PDF export estimate."""
    total = 0
    for lvl in level_nums:
        subs = levels_data.SUBLEVELS.get(lvl, [])
        total += len(subs) * len(MAIN_SHEETS)
    return total


def build_level_single_pdf(level_num: int, progress_cb=None):
    """Generates the 4 main sheets (no remedials) for every sublevel in a
    level, merged sublevel-by-sublevel into ONE PDF, ready for printing.
    Returns (pdf_bytesio, failures_list). progress_cb(done, total) is
    called after each worksheet."""
    subs = levels_data.SUBLEVELS.get(level_num, [])
    total = len(subs) * len(MAIN_SHEETS)
    done = 0
    failures = []

    writer = PdfWriter()
    for sublevel_code, _topic in subs:
        for sheet in MAIN_SHEETS:
            ws_id = f"{sublevel_code}-{sheet}"
            try:
                pdf_bytes = build_pdf(level_num, sublevel_code, sheet).read()
                writer.append(BytesIO(pdf_bytes))
            except Exception as e:
                failures.append(f"{ws_id}: {e}")
            done += 1
            if progress_cb:
                progress_cb(done, total)

    out_buf = BytesIO()
    writer.write(out_buf)
    writer.close()
    out_buf.seek(0)
    return out_buf, failures


def build_multi_level_single_pdfs(level_nums: list, progress_cb=None):
    """Generates one merged PDF per level (main sheets only) across multiple
    levels, and packages those level-PDFs into a ZIP (one PDF file per
    level inside, instead of one PDF per worksheet). Returns
    (zip_bytesio, failures_list). progress_cb(done, total) is called after
    each worksheet across all levels."""
    total = count_main_pdfs_for_levels(level_nums)
    done = 0
    failures = []

    zip_buf = BytesIO()
    with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for lvl in level_nums:
            subs = levels_data.SUBLEVELS.get(lvl, [])
            level_name = levels_data.LEVELS.get(lvl, {}).get("name", f"Level {lvl}")
            fname = f"Level{lvl:02d} - {level_name}".replace("/", "-") + ".pdf"

            writer = PdfWriter()
            for sublevel_code, _topic in subs:
                for sheet in MAIN_SHEETS:
                    ws_id = f"{sublevel_code}-{sheet}"
                    try:
                        pdf_bytes = build_pdf(lvl, sublevel_code, sheet).read()
                        writer.append(BytesIO(pdf_bytes))
                    except Exception as e:
                        failures.append(f"{ws_id}: {e}")
                    done += 1
                    if progress_cb:
                        progress_cb(done, total)

            level_buf = BytesIO()
            writer.write(level_buf)
            writer.close()
            zf.writestr(fname, level_buf.getvalue())

        manifest = (
            f"Fear Less Maths -- Level-wise Single-PDF Export Manifest\n"
            f"Levels included: {level_nums}\n"
            f"Sheets included per sublevel: {MAIN_SHEETS} (remedials excluded)\n"
            f"Total worksheets: {total}\n"
            f"Successful: {total - len(failures)}\n"
            f"Failed: {len(failures)}\n\n"
        )
        if failures:
            manifest += "Failed worksheets (skipped, not included):\n"
            manifest += "\n".join(failures)
        zf.writestr("MANIFEST.txt", manifest)

    zip_buf.seek(0)
    return zip_buf, failures
