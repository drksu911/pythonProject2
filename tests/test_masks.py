import pytest
from src.masks import get_mask_card_number, get_mask_account


class TestMasks:
    """Тесты для модуля masks."""

    @pytest.mark.parametrize("card_number, expected", [
        (7000792289606361, "7000 79** **** 6361"),
        ("7000792289606361", "7000 79** **** 6361"),
        (1234567812345678, "1234 56** **** 5678"),
        ("0000000000000000", "0000 00** **** 0000"),
    ])
    def test_get_mask_card_number_valid(self, card_number, expected):
        """Тестирование маскировки номера карты с валидными данными."""
        assert get_mask_card_number(card_number) == expected

    @pytest.mark.parametrize("invalid_card_number, expected_error", [
        ("123456789012345", "Номер карты должен содержать 16 цифр"),  # 15 цифр
        ("12345678901234567", "Номер карты должен содержать 16 цифр"),  # 17 цифр
        ("abcdefghijklmnop", "Номер карты должен содержать только цифры"),  # не цифры
        ("", "Номер карты должен содержать 16 цифр"),  # пустая строка
        (0, "Номер карты должен содержать 16 цифр"),  # число 0
    ])
    def test_get_mask_card_number_invalid(self, invalid_card_number, expected_error):
        """Тестирование маскировки номера карты с невалидными данными."""
        with pytest.raises(ValueError) as exc_info:
            get_mask_card_number(invalid_card_number)
        assert str(exc_info.value) == expected_error

    @pytest.mark.parametrize("account_number, expected", [
        (73654108430135874305, "**4305"),
        ("73654108430135874305", "**4305"),
        (1234567890, "**7890"),
        (1234, "**1234"),
    ])
    def test_get_mask_account_valid(self, account_number, expected):
        """Тестирование маскировки номера счета с валидными данными."""
        assert get_mask_account(account_number) == expected

    @pytest.mark.parametrize("invalid_account_number, expected_error", [
        ("123", "Номер счета должен содержать минимум 4 цифры"),  # 3 цифры
        ("", "Номер счета должен содержать минимум 4 цифры"),  # пустая строка
        ("abcdef", "Номер счета должен содержать только цифры"),  # не цифры
    ])
    def test_get_mask_account_invalid(self, invalid_account_number, expected_error):
        """Тестирование маскировки номера счета с невалидными данными."""
        with pytest.raises(ValueError) as exc_info:
            get_mask_account(invalid_account_number)
        assert str(exc_info.value) == expected_error
