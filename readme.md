pyinstaller --onefile --name=invoice_merge_v3.2.exe --add-data "core\\config\\ui_text.json;config" --add-data "core\\actions;core\\actions" main.py

    Added support for "Sent Items"

<!-- pyinstaller --onefile --name=InvoiceMergeAndMail --add-data "core\\config\\ui_text.json;config" --add-data "core\\actions;core\\actions" --hidden-import core.actions.email_invoices  --hidden-import core.actionsm.merge_invoices --hidden-import core.actions.update_settings --hidden-import core.invoice_processor --hidden-import core.waybill --hidden-import core.merger main.py -->


