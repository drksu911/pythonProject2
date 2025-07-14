from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(users_data: str) -> str:
    """Функция обработки информации о картах и счетах"""
    if users_data.startswith("Счет"):
        masked_data = get_mask_account(users_data)
    else:
        masked_data = get_mask_card_number(users_data)

    return masked_data


def get_date(date_info: str) -> str:
    """Функция форматирования даты ДД.ММ.ГГГГ"""

    date_str = date_info.strip()
    masked = f"{date_str[8:10]}.{date_str[5:7]}.{date_str[:4]}"
    return masked


print("Введите номер счета или номер карты", sep="\n")
users_data = input()
date_info = "2024-03-11T02:26:18.671407"
print(mask_account_card(users_data))
print(get_date(date_info))
