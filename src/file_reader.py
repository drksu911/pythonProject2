import logging
import os
from typing import Any, Dict, List

import pandas as pd

# Настройка логера для модуля file_reader
logger = logging.getLogger("file_reader")
logger.setLevel(logging.DEBUG)

# Создаем папку logs, если она не существует
os.makedirs("logs", exist_ok=True)

# Создаем file_handler для записи логов в файл с указанием кодировки UTF-8
file_handler = logging.FileHandler("logs/file_reader.log", mode="w", encoding="utf-8")
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


def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из CSV-файла.

    Args:
        file_path (str): Путь к CSV-файлу

    Returns:
        List[Dict[str, Any]]: Список словарей с данными о транзакциях.
        Если файл не найден или произошла ошибка чтения, возвращается пустой список.
    """
    try:
        # Читаем CSV-файл с помощью pandas
        df: pd.DataFrame = pd.read_csv(file_path)

        # Преобразуем DataFrame в список словарей и явно приводим ключи к строковому типу
        transactions_dicts = df.to_dict("records")
        transactions: List[Dict[str, Any]] = [
            {str(k): v for k, v in transaction.items()}
            for transaction in transactions_dicts
        ]

        logger.info(
            "Успешно прочитан CSV-файл %s, количество записей: %d",
            file_path,
            len(transactions),
        )
        return transactions

    except FileNotFoundError:
        logger.error("CSV-файл %s не найден.", file_path)
        return []
    except pd.errors.EmptyDataError:
        logger.error("CSV-файл %s пуст.", file_path)
        return []
    except pd.errors.ParserError:
        logger.error("Ошибка парсинга CSV-файла %s.", file_path)
        return []
    except Exception as e:
        logger.error("Ошибка при чтении CSV-файла %s: %s", file_path, str(e))
        return []


def read_excel_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает финансовые операции из Excel-файла.

    Args:
        file_path (str): Путь к Excel-файлу

    Returns:
        List[Dict[str, Any]]: Список словарей с данными о транзакциях.
        Если файл не найден или произошла ошибка чтения, возвращается пустой список.
    """
    try:
        # Читаем Excel-файл с помощью pandas
        df: pd.DataFrame = pd.read_excel(file_path)

        # Преобразуем DataFrame в список словарей и явно приводим ключи к строковому типу
        transactions_dicts = df.to_dict("records")
        transactions: List[Dict[str, Any]] = [
            {str(k): v for k, v in transaction.items()}
            for transaction in transactions_dicts
        ]

        logger.info(
            "Успешно прочитан Excel-файл %s, количество записей: %d",
            file_path,
            len(transactions),
        )
        return transactions

    except FileNotFoundError:
        logger.error("Excel-файл %s не найден.", file_path)
        return []
    except pd.errors.EmptyDataError:
        logger.error("Excel-файл %s пуст.", file_path)
        return []
    except Exception as e:
        logger.error("Ошибка при чтении Excel-файла %s: %s", file_path, str(e))
        return []
