from lxml import etree

import re

def replace_placeholders(template: str, values: dict) -> str:
    """
    Replaces placeholders like [ACCOUNT], [DATE] with values from the dictionary.

    Args:
        template (str): The string containing placeholders like [ACCOUNT].
        values (dict): Dictionary of placeholder-value pairs, e.g. {"ACCOUNT": "12345"}

    Returns:
        str: The template string with placeholders replaced.
    
    Example Usage:
        template = "Invoice for [ACCOUNT] due on [DATE]."
        data = {
            "ACCOUNT": "ACC-778902",
            "DATE": "2025-07-31"
        }
        final_output = replace_placeholders(template, data)
    """
    def replacement(match):
        key = match.group(1)
        return str(values.get(key, match.group(0)))  # Leave placeholder untouched if not found

    return re.sub(r"\[([A-Z_]+)\]", replacement, template)

def load_template(tab_name):
    tree = etree.parse(f"{tab_name.lower()}.xml")
    root = tree.getroot()
    subject = root.findtext("Subject")
    body = root.findtext("Body")
    signature = root.findtext("Signature")
    return subject, body, signature

def build_message(from_addr, to, cc, bcc, subject, body, signature, attachment):
    full_body = f"{body}\n\n{signature}"
    return {
        "from": from_addr,
        "to": to,
        "cc": cc,
        "bcc": bcc,
        "subject": subject,
        "body": full_body,
        "attachment": attachment
    }