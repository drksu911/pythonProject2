import json
import logging
import os
from typing import Any, Dict, List

# Создаем папку logs, если она не существует
os.makedirs("logs", exist_ok=True)

# Настройка логера для модуля utils
logger = logging.getLogger("utils")
logger.setLevel(logging.DEBUG)

# Создаем file_handler для записи логов в файл с указанием кодировки UTF-8
file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")
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


def read_json_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает JSON-файл и возвращает список словарей с данными о финансовых транзакциях.

    Args:
        file_path (str): Путь к JSON-файлу

    Returns:
        List[Dict[str, Any]]: Список словарей с данными о транзакциях.
        Если файл пустой, содержит не список или не найден, возвращается пустой список.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

            if not isinstance(data, list):
                logger.warning(
                    "Файл %s не содержит список. Возвращен пустой список.", file_path
                )
                return []

            logger.info(
                "Успешно прочитан файл %s, количество записей: %d", file_path, len(data)
            )
            return data

    except FileNotFoundError:
        logger.error("Файл %s не найден.", file_path)
        return []
    except json.JSONDecodeError:
        logger.error("Файл %s содержит невалидный JSON.", file_path)
        return []
    except Exception as e:
        logger.error("Ошибка при чтении файла %s: %s", file_path, str(e))
        return []
