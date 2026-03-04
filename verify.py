import os
os.environ['MOCK_MODE'] = 'true'
from tester.runner import run_tests
import storage
import json

def verify():
    print("Starting mock run...")
    data = run_tests()
    storage.save_run(data)
    with open('verification_result.json', 'w') as f:
        json.dump(data, f, indent=2)
    print("Mock run complete. Results saved.")

if __name__ == "__main__":
    verify()
    print("Verification script finished.")
