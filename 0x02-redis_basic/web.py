#!/usr/bin/env python3
"""
Web request caching and tracking module
"""
import redis
import requests
from functools import wraps
from typing import Callable


redis_store = redis.Redis()
"""module-level Redis client.
"""


def cache_page(method: Callable) -> Callable:
    """deco cache"""
    @wraps(method)
    def wrapper(url) -> str:
        """wrapper"""
        count_key = f'count:{url}'
        redis_store.incr(count_key)
        result = redis_store.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_store.set(f'count:{url}', 0)
        redis_store.setex(f'result:{url}', 10, result)
        return result
    return wrapper


@cache_page
def get_page(url: str) -> str:
    """Fetch the HTML content of the specified URL."""
    return requests.get(url).text


if __name__ == "__main__":
    test_url = (
        "http://slowwly.robertomurray.co.uk/delay/5000/url/"
        "http://www.example.com"
    )

    # Fetch the page multiple times to test caching and tracking
    for _ in range(3):
        content = get_page(test_url)
        print(content[:100])  # Print the first 100 characters of the content

    # Print the access count for the URL
    access_count = redis_store.get(f"count:{test_url}")
    if access_count is not None:
        print(f"Access count for {test_url}: {access_count.decode('utf-8')}")
    else:
        print(f"Access count for {test_url}: 0")

