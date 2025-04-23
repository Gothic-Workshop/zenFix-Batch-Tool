
import os
from colorama import Fore
from utils.file_utils import list_files, get_user_selection
from utils.log_utils import log, log_action
from modules.prompt_replacements import load_fix_map

OUTPUT_FOLDER = "zenfix_output"

FOLDERS = {
    "input": "zenfix_input",
    "output": "zenfix_output",
    "instances": "zenfix_instances"
}

def apply_fix(input_file, fix_map, output_name_suffix):
    try:
        with open(input_file, 'r', encoding='windows-1250') as f:
            lines = f.readlines()
    except:
        log_action("Fix Blocks", os.path.basename(input_file), "fail", "Unreadable input file")
        return

    inside_block = False
    block = []
    fixed_lines = []
    fixed = 0
    total = 0

    for line in lines:
        stripped = line.strip()

        if stripped.startswith('[% oCItem'):
            inside_block = True
            block = [line]
            continue

        if inside_block:
            block.append(line)
            if stripped == '[]' and any("itemInstance=string:" in l for l in block):
                inside_block = False
                total += 1

                vob_index = next((i for i, l in enumerate(block) if "vobName=string:" in l), -1)
                item_index = next((i for i, l in enumerate(block) if "itemInstance=string:" in l), -1)

                if vob_index != -1 and item_index != -1:
                    vob = block[vob_index].split(":", 1)[1].strip()
                    item = block[item_index].split(":", 1)[1].strip()
                    if vob in fix_map and item == "":
                        fixed += 1
                        block[vob_index] = f"            vobName=string:{fix_map[vob]}\n"
                        block[item_index] = f"            itemInstance=string:{fix_map[vob]}\n"

                fixed_lines.extend(block)
                block = []
            continue

        fixed_lines.append(line)

    name = os.path.basename(input_file).rsplit(".", 1)[0]
    out_file = os.path.join(OUTPUT_FOLDER, f"{name}_{output_name_suffix}.zen")
    with open(out_file, 'w', encoding='windows-1250') as f:
        f.writelines(fixed_lines)

    log_action("Fix Blocks", os.path.basename(input_file), "success", f"{fixed} fixed / {total} total")
    log(Fore.GREEN + f"✅ Fixed {fixed}/{total} blocks.")
    log(Fore.YELLOW + f"💾 Saved to: {out_file}")


def fix_selected_block():
    zens = list_files(FOLDERS["input"], ".zen")
    selected = get_user_selection(zens, "Choose ZEN:")
    if not selected:
        return

    name = selected.rsplit(".", 1)[0]
    fix = f"{name}_instanceFix.txt"
    fix_files = list_files(FOLDERS["instances"], "_instanceFix.txt")

    if fix not in fix_files:
        log(Fore.RED + f"❌ No fix list found for {selected}")
        return

    fix_map = load_fix_map(os.path.join(FOLDERS["instances"], fix))
    apply_fix(os.path.join(FOLDERS["input"], selected), fix_map, "InstanceFixed")

def fix_all_blocks_multi():
    fix_files = list_files(FOLDERS["instances"], "_instanceFix.txt")
    for file in fix_files:
        name = file.split("_instanceFix")[0] + ".zen"
        print(Fore.CYAN + f"Processing fix file: {file}")
        print(Fore.CYAN + f"Looking for ZEN: {name}")
        zen_files = {f.lower(): f for f in os.listdir(FOLDERS["input"])}
        if name.lower() in zen_files:
            actual_name = zen_files[name.lower()]
            print(Fore.GREEN + f"✅ Applying fix to {actual_name}")
            fix_map = load_fix_map(os.path.join(FOLDERS["instances"], file))
            apply_fix(os.path.join(FOLDERS["input"], actual_name), fix_map, "InstanceFixed")
