#!/usr/bin/env python3

"""create a cache class and two methods that stores an instance"""

import redis
from typing import Union
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
