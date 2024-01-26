import argparse
import time
from datetime import datetime

import mono
import sheet
from processed import filter_dups
from settings import get_mono_key


def get_epoch_time(date_str):
    date_obj = datetime.strptime(date_str, '%d.%m.%y')
    epoch_time = int(time.mktime(date_obj.timetuple()))

    return epoch_time


def main(from_date, to_date, output=None):
    mono_key = get_mono_key()

    from_ = get_epoch_time(from_date)
    to_ = get_epoch_time(to_date)
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
    parser.add_argument("--from", "-f", dest="from_date", required=True,
                        help="Start date for fetching transactions (format: DD.MM.YY)")
    parser.add_argument("--to", "-t", dest="to_date", required=True,
                        help="End date for fetching transactions (format: DD.MM.YY)")
    args = parser.parse_args()

    main(args.from_date, args.to_date, args.output)
