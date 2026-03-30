import os
import re
from collections import defaultdict

from colorama import Fore

from utils.config_loader import load_focusname_prefixes, load_script_path
from utils.file_utils import get_user_selection, list_files
from utils.log_utils import log

INPUT_FOLDER = "zenfix_input"
OUTPUT_FOLDER = "zenfix_output"

FOCUS_LINE_PREFIX = "focusName=string:"
VOB_LINE_PREFIX = "vobName=string:"


def _load_focus_tokens_from_scripts(script_path):
    """Load identifier-like tokens from all .d files under the configured script folder."""
    token_pattern = re.compile(r"\b([A-Za-z_][A-Za-z0-9_]*)\b")
    tokens = set()

    for root_dir, _, files in os.walk(script_path):
        for file_name in files:
            if not file_name.lower().endswith(".d"):
                continue

            file_path = os.path.join(root_dir, file_name)
            try:
                with open(file_path, "r", encoding="windows-1250") as source:
                    for line in source:
                        tokens.update(token_pattern.findall(line))
            except Exception as exc:
                log(Fore.YELLOW + f"?? Could not read {file_path}: {exc}")

    return tokens


def _extract_omob_focus_entries(zen_path):
    """Extract (focusName, vobName, line_no) from oCMOB-derived blocks."""
    entries = []

    with open(zen_path, "r", encoding="windows-1250") as source:
        lines = source.readlines()

    in_omob_block = False
    current_focus = ""
    current_vob = ""
    current_focus_line = 0

    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()

        if stripped.startswith("[% "):
            if in_omob_block and current_focus:
                entries.append((current_focus, current_vob, current_focus_line))

            in_omob_block = stripped.lower().startswith("[% ocmob")
            current_focus = ""
            current_vob = ""
            current_focus_line = 0
            continue

        if not in_omob_block:
            continue

        if stripped.startswith(FOCUS_LINE_PREFIX):
            current_focus = stripped.split(FOCUS_LINE_PREFIX, 1)[1].strip()
            current_focus_line = idx
        elif stripped.startswith(VOB_LINE_PREFIX):
            current_vob = stripped.split(VOB_LINE_PREFIX, 1)[1].strip()

    if in_omob_block and current_focus:
        entries.append((current_focus, current_vob, current_focus_line))

    return entries


def _focus_family_key(focus_name):
    """Group variants like MOBNAME_GRAVE, MOBNAME_GRAVE_1, MOBNAME_GRAVEA under one family key."""
    if not focus_name:
        return focus_name

    cleaned = re.sub(r"[_-]?\d+$", "", focus_name)
    if cleaned.startswith("MOBNAME_"):
        parts = cleaned.split("_")
        if len(parts) >= 2:
            return "_".join(parts[:2])

    return cleaned


def _write_report(report_path, zen_name, invalid_entries, repeated_families):
    lines = [f"FocusName report for: {zen_name}", ""]

    if invalid_entries:
        lines.append("Invalid focusName values (not found in scripts):")
        for focus_name, vob_name, line_no in invalid_entries:
            vob_display = vob_name or "<no vobName>"
            lines.append(f"  - {focus_name} | vobName={vob_display} | line={line_no}")
    else:
        lines.append("Invalid focusName values: none")

    lines.append("")

    if repeated_families:
        lines.append("Repeated focusName families:")
        for family, values in sorted(repeated_families.items()):
            pretty_values = ", ".join(sorted(values))
            lines.append(f"  - {family}* -> {pretty_values}")
    else:
        lines.append("Repeated focusName families: none")

    lines.append("")

    with open(report_path, "w", encoding="utf-8") as out:
        out.write("\n".join(lines) + "\n")


def check_focus_names_for_zen(zen_path, valid_focus_tokens, check_repeats=True):
    basename = os.path.basename(zen_path).rsplit(".", 1)[0]
    entries = _extract_omob_focus_entries(zen_path)

    if not entries:
        log(Fore.CYAN + f"?? {basename}: no oCMOB focusName values found.")
        return

    invalid_entries = [
        (focus_name, vob_name, line_no)
        for focus_name, vob_name, line_no in entries
        if focus_name not in valid_focus_tokens
    ]

    repeated_families = {}
    if check_repeats:
        groups = defaultdict(set)
        for focus_name, _, _ in entries:
            groups[_focus_family_key(focus_name)].add(focus_name)
        repeated_families = {family: values for family, values in groups.items() if len(values) > 1}

    report_path = os.path.join(OUTPUT_FOLDER, f"{basename}_FocusNameReport.txt")
    _write_report(report_path, basename, invalid_entries, repeated_families)

    if invalid_entries:
        log(Fore.YELLOW + f"?? {basename}: found {len(invalid_entries)} invalid focusName entries.")
    else:
        log(Fore.GREEN + f"? {basename}: all oCMOB focusName values exist in scripts.")

    if check_repeats:
        if repeated_families:
            log(Fore.YELLOW + f"?? {basename}: found {len(repeated_families)} repeated focusName families.")
        else:
            log(Fore.GREEN + f"? {basename}: no repeated focusName families.")

    log(Fore.GREEN + f"?? Report saved: {report_path}")


def _ask_repeat_check_enabled():
    choice = input("Check repeated focusName families (e.g. MOBNAME_GRAVE*)? [Y/n]: ").strip().lower()
    return choice in {"", "y", "yes"}


def check_focus_names_single():
    files = list_files(INPUT_FOLDER, ".zen")
    selected = get_user_selection(files, "Select a ZEN file to scan focusName values:")
    if not selected:
        return

    script_path = load_script_path()
    if not script_path:
        log(Fore.RED + "? Script path is not configured. Cannot validate focusName values.")
        return

    valid_tokens = _load_focus_tokens_from_scripts(script_path)
    if not valid_tokens:
        log(Fore.RED + "? Could not load tokens from scripts. Cannot validate focusName values.")
        return

    check_repeats = _ask_repeat_check_enabled()
    check_focus_names_for_zen(os.path.join(INPUT_FOLDER, selected), valid_tokens, check_repeats)


def check_focus_names_all():
    files = list_files(INPUT_FOLDER, ".zen")
    if not files:
        log(Fore.RED + "? No ZEN files in input folder.")
        return

    script_path = load_script_path()
    if not script_path:
        log(Fore.RED + "? Script path is not configured. Cannot validate focusName values.")
        return

    valid_tokens = _load_focus_tokens_from_scripts(script_path)
    if not valid_tokens:
        log(Fore.RED + "? Could not load tokens from scripts. Cannot validate focusName values.")
        return

    check_repeats = _ask_repeat_check_enabled()
    for file_name in files:
        check_focus_names_for_zen(os.path.join(INPUT_FOLDER, file_name), valid_tokens, check_repeats)


def _write_prefix_duplicate_report(report_path, prefixes, duplicates):
    lines = ["Configured focusName prefix duplicate report", ""]
    lines.append("Configured prefixes:")
    if prefixes:
        for prefix in prefixes:
            lines.append(f"  - {prefix}")
    else:
        lines.append("  - <none>")

    lines.append("")

    if not duplicates:
        lines.append("No duplicates found for configured prefixes.")
    else:
        lines.append("Duplicate focusName values:")
        for focus_name, occurrences in sorted(duplicates.items()):
            lines.append(f"  - {focus_name} (count={len(occurrences)})")
            for item in occurrences:
                lines.append(
                    f"      * file={item['file']} | line={item['line']} | vobName={item['vob_name'] or '<no vobName>'}"
                )
    lines.append("")

    with open(report_path, "w", encoding="utf-8") as out:
        out.write("\n".join(lines) + "\n")


def check_mobname_duplicates_by_prefix_all():
    files = list_files(INPUT_FOLDER, ".zen")
    if not files:
        log(Fore.RED + "? No ZEN files in input folder.")
        return

    prefixes = load_focusname_prefixes()
    if not prefixes:
        log(Fore.RED + "? No focusName prefixes configured in config.xml (<focusNamePrefixes list=\"...\" />).")
        return

    matches = defaultdict(list)

    for file_name in files:
        zen_path = os.path.join(INPUT_FOLDER, file_name)
        entries = _extract_omob_focus_entries(zen_path)
        for focus_name, vob_name, line_no in entries:
            if any(focus_name.startswith(prefix) for prefix in prefixes):
                matches[focus_name].append({
                    "file": file_name,
                    "line": line_no,
                    "vob_name": vob_name,
                })

    duplicates = {focus_name: occ for focus_name, occ in matches.items() if len(occ) > 1}

    report_path = os.path.join(OUTPUT_FOLDER, "FocusNamePrefixDuplicatesReport.txt")
    _write_prefix_duplicate_report(report_path, prefixes, duplicates)

    if duplicates:
        log(Fore.YELLOW + f"?? Found {len(duplicates)} duplicated focusName values for configured prefixes.")
    else:
        log(Fore.GREEN + "? No duplicated focusName values found for configured prefixes.")

    log(Fore.GREEN + f"?? Report saved: {report_path}")
