import signal
import time
import sys
import os
import logging
import subprocess


logging.basicConfig(level=logging.INFO)

pid = os.getpid()
print(f"Process ID (PID): {pid}")

def custom_handler(signum, frame):
    print(f"Received signal {signum}. Exiting...")
    sys.exit(0)

def custom_user1_handler(signum, frame):
    print(f"Received signal {signum}. Exiting...")
    sys.exit(0)

def custom_user2_handler(signum, frame):
    print(f"Received signal {signum}. Changing logging level...")
    logging.getLogger().setLevel(logging.DEBUG)

# Set up a signal handler for SIGINT
#signal.signal(signal.SIGINT, custom_handler)
signal.signal(signal.SIGUSR1, custom_user1_handler)
signal.signal(signal.SIGUSR2, custom_user2_handler)

# Run subprocess
# command = ["python3", "my_signal_subprocess.py"]
command = ["sleep", "120"]
process = subprocess.Popen(command)
pid = process.pid
print(f"Subprocess started with PID: {pid}")

try:
    print("Press Ctrl+C to trigger SIGINT.")
    while True:
        logging.info("INFO message")
        logging.debug("DEBUG message")
        time.sleep(2)  # Simulate a long-running process
except KeyboardInterrupt:
    print("\nKeyboardInterrupt caught. Exiting gracefully.")

print("Process ended.")

