#!/usr/bin/env python3

"""create a cache class and two methods that stores an instance"""

import redis
from typing import Union, Callable
import uuid


class Cache:
    """generates random key, stores instance of client as private variable
    then flushes the instance"""
    def __init__(self):
        key = str(uuid.uuid4())
        self._redis = redis.Redis()
        self._redis.flushdb()

    """method takes data arg and returns a string, generates a random key
    stores the input data then returns the key"""
    def store(self, data: Union[str, bytes, int, float]) -> str:
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable, default=None):
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is not None:
            value = fn(value)
        return value

    def get_str(self, key: str):
        return self.get(key, lambda x: x.decode('utf-8'))

    def get_int(self, key: str):
        return self.get(key, lambda x: int(x))
