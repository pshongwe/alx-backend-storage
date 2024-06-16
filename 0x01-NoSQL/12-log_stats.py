#!/usr/bin/env python3
"""Provides stats about Nginx logs stored in MongoDB."""
from pymongo import MongoClient


def get_nginx_stats():
    """Prints statistics about Nginx logs."""
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")
    print("Methods:")
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        method_count = collection.count_documents({'method': method})
        print(f"    method {method}: {method_count}")
    status_check_count = collection.count_documents({'method': 'GET', 'path': '/status'})
    print(f"{status_check_count} status check")


if __name__ == '__main__':
    get_nginx_stats()
