#!/usr/bin/env python3
"""
Web request caching and tracking module
"""
import redis
import requests
from functools import wraps
from typing import Callable


cache_client = redis.Redis()


def cache_page(method: Callable) -> Callable:
    """deco cache"""
    @wraps(method)
    def wrapper(url) -> str:
        """wrapper"""
        count_key = f"count:{url}"
        cache_client.incr(count_key)
        cached_content = cache_client.get(f"result:{url}")
        if cached_content:
            return cached_content.decode("utf-8")
        response_content = method(url)
        cache_client.set(f"count:{url}", 0)
        cache_client.setex(f"result:{url}", 10, response_content)

        return response_content
    return wrapper


@cache_page
def get_page(url: str) -> str:
    """Fetch the HTML content of the specified URL."""
    response = requests.get(url)
    return response.text
