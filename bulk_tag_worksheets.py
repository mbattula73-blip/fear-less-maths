"""
bulk_tag_worksheets.py — One-time script to pre-populate db.worksheet_tags
for every base worksheet (sheets 1-4) across all levels, using the
heuristic auto-tagger in concept_tagger.py.

Remedial sheets ('...R') are NOT tagged separately — db.py's
get_worksheet_tags_with_fallback() already falls back to the base sheet's
tags automatically, since remedial sheets test the same concepts per
question number (only the numbers in the text change).

Safe to re-run: it overwrites any existing tags for a worksheet with fresh
auto-tagged ones. If you've hand-edited tags via the "Concept Tags" tab and
want to keep them, do NOT re-run this for that worksheet — use the tab
to edit individual sheets instead.

Usage:
    python3 bulk_tag_worksheets.py            # tag everything
    python3 bulk_tag_worksheets.py --level 9  # tag just one level
    python3 bulk_tag_worksheets.py --dry-run  # preview without saving
"""
import sys
import argparse

sys.path.insert(0, ".")

from levels_data import SUBLEVELS
from ws_helpers import numbered_questions
from concept_tagger import auto_tag_worksheet
import db


def tag_all(level_filter=None, dry_run=False, verbose=False):
    levels = [level_filter] if level_filter else sorted(SUBLEVELS.keys())
    total_worksheets = 0
    total_questions = 0
    total_specific = 0
    errors = []

    for lvl in levels:
        for code, topic in SUBLEVELS.get(lvl, []):
            for sheet in ["1", "2", "3", "4"]:
                ws_id = f"{code}-{sheet}"
                try:
                    nq = numbered_questions(code, sheet)
                    if not nq:
                        continue
                    tags = auto_tag_worksheet(nq, topic)
                    specific = sum(1 for t in tags.values() if t != topic)
                    total_worksheets += 1
                    total_questions += len(tags)
                    total_specific += specific
                    if verbose:
                        print(f"  {ws_id}: {len(tags)} Qs, {specific} specifically tagged")
                    if not dry_run:
                        db.set_worksheet_tags(ws_id, tags)
                except Exception as e:
                    errors.append((ws_id, str(e)[:80]))

    print(f"\n{'DRY RUN — ' if dry_run else ''}Tagging complete.")
    print(f"Worksheets processed: {total_worksheets}")
    print(f"Questions tagged: {total_questions}")
    print(f"Specifically tagged (beyond sublevel fallback): {total_specific} "
          f"({total_specific/total_questions*100:.1f}%)" if total_questions else "")
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for ws_id, err in errors[:20]:
            print(f"  {ws_id}: {err}")
    else:
        print("Errors: NONE")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bulk auto-tag worksheet questions with concept labels.")
    parser.add_argument("--level", type=int, default=None, help="Only tag this level number (1-20).")
    parser.add_argument("--dry-run", action="store_true", help="Preview without saving to the database.")
    parser.add_argument("--verbose", action="store_true", help="Print per-worksheet detail.")
    args = parser.parse_args()
    tag_all(level_filter=args.level, dry_run=args.dry_run, verbose=args.verbose)
