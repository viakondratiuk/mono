import json
import logging

from google.oauth2.service_account import Credentials

PROJECT_PATH = "/Users/viakondratiuk/Library/Mobile Documents/com~apple~CloudDocs/Projects/MonoSheets/"

MONO_CREDENTIALS = PROJECT_PATH + "keys/mono.json"
MONO_ACCOUNT = ["0", "Zo8gULDo8uViptjkYqEf3Q"]
# MONO_ACCOUNT = "Zo8gULDo8uViptjkYqEf3Q"
MONO_API_URL = "https://api.monobank.ua/personal/statement/{}/{}/{}"

SHEETS_CREDENTIALS = PROJECT_PATH + "keys/sheets.json"
SHEETS_SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SHEETS_ID = "1oCe1veZB8FSpUsYZboErNpJr7T-0rq__WxZ95q0ZawU"

DB_FILE = PROJECT_PATH + "db.json"

DATE_FORMAT = "%d.%m.%y"

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def get_mono_key() -> str:
    with open(MONO_CREDENTIALS, "r") as file:
        data = json.load(file)
        return data.get("API_KEY")


def get_sheet_credentials():
    return Credentials.from_service_account_file(SHEETS_CREDENTIALS, scopes=SHEETS_SCOPES)
