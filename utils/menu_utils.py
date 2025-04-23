
import os
from colorama import Fore
from pyfiglet import Figlet

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    input(Fore.CYAN + "\n↩️  Press Enter to continue...")

def print_title():
    #print(Fore.CYAN + "zenFix Batch Tool - Version 3")
    f = Figlet(font='slant')  # You can also try 'big', 'block', 'doom', etc.
    print(Fore.CYAN + f.renderText(" zenFix"))
    print(Fore.YELLOW + "Batch Tool - Version 2")
