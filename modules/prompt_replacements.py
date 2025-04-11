
from utils.file_utils import write_lines
from utils.log_utils import log, log_action
from colorama import Fore

def prompt_replacements(broken_list, output_file):
    fix_map = {}
    print(Fore.YELLOW + "\n🛠 Prompting replacements:")
    for b in broken_list:
        replacement = input(f"Replace '{b}' with: ").strip()
        if replacement:
            fix_map[b] = replacement
    lines = [f"{k} -> {v}" for k, v in fix_map.items()]
    write_lines(output_file, lines)
    log_action("Prompt Fixes", output_file)
    log(Fore.GREEN + f"✅ Fix map saved: {output_file}")
    return fix_map

def load_fix_map(path):
    fix_map = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if '->' in line:
                k, v = line.strip().split('->')
                fix_map[k.strip()] = v.strip()
    return fix_map
