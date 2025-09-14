import pytest
from src.widget import mask_account_card, get_date


class TestWidget:
    """Тесты для модуля widget."""

    @pytest.mark.parametrize("account_info, expected", [
        ("Visa Platinum 7000792289606361", "Visa Platinum 7000 79** **** 6361"),
        ("Maestro 7000792289606361", "Maestro 7000 79** **** 6361"),
        ("Счет 73654108430135874305", "Счет **4305"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
    ])
    def test_mask_account_card_valid(self, account_info, expected):
        """Тестирование маскировки карты/счета с валидными данными."""
        assert mask_account_card(account_info) == expected

    @pytest.mark.parametrize("invalid_account_info, expected_error", [
        ("Visa Platinum", "Строка должна содержать тип и номер карты/счета"),
        ("Счет", "Строка должна содержать тип и номер карты/счета"),
        ("", "Строка с информацией об аккаунте не может быть пустой"),
        ("   ", "Строка с информацией об аккаунте не может быть пустой"),
        ("Invalid Type abc123", "Строка должна содержать тип и номер карты/счета"),
        ("Visa Platinum 123456789012345", "Номер карты должен содержать 16 цифр"),  # 15 цифр
        ("Visa Platinum 12345678901234567", "Номер карты должен содержать 16 цифр"),  # 17 цифр
    ])
    def test_mask_account_card_invalid(self, invalid_account_info, expected_error):
        """Тестирование маскировки карты/счета с невалидными данными."""
        with pytest.raises(ValueError) as exc_info:
            mask_account_card(invalid_account_info)
        assert str(exc_info.value) == expected_error

    @pytest.mark.parametrize("date_string, expected", [
        ("2024-03-11T02:26:18.671407", "11.03.2024"),
        ("2019-07-03T18:35:29.512364", "03.07.2019"),
        ("2018-06-30T02:08:58.425572", "30.06.2018"),
        ("2020-01-01T00:00:00.000000", "01.01.2020"),
    ])
    def test_get_date_valid(self, date_string, expected):
        """Тестирование преобразования даты с валидными данными."""
        assert get_date(date_string) == expected

    @pytest.mark.parametrize("invalid_date_string, expected_error", [
        ("2024-03-11", "Дата должна быть в формате ISO с разделителем 'T'"),
        ("11.03.2024", "Дата должна быть в формате ISO с разделителем 'T'"),
        ("invalid-date", "Дата должна быть в формате ISO с разделителем 'T'"),
        ("", "Дата должна быть в формате ISO с разделителем 'T'"),
        ("   ", "Дата должна быть в формате ISO с разделителем 'T'"),
        ("2024-03-11T", "Некорректный формат даты"),
        ("T02:26:18.671407", "Некорректный формат даты"),
        ("2024-03-11T02:26:18.671407Textra", "Некорректный формат даты"),
    ])
    def test_get_date_invalid(self, invalid_date_string, expected_error):
        """Тестирование преобразования даты с невалидными данными."""
        with pytest.raises(ValueError) as exc_info:
            get_date(invalid_date_string)
        assert str(exc_info.value) == expected_error
