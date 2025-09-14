import logging
import os
from decimal import Decimal, InvalidOperation
from typing import Any, Dict

import requests
from dotenv import load_dotenv
from requests.exceptions import RequestException

# Загрузка переменных окружения
load_dotenv()

# Настройка логера для модуля external_api
logger = logging.getLogger("external_api")
logger.setLevel(logging.DEBUG)

# Создаем папку logs, если она не существует
os.makedirs("logs", exist_ok=True)

# Создаем file_handler для записи логов в файл с указанием кодировки UTF-8
file_handler = logging.FileHandler("logs/external_api.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Создаем formatter для определения формата записей логов
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)

# Добавляем handler к логеру
logger.addHandler(file_handler)

# Отключаем распространение логов в корневой логер
logger.propagate = False


def convert_currency_to_rub(transaction: Dict[str, Any]) -> float:
    """
    Конвертирует сумму транзакции в рубли.

    Args:
        transaction (Dict[str, Any]): Словарь с данными о транзакции

    Returns:
        float: Сумма транзакции в рублях

    Raises:
        ValueError: Если не удается конвертировать сумму
    """
    try:
        operation_amount = transaction.get("operationAmount", {})
        amount = Decimal(str(operation_amount.get("amount", 0)))
        currency_code = operation_amount.get("currency", {}).get("code", "RUB")

        # Если валюта уже в рублях, возвращаем сумму
        if currency_code == "RUB":
            return float(amount)

        # Конвертируем USD и EUR
        if currency_code in ["USD", "EUR"]:
            api_key = os.getenv("EXCHANGE_RATE_API_KEY")
            if not api_key:
                logger.error("API ключ для конвертации валют не найден")
                raise ValueError("API ключ для конвертации валют не найден")

            # Получаем курс валют
            exchange_rate = get_exchange_rate(currency_code, api_key)
            converted_amount = amount * Decimal(str(exchange_rate))

            return float(converted_amount)

        # Для других валют возвращаем исходную сумму
        logger.warning(f"Конвертация для валюты {currency_code} не поддерживается")
        return float(amount)

    except (InvalidOperation, ValueError, KeyError) as e:
        logger.error(f"Ошибка конвертации валюты: {str(e)}")
        raise ValueError(f"Ошибка конвертации валюты: {str(e)}")


def get_exchange_rate(currency_code: str, api_key: str) -> float:
    """
    Получает текущий курс валюты к рублю через внешнее API.

    Args:
        currency_code (str): Код валюты (USD или EUR)
        api_key (str): API ключ для доступа к сервису

    Returns:
        float: Курс валюты к рублю

    Raises:
        ValueError: Если не удается получить курс валюты
    """
    url = f"https://api.apilayer.com/exchangerates_data/latest?base={currency_code}&symbols=RUB"

    try:
        headers = {"apikey": api_key}
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        if not data.get("success", False):
            error_info = data.get("error", {}).get("info", "Unknown error")
            raise ValueError(f"API error: {error_info}")

        rates = data.get("rates", {})
        rub_rate = rates.get("RUB")

        if rub_rate is None:
            raise ValueError("Курс рубля не найден в ответе API")

        return rub_rate

    except RequestException as e:
        logger.error(f"Ошибка при запросе к API: {str(e)}")
        raise ValueError(f"Ошибка при запросе к API: {str(e)}")
    except (KeyError, ValueError) as e:
        logger.error(f"Ошибка при обработке ответа API: {str(e)}")
        raise ValueError(f"Ошибка при обработке ответа API: {str(e)}")
