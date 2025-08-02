# actions/email_invoices.py

menu_id = "email_invoices"
label_key = "main_menu.email_invoices"

from core.spinner import Spinner
from core.folders import create_timestamped_folder
from core.excel_handler import email_all_invoices
from core.menu_registry import standardize_action_output

def email_invoices_workflow(data):
    #Confirm that the Excel file exists
    #Confirm that the timestamped directory exists
    while True:
        tab = input("Enter Group Name to Email: ").strip()
        with Spinner(f"Sending emails for group {tab}"):
            email_all_invoices(data["EXCEL_FILE"],tab,data["timestamped_folder"])
        print(f"All messages processed for Group {tab}\n")
        choice = input("Press 1 to email another group or [ESC] to return to the Main Menu: ").strip()
        if choice != "1":
            break    

def execute():    
    answers = {
        "EXCEL_FILE": "email_map.xlsx",
        "timestamped_folder": create_timestamped_folder()
    }
    return standardize_action_output(lambda: email_invoices_workflow(answers),answers,requires_confirmation=False)