
import os
from colorama import Fore
from utils.item_validator import validate_item
from utils.file_utils import write_lines
from utils.log_utils import log
from modules.prompt_replacements import prompt_replacements, load_fix_map

INPUT_FOLDER = "zenfix_input"
OUTPUT_FOLDER = "zenfix_output"
INSTANCE_FOLDER = "zenfix_instances"

def parse_contains_line(line):
    raw = line.split("contains=string:")[1].strip()
    tokens = [x.strip() for x in raw.split(",") if x.strip()]
    return tokens

def validate_container_entries(zen_path):
    basename = os.path.basename(zen_path).rsplit(".", 1)[0]
    list_path = os.path.join(INSTANCE_FOLDER, f"{basename}_Containers_instanceList.txt")
    fix_path = os.path.join(INSTANCE_FOLDER, f"{basename}_Containers_instanceFix.txt")

    invalid_items = {}

    with open(zen_path, 'r', encoding='windows-1250') as f:
        lines = f.readlines()

    for line in lines:
        if "contains=string:" in line:
            items = parse_contains_line(line)
            for item in items:
                base_item = item.split(":")[0]
                if not validate_item(base_item):
                    invalid_items[base_item] = None

    if not invalid_items:
        log(Fore.GREEN + f"✔ All container items in {basename} are valid.")
        return

    write_lines(list_path, sorted(invalid_items.keys()))
    log(Fore.YELLOW + f"🔍 Found {len(invalid_items)} invalid items in {basename}.")
    log(Fore.GREEN + f"📄 Saved list to: {list_path}")

    fix_map = prompt_replacements(sorted(invalid_items.keys()), fix_path)
    apply_container_fixes(zen_path, fix_map)

def apply_container_fixes(zen_path, fix_map):
    basename = os.path.basename(zen_path).rsplit(".", 1)[0]
    out_path = os.path.join(OUTPUT_FOLDER, f"{basename}_ContainersFixed.zen")

    with open(zen_path, 'r', encoding='windows-1250') as f:
        lines = f.readlines()

    out_lines = []
    for line in lines:
        if "contains=string:" in line:
            parts = line.split("contains=string:")
            if len(parts) < 2:
                out_lines.append(line)
                continue
            prefix = parts[0] + "contains=string:"
            raw_items = parts[1].strip()
            tokens = [x.strip() for x in raw_items.split(",") if x.strip()]
            replaced = []
            for token in tokens:
                base = token.split(":")[0]
                suffix = ":" + token.split(":")[1] if ":" in token else ""
                if base in fix_map:
                    replaced.append(fix_map[base] + suffix)
                else:
                    replaced.append(token)
            line = prefix + ",".join(replaced) + "\n"
        out_lines.append(line)

    with open(out_path, 'w', encoding='windows-1250') as f:
        f.writelines(out_lines)

    log(Fore.GREEN + f"✅ Rewritten {basename} with replacements → {out_path}")
