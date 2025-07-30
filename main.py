import os
import datetime
import msvcrt

from core.folders import get_default_folder_paths, validate_folders
from core.invoice_processor import extract_number, process_all_folders
from core.waybill import split_waybill_pdfs
from core.merger import merge_all_invoices, override_matching_files

def create_timestamped_folder():
    now = datetime.datetime.now()
    timestamped_folder = now.strftime('%y%m_Invoices')
    os.makedirs(timestamped_folder, exist_ok=True)
    return timestamped_folder

def main():

    try:

        # Get Default Folder Configuration
        folders = get_default_folder_paths()        
        
        # Ensure All Expected Folders Are Present
        valid, key = validate_folders(folders)
        if not valid:
            print(f"Error: The '{key}' folder is missing.")
            return        
        
        # Process and Rename PDF Files
        process_all_folders(folders)

        # Special Handling By Batch Instead of By Page
        split_waybill_pdfs(folders['waybill'])
        
        # Merge Files Using the comet_folder as the source of truth
        timestamped_folder = create_timestamped_folder()
        merge_all_invoices(folders,timestamped_folder)
        override_matching_files(folders['comet'],timestamped_folder)

        # Provide Successful Ending Text to the User
        print("Current working directory: ", os.getcwd())
        print("Press any key to continue...")

    except Exception as e:

        print(f"An unexpected error occured:  {e}")

    finally:

        msvcrt.getch() # Wait for user to press any key (no ENTER requiredj)

if __name__ == '__main__':
    main()