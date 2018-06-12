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
                if result: return json.loads(result.decode('utf-8'))
                result = func(*args, **kwargs)
                save = json.dumps(result)
                self._redis.set(func.__name__, save)
                self._redis.expire(func.__name__, timeout)
                return result
            return wrapper
        return decorator

if __name__ == '__main__':
    r = redis.StrictRedis(host='localhost',port=6379,db=0)
    cache = RedisCache(r)
    @cache.cache(timeout=10)
    def test():
        return {'a':1}
    result = test()
    print(result)
