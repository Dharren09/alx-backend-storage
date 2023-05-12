#!/usr/bin/env python3
"""creates a class, init method and a store instance tthat take in a 
data argument and returns a str"""

import redis
from typing import Union, Callable
import uuid
from functools import wraps


class Cache:
    """initializes the Cache class"""

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """stores the given data in Redis and returns the key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
