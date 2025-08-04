import sys

from core.utils.pause import pause

def fatal(message, code=1):
    print(f"\n[FATAL] {message}")
    pause()
    sys.exit(code)

def non_fatal(message):
    print(f"\n[ERROR] {message}")
    pause()
