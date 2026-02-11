import os

from colorama import Fore, init

from modules.batch_fix import batch_fix
from modules.check_chest_visuals import check_chest_visuals_single
from modules.check_containers import check_all_containers, validate_container_entries
from modules.convert_zen import convert_zen
from modules.count_vob_visuals import count_vob_visuals_single
from modules.fix_blocks import apply_fix, fix_all_blocks_multi, fix_selected_block
from modules.prompt_replacements import load_fix_map, prompt_replacements
from modules.scan_broken_instances import scan_broken_instances
from utils.config_loader import load_script_path
from utils.file_utils import get_user_selection, list_files
from utils.item_validator import scan_valid_items
from utils.log_utils import log, save_log
from utils.menu_utils import clear_screen, pause, print_about_info, print_title
from utils.run_action import run_action

FOLDERS = {
    "input": "zenfix_input",
    "output": "zenfix_output",
    "instances": "zenfix_instances",
    "broken": "zenfix_broken",
    "log": "zenfix_log",
}

init(autoreset=True)


def ensure_folders():
    for path in FOLDERS.values():
        os.makedirs(path, exist_ok=True)


def _scan_single_zen():
    files = list_files(FOLDERS["input"], ".zen")
    selected = get_user_selection(files, "Choose ZEN file:")
    if selected:
        scan_broken_instances(os.path.join(FOLDERS["input"], selected), FOLDERS["instances"])


def _scan_all_zen():
    files = list_files(FOLDERS["input"], ".zen")
    for file_name in files:
        scan_broken_instances(os.path.join(FOLDERS["input"], file_name), FOLDERS["instances"])


def _prompt_replacement_single():
    files = list_files(FOLDERS["instances"], "_instanceList.txt")
    selected = get_user_selection(files, "Choose file:")
    if not selected:
        return

    selected_path = os.path.join(FOLDERS["instances"], selected)
    with open(selected_path, encoding="utf-8") as source_file:
        broken_instances = source_file.read().splitlines()

    output_path = os.path.join(FOLDERS["instances"], selected.replace("_instanceList", "_instanceFix"))
    prompt_replacements(broken_instances, output_path)


def _prompt_replacement_all():
    files = list_files(FOLDERS["instances"], "_instanceList.txt")
    for file_name in files:
        source_path = os.path.join(FOLDERS["instances"], file_name)
        with open(source_path, encoding="utf-8") as source_file:
            broken_instances = source_file.read().splitlines()

        output_path = os.path.join(FOLDERS["instances"], file_name.replace("_instanceList", "_instanceFix"))
        prompt_replacements(broken_instances, output_path)


def _fix_specific_single():
    files = list_files(FOLDERS["instances"], "_instanceFix.txt")
    selected = get_user_selection(files, "Choose fix file:")
    if not selected:
        return

    fix_map = load_fix_map(os.path.join(FOLDERS["instances"], selected))
    instance_name = input("Enter instance name: ").strip()

    if not instance_name:
        log(Fore.RED + "❌ Instance name cannot be empty.")
        return
    if instance_name not in fix_map:
        log(Fore.RED + f"❌ Instance '{instance_name}' not found in selected fix map.")
        return

    zen_name = selected.split("_instanceFix")[0] + ".zen"
    apply_fix(
        os.path.join(FOLDERS["input"], zen_name),
        {instance_name: fix_map[instance_name]},
        "InstanceFixed",
    )


def _fix_specific_multi():
    instance_name = input("Enter instance name: ").strip()
    if not instance_name:
        log(Fore.RED + "❌ Instance name cannot be empty.")
        return

    matched = 0
    for fix_file in list_files(FOLDERS["instances"], "_instanceFix.txt"):
        fix_map = load_fix_map(os.path.join(FOLDERS["instances"], fix_file))
        if instance_name in fix_map:
            zen_name = fix_file.split("_instanceFix")[0] + ".zen"
            apply_fix(
                os.path.join(FOLDERS["input"], zen_name),
                {instance_name: fix_map[instance_name]},
                "InstanceFixed",
            )
            matched += 1

    if not matched:
        log(Fore.YELLOW + f"⚠️ No matching replacement found for '{instance_name}'.")


def _container_check_single():
    files = list_files(FOLDERS["input"], ".zen")
    selected = get_user_selection(files, "Choose ZEN file to scan:")
    if selected:
        validate_container_entries(os.path.join(FOLDERS["input"], selected))


def _validate_scripts(script_path):
    print(Fore.BLUE + f"🧭 Using script path: {script_path}")
    from utils.item_validator import VALID_ITEMS

    print(Fore.MAGENTA + f"🔎 Valid items loaded: {len(VALID_ITEMS)}")


def show_main_menu():
    clear_screen()
    print_title()

    zen_files = list_files(FOLDERS["input"], ".zen")
    fix_files = list_files(FOLDERS["instances"], "_instanceFix.txt")

    print(Fore.CYAN + "\n=== zenFix Utility Menu ===")
    print(Fore.CYAN + f"Input ZENs: {len(zen_files)} | Fix maps: {len(fix_files)}")

    print(Fore.LIGHTRED_EX + "\n [0] Exit")
    print(Fore.YELLOW + " [1] About")

    print(Fore.LIGHTWHITE_EX + "\n -- Instance Discovery & Mapping --")
    print(" [2] Scan Broken Instances (single ZEN)")
    print(" [3] Scan Broken Instances (all ZENs)")
    print(" [4] Prompt Replacements (single list)")
    print(" [5] Prompt Replacements (all lists)")

    print(Fore.LIGHTWHITE_EX + "\n -- Fix Application --")
    print(" [6] Fix Specific Instance (single ZEN)")
    print(" [7] Fix Specific Instance (all ZENs)")
    print(" [8] Fix All Blocks (single ZEN)")
    print(" [9] Fix All Blocks (all ZENs)")
    print(" [10] Batch Fix (scan + prompt + fix)")

    print(Fore.LIGHTWHITE_EX + "\n -- Validation & Analysis --")
    print(" [11] Check Containers (single ZEN)")
    print(" [12] Check Containers (all ZENs)")
    print(" [13] Check Chest Visuals")
    print(" [14] Count zCVob Visual Usage")
    print(Fore.LIGHTYELLOW_EX + " [15] Validate Scripts")

    print(Fore.LIGHTWHITE_EX + "\n -- Conversion --")
    print(" [16] Convert ZEN between Gothic versions")


def main():
    os.system("title zenFix Batch Tool")

    ensure_folders()
    script_path = load_script_path()
    if script_path:
        scan_valid_items(script_path)

    actions = {
        1: lambda: print_about_info(script_path),
        2: lambda: run_action(_scan_single_zen),
        3: lambda: run_action(_scan_all_zen),
        4: lambda: run_action(_prompt_replacement_single),
        5: lambda: run_action(_prompt_replacement_all),
        6: lambda: run_action(_fix_specific_single),
        7: lambda: run_action(_fix_specific_multi),
        8: lambda: run_action(fix_selected_block),
        9: lambda: run_action(fix_all_blocks_multi),
        10: lambda: run_action(batch_fix),
        11: lambda: run_action(_container_check_single),
        12: lambda: run_action(check_all_containers),
        13: lambda: run_action(check_chest_visuals_single),
        14: lambda: run_action(count_vob_visuals_single),
        15: lambda: _validate_scripts(script_path),
        16: lambda: run_action(convert_zen),
    }

    while True:
        show_main_menu()
        choice_raw = input(Fore.LIGHTGREEN_EX + "\nSelect an option: ").strip().lower()

        if choice_raw in {"0", "q", "quit", "exit"}:
            break

        if not choice_raw.isdigit():
            log(Fore.RED + "❌ Invalid input. Enter a menu number.")
            pause()
            continue

        choice = int(choice_raw)
        action = actions.get(choice)
        if not action:
            log(Fore.RED + "❌ Unknown option.")
            pause()
            continue

        action()
        pause()

    save_log()
    print(Fore.CYAN + "Goodbye!")


if __name__ == "__main__":
    main()
