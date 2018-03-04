# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ShiyanlouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class CourseimageItem(scrapy.Item):
    image_urls = scrapy.Field()
    images = scrapy.Field()


class MultipagecourseItem(scrapy.Item):
    name = scrapy.Field()
    image = scrapy.Field()
    author = scrapy.Field()
