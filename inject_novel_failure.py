import os
import time
import signal
import sys

files = []

def cleanup(signum=None, frame=None):
    print("\nCleaning up file handles...")
    for f in files:
        try:
            f.close()
        except:
            pass
    print("Cleanup complete.")
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)

print("Injecting novel failure: database_connection_exhaustion")
print("Opening many file handles to simulate resource exhaustion...")

try:
    while True:
        for i in range(500):
            f = open("/dev/null", "r")
            files.append(f)

        print(f"Open handles: {len(files)}")
        time.sleep(2)

except KeyboardInterrupt:
    cleanup()