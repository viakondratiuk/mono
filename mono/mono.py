import json

import requests

import settings
from settings import logger


def get_transactions(from_: int, to_: int) -> list[dict[str, any]]:
    mono_key = settings.get_mono_key()
    url = settings.MONO_API_URL.format(settings.MONO_ACCOUNT, from_, to_)
    logger.info(f"...Mono: Url {url}")

    response = requests.get(url, headers={"X-Token": mono_key})
    json_ = response.json()
    if "errorDescription" in json_:
        logger.warning(f"...Mono: Error {json_}")
        return []

    logger.info(f"...Mono: Extracted {len(json_)} transactions")
    return json_


def dump(transactions) -> None:
    with open("../transactions.json", "w", encoding="utf-8") as f:
        json.dump(transactions, f, indent=4, ensure_ascii=False)
    logger.info("...Mono: Transactions dumped to file successfully.")


def load() -> str:
    with open("../transactions.json", "r") as f:
        data = json.load(f)
    logger.info("...Mono: Transactions loaded from file successfully.")
    return data
