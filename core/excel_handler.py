import os
import re

import openpyxl

from core.email_builder import load_template, build_message, replace_placeholders
from core.mailer import send_email

def find_attachment(folder, account):
    pattern = re.compile(rf"^{re.escape(account)}\sINV\s.*\.pdf$", re.IGNORECASE)
    for fname in os.listdir(folder):
        if pattern.match(fname):
            return os.path.join(folder, fname)
    return None

def load_sheet(file_name, tab_name):
    wb = openpyxl.load_workbook(file_name)
    if tab_name not in wb.sheetnames:
        raise ValueError(f"Tab '{tab_name}' not found.")
    return wb, wb[tab_name]

def read_email_rows(sheet, folder):
    from_email = sheet['A1'].value
    records = []
    for i, row in enumerate(sheet.iter_rows(min_row=3, values_only=True), start=3):
        account, to, cc, bcc, status = row
        if status and status.lower().startswith("sent"):
            continue
        attachment = find_attachment(folder, str(account))
        records.append({
            "account": account,
            "to": to.split(";") if to else [],
            "cc": cc.split(";") if cc else [],
            "bcc": bcc.split(";") if bcc else [],
            "status_row": i,
            "attachment": attachment
        })
    return from_email, records

def record_status(sheet, row_index, result):
    col = "E"
    cell = sheet[f"{col}{row_index}"]
    cell.value = result
    if result.startswith("Error"):
        cell.font = openpyxl.styles.Font(color="FF0000")

def email_all_invoices(EXCEL_FILE, tab, TIMESTAMPED_FOLDER):
    wb, sheet = load_sheet(EXCEL_FILE, tab)
    from_email, rows = read_email_rows(sheet, TIMESTAMPED_FOLDER)
    subject, body, signature = load_template(tab)

    subject_template = subject
    body_template = body
    signature_template = signature
    for row in rows:        
        data = {
            "ACCOUNT": row["account"]
        }
        subject = replace_placeholders(subject_template,data)
        body = replace_placeholders(body_template,data)
        signature = replace_placeholders(signature_template,data)

        msg = build_message(from_email, row["to"], row["cc"], row["bcc"], subject, body, signature, row["attachment"])
        result = send_email(msg)
        record_status(sheet, row["status_row"], result)

    wb.save(EXCEL_FILE)
