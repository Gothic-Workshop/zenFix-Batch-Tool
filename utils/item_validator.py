import os
import re
from colorama import Fore

VALID_ITEMS = set()

def scan_valid_items(script_path):
    global VALID_ITEMS
    VALID_ITEMS.clear()
    pattern = re.compile(r'\bINSTANCE\s+(\w+)\s*\(\s*C_Item\s*\)', re.IGNORECASE)

    total_files = 0
    total_matches = 0

    print(Fore.MAGENTA + f"\n🔍 Scanning script path: {script_path}\n")

    for root_dir, _, files in os.walk(script_path):
        for file in files:
            if file.lower().endswith(".d"):
                path = os.path.join(root_dir, file)
                found = []
                try:
                    with open(path, 'r', encoding='windows-1250') as f:
                        for line in f:
                            m = pattern.match(line)
                            if m:
                                found.append(m.group(1))
                except Exception as e:
                    print(Fore.YELLOW + f"⚠️ Could not read {file}: {e}")
                    continue

                if found:
                    VALID_ITEMS.update(i.lower() for i in found)
                    total_files += 1
                    total_matches += len(found)
                    sample = ', '.join(found[:5])
                    print(Fore.GREEN + f"✅ {file}: {len(found)} items ({sample}{'...' if len(found) > 5 else ''})")

    print(Fore.CYAN + f"\n📦 Finished. {total_matches} total items found from {total_files} files.")
    print(Fore.MAGENTA + f"💾 Items stored in memory: {len(VALID_ITEMS)}\n")

def validate_item(name):
    return name.lower() in VALID_ITEMS
