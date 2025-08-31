import os
import sys
from dotenv import load_dotenv

# Добавляем src в путь для импорта
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Загружаем переменные окружения
load_dotenv()

from src.utils import load_transactions
from src.external_api import convert_amount_to_rub


def main():
    """Основная функция приложения"""
    # Загрузка транзакций
    transactions = load_transactions('data/operations.json')

    print(f"Загружено транзакций: {len(transactions)}")

    # Конвертация и вывод сумм
    for i, transaction in enumerate(transactions, 1):
        try:
            amount_rub = convert_amount_to_rub(transaction)
            currency = transaction['operationAmount']['currency']['code']
            print(f"{i}. Сумма: {amount_rub:.2f} RUB (исходно: {transaction['operationAmount']['amount']} {currency})")
        except Exception as e:
            print(f"{i}. Ошибка конвертации: {e}")


if __name__ == "__main__":
    main()