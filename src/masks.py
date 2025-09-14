import logging
import os
from typing import Union

# Создаем папку logs, если она не существует
os.makedirs("logs", exist_ok=True)

# Настройка логера для модуля masks
logger = logging.getLogger("masks")
logger.setLevel(logging.DEBUG)

# Создаем file_handler для записи логов в файл с указанием кодировки UTF-8
file_handler = logging.FileHandler("logs/masks.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Создаем formatter для определения формата записей логов
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
file_handler.setFormatter(file_formatter)

# Добавляем handler к логеру
logger.addHandler(file_handler)

# Отключаем распространение логов в корневой логер
logger.propagate = False


def get_mask_card_number(card_number: Union[int, str]) -> str:
    """
    Маскирует номер банковской карты в формате XXXX XX** **** XXXX.

    Args:
        card_number (int | str): Номер карты как целое число или строка.

    Returns:
        str: Замаскированный номер карты.

    Raises:
        ValueError: Если номер карты не содержит 16 цифр или содержит недопустимые символы.
    """
    str_number = str(card_number).replace(" ", "")

    # Проверяем, что строка не пустая
    if not str_number:
        logger.error("Получена пустая строка для маскирования карты")
        raise ValueError("Номер карты должен содержать 16 цифр")

    # Проверяем, что строка состоит только из цифр
    if not str_number.isdigit():
        logger.error("Номер карты содержит недопустимые символы: %s", str_number)
        raise ValueError("Номер карты должен содержать только цифры")

    # Проверяем длину номера карты
    if len(str_number) != 16:
        logger.error(
            "Номер карты имеет неправильную длину: %d вместо 16", len(str_number)
        )
        raise ValueError("Номер карты должен содержать 16 цифр")

    logger.info("Успешно замаскирован номер карты: %s", str_number)
    return f"{str_number[:4]} {str_number[4:6]}** **** {str_number[-4:]}"


def get_mask_account(account_number: Union[int, str]) -> str:
    """
    Маскирует номер счета в формате **XXXX.

    Args:
        account_number (int | str): Номер счета как целое число или строка.

    Returns:
        str: Замаскированный номер счета.

    Raises:
        ValueError: Если номер счета содержит менее 4 цифр или содержит недопустимые символы.
    """
    str_number = str(account_number).replace(" ", "")

    # Проверяем, что строка не пустая
    if not str_number:
        logger.error("Получена пустая строка для маскирования счета")
        raise ValueError("Номер счета должен содержать минимум 4 цифры")

    # Проверяем, что строка состоит только из цифр
    if not str_number.isdigit():
        logger.error("Номер счета содержит недопустимые символы: %s", str_number)
        raise ValueError("Номер счета должен содержать только цифры")

    # Проверяем длину номера счета
    if len(str_number) < 4:
        logger.error(
            "Номер счета имеет неправильную длину: %d вместо минимум 4", len(str_number)
        )
        raise ValueError("Номер счета должен содержать минимум 4 цифры")

    logger.info("Успешно замаскирован номер счета: %s", str_number)
    return f"**{str_number[-4:]}"
