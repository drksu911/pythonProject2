date_list = [
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


def sort_by_date(date_list: list[dict], reverse: bool = True) -> list[dict]:
    """Сортировка по дате"""

    sorted_list = date_list.copy()
    sorted_list.sort(key=lambda x: x["date"], reverse=reverse)
    return sorted_list


print("Функция возвращает словари по заданному значению")
print(filter_by_state(date_list))
print(filter_by_state(date_list, "CANCELED"))


print("Функция сортирует по убыванию (новые - старые)")
print(sort_by_date(date_list))

print("Функция сортирует по возрастанию (старые - новые)")
print(sort_by_date(date_list, reverse=False))
