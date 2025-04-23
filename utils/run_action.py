
from utils.menu_utils import clear_screen, pause

def run_action(action_func, *args, **kwargs):
    clear_screen()
    action_func(*args, **kwargs)