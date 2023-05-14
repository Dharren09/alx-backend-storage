#!/usr/bin/env python3
"""creates a class, init method and a store instance tthat take in a
data argument and returns a str"""

import redis
from typing import Union, Callable, Optional
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
        key = method.__qualname__
        input_list_key = f"{key}:inputs"
        output_list_key = f"{key}:outputs"

        self._redis.rpush(input_list_key, str(args))
        output = method(self, *args)
        self._redis.rpush(output_list_key, str(output))

        return output
    return wrapper

def replay(method: Callable) -> None:
    """Display the history of calls of a particular function"""
    if not callable(method):
        raise TypeError("fn must be callable")

    r = redis.Redis()
    f_name = method.__qualname__
    n_calls = r.get(f_name)
    try:
        n_calls = int(n_calls)
    except Exception:
        n_calls = 0
    print(f'{f_name} was called {n_calls} times:')

    ins = r.lrange(f_name + ":inputs", 0, -1)
    outs = r.lrange(f_name + ":outputs", 0, -1)

    for i, o in zip(ins, outs):
        try:
            i = i.decode('utf-8')
        except Exception:
            i = ""
        try:
            o = o.decode('utf-8')
        except Exception:
            o = ""

        print(f'{f_name}(*{i}) -> {o}')


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

    def get(self, key, fn: Optional[callable] = None):
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
        """ return integers from redis database"""
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
