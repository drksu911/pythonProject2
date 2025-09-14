from src.utils import read_json_file
from src.file_reader import read_csv_file, read_excel_file
from src.processing import filter_by_state, sort_by_date
from src.external_api import convert_currency_to_rub
from src.operations import process_bank_search, process_bank_operations
from src.masks import get_mask_card_number, get_mask_account
from src.widget import mask_account_card, get_date
import logging
import os

# Настройка логирования только для файла
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/main.log", mode="w", encoding="utf-8")
    ]
)

logger = logging.getLogger("main")


def display_transaction(transaction: dict) -> None:
    """
    Отображает информацию о транзакции в удобочитаемом формате.

    Args:
        transaction (dict): Словарь с данными о транзакции
    """
    try:
        # Форматируем дату
        date_str = get_date(transaction['date']) if 'date' in transaction else "Дата неизвестна"

        # Форматируем описание
        description = transaction.get('description', 'Описание отсутствует')

        # Форматируем отправителя и получателя
        from_account = ""
        if 'from' in transaction:
            from_account = mask_account_card(transaction['from']) + " -> "

        to_account = mask_account_card(transaction['to']) if 'to' in transaction else "Неизвестный счет"

        # Конвертируем сумму в рубли
        amount_rub = convert_currency_to_rub(transaction)

        print(f"{date_str} {description}")
        print(f"{from_account}{to_account}")
        print(f"Сумма: {amount_rub:.2f} руб.\n")
    except Exception as e:
        logger.error(f"Ошибка при отображении транзакции: {e}")


def get_user_choice(prompt: str, valid_choices: list) -> str:
    """
    Получает выбор пользователя с валидацией.

    Args:
        prompt (str): Подсказка для пользователя
        valid_choices (list): Список допустимых вариантов ответа

    Returns:
        str: Выбор пользователя
    """
    while True:
        choice = input(prompt).strip().lower()
        if choice in valid_choices:
            return choice
        print(f"Неверный выбор. Пожалуйста, выберите один из: {', '.join(valid_choices)}")


def main():
    """Основная функция программы."""
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")

    # Выбор источника данных
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    file_choice = get_user_choice("Ваш выбор: ", ["1", "2", "3"])

    # Загрузка данных
    transactions = []
    if file_choice == "1":
        transactions = read_json_file("data/operations.json")
        print("Для обработки выбран JSON-файл.")
    elif file_choice == "2":
        transactions = read_csv_file("data/transactions.csv")
        print("Для обработки выбран CSV-файл.")
    else:
        transactions = read_excel_file("data/transactions_excel.xlsx")
        print("Для обработки выбран XLSX-файл.")

    if not transactions:
        print("Не удалось загрузить транзакции или файл пуст.")
        return

    # Фильтрация по статусу
    valid_states = ["executed", "canceled", "pending"]
    while True:
        state_input = input("Введите статус, по которому необходимо выполнить фильтрацию. "
                            "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING: ").strip().lower()

        if state_input in valid_states:
            filtered_transactions = filter_by_state(transactions, state_input.upper())
            print(f"Операции отфильтрованы по статусу \"{state_input.upper()}\"")
            break
        else:
            print(f"Статус операции \"{state_input}\" недоступен.")

    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    # Сортировка по дате
    sort_choice = get_user_choice("Отсортировать операции по дате? (да/нет): ", ["да", "нет"])
    if sort_choice == "да":
        order_choice = get_user_choice("Отсортировать по возрастанию или по убыванию? (по возрастанию/по убыванию): ",
                                       ["по возрастанию", "по убыванию"])
        reverse = order_choice == "по убыванию"
        filtered_transactions = sort_by_date(filtered_transactions, reverse)

    # Фильтрация по валюте
    currency_choice = get_user_choice("Выводить только рублевые транзакции? (да/нет): ", ["да", "нет"])
    if currency_choice == "да":
        filtered_transactions = [t for t in filtered_transactions
                                 if t.get('operationAmount', {}).get('currency', {}).get('code') == 'RUB']

    # Поиск по описанию
    search_choice = get_user_choice("Отфильтровать список транзакций по определенному слову в описании? (да/нет): ",
                                    ["да", "нет"])
    if search_choice == "да":
        search_word = input("Введите слово для поиска в описании: ").strip()
        if search_word:
            filtered_transactions = process_bank_search(filtered_transactions, search_word)

    # Вывод результатов
    if not filtered_transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print("Распечатываю итоговый список транзакций...")
    print(f"Всего банковских операций в выборке: {len(filtered_transactions)}\n")

    for transaction in filtered_transactions:
        display_transaction(transaction)

    # Дополнительная статистика
    stats_choice = get_user_choice("Показать статистику по категориям операций? (да/нет): ", ["да", "нет"])
    if stats_choice == "да":
        categories = ["перевод", "оплата", "покупка", "снятие", "вклад"]
        stats = process_bank_operations(filtered_transactions, categories)
        print("\nСтатистика по категориям операций:")
        for category, count in stats.items():
            print(f"{category.capitalize()}: {count} операций")


if __name__ == "__main__":
    main()