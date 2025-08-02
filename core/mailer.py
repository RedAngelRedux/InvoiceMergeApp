import os
import smtplib

from email.message import EmailMessage
from datetime import datetime
from core.config_loader import SMTP_CONFIG

def send_email(message):

    host = SMTP_CONFIG["host"]
    port = SMTP_CONFIG["port"]
    user = SMTP_CONFIG["user"]
    password = SMTP_CONFIG["password"]
    
    try:
        msg = EmailMessage()
        msg["From"] = message["from"]
        msg["To"] = ", ".join(message["to"])
        if message.get("cc"):
            msg["Cc"] = ", ".join(message["cc"])
        if message.get("bcc"):
            msg["Bcc"] = ", ".join(message["bcc"])
        msg["Subject"] = message["subject"]
        msg.set_content(message["body"])

        if message.get("attachment"):
            with open(message["attachment"], "rb") as f:
                msg.add_attachment(
                    f.read(), 
                    maintype="application", 
                    subtype="pdf",
                    filename=os.path.basename(message["attachment"]))

        with smtplib.SMTP_SSL(host, port) as server:            
            server.login(user, password)
            server.send_message(msg)

        return f"Sent on {datetime.now().strftime('%m/%d/%Y %H:%M')}"

    except Exception as e:
        return f"Error: {str(e)}"