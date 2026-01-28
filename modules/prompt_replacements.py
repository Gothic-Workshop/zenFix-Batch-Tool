
import os
from colorama import Fore
from utils.log_utils import log
from utils.fix_suggestions import load_fix_history, suggest_fix, update_fix_history

def prompt_replacements(broken_items, output_path):
    if not broken_items:
        log(Fore.YELLOW + "⚠️ No broken instances in list.")
        return {}

    fix_map = {}
    history = load_fix_history()

    for b in broken_items:
        suggestion = suggest_fix(b, history)
        print(Fore.CYAN + f"Broken instance for: {b}")
        if suggestion:
            print(Fore.YELLOW + f"Suggested fix: {suggestion}")
            print(" [1] Accept suggestion")
            print(" [2] Enter custom")
            print(" [0] Skip")
            choice = input("> ").strip()
            if choice == "1":
                fix_map[b] = suggestion
                update_fix_history(b, suggestion)
                continue
            elif choice == "2":
                replacement = input("Enter custom fix: ").strip()
                if replacement:
                    fix_map[b] = replacement
                    update_fix_history(b, replacement)
                continue
            else:
                continue
        else:
            replacement = input(f"Replace '{b}' with: ").strip()
            if replacement:
                fix_map[b] = replacement
                update_fix_history(b, replacement)

    with open(output_path, 'w', encoding='utf-8') as f:
        for k, v in fix_map.items():
            f.write(f"{k} -> {v}\n")

    log(Fore.GREEN + f"✅ Fix map saved: {output_path}")
    return fix_map

def load_fix_map(path):
    fix_map = {}
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            if '->' in line:
                k, v = line.strip().split('->', 1)
                k = k.strip()
                v = v.strip()
                if not k or not v:
                    continue
                fix_map[k] = v
    return fix_map
