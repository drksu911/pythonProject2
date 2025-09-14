import functools
from datetime import datetime
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования работы функций.

    Args:
        filename (Optional[str]): Имя файла для записи логов.
                                 Если не указано, логи выводятся в консоль.

    Returns:
        Callable: Декорированная функция
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Формируем информацию о вызове
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            func_name = func.__name__
            inputs = f"Inputs: {args}, {kwargs}"

            try:
                # Вызываем оригинальную функцию
                result = func(*args, **kwargs)

                # Формируем сообщение об успехе
                success_message = f"{timestamp} - {func_name} ok\n"

                # Логируем результат
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(success_message)
                else:
                    print(success_message, end="")

                return result

            except Exception as e:
                # Формируем сообщение об ошибке
                error_message = (
                    f"{timestamp} - {func_name} error: {type(e).__name__}. {inputs}\n"
                )

                # Логируем ошибку
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(error_message)
                else:
                    print(error_message, end="")

                # Пробрасываем исключение дальше
                raise

        return wrapper

    return decorator
