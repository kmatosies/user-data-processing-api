import time
import requests
import sys

url = "http://127.0.0.1:8000/health"
for i in range(30):
    try:
        r = requests.get(url, timeout=2)
        print(r.status_code)
        print(r.text)
        sys.exit(0)
    except Exception:
        time.sleep(0.5)

print("failed")
