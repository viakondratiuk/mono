from tinydb import TinyDB
from tinydb import Query

from settings import logger
from settings import DB_FILE

db = TinyDB(DB_FILE)
processed_ids_table = db.table("processed_ids")
last_updated_table = db.table("last_updated")


def get_last_updated() -> int:
    result = last_updated_table.get(Query().name == "last_updated")
    if result:
        return result["timestamp"]
    return -1


def save_last_updated(timestamp):
    last_updated_table.upsert({"name": "last_updated", "timestamp": timestamp}, Query().name == "last_updated")


def read_ids():
    return {item["id"] for item in processed_ids_table.all()}


def save_ids(processed_ids):
    processed_ids_table.truncate()
    processed_ids_table.insert_multiple([{"id": pid} for pid in processed_ids])


def filter_dups(transactions: list[dict[str, any]]) -> list[dict[str, any]]:
    processed_ids = read_ids()
    new_transactions = [t for t in transactions if t["id"] not in processed_ids]
    logger.info(f"...Filter: filtered {len(transactions) - len(new_transactions)} transactions")

    save_ids(processed_ids.union(t["id"] for t in new_transactions))

    return new_transactions
