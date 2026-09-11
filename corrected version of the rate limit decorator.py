import functools
import time
import weakref
from collections import deque
from threading import RLock


def rate_limit(max_calls: int, period: float):
    """
    Decorator that limits the number of times a function can be called
    within a given time period.

    For instance methods, the limit is applied per instance.
    For regular functions, the limit is applied globally.
    """

    if not isinstance(max_calls, int) or isinstance(max_calls, bool):
        raise TypeError("max_calls must be an integer")

    if max_calls <= 0:
        raise ValueError("max_calls must be greater than zero")

    if not isinstance(period, (int, float)) or isinstance(period, bool):
        raise TypeError("period must be a number")

    if period <= 0:
        raise ValueError("period must be greater than zero")

    def decorator(func):
        global_calls = deque()
        instance_calls = weakref.WeakKeyDictionary()
        lock = RLock()

        def bucket_for(args):
            """
            Returns the deque that stores call timestamps.
            Uses a separate bucket for each object instance.
            """
            if args:
                possible_instance = args[0]

                try:
                    weakref.ref(possible_instance)
                except TypeError:
                    pass
                else:
                    return instance_calls.setdefault(
                        possible_instance,
                        deque()
                    )

            return global_calls

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            now = time.monotonic()

            with lock:
                calls = bucket_for(args)

                # Remove expired timestamps
                while calls and now - calls[0] >= period:
                    calls.popleft()

                # Check rate limit
                if len(calls) >= max_calls:
                    raise RuntimeError("Rate limit exceeded")

                calls.append(now)

            return func(*args, **kwargs)

        return wrapper

    return decorator