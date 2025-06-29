from typing import Union


def get_mask_card_number(card_number: Union[str, int]) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску."""

    card_str = str(card_number).strip()
    masked = f"{card_str[:4]} {card_str[4:6]}** **** {card_str[-4:]}"
    return masked


def get_mask_account(account_number: Union[str, int]) -> str:
    """Функция принимает на вход номер счета и возвращает его маску"""

    account_str = str(account_number).strip()
    masked = f"**{account_str[-4:]}"
    return masked


card_number = "1234567890123456"
account_number = "73654108430135874305"

print(get_mask_card_number(card_number))
print(get_mask_account(account_number))
