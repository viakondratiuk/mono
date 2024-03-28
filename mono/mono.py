import json

import requests

import settings
from settings import logger


def get_transactions(from_: int, to_: int) -> list:
    transactions = []
    for account in settings.MONO_ACCOUNT:
        url = settings.MONO_API_URL.format(account, from_, to_)
        logger.info(f"...Mono: Url {url}")

        response = requests.get(url, headers={"X-Token": settings.get_mono_key()})
        if response.status_code != 200 or "errorDescription" in response.json():
            error_info = response.json().get("errorDescription", "No error description")
            logger.warning(f"...Mono: Error {error_info}")
            continue

        account_transactions = response.json()
        account_type = "slava" if account == "0" else "white"
        for t in account_transactions:
            t.update({"account": account_type})
            transactions.append(t)

        logger.info(f"...Mono: Extracted {len(account_transactions)} transactions")

    return sorted(transactions, key=lambda x: x["time"], reverse=True) 


def dump(transactions) -> None:
    with open("../transactions.json", "w", encoding="utf-8") as f:
        json.dump(transactions, f, indent=4, ensure_ascii=False)
    logger.info("...Mono: Transactions dumped to file successfully.")


def load() -> str:
    with open("../transactions.json", "r") as f:
        data = json.load(f)
    logger.info("...Mono: Transactions loaded from file successfully.")
    return data
