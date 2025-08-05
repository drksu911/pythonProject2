import pytest
from src.decorators import log


@log()
def add(x, y):
    return x + y


@log()
def divide(x, y):
    return x / y


@log(filename="test.log")
def multiply(x, y):
    return x * y


@log(filename="test.log")
def get_item(items, index):
    return items[index]


def test_add_success(capsys):
    """
    Тест успешного выполнения функции add с логированием в консоль.
    """
    result = add(5, 3)

    assert result == 8

    captured = capsys.readouterr()
    assert "INFO: Function 'add' started." in captured.out
    assert "INFO: Function 'add' finished successfully" in captured.out
    assert "Result: 8" in captured.out


def test_divide_error(capsys):
    """
    Тест выполнения функции divide с ошибкой ZeroDivisionError и логированием в консоль.
    """
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()
    assert "INFO: Function 'divide' started." in captured.out
    assert "ERROR: Function 'divide' failed." in captured.out
    assert "Error type: ZeroDivisionError" in captured.out
    assert "Arguments: args=(10, 0), kwargs={}" in captured.out


def test_multiply_to_file(tmp_path):
    """
    Тест успешного выполнения функции multiply с логированием в файл.
    Используется фикстура tmp_path для создания временного файла.
    """
    log_file = tmp_path / "test.log"

    @log(filename=log_file)
    def multiply_temp(x, y):
        return x * y

    result = multiply_temp(4, 5)

    assert result == 20

    with open(log_file, "r") as f:
        log_content = f.read()

    assert "INFO: Function 'multiply_temp' started." in log_content
    assert "INFO: Function 'multiply_temp' finished successfully" in log_content
    assert "Result: 20" in log_content


def test_get_item_error_to_file(tmp_path):
    """
    Тест выполнения функции get_item с ошибкой IndexError и логированием в файл.
    """
    log_file = tmp_path / "test_error.log"

    @log(filename=log_file)
    def get_item_temp(items, index):
        return items[index]

    with pytest.raises(IndexError):
        get_item_temp([1, 2, 3], 5)

    with open(log_file, "r") as f:
        log_content = f.read()

    assert "INFO: Function 'get_item_temp' started." in log_content
    assert "ERROR: Function 'get_item_temp' failed." in log_content
    assert "Error type: IndexError" in log_content
    assert "Arguments: args=([1, 2, 3], 5), kwargs={}" in log_content