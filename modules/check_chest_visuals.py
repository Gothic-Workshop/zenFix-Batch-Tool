
import os
from colorama import Fore
from utils.file_utils import list_files, get_user_selection
from utils.log_utils import log
from utils.config_loader import load_chest_config, load_config, load_directories

DIRECTORIES = load_directories()
BASE_CONFIG = load_config()
CHEST_CONFIG = load_chest_config()
INPUT_FOLDER = DIRECTORIES["input"]
OUTPUT_FOLDER = DIRECTORIES["output"]

def load_visual_map():
    return CHEST_CONFIG.get("visual_map", {})

def get_field_value(block, prefix):
    for line in block:
        if prefix in line:
            parts = line.split(":", 1)
            if len(parts) == 2:
                return parts[1].strip()
    return ""

def check_chest_visuals_single():
    files = list_files(INPUT_FOLDER, ".zen")
    if not files:
        log(Fore.RED + "❌ No ZEN files in input.")
        return

    selected = get_user_selection(files, "Select a ZEN file to scan:")
    if not selected:
        return

    visual_map = load_visual_map()
    path = os.path.join(INPUT_FOLDER, selected)
    name = os.path.splitext(selected)[0]
    out_path = os.path.join(OUTPUT_FOLDER, f"{name}_ChestFix.zen")

    read_encoding = BASE_CONFIG.get("validation", {}).get("encoding", "windows-1252")

    try:
        with open(path, "r", encoding=read_encoding) as f:
            lines = f.readlines()
    except Exception as e:
        log(Fore.RED + f"❌ Could not read {selected}: {e}")
        return

    inside_block = False
    block = []
    result = []
    fixed_count = 0
    i = 0
    changed = False

    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("[% oCMobContainer"):
            inside_block = True
            block = [line]
            i += 1
            while i < len(lines):
                block.append(lines[i])
                if lines[i].strip().startswith("contains=string:"):
                    break
                i += 1
            i += 1

            visual = get_field_value(block, "visual=string:")
            locked = get_field_value(block, "locked=bool:")
            key = get_field_value(block, "keyInstance=string:")
            pick = get_field_value(block, "pickLockStr=string:")
            vob_name = get_field_value(block, "vobName=string:")

            if CHEST_CONFIG.get("validate_visuals", True) and locked == "0" and "LOCKED" in visual.upper():
                print(Fore.YELLOW + f"⚠️ Unlocked chest '{vob_name}' uses LOCKED visual: {visual}")
                new_visual = visual_map.get(visual, "")
                if new_visual:
                    print(Fore.CYAN + f"Suggested visual: {new_visual}")
                    should_apply = CHEST_CONFIG.get("auto_fix_wrong_locked_visuals", False)
                    if not should_apply:
                        print(" [1] Accept")
                        print(" [2] Skip")
                        choice = input("> ").strip()
                        should_apply = choice == "1"
                    if should_apply:
                        block = [l if not l.strip().startswith("visual=string:") else f"            visual=string:{new_visual}\n" for l in block]
                        fixed_count += 1
                        changed = True

            if locked == "-1":
                if CHEST_CONFIG.get("report_impossible_locked_chests", True) and CHEST_CONFIG.get("validate_key_instance", True) and CHEST_CONFIG.get("validate_picklock", True) and not key and not pick:
                    print(Fore.RED + f"❌ Locked chest '{vob_name}' has no keyInstance or pickLockStr (visual: {visual})")
                if CHEST_CONFIG.get("validate_visuals", True) and "LOCKED" not in visual.upper():
                    print(Fore.YELLOW + f"⚠️ Locked chest '{vob_name}' uses UNLOCKED visual: {visual}")

            result.extend(block)
        else:
            result.append(line)
            i += 1

    if changed:
        with open(out_path, "w", encoding=read_encoding) as f:
            f.writelines(result)
        log(Fore.GREEN + f"✅ {selected}: Fixed {fixed_count} chest visuals.")
    else:
        log(Fore.CYAN + f"ℹ️ No changes made to: {selected}")