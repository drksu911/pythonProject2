import os
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()


def convert_amount_to_rub(transaction: Dict[str, Any]) -> float:
    """Конвертирует сумму транзакции в рубли."""
    try:
        amount = float(transaction["operationAmount"]["amount"])
        currency = transaction["operationAmount"]["currency"]["code"]

        if currency == "RUB":
            return amount

        if currency in ["USD", "EUR"]:
            return convert_currency(amount, currency)

        return amount

    except (KeyError, ValueError, TypeError):
        return 0.0


def convert_currency(amount: float, currency: str) -> float:
    """Конвертирует сумму в рубли по текущему курсу."""
    api_key = os.getenv("API_KEY")
    api_url = os.getenv("API_URL")

    if not api_key or not api_url:
        raise ValueError("API credentials not configured")

    try:
        headers = {"apikey": api_key}
        params = {"base": currency, "symbols": "RUB"}

        response = requests.get(api_url, headers=headers, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        rate = data["rates"]["RUB"]

        return amount * rate

    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Error converting currency: {e}")
        return 0.0
