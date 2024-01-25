
import json
import requests
import time


def get_transactions(api_key: str, from_: int, to_: int) -> str:
    ACCOUNT = "0"
    TO = int(time.time())
    FROM = TO - 24*3600
    API_URL = f"https://api.monobank.ua/personal/statement/{ACCOUNT}/{from_}/{to_}"
    headers = {'X-Token': api_key}
    
    response = requests.get(API_URL, headers=headers)
    json = response.json()
    print(f"Mono: extracted {len(json)} transactions")

    return json


def dump(transactions: str) -> None:
    with open('transactions.json', 'w') as f:
        json.dump(transactions, f, indent=4)


def load() -> str:
    with open('transactions.json', 'r') as f:
        return json.load(f)
    