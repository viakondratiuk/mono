import json

from google.oauth2.service_account import Credentials

MONO_KEY_PATH = "keys/mono.json"

SHEETS_SERVICE_ACCOUNT = 'keys/sheets.json'
SHEETS_SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SHEETS_ID = '1L1f-c31oWSG-CTGuSe1XqSAWWHwX6_7XiUTlBoeHh3E'


def get_mono_key() -> str:
    with open(MONO_KEY_PATH, "r") as file:
        data = json.load(file)
    
    return data["API_KEY"]


def get_sheet_credentials():
    return Credentials.from_service_account_file(SHEETS_SERVICE_ACCOUNT, scopes=SHEETS_SCOPES)
