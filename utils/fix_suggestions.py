
import os
import json
import difflib

HISTORY_FILE = "fix_history.json"

def load_fix_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_fix_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, indent=2)

def suggest_fix(vob_name, history):
    if vob_name in history:
        return history[vob_name]

    candidates = difflib.get_close_matches(vob_name, history.keys(), n=1, cutoff=0.6)
    if candidates:
        return history[candidates[0]]
    return None

def update_fix_history(vob_name, item_instance):
    history = load_fix_history()
    if vob_name not in history:
        history[vob_name] = item_instance
        save_fix_history(history)
