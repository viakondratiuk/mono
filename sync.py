import json

import mono
import sheet
from settings import get_mono_key


mono_key = get_mono_key()
transactions = mono.get_transactions(mono_key)
print(f"Mono: Got {len(transactions)} transactions")

# TODO: Save as debug part
# with open('transactions.json', 'w') as f:
#     json.dump(transactions, f, indent=4)

# with open('transactions.json', 'r') as f:
#     transactions = json.load(f)

values = []
for transaction in transactions:
    row = [
        transaction["id"],
        transaction["time"],
        transaction["description"],
        transaction["mcc"],
        transaction["originalMcc"],
        transaction["amount"],
        transaction["operationAmount"],
        transaction["currencyCode"],
        transaction["commissionRate"],
        transaction["cashbackAmount"],
        transaction["balance"],
        transaction["hold"],
        transaction["receiptId"],
    ]
    values.append(row)

body = {
    'values': values
}

sheet.save(body)
