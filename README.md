# 🏦 Breach Lab: Cybersecurity Engineering Portfolio

Breach Lab is a high-fidelity cybersecurity simulation environment consisting of a vulnerable banking application (**MeridianBank**) and a defensive monitoring system (**Breach Sentinel**). 

This project demonstrates the full lifecycle of a data breach: from initial vulnerability exploitation and exfiltration to real-time detection, source attribution using honey-records, and formal incident response reporting.

## 🛠 Architecture

- **Exfil-Lab (Offensive)**: A FastAPI banking app with intentional BOLA/IDOR, permissive storage, and credential leaks.
- **Breach Sentinel (Defensive)**: A heuristic engine that monitors API logs and uses canary tokens for data attribution.
- **SOC Dashboard**: A React/Tailwind frontend for real-time alert monitoring and breach claim verification.

## 🎯 Threat Model

| Component | Attacker Goal | Technique | MITRE ATT&CK |
| :--- | :--- | :--- | :--- |
| API Endpoints | Mass Customer Exfiltration | BOLA/IDOR Scraping | T1592 |
| Cloud Storage | Bulk PII Download | Permissive Bucket Access | T1530 |
| Vendor API | Third-Party Data Theft | Excessive Privileges | T1199 |
| Internal Jobs | System Admin Access | Hardcoded Credentials | T1552.001 |

## 🚀 Quick Start (Under 5 Minutes)

### Prerequisites
- Docker & Docker Compose

### Deployment
```bash
# Clone the repo
git clone <your-repo-url>
cd breach-lab

# Spin up the entire lab
docker-compose up --build -d
```

### Access Points
- **Bank API**: `http://localhost:8000`
- **SOC Dashboard**: `http://localhost:3000`

## 🧪 Demo Checklist (Validation Suite)

Follow these steps to demonstrate the system's effectiveness:

1. **Test IDOR Detection**
   - Run: `python exfil-lab/attack_scripts.py --attack idor --mode fast`
   - **Verify**: Open the Dashboard $\rightarrow$ "Live Detections" $\rightarrow$ See `RATE_LIMIT_EXCEEDED` alert.

2. **Test Storage Leak**
   - Run: `python exfil-lab/attack_scripts.py --attack storage`
   - **Verify**: Dashboard $\rightarrow$ "Live Detections" $\rightarrow$ See `SENSITIVE_PATH_ACCESS` for `/storage/exports/`.

3. **Test Vendor Abuse**
   - Run: `python exfil-lab/attack_scripts.py --attack vendor`
   - **Verify**: Dashboard $\rightarrow$ "Live Detections" $\rightarrow$ See alert for `/api/vendor/credit-check/`.

4. **Test Attribution (The "Smoking Gun")**
   - Upload the `customer_data_full.json` (obtained from Step 2) to the **Claim Verifier** page.
   - **Verify**: Dashboard $\rightarrow$ "Claim Verifier" $\rightarrow$ See "Identified Sources: S3_BUCKET".

## 🛡️ Security Disclaimer
This project uses **100% synthetic data** generated via the `Faker` library. No real PII or breach data was used in the creation of this project. All attack logic is hardcoded to localhost.
