import argparse
from datetime import datetime
from typing import Optional

import mono
import sheet
from date import get_end_of_day
from date import get_timestamp
from db import filter_dups
from db import get_last_updated
from db import save_last_updated
from settings import DATE_FORMAT
from settings import get_mono_key


def main(from_date: datetime, to_date: datetime, output: Optional[bool]) -> None:
    mono_key = get_mono_key()

    from_timestamp = get_timestamp(from_date)
    to_timestamp = get_timestamp(to_date, end_of_day=True)
    all_transactions = mono.get_transactions(mono_key, from_timestamp, to_timestamp)
    # all_transactions = mono.load()
    if output:
        mono.dump(all_transactions)

    filtered_transactions = filter_dups(all_transactions)
    body = sheet.format(filtered_transactions)
    sheet.save(body)

    if filtered_transactions:
        most_recent_timestamp = max(t["time"] for t in filtered_transactions)
        save_last_updated(most_recent_timestamp)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to sync transactions from a bank API to a Google Spreadsheet")
    parser.add_argument("--output", "-o", action="store_true",
                        help="Path to the output file where transactions will be saved")
    parser.add_argument("--from", "-f", dest="from_date", type=lambda d: datetime.strptime(d, DATE_FORMAT),
                        help="Start date for fetching transactions (format: DD.MM.YY)")
    parser.add_argument("--to", "-t", dest="to_date", type=lambda d: datetime.strptime(d, DATE_FORMAT),
                        help="End date for fetching transactions (format: DD.MM.YY)")
    parser.add_argument("--day", "-d", type=lambda d: datetime.strptime(d, DATE_FORMAT),
                        help="Fetch transactions for a day (format: DD.MM.YY)")

    args = parser.parse_args()

    from_date = None
    to_date = None

    if args.day:
        from_date = args.day
        to_date = get_end_of_day(args.day)
    elif args.from_date:
        from_date = args.from_date
        to_date = args.to_date if args.to_date else datetime.now()
    else:
        last_updated = get_last_updated()
        from_date = datetime.fromtimestamp(last_updated) if last_updated != -1 else datetime.now()
        to_date = datetime.now()

    main(from_date, to_date, args.output)
