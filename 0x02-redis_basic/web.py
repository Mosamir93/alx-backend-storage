#!/usr/bin/env python3
"""Get_page function module."""
import requests
import redis


def get_page(url: str) -> str:
    """Track how many times a particular URL was accessed in the key
    "count:{url}" and cache the result with an expiration time of 10 seconds.
    """
    count = f"count:{url}"
    r = redis.Redis()
    r.incr(count)

    cached_page = r.get(url)
    if cached_page:
        return cached_page.decode('utf-8')
    response = requests.get(url)
    r.setex(url, 10, response.content)
    return response.content
