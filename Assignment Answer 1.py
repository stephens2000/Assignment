import time
from functools import wraps


def rate_limit(max_calls: int, period: int):
    """
    Decorator that limits the number of function calls
    within a specified time period.

    Args:
        max_calls (int): Maximum number of allowed calls.
        period (int): Time window in seconds.
    """
    def decorator(func):
        calls = []

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal calls

            now = time.time()

            # Keep only timestamps within the allowed period
            calls = [t for t in calls if now - t < period]

            if len(calls) >= max_calls:
                raise Exception(
                    f"Rate limit exceeded. Maximum {max_calls} calls "
                    f"allowed within {period} seconds."
                )

            calls.append(now)
            return func(*args, **kwargs)

        return wrapper

    return decorator


@rate_limit(max_calls=3, period=10)
def fetch_user_data(user_id):
    return f"Data for {user_id}"


# Example usage
try:
    print(fetch_user_data(101))
    print(fetch_user_data(102))
    print(fetch_user_data(103))
    print(fetch_user_data(104))  # Raises exception
except Exception as e:
    print(e)