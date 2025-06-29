from typing import Union


def get_mask_card_number(card_number: Union[str, int]) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску."""

    card_str = str(card_number).strip()
    name_pay = ""
    number_pay = ""
    for symbol in card_str:
        if symbol.isdigit():
            number_pay += symbol
        else:
            name_pay += symbol
    masked = f"{name_pay}{number_pay[:4]} {number_pay[4:6]}** **** {number_pay[-4:]}"
    return masked


def get_mask_account(account_number: Union[str, int]) -> str:
    """Функция принимает на вход номер счета и возвращает его маску"""

    account_str = str(account_number).strip()
    masked = f"Счет **{account_str[-4:]}"
    return masked
