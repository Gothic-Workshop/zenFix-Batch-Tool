import os
import subprocess
from utils.config_loader import load_gothiczen_path
from utils.file_utils import list_files, get_user_selection
from utils.log_utils import log
from colorama import Fore

INPUT_FOLDER = "zenfix_input"
OUTPUT_FOLDER = "zenfix_output"

VERSIONS = {
    "1": ("101", "Gothic 1 Demo"),
    "2": ("108", "Gothic 1"),
    "3": ("130", "Gothic 2"),
    "4": ("26", "Night of the Raven")
}

def convert_zen():
    gothiczen = load_gothiczen_path()
    if not os.path.isfile(gothiczen):
        log(Fore.RED + f"? GothicZEN.exe not found at: {gothiczen}")
        return

    files = list_files(INPUT_FOLDER, ".zen")
    if not files:
        log(Fore.RED + "? No ZEN files found in input folder.")
        return

    selected = get_user_selection(files, "Select a ZEN file to convert:")
    if not selected:
        return

    print(Fore.CYAN + "\nSource version:")
    for key, (code, name) in VERSIONS.items():
        print(f" {key}) {name} ({code})")
    src_key = input("Choose source version [1-4]: ").strip()

    print(Fore.CYAN + "\nTarget version:")
    for key, (code, name) in VERSIONS.items():
        print(f" {key}) {name} ({code})")
    tgt_key = input("Choose target version [1-4]: ").strip()

    if src_key not in VERSIONS or tgt_key not in VERSIONS:
        log(Fore.RED + "? Invalid version selection.")
        return

    src_ver = VERSIONS[src_key][0]
    tgt_ver = VERSIONS[tgt_key][0]

    input_path = os.path.join(INPUT_FOLDER, selected)
    name_wo_ext = os.path.splitext(selected)[0]
    output_name = f"{name_wo_ext}_{tgt_ver}.ZEN"
    output_path = os.path.join(OUTPUT_FOLDER, output_name)

    command = [
        gothiczen,
        src_ver,
        tgt_ver,
        f'"{input_path}"',
        f'"{output_path}"'
    ]

    try:
        subprocess.run(" ".join(command), shell=True, check=True)
        log(Fore.GREEN + f"? Converted: {selected} ? {output_name}")
    except subprocess.CalledProcessError as e:
        log(Fore.RED + f"? Conversion failed: {e}")
