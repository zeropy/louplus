# -*- coding: utf-8 -*-
import scrapy
from shiyanlougithub.items import RepoItem


class ReposSpider(scrapy.Spider):
    # 爬虫标识符号，在 scrapy 项目中可能会有多个爬虫，name 用于标识每个爬虫，不能相同
    name = 'repos'
    #allowed_domains = ['github.com']
    #start_urls = ['http://github.com/']

    @property
    def start_urls(self):
        # 返回一个可迭代对象
        url_tmpl = 'https://github.com/shiyanlou?tab=repositories&page={}'
        urls = (url_tmpl.format(i) for i in range(1,5))
        return urls

    def parse(self, response):
        """ 这个方法作为 `scrapy.Request` 的 callback，在里面编写提取数据的代码。scrapy 中的下载器会下载 `start_reqeusts` 中定义的每个 `Request` 并且结果封装为一个 response 对象传入这个方法。
        """
        for repo in response.css('li.public'):
            item = RepoItem({
                'name':repo.css('h3 a::text').re_first('\s*(\S+)'),
                'update_time': repo.css('relative-time::attr(datetime)').extract_first()
            })
            yield item
