import pytest
from src.generators import filter_by_currency, transaction_descriptions, card_number_generator

@pytest.fixture
def real_transactions():
    return [
        {
            "id": 939719570,
            "operationAmount": {
                "currency": {"code": "USD"},
            },
            "description": "Перевод организации"
        },
        {
            "id": 142264268,
            "operationAmount": {
                "currency": {"code": "USD"},
            },
            "description": "Перевод со счета на счет"
        },
        {
            "id": 873106923,
            "operationAmount": {
                "currency": {"code": "RUB"},
            },
            "description": "Перевод со счета на счет"
        },
        {
            "id": 895315941,
            "operationAmount": {
                "currency": {"code": "USD"},
            },
            "description": "Перевод с карты на карту"
        },
        {
            "id": 594226727,
            "operationAmount": {
                "currency": {"code": "RUB"},
            },
            "description": "Перевод организации"
        }
    ]

def test_filter_usd_currency(real_transactions):
    usd_transactions = filter_by_currency(real_transactions, "USD")
    results = list(usd_transactions)
    assert len(results) == 3
    assert results[0]["id"] == 939719570
    assert results[1]["id"] == 142264268
    assert results[2]["id"] == 895315941

def test_filter_rub_currency(real_transactions):
    rub_transactions = filter_by_currency(real_transactions, "RUB")
    results = list(rub_transactions)
    assert len(results) == 2
    assert results[0]["id"] == 873106923
    assert results[1]["id"] == 594226727

def test_filter_eur_currency(real_transactions):
    eur_transactions = filter_by_currency(real_transactions, "EUR")
    assert len(list(eur_transactions)) == 0


def test_transaction_descriptions_real_data(real_transactions):
    gen = transaction_descriptions(real_transactions)
    results = list(gen)
    assert results == [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации"
    ]

def test_transaction_descriptions_empty_input():
    assert list(transaction_descriptions([])) == []

@pytest.mark.parametrize("index, expected", [
    (0, "Перевод организации"),
    (1, "Перевод со счета на счет"),
    (3, "Перевод с карты на карту")
])
def test_transaction_descriptions_specific_items(real_transactions, index, expected):
    gen = transaction_descriptions(real_transactions)
    for _ in range(index):
        next(gen)
    assert next(gen) == expected


@pytest.mark.parametrize("start, end, expected", [
    (1, 1, ["0000 0000 0000 0001"]),
    (1, 3, [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003"
    ]),
    (9999, 10001, [
        "0000 0000 0000 9999",
        "0000 0000 0001 0000",
        "0000 0000 0001 0001"
    ]),
])
def test_card_number_generator(start, end, expected):
    assert list(card_number_generator(start, end)) == expected