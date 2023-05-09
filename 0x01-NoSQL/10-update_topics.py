#!/usr/bin/env python3

"""function that changes all topics od a school doc
based on the name.
name (string)- school name to update
topics(list of strings) list that will be approached in school
"""


def update_topics(mongo_collection, name, topics):
    """updates all topics of a school based on school name"""
    result = mongo_collection.update_many({'name': name}, {'$set': {'topics': topics}})
    return result.modified_count
