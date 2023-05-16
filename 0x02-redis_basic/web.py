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
        # track the number of requests made by the server to load html
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
    in the key cache the result with an expiration of 10 secs"""
    return requests.get(url).text


if __name__ == "__main__":
    url = "http://google.com"

    # Testing the get_page function
    assert r.get("count:{}".format(url)) is None
    get_page(url)
    assert int(r.get("count:{}".format(url)).decode("utf-8")) == 1
    assert r.ttl("cached_html:{}".format(url)) > 0  # HTML content is cached
    time.sleep(10)
    assert r.get("cached_html:{}".format(url)) is None
    assert r.get("count:{}".format(url)) is None
