import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.file_reader import read_csv_file, read_excel_file


class TestFileReader:
    """Тесты для модуля file_reader."""

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

    @patch('src.file_reader.pd.read_csv')
    def test_read_csv_file_success(self, mock_read_csv, sample_transactions):
        """Тестирование успешного чтения CSV-файла."""
        # Мокируем DataFrame
        mock_df = MagicMock()
        mock_df.to_dict.return_value = sample_transactions
        mock_read_csv.return_value = mock_df

        result = read_csv_file("test.csv")

        # Проверяем результат
        assert result == sample_transactions
        mock_read_csv.assert_called_once_with("test.csv")

    @patch('src.file_reader.pd.read_csv')
    def test_read_csv_file_not_found(self, mock_read_csv):
        """Тестирование чтения несуществующего CSV-файла."""
        mock_read_csv.side_effect = FileNotFoundError("File not found")

        result = read_csv_file("nonexistent.csv")

        assert result == []

    @patch('src.file_reader.pd.read_csv')
    def test_read_csv_file_empty(self, mock_read_csv):
        """Тестирование чтения пустого CSV-файла."""
        mock_read_csv.side_effect = pd.errors.EmptyDataError("No columns to parse")

        result = read_csv_file("empty.csv")

        assert result == []

    @patch('src.file_reader.pd.read_csv')
    def test_read_csv_file_parse_error(self, mock_read_csv):
        """Тестирование чтения CSV-файла с ошибкой парсинга."""
        mock_read_csv.side_effect = pd.errors.ParserError("Error parsing file")

        result = read_csv_file("invalid.csv")

        assert result == []

    @patch('src.file_reader.pd.read_excel')
    def test_read_excel_file_success(self, mock_read_excel, sample_transactions):
        """Тестирование успешного чтения Excel-файла."""
        # Мокируем DataFrame
        mock_df = MagicMock()
        mock_df.to_dict.return_value = sample_transactions
        mock_read_excel.return_value = mock_df

        result = read_excel_file("test.xlsx")

        # Проверяем результат
        assert result == sample_transactions
        mock_read_excel.assert_called_once_with("test.xlsx")

    @patch('src.file_reader.pd.read_excel')
    def test_read_excel_file_not_found(self, mock_read_excel):
        """Тестирование чтения несуществующего Excel-файла."""
        mock_read_excel.side_effect = FileNotFoundError("File not found")

        result = read_excel_file("nonexistent.xlsx")

        assert result == []

    @patch('src.file_reader.pd.read_excel')
    def test_read_excel_file_empty(self, mock_read_excel):
        """Тестирование чтения пустого Excel-файла."""
        mock_read_excel.side_effect = pd.errors.EmptyDataError("No columns to parse")

        result = read_excel_file("empty.xlsx")

        assert result == []

    @patch('src.file_reader.pd.read_excel')
    def test_read_excel_file_general_error(self, mock_read_excel):
        """Тестирование чтения Excel-файла с общей ошибкой."""
        mock_read_excel.side_effect = Exception("General error")

        result = read_excel_file("error.xlsx")

        assert result == []