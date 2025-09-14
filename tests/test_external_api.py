import pytest
import os
from unittest.mock import patch, MagicMock
from decimal import Decimal
from requests.exceptions import ConnectionError
from src.external_api import convert_currency_to_rub, get_exchange_rate


class TestExternalApi:
    """Тесты для модуля external_api."""

    @pytest.fixture
    def sample_transaction_rub(self):
        """Фикстура с транзакцией в рублях."""
        return {
            "operationAmount": {
                "amount": "1000.00",
                "currency": {
                    "name": "руб.",
                    "code": "RUB"
                }
            }
        }

    @pytest.fixture
    def sample_transaction_usd(self):
        """Фикстура с транзакцией в USD."""
        return {
            "operationAmount": {
                "amount": "100.00",
                "currency": {
                    "name": "USD",
                    "code": "USD"
                }
            }
        }

    @pytest.fixture
    def sample_transaction_eur(self):
        """Фикстура с транзакцией в EUR."""
        return {
            "operationAmount": {
                "amount": "50.00",
                "currency": {
                    "name": "EUR",
                    "code": "EUR"
                }
            }
        }

    def test_convert_currency_to_rub_rub(self, sample_transaction_rub):
        """Тестирование конвертации рублевой транзакции."""
        result = convert_currency_to_rub(sample_transaction_rub)
        assert result == 1000.00

    @patch('src.external_api.get_exchange_rate')
    @patch('src.external_api.os.getenv')
    def test_convert_currency_to_rub_usd(self, mock_getenv, mock_get_rate, sample_transaction_usd):
        """Тестирование конвертации USD транзакции."""
        # Мокируем получение API ключа и курса валют
        mock_getenv.return_value = "test_api_key"
        mock_get_rate.return_value = 75.50

        result = convert_currency_to_rub(sample_transaction_usd)

        # Проверяем результат конвертации
        expected = 100.00 * 75.50
        assert result == expected

        # Проверяем вызовы функций
        mock_getenv.assert_called_with('EXCHANGE_RATE_API_KEY')
        mock_get_rate.assert_called_with('USD', 'test_api_key')

    @patch('src.external_api.get_exchange_rate')
    @patch('src.external_api.os.getenv')
    def test_convert_currency_to_rub_eur(self, mock_getenv, mock_get_rate, sample_transaction_eur):
        """Тестирование конвертации EUR транзакции."""
        # Мокируем получение API ключа и курса валют
        mock_getenv.return_value = "test_api_key"
        mock_get_rate.return_value = 85.25

        result = convert_currency_to_rub(sample_transaction_eur)

        # Проверяем результат конвертации
        expected = 50.00 * 85.25
        assert result == expected

        # Проверяем вызовы функций
        mock_getenv.assert_called_with('EXCHANGE_RATE_API_KEY')
        mock_get_rate.assert_called_with('EUR', 'test_api_key')

    @patch('src.external_api.os.getenv')
    def test_convert_currency_to_rub_no_api_key(self, mock_getenv, sample_transaction_usd):
        """Тестирование конвертации без API ключа."""
        mock_getenv.return_value = None

        with pytest.raises(ValueError, match="API ключ для конвертации валют не найден"):
            convert_currency_to_rub(sample_transaction_usd)

    @patch('src.external_api.requests.get')
    def test_get_exchange_rate_success(self, mock_get):
        """Тестирование успешного получения курса валют."""
        # Мокируем ответ API
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "rates": {
                "RUB": 75.50
            }
        }
        mock_get.return_value = mock_response

        result = get_exchange_rate('USD', 'test_api_key')

        assert result == 75.50
        mock_get.assert_called_once()

    @patch('src.external_api.requests.get')
    def test_get_exchange_rate_api_error(self, mock_get):
        """Тестирование обработки ошибки API."""
        # Мокируем ответ с ошибкой
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": False,
            "error": {
                "info": "Invalid API key"
            }
        }
        mock_get.return_value = mock_response

        with pytest.raises(ValueError, match="API error: Invalid API key"):
            get_exchange_rate('USD', 'invalid_api_key')

    @patch('src.external_api.requests.get')
    def test_get_exchange_rate_network_error(self, mock_get):
        """Тестирование обработки сетевой ошибки."""
        # Используем ConnectionError из requests.exceptions
        mock_get.side_effect = ConnectionError("Network error")

        with pytest.raises(ValueError, match="Ошибка при запросе к API: Network error"):
            get_exchange_rate('USD', 'test_api_key')

    @patch('src.external_api.requests.get')
    def test_get_exchange_rate_no_rub_rate(self, mock_get):
        """Тестирование обработки отсутствия курса рубля в ответе."""
        # Мокируем ответ API без курса рубля
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "success": True,
            "rates": {
                "USD": 1.0  # Нет курса RUB
            }
        }
        mock_get.return_value = mock_response

        with pytest.raises(ValueError, match="Курс рубля не найден в ответе API"):
            get_exchange_rate('USD', 'test_api_key')