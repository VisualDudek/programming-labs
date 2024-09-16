import os
import time
import signal
import sys


parent_pid = os.getppid()
pid = os.getpid()

print(f"Process ID of subprocess (PID): {pid}")
print(f"The Parent PID of subprocess is: {parent_pid}")

def custom_handler(signum, frame):
    print(f"Received signal {signum}. Exiting...")
    sys.exit(0)

signal.signal(signal.SIGINT, custom_handler)

while True:
    print("Running from subprocess ...")
    time.sleep(2)

