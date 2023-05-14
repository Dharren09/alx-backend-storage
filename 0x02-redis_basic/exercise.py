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

def call_history(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args):
        input_list_key = f"{method.__qualname__}:inputs"
        output_list_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_list_key, str(args))
        output = method(self, *args)
        self._redis.rpush(output_list_key, str(output))

        return output
    return wrapper

def replay(method: Callable) -> None:
    @wraps(method)
    def wrapper(self, *args):
        redis_instance = redis.Redis()
        input_list_key = f"{method.__qualname__}:inputs"
        output_list_key = f"{method.__qualname__}:outputs"

        input_list = redis_instance.lrange(input_list_key, 0, -1)
        output_list = redis_instance.lrange(output_list_key, 0, -1)
        
        print(f"{method.__qualname__} was called {len(input_list)} times:")

        for inputs, output in zip(input_list, output_list):
            inputs = eval(inputs.decode())
            output = output.decode()

            print(f"{method.__qualname__}{inputs} -> {output}")

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
    @call_history
    @replay
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
