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
            repo_url = repo.css('h3 a::attr(href)').extract_first()
            request = scrapy.Request(url=response.urljoin(repo_url),callback=self.parse_repo)
            request.meta['item'] = item

            yield request

    def parse_repo(self,response):
        item = response.meta['item']
        item['commits'] = response.css('li.commits span::text').re_first('([\d,]+)')
        item['branchs'] = response.xpath('//div[@class="stats-switcher-wrapper"]/ul/li[2]').css('span::text').re_first('[\d,]+')
        item['releases'] = response.xpath('//div[@class="stats-switcher-wrapper"]/ul/li[3]').css('span::text').re_first('[\d,]+')
        yield item
