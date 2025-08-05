import datetime
import functools


def log(filename=None):
    """
    Декоратор для логирования выполнения функции.

    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            log_message = ""
            start_time = datetime.datetime.now()

            try:
                log_message += (
                    f"[{start_time}] INFO: Function '{func.__name__}' started."
                )
                if filename:
                    with open(filename, "a") as f:
                        f.write(log_message + "\n")
                else:
                    print(log_message)
                result = func(*args, **kwargs)

                end_time = datetime.datetime.now()
                execution_time = end_time - start_time
                log_message = (
                    f"[{end_time}] INFO: Function '{func.__name__}' finished successfully in {execution_time}. "
                    f"Result: {result}"
                )
                if filename:
                    with open(filename, "a") as f:
                        f.write(log_message + "\n")
                else:
                    print(log_message)
                return result

            except Exception as e:
                end_time = datetime.datetime.now()
                log_message = (
                    f"[{end_time}] ERROR: Function '{func.__name__}' failed. "
                    f"Error type: {type(e).__name__}. "
                    f"Arguments: args={args}, kwargs={kwargs}"
                )
                if filename:
                    with open(filename, "a") as f:
                        f.write(log_message + "\n")
                else:
                    print(log_message)
                raise

        return wrapper

    return decorator


@log(filename="mylog.txt")
def my_function(x, y):
    return x + y


my_function(1, 2)
