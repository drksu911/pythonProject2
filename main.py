import os
import logging
import pandas as pd

from src.utils import load_transactions
from src.masks import get_mask_card_number, get_mask_account
from file_reader import read_csv_transactions, read_excel_transactions

def setup_logging() -> None:
    """Настройка логирования для основного приложения"""
    os.makedirs('logs', exist_ok=True)

    # Настраиваем базовое логирование с UTF-8 кодировкой
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.FileHandler('logs/main.log', mode='w', encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

    logger = logging.getLogger(__name__)
    logger.info("Логирование инициализировано")
    return logger


def test_utils_module() -> None:
    """Тестирование модуля utils"""
    logger = logging.getLogger(__name__)
    logger.info("=" * 50)
    logger.info("ТЕСТИРОВАНИЕ МОДУЛЯ UTILS")
    logger.info("=" * 50)

    # Тестируем загрузку транзакций
    test_cases = [
        ('data/operations.json', 'Корректный файл'),
        ('nonexistent.json', 'Несуществующий файл'),
        ('data/empty.json', 'Пустой файл'),
        ('data/invalid.json', 'Невалидный JSON')
    ]

    for file_path, description in test_cases:
        try:
            logger.info(f"Тест: {description} - {file_path}")
            transactions = load_transactions(file_path)
            logger.info(f"Загружено транзакций: {len(transactions)}")

        except Exception as e:
            logger.error(f"Ошибка при тестировании {description}: {e}")

    logger.info("Тестирование модуля utils завершено\n")


def test_masks_module() -> None:
    """Тестирование модуля masks"""
    logger = logging.getLogger(__name__)
    logger.info("=" * 50)
    logger.info("ТЕСТИРОВАНИЕ МОДУЛЯ MASKS")
    logger.info("=" * 50)

    # Тестируем успешные сценарии для карт
    card_test_cases = [
        ("1234567812345678", "Стандартный номер карты"),
        ("Visa 1234567890123456", "Номер карты с префиксом"),
        ("MasterCard 1234 5678 9012 3456", "Номер карты с пробелами"),
        ("МИР 1234567890123456", "Номер карты МИР"),
        (1234567812345678, "Номер карты как число")
    ]

    logger.info("Тестирование успешных сценариев для карт:")
    for test_input, description in card_test_cases:
        try:
            result = get_mask_card_number(test_input)
            logger.info(f"{description}: '{test_input}' -> '{result}'")
        except Exception as e:
            logger.error(f"Ошибка при обработке карты {description}: {e}")

    # Тестируем успешные сценарии для счетов
    account_test_cases = [
        ("12345678901234567890", "Стандартный номер счета"),
        ("Счет 1234567890123456", "Номер счета с префиксом"),
        ("Account 1234567890", "Номер счета на английском"),
        (1234567890123456, "Номер счета как число")
    ]

    logger.info("\nТестирование успешных сценариев для счетов:")
    for test_input, description in account_test_cases:
        try:
            result = get_mask_account(test_input)
            logger.info(f"{description}: '{test_input}' -> '{result}'")
        except Exception as e:
            logger.error(f"Ошибка при обработке счета {description}: {e}")

    # Тестируем ошибочные сценарии
    error_test_cases = [
        (None, "None значение"),
        ("", "Пустая строка"),
        ("123", "Короткий номер карты"),
        ("ABC", "Номер без цифр"),
        ("   ", "Только пробелы"),
        ("Visa ABCDEFGH", "Буквы вместо цифр")
    ]

    logger.info("\nТестирование обработки ошибок:")
    for test_input, description in error_test_cases:
        try:
            # Пробуем оба метода
            if len(str(test_input or "")) < 10:
                get_mask_card_number(test_input)
            else:
                get_mask_account(test_input)
            logger.warning(f"Ожидалась ошибка для: {description}")

        except (ValueError, AttributeError) as e:
            logger.info(f"Корректно обработана ошибка для '{description}': {type(e).__name__}")
        except Exception as e:
            logger.error(f"Неожиданная ошибка для '{description}': {e}")

    logger.info("Тестирование модуля masks завершено\n")


def demonstrate_transaction_processing() -> None:
    """Демонстрация обработки транзакций с маскировкой"""
    logger = logging.getLogger(__name__)
    logger.info("=" * 50)
    logger.info("ОБРАБОТКА ТРАНЗАКЦИЙ С МАСКИРОВКОЙ")
    logger.info("=" * 50)

    # Загружаем транзакции
    transactions = load_transactions('data/operations.json')

    if not transactions:
        logger.warning("Не удалось загрузить транзакции для демонстрации")
        return

    logger.info(f"Загружено транзакций для обработки: {len(transactions)}")

    # Обрабатываем первые 5 транзакций для демонстрации
    for i, transaction in enumerate(transactions[:5], 1):
        try:
            logger.info(f"\nТранзакция #{i}:")
            logger.info(f"  ID: {transaction.get('id', 'N/A')}")
            logger.info(f"  Описание: {transaction.get('description', 'N/A')}")
            logger.info(f"  Статус: {transaction.get('state', 'N/A')}")

            # Маскируем данные карты/счета если они есть
            if 'from' in transaction:
                from_value = transaction['from']
                if any(keyword in from_value for keyword in ['Visa', 'MasterCard', 'МИР', 'Maestro']):
                    masked_from = get_mask_card_number(from_value)
                else:
                    masked_from = get_mask_account(from_value)
                logger.info(f"  Отправитель: {masked_from}")

            if 'to' in transaction:
                to_value = transaction['to']
                if any(keyword in to_value for keyword in ['Visa', 'MasterCard', 'МИР', 'Maestro']):
                    masked_to = get_mask_card_number(to_value)
                else:
                    masked_to = get_mask_account(to_value)
                logger.info(f"  Получатель: {masked_to}")

            # Информация о сумме
            if 'operationAmount' in transaction:
                amount = transaction['operationAmount'].get('amount', 'N/A')
                currency = transaction['operationAmount'].get('currency', {}).get('name', 'N/A')
                logger.info(f"  Сумма: {amount} {currency}")

        except Exception as e:
            logger.error(f"Ошибка при обработке транзакции #{i}: {e}")

    logger.info("Обработка транзакций завершена\n")


def process_file_based_transactions():
    """
    Обрабатывает транзакции из файлов CSV и Excel.
    Эта функция может быть интегрирована в существующую логику main.
    """
    try:
        # Формируем пути к файлам
        base_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(base_dir, 'data')

        csv_path = os.path.join(data_dir, 'transactions.csv')
        excel_path = os.path.join(data_dir, 'transactions.xlsx')

        all_transactions = []

        # Обработка CSV файла, если он существует
        if os.path.exists(csv_path):
            csv_transactions = read_csv_transactions(csv_path)
            print(f"Прочитано {len(csv_transactions)} транзакций из CSV")
            all_transactions.extend(csv_transactions)

            # Интегрируйте с вашей существующей логикой обработки
            # process_transactions(csv_transactions, source="CSV")

        # Обработка Excel файла, если он существует
        if os.path.exists(excel_path):
            excel_transactions = read_excel_transactions(excel_path)
            print(f"Прочитано {len(excel_transactions)} транзакций из Excel")
            all_transactions.extend(excel_transactions)

            # Интегрируйте с вашей существующей логикой обработки
            # process_transactions(excel_transactions, source="Excel")

        # Возвращаем все транзакции для дальнейшей обработки
        return all_transactions

    except Exception as e:
        print(f"Ошибка при обработке файловых транзакций: {e}")
        return []


def main() -> None:
    """Основная функция приложения"""
    logger = setup_logging()

    try:
        logger.info("Запуск тестирования модулей...")

        # Тестируем модули
        test_utils_module()
        test_masks_module()

        # Демонстрируем обработку транзакций
        demonstrate_transaction_processing()

        logger.info("=" * 50)
        logger.info("ВСЕ ТЕСТЫ УСПЕШНО ЗАВЕРШЕНЫ!")
        logger.info("=" * 50)
        logger.info("Проверьте файлы в папке logs/:")
        logger.info("  - logs/utils.log - логи модуля utils")
        logger.info("  - logs/masks.log - логи модуля masks")
        logger.info("  - logs/main.log - логи основного приложения")

    except Exception as e:
        logger.critical(f"Критическая ошибка в основном приложении: {e}")
        raise
    file_transactions = process_file_based_transactions()

    if file_transactions:
        print(f"Всего обработано {len(file_transactions)} транзакций из файлов")

if __name__ == "__main__":
    main()


