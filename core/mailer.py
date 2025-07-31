import os
import smtplib

from email.message import EmailMessage
from datetime import datetime

SMTP_SERVER = "smtp.1and1.com"
SMTP_PORT = 465
USERNAME = "snava@topprioritycouriers.com"
PASSWORD = "tpc-4604-M.I.S.M@nager-2024"

def send_email(message):
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

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:            
            server.login(USERNAME, PASSWORD)
            server.send_message(msg)

        return f"Sent on {datetime.now().strftime('%m/%d/%Y %H:%M')}"

    except Exception as e:
        return f"Error: {str(e)}"