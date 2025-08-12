import imaplib
import time
# import logging
from contextlib import contextmanager

@contextmanager
def imap_connection(server: str, username: str, password: str):
    """
    Context manager for IMAP4_SSL connection.

    Yields:
        imaplib.IMAP4_SSL: Authenticated IMAP connection
    """
    imap = None
    try:
        imap = imaplib.IMAP4_SSL(server)
        imap.login(username, password)
        yield imap
    except Exception as e:
        # logging.error(f"IMAP connection error: {e}")
        print(f"IMAP connection error: {e}")
        raise
    finally:
        if imap:
            try:
                imap.logout()
            except Exception as e:
                print(f"IMAP logout failed: {e}")
                # logging.warning(f"IMAP logout failed: {e}")

# Common Sent folder names (ordered by priority)
SENT_CANDIDATES = [
    "Sent",
    "Sent Items",
    "Sent Mail",
    "Sent Messages",
    "[Gmail]/Sent Mail",
]

def find_sent_folder(imap):
    status, folders = imap.list()
    if status != "OK":
        raise RuntimeError("Failed to list folders")

    # Normalize folder names
    folder_names = [f.decode().split(' "/" ')[-1].strip('"') for f in folders]

    # Try to find a match
    for candidate in SENT_CANDIDATES:
        for folder in folder_names:
            if folder.lower() == candidate.lower():
                return f'"{folder}"'
    return "InvoiceArchive"

    # Fallback: return first folder that contains "sent"
    for folder in folder_names:
        if "sent" in folder.lower():
            return f'"{folder}"'

    raise ValueError("No Sent folder found")

# def folder_exists(imap: imaplib.IMAP4_SSL, folder: str) -> bool:
#     typ, folders = imap.list()
#     if typ != "OK":
#         return False    
#     return any(f'"{folder}"' in f.decode() for f in folders)

def folder_exists(imap, folder: str) -> bool:
    typ, folders = imap.list()
    if typ != "OK":
        # print("IMAP LIST failed:", typ)
        return False

    # print("Available folders:")
    for raw in folders:
        decoded = raw.decode()
        # print("  →", decoded)

    # Check for folder match
    for raw in folders:
        decoded = raw.decode()
        if folder in decoded:
            # print(f"Matched folder: {decoded}")
            return True

    # print(f"Folder '{folder}' not found.")
    return False

def archive_sent_email(imap: imaplib.IMAP4_SSL, msg_bytes: bytes, folder: str = "InvoiceArchive"):
    """
    Uploads a sent email message to the specified IMAP folder.

    Args:
        imap (imaplib.IMAP4_SSL): Active IMAP connection
        msg_bytes (bytes): Raw email message
        folder (str): Target folder name
    """
    try:
        folder = find_sent_folder(imap)
        if folder_exists(imap,folder):
            imap.append(folder, '', imaplib.Time2Internaldate(time.time()), msg_bytes)
            return True
        else:
            raise FileNotFoundError(f"Failed to archive email to '{folder}'")
    except Exception as e:
        raise