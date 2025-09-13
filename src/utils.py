import json
import logging
import os
from typing import Any, Dict, List

# Создаем и настраиваем логер для модуля utils
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

# Создаем file handler с указанием кодировки UTF-8
file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)

# Создаем форматтер
file_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
)

file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает транзакции из JSON-файла.

    Args:
        file_path: Путь к JSON-файлу с транзакциями

    Returns:
        List[Dict[str, Any]]: Список словарей с данными транзакций
    """
    try:
        logger.debug(f"Начало загрузки транзакций из файла: {file_path}")

        if not os.path.exists(file_path):
            logger.warning(f"Файл не найден: {file_path}")
            return []

        if os.path.getsize(file_path) == 0:
            logger.warning(f"Файл пустой: {file_path}")
            return []

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            logger.warning(f"Файл не содержит список: {file_path}")
            return []

        logger.info(f"Успешно загружено {len(data)} транзакций из файла: {file_path}")
        return data

    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}: {e}")
        return []
    except PermissionError as e:
        logger.error(f"Ошибка доступа к файлу {file_path}: {e}")
        return []
    except OSError as e:
        logger.error(f"Системная ошибка при работе с файлом {file_path}: {e}")
        return []
    except Exception as e:
        logger.critical(f"Неожиданная ошибка при загрузке транзакций: {e}")
        return []
