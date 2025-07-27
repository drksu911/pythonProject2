from typing import Union


def get_mask_card_number(card_number: Union[str, int]) -> str:
    """Функция принимает на вход номер карты и возвращает ее маску"""
    if card_number is None:
        raise AttributeError("Номер карты не может быть None")

    card_str = str(card_number).strip()

    if not card_str:
        raise ValueError("Номер карты не может быть пустым")

    # Извлекаем только цифры
    digits = [c for c in card_str if c.isdigit()]

    if len(digits) < 6:
        raise ValueError("Номер карты должен содержать минимум 6 цифр")

    # Находим начало и конец цифровой части
    first_digit_pos = next((i for i, c in enumerate(card_str) if c.isdigit()), 0)
    last_digit_pos = len(card_str) - next(
        (i for i, c in enumerate(reversed(card_str)) if c.isdigit()), 0
    )

    # Разделяем на префикс, цифры и суффикс
    prefix = card_str[:first_digit_pos]
    suffix = card_str[last_digit_pos:]

    # Формируем маскированную часть
    masked_digits = (
        f"{''.join(digits[:4])} {''.join(digits[4:6])}** **** {''.join(digits[-4:])}"
    )

    return f"{prefix}{masked_digits}{suffix}"


def get_mask_account(account_number: Union[str, int]) -> str:
    """Функция принимает на вход номер счета и возвращает его маску"""
    if account_number is None:
        raise AttributeError("Номер счета не может быть None")

    account_str = str(account_number).strip()

    if not account_str:
        raise ValueError("Номер счета не может быть пустым")

    # Извлекаем только цифры из номера
    digits = [c for c in account_str if c.isdigit()]

    if not digits:
        raise ValueError("Номер счета должен содержать цифры")

    # Берем последние 4 цифры
    last_four = "".join(digits[-4:]) if len(digits) >= 4 else "".join(digits)

    return f"Счет **{last_four}"


# Пример вызова функции для маскирования номера карты
masked_card = get_mask_card_number("1234567812345678")
print(masked_card)

# Пример с префиксом
masked_card_with_prefix = get_mask_card_number("Visa 1234567890123456")
print(masked_card_with_prefix)

# Пример вызова функции для маскирования счета
masked_account = get_mask_account("12345678901234567890")
print(masked_account)

# Пример с префиксом "Счет"
masked_account_with_prefix = get_mask_account("Счет 1234567890123456")
print(masked_account_with_prefix)
