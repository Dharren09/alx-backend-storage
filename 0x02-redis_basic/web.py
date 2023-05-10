#!/usr/bin/env python3
"""implements a fn which uses requests to obtain an HTML content"""

import requests
import redis
from typing import Callable
from functools import wraps


"""initiates the redis instance"""
redis_store = redis.Redis()


def data_cacher(method: Callable) -> Callable:
    """function that caches the output of fetched data"""
    @wraps(method)
    def invoker(url) -> str:
        redis_store.incr(f'count:{url}')
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return invoker


@data_cacher
def get_page(url: str) -> str:
    """trackss how many times a particular URL was accessed 
    in the key cache the result with an expiration of 10 secs"""
    return requests.get(url).text
