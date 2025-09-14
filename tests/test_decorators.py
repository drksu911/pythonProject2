import os
import pytest
from src.decorators import log


class TestDecorators:
    """Тесты для модуля decorators."""

    def test_log_to_console_success(self, capsys):
        """Тестирование логирования успешного выполнения в консоль."""

        @log()
        def test_func(x, y):
            return x + y

        result = test_func(2, 3)

        # Проверяем результат выполнения
        assert result == 5

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        assert "test_func ok" in captured.out
        assert "error" not in captured.out

    def test_log_to_console_error(self, capsys):
        """Тестирование логирования ошибки в консоль."""

        @log()
        def test_func():
            raise ValueError("Test error")

        # Проверяем, что исключение пробрасывается
        with pytest.raises(ValueError):
            test_func()

        # Проверяем вывод в консоль
        captured = capsys.readouterr()
        assert "test_func error: ValueError" in captured.out
        assert "Inputs: (), {}" in captured.out

    def test_log_to_file_success(self, tmp_path):
        """Тестирование логирования успешного выполнения в файл."""
        log_file = tmp_path / "test_log.txt"

        @log(filename=str(log_file))
        def test_func(x, y):
            return x * y

        result = test_func(4, 5)

        # Проверяем результат выполнения
        assert result == 20

        # Проверяем запись в файл
        assert log_file.exists()
        content = log_file.read_text(encoding="utf-8")
        assert "test_func ok" in content
        assert "error" not in content

    def test_log_to_file_error(self, tmp_path):
        """Тестирование логирования ошибки в файл."""
        log_file = tmp_path / "test_log.txt"

        @log(filename=str(log_file))
        def test_func(a, b=10):
            raise RuntimeError("Custom error")

        # Проверяем, что исключение пробрасывается
        with pytest.raises(RuntimeError):
            test_func(1, b=2)

        # Проверяем запись в файл
        assert log_file.exists()
        content = log_file.read_text(encoding="utf-8")
        assert "test_func error: RuntimeError" in content
        assert "Inputs: (1,), {'b': 2}" in content

    def test_log_preserves_function_metadata(self):
        """Тестирование сохранения метаданных функции."""

        @log()
        def test_func(x: int, y: int) -> int:
            """Test function for decorator"""
            return x + y

        # Проверяем сохранение метаданных
        assert test_func.__name__ == "test_func"
        assert test_func.__doc__ == "Test function for decorator"  # Убрана точка в ожидаемом значении
        assert test_func.__annotations__ == {"x": int, "y": int, "return": int}

    def test_log_multiple_calls(self, tmp_path):
        """Тестирование множественных вызовов с записью в файл."""
        log_file = tmp_path / "multi_log.txt"

        @log(filename=str(log_file))
        def test_func(x):
            return x ** 2

        # Вызываем функцию несколько раз
        results = [test_func(i) for i in range(3)]

        # Проверяем результаты
        assert results == [0, 1, 4]

        # Проверяем записи в файле
        content = log_file.read_text(encoding="utf-8")
        lines = content.strip().split("\n")
        assert len(lines) == 3
        assert all("test_func ok" in line for line in lines)

    def test_log_with_different_arguments(self, capsys):
        """Тестирование с различными типами аргументов."""

        @log()
        def test_func(a, b=10, *args, **kwargs):
            return f"{a}-{b}-{args}-{kwargs}"

        result = test_func(1, 2, 3, 4, key="value")

        # Проверяем результат
        assert "1-2-(3, 4)-{'key': 'value'}" in result

        # Проверяем, что в логе нет ошибок
        captured = capsys.readouterr()
        assert "test_func ok" in captured.out
        assert "error" not in captured.out
