# utils/pause.py
import sys
import os

def pause(message="Press any key to continue...", return_key=False):
    print(message, end='', flush=True)

    if os.name == 'nt':
        import msvcrt
        key = msvcrt.getch()
    else:
        import termios
        import tty
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    print()  # Move to next line after keypress
    return key if return_key else None