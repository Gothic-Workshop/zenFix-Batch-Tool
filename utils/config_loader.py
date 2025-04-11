
import os
import xml.etree.ElementTree as ET
from colorama import Fore

CONFIG_PATH = "config.xml"

def load_script_path():
    if not os.path.exists(CONFIG_PATH):
        print(Fore.YELLOW + "⚠ config.xml not found.")
        return None
    try:
        tree = ET.parse(CONFIG_PATH)
        root = tree.getroot()
        scripts_tag = root.find("scripts")
        if scripts_tag is not None:
            path = scripts_tag.get("src")
            if path and os.path.isdir(path):
                print(Fore.GREEN + f"✅ Script path loaded: {path}")
                return path
            else:
                print(Fore.RED + f"❌ Invalid path in config: {path}")
        else:
            print(Fore.RED + "❌ <scripts> tag not found in config.xml")
    except ET.ParseError as e:
        print(Fore.RED + f"❌ XML parse error: {e}")
    return None
