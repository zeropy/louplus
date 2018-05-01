# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import ShiyanlougithubItem

class ShiyanlouSpider(scrapy.Spider):
    name = 'shiyanlou'
    allowed_domains = ['github.com']
    # start_urls = ['https://github.com/shiyanlou?tab=repositories']

    @property
    def start_urls(self):
        temp_url = 'https://github.com/shiyanlou?tab=repositories&page={}'
        urls = [ temp_url.format(i) for i in range(1,5)]
        return urls

    def parse(self, response):
        for repo in response.css('div#user-repositories-list li'):
            name = repo.css('h3 a::text').re_first(' +(.*)')
            update_time = repo.css('relative-time::attr(datetime)').extract_first()
            yield ShiyanlougithubItem(
                name = name,
                update_time = update_time
            )
