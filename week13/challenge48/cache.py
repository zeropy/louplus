#!/usr/bin/env python
# coding=utf-8
import redis
import json

class RedisCache(object):
    def __init__(self, redis_client):
        self._redis = redis_client

    def cache(self, timeout=0):
        def decorator(func):
            def wrapper(*args, **kwargs):
                result = self._redis.get(func.__name__)
                if result: return json.loads(result)
                result = func(*args, **kwargs)
                result = json.dumps(result)
                self._redis.set(func.__name__, result)
                self._redis.expire(func.__name__, timeout)
                return result
            return wrapper
        return decorator
