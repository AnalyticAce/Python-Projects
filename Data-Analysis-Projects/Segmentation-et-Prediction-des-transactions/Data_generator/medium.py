import random
import json
from datetime import datetime, timedelta
from faker import Faker

fake = Faker()

def generate_transaction_data(num_companies, min_transactions, max_transactions):
    companies = []
    transactions = []

    # Generate company names and URLs
    for i in range(num_companies):
        company_name = fake.company()
        company = {
            "company_id": i + 1,
            "company_name": company_name,
            "company_url": generate_fake_url(company_name)
        }
        companies.append(company)

    # Generate transactions
    transaction_id = 1
    for company in companies:
        num_transactions = random.randint(min_transactions, max_transactions)

        for _ in range(num_transactions):
            transaction = {
                "transaction_id": transaction_id,
                "company_id": company["company_id"],
                "company_name": company["company_name"],
                "company_url": company["company_url"],
                "transaction_date": generate_random_date(),
                "transaction_time": generate_random_time(),
                "transaction_amount": generate_random_amount(),
                "transaction_details": generate_random_details()
            }

            shuffle_transaction_items(transaction)

            transactions.append(transaction)
            transaction_id += 1

    transactions = introduce_messy_data(transactions)

    random.shuffle(transactions)

    return transactions


def shuffle_transaction_items(transaction):
    items = list(transaction.items())
    random.shuffle(items)
    shuffled_transaction = dict(items)
    transaction.clear()
    transaction.update(shuffled_transaction)


def introduce_messy_data(transactions):
    num_missing_values = random.randint(50, 200)
    for _ in range(num_missing_values):
        transaction = random.choice(transactions)
        field = random.choice(["company_name", "transaction_date", "transaction_time", "transaction_amount"])
        transaction[field] = None

    num_inconsistent_names = random.randint(20, 50)
    for _ in range(num_inconsistent_names):
        transaction = random.choice(transactions)
        transaction["company_name"] = fake.random_element()

    num_inconsistent_dates = random.randint(20, 50)
    for _ in range(num_inconsistent_dates):
        transaction = random.choice(transactions)
        transaction["transaction_date"] = generate_random_date()

    num_incorrect_amounts = random.randint(20, 50)
    for _ in range(num_incorrect_amounts):
        transaction = random.choice(transactions)
        transaction["transaction_amount"] = round(random.uniform(100000, 1000000), 2)

    return transactions


def generate_random_date():
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 12, 31)
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date.strftime("%Y-%m-%d")

def generate_random_time():
    random_time = datetime.strptime(f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}", "%H:%M")
    return random_time.strftime("%H:%M")

def generate_random_amount():
    return round(random.uniform(10, 10000), 2)


def generate_random_details():
    return fake.text(max_nb_chars=200)

def generate_fake_url(company_name):
    domain = ".com"
    if " " in company_name:
        company_name = company_name.replace(" ", "-")
    if "," in company_name:
        company_name = company_name.replace(",", "")
    if "&" in company_name:
        company_name = company_name.replace("&", "and")
    if len(company_name.split()) > 1:
        subdomain = "-".join(company_name.split()[:-1])
        company_name = company_name.split()[-1]
        return f"http://{subdomain}.{company_name}{domain}"
    return f"http://{company_name}{domain}"

num_companies = random.randint(50, 200)
min_transactions = 20
max_transactions = 30

transactions = generate_transaction_data(num_companies, min_transactions, max_transactions)

transaction_data = json.dumps(transactions, separators=(",", ":"))

with open("Data/transaction_data_messy.json", "w") as file:
    file.write(transaction_data)

print("Transaction data has been generated and saved to Data folder.")