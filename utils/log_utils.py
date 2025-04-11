
import os
from datetime import datetime
import re
from colorama import Fore

LOG_LINES = []
LOG_FOLDER = "zenfix_log"

def log(line):
    print(line)
    LOG_LINES.append(line)

def log_action(action, target, status="success", detail=""):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] ({action}) {target} – {status}"
    if detail:
        entry += f": {detail}"
    LOG_LINES.append(entry)

def strip_ansi(text):
    return re.sub(r'\x1b\[[0-9;]*m', '', text)

def save_log():
    if not LOG_LINES:
        return
        
    os.makedirs(LOG_FOLDER, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    path = os.path.join(LOG_FOLDER, f"zenFix_Log_{timestamp}.txt")
    with open(path, 'w', encoding='utf-8') as f:
        for entry in LOG_LINES:
            f.write(strip_ansi(entry) + "\n")
    print(Fore.CYAN + f"📝 Log saved to: {path}")
