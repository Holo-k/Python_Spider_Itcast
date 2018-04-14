# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class TencentWithCrawlTemplatePipeline(object):
    def __init__(self, file):
        self.file = file

    @classmethod
    def from_crawler(cls, crawler):
        return cls(file=open('./data.json', mode='w', encoding='utf-8'))

    def process_item(self, item, spider):
        self.file.write(
            json.dumps(dict(item), ensure_ascii=False, indent=1))
        return item

    def close_spider(self, spider):
        self.file.close()
