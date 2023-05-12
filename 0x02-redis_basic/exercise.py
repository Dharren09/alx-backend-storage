#!/usr/bin/env python3
"""creates a class, init method and a store instance tthat take in a
data argument and returns a str"""

import redis
from typing import Union
import uuid


class Cache:
    """
    initializes the Cache class
    generates random key, stores instance of client as private variable
    then flushes the instance
    """

    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb

    """
    method takes data arg and returns a string, generates a random key
    stores the input data then returns the key
    """

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """stores the given data in Redis and returns the key"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
