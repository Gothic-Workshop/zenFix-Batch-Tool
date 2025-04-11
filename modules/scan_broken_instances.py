
import os
from colorama import Fore
from utils.file_utils import write_lines
from utils.log_utils import log, log_action

def find_broken_instances(file_path):
    broken = set()
    try:
        with open(file_path, 'r', encoding='windows-1250') as f:
            lines = f.readlines()
    except:
        log(Fore.RED + f"❌ Failed to read {file_path}")
        return broken

    inside_block = False
    block = []

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
                vob = next((l.split(":", 1)[1].strip() for l in block if "vobName=string:" in l), None)
                item = next((l.split(":", 1)[1].strip() for l in block if "itemInstance=string:" in l), None)
                if vob and item == "":
                    broken.add(vob)
    return broken

def scan_broken_instances(file_path, instances_dir):
    broken = find_broken_instances(file_path)
    name = os.path.basename(file_path).rsplit(".", 1)[0]
    if broken:
        output_file = os.path.join(instances_dir, f"{name}_instanceList.txt")
        write_lines(output_file, sorted(broken))
        log_action("Scan Broken", os.path.basename(file_path), "success", f"{len(broken)} broken")
        log(Fore.YELLOW + f"🔍 {file_path}: Found {len(broken)} broken instances.")
        log(Fore.GREEN + f"✅ Saved to: {output_file}")
    else:
        log_action("Scan Broken", os.path.basename(file_path), "success", "no broken entries")
        log(Fore.GREEN + f"✅ {file_path}: No broken instances found.")
