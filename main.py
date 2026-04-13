import random
import string
import requests
import time
import json
import os
import webbrowser
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
RESET = "\033[0m"
generated_set = set()
results_list = []
def check_username(name):
    url = f"https://api.mojang.com/users/profiles/minecraft/{name}"
    for attempt in range(5):
        try:
            response = requests.get(url, timeout=5)
            try:
                data = response.json()
            except Exception:
                data = None
            if isinstance(data, dict) and "id" in data and "name" in data:
                return {"status": "TAKEN", "code": response.status_code, "data": data}
            if isinstance(data, dict) and "errorMessage" in data:
                return {"status": "AVAILABLE", "code": 204, "data": data}
            if response.status_code == 429:
                time.sleep(1)
                continue
            return {"status": "UNKNOWN", "code": response.status_code, "data": data}
        except Exception:
            time.sleep(1)
            continue
    return {"status": "FAIL", "code": None, "data": None}
print("Choose mode:")
print("1 = Numbers")
print("2 = Letters")
print("3 = Any (Letters + Numbers)")
mode = input("Enter 1, 2, or 3: ")
try:
    length = int(input("Enter username length (3-16): "))
except:
    length = 3
if length < 3:
    length = 3
elif length > 16:
    length = 16
try:
    times = int(input("How many usernames to generate? "))
except:
    times = 1000
def generate_name():
    if mode == "1":
        return ''.join(random.choices(string.digits, k=length))
    elif mode == "2":
        return ''.join(random.choices(string.ascii_lowercase, k=length))
    elif mode == "3":
        chars = string.ascii_lowercase + string.digits
        return ''.join(random.choices(chars, k=length))
    else:
        return "???"
print(f"\nChecking {times} usernames (length={length})...\n")
available_count = 0
for i in range(times):
    username = generate_name()
    if username in generated_set:
        continue
    generated_set.add(username)
    result = check_username(username)
    result["username"] = username
    results_list.append(result)
    status = result["status"]
    data = result["data"]
    if status == "AVAILABLE":
        print(f"{GREEN}{username} - {status} - {data}{RESET}")
        available_count += 1
    elif status == "TAKEN":
        print(f"{RED}{username} - {status} - {data}{RESET}")
    elif status == "UNKNOWN":
        print(f"{YELLOW}{username} - {status} - {data}{RESET}")
    else:
        print(f"{YELLOW}{username} - FAIL - {data}{RESET}")
json_file = "results.json"
with open(json_file, "w", encoding="utf-8") as f:
    json.dump(results_list, f, indent=2)
html_file = "results.html"
html = "<html><head><title>Minecraft Report</title></head><body>"
html += "<h2>Minecraft Username Report</h2>"
html += "<pre>" + json.dumps(results_list, indent=2) + "</pre>"
html += "</body></html>"

with open(html_file, "w", encoding="utf-8") as f:
    f.write(html)
try:
    webbrowser.open(html_file)
    os.startfile(json_file)
except:
    print("Could not auto-open files")
print("\nDone!")
print(f"Available usernames found: {available_count}")
print(f"Saved: {html_file}, {json_file}")
input("\nPress Enter to exit...")
