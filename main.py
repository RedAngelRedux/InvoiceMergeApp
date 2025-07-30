import os
import re
from PyPDF2 import PdfReader, PdfWriter
import fitz #PyMuPDF
import datetime
import msvcrt

def extract_number(text,patterns):
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return None

def split_waybill_pdfs(folder):
    for filename in os.listdir(folder):
        if filename.lower().endswith(".pdf"):
            doc = fitz.open(os.path.join(folder,filename))
            invoice_chunks = []
            current_chunk = []
            current_account = None

            for i in range(len(doc)):
                text = doc[i].get_text()
                acct = extract_number(text,[r'ACCOUNT:\s*([A-Za-z0-9]+)'])

                if acct: #Detected start of new invoice

                    if current_chunk:
                        invoice_chunks.append((current_account,current_chunk))
                    current_chunk = [i]
                    current_account = acct
                else:
                    current_chunk.append(i)

            # Add last chunk
            
            if current_chunk and current_account:
                invoice_chunks.append((current_account,current_chunk))

            # Save each invoice as a separate PDF

            for acct, pages in invoice_chunks:
                out_doc = fitz.open()
                for p in pages:
                    out_doc.insert_pdf(doc, from_page=p, to_page=p)
                out_path = os.path.join(folder,f"{acct}_Waybill.pdf")
                out_doc.save(out_path)     
                if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
                    print(f"✅ File saved and non-empty: {out_path}")
                else:
                    print(f"⚠️ File missing or empty: {out_path}")           
                out_doc.close()

            doc.close()



def save_pages_with_account_number(reader, writer, account_number, suffix, pages, folder):
    output_file_name = f"{account_number}{suffix}.pdf"
    output_file_path = os.path.join(folder, output_file_name)

    if os.path.exists(output_file_path):
        existing_reader = PdfReader(output_file_path)
        for page in existing_reader.pages:
            writer.add_page(page)
            
    for page in pages:
        writer.add_page(reader.pages[page])

    with open(output_file_path, 'wb') as output_file:
        writer.write(output_file)


def rename_and_split_pdf_files(folder):
    for filename in os.listdir(folder):
        old_file_path = os.path.join(folder, filename)
        if filename.lower().endswith('.pdf'):
            if 'mm dental' in filename.lower():
                new_file_path = os.path.join(folder,"25002_UnisonCharges.pdf")
                os.rename(old_file_path,new_file_path)
                print(f"Renamed: {old_file_path} -> {new_file_path}")
            elif 'artidental' in filename.lower():
                new_file_path = os.path.join(folder,"25001_UnisonCharges.pdf")
                os.rename(old_file_path,new_file_path)
                print(f"Renamed: {old_file_path} -> {new_file_path}")
            else:
                reader = PdfReader(old_file_path)
                pages_by_account = {}

                for i, page in enumerate(reader.pages):
                    text = page.extract_text()

                    # Check each pattern
                    patterns_weight = [r'Period: To \d{2}/\d{2}/\d{4} \d{2}/\d{2}/\d{4}(\d+)\n']
                    patterns_rapid = [r'(\d+)\sACCOUNT NO:']
                    patterns_unison = [r'Account No.:\s*(\d+)']
                    patterns_misc = [r'ACCT\s*(\d+)',r'ACCT:\s*(\d+)',r'Acct#:\s+(\w{1,10})',r'ACCT\s*#\s*([A-Za-z0-9]+)']

                    account_number_weight = extract_number(text, patterns_weight)
                    account_number_rapid = extract_number(text, patterns_rapid)
                    account_number_unison = extract_number(text, patterns_unison)
                    account_number_misc = extract_number(text,patterns_misc)

                    if account_number_weight:
                        account_number = account_number_weight
                        suffix = "_WeightCharges"
                    elif account_number_rapid:
                        account_number = account_number_rapid
                        suffix = "_RapidCharges"
                    elif account_number_unison:
                        account_number = account_number_unison
                        suffix = "_UnisonCharges"
                    elif account_number_misc:
                        account_number = account_number_misc
                        if folder == "Detail":
                            suffix = "_Consolidated"
                        else:
                            suffix = "_Miscellaneous"                    
                    else:
                        continue

                    account_pages = pages_by_account.get(account_number, ([], suffix))
                    account_pages[0].append(i)
                    pages_by_account[account_number] = account_pages

                for account_number, (pages, suffix) in pages_by_account.items():
                    writer = PdfWriter()
                    save_pages_with_account_number(reader, writer,account_number,suffix, pages,folder)

            #os.remove(old_file_path)

def rename_pdf_files(folder):

    patterns = [r'#33-\d{7}\s*(\d+)',r'AS OF:\s\d+ \n(\d+)',r'\n(\d{6})\n']
    for filename in os.listdir(folder):
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(folder, filename)
            reader = PdfReader(file_path)
            first_page = reader.pages[0]
            text = first_page.extract_text()
            account_number = extract_number(text,patterns)
            if account_number:
                new_filename = f"{account_number}_{filename}"
                new_file_path = os.path.join(folder, new_filename)
                os.rename(file_path, new_file_path)


def create_timestamped_folder():
    now = datetime.datetime.now()
    timestamped_folder = now.strftime('%y%m_Invoices')
    os.makedirs(timestamped_folder, exist_ok=True)
    return timestamped_folder

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


def main():
    try:
        comet_folder = 'Invoice' # Comet Generated Invoices - Eech File Contains One Page for One Account
        consolidated_list_folder = "Detail" # Comet's Consolidated Report - Each File Contains Multiple Pages for Multiple Accounts
        weights_folder = "Weights" # Unison Generated Weight Charges Report - Each File Contains Multiple Pages for Multiple Accounts
        rapid_folder = "Rapid" # Rapid Generated Invoices - Each File Contains Multiple Pages for Multiple Accounts
        unison_folder = "Unison" # Unison Generated Invoices - Each File Contains Multiple Pages for Multiple Accounts
        misc_folder = 'Misc' # Files Generated from Multiple Sources Not Covered Above - Each File Contains Multiple Pages for Multiple Accounts
        waybill_folder = "Waybill" # Files in this folder have an identifiale account number on the first page of each invoice but not on subsequent pages

        # Check if all expected folders are present
        for folder in [comet_folder, consolidated_list_folder,weights_folder,rapid_folder,unison_folder,misc_folder]:
            if not os.path.exists(folder):
                print(f"Error: The folder '{folder}' is missing.")
                return    

        # Process files in each folder
        rename_pdf_files(comet_folder)
        for folder in [consolidated_list_folder,weights_folder,rapid_folder,unison_folder,misc_folder]:
            rename_and_split_pdf_files(folder)
        split_waybill_pdfs(waybill_folder)
        
        # Using the comet_folder as the source of truth, match each invoice with the backups found in all folders
        timestamped_folder = create_timestamped_folder()
        for filename in os.listdir(comet_folder):
            if filename.lower().endswith('.pdf'):
                account_number = filename.split('_')[0]
                merge_pdfs(account_number,timestamped_folder,comet_folder,consolidated_list_folder,weights_folder,rapid_folder,unison_folder,misc_folder,waybill_folder)
        
        override_matching_files(comet_folder,timestamped_folder)
        print("Current working directory: ", os.getcwd())
        print("Press any key to continue...")
    except Exception as e:
        print(f"An unexpected error occured:  {e}")
    finally:
        msvcrt.getch() # Wait for user to press any key (no ENTER requiredj)


if __name__ == '__main__':
    main()