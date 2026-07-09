"""
Fear Less Maths — Personalised Class Plan Export.

Generates ONLY the worksheets assigned to a given class in the published
5-month plan (class_plan_2026_27.py) — not a whole level, the specific
sublevels and sheet depths that plan calls for. Reuses pdf_engine.build_pdf()
exactly as-is, same as bulk_export.py.
"""
import zipfile
from io import BytesIO

import levels_data
from pdf_engine import build_pdf
from class_plan_2026_27 import CLASS_PLAN_2026_27


def count_pdfs_for_class(class_name: str) -> int:
    plan = CLASS_PLAN_2026_27.get(class_name, [])
    total = 0
    for item in plan:
        total += len(item["high_sublevels"]) * len(item["high_sheets"])
        total += len(item["med_sublevels"]) * len(item["med_sheets"])
    return total


def build_class_plan_zip(class_name: str, progress_cb=None):
    """Generates every worksheet assigned to this class in the 5-month plan.
    Returns (zip_bytesio, failures_list). progress_cb(done, total) is
    called after each PDF, same pattern as bulk_export.py."""
    plan = CLASS_PLAN_2026_27.get(class_name, [])
    total = count_pdfs_for_class(class_name)
    done = 0
    failures = []

    zip_buf = BytesIO()
    with zipfile.ZipFile(zip_buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for item in plan:
            lvl = item["level"]
            level_name = levels_data.LEVELS.get(lvl, {}).get("name", f"Level {lvl}")
            folder = f"Level{lvl:02d} - {level_name}".replace("/", "-")

            # Core (HIGH-priority) sublevels at this level's assigned depth
            for sublevel_code in item["high_sublevels"]:
                for sheet in item["high_sheets"]:
                    ws_id = f"{sublevel_code}-{sheet}"
                    try:
                        pdf_bytes = build_pdf(lvl, sublevel_code, sheet).read()
                        zf.writestr(f"{folder}/{ws_id}.pdf", pdf_bytes)
                    except Exception as e:
                        failures.append(f"{ws_id}: {e}")
                    done += 1
                    if progress_cb:
                        progress_cb(done, total)

            # Word-problem (MED-HIGH) sublevels, always at 2-sheet depth
            for sublevel_code in item["med_sublevels"]:
                for sheet in item["med_sheets"]:
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
            f"Fear Less Maths -- Personalised 5-Month Plan Export\n"
            f"Class: {class_name}\n"
            f"Total worksheets: {total}\n"
            f"Successful: {total - len(failures)}\n"
            f"Failed: {len(failures)}\n\n"
            f"This ZIP contains exactly the worksheets assigned to {class_name} in the\n"
            f"published 5-month plan (16 FLM days/month x 5 months) -- not a full level.\n"
        )
        if failures:
            manifest += "\nFailed worksheets (skipped, not included in this zip):\n"
            manifest += "\n".join(failures)
        zf.writestr("MANIFEST.txt", manifest)

    zip_buf.seek(0)
    return zip_buf, failures
