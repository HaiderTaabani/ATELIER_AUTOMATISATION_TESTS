import requests
import json

def diagnostic():
    test_urls = {
        "CountAPI": "https://api.countapi.xyz/hit/demo/key",
        "Agify": "https://api.agify.io?name=michael",
        "Google": "https://www.google.com"
    }
    
    report = {}
    
    for name, url in test_urls.items():
        try:
            # Try with total bypass
            r = requests.get(url, timeout=5, proxies={"http": None, "https": None})
            report[name] = {"status": r.status_code, "msg": "Success with bypass"}
        except Exception as e:
            report[name] = {"status": "ERROR", "msg": str(e)}
            
    print(json.dumps(report, indent=2))

if __name__ == "__main__":
    diagnostic()
