from datetime import datetime
from typing import Dict, List

date_lists = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]


def filter_by_state(date_list: list[dict], state: str = "EXECUTED") -> list[dict]:
    """Возвращает словари по указанному значению"""
    new_list = []
    for item in date_list:
        if isinstance(item, dict) and item.get("state") == state:
            new_list.append(item)
    return new_list


def filter_by_states(data: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """Фильтрует список словарей по значению ключа 'state'"""
    if not isinstance(data, list):
        raise TypeError("Входные данные должны быть списком")

    return [
        item for item in data if isinstance(item, dict) and item.get("state") == state
    ]


def sort_by_date(data: List[Dict], reverse: bool = True) -> List[Dict]:
    """Сортирует список словарей по дате"""
    if not isinstance(data, list):
        raise TypeError("Входные данные должны быть списком")

    try:
        return sorted(
            data, key=lambda x: datetime.fromisoformat(x["date"]), reverse=reverse
        )
    except (KeyError, ValueError) as e:
        raise ValueError(f"Некорректный формат даты: {e}")


print("Функция возвращает словари по заданному значению")
print(filter_by_state(date_lists))
print(filter_by_state(date_lists, "CANCELED"))


print("Функция сортирует по убыванию (новые - старые)")
print(sort_by_date(date_lists))

print("Функция сортирует по возрастанию (старые - новые)")
print(sort_by_date(date_lists, reverse=False))
