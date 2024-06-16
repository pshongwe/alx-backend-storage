#!/usr/bin/env python3
from pymongo import MongoClient
"""log_stats """


def log_stats():
    """Provides some stats about Nginx logs stored in MongoDB"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    collection = client.logs.nginx

    total_logs = collection.count_documents({})
    get_logs = len(list(collection.find({'method': 'GET'})))
    post_logs = len(list(collection.find({'method': 'POST'})))
    put_logs = len(list(collection.find({'method': 'PUT'})))
    patch_logs = len(list(collection.find({'method': 'PATCH'})))
    delete_logs = len(list(collection.find({'method': 'DELETE'})))
    status_check = len(list(collection.find(
                                              {'method': 'GET',
                                               'path': '/status'})))

    print(f"{total_logs} logs")
    print("Methods:")
    print(f"    method GET: {get_logs}")
    print(f"    method POST: {post_logs}")
    print(f"    method PUT: {put_logs}")
    print(f"    method PATCH: {patch_logs}")
    print(f"    method DELETE: {delete_logs}")
    print(f"{status_check} status check")


if __name__ == "__main__":
    log_stats()
