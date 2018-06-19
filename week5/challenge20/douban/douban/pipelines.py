# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import redis
import json
import os


class DoubanPipeline(object):
    def process_item(self, item, spider):
        len = self.redis.llen('douban_movie:items')
        if len > 30:
            os.abort()
        try:
            item['score'] = float(item['score'])
        except:
            # print(111111111)
            return item
        if item['score'] >= 8:
            self.redis.lpush('douban_movie:items', json.dumps(dict(item)))
        return item

    def open_spider(self, spider):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=0)
