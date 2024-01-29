import argparse
from datetime import datetime
from typing import Optional

import settings
from db import tinydb
from mono import mono
from sheets import sheet
from utils import date


def main(from_date: datetime, to_date: datetime, output: Optional[bool]) -> None:
    from_timestamp = date.to_timestamp(from_date)
    to_timestamp = date.to_timestamp(to_date, end_of_day=True)

    mono_key = settings.get_mono_key()
    all_transactions = mono.get_transactions(mono_key, from_timestamp, to_timestamp)
    # all_transactions = mono.load()
    if output:
        mono.dump(all_transactions)

    filtered_transactions = tinydb.filter_dups(all_transactions)
    body = sheet.format(filtered_transactions)
    sheet.save(body)

    if filtered_transactions:
        most_recent_timestamp = max(t["time"] for t in filtered_transactions)
        tinydb.save_last_updated(most_recent_timestamp)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to sync transactions from a bank API to a Google Spreadsheet")
    parser.add_argument("--output", "-o", action="store_true",
                        help="Path to the output file where transactions will be saved")
    parser.add_argument("--from", "-f", dest="from_date", type=lambda d: datetime.strptime(d, settings.DATE_FORMAT),
                        help="Start date for fetching transactions (format: DD.MM.YY)")
    parser.add_argument("--to", "-t", dest="to_date", type=lambda d: datetime.strptime(d, settings.DATE_FORMAT),
                        help="End date for fetching transactions (format: DD.MM.YY)")
    parser.add_argument("--day", "-d", type=lambda d: datetime.strptime(d, settings.DATE_FORMAT),
                        help="Fetch transactions for a day (format: DD.MM.YY)")

    args = parser.parse_args()

    from_date = None
    to_date = None

    if args.day:
        from_date = args.day
        to_date = date.get_end_of_day(args.day)
    elif args.from_date:
        from_date = args.from_date
        to_date = args.to_date if args.to_date else datetime.now()
    else:
        last_updated = tinydb.get_last_updated()
        from_date = datetime.fromtimestamp(last_updated) if last_updated != -1 else datetime.now()
        to_date = datetime.now()

    main(from_date, to_date, args.output)
