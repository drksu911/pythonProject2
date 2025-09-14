import pytest
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator


class TestGenerators:
    """Тесты для модуля generators."""

    @pytest.fixture
    def sample_transactions(self):
        """Фикстура с примером транзакций для тестирования."""
        return [
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
            },
            {
                "id": 142264268,
                "state": "EXECUTED",
                "date": "2019-04-04T23:20:05.206878",
                "operationAmount": {
                    "amount": "79114.93",
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Перевод со счета на счет",
                "from": "Счет 19708645243227258542",
                "to": "Счет 75651667383060284188"
            },
            {
                "id": 873106923,
                "state": "EXECUTED",
                "date": "2019-03-23T01:09:46.296404",
                "operationAmount": {
                    "amount": "43318.34",
                    "currency": {
                        "name": "руб.",
                        "code": "RUB"
                    }
                },
                "description": "Перевод со счета на счет",
                "from": "Счет 44812258784861134719",
                "to": "Счет 74489636417521191160"
            },
            {
                "id": 895315941,
                "state": "EXECUTED",
                "date": "2018-08-19T04:27:37.904916",
                "operationAmount": {
                    "amount": "56883.54",
                    "currency": {
                        "name": "USD",
                        "code": "USD"
                    }
                },
                "description": "Перевод с карты на карту",
                "from": "Visa Classic 6831982476737658",
                "to": "Visa Platinum 8990922113665229"
            },
            {
                "id": 594226727,
                "state": "CANCELED",
                "date": "2018-09-12T21:27:25.241689",
                "operationAmount": {
                    "amount": "67314.70",
                    "currency": {
                        "name": "руб.",
                        "code": "RUB"
                    }
                },
                "description": "Перевод организации",
                "from": "Visa Platinum 1246377376343588",
                "to": "Счет 14211924144426031657"
            }
        ]

    def test_filter_by_currency_usd(self, sample_transactions):
        """Тестирование фильтрации транзакций по USD."""
        usd_transactions = list(filter_by_currency(sample_transactions, "USD"))

        # Должно быть 3 транзакции в USD
        assert len(usd_transactions) == 3

        # Проверяем, что все транзакции в USD
        for transaction in usd_transactions:
            assert transaction["operationAmount"]["currency"]["code"] == "USD"

    def test_filter_by_currency_rub(self, sample_transactions):
        """Тестирование фильтрации транзакций по RUB."""
        rub_transactions = list(filter_by_currency(sample_transactions, "RUB"))

        # Должно быть 2 транзакции в RUB
        assert len(rub_transactions) == 2

        # Проверяем, что все транзакции в RUB
        for transaction in rub_transactions:
            assert transaction["operationAmount"]["currency"]["code"] == "RUB"

    def test_filter_by_currency_empty(self):
        """Тестирование фильтрации пустого списка транзакций."""
        empty_transactions = list(filter_by_currency([], "USD"))
        assert len(empty_transactions) == 0

    def test_filter_by_currency_nonexistent(self, sample_transactions):
        """Тестирование фильтрации по несуществующей валюте."""
        eur_transactions = list(filter_by_currency(sample_transactions, "EUR"))
        assert len(eur_transactions) == 0

    def test_transaction_descriptions(self, sample_transactions):
        """Тестирование генератора описаний транзакций."""
        descriptions = list(transaction_descriptions(sample_transactions))

        expected_descriptions = [
            "Перевод организации",
            "Перевод со счета на счет",
            "Перевод со счета на счет",
            "Перевод с карты на карту",
            "Перевод организации"
        ]

        assert descriptions == expected_descriptions

    def test_transaction_descriptions_empty(self):
        """Тестирование генератора описаний для пустого списка."""
        descriptions = list(transaction_descriptions([]))
        assert len(descriptions) == 0

    @pytest.mark.parametrize("start, end, expected_count", [
        (1, 5, 5),
        (10, 15, 6),
        (9999999999999995, 9999999999999999, 5),
        (1, 1, 1),
    ])
    def test_card_number_generator_count(self, start, end, expected_count):
        """Тестирование количества сгенерированных номеров карт."""
        cards = list(card_number_generator(start, end))
        assert len(cards) == expected_count

    @pytest.mark.parametrize("start, end, expected_first, expected_last", [
        (1, 5, "0000 0000 0000 0001", "0000 0000 0000 0005"),
        (9995, 10000, "0000 0000 0000 9995", "0000 0000 0001 0000"),
        (1, 1, "0000 0000 0000 0001", "0000 0000 0000 0001"),
    ])
    def test_card_number_generator_values(self, start, end, expected_first, expected_last):
        """Тестирование значений сгенерированных номеров карт."""
        cards = list(card_number_generator(start, end))
        assert cards[0] == expected_first
        assert cards[-1] == expected_last

    def test_card_number_generator_format(self):
        """Тестирование формата сгенерированных номеров карт."""
        cards = list(card_number_generator(1234567890123456, 1234567890123456))
        assert len(cards) == 1
        assert cards[0] == "1234 5678 9012 3456"

        # Проверяем, что все части состоят из 4 цифр
        parts = cards[0].split()
        assert len(parts) == 4
        for part in parts:
            assert len(part) == 4
            assert part.isdigit()
