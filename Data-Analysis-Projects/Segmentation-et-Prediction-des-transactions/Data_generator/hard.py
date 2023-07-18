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

        # Generate irregular transaction frequencies
        transaction_dates = generate_irregular_transaction_dates(num_transactions)

        for date in transaction_dates:
            transaction = {
                "transaction_id": transaction_id,
                "company_id": company["company_id"],
                "company_name": company["company_name"],
                "company_url": company["company_url"],
                "transaction_date": date.strftime("%Y-%m-%d"),
                "transaction_time": generate_random_time(),
                "transaction_amount": generate_random_amount(),
                "transaction_details": generate_random_details()
            }

            # Shuffle the order of items within the transaction record
            shuffle_transaction_items(transaction)

            transactions.append(transaction)
            transaction_id += 1

    # Introduce some messy data
    transactions = introduce_messy_data(transactions)

    # Introduce duplicate transactions
    transactions = introduce_duplicate_transactions(transactions)

    # Randomize the order of transactions
    random.shuffle(transactions)

    return transactions


def generate_irregular_transaction_dates(num_transactions):
    transaction_dates = []

    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 12, 31)

    # Generate irregular transaction dates
    for _ in range(num_transactions):
        transaction_date = random_date_with_irregularity(start_date, end_date, transaction_dates)
        transaction_dates.append(transaction_date)

    return sorted(transaction_dates)

def generate_random_date():
    start_date = datetime(2022, 1, 1)
    end_date = datetime(2022, 12, 31)
    random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_date.strftime("%Y-%m-%d")

def random_date_with_irregularity(start_date, end_date, existing_dates):
    while True:
        transaction_date = random_date(start_date, end_date)

        # Check if the transaction date is not too close to an existing date
        too_close = any(abs((transaction_date - existing_date).days) < 7 for existing_date in existing_dates)

        if not too_close:
            return transaction_date


def random_date(start_date, end_date):
    return start_date + timedelta(days=random.randint(0, (end_date - start_date).days))


def shuffle_transaction_items(transaction):
    items = list(transaction.items())
    random.shuffle(items)
    shuffled_transaction = dict(items)
    transaction.clear()
    transaction.update(shuffled_transaction)


def introduce_messy_data(transactions):
    # Introduce missing values
    num_missing_values = random.randint(50, 200)
    for _ in range(num_missing_values):
        transaction = random.choice(transactions)
        field = random.choice(["company_name", "transaction_date", "transaction_time", "transaction_amount"])
        transaction[field] = None

    # Introduce inconsistent company names
    num_inconsistent_names = random.randint(20, 50)
    for _ in range(num_inconsistent_names):
        transaction = random.choice(transactions)
        transaction["company_name"] = fake.random_element()

    # Introduce inconsistent transaction dates
    num_inconsistent_dates = random.randint(20, 50)
    for _ in range(num_inconsistent_dates):
        transaction = random.choice(transactions)
        transaction["transaction_date"] = generate_random_date()

    # Introduce incorrect transaction amounts
    num_incorrect_amounts = random.randint(20, 50)
    for _ in range(num_incorrect_amounts):
        transaction = random.choice(transactions)
        transaction["transaction_amount"] = round(random.uniform(100000, 1000000), 2)

    return transactions


def introduce_duplicate_transactions(transactions):
    num_duplicates = random.randint(50, 200)
    num_transactions = len(transactions)

    for _ in range(num_duplicates):
        index = random.randint(0, num_transactions - 1)
        transaction = transactions[index]

        duplicate_transaction = {
            "transaction_id": num_transactions + 1,
            "company_id": transaction["company_id"],
            "company_name": transaction["company_name"],
            "company_url": transaction["company_url"],
            "transaction_date": transaction["transaction_date"],
            "transaction_time": transaction["transaction_time"],
            "transaction_amount": transaction["transaction_amount"],
            "transaction_details": transaction["transaction_details"]
        }

        transactions.append(duplicate_transaction)

    return transactions


def generate_random_time():
    random_time = datetime.strptime(f"{random.randint(0, 23):02d}:{random.randint(0, 59):02d}", "%H:%M")
    return random_time.strftime("%H:%M")


def generate_random_amount():
    return round(random.uniform(10, 10000), 2)


def generate_random_details():
    return fake.text(max_nb_chars=200)


def generate_fake_url(company_name):
    domain = ".com"  # Default domain
    if " " in company_name:  # Remove spaces and add hyphens
        company_name = company_name.replace(" ", "-")
    if "," in company_name:  # Remove commas
        company_name = company_name.replace(",", "")
    if "&" in company_name:  # Replace ampersand with "and"
        company_name = company_name.replace("&", "and")
    if len(company_name.split()) > 1:  # Generate subdomains for multi-word company names
        subdomain = "-".join(company_name.split()[:-1])
        company_name = company_name.split()[-1]
        return f"http://{subdomain}.{company_name}{domain}"
    return f"http://{company_name}{domain}"


# Configuration
num_companies = random.randint(50, 200)
min_transactions = 20
max_transactions = 30

# Generate transaction data
transactions = generate_transaction_data(num_companies, min_transactions, max_transactions)

# Convert transactions to a JSON string with all items on the same line
transaction_data = json.dumps(transactions, separators=(",", ":"))

# Save data to JSON file
with open("Data/transaction_data_final.json", "w") as file:
    file.write(transaction_data)

print("Transaction data has been generated and saved to Data folder.")
