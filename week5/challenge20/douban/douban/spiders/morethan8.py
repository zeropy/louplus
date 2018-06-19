# -*- coding: utf-8 -*-
import scrapy
# from scrapy.spiders import Rule
# from scrapy.linkextractors import LinkExtractor
from douban.items import DoubanItem


class Morethan8Spider(scrapy.spiders.CrawlSpider):
    name = 'morethan8'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/subject/3011091/']

    def parse(self, response):
        item = DoubanItem()
        item['url'] = response.url
        item['name'] = response.css('div#content h1 span::text').extract_first()
        item['summary'] = response.xpath('//span[@property="v:summary"]/text()').extract()
        item['score'] = response.css('strong.rating_num::text').extract_first()
        yield item

        for link in response.css('div.recommendations-bd a::attr(href)'):
            yield response.follow(link)
