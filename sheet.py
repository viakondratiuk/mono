from datetime import datetime
from datetime import timezone
from zoneinfo import ZoneInfo

from googleapiclient.discovery import build

from settings import get_sheet_credentials
from settings import SHEETS_ID


def save(body: dict) -> None:
    credentials = get_sheet_credentials()
    service = build('sheets', 'v4', credentials=credentials)

    range_ = 'Sheet1!A3:A'

    result = service.spreadsheets().values().append(
        spreadsheetId=SHEETS_ID, range=range_,
        valueInputOption='USER_ENTERED',
        insertDataOption='INSERT_ROWS',
        body=body).execute()

    print(f"Appended {result.get('updates').get('updatedRows')} rows.")


def format(transactions: list[dict[str, any]]) -> dict[str, any]:
    keys_order = [
        "time", "amount", "mcc", "description",
        "commissionRate", "balance",
    ]
    kyiv_timezone = ZoneInfo("Europe/Kiev")
    values = []
    for transaction in transactions:
        row = []
        for key in keys_order:
            if key == 'time':
                time_value = transaction.get(key, 0)
                utc_dt = datetime.fromtimestamp(time_value, tz=timezone.utc)
                kyiv_dt = utc_dt.astimezone(kyiv_timezone) 
                date = kyiv_dt.strftime('%Y-%m-%d')
                time = kyiv_dt.strftime('%H:%M:%S')
                row.append(date)
                row.append(time)
            elif key == "amount" or key == "balance":
                value = transaction.get(key, 0)
                row.append(value / 100)
            else:
                row.append(transaction.get(key, 'N/A'))
        
        values.append(row)

    return {'values': values}
