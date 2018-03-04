# -*- coding: utf-8 -*-
import scrapy
from shiyanlou.items import CourseimageItem


class CourseimageSpider(scrapy.Spider):
    name = 'courseimage'
    #allowed_domains = ['shiyanlou.com/course']
    start_urls = ['https://shiyanlou.com/courses/']

    def parse(self, response):
        item = CourseimageItem()
        item['image_urls'] = response.xpath('//div[@class="course-img"]/img/@src').extract()
        yield item
