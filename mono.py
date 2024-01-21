
import requests
import time


def get_transactions(api_key: str) -> str:
    ACCOUNT = "0"
    TO = int(time.time())
    FROM = TO - 24*3600
    API_URL = f"https://api.monobank.ua/personal/statement/{ACCOUNT}/{FROM}/{TO}"
    headers = {'X-Token': api_key}
    
    response = requests.get(API_URL, headers=headers)
    
    return response.json()
