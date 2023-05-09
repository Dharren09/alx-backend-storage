#!/usr/bin/env python3

"""fx lits all documebts in a collection"""

def list_all(mongo_collection):
    """finding all documnets"""
    all_docs = mongo_collection.find({})
    result = []
    for document in all_docs:
        result.append(document)
    return result
