import json
import time
import re
from datetime import datetime
from collections import defaultdict

# --- CONFIGURATION ---
LOG_FILE = "access.log"
DETECTIONS_FILE = "detections.json"
# Thresholds for heuristics
RATE_LIMIT_THRESHOLD = 10  # Requests per 10 seconds from same IP to same endpoint
SENSITIVE_PATHS = [
    "/storage/exports/",
    "/api/internal/sync-job",
    "/api/vendor/credit-check/"
]

class BreachSentinel:
    def __init__(self):
        self.request_history = defaultdict(list) # {ip: [timestamp, ...]}
        self.detections = []
        self.honey_records = self._load_honey_records()

    def _load_honey_records(self):
        try:
            with open("seed_data.json", "r") as f:
                data = json.load(f)
                # Create a map of token -> source_system
                return {c["canary_token"]: c["source_system"] for c in data["canaries"] if "canary_token" in c}
        except FileNotFoundError:
            print("[-] Warning: seed_data.json not found. Honey-record matching will be disabled.")
            return {}

    def analyze_log_line(self, line):
        try:
            log = json.loads(line)
            ip = log["ip"]
            url = log["url"]
            timestamp = log["timestamp"]

            # 1. Heuristic: Sensitive Path Access
            for path in SENSITIVE_PATHS:
                if path in url:
                    self._trigger_detection(
                        "SENSITIVE_PATH_ACCESS",
                        f"Access to protected path: {url}",
                        ip,
                        timestamp
                    )

            # 2. Heuristic: Rate-Based Detection (IDOR Scraping)
            if "/api/accounts/" in url:
                now = time.time()
                self.request_history[ip].append(now)
                # Clean old entries (older than 10s)
                self.request_history[ip] = [t for t in self.request_history[ip] if now - t < 10]

                if len(self.request_history[ip]) > RATE_LIMIT_THRESHOLD:
                    self._trigger_detection(
                        "RATE_LIMIT_EXCEEDED",
                        f"Potential IDOR scraping detected: {len(self.request_history[ip])} requests in 10s",
                        ip,
                        timestamp
                    )

        except Exception as e:
            print(f"[-] Error parsing log line: {e}")

    def _trigger_detection(self, rule_id, summary, ip, timestamp):
        detection = {
            "detection_id": f"DET-{int(time.time()*1000)}",
            "rule_id": rule_id,
            "summary": summary,
            "source_ip": ip,
            "timestamp": timestamp,
            "severity": "HIGH" if "SENSITIVE" in rule_id else "MEDIUM"
        }
        self.detections.append(detection)
        print(f"[!] ALERT: {rule_id} | {summary} | IP: {ip}")

        with open(DETECTIONS_FILE, "w") as f:
            json.dump(self.detections, f, indent=4)

    def attribute_leak(self, sample_data):
        """
        Analyzes a leaked sample file to identify which system was breached
        by matching against honey-records.
        """
        print("[*] Analyzing leaked sample for honey-records...")
        found_sources = set()

        # sample_data is expected to be a list of records (dicts)
        for record in sample_data:
            # Check every value in the record for a honey token
            for value in record.values():
                if isinstance(value, str) and value in self.honey_records:
                    source = self.honey_records[value]
                    found_sources.add(source)
                    print(f"[+] Found canary token! Source: {source}")

        if not found_sources:
            return "Unknown - No honey-records found"

        return list(found_sources)

    def run(self):
        print("[*] Breach Sentinel is active. Monitoring access.log...")
        # Tail the log file
        try:
            with open(LOG_FILE, "r") as f:
                # Go to end of file
                f.seek(0, 2)
                while True:
                    line = f.readline()
                    if not line:
                        time.sleep(0.1)
                        continue
                    self.analyze_log_line(line)
        except FileNotFoundError:
            print(f"[-] Error: {LOG_FILE} not found. Waiting for API to start...")
            time.sleep(5)
            self.run()

if __name__ == "__main__":
    sentinel = BreachSentinel()
    sentinel.run()
