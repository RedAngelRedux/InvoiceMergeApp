# core/utils/spinner.py

import threading
import time
import sys

class Spinner:
    def __init__(self, message="Processing...", delay=0.1):
        self.message = message
        self.delay = delay
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._spin)

    def _spin(self):
        while not self._stop_event.is_set():
            for char in "|/-\\":
                sys.stdout.write(f"\r{self.message} {char}")
                sys.stdout.flush()
                time.sleep(self.delay)
        sys.stdout.write(f"\r{self.message} Done!{' ' * 10}\n")
        sys.stdout.flush()

    def __enter__(self):
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop_event.set()
        self._thread.join()
        time.sleep(0.2)  # Optional polish