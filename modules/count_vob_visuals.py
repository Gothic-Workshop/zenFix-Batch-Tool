import os
from collections import Counter

from colorama import Fore

from utils.file_utils import list_files, get_user_selection
from utils.log_utils import log

INPUT_FOLDER = "zenfix_input"
OUTPUT_FOLDER = "zenfix_output"


def _normalize_visual_filters(raw_input):
    values = [v.strip() for v in raw_input.split(",") if v.strip()]
    return {v.upper() for v in values}


def _write_report(path, counts, total_matched, filters_used):
    with open(path, "w", encoding="utf-8") as f:
        f.write("# VOB Visual Usage Report\n")
        if filters_used:
            f.write(f"Filters: {', '.join(sorted(filters_used))}\n")
        else:
            f.write("Filters: (none - counted all non-empty visuals)\n")
        f.write(f"Total matched VOBs: {total_matched}\n\n")

        for visual, amount in counts.most_common():
            f.write(f"{amount}\t{visual}\n")


def count_vob_visuals_single():
    files = list_files(INPUT_FOLDER, ".zen")
    if not files:
        log(Fore.RED + "? No ZEN files in input.")
        return

    selected = get_user_selection(files, "Select a ZEN file to scan:")
    if not selected:
        return

    raw_filters = input(
        Fore.CYAN + "Enter visual names to include (comma-separated, leave empty for all visuals):\n> "
    ).strip()
    visual_filters = _normalize_visual_filters(raw_filters)

    path = os.path.join(INPUT_FOLDER, selected)
    out_name = f"{os.path.splitext(selected)[0]}_VobVisualCount.txt"
    out_path = os.path.join(OUTPUT_FOLDER, out_name)

    try:
        with open(path, "r", encoding="windows-1250") as f:
            lines = f.readlines()
    except Exception as e:
        log(Fore.RED + f"? Could not read {selected}: {e}")
        return

    counts = Counter()
    total_matched = 0

    inside_zcvob = False
    current_visual = ""
    current_show_visual = ""

    def flush_current():
        nonlocal total_matched

        visual_clean = current_visual.strip()
        if not visual_clean:
            return

        if current_show_visual != "1":
            return

        visual_key = visual_clean.upper()
        if visual_filters and visual_key not in visual_filters:
            return

        counts[visual_clean] += 1
        total_matched += 1

    for line in lines:
        stripped = line.strip()

        if stripped.startswith("[% "):
            if inside_zcvob:
                flush_current()

            parts = stripped[3:].split()
            class_name = parts[0] if parts else ""

            inside_zcvob = class_name == "zCVob"
            current_visual = ""
            current_show_visual = ""
            continue

        if not inside_zcvob:
            continue

        if stripped.startswith("visual=string:"):
            current_visual = stripped.split(":", 1)[1]
        elif stripped.startswith("showVisual=bool:"):
            current_show_visual = stripped.split(":", 1)[1].strip()

    if inside_zcvob:
        flush_current()

    if not counts:
        log(Fore.YELLOW + "?? No matching zCVob entries found with showVisual=1.")
        return

    _write_report(out_path, counts, total_matched, visual_filters)

    print(Fore.GREEN + f"\n? Found {total_matched} matching zCVob entries.")
    print(Fore.CYAN + "Visual usage (most -> least):")
    for visual, amount in counts.most_common():
        print(f" {amount:>5}x  {visual}")

    log(Fore.GREEN + f"? Saved visual usage report to: {out_path}")
