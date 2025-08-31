import pytest
from unittest.mock import patch, MagicMock
from src.external_api import convert_amount_to_rub, convert_currency


def test_convert_amount_to_rub_rub():
    """Тест конвертации RUB в RUB"""
    transaction = {
        'operationAmount': {
            'amount': '100.50',
            'currency': {'code': 'RUB'}
        }
    }

    result = convert_amount_to_rub(transaction)
    assert result == 100.50


def test_convert_amount_to_rub_usd():
    """Тест конвертации USD в RUB"""
    transaction = {
        'operationAmount': {
            'amount': '100.00',
            'currency': {'code': 'USD'}
        }
    }

    with patch('src.external_api.convert_currency') as mock_convert:
        mock_convert.return_value = 7500.0
        result = convert_amount_to_rub(transaction)
        assert result == 7500.0
        mock_convert.assert_called_once_with(100.0, 'USD')


def test_convert_amount_to_rub_invalid():
    """Тест невалидной транзакции"""
    transaction = {'invalid': 'data'}
    result = convert_amount_to_rub(transaction)
    assert result == 0.0


@patch('src.external_api.requests.get')
@patch('src.external_api.os.getenv')
def test_convert_currency_success(mock_getenv, mock_get):
    """Тест успешной конвертации валюты"""
    mock_getenv.side_effect = lambda key: {
        'API_KEY': 'test_key',
        'API_URL': 'https://test.com'
    }[key]

    mock_response = MagicMock()
    mock_response.json.return_value = {'rates': {'RUB': 75.0}}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = convert_currency(100.0, 'USD')
    assert result == 7500.0


@patch('src.external_api.os.getenv')
def test_convert_currency_no_api_key(mock_getenv):
    """Тест отсутствия API ключа"""
    mock_getenv.return_value = None

    with pytest.raises(ValueError):
        convert_currency(100.0, 'USD')