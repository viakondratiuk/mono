from pprint import pprint

import mono
import sheet
from settings import get_mono_key


# mono_key = get_mono_key()
# transactions = mono.get_transactions(mono_key)

# pprint(transactions)

body = {
    'values': [
        ['A1', 'B1', 'C1', 'D1'],
        ['A2', 'B2', 'C2', 'D2'],
    ]
}
sheet.save(body)
