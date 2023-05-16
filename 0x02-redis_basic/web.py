#!/usr/bin/env python3
"""implements a fn which uses requests to obtain an HTML content"""

import redis
import requests
from typing import Callable
from functools import wraps


"""initiates the redis instance"""
r = redis.Redis()


def track_count(method: Callable) -> Callable:
    """function that caches the output of fetched data"""
    @wraps(method)
    def invoker(url) -> str:
        """ Wrapper for the decorated function """
        cached_html = r.get("cached_html:{}".format(url))
        if cached_html:
            return cached_html.decode('utf-8')
        # track nombre of request made by the server to load html
        r.incr("count:{}".format(url))

        # make a new request
        html = method(url)
        # make  a new copy on the chache with 10 sec of expiration
        r.setex("cached_html:{}".format(url), 10, html)

        return html

    return invoker


@track_count
def get_page(url: str) -> str:
    """trackss how many times a particular URL was accessed
    in the key cache the result with an expiration of 10 secs"""
    return requests.get(url).text
