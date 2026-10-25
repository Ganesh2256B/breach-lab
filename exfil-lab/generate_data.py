import json
import random
import uuid
from datetime import datetime, timedelta
from faker import Faker

def generate_synthetic_data(seed=42, num_customers=100):
    # Seed for reproducibility
    random.seed(seed)
    fake = Faker()
    fake.seed_instance(seed)

    print(f"Generating synthetic data for {num_customers} customers...")

    customers = []
    accounts = []
    transactions = []
    canaries = []

    # 1. Generate Customers
    for i in range(num_customers):
        customer_id = str(uuid.uuid4())
        # Every 10th customer is a canary record to ensure spread
        is_canary = (i % 10 == 0)

        name = fake.name()
        if is_canary:
            name = f"CANARY_{fake.word().upper()}_{random.randint(1000, 9999)}"
            canary_token = f"honey-token-{uuid.uuid4().hex[:8]}"
        else:
            canary_token = None

        customer = {
            "customer_id": customer_id,
            "full_name": name,
            "email": fake.email(),
            "phone": fake.phone_number(),
            "address": fake.address().replace('\n', ', '),
            "ssn_last_4": fake.random_number(digits=4, fix_len=True),
            "created_at": (datetime.now() - timedelta(days=random.randint(365, 3650))).isoformat(),
            "is_canary": is_canary,
            "canary_token": canary_token
        }
        customers.append(customer)

        # 2. Generate Accounts for each customer (1-3 accounts)
        for _ in range(random.randint(1, 3)):
            account_id = f"ACC-{random.randint(10000000, 99999999)}"
            account_type = random.choice(["Checking", "Savings", "Investment"])
            balance = round(random.uniform(100.0, 50000.0), 2)

            account = {
                "account_id": account_id,
                "customer_id": customer_id,
                "account_type": account_type,
                "balance": balance,
                "currency": "USD",
                "status": "Active",
                "opened_at": (datetime.now() - timedelta(days=random.randint(365, 1825))).isoformat()
            }
            accounts.append(account)

            # Create a canary record specifically for this account if customer is canary
            if is_canary:
                canaries.append({
                    "record_id": account_id,
                    "canary_token": canary_token,
                    "source_system": "DATABASE",
                    "detection_tag": f"DB_CANARY_{customer_id[:8]}"
                })

    # 3. Generate Transactions
    for _ in range(num_customers * 10):
        acc_from = random.choice(accounts)["account_id"]
        acc_to = random.choice(accounts)["account_id"]
        if acc_from == acc_to: continue

        amount = round(random.uniform(5.0, 2000.0), 2)
        tx_date = (datetime.now() - timedelta(days=random.randint(0, 90))).isoformat()

        transactions.append({
            "tx_id": str(uuid.uuid4()),
            "from_account": acc_from,
            "to_account": acc_to,
            "amount": amount,
            "timestamp": tx_date,
            "description": fake.sentence(nb_words=3),
            "category": random.choice(["Groceries", "Utilities", "Rent", "Entertainment", "Salary"])
        })

    # 4. Generate specific "Storage Bucket" canaries
    # These are records that only exist in the 'cloud export' but not necessarily the live DB
    for i in range(5):
        canary_id = f"S3-EXPORT-CANARY-{i}"
        token = f"s3-honey-{uuid.uuid4().hex[:8]}"
        canaries.append({
            "record_id": canary_id,
            "canary_token": token,
            "source_system": "S3_BUCKET",
            "detection_tag": f"S3_CANARY_{i}"
        })

    data = {
        "metadata": {
            "generated_at": datetime.now().isoformat(),
            "seed": seed,
            "customer_count": num_customers,
            "account_count": len(accounts),
            "transaction_count": len(transactions),
            "canary_count": len(canaries),
            "note": "SYNTHETIC DATA - FOR LAB PURPOSES ONLY"
        },
        "customers": customers,
        "accounts": accounts,
        "transactions": transactions,
        "canaries": canaries
    }

    return data

if __name__ == "__main__":
    synthetic_data = generate_synthetic_data()
    with open("seed_data.json", "w") as f:
        json.dump(synthetic_data, f, indent=4)
    print("Successfully generated seed_data.json")
