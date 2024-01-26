from settings import PROCESSED_IDS_FILE
from settings import logger


def read_ids():
    try:
        with open(PROCESSED_IDS_FILE, 'r') as file:
            return {line.strip() for line in file}
    except FileNotFoundError:
        return set()


def save_ids(processed_ids):
    with open(PROCESSED_IDS_FILE, 'w') as file:
        for pid in processed_ids:
            file.write(f"{pid}\n")


def filter_dups(transactions: list[dict[str, any]]) -> list[dict[str, any]]:
    processed_ids = read_ids()
    new_transactions = list(filter(lambda t: t['id'] not in processed_ids, transactions))
    logger.info(f"...Filter: filtered {len(transactions) - len(new_transactions)} transactions")

    processed_ids.update(t['id'] for t in new_transactions)
    save_ids(processed_ids)

    return new_transactions
