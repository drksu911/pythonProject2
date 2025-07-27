from datetime import datetime
from typing import Union


def mask_account_card(number_acc_or_card: str) -> str:
    """Функция обработки информации о картах и счетах"""
    if not isinstance(number_acc_or_card, str):
        raise ValueError("Входные данные должны быть строкой")

    cleaned = number_acc_or_card.strip()
    if not cleaned:
        raise ValueError("Пустая строка")

    parts = cleaned.split()

    if cleaned.startswith("Счет"):
        if len(parts) < 2:
            raise ValueError("Не указан номер счета")

        account_num = parts[-1]

        if not account_num.isdigit():
            raise ValueError("Номер счета должен содержать только цифры")

        if len(account_num) < 4:
            raise ValueError("Номер счета должен содержать минимум 4 цифры")

        return f"{' '.join(parts[:-1])} **{account_num[-4:]}"

    else:
        if len(parts) < 2:
            raise ValueError("Не указан номер карты")

        card_num = parts[-1]

        if not card_num.isdigit():
            raise ValueError("Номер карты должен содержать только цифры")

        if len(card_num) != 16:
            raise ValueError("Номер карты должен содержать ровно 16 цифр")

        return f"{' '.join(parts[:-1])} {card_num[:4]} {card_num[4:6]}** **** {card_num[-4:]}"


def get_date(date_info: Union[str, None]) -> str:
    """
    Функция форматирования даты из строки в формате ДД.ММ.ГГГГ
    Обрабатывает даты в формате ISO (YYYY-MM-DD или YYYY-MM-DDTHH:MM:SS)
    """
    if date_info is None:
        raise AttributeError("Дата не может быть None")

    date_str = date_info.strip()

    if not date_str:
        raise ValueError("Пустая строка даты")

    try:
        # Пробуем распарсить дату в ISO формате
        dt = datetime.fromisoformat(date_str)
        return dt.strftime("%d.%m.%Y")
    except ValueError:
        raise ValueError(
            "Неверный формат даты. Ожидается ISO формат (YYYY-MM-DD или YYYY-MM-DDTHH:MM:SS)"
        )


print(mask_account_card("Visa 1234567890123456"))
print(get_date("2023-12-31T23:59:59"))
