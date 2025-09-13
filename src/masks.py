import logging
from typing import Union

# Создаем и настраиваем логер для модуля masks
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

# Создаем file handler с указанием кодировки UTF-8
file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Создаем форматтер
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def get_mask_card_number(card_number: Union[str, int]) -> str:
    """
    Функция принимает на вход номер карты и возвращает ее маску.

    Args:
        card_number: Номер карты в виде строки или числа

    Returns:
        str: Замаскированный номер карты

    Raises:
        AttributeError: Если номер карты None
        ValueError: Если номер карты пустой или содержит меньше 6 цифр
    """
    try:
        logger.debug(f"Начало маскировки номера карты: {card_number}")

        if card_number is None:
            error_msg = "Номер карты не может быть None"
            logger.error(error_msg)
            raise AttributeError(error_msg)

        card_str = str(card_number).strip()

        if not card_str:
            error_msg = "Номер карты не может быть пустым"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Извлекаем только цифры
        digits = [c for c in card_str if c.isdigit()]

        if len(digits) < 6:
            error_msg = "Номер карты должен содержать минимум 6 цифр"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Находим начало и конец цифровой части
        first_digit_pos = next((i for i, c in enumerate(card_str) if c.isdigit()), 0)
        last_digit_pos = len(card_str) - next(
            (i for i, c in enumerate(reversed(card_str)) if c.isdigit()), 0
        )

        # Разделяем на префикс, цифры и суффикс
        prefix = card_str[:first_digit_pos]
        suffix = card_str[last_digit_pos:]

        # Формируем маскированную часть
        masked_digits = f"{''.join(digits[:4])} {''.join(digits[4:6])}** **** {''.join(digits[-4:])}"

        result = f"{prefix}{masked_digits}{suffix}"
        logger.info(f"Успешно замаскирован номер карты: {result}")

        return result

    except (AttributeError, ValueError):
        # Эти ошибки уже залогированы выше, просто пробрасываем дальше
        raise
    except Exception as e:
        error_msg = f"Неожиданная ошибка при маскировке номера карты {card_number}: {e}"
        logger.critical(error_msg)
        raise RuntimeError(error_msg) from e


def get_mask_account(account_number: Union[str, int]) -> str:
    """
    Функция принимает на вход номер счета и возвращает его маску.

    Args:
        account_number: Номер счета в виде строки или числа

    Returns:
        str: Замаскированный номер счета

    Raises:
        AttributeError: Если номер счета None
        ValueError: Если номер счета пустой или не содержит цифр
    """
    try:
        logger.debug(f"Начало маскировки номера счета: {account_number}")

        if account_number is None:
            error_msg = "Номер счета не может быть None"
            logger.error(error_msg)
            raise AttributeError(error_msg)

        account_str = str(account_number).strip()

        if not account_str:
            error_msg = "Номер счета не может быть пустым"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Извлекаем только цифры из номера
        digits = [c for c in account_str if c.isdigit()]

        if not digits:
            error_msg = "Номер счета должен содержать цифры"
            logger.error(error_msg)
            raise ValueError(error_msg)

        # Берем последние 4 цифры
        last_four = "".join(digits[-4:]) if len(digits) >= 4 else "".join(digits)

        result = f"Счет **{last_four}"
        logger.info(f"Успешно замаскирован номер счета: {result}")

        return result

    except (AttributeError, ValueError):
        # Эти ошибки уже залогированы выше, просто пробрасываем дальше
        raise
    except Exception as e:
        error_msg = (
            f"Неожиданная ошибка при маскировке номера счета {account_number}: {e}"
        )
        logger.critical(error_msg)
        raise RuntimeError(error_msg) from e


# Примеры использования с логированием
if __name__ == "__main__":
    try:
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

        # Примеры с ошибками (для тестирования логирования)
        try:
            get_mask_card_number("")  # Пустая строка
        except ValueError:
            pass

        try:
            get_mask_card_number("123")  # Слишком короткий номер
        except ValueError:
            pass

    except Exception as e:
        logger.error(f"Ошибка в основном блоке: {e}")
