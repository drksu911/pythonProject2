import re
from collections import Counter
from typing import Any, Dict, List


def process_bank_search(
    data: List[Dict[str, Any]], search: str
) -> List[Dict[str, Any]]:
    """
    Ищет транзакции по заданной строке в описании с использованием регулярных выражений.

    Args:
        data (List[Dict[str, Any]]): Список словарей с транзакциями
        search (str): Строка для поиска в описании транзакций

    Returns:
        List[Dict[str, Any]]: Отфильтрованный список транзакций
    """
    try:
        pattern = re.compile(search, re.IGNORECASE)
        return [
            transaction
            for transaction in data
            if "description" in transaction
            and pattern.search(transaction["description"])
        ]
    except re.error:
        # В случае ошибки в регулярном выражении возвращаем пустой список
        return []


def process_bank_operations(
    data: List[Dict[str, Any]], categories: List[str]
) -> Dict[str, int]:
    """
    Подсчитывает количество операций по заданным категориям.

    Args:
        data (List[Dict[str, Any]]): Список словарей с транзакциями
        categories (List[str]): Список категорий для подсчета

    Returns:
        Dict[str, int]: Словарь с количеством операций по категориям
    """
    # Приводим категории к нижнему регистру для регистронезависимого поиска
    categories_lower = [cat.lower() for cat in categories]

    # Создаем счетчик с явной аннотацией типа
    counter: Counter[str] = Counter()

    for transaction in data:
        if "description" in transaction:
            description = transaction["description"].lower()
            # Проверяем, содержит ли описание любую из категорий
            for category in categories_lower:
                if category in description:
                    counter[category] += 1
                    break  # Прерываем цикл после первого совпадения

    return dict(counter)
