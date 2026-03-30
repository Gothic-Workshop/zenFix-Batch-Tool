import os
import tomllib
from colorama import Fore

CONFIG_PATH = "config.toml"

DEFAULT_CONFIG = {
    "paths": {
        "scripts": "",
        "gothiczen": "",
    },
    "features": {
        "batch_fix": True,
        "container_check": True,
        "chest_validation": True,
        "recommendation_system": True,
    },
    "focus": {
        "name_prefixes": [
            "MOBNAME_GRAVE",
            "MOBNAME_CHEST",
        ],
    },
    "chests": {
        "validate_visuals": True,
        "validate_key_instance": True,
        "validate_picklock": True,
        "report_impossible_locked_chests": True,
        "auto_fix_wrong_locked_visuals": False,
        "visual_map": {
            "CHESTBIG_OCCHESTLARGELOCKED.MDS": "CHESTBIG_OCCHESTLARGE.MDS",
            "CHESTBIG_OCCHESTMEDIUMLOCKED.MDS": "CHESTBIG_OCCHESTMEDIUM.MDS",
            "CHESTBIG_OCCRATELARGELOCKED.MDS": "CHESTBIG_OCCRATELARGE.MDS",
            "CHESTSMALL_OCCHESTSMALLLOCKED.MDS": "CHESTSMALL_OCCHESTSMALL.MDS",
            "CHESTSMALL_OCCRATESMALLLOCKED.MDS": "CHESTSMALL_OCCRATESMALL.MDS",
            "CHESTSMALL_NW_POOR_LOCKED.MDS": "CHESTSMALL_NW_POOR_OPEN.MDS",
            "CHESTBIG_NW_RICH_LOCKED.MDS": "CHESTBIG_NW_RICH_OPEN.MDS",
            "CHESTBIG_NW_NORMAL_LOCKED.MDS": "CHESTBIG_NW_NORMAL_OPEN.MDS",
            "CHESTBIG_ADD_STONE_LOCKED.MDS": "CHESTBIG_ADD_STONE_OPEN.MDS",
        },
    },
    "validation": {
        "case_sensitive": False,
        "normalize_whitespace": True,
        "encoding": "windows-1252",
    },
    "history": {
        "file": "fix_history.json",
        "max_suggestions": 3,
        "use_similarity": True,
    },
    "directories": {
        "input": "zenFix_Input",
        "output": "zenFix_Output",
        "instances": "zenFix_Instances",
        "broken": "zenFix_Broken",
        "logs": "zenFix_Log",
    },
    "logging": {
        "enabled": True,
        "per_zen_log": True,
        "minimal_format": True,
    },
}


def _deep_merge(base, override):
    merged = dict(base)
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def load_config():
    if not os.path.exists(CONFIG_PATH):
        print(Fore.YELLOW + f"⚠ {CONFIG_PATH} not found. Using defaults.")
        return DEFAULT_CONFIG

    with open(CONFIG_PATH, "rb") as file:
        parsed = tomllib.load(file)

    return _deep_merge(DEFAULT_CONFIG, parsed)


def load_script_path():
    path = load_config().get("paths", {}).get("scripts", "")
    if not path:
        print(Fore.YELLOW + "⚠ No scripts path configured in config.toml.")
        return None
    if not os.path.isdir(path):
        print(Fore.RED + f"❌ Invalid scripts path in config.toml: {path}")
        return None

    print(Fore.GREEN + f"✅ Script path loaded: {path}")
    return path


def load_focusname_prefixes():
    prefixes = load_config().get("focus", {}).get("name_prefixes", [])
    return [item.strip() for item in prefixes if isinstance(item, str) and item.strip()]


def load_gothiczen_path():
    return load_config().get("paths", {}).get("gothiczen", "")


def load_directories():
    return load_config().get("directories", {}).copy()


def load_chest_config():
    return load_config().get("chests", {}).copy()


def load_feature_flags():
    return load_config().get("features", {}).copy()
