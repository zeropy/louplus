# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import RepoItem


class ReposSpider(scrapy.Spider):
    name = 'repos'
    #allowed_domains = ['github.com']
    #start_urls = ['http://github.com/']

    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?tab=repositories&page={}'
        urls = (url_tmpl.format(i) for i in range(1,5))
        return urls

    def parse(self, response):
        for repo in response.css('li.public'):
            item = RepoItem({
                'name':repo.css('h3 a::text').re_first('\s*(\S+)'),
                'update_time': repo.css('relative-time::attr(datetime)').extract_first()
            })
            yield item
