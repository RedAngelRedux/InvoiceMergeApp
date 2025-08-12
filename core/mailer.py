import os
import smtplib
import mimetypes

from contextlib import contextmanager
from email.message import EmailMessage
from datetime import datetime
from core.config_loader import SMTP_CONFIG, IMAP_CONFIG
from core.utils.imap_utils import imap_connection, archive_sent_email

def build_email_message(payload):
    msg = EmailMessage()

    # Basic headers
    msg["From"] = payload["from"]
    msg["To"] = ", ".join(payload["to"]) if isinstance(payload["to"], list) else payload["to"]
    if payload.get("cc"):
        msg["Cc"] = ", ".join(payload["cc"]) if isinstance(payload["cc"], list) else payload["cc"]
    if payload.get("bcc"):
        msg["Bcc"] = ", ".join(payload["bcc"]) if isinstance(payload["bcc"], list) else payload["bcc"]
    msg["Subject"] = payload["subject"]

    # Body
    msg.set_content(payload["body"])

    # Attachment (optional)
    attachment = payload.get("attachment")
    if attachment:
        if isinstance(attachment, str) and os.path.isfile(attachment):
            # Guess MIME type
            mime_type, _ = mimetypes.guess_type(attachment)
            maintype, subtype = mime_type.split("/") if mime_type else ("application", "octet-stream")

            with open(attachment, "rb") as f:
                file_data = f.read()
                file_name = os.path.basename(attachment)
                msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=file_name)
        elif isinstance(attachment, bytes):
            # If it's already bytes, attach it directly
            msg.add_attachment(attachment, maintype="application", subtype="octet-stream", filename="attachment.bin")

    return msg

def send_email(message):

    host = SMTP_CONFIG["host"]
    port = SMTP_CONFIG["port"]
    # user = SMTP_CONFIG["user"]
    user = message["from"]
    # password = SMTP_CONFIG["password"]
    password = message["password"]
    
    try:
        # msg = EmailMessage()
        # msg["From"] = message["from"]
        # msg["To"] = ", ".join(message["to"])
        # if message.get("cc"):
        #     msg["Cc"] = ", ".join(message["cc"])
        # if message.get("bcc"):
        #     msg["Bcc"] = ", ".join(message["bcc"])
        # msg["Subject"] = message["subject"]
        # msg.set_content(message["body"])

        # if message.get("attachment"):
        #     with open(message["attachment"], "rb") as f:
        #         msg.add_attachment(
        #             f.read(), 
        #             maintype="application", 
        #             subtype="pdf",
        #             filename=os.path.basename(message["attachment"]))
        msg = build_email_message(message)
        with smtplib.SMTP_SSL(host, port) as server:
            server.login(user, password)
            server.send_message(msg)

        return f"Sent on {datetime.now().strftime('%m/%d/%Y %H:%M')}", True

    except Exception as e:
        return f"Error: {str(e)}", False
    
def archive_email(message, folder = "Sent"):
    host = IMAP_CONFIG["host"]
    user = message["from"]
    password = message["password"]
    try:
        msg = build_email_message(message)
        with imap_connection(host,user,password) as imap:
            archive_sent_email(imap, msg.as_bytes(), folder)
        return f"Archived on {datetime.now().strftime('%m/%d/%Y %H:%M')}", True
    except Exception as e:
        return f"Error: {e}", False