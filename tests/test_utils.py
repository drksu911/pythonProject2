import pytest
import json
import tempfile
import os
from unittest.mock import mock_open, patch
from src.utils import load_transactions


def test_load_transactions_valid_file():
    """Тест загрузки корректного JSON-файла"""
    test_data = [
        {"id": 1, "amount": "100.50"},
        {"id": 2, "amount": "200.75"}
    ]

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_data, f)
        temp_path = f.name

    try:
        result = load_transactions(temp_path)
        assert result == test_data
    finally:
        os.unlink(temp_path)


def test_load_transactions_empty_file():
    """Тест пустого файла"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_path = f.name

    try:
        result = load_transactions(temp_path)
        assert result == []
    finally:
        os.unlink(temp_path)


def test_load_transactions_invalid_json():
    """Тест некорректного JSON"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        f.write("invalid json")
        temp_path = f.name

    try:
        result = load_transactions(temp_path)
        assert result == []
    finally:
        os.unlink(temp_path)


def test_load_transactions_not_list():
    """Тест JSON не списка"""
    test_data = {"id": 1, "amount": "100.50"}

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(test_data, f)
        temp_path = f.name

    try:
        result = load_transactions(temp_path)
        assert result == []
    finally:
        os.unlink(temp_path)


def test_load_transactions_nonexistent_file():
    """Тест несуществующего файла"""
    result = load_transactions("nonexistent.json")
    assert result == []