#!/usr/bin/env python3
"""Provides stats about Nginx logs stored in MongoDB."""
from pymongo import MongoClient


def get_nginx_stats(collection):
    """Prints statistics about Nginx logs."""
    total_logs = collection.count_documents({})
    print(f"{total_logs} logs")
    print("Methods:")
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        method_count = len(list(collection.find({'method': method})))
        print(f"\tmethod {method}: {method_count}")

    get_status = {'method': 'GET', 'path': '/status'}
    status_check_count = len(list(collection.find(get_status)))
    print(f"{status_check_count} status check")


if __name__ == '__main__':
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx
    get_nginx_stats(collection)
