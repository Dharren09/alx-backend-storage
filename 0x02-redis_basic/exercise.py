#!/usr/bin/env python3
"""
A class that represents a cache with method decorators and a replay function.
"""

import redis
from typing import Union, Callable, Optional
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """
    Decorator that counts the number of times a method is called.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wrapper function that increments the
        method call count and calls the method.
        """
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator that stores the input and output history of a method.
    """
    @wraps(method)
    def wrapper(self, *args):
        """
        Wrapper function that stores the input
        and output history and calls the method.
        """
        key = method.__qualname__
        input_list_key = f"{key}:inputs"
        output_list_key = f"{key}:outputs"

        self._redis.rpush(input_list_key, str(args))
        output = method(self, *args)
        self._redis.rpush(output_list_key, str(output))

        return output

    return wrapper


def replay(instance: object):
    """
    Displays the history of calls for all methods in the instance.
    """
    redis_client = redis.Redis()
    methods = [m for m in dir(instance) if callable(getattr(instance, m))]
    for method_name in methods:
        if method_name.startswith("__"):
            continue
        inputs = redis_client.lrange(f"{method_name}:inputs", 0, -1)
        outputs = redis_client.lrange(f"{method_name}:outputs", 0, -1)
        count = redis_client.get(method_name).decode("utf-8")
        print(f"{method_name} was called {count} times:")
        for i, j in zip(inputs, outputs):
            print(f"{method_name}(*{i.decode('utf-8')}) ->
                    {j.decode('utf-8')}")


class Cache:
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores the given data in Redis and returns the key."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key, fn: Optional[callable] = None):
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is None:
            return value
        return fn(value)

    def get_str(self, key):
        """Returns the string representation of the stored value."""
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key):
        """Returns the integer representation of the stored value."""
        return self.get(key, int)


if __name__ == "__main__":
    cache = Cache()

    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8"),
        "egg": str,
        "eggsperiment": len,
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value

    replay(cache)
