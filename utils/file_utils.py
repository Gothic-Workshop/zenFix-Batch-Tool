
import os
from colorama import Fore

def list_files(folder, pattern):
    try:
        files = os.listdir(folder)
    except FileNotFoundError:
        return []
    return [f for f in files if pattern.lower() in f.lower()]

def get_user_selection(options, prompt):
    if not options:
        print(Fore.YELLOW + "⚠️ No options available.")
        return None

    while True:
        print(Fore.CYAN + prompt)  # heading first
        for i, opt in enumerate(options, 1):
            print(f" {i}) {opt}")
        print(" 0) Back")
        try:
            index = int(input("> ")) - 1
        except ValueError:
            print(Fore.RED + "❌ Invalid selection.")
            continue

        if index == -1:
            return None
        if 0 <= index < len(options):
            return options[index]

        print(Fore.RED + "❌ Invalid selection.")

def read_lines(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def write_lines(path, lines):
    with open(path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + "\n")
