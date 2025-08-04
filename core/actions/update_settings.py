# actions/update_settings.py

menu_id = "update_settings"
label_key = "main_menu.update_settings"

from core.utils.error_handler import non_fatal
from core.config_loader import render_message

def update_setings_workflow(data):
    # do actual work here
    return

def execute():
    # gather necessary data and return pointer to action method
    non_fatal(
        render_message("Update Settings is not yet implemented.",feature="Update Settings")
    )
    return None