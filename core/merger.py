import os
import re
import fitz
import datetime

from core.invoice_processor import extract_number

def merge_pdfs(account_number, output_folder, *input_folders):
    comet_folder,consolidated_list_folder,weights_folder,rapid_folder,unison_folder,misc_folder,waybill_folder = input_folders
    merger = fitz.open()
    account_found = False
    invoice_number = ""
    invoice_date = ""
    patterns = [r'\nCAL [TCL]-\d+\n(\d{6})\n[A-Za-z]+',r'\n(\d{6})\n']  # MMDDYY

    def add_pages_from_folder(folder):
        nonlocal account_found, invoice_number, invoice_date
        for filename in os.listdir(folder):
            if filename.startswith(account_number) and filename.lower().endswith('.pdf'):
                account_found = True
                file_path = os.path.join(folder, filename)
                doc = fitz.open(file_path)
                if folder == comet_folder and doc.page_count > 0:
                    match = re.search(r'_[TCL](\d+)', filename)
                    #invoice_number = filename.split('T')[1].split('.')[0]
                    invoice_number = match.group(1)
                    # Process first page
                    first_page = doc[0]
                    text = first_page.get_text()
                    if not invoice_date:
                        invoice_date = extract_number(text, patterns)
                merger.insert_pdf(doc)
                doc.close()

    add_pages_from_folder(comet_folder)
    add_pages_from_folder(waybill_folder)
    add_pages_from_folder(consolidated_list_folder)
    add_pages_from_folder(weights_folder)
    add_pages_from_folder(rapid_folder)
    add_pages_from_folder(unison_folder)
    add_pages_from_folder(misc_folder)
    
    # Write the merged file or copy the Comet file if no matches found
    merged_filename = f"{account_number} INV {invoice_number} {invoice_date}.pdf"
    merged_filepath = os.path.join(output_folder, merged_filename)

    if account_found:
        merger.save(merged_filepath)
    else:
        comet_file_path = os.path.join(comet_folder, f"{account_number}_*.pdf")
        for filename in os.listdir(comet_folder):
            if filename.startswith(account_number) and filename.lower().endswith('.pdf'):
                comet_file_path = os.path.join(comet_folder, filename)
                final_filename = f"{account_number} INV 123456 MMDDYY.pdf"
                final_filepath = os.path.join(output_folder, final_filename)
                with open(comet_file_path, 'rb') as src, open(final_filepath, 'wb') as dst:
                    dst.write(src.read())

def merge_all_invoices(folders,timestamped_folder):
    for filename in os.listdir(folders['comet']):
        if filename.lower().endswith('.pdf'):
            account_number = filename.split('_')[0]
            merge_pdfs(account_number,timestamped_folder,folders['comet'],folders['consolidated_list'],folders['weights'],folders['rapid'],folders['unison'],folders['misc'],folders['waybill'])

def override_matching_files(comet_folder, timestamped_folder):
    for comet_filename in os.listdir(comet_folder):
        if comet_filename.lower().endswith('.pdf'):
            # Extract account number from comet file name (AAAAA_XNNNNNN.pdf)
            comet_parts = comet_filename.split('_')
            if len(comet_parts) < 2:
                continue  # Skip files that don't match the expected naming convention
            
            comet_account = comet_parts[0]  # Extract account number
            comet_suffix = comet_parts[1]   # Extract suffix (XNNNNNN.pdf)

            # Loop through timestamped_folder to find a matching file
            for timestamped_filename in os.listdir(timestamped_folder):
                if timestamped_filename.lower().endswith('.pdf') and timestamped_filename.startswith(comet_account):
                    # Matching account number found
                    timestamped_file_path = os.path.join(timestamped_folder, timestamped_filename)
                    comet_file_path = os.path.join(comet_folder, comet_filename)
                    
                    # Generate new filename for the overridden file by dropping AAAAA_
                    new_filename = comet_suffix  # Drop the prefix (AAAAA_)
                    new_file_path = os.path.join(comet_folder, new_filename)

                    # Copy and replace the file using fitz
                    try:
                        with fitz.open(timestamped_file_path) as src_doc:
                            with fitz.open() as new_doc:
                                new_doc.insert_pdf(src_doc)
                                new_doc.save(new_file_path)
                                print(f"Overridden: {comet_file_path} -> {new_file_path}")

                        # Delete the original file in comet_folder
                        os.remove(comet_file_path)
                        print(f"Deleted: {comet_file_path}")

                    except Exception as e:
                        print(f"Error processing file '{timestamped_filename}': {e}")
