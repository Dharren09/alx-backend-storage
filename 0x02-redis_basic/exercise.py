#!/usr/bin/env python3
"""creates a class, init method and a store instance tthat take in a
data argument and returns a str"""

import redis
from typing import Union, Callable
import uuid
from functools import wraps

def count_calls(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """get qualified name of the method"""
        key = method.__qualname__
        """get increment of the count"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


class Cache:
    def __init__(self):
        """
        initilaizes a redis database
        creates a private variable then flushes out
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """stores the given data in Redis and returns the key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key, fn=None):
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is None:
            return value
        return fn(value)

    def get_str(self, key):
        """return str rep."""
        return self.get(key, lambda d: d.decode("utf-8"))

    def get_int(self, key):
        """ return integers"""
        return self.get(key, int)


if __name__ == "__main__":
    cache = Cache()

    TEST_CASES = {
        b"foo": None,
        123: int,
        "bar": lambda d: d.decode("utf-8")
    }

    for value, fn in TEST_CASES.items():
        key = cache.store(value)
        assert cache.get(key, fn=fn) == value
