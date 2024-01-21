from pprint import pprint

from mono import get_transactions
from settings import get_mono_key


mono_key = get_mono_key()
transactions = get_transactions(mono_key)

pprint(transactions)
