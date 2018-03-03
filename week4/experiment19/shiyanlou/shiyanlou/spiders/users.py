# -*- coding: utf-8 -*-
import scrapy
from shiyanlou.items import UserItem


class UsersSpider(scrapy.Spider):
    name = 'users'

    @property
    def start_urls(self):
        return ('https://www.shiyanlou.com/user/{}'.format(i)
                for i in range(525000,524800,-10)
                )


    def parse(self, response):
        yield UserItem({
            'name':response.css('div.userinfo-banner-meta span.username::text').extract_first(),
            'type':response.css('a.member-icon img.user-icon::attr(title)').extract_first(default='普通会员'),
            'status':response.xpath('//div[@class="userinfo-banner-status"]/span[1]/text()').extract_first(),
            'school':response.xpath('//div[@class="userinfo-banner-status"]/span[2]/text()').extract_first(),
            'job':response.xpath('//div[@class="userinfo-banner-status"]/span[2]/text()').extract_first(),
            'level':response.css('div.userinfo-banner-meta span.user-level::text').re_first('L(\d+)'),
            'join_date':response.css('span.join-date::text').re_first('\d{4}-\d{2}-\d{2}'),
            'learn_courses_num':response.css('span.latest-learn-num::text').extract_first()
        })
