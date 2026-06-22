"""
ws_helpers.py — small helpers shared by the analytics module tabs.
"""
from content import get_questions

# Shared with pages/1_Daily_Entry.py (the dropdown staff pick from) and
# seed_demo_data.py (so demo data exercises the same categories) — kept in
# one place so they can't drift out of sync.
MISTAKE_TYPES = [
    "Calculation slip",
    "Concept not understood",
    "Wrong method/formula used",
    "Misread the question",
    "Careless / rushed",
    "No attempt",
    "Other",
]


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


def remedial_id_for(sublevel_code: str, sheet_num: str) -> str:
    """
    Given a (possibly non-remedial) sheet number, returns the matching remedial
    worksheet id, e.g. ('4A','1') -> '4A-1R'. If sheet_num is already remedial,
    returns the same worksheet id unchanged.
    """
    sn = str(sheet_num)
    base = sn if sn.endswith("R") else f"{sn}R"
    return f"{sublevel_code}-{base}"


def build_whatsapp_link(parent_whatsapp: str, message: str) -> str:
    """Builds a wa.me click-to-send link that opens WhatsApp with the message
    pre-filled to the parent's number. parent_whatsapp should already be
    normalized (digits incl. country code)."""
    from urllib.parse import quote
    digits = "".join(ch for ch in str(parent_whatsapp) if ch.isdigit())
    return f"https://wa.me/{digits}?text={quote(message)}"


def build_whatsapp_report(student_name: str, worksheet_id: str, total_questions: int,
                           wrong_qs: list, resolved_topics: dict, remedial_id: str = None) -> str:
    """Builds a short, plain-language WhatsApp report for a parent."""
    n_wrong = len(wrong_qs)
    n_correct = total_questions - n_wrong

    if n_wrong == 0:
        return (
            f"Hi! {student_name} completed worksheet {worksheet_id} today and got "
            f"all {total_questions} questions correct. Great work! 🎉"
        )

    topics = [t for t in resolved_topics.values() if t and t != "(untagged)"]
    unique_topics = sorted(set(topics))

    lines = [f"Hi! {student_name} attempted worksheet {worksheet_id} today — "
             f"{n_correct}/{total_questions} correct."]

    if unique_topics:
        if len(unique_topics) == 1:
            lines.append(f"They need a bit more practice with: {unique_topics[0]}.")
        else:
            topic_list = ", ".join(unique_topics[:-1]) + f" and {unique_topics[-1]}"
            lines.append(f"They need a bit more practice with: {topic_list}.")
    else:
        lines.append(f"They missed {n_wrong} question(s) — topics not yet tagged for this worksheet.")

    if remedial_id:
        lines.append(f"A remedial worksheet ({remedial_id}) has been assigned to help reinforce this.")

    lines.append("Please encourage them to revise this at home. Thank you! 🙏")
    return " ".join(lines)

