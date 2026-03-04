from .client import APIClient
from .tests import run_all_tests
from datetime import datetime
import json

def calculate_p95(latencies):
    if not latencies:
        return 0
    sorted_latencies = sorted(latencies)
    idx = int(0.95 * len(sorted_latencies))
    return sorted_latencies[idx]

def run_tests():
    client = APIClient("https://api.countapi.xyz", timeout=3, max_retries=1)
    
    start_time = datetime.now()
    test_results = run_all_tests(client)
    end_time = datetime.now()
    
    passed = len([r for r in test_results if r["status"] == "PASS"])
    failed = len(test_results) - passed
    error_rate = failed / len(test_results) if test_results else 0
    
    latencies = [r["latency_ms"] for r in test_results]
    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    p95_latency = calculate_p95(latencies)
    
    availability = 1.0 if failed == 0 else (passed / len(test_results))
    
    summary = {
        "api": "CountAPI",
        "timestamp": start_time.isoformat(),
        "summary": {
            "passed": passed,
            "failed": failed,
            "error_rate": round(error_rate, 3),
            "latency_ms_avg": round(avg_latency, 2),
            "latency_ms_p95": round(p95_latency, 2),
            "availability": round(availability, 2)
        },
        "tests": test_results
    }
    
    return summary

if __name__ == "__main__":
    results = run_tests()
    print(json.dumps(results, indent=2))
