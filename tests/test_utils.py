import pytest
import json
from unittest.mock import mock_open, patch
from src.utils import read_json_file


class TestUtils:
    """Тесты для модуля utils."""

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
            }
        ]

    def test_read_json_file_success(self, sample_transactions, tmp_path):
        """Тестирование успешного чтения JSON-файла."""
        # Создаем временный файл
        file_path = tmp_path / "test_operations.json"
        file_path.write_text(json.dumps(sample_transactions), encoding='utf-8')

        # Читаем файл
        result = read_json_file(str(file_path))

        # Проверяем результат
        assert result == sample_transactions

    def test_read_json_file_empty(self, tmp_path):
        """Тестирование чтения пустого файла."""
        file_path = tmp_path / "empty.json"
        file_path.write_text("", encoding='utf-8')

        result = read_json_file(str(file_path))
        assert result == []

    def test_read_json_file_invalid_json(self, tmp_path):
        """Тестирование чтения файла с невалидным JSON."""
        file_path = tmp_path / "invalid.json"
        file_path.write_text("{invalid json}", encoding='utf-8')

        result = read_json_file(str(file_path))
        assert result == []

    def test_read_json_file_not_list(self, tmp_path):
        """Тестирование чтения файла, который не содержит список."""
        file_path = tmp_path / "not_list.json"
        file_path.write_text('{"key": "value"}', encoding='utf-8')

        result = read_json_file(str(file_path))
        assert result == []

    def test_read_json_file_not_found(self):
        """Тестирование чтения несуществующего файла."""
        result = read_json_file("nonexistent.json")
        assert result == []
