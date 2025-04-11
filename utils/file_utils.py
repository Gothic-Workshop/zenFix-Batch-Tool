
import os
from colorama import Fore

def list_files(folder, pattern):
    return [f for f in os.listdir(folder) if pattern.lower() in f.lower()]

def get_user_selection(options, prompt):
    for i, opt in enumerate(options, 1):
        print(f" {i}) {opt}")
    print(" 0) Back")
    print(Fore.CYAN + prompt)
    try:
        index = int(input("> ")) - 1
        if index == -1:
            return None
        elif 0 <= index < len(options):
            return options[index]
    except ValueError:
        pass
    print(Fore.RED + "❌ Invalid selection.")
    return get_user_selection(options, prompt)

def read_lines(path):
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def write_lines(path, lines):
    with open(path, 'w', encoding='utf-8') as f:
        for line in lines:
            f.write(line + "\n")
