import random
import string

def generate_random_key(length=8):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

def test_hit_endpoint(client):
    key = "demo_key_" + generate_random_key()
    resp, latency, error = client.get(f"/hit/test_namespace/{key}")
    
    if error:
        return {"name": "GET /hit", "status": "FAIL", "latency_ms": latency, "details": error}
    
    if resp.status_code == 200:
        data = resp.json()
        if "value" in data and isinstance(data["value"], int):
            return {"name": "GET /hit", "status": "PASS", "latency_ms": latency}
        else:
            return {"name": "GET /hit", "status": "FAIL", "latency_ms": latency, "details": "Invalid JSON structure"}
    else:
        return {"name": "GET /hit", "status": "FAIL", "latency_ms": latency, "details": f"Status code {resp.status_code}"}

def test_get_endpoint(client):
    # We use 'demo/key' which is likely to exist or persist during short tests
    resp, latency, error = client.get("/get/test_namespace/demo_key")
    
    if error:
        return {"name": "GET /get", "status": "FAIL", "latency_ms": latency, "details": error}
    
    if resp.status_code in [200, 404]: # 404 is valid for non-existent key, but for contract we expect 200 if key exists
        return {"name": "GET /get", "status": "PASS", "latency_ms": latency}
    else:
        return {"name": "GET /get", "status": "FAIL", "latency_ms": latency, "details": f"Status code {resp.status_code}"}

def test_info_endpoint(client):
    resp, latency, error = client.get("/info/test_namespace/demo_key")
    
    if error:
        return {"name": "GET /info", "status": "FAIL", "latency_ms": latency, "details": error}
    
    if resp.status_code == 200:
        data = resp.json()
        required_fields = ["namespace", "key", "value"]
        if all(field in data for field in required_fields):
            return {"name": "GET /info", "status": "PASS", "latency_ms": latency}
        else:
            return {"name": "GET /info", "status": "FAIL", "latency_ms": latency, "details": "Missing fields in info"}
    elif resp.status_code == 404:
        return {"name": "GET /info", "status": "PASS", "latency_ms": latency, "details": "Key not found (valid 404)"}
    else:
        return {"name": "GET /info", "status": "FAIL", "latency_ms": latency, "details": f"Status code {resp.status_code}"}

def test_invalid_namespace(client):
    # Very long or invalid namespace
    resp, latency, error = client.get("/get/this_namespace_does_not_exist_12345/some_key")
    
    if error:
        return {"name": "Invalid Namespace", "status": "FAIL", "latency_ms": latency, "details": error}
    
    if resp.status_code == 404:
        return {"name": "Invalid Namespace", "status": "PASS", "latency_ms": latency}
    else:
        return {"name": "Invalid Namespace", "status": "FAIL", "latency_ms": latency, "details": f"Expected 404, got {resp.status_code}"}

def test_status_endpoint(client):
    # CountAPI doesn't have a direct health check usually, but we check root or simple get
    resp, latency, error = client.get("/")
    
    if error:
        return {"name": "API Status (Root)", "status": "FAIL", "latency_ms": latency, "details": error}
    
    if resp.status_code < 500:
        return {"name": "API Status (Root)", "status": "PASS", "latency_ms": latency}
    else:
        return {"name": "API Status (Root)", "status": "FAIL", "latency_ms": latency, "details": f"Server Error {resp.status_code}"}

def test_robustness_retry(client):
    # This is more of a smoke test to see if the client handles a simple valid request without failing
    resp, latency, error = client.get("/hit/demo/robustness_test")
    
    if error:
        return {"name": "Robustness Smoke Test", "status": "FAIL", "latency_ms": latency, "details": error}
    
    if resp.status_code == 200:
        return {"name": "Robustness Smoke Test", "status": "PASS", "latency_ms": latency}
    else:
        return {"name": "Robustness Smoke Test", "status": "FAIL", "latency_ms": latency, "details": f"Status code {resp.status_code}"}

def run_all_tests(client):
    results = []
    results.append(test_hit_endpoint(client))
    results.append(test_get_endpoint(client))
    results.append(test_info_endpoint(client))
    results.append(test_invalid_namespace(client))
    results.append(test_status_endpoint(client))
    results.append(test_robustness_retry(client))
    return results
