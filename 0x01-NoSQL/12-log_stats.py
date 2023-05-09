#!/usr/bin/env python3
"""
script provides somme stats about nginx logs stored in MongoDB
"""

from pymongo import MongoClient

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    print("{} logs".format(nginx_collection.count_documents({})))
    print("Methods:")
    for item in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        print("\tmethod {}: {}".format(item,
              nginx_collection.count_documents({"method": item})))
    print("{} status check".format(nginx_collection.count_documents(
          {"method": "GET", "path": "/status"})))
