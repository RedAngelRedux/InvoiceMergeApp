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

def archive_sent_email(imap: imaplib.IMAP4_SSL, msg_bytes: bytes, folder: str = "Sent"):
    """
    Uploads a sent email message to the specified IMAP folder.

    Args:
        imap (imaplib.IMAP4_SSL): Active IMAP connection
        msg_bytes (bytes): Raw email message
        folder (str): Target folder name
    """
    try:
        if folder_exists(imap,folder):
            imap.append(folder, '', imaplib.Time2Internaldate(time.time()), msg_bytes)
            return True
        else:
            raise FileNotFoundError(f"Failed to archive email to '{folder}'")
    except Exception as e:
        raise