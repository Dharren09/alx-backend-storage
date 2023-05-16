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
        # track number of requests made by the server to load html
        r.incr("count:{}".format(url), amount=1)

        # make a new request
        html = method(url)
        # make a new copy in the cache with 10 sec of expiration
        r.setex("cached_html:{}".format(url), 10, html)

        return html

    return invoker


@track_count
def get_page(url: str) -> str:
    """tracks how many times a particular URL was accessed
    and caches the result with an expiration of 10 secs"""
    return requests.get(url).text


if __name__ == "__main__":
    # Test the get_page function
    url = "http://google.com"
    assert get_page(url) == get_page(urli)
    assert r.ttl("cached_html:{}".format(url)) >= 1
    assert r.get("count:{}".format(url)) == b"1"
