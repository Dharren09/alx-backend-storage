#!/usr/bin/env python3
"""
script for improving a previous script by adding top 10 of the
the most present IPs in collection nginx of db logs
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
    print("IPs:")
    result = {}
    for item in nginx_collection.find():
        result[item["ip"]] = 0

    for item in nginx_collection.find():
        key = item["ip"]
        result[key] += 1

    count = 0
    for key, value in sorted(result.items(), key=lambda x: x[1], reverse=True):
        count += 1
        print(f"\t{key}: {value}")
        if count == 10:
            break
