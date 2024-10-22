#!/usr/bin/env python3
"""
Python script that provides
some stats about Nginx logs stored in MongoDB
"""


from pymongo import MongoClient


if __name__ == "__main__":
    """
    Provides some stats about Nginx logs
    """
    client = MongoClient()
    db = client.logs
    collection = db.nginx

    logs = collection.count_documents({})
    print(f"{logs} logs")
    print("Methods:")

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        count = collection.count_documents({"method": method})
        print(f"\tmethod {method}: {count}")

    status = collection.count_documents({"method": "GET", "path": "/status"})
    print(f"{status} status check")

    print("IPs:")
    top_ips = collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])

    for ip in top_ips:
        print(f"\t{ip['_id']}: {ip['count']}")
