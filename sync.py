import argparse
from datetime import datetime

import mono
import sheet
from processed import filter_dups
from settings import DATE_FORMAT
from settings import get_mono_key


def get_end_of_day(date_obj):
    return date_obj.replace(hour=23, minute=59, second=59)


def get_epoch_time(date_obj, end_of_day=False):
    if end_of_day:
        date_obj = get_end_of_day(date_obj)
    epoch_time = int(date_obj.timestamp())
    return epoch_time


def main(from_date, to_date, output=None):
    mono_key = get_mono_key()

    from_ = get_epoch_time(from_date)
    to_ = get_epoch_time(to_date, end_of_day=True)
    all_transactions = mono.get_transactions(mono_key, from_, to_)
    # all_transactions = mono.load()
    if output:
        mono.dump(all_transactions)

    filtered_transactions = filter_dups(all_transactions)
    body = sheet.format(filtered_transactions)
    sheet.save(body)


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

    if args.day:
        args.from_date = args.day
        args.to_date = get_end_of_day(args.day)

    if not args.from_date:
        raise ValueError("The '--from' date must be provided or use '--day' to specify a day.")
    if not args.to_date:
        args.to_date = datetime.now()

    main(args.from_date, args.to_date, args.output)
