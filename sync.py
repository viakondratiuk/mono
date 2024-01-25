import json

import mono
import sheet
from settings import get_mono_key


mono_key = get_mono_key()
transactions = mono.get_transactions(mono_key)
print(f"Mono: extracted {len(transactions)} transactions")

# mono.dump(transactions)
# transactions = mono.load()

body = sheet.format(transactions)
sheet.save(body)
