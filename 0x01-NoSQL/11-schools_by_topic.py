#!/usr/bin/env python3

"""function returns a list of school having a specific topic"""


def schools_by_topic(mongo_collection, topic):
    """topic is searched and result returned as a list"""
    return mongo_collection.find({"topics": topic})
