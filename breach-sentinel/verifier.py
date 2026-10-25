import json
import os
import uuid
from datetime import datetime

# --- CONFIGURATION ---
DETECTIONS_FILE = "detections.json"
SEED_DATA_FILE = "seed_data.json"
REPORTS_DIR = "reports"

if not os.path.exists(REPORTS_DIR):
    os.makedirs(REPORTS_DIR)

class ClaimVerifier:
    def __init__(self):
        self.honey_records = self._load_honey_records()
        self.all_customers = self._load_all_customers()

    def _load_honey_records(self):
        try:
            with open(SEED_DATA_FILE, "r") as f:
                data = json.load(f)
                return {c["canary_token"]: c["source_system"] for c in data["canaries"] if "canary_token" in c}
        except FileNotFoundError:
            return {}

    def _load_all_customers(self):
        try:
            with open(SEED_DATA_FILE, "r") as f:
                data = json.load(f)
                return {c["customer_id"]: c for c in data["customers"]}
        except FileNotFoundError:
            return {}

    def verify_claim(self, uploaded_file_path):
        """
        Validates a breach claim by analyzing the uploaded sample.
        """
        try:
            with open(uploaded_file_path, "r") as f:
                sample_data = json.load(f)
        except Exception as e:
            return {"error": f"Invalid file format: {str(e)}"}

        if not isinstance(sample_data, list):
            # Handle case where sample is wrapped in an object
            if isinstance(sample_data, dict) and "records" in sample_data:
                sample_data = sample_data["records"]
            else:
                return {"error": "Invalid sample structure. Expected a list of records."}

        claimed_count = len(sample_data)
        real_records = []
        canary_matches = set()
        structural_failures = 0

        for record in sample_data:
            # 1. Structural Validation
            # A real record must have at least a customer_id or full_name
            if not any(key in record for key in ["customer_id", "full_name"]):
                structural_failures += 1
                continue

            # 2. Real Identity Validation
            cust_id = record.get("customer_id")
            if cust_id and cust_id in self.all_customers:
                real_records.append(record)

            # 3. Canary Matching
            for val in record.values():
                if isinstance(val, str) and val in self.honey_records:
                    canary_matches.add(self.honey_records[val])

        real_count = len(real_records)

        return {
            "claimed_scope": claimed_count,
            "verified_scope": real_count,
            "fake_record_count": claimed_count - real_count,
            "structural_failures": structural_failures,
            "identified_sources": list(canary_matches),
            "is_authentic": real_count > 0,
            "authenticity_score": (real_count / claimed_count) if claimed_count > 0 else 0
        }

class ReportGenerator:
    @staticmethod
    def generate_incident_timeline(detections):
        """Generates a chronological timeline of the breach."""
        timeline = []
        for det in sorted(detections, key=lambda x: x["timestamp"]):
            timeline.append(f"[{det['timestamp']}] {det['severity']} - {det['rule_id']}: {det['summary']} (Source: {det['source_ip']})")

        return "\n".join(timeline)

    @staticmethod
    def generate_breach_report(verification, detections):
        """Generates a formal breach report."""
        timeline = ReportGenerator.generate_incident_timeline(detections)

        report = f"""# INCIDENT RESPONSE REPORT: BREACH-LAB-001
Date: {datetime.now().strftime('%Y-%m-%d')}
Status: FINAL

## 1. Executive Summary
A data exfiltration event was detected. The attacker successfully accessed {verification['verified_scope']} records.
Authenticity: {"Confirmed" if verification['is_authentic'] else "Unverified"}
Identified Leak Sources: {', '.join(verification['identified_sources']) if verification['identified_sources'] else "Unknown"}

## 2. Scope Analysis
- Claimed Records: {verification['claimed_scope']}
- Verified Records: {verification['verified_scope']}
- Invalid/Fake Records: {verification['fake_record_count']}
- Structural Integrity Issues: {verification['structural_failures']}

## 3. Detection Timeline
{timeline}

## 4. Remediation Steps
- Rotated service account tokens.
- Closed permissive cloud storage buckets.
- Implemented strict BOLA/IDOR checks on account endpoints.
- Restricted vendor API scopes.
"""
        return report

    @staticmethod
    def generate_customer_notification(customer_record):
        """Generates a personalized notification for a breached customer."""
        return f"""
Dear {customer_record.get('full_name', 'Valued Customer')},

We are writing to inform you of a security incident involving your account information.
Our systems indicate that your data may have been accessed.

Affected Information: {', '.join([k for k in customer_record.keys() if k != 'canary_token'])}

We have already taken steps to secure your account. We recommend you update your password immediately.

Sincerely,
MeridianBank Security Team
"""

    def export_report(self, filename, content):
        path = os.path.join(REPORTS_DIR, filename)
        with open(path, "w") as f:
            f.write(content)
        return path

if __name__ == "__main__":
    # Quick local test
    verifier = ClaimVerifier()
    generator = ReportGenerator()

    # Simulate a leak file
    leak_data = [
        {"customer_id": "fake-1", "full_name": "Fake Person"}, # Fake
        {"customer_id": "real-1", "full_name": "Real Person", "canary_token": "some-token"}, # Real
    ]
    with open("sample_leak.json", "w") as f:
        json.dump(leak_data, f)

    res = verifier.verify_claim("sample_leak.json")
    print(f"Verification Result: {res}")
