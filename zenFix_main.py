import os
from colorama import init, Fore
from pyfiglet import Figlet

from utils.config_loader import load_script_path
from utils.item_validator import scan_valid_items
from utils.file_utils import list_files, get_user_selection
from utils.log_utils import log, log_action, save_log
from utils.menu_utils import clear_screen, pause, print_title
from utils.run_action import run_action

from modules.batch_fix import batch_fix
from modules.check_chest_visuals import check_chest_visuals_single
from modules.check_containers import validate_container_entries, check_all_containers
from modules.scan_broken_instances import scan_broken_instances
from modules.prompt_replacements import prompt_replacements, load_fix_map
from modules.fix_blocks import apply_fix, fix_selected_block, fix_all_blocks_multi
from modules.convert_zen import convert_zen


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
    print(" [5] Prompt Replacement (multi)\n")

    print(" [6] Fix Specific Blocks")
    print(" [7] Fix Specific Blocks (multi)")
    print(" [8] Fix All Blocks")
    print(" [9] Fix All Blocks (multi)")
    print(" [10] Batch Fix\n")

    print(" [11] Check Containers")
    print(" [12] Check Containers (multi)")
    print(" [13] Check Chest Visuals\n")

    print(" [14] Convert ZEN between Gothic versions\n")

    print(Fore.LIGHTYELLOW_EX + " [15] Validate Scripts")

def main():
    os.system("title zenFix Batch Tool")

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
            clear_screen()
            print_title()
            print(Fore.CYAN + "\nzenFix Batch Tool – Utility for batch fixing broken item instances and containers in Gothic .ZEN files.\nShamelessly written with ChatGPT by DamianQ.")
            print(Fore.BLUE + "\n\nGitHub Repo: https://github.com/Gothic-Workshop/zenFix-Batch-Tool\n\nGothicZEN made by withmorten")
        elif choice == 2:
            run_action(lambda: (
                lambda files=list_files(FOLDERS["input"], ".zen"):
                    scan_broken_instances(os.path.join(FOLDERS["input"], selected), FOLDERS["instances"])
                    if (selected := get_user_selection(files, "Choose ZEN file:")) else None
            )())

        elif choice == 3:
            run_action(lambda: [
                scan_broken_instances(os.path.join(FOLDERS["input"], file), FOLDERS["instances"])
                for file in list_files(FOLDERS["input"], ".zen")
            ])

        elif choice == 4:
            run_action(lambda: (
                lambda files=list_files(FOLDERS["instances"], "_instanceList.txt"):
                    prompt_replacements(
                        open(os.path.join(FOLDERS["instances"], selected), encoding='utf-8').read().splitlines(),
                        os.path.join(FOLDERS["instances"], selected.replace("_instanceList", "_instanceFix"))
                    )
                    if (selected := get_user_selection(files, "Choose file:")) else None
            )())

        elif choice == 5:
            run_action(lambda: [
                prompt_replacements(
                    open(os.path.join(FOLDERS["instances"], file), encoding='utf-8').read().splitlines(),
                    os.path.join(FOLDERS["instances"], file.replace("_instanceList", "_instanceFix"))
                )
                for file in list_files(FOLDERS["instances"], "_instanceList.txt")
            ])

        elif choice == 6:
            run_action(lambda: (
                lambda files=list_files(FOLDERS["instances"], "_instanceFix.txt"):
                    (
                        lambda fix_map=load_fix_map(os.path.join(FOLDERS["instances"], selected)):
                            (inst := input("Enter instance name: ").strip()) and
                            apply_fix(
                                os.path.join(FOLDERS["input"], selected.split("_instanceFix")[0] + ".zen"),
                                {inst: fix_map[inst]},
                                inst
                            )
                        if (selected := get_user_selection(files, "Choose fix file:")) else None
                    )()
            )())

        elif choice == 7:
            run_action(lambda: (
                (inst := input("Enter instance name: ").strip()) and [
                    apply_fix(
                        os.path.join(FOLDERS["input"], ff.split("_instanceFix")[0] + ".zen"),
                        {inst: fix_map[inst]},
                        inst
                    )
                    for ff in list_files(FOLDERS["instances"], "_instanceFix.txt")
                    if (fix_map := load_fix_map(os.path.join(FOLDERS["instances"], ff))) and inst in fix_map
                ]
            ))

        elif choice == 8:
            run_action(lambda: fix_selected_block())

        elif choice == 9:
            run_action(fix_all_blocks_multi)

        elif choice == 10:
            run_action(batch_fix)

        elif choice == 11:
            run_action(lambda: (
                lambda files=list_files(FOLDERS["input"], ".zen"):
                    validate_container_entries(os.path.join(FOLDERS["input"], selected))
                if (selected := get_user_selection(files, "Choose ZEN file to scan:")) else None
            )())

        elif choice == 12:
            run_action(check_all_containers)

        elif choice == 13:
            run_action(check_chest_visuals_single)

        elif choice == 14:
            run_action(convert_zen)

        elif choice == 15:
            print(Fore.BLUE + f"🧭 Using script path: {script_path}")
            from utils.item_validator import VALID_ITEMS
            print(Fore.MAGENTA + f"🔎 Valid items loaded: {len(VALID_ITEMS)}")

        pause()

    save_log()
    print(Fore.CYAN + "Goodbye!")

if __name__ == "__main__":
    main()
