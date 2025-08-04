import os
import datetime

def validate_folders(folders):
    for key, path in folders.items():
        if not os.path.exists(path):            
            return [False, key]
    return [True, ""]

def get_default_folder_paths():
    
    # These paths are hosd-coded for now, but later they will be configurable
    comet = 'Invoice' # Comet Generated Invoices - Eech File Contains One Page for One Account
    consolidated_list = "Detail" # Comet's Consolidated Report - Each File Contains Multiple Pages for Multiple Accounts
    weights = "Weights" # Unison Generated Weight Charges Report - Each File Contains Multiple Pages for Multiple Accounts
    rapid = "Rapid" # Rapid Generated Invoices - Each File Contains Multiple Pages for Multiple Accounts
    unison = "Unison" # Unison Generated Invoices - Each File Contains Multiple Pages for Multiple Accounts
    misc = 'Misc' # Files Generated from Multiple Sources Not Covered Above - Each File Contains Multiple Pages for Multiple Accounts
    waybill = "Waybill" # Files in this folder have an identifiale account number on the first page of each invoice but not on subsequent pages

    folder_names = {
        'comet': comet,
        'consolidated_list': consolidated_list,
        'weights': weights,
        'rapid': rapid,
        'unison': unison,
        'misc': misc,
        'waybill': waybill
    }

    return folder_names

def generate_timestamped_folder_name():
    now = datetime.datetime.now()
    return now.strftime('%y%m_Invoices')

def create_timestamped_folder(foldername=None):
    # now = datetime.datetime.now()
    # timestamped_folder = now.strftime('%y%m_Invoices')

    timestamped_folder = foldername if foldername is not None else generate_timestamped_folder_name()
    #timestamped_folder = generate_timestamped_folder_name()
    os.makedirs(timestamped_folder, exist_ok=True)
    return timestamped_folder
