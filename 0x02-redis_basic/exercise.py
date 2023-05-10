#!/usr/bin/env python3

"""create a cache class and two methods that stores an instance"""

import redis
from typing import Union, Callable
import uuid
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """func that increments the count for the key nd returns it"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator that stores the history of outputs and inputs"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key_inputs = method.__qualname__ + ":inputs"
        key_outputs = method.__qualname__ + ":outputs"

        self._redis.rpush(key_inputs, str(args))
        """executes the wrapped fn to get the output"""
        output = method(self, *args, **kwargs)

        self._redis.rpush(key_outputs, str(output))
        return output
    return wrapper


def replay(method):
    """fn displays the history of calls of a particular function"""
    inputs_key = method.__qualname__ + ":inputs"
    outputs_key = method.__qualname__ + ":outputs"

    inputs = [i.decode('utf-8') for i in conn.lrange(inputs_key, 0, -1)]
    outputs = [o.decode('utf-8') for o in conn.lrange(outputs_key, 0, -1)]

    calls = [f"{method.__qualname__}{str(args)} -> {output.decode()}"
             for args, output in zip(inputs, outputs)]

    return f"{method.__qualname__} was called {len(calls)}
    times: \n" + "\n".join(calls)


class Cache:
    """generates random key, stores instance of client as private variable
    then flushes the instance"""

    def __init__(self):
        key = str(uuid.uuid4())
        self._redis = redis.Redis()
        self._redis.flushdb()

    """method takes data arg and returns a string, generates a random key
    stores the input data then returns the key"""
    @ count_calls
    @ call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(
        self,
        key: str,
        fn: Callable = None,
        default=None
    ) -> Union[str, bytes, int, float, None]:
        value = self._redis.get(key)
        if value is None:
            return default
        if fn is not None:
            value = fn(value)
        return value

    def get_str(self, key: str):
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str):
        return self.get(key, lambda x: int(x))
