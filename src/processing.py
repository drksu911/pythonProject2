from typing import Any, Dict, List


def filter_by_state(
    operations: List[Dict[str, Any]], state: str = "EXECUTED"
) -> List[Dict[str, Any]]:
    """
    Фильтрует список операций по статусу.

    Args:
        operations (List[Dict[str, Any]]): Список операций (словарей)
        state (str, optional): Статус для фильтрации. По умолчанию "EXECUTED".

    Returns:
        List[Dict[str, Any]]: Отфильтрованный список операций
    """
    return [operation for operation in operations if operation.get("state") == state]


def sort_by_date(
    operations: List[Dict[str, Any]], reverse: bool = True
) -> List[Dict[str, Any]]:
    """
    Сортирует список операций по дате.

    Args:
        operations (List[Dict[str, Any]]): Список операций (словарей)
        reverse (bool, optional): Порядок сортировки (True - по убыванию, False - по возрастанию).
                                  По умолчанию True.

    Returns:
        List[Dict[str, Any]]: Отсортированный список операций
    """
    return sorted(operations, key=lambda x: x["date"], reverse=reverse)
