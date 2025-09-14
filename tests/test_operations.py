import pytest
from src.operations import process_bank_search, process_bank_operations


class TestOperations:
    """Тесты для модуля operations."""

    @pytest.fixture
    def sample_transactions(self):
        """Фикстура с примером транзакций."""
        return [
            {
                "id": 441945886,
                "state": "EXECUTED",
                "date": "2019-08-26T10:50:58.294041",
                "operationAmount": {
                    "amount": "31957.58",
                    "currency": {
                        "name": "руб.",
                        "code": "RUB"
                    }
                },
                "description": "Перевод организации",
                "from": "Maestro 1596837868705199",
                "to": "Счет 64686473678894779589"
            },
            {
                "id": 41428829,
                "state": "EXECUTED",
                "date": "2019-07-03T18:35:29.512364",
                "operationAmount": {
                    "amount": "8221.37",
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Перевод со счета на счет",
                "from": "MasterCard 7158300734726758",
                "to": "Счет 35383033474447895560"
            },
            {
                "id": 939719570,
                "state": "EXECUTED",
                "date": "2018-06-30T02:08:58.425572",
                "operationAmount": {
                    "amount": "9824.07",
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Перевод организации",
                "from": "Счет 75106830613657916952",
                "to": "Счет 11776614605963066702"
            }
        ]

    def test_process_bank_search_found(self, sample_transactions):
        """Тестирование поиска транзакций по описанию (найдены)."""
        result = process_bank_search(sample_transactions, "перевод")
        assert len(result) == 3

        result = process_bank_search(sample_transactions, "организации")
        assert len(result) == 2

    def test_process_bank_search_not_found(self, sample_transactions):
        """Тестирование поиска транзакций по описанию (не найдены)."""
        result = process_bank_search(sample_transactions, "покупка")
        assert len(result) == 0

    def test_process_bank_search_case_insensitive(self, sample_transactions):
        """Тестирование регистронезависимого поиска."""
        result = process_bank_search(sample_transactions, "ПЕРЕВОД")
        assert len(result) == 3

    def test_process_bank_search_invalid_regex(self, sample_transactions):
        """Тестирование обработки невалидного регулярного выражения."""
        result = process_bank_search(sample_transactions, "[")
        assert len(result) == 0

    def test_process_bank_operations(self, sample_transactions):
        """Тестирование подсчета операций по категориям."""
        categories = ["перевод", "оплата", "покупка"]
        result = process_bank_operations(sample_transactions, categories)

        assert "перевод" in result
        assert result["перевод"] == 3
        assert "оплата" not in result

    def test_process_bank_operations_case_insensitive(self, sample_transactions):
        """Тестирование регистронезависимого подсчета."""
        categories = ["ПЕРЕВОД", "ОПЛАТА"]
        result = process_bank_operations(sample_transactions, categories)

        assert "перевод" in result
        assert result["перевод"] == 3

    def test_process_bank_operations_empty_categories(self, sample_transactions):
        """Тестирование подсчета с пустым списком категорий."""
        result = process_bank_operations(sample_transactions, [])
        assert result == {}

    def test_process_bank_operations_no_matches(self, sample_transactions):
        """Тестирование подсчета без совпадений."""
        result = process_bank_operations(sample_transactions, ["покупка"])
        assert result == {}
