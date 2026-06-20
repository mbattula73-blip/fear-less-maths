"""
ws_helpers.py — small helpers shared by the analytics module tabs.
"""
from content import get_questions


def numbered_questions(sublevel_code: str, sheet_num: str):
    """
    Returns [(q_num, preview_text), ...] for a worksheet, matching the same
    numbering pdf_engine.py uses (concept_box/tips_box items are not numbered).
    """
    items = get_questions(sublevel_code, sheet_num)
    out = []
    n = 0
    for it in items:
        if it.get("type") not in ("concept_box", "tips_box"):
            n += 1
            preview = (it.get("text") or "").strip()
            if len(preview) > 70:
                preview = preview[:67] + "..."
            out.append((n, preview))
    return out
