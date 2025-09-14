from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_info: str) -> str:
    """
    Маскирует номер карты или счета в строке с информацией об аккаунте.

    Args:
        account_info (str): Строка с информацией об аккаунте в формате
                           "Тип Номер" (например, "Visa Platinum 7000792289606361")

    Returns:
        str: Строка с замаскированным номером карты или счета.

    Raises:
        ValueError: Если не удается извлечь номер из строки.
    """
    if not account_info or not account_info.strip():
        raise ValueError("Строка с информацией об аккаунте не может быть пустой")

    # Разделяем строку на части
    parts = account_info.split()

    if len(parts) < 2:
        raise ValueError("Строка должна содержать тип и номер карты/счета")

    # Извлекаем номер (последняя часть строки)
    number_str = parts[-1]

    # Проверяем, что номер состоит только из цифр
    if not number_str.isdigit():
        raise ValueError("Строка должна содержать тип и номер карты/счета")

    # Определяем тип аккаунта (все части кроме последней)
    account_type = " ".join(parts[:-1])

    # Определяем, является ли номер счетом или картой
    if account_type.lower() == "счет":
        masked_number = get_mask_account(number_str)
    else:
        # Проверяем, что номер карты имеет правильную длину
        if len(number_str) != 16:
            raise ValueError("Номер карты должен содержать 16 цифр")
        masked_number = get_mask_card_number(number_str)

    return f"{account_type} {masked_number}"


def get_date(date_string: str) -> str:
    """
    Преобразует дату из формата ISO в формат ДД.ММ.ГГГГ.

    Args:
        date_string (str): Дата в формате ISO (например, "2024-03-11T02:26:18.671407")

    Returns:
        str: Дата в формате ДД.ММ.ГГГГ (например, "11.03.2024")

    Raises:
        ValueError: Если строка не соответствует формату ISO.
    """
    if not date_string or "T" not in date_string:
        raise ValueError("Дата должна быть в формате ISO с разделителем 'T'")

    # Разделяем дату и время
    date_time_parts = date_string.split("T")

    if len(date_time_parts) != 2 or not date_time_parts[0] or not date_time_parts[1]:
        raise ValueError("Некорректный формат даты")

    try:
        # Извлекаем часть с датой
        date_part = date_time_parts[0]

        # Разделяем год, месяц и день
        date_components = date_part.split("-")

        if len(date_components) != 3:
            raise ValueError("Некорректный формат даты")

        year, month, day = date_components

        # Проверяем, что компоненты даты являются числами
        if not (year.isdigit() and month.isdigit() and day.isdigit()):
            raise ValueError("Некорректный формат даты")

        # Форматируем в нужный вид
        return f"{day}.{month}.{year}"
    except (IndexError, ValueError):
        raise ValueError("Некорректный формат даты")
