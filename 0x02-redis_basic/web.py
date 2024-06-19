#!/usr/bin/env python3
"""
Web request caching and tracking module
"""
import redis
import requests
from functools import wraps
from typing import Callable


cache_client = redis.Redis()


def track_and_cache(expiration: int = 10):
    """Decorator to track URL access and cache the response with expiration."""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(url: str, *args, **kwargs) -> str:
            access_count_key = f"access_count:{url}"
            cache_client.incr(access_count_key)

            cached_content = cache_client.get(f"cached_response:{url}")
            if cached_content:
                return cached_content.decode('utf-8')

            response_content = func(url, *args, **kwargs)
            cache_client.setex(f"cached_response:{url}",
                               expiration, response_content)

            return response_content
        return wrapper
    return decorator


@track_and_cache()
def fetch_url_content(url: str) -> str:
    """Fetch the HTML content of the specified URL."""
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    test_url = (
        "http://slowwly.robertomurray.co.uk/delay/5000/url/"
        "http://www.example.com"
    )

    for _ in range(3):
        content = fetch_url_content(test_url)
        print(content[:100])  # Print the first 100 characters of the content

    access_count = cache_client.get(f"access_count:{test_url}")
    print(f"Access count for {test_url}: {access_count.decode('utf-8')}")
