from googleapiclient.discovery import build

from settings import get_sheet_credentials
from settings import SHEETS_ID


def save(body: str) -> None:
    credentials = get_sheet_credentials()
    service = build('sheets', 'v4', credentials=credentials)

    # Specify the range and values to be updated
    range_ = 'Sheet1!A2:M5'  # Example range

    # Call the Sheets API to update the range
    result = service.spreadsheets().values().update(
        spreadsheetId=SHEETS_ID, range=range_,
        valueInputOption='RAW', body=body).execute()

    print(f"Sheets: updated {result.get('updatedCells')} cells.")
