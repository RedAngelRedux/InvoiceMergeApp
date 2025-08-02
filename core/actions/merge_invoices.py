# actions/merge_invoices.py

menu_id = "merge_invoices"
label_key = "main_menu.merge_invoices"

from core.spinner import Spinner
from core.folders import get_default_folder_paths, validate_folders, create_timestamped_folder
from core.invoice_processor import process_all_folders
from core.waybill import split_waybill_pdfs
from core.merger import merge_all_invoices, override_matching_files
from core.menu_registry import standardize_action_output

def merge_invoices_workflow():
    with Spinner("Processing Invoices..."):
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

def execute():
    return standardize_action_output(merge_invoices_workflow,requires_confirmation=False)
