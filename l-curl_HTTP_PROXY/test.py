#!/usr/bin/env python3
import os

print("Content-Type: text/plain")
print()
print("============ HTTP_PROXY =============")
print("HTTP_PROXY environment variable is:", os.environ.get("HTTP_PROXY", "Not Set"))
print()

for key, value in os.environ.items():
          print(f"{key}: {value}")

