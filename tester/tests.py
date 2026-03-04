def test_single_name(client):
    resp, latency, error = client.get("/?name=michael")
    
    if error:
        return {"name": "GET /?name=michael", "status": "FAIL", "latency_ms": latency, "details": error}
    
    if resp.status_code == 200:
        data = resp.json()
        if all(k in data for k in ["name", "age", "count"]):
            return {"name": "GET /?name=michael", "status": "PASS", "latency_ms": latency}
        else:
            return {"name": "GET /?name=michael", "status": "FAIL", "latency_ms": latency, "details": "Missing fields in JSON"}
    else:
        return {"name": "GET /?name=michael", "status": "FAIL", "latency_ms": latency, "details": f"Status {resp.status_code}"}

def test_multiple_names(client):
    resp, latency, error = client.get("/?name[]=michael&name[]=peter")
    
    if error:
        return {"name": "GET multiple names", "status": "FAIL", "latency_ms": latency, "details": error}
    
    if resp.status_code == 200:
        data = resp.json()
        if isinstance(data, list) and len(data) == 2:
            return {"name": "GET multiple names", "status": "PASS", "latency_ms": latency}
        else:
            return {"name": "GET multiple names", "status": "FAIL", "latency_ms": latency, "details": "Expected list of 2 items"}
    else:
        return {"name": "GET multiple names", "status": "FAIL", "latency_ms": latency, "details": f"Status {resp.status_code}"}

def test_with_country(client):
    resp, latency, error = client.get("/?name=michael&country_id=FR")
    
    if error:
        return {"name": "GET with country", "status": "FAIL", "latency_ms": latency, "details": error}
    
    if resp.status_code == 200:
        return {"name": "GET with country", "status": "PASS", "latency_ms": latency}
    else:
        return {"name": "GET with country", "status": "FAIL", "latency_ms": latency, "details": f"Status {resp.status_code}"}

def test_missing_name(client):
    # Agify requires 'name' parameter, returns 422
    resp, latency, error = client.get("/")
    
    if error:
        return {"name": "Invalid Request (Missing name)", "status": "FAIL", "latency_ms": latency, "details": error}
    
    # In mock mode or real, we expect 422 for Agify root without name
    if resp.status_code == 422:
        return {"name": "Invalid Request (Missing name)", "status": "PASS", "latency_ms": latency}
    else:
        return {"name": "Invalid Request (Missing name)", "status": "FAIL", "latency_ms": latency, "details": f"Expected 422, got {resp.status_code}"}

def test_qos_root(client):
    # Check Agify website/root to measure availability
    resp, latency, error = client.get("https://agify.io")
    
    if error:
        return {"name": "Agify Landing Page", "status": "FAIL", "latency_ms": latency, "details": error}
    
    if resp.status_code == 200:
        return {"name": "Agify Landing Page", "status": "PASS", "latency_ms": latency}
    else:
        return {"name": "Agify Landing Page", "status": "FAIL", "latency_ms": latency, "details": f"Status {resp.status_code}"}

def test_response_types(client):
    # Functional test for data types
    resp, latency, error = client.get("/?name=test")
    
    if error:
        return {"name": "Type Check (name/age)", "status": "FAIL", "latency_ms": latency, "details": error}
    
    if resp.status_code == 200:
        data = resp.json()
        if isinstance(data.get("age"), (int, type(None))) and isinstance(data.get("name"), str):
            return {"name": "Type Check (name/age)", "status": "PASS", "latency_ms": latency}
        else:
            return {"name": "Type Check (name/age)", "status": "FAIL", "latency_ms": latency, "details": "Type mismatch"}
    else:
        return {"name": "Type Check (name/age)", "status": "FAIL", "latency_ms": latency, "details": f"Status {resp.status_code}"}

def run_all_tests(client):
    results = []
    results.append(test_single_name(client))
    results.append(test_multiple_names(client))
    results.append(test_with_country(client))
    results.append(test_missing_name(client))
    results.append(test_qos_root(client))
    results.append(test_response_types(client))
    return results
