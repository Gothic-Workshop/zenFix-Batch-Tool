
import os
from colorama import Fore
from utils.config_loader import load_script_path
from utils.item_validator import scan_valid_items, validate_item
from utils.file_utils import write_lines
from utils.log_utils import log, log_action
from modules.prompt_replacements import prompt_replacements
from modules.fix_blocks import apply_fix
from modules.scan_broken_instances import find_broken_instances

INPUT_FOLDER = "zenfix_input"
OUTPUT_FOLDER = "zenfix_output"
INSTANCE_FOLDER = "zenfix_instances"

def batch_fix():
    os.makedirs(INSTANCE_FOLDER, exist_ok=True)
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    script_path = load_script_path()
    if not script_path:
        return

    scan_valid_items(script_path)
    zens = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(".zen")]
    if not zens:
        log(Fore.RED + "❌ No ZEN files found in input folder.")
        return

    all_broken = set()
    zen_map = {}

    for z in zens:
        zpath = os.path.join(INPUT_FOLDER, z)
        broken = find_broken_instances(zpath)
        if broken:
            zen_map[z] = broken
            all_broken.update(broken)

    if not all_broken:
        log(Fore.CYAN + "✔ No broken instances found in any file.")
        return

    list_path = os.path.join(INSTANCE_FOLDER, "batchFix_instanceList.txt")
    write_lines(list_path, sorted(all_broken))
    log(Fore.GREEN + f"📄 Saved broken instance list: {list_path}")

    fix_path = os.path.join(INSTANCE_FOLDER, "batchFix_instanceFix.txt")
    fix_map = prompt_replacements(sorted(all_broken), fix_path)

    for z in zen_map:
        apply_fix(os.path.join(INPUT_FOLDER, z), fix_map, "InstanceFixed")
