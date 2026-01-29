import os
import json
import hmac
import hashlib
from datetime import datetime, timezone

def main():
    # SET TO TRUE FOR TESTING, FALSE FOR SUBMISSION
    DRY_RUN = True 
    
    SECRET = os.environ.get("B12_SIGNING_SECRET", "dummy-secret-if-testing-locally")
    repo_path = os.getenv("GITHUB_REPOSITORY", "https://github.com/NabeelAhmed314")
    run_id = os.getenv("GITHUB_RUN_ID", "123456789")

    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(timespec='milliseconds').replace('+00:00', 'Z'),
        "name": "Nabeel Ahmed",
        "email": "nabeelahmadgit000@gmail.com",
        "resume_link": "https://drive.google.com/file/d/1h6T_NxxUIUPxZrOlt68-6swYNCH2jSCK/view?usp=sharing",
        "repository_link": f"https://github.com/{repo_path}",
        "action_run_link": f"https://github.com/{repo_path}/actions/runs/{run_id}"
    }

    # Generate Canonical JSON
    json_body = json.dumps(payload, sort_keys=True, separators=(',', ':')).encode('utf-8')

    # Generate Signature
    signature = hmac.new(
        SECRET.encode('utf-8'),
        msg=json_body,
        digestmod=hashlib.sha256
    ).hexdigest()
    
    if DRY_RUN:
        print("\n[DRY RUN] Skipping actual POST request.")
        print("--- DRY RUN RESULTS ---")
        print(f"Canonical JSON: {json_body.decode('utf-8')}")
        print(f"X-Signature-256: sha256={signature}")
    else:
        import requests
        print("\n[LIVE] Sending request to B12...")
        headers = {"Content-Type": "application/json", "X-Signature-256": f"sha256={signature}"}
        response = requests.post("https://b12.io/apply/submission", data=json_body, headers=headers)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")

if __name__ == "__main__":
    main()
