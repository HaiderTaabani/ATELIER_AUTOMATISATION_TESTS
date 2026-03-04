import requests
import sys

def check():
    url = "https://api.agify.io?name=michael"
    print(f"Testing {url}...")
    try:
        r = requests.get(url, proxies={"http": None, "https": None}, timeout=10)
        print(f"Status: {r.status_code}")
        print(f"Response: {r.text}")
    except Exception as e:
        print(f"Error: {e}")
    sys.stdout.flush()

if __name__ == "__main__":
    check()
