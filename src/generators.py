from typing import Any, Dict, Iterator, List


def filter_by_currency(
    transactions: List[Dict[str, Any]], currency_code: str
) -> Iterator[Dict[str, Any]]:
    """
    Фильтрует транзакции по заданной валюте и возвращает итератор.

    Args:
        transactions (List[Dict[str, Any]]): Список транзакций
        currency_code (str): Код валюты для фильтрации (например, "USD")

    Yields:
        Dict[str, Any]: Транзакции в заданной валюте
    """
    for transaction in transactions:
        operation_amount = transaction.get("operationAmount", {})
        currency = operation_amount.get("currency", {})
        if currency.get("code") == currency_code:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генератор, который возвращает описание каждой операции по очереди.

    Args:
        transactions (List[Dict[str, Any]]): Список транзакций

    Yields:
        str: Описание операции
    """
    for transaction in transactions:
        yield transaction.get("description", "")


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генератор номеров банковских карт в заданном диапазоне.

    Args:
        start (int): Начальное значение диапазона
        end (int): Конечное значение диапазона

    Yields:
        str: Номер карты в формате XXXX XXXX XXXX XXXX
    """
    for number in range(start, end + 1):
        # Форматируем номер с ведущими нулями
        card_str = str(number).zfill(16)
        # Разбиваем на группы по 4 цифры
        formatted_card = " ".join([card_str[i : i + 4] for i in range(0, 16, 4)])
        yield formatted_card
