import json
import logging

from google.oauth2.service_account import Credentials

MONO_CREDENTIALS = "keys/mono.json"
MONO_ACCOUNT = "0"
MONO_API_URL = "https://api.monobank.ua/personal/statement/{}/{}/{}"

SHEETS_CREDENTIALS = "keys/sheets.json"
SHEETS_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SHEETS_ID = "1L1f-c31oWSG-CTGuSe1XqSAWWHwX6_7XiUTlBoeHh3E"

DB_FILE = "db.json"

DATE_FORMAT = "%d.%m.%y"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def get_mono_key() -> str:
    with open(MONO_CREDENTIALS, "r") as file:
        data = json.load(file)
        return data.get("API_KEY")


def get_sheet_credentials():
    return Credentials.from_service_account_file(SHEETS_CREDENTIALS, scopes=SHEETS_SCOPES)
