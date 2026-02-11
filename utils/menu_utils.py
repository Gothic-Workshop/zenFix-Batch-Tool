import os
from colorama import Fore
from pyfiglet import Figlet

REPO_URL = "https://github.com/Gothic-Workshop/zenFix-Batch-Tool"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input(Fore.CYAN + "\n↩️  Press Enter to continue...")

def print_title():
    f = Figlet(font='slant')  # You can also try 'big', 'block', 'doom', etc.
    print(Fore.CYAN + f.renderText(" zenFix"))
    print(Fore.YELLOW + "Batch Tool - Version 3")


def print_about_info(script_path=None):
    clear_screen()
    print_title()
    print(Fore.CYAN + "\nzenFix Batch Tool")
    print(Fore.WHITE + "Batch utility for finding and fixing broken item and container data in Gothic .ZEN files.")
    print(Fore.WHITE + "It supports scan -> replacement mapping -> fix workflows, plus validation and conversion tools.")
    print(Fore.BLUE + f"\nGitHub: {REPO_URL}")

    if script_path:
        print(Fore.GREEN + f"Loaded script path: {script_path}")
    else:
        print(Fore.YELLOW + "Loaded script path: (not configured)")

    print(Fore.YELLOW + "\nTip: Start with [3] Scan Broken Instances (all ZENs), then [5] Prompt Replacements, then [9] Fix All Blocks.")
