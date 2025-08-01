# actions/email_invoices.py

menu_id = "email_invoices"
label_key = "main_menu.email_invoices"

from core.spinner import Spinner
from core.folders import create_timestamped_folder
from core.excel_handler import email_all_invoices


def execute():

    # stop_event = threading.Event()
    # spinner_thread = threading.Thread(target=spinner, args=("Starting Process",stop_event))
    # spinner_thread.start()

    # Email Invoices
    EXCEL_FILE = "email_map.xlsx"
    timestamped_folder = create_timestamped_folder()
    while True:
        tab = input("Enter Group Name to Email: ").strip()
        with Spinner(f"Sending emails for group {tab}"):
            email_all_invoices(EXCEL_FILE,tab,timestamped_folder)
        print(f"All messages processed for Group {tab}\n")
        choice = input("Press 1 to email another group or 2 to return to the Main Menu: ").strip()
        if choice != "1":
            break

    # stop_event.set()
    # spinner_thread.join()
    # time.sleep(0.2)
