import requests
import time

IMPORT_URL = "http://127.0.0.1:8000/api/v1/import/users"
GET_URL = "http://127.0.0.1:8000/api/v1/users/{user_id}"
JSON_URL = "http://127.0.0.1:9000/test_users.json"


def run():
    print("Posting import request to", IMPORT_URL)
    try:
        r = requests.post(IMPORT_URL, data={"url": JSON_URL}, timeout=30)
        print("Import POST status:", r.status_code)
        print(r.text)
    except Exception as e:
        print("Import request failed:", e)
        return

    # wait a moment for DB commit
    time.sleep(1)

    user_id = "user-123"
    print("Querying GET user", user_id)
    try:
        r = requests.get(GET_URL.format(user_id=user_id), timeout=10)
        print("GET status:", r.status_code)
        print(r.text)
    except Exception as e:
        print("GET request failed:", e)


if __name__ == "__main__":
    run()
