# actions/email_invoices.py

menu_id = "email_invoices"
label_key = "main_menu.email_invoices"

from pathlib import Path

from core.folders import create_timestamped_folder, generate_timestamped_folder_name
from core.excel_handler import email_all_invoices
from core.menu_registry import standardize_action_output
from core.utils.error_handler import non_fatal
from core.utils.uiux import prompt_filename, file_exists, folder_exists
from core.utils.pause import pause

def email_invoices_workflow(data):
    #Confirm that the Excel file exists    
    #Confirm that the timestamped directory exists
    try:
        while True:
            tab = input("Enter Group Name to Email: ").strip()
            email_all_invoices(data["EXCEL_FILE"],tab,data["timestamped_folder"])
            print(f"All messages processed for Group {tab}\n")
            choice = input("Press 1 to email another group or any other key to return to the Main Menu: ").strip()
            if choice == "1": continue
            else:  return True
    except Exception as e:
        non_fatal(f" {e} ")
        return True

def execute():

    excel_file = "email_map.xlsx"
    timestamped_folder = generate_timestamped_folder_name()
        
    if not file_exists(excel_file):
        excel_file = prompt_filename(
            prompt="Enter file name of the Excel mapper",
            default=excel_file,
            validate_exists=True,
            allowed_extensions=[".xlsx"]
        )
        if excel_file is None: # Operation was canceled by the user
            pause()
            return None
    
    if not folder_exists(timestamped_folder):
        timestamped_folder = prompt_filename(
            prompt="Enter name of the attachement folder",
            default=timestamped_folder
        )
        if timestamped_folder is None: # Operation was canceled by the user
            pause()
            return None
        else:
            create_timestamped_folder(timestamped_folder)

    answers = {
        "EXCEL_FILE": excel_file,
        "timestamped_folder": timestamped_folder
    }

    return standardize_action_output(lambda: email_invoices_workflow(answers),answers,requires_confirmation=False)
