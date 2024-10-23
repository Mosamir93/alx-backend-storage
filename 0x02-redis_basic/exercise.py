#!/usr/bin/env python3
"""A Cache class."""
import redis
import uuid
from typing import Union, Callable, Optional


class Cache:
    def __init__(self):
        """Initialiase the redis connection."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store the  data in redis."""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None):
        """Takes a key string argument and an
        optional Callable argument named fn"""
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """Retrieve and convert the data to a string."""
        return self.get(key).decode('utf-8')

    def get_int(self, key: str) -> int:
        """Retrieve and convert the data to an integer."""
        return int(self.get(key))
