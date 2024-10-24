#!/usr/bin/env python3
"""A Cache class."""
import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times a method is called."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs
    and outputs for a particular function."""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        inputs_key = method.__qualname__ + ":inputs"
        outputs_key = method.__qualname__ + ":outputs"

        self._redis.rpush(inputs_key, str(args))

        output = method(self, *args, **kwargs)
        self._redis.rpush(outputs_key, output)
        return output
    return wrapper


def replay(fn: Callable) -> None:
    """Display the history of calls of a particular function."""
    r = redis.Redis()
    inputs = r.lrange(fn.__qualname__ + ":inputs", 0, -1)
    outputs = r.lrange(fn.__qualname__ + ":outputs", 0, -1)
    print(f"{fn.__qualname__} was called {len(outputs)} times:")
    for inp, out in zip(inputs, outputs):
        print(f"{fn.__qualname__}(*{(inp.decode('utf-8'))}) -> "
              f"{out.decode('utf-8')}")


class Cache:
    def __init__(self):
        """Initialiase the redis connection."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
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
