import os
import re
from PyPDF2 import PdfReader, PdfWriter

def extract_number(text,patterns):
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)
    return None

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

def process_all_folders(folders):
    rename_pdf_files(folders['comet'])
    for folder in [folders['consolidated_list'],folders['weights'],folders['rapid'],folders['unison'],folders['misc']]:
        rename_and_split_pdf_files(folder)
