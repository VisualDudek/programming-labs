#!/bin/env python

import threading
import platform
import multiprocessing
import argparse


# Set up argumet parser
parser = argparse.ArgumentParser(description='A script to demonstrate threading with custom parameters.')
parser.add_argument('-n', type=int, default=100_000, help='Number of increments per thread (default: 100,000)')
parser.add_argument('-t', '--threads', type=int, default=10, help='Number of threads (default: 10)')
parser.add_argument('-l', action='store_true', help='If present, enables thread lock')

args = parser.parse_args()
N = args.n
N_THREADS = args.threads
LOCK = args.l

python_version = platform.python_version()
cpu_cores = multiprocessing.cpu_count()

print(f"Python version: {python_version}, run: pyenv shell 3.9.x to setup version,\n\t deactivate to exit shell: pyrnv shell --unset")
print(f"Number of CPU cores: {cpu_cores} \n")
print("Load CPU using: stress-ng --cpu 16 --cpu-load 90 --timeout 60s")
print("Check CPU usage using: htop")
print("Check context switches using: vmstat 1")

# Print the parameters being used
print(f"Parameters:\n\t n (increments per thread) = {N:_},\n\t t (number of threads) = {N_THREADS}")
print(f"\t Lock: {LOCK}\n")


# Shared resource
counter = 0
lock = threading.Lock()

# Function to increment the counter
def increment():
    global counter
    for _ in range(N):
        if LOCK:
            with lock:
                counter += 1
        else: 
            counter += 1

# Create threads
threads = []
for i in range(N_THREADS):
    thread = threading.Thread(target=increment)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

# Print the final value of counter
if counter == N * N_THREADS:
    print(f"Final counter value: {counter:_}")
else:
    print(f"Final counter value: {counter:_} BUT it should be: {N*N_THREADS:_}")
