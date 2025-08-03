import sys

def fatal(message, code=1):
    print(f"[FATAL] {message}")
    sys.exit(code)