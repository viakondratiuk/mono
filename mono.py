import json

import requests

from settings import MONO_ACCOUNT
from settings import MONO_API_URL
from settings import logger


def get_transactions(api_key: str, from_: int, to_: int) -> list[dict[str, any]]:
    response = requests.get(MONO_API_URL.format(MONO_ACCOUNT, from_, to_), headers={"X-Token": api_key})
    json_ = response.json()
    if "errorDescription" in json_:
        logger.warning("...Mono: Too many requests, try later")
        return []

    logger.info(f"...Mono: Extracted {len(json_)} transactions")
    return json_


def dump(transactions) -> None:
    with open("transactions.json", "w", encoding="utf-8") as f:
        json.dump(transactions, f, indent=4, ensure_ascii=False)
    logger.info("...Mono: Transactions dumped to file successfully.")


def load() -> str:
    with open("transactions.json", "r") as f:
        data = json.load(f)
    logger.info("...Mono: Transactions loaded from file successfully.")
    return data
