pyinstaller --onefile --name=invoice_merge_v3.4.exe --add-data "core\\config\\ui_text.json;config" --add-data "core\\actions;core\\actions" main.py
RELEASED ON:  
    Updated RegEx for Rapid invoices to activate whether or not there is a space between ACCOUNT and NO.  Apparently there is a slight difference when printing
        invoices "in bulk" versus "by account number".


pyinstaller --onefile --name=invoice_merge_v3.3.exe --add-data "core\\config\\ui_text.json;config" --add-data "core\\actions;core\\actions" main.py
RELEASED ON:  
    Fixed typo during ENVIONMENT VARIABLE setup; setup_smtp_env.bat
    Added SMTP handshake; excel_handler.py, mailer.py
    Cleaned up formatting; email_invoice.py
    Set InvoiceArchive as default "Sent" folder, if expected Sent folder not found; imap_utils.py


pyinstaller --onefile --name=invoice_merge_v3.2.exe --add-data "core\\config\\ui_text.json;config" --add-data "core\\actions;core\\actions" main.py
RELEASED ON:  2025/08/10
    Added support for "Sent Items"

<!-- pyinstaller --onefile --name=InvoiceMergeAndMail --add-data "core\\config\\ui_text.json;config" --add-data "core\\actions;core\\actions" --hidden-import core.actions.email_invoices  --hidden-import core.actionsm.merge_invoices --hidden-import core.actions.update_settings --hidden-import core.invoice_processor --hidden-import core.waybill --hidden-import core.merger main.py -->


