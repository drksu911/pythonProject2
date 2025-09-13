import os
from typing import List, Dict, Any
import pandas as pd


def read_csv_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает финансовые операции из CSV-файла с использованием pandas.

    Args:
        file_path (str): Путь к CSV-файлу

    Returns:
        List[Dict[str, Any]]: Список словарей с транзакциями

    Raises:
        FileNotFoundError: Если файл не найден
        Exception: При других ошибках чтения файла
    """
    # Проверяем существование файла
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден")

    try:
        # Читаем CSV с помощью pandas
        df = pd.read_csv(file_path)

        # Заменяем NaN значения на None для совместимости с JSON
        df = df.where(pd.notnull(df), None)

        # Конвертируем DataFrame в список словарей
        transactions = df.to_dict('records')

        return transactions

    except Exception as e:
        raise Exception(f"Ошибка при чтении CSV: {str(e)}")


def read_excel_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Читает финансовые операции из XLSX-файла с использованием pandas.

    Args:
        file_path (str): Путь к XLSX-файлу

    Returns:
        List[Dict[str, Any]]: Список словарей с транзакциями

    Raises:
        FileNotFoundError: Если файл не найден
        Exception: При других ошибках чтения файла
    """
    # Проверяем существование файла
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл {file_path} не найден")

    try:
        # Читаем Excel с помощью pandas
        df = pd.read_excel(file_path)

        # Заменяем NaN значения на None для совместимости с JSON
        df = df.where(pd.notnull(df), None)

        # Конвертируем DataFrame в список словарей
        transactions = df.to_dict('records')

        return transactions

    except Exception as e:
        raise Exception(f"Ошибка при чтении Excel: {str(e)}")


# Функция для демонстрации работы модуля (необязательная)
def demonstrate_file_reading():
    """Демонстрирует работу функций чтения файлов"""
    try:
        # Формируем пути к файлам
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, 'data')

        csv_path = os.path.join(data_dir, 'transactions.csv')
        excel_path = os.path.join(data_dir, 'transactions.xlsx')

        # Проверяем существование файлов
        csv_exists = os.path.exists(csv_path)
        excel_exists = os.path.exists(excel_path)

        if csv_exists:
            # Чтение CSV
            csv_transactions = read_csv_transactions(csv_path)
            print(f"Прочитано {len(csv_transactions)} транзакций из CSV")

            # Вывод первых нескольких транзакций для демонстрации
            if csv_transactions:
                print("Первые 3 транзакции из CSV:")
                for i, transaction in enumerate(csv_transactions[:3]):
                    print(f"{i + 1}. {transaction}")

        if excel_exists:
            # Чтение Excel
            excel_transactions = read_excel_transactions(excel_path)
            print(f"Прочитано {len(excel_transactions)} транзакций из Excel")

            # Вывод первых нескольких транзакций для демонстрации
            if excel_transactions:
                print("Первые 3 транзакции из Excel:")
                for i, transaction in enumerate(excel_transactions[:3]):
                    print(f"{i + 1}. {transaction}")

        if not csv_exists and not excel_exists:
            print("Файлы transactions.csv и transactions.xlsx не найдены в папке data/")

    except Exception as e:
        print(f"Ошибка при чтении файлов: {e}")


if __name__ == "__main__":
    # Код выполняется только при прямом запуске file_reader.py
    demonstrate_file_reading()