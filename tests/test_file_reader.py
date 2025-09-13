import unittest
from unittest.mock import patch, MagicMock
from file_reader import read_csv_transactions, read_excel_transactions
import pandas as pd
import os


class TestFileReader(unittest.TestCase):

    @patch('pandas.read_csv')
    @patch('os.path.exists', return_value=True)
    def test_read_csv_transactions_success(self, mock_exists, mock_read_csv):
        """Тест успешного чтения CSV файла с использованием pandas"""
        # Создаем mock DataFrame с реальными данными
        test_data = [
            {'id': 650703, 'state': 'EXECUTED', 'amount': 16210},
            {'id': 650704, 'state': 'PENDING', 'amount': 5000}
        ]
        mock_df = pd.DataFrame(test_data)
        mock_read_csv.return_value = mock_df

        # Вызываем тестируемую функцию
        result = read_csv_transactions('test.csv')

        # Проверяем результаты
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['id'], 650703)
        self.assertEqual(result[0]['state'], 'EXECUTED')
        self.assertEqual(result[1]['amount'], 5000)

        # Проверяем, что функции были вызваны с правильными параметрами
        mock_exists.assert_called_once_with('test.csv')
        mock_read_csv.assert_called_once_with('test.csv')

    @patch('pandas.read_excel')
    @patch('os.path.exists', return_value=True)
    def test_read_excel_transactions_success(self, mock_exists, mock_read_excel):
        """Тест успешного чтения Excel файла с использованием pandas"""
        # Создаем mock DataFrame с реальными данными
        test_data = [
            {'id': 650705, 'state': 'EXECUTED', 'amount': 7500},
            {'id': 650706, 'state': 'CANCELED', 'amount': 3000}
        ]
        mock_df = pd.DataFrame(test_data)
        mock_read_excel.return_value = mock_df

        # Вызываем тестируемую функцию
        result = read_excel_transactions('test.xlsx')

        # Проверяем результаты
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['id'], 650705)
        self.assertEqual(result[0]['state'], 'EXECUTED')
        self.assertEqual(result[1]['amount'], 3000)

        # Проверяем, что функции были вызваны с правильными параметрами
        mock_exists.assert_called_once_with('test.xlsx')
        mock_read_excel.assert_called_once_with('test.xlsx')

    @patch('os.path.exists', return_value=False)
    def test_read_csv_transactions_file_not_found(self, mock_exists):
        """Тест обработки отсутствующего CSV файла"""
        with self.assertRaises(FileNotFoundError):
            read_csv_transactions('nonexistent.csv')

        mock_exists.assert_called_once_with('nonexistent.csv')

    @patch('os.path.exists', return_value=False)
    def test_read_excel_transactions_file_not_found(self, mock_exists):
        """Тест обработки отсутствующего Excel файла"""
        with self.assertRaises(FileNotFoundError):
            read_excel_transactions('nonexistent.xlsx')

        mock_exists.assert_called_once_with('nonexistent.xlsx')


if __name__ == '__main__':
    unittest.main()