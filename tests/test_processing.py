import pytest
from src.processing import filter_by_state, sort_by_date


class TestProcessing:
    """Тесты для модуля processing."""

    def test_filter_by_state_default(self, sample_operations):
        """Тестирование фильтрации по состоянию со значением по умолчанию."""
        result = filter_by_state(sample_operations)
        assert len(result) == 2
        assert all(op["state"] == "EXECUTED" for op in result)

    @pytest.mark.parametrize("state, expected_count", [
        ("EXECUTED", 2),
        ("CANCELED", 2),
        ("PENDING", 1),
        ("NONEXISTENT", 0),
    ])
    def test_filter_by_state_parametrized(self, sample_operations, state, expected_count):
        """Параметризованное тестирование фильтрации по разным состояниям."""
        result = filter_by_state(sample_operations, state)
        assert len(result) == expected_count
        if expected_count > 0:
            assert all(op["state"] == state for op in result)

    def test_sort_by_date_descending(self, sample_operations):
        """Тестирование сортировки по убыванию даты (по умолчанию)."""
        result = sort_by_date(sample_operations)
        dates = [op["date"] for op in result]
        assert dates == sorted(dates, reverse=True)

    def test_sort_by_date_ascending(self, sample_operations):
        """Тестирование сортировки по возрастанию даты."""
        result = sort_by_date(sample_operations, False)
        dates = [op["date"] for op in result]
        assert dates == sorted(dates)

    def test_sort_by_date_empty(self):
        """Тестирование сортировки пустого списка."""
        result = sort_by_date([])
        assert result == []

    def test_filter_by_state_empty(self):
        """Тестирование фильтрации пустого списка."""
        result = filter_by_state([])
        assert result == []
