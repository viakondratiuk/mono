from pprint import pprint

import mono
import sheet
from settings import get_mono_key


# mono_key = get_mono_key()
# transactions = mono.get_transactions(mono_key)

# pprint(transactions)

test = {"test1": 1, "test2": 2}
sheet.save(test)
