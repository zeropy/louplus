# -*- coding: utf-8 -*-

from shiyanlougithub.items import RepoItem
from sqlalchemy.orm import sessionmaker
from shiyanlougithub.models import Repository,engine
from datetime import datetime
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class ShiyanlougithubPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item,RepoItem):
            self._process_repo_item(item)
        return item

    def _process_repo_item(self,item):
        item['update_time'] = datetime.strptime(item['update_time'],'%Y-%m-%dT%H:%M:%SZ')
        self.session.add(
            Repository(**item)
        )

    def open_spider(self,spider):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def close_spider(self,spider):
        self.session.commit()
        self.session.close()
