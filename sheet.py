from typing import List, Dict, Any
from datetime import datetime

from googleapiclient.discovery import build

from settings import get_sheet_credentials
from settings import SHEETS_ID


def save(body: str) -> None:
    credentials = get_sheet_credentials()
    service = build('sheets', 'v4', credentials=credentials)

    range_ = 'Sheet1!A2:N5'

    result = service.spreadsheets().values().update(
        spreadsheetId=SHEETS_ID, range=range_,
        valueInputOption='RAW', body=body).execute()

    print(f"Sheets: updated {result.get('updatedCells')} cells.")


def format(transactions: list[dict[str, any]]) -> dict[str, any]:
    keys_order = [
        "id", "time", "description", "mcc", "originalMcc",
        "amount", "operationAmount", "currencyCode", "commissionRate",
        "cashbackAmount", "balance", "hold", "receiptId"
    ]

    values = []
    for transaction in transactions:
        row = []
        for key in keys_order:
            if key == 'time':
                time_value = transaction.get(key, 0)
                date = datetime.utcfromtimestamp(time_value).strftime('%Y-%m-%d')
                time = datetime.utcfromtimestamp(time_value).strftime('%H:%M:%S')
                row.append(date)
                row.append(time)
            else:
                row.append(transaction.get(key, 'N/A'))
        
        values.append(row)

    return {'values': values}
