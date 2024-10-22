#!/usr/bin/env python3
"""
Python function that returns the list
of school having a specific topic.
"""


def schools_by_topic(mongo_collection, topic):
    """Returns a list of schools with a specific topic."""
    return list(mongo_collection.find({'topics': topic}))
