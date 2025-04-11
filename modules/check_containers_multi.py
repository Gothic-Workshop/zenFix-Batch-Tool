
import os
from modules.check_containers import validate_container_entries
from utils.log_utils import log
from colorama import Fore

INPUT_FOLDER = "zenfix_input"

def check_all_containers():
    zens = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(".zen")]
    if not zens:
        log(Fore.RED + "❌ No ZEN files in input folder.")
        return
    for z in zens:
        log(Fore.CYAN + f"🔍 Checking: {z}")
        validate_container_entries(os.path.join(INPUT_FOLDER, z))
