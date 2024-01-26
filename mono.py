import json

import requests

from settings import MONO_ACCOUNT
from settings import MONO_API_URL


def get_transactions(api_key: str, from_: int, to_: int) -> str:
    response = requests.get(MONO_API_URL.format(MONO_ACCOUNT, from_, to_), headers={'X-Token': api_key})
    json_ = response.json()
    print(f"Mono: extracted {len(json_)} transactions")

    return json_


def dump(transactions: str) -> None:
    with open('transactions.json', 'w') as f:
        json.dump(transactions, f, indent=4)


def load() -> str:
    with open('transactions.json', 'r') as f:
        return json.load(f)
