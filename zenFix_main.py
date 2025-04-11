import os
from colorama import init, Fore
from pyfiglet import Figlet
from utils.config_loader import load_script_path
from utils.item_validator import scan_valid_items
from utils.file_utils import list_files, get_user_selection
from utils.log_utils import log, log_action, save_log
from utils.menu_utils import clear_screen, pause, print_title
from modules.batch_fix import batch_fix
from modules.check_containers import validate_container_entries
from modules.check_containers_multi import check_all_containers
from modules.scan_broken_instances import scan_broken_instances
from modules.prompt_replacements import prompt_replacements, load_fix_map
from modules.fix_blocks import apply_fix

FOLDERS = {
    "input": "zenfix_input",
    "output": "zenfix_output",
    "instances": "zenfix_instances"
}

init(autoreset=True)

def ensure_folders():
    for path in FOLDERS.values():
        os.makedirs(path, exist_ok=True)
    os.makedirs("zenfix_broken", exist_ok=True)
    os.makedirs("zenfix_log", exist_ok=True)

def show_main_menu():
    clear_screen()
    print_title()
    print(Fore.CYAN + "\n=== zenFix Utility Menu ===")

    print(Fore.LIGHTRED_EX + " [0] Exit")
    print(Fore.YELLOW + " [1] About\n")

    print(" [2] Scan Broken Instances")
    print(" [3] Scan Broken Instances (multi)")
    print(" [4] Prompt Replacement")
    print(" [5] Prompt Replacement (multi)")
    print(" [6] Fix Specific Blocks")
    print(" [7] Fix Specific Blocks (multi)")
    print(" [8] Fix All Blocks")
    print(" [9] Fix All Blocks (multi)\n")

    print(" [10] Batch Fix")
    print(" [11] Check Containers")
    print(" [12] Check Containers (multi)\n")

    print(Fore.LIGHTYELLOW_EX + " [13] Check Item Validation")

def main():
    ensure_folders()
    script_path = load_script_path()
    if script_path:
        scan_valid_items(script_path)


    while True:
        show_main_menu()
        try:
            choice = int(input(Fore.LIGHTGREEN_EX + "\nSelect an option: "))
        except ValueError:
            log(Fore.RED + "❌ Invalid input.")
            pause()
            continue

        if choice == 0:
            break
        elif choice == 1:
            print(Fore.CYAN + "\nzenFix Batch Tool – Utility for batch fixing broken item instances and containers in Gothic .ZEN files. Shamelessly written with ChatGPT by DamianQ.\n")
        elif choice == 2:
            files = list_files(FOLDERS["input"], ".zen")
            if not files:
                log(Fore.RED + "❌ No ZEN files.")
            else:
                selected = get_user_selection(files, "Choose ZEN file:")
                if selected:
                    scan_broken_instances(os.path.join(FOLDERS["input"], selected), FOLDERS["instances"])
        elif choice == 3:
            for file in list_files(FOLDERS["input"], ".zen"):
                scan_broken_instances(os.path.join(FOLDERS["input"], file), FOLDERS["instances"])
        elif choice == 4:
            files = list_files(FOLDERS["instances"], "_instanceList.txt")
            if not files:
                log(Fore.RED + "❌ No instanceList files.")
            else:
                selected = get_user_selection(files, "Choose file:")
                if selected:
                    items = open(os.path.join(FOLDERS["instances"], selected), encoding='utf-8').read().splitlines()
                    prompt_replacements(items, os.path.join(FOLDERS["instances"], selected.replace("_instanceList", "_instanceFix")))
        elif choice == 5:
            for file in list_files(FOLDERS["instances"], "_instanceList.txt"):
                items = open(os.path.join(FOLDERS["instances"], file), encoding='utf-8').read().splitlines()
                prompt_replacements(items, os.path.join(FOLDERS["instances"], file.replace("_instanceList", "_instanceFix")))
        elif choice == 6:
            files = list_files(FOLDERS["instances"], "_instanceFix.txt")
            if not files:
                log(Fore.RED + "❌ No fix files.")
            else:
                selected = get_user_selection(files, "Choose fix file:")
                if selected:
                    fix_map = load_fix_map(os.path.join(FOLDERS["instances"], selected))
                    inst = input("Enter instance name: ").strip()
                    if inst in fix_map:
                        apply_fix(os.path.join(FOLDERS["input"], selected.split("_instanceFix")[0] + ".zen"), {inst: fix_map[inst]}, inst)
        elif choice == 7:
            inst = input("Enter instance name: ").strip()
            for ff in list_files(FOLDERS["instances"], "_instanceFix.txt"):
                fix_map = load_fix_map(os.path.join(FOLDERS["instances"], ff))
                if inst in fix_map:
                    apply_fix(os.path.join(FOLDERS["input"], ff.split("_instanceFix")[0] + ".zen"), {inst: fix_map[inst]}, inst)
        elif choice == 8:
            zens = list_files(FOLDERS["input"], ".zen")
            selected = get_user_selection(zens, "Choose ZEN:")
            if selected:
                name = selected.rsplit(".", 1)[0]
                fix = name + "_instanceFix.txt"
                if fix in list_files(FOLDERS["instances"], "_instanceFix.txt"):
                    fix_map = load_fix_map(os.path.join(FOLDERS["instances"], fix))
                    apply_fix(os.path.join(FOLDERS["input"], selected), fix_map, "InstanceFixed")
        elif choice == 9:
            for file in list_files(FOLDERS["instances"], "_instanceFix.txt"):
                name = file.split("_instanceFix")[0] + ".zen"
                if name in os.listdir(FOLDERS["input"]):
                    fix_map = load_fix_map(os.path.join(FOLDERS["instances"], file))
                    apply_fix(os.path.join(FOLDERS["input"], name), fix_map, "InstanceFixed")
        elif choice == 10:
            batch_fix()
        elif choice == 11:
            files = list_files(FOLDERS["input"], ".zen")
            selected = get_user_selection(files, "Choose ZEN file to scan:")
            if selected:
                validate_container_entries(os.path.join(FOLDERS["input"], selected))
        elif choice == 12:
            check_all_containers()
        elif choice == 13:
            print(Fore.BLUE + f"🧭 Using script path: {script_path}")
            from utils.item_validator import VALID_ITEMS
            print(Fore.MAGENTA + f"🔎 Valid items loaded: {len(VALID_ITEMS)}")
        pause()

    save_log()
    print(Fore.CYAN + "Goodbye!")

if __name__ == "__main__":
    main()
