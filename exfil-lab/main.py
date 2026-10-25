import json
import os
from fastapi import FastAPI, HTTPException, Depends, Header, Request
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional
import uuid

app = FastAPI(title="MeridianBank API", version="1.0.0")

# --- DATA LOADING ---
DATA_FILE = "seed_data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        # In a real run, the user would have run generate_data.py
        # We'll return a basic structure to avoid crashes if they haven't yet
        return {"customers": [], "accounts": [], "transactions": [], "canaries": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# --- MODELS ---
class AccountDetail(BaseModel):
    account_id: str
    customer_id: str
    account_type: str
    balance: float
    currency: str
    status: str

# --- VULNERABILITY 3: Hardcoded Creds (Simulated) ---
# This "service account" is used by background jobs but is hardcoded in the source
SERVICE_ACCOUNT_TOKEN = "mb_svc_prod_secret_2024_admin_access"

# --- MIDDLEWARE FOR LOGGING (For Breach Sentinel) ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    # We log to a file that Breach Sentinel will watch
    log_entry = {
        "timestamp": os.popen("date -u UTC").read().strip(),
        "method": request.method,
        "url": str(request.url),
        "ip": request.client.host,
        "headers": dict(request.headers),
        "params": dict(request.query_params),
    }
    with open("access.log", "a") as log_file:
        log_file.write(json.dumps(log_entry) + "\n")

    response = await call_next(request)
    return response

# --- ENDPOINTS ---

@app.get("/")
def root():
    return {"message": "Welcome to MeridianBank Secure Portal", "status": "Online"}

# VULNERABILITY 1: IDOR/BOLA
# The endpoint accepts an account_id but DOES NOT verify if the authenticated user owns it.
@app.get("/api/accounts/{account_id}", response_model=AccountDetail)
def get_account_details(account_id: str, x_user_id: Optional[str] = Header(None)):
    """
    VULNERABILITY: IDOR.
    The 'x-user-id' header is used for simulation of authentication,
    but the logic never checks if account_id belongs to x-user-id.
    """
    data = load_data()
    account = next((acc for acc in data["accounts"] if acc["account_id"] == account_id), None)

    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    return account

# VULNERABILITY 2: Permissive Cloud Storage (Simulated)
# This endpoint simulates a public S3 bucket holding an export.
@app.get("/storage/exports/customer_data_full.json")
def get_public_export():
    """
    VULNERABILITY: Overly permissive cloud storage.
    This file should be private, but is accessible to anyone.
    """
    data = load_data()
    # Simulate an export file containing PII and Canaries
    export_content = {
        "export_date": "2024-10-01",
        "records": data["customers"]
    }

    # In a real deployment, this would be a static file on an S3 bucket.
    # Here we save it to a temp file and serve it.
    with open("customer_data_full.json", "w") as f:
        json.dump(export_content, f)

    return FileResponse("customer_data_full.json", media_type="application/json")

# VULNERABILITY 4: Third-Party Vendor Integration
# This endpoint is meant for a "Credit Scoring Vendor" but provides far too much data.
@app.get("/api/vendor/credit-check/{customer_id}")
def vendor_credit_check(customer_id: str, authorization: Optional[str] = Header(None)):
    """
    VULNERABILITY: Excessive Vendor Access.
    The vendor only needs a credit score, but the API returns the full customer profile.
    """
    if authorization != "Bearer vendor_secret_token_99":
        raise HTTPException(status_code=403, detail="Unauthorized Vendor Access")

    data = load_data()
    customer = next((c for c in data["customers"] if c["customer_id"] == customer_id), None)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    # Returns the entire PII object instead of just a score
    return {
        "credit_score": random.randint(300, 850),
        "full_profile": customer
    }

# Background Job Simulation (for Hardcoded Creds)
@app.post("/api/internal/sync-job")
def trigger_sync_job(token: str):
    """
    Simulates a background sync job.
    VULNERABILITY: Uses the hardcoded SERVICE_ACCOUNT_TOKEN.
    """
    if token != SERVICE_ACCOUNT_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid Service Token")

    return {"status": "Sync successful", "records_processed": 100}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
