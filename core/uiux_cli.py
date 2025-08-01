import sys
import time
import threading

## spinner Usage
# import threading
# import time
# from core.uiux_cli import spinner

# stop_event = threading.Event()
# spinner_thread = threading.Thread(target=spinner, args=("Starting Process",stop_event))
# spinner_thread.start()

# time.sleep(5) #Replace with actual logic

# stop_event.set()
# spinner_thread.join()
# time.sleep(0.2)

# def spinner(message, stop_event):
#     while not stop_event.is_set():
#         for char in "|/-\\":
#             sys.stdout.write(f"\r{message}   {char}   ")
#             sys.stdout.flush()
#             time.sleep(0.1)
#     sys.stdout.write("\rDone!          \n")
#     sys.stdout.flush()

# # progress_bar Usage
# total = 100
# for i in range(total):
#     progress_bar(i + 1, total)
#     time.sleep(0.05)  # Simulate work
# print("\nDone!")

def progress_bar(current, total, bar_length=40):
    fraction = current / total
    arrow = '█' * int(bar_length * fraction)
    padding = '-' * (bar_length - len(arrow))
    percent = int(fraction * 100)
    sys.stdout.write(f'\rProgress: [{arrow}{padding}] {percent}%')
    sys.stdout.flush()