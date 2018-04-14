# -*- coding: utf-8 -*-
import scrapy
from douyu.items import DouyuMVItem
import json


class DouyumeinvSpider(scrapy.Spider):
    name = 'douyumeinv'
    allowed_domains = ['capi.douyucdn.cn']
    start_urls = ['http://capi.douyucdn.cn/']
    url = 'http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset={offset}'

    def start_requests(self):
        offset = 0
        while True:
            if offset > 420:
                break
            yield scrapy.Request(
                self.url.format(offset=offset), callback=self.parse_detail)
            offset += 20

    def parse_detail(self, response):
        data = json.loads(response.text)['data']
        for eve_data in data:
            Item = DouyuMVItem()
            nickname = eve_data['nickname']
            image_link = eve_data['vertical_src']
            for field in Item.fields:
                try:
                    Item[field] = eval(field)
                except NameError as e:
                    pass
            yield Item
