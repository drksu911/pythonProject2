import pytest
from datetime import datetime
from typing import List, Dict, Union
from src.widget import mask_account_card, get_date


# Фикстуры для mask_account_card
@pytest.fixture
def valid_card_data() -> List[Dict[str, str]]:
    return [
        {"input": "Visa Platinum 7000792289606361", "expected": "Visa Platinum 7000 79** **** 6361"},
        {"input": "MasterCard 7158300734726758", "expected": "MasterCard 7158 30** **** 6758"},
        {"input": "МИР 1234567890123456", "expected": "МИР 1234 56** **** 3456"}
    ]


@pytest.fixture
def valid_account_data() -> List[Dict[str, str]]:
    return [
        {"input": "Счет 64686473678894779589", "expected": "Счет **9589"},
        {"input": "Счет 35383033474447895560", "expected": "Счет **5560"}
    ]


@pytest.fixture
def invalid_card_data() -> List[str]:
    return [
        "",
        "   ",
        "Visa 1234",
        "Visa 123456789012345",  # 15 цифр
        "Visa 12345678901234567",  # 17 цифр
        "Visa 12345678901234ab"  # буквы в номере
    ]


@pytest.fixture
def invalid_account_data() -> List[str]:
    return [
        "",
        "   ",
        "Счет 123",
        "Счет abcdefghijklmnop",
        "Счет 1234567890"  # слишком короткий
    ]


# Фикстуры для get_date
@pytest.fixture
def valid_date_data() -> List[Dict[str, str]]:
    return [
        {"input": "2019-07-03T18:35:29.512364", "expected": "03.07.2019"},
        {"input": "2018-06-30T02:08:58.425572", "expected": "30.06.2018"},
        {"input": "2020-01-01", "expected": "01.01.2020"},  # Дата без времени
        {"input": "2021-12-31T23:59:59", "expected": "31.12.2021"}  # Дата с временем без микросекунд
    ]


@pytest.fixture
def invalid_date_data() -> List[str]:
    return [
        "",
        "   ",
        None,
        "2020/01/01",
        "01.01.2020",
        "2020-13-01",  # Неверный месяц
        "2020-01-32",  # Неверный день
        "not a date",
        "01-01-2020",  # Обратный формат
        "2020-01-01T25:00:00"  # Неверное время
    ]


# Тесты для mask_account_card
def test_mask_account_card_valid_cards(valid_card_data: List[Dict[str, str]]) -> None:
    for item in valid_card_data:
        assert mask_account_card(item["input"]) == item["expected"]


def test_mask_account_card_valid_accounts(valid_account_data: List[Dict[str, str]]) -> None:
    for item in valid_account_data:
        assert mask_account_card(item["input"]) == item["expected"]


def test_mask_account_card_invalid_accounts():
    """Тест обработки невалидных номеров счетов"""
    test_cases = [
        # (input, expected_error_message)
        ("", "Пустая строка"),
        ("   ", "Пустая строка"),
        ("Счет", "Не указан номер счета"),
        ("Счет 123", "Номер счета должен содержать минимум 4 цифры"),
        ("Счет abc", "Номер счета должен содержать только цифры"),
        ("Счет 12-34", "Номер счета должен содержать только цифры"),
        ("Счет 1234567890", "**7890")  # 10 цифр - валидный случай
    ]

    for input_str, expected in test_cases:
        if expected.startswith("**"):
            # Проверяем что длинные номера обрабатываются правильно
            assert expected in mask_account_card(input_str)
        else:
            with pytest.raises(ValueError) as exc_info:
                mask_account_card(input_str)
            assert expected in str(exc_info.value)


# Тесты для get_date
def test_get_date_valid(valid_date_data: List[Dict[str, str]]) -> None:
    for item in valid_date_data:
        assert get_date(item["input"]) == item["expected"]


def test_get_date_invalid(invalid_date_data: List[str]) -> None:
    for item in invalid_date_data:
        with pytest.raises((ValueError, AttributeError)):
            get_date(item)


# Дополнительные тесты для граничных случаев
def test_mask_account_card_edge_cases():
    # Карта с пробелами
    assert mask_account_card("  Visa 1234567890123456  ") == "Visa 1234 56** **** 3456"
    # Счет с пробелами
    assert mask_account_card("  Счет 12345678901234567890  ") == "Счет **7890"


def test_get_date_edge_cases():
    # Граничные даты
    assert get_date("0001-01-01") == "01.01.0001"  # Минимальная дата
    assert get_date("9999-12-31") == "31.12.9999"  # Максимальная дата
    assert get_date("2020-02-29") == "29.02.2020"  # Високосный год

    with pytest.raises(ValueError):
        get_date("2020-02-30")  # Несуществующая дата