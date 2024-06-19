#!/usr/bin/env python3
"""
Web cache and tracker
"""
import requests
import redis
from functools import wraps
from typing import Callable


redis_client = redis.Redis()


def cache_with_expiration(expiration: int):
    """cache with ttl"""
    def decorator(method: Callable) -> Callable:
        """deco"""
        @wraps(method)
        def wrapper(url: str, *args, **kwargs) -> str:
            """wrapper"""
            count_key = f"count:{url}"
            redis_client.incr(count_key)

            cached_content = redis_client.get(url)
            if cached_content:
                return cached_content.decode('utf-8')

            result = method(url, *args, **kwargs)

            redis_client.setex(url, expiration, result)

            return result
        return wrapper
    return decorator


@cache_with_expiration(10)
def get_page(url: str) -> str:
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    domain = "slowwly.robertomurray.co.uk"
    url = f"http://{domain}/delay/5000/url/http://www.example.com"

    for _ in range(3):
        content = get_page(url)
        print(content[:100])

    access_count = redis_client.get(f"count:{url}")
    print(f"Access count for {url}: {access_count.decode('utf-8')}")
