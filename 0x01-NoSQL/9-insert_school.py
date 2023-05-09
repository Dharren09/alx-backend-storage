#!/usr/bin/env python3

""" function that inserts a new doc in a collection based on kwargs"""

def insert_school(mongo_collection, **kwargs):
    """initialize an empty set for new document"""
    new_doc = {}
    for key, value in kwargs.items():
        new_doc[key] = value
    result = mongo_collection.insert_one(new_doc)
    return result.inserted_id
