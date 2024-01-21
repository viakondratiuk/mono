import requests

import gspread
from oauth2client.service_account import ServiceAccountCredentials


def save(data: str) -> None:
    # Google Sheets setup
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
    client = gspread.authorize(creds)
    sheet = client.open("Test").sheet1

    for item in data:
        row = [str(value) for value in item.values()]
        sheet.append_row(row)

    print("Data written to Google Sheet successfully.")
