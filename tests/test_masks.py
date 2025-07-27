import pytest
from typing import Union, List, Dict, Tuple
from src.masks import get_mask_card_number, get_mask_account


# Фикстуры для тестов get_mask_card_number
@pytest.fixture
def valid_card_numbers() -> List[Dict[str, Union[str, int]]]:
    return [
        {"input": "1234567812345678", "expected": "1234 56** **** 5678"},
        {"input": 5555555555554444, "expected": "5555 55** **** 4444"},
        {"input": "1234-5678-1234-5678", "expected": "1234 56** **** 5678"},
        {"input": "Visa 1234 5678 9012 3456", "expected": "Visa 1234 56** **** 3456"},
        {"input": "MC#1234-5678-9012-3456", "expected": "MC#1234 56** **** 3456"},
    ]


@pytest.fixture
def edge_case_card_numbers() -> List[Dict[str, Union[str, int]]]:
    return [
        {"input": "12345678901234567890", "expected": "1234 56** **** 7890"},
        {"input": "123456", "expected": "1234 56** **** 3456"},
        {"input": " 1234 5678 9012 3456 ", "expected": "1234 56** **** 3456"},
    ]


@pytest.fixture
def invalid_card_inputs() -> List[Tuple[Union[str, None], type]]:
    return [
        (None, AttributeError),
        ("", ValueError),
        ("   ", ValueError),
        ("123", ValueError),
        ("abc123", ValueError),
        ("12345", ValueError),  # Меньше 6 цифр
    ]


# Фикстуры для тестов get_mask_account
@pytest.fixture
def valid_account_numbers() -> List[Dict[str, Union[str, int]]]:
    return [
        {"input": "12345678901234567890", "expected": "Счет **7890"},
        {"input": 98765432109876543210, "expected": "Счет **3210"},
        {"input": "Счет 12345678", "expected": "Счет **5678"},
        {"input": "Счет 1234-5678-9012-3456", "expected": "Счет **3456"},
    ]


@pytest.fixture
def edge_case_account_numbers() -> List[Dict[str, Union[str, int]]]:
    return [
        {"input": "1234", "expected": "Счет **1234"},
        {"input": "1234567890", "expected": "Счет **7890"},
        {"input": " 12345678901234567890 ", "expected": "Счет **7890"},
    ]


@pytest.fixture
def invalid_account_inputs() -> List[Tuple[Union[str, None], type]]:
    return [
        (None, AttributeError),
        ("", ValueError),
        ("   ", ValueError),
        ("abc", ValueError),
        ("Счет", ValueError),
        ("Счет abc", ValueError),
    ]


# Тесты для get_mask_card_number
def test_get_mask_card_number_valid(valid_card_numbers):
    """Тестирование валидных номеров карт"""
    for case in valid_card_numbers:
        result = get_mask_card_number(case["input"])
        assert result == case["expected"], f"Для входа {case['input']} ожидалось {case['expected']}, получено {result}"


def test_get_mask_card_number_edge_cases(edge_case_card_numbers):
    """Тестирование граничных случаев для номеров карт"""
    for case in edge_case_card_numbers:
        result = get_mask_card_number(case["input"])
        assert result == case["expected"], f"Для входа {case['input']} ожидалось {case['expected']}, получено {result}"


def test_get_mask_card_number_invalid(invalid_card_inputs):
    """Тестирование невалидных входных данных для карт"""
    for input_data, expected_exception in invalid_card_inputs:
        with pytest.raises(expected_exception) as exc_info:
            get_mask_card_number(input_data)
        assert str(exc_info.value), "Сообщение об ошибке не должно быть пустым"


# Тесты для get_mask_account
def test_get_mask_account_valid(valid_account_numbers):
    """Тестирование валидных номеров счетов"""
    for case in valid_account_numbers:
        result = get_mask_account(case["input"])
        assert result == case["expected"], f"Для входа {case['input']} ожидалось {case['expected']}, получено {result}"


def test_get_mask_account_edge_cases(edge_case_account_numbers):
    """Тестирование граничных случаев для номеров счетов"""
    for case in edge_case_account_numbers:
        result = get_mask_account(case["input"])
        assert result == case["expected"], f"Для входа {case['input']} ожидалось {case['expected']}, получено {result}"


def test_get_mask_account_invalid(invalid_account_inputs):
    """Тестирование невалидных входных данных для счетов"""
    for input_data, expected_exception in invalid_account_inputs:
        with pytest.raises(expected_exception) as exc_info:
            get_mask_account(input_data)
        assert str(exc_info.value), "Сообщение об ошибке не должно быть пустым"


# Параметризованные тесты для специальных форматов
@pytest.mark.parametrize("input_card,expected", [
    ("MC#1234-5678-9012-3456", "MC#1234 56** **** 3456"),
    ("Visa 1234 5678 9012 3456", "Visa 1234 56** **** 3456"),
    ("1234.5678.9012.3456", "1234 56** **** 3456"),
    ("1234 5678 9012 3456", "1234 56** **** 3456"),
    (" 1234 5678 9012 3456 ", "1234 56** **** 3456"),
])
def test_get_mask_card_number_special_formats(input_card, expected):
    """Тестирование специальных форматов номеров карт"""
    result = get_mask_card_number(input_card)
    assert result == expected, f"Для входа {input_card} ожидалось {expected}, получено {result}"


@pytest.mark.parametrize("input_account,expected", [
    ("1234 5678 9012 3456 7890", "Счет **7890"),
    ("1234-5678-9012-3456-7890", "Счет **7890"),
    ("1234.5678.9012.3456.7890", "Счет **7890"),
    (" 12345678901234567890 ", "Счет **7890"),
    ("Счет 1234-5678-9012-3456", "Счет **3456"),
])
def test_get_mask_account_special_formats(input_account, expected):
    """Тестирование специальных форматов номеров счетов"""
    result = get_mask_account(input_account)
    assert result == expected, f"Для входа {input_account} ожидалось {expected}, получено {result}"