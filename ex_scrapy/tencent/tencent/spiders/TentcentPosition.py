# -*- coding: utf-8 -*-
import scrapy
from tencent.items import TencentItem


class TentcentpositionSpider(scrapy.Spider):
    name = 'TentcentPosition'
    allowed_domains = ['https://hr.tencent.com']
    start_urls = ['https://hr.tencent.com']
    url = 'https://hr.tencent.com/position.php/?&start={start}'

    def start_requests(self):
        offset = 0
        while True:
            if offset >= 4010:
                break
            yield scrapy.Request(
                self.url.format(start=offset), callback=self.parse_detial)
            offset += 10

    def parse_detial(self, response):
        eve_position_data = response.xpath(
            '//tr[@class="even"]|//tr[@class="odd"]')
        for eve_data in eve_position_data:
            Item = TencentItem()
            positionName = eve_data.xpath('./td[1]/a/text()').extract_first()
            positionLink = eve_data.xpath('./td[1]/a/@href').extract_first()
            positionType = eve_data.xpath('./td[2]/text()').extract_first()
            positionNum = eve_data.xpath('./td[3]/text()').extract_first()
            positionWorlLocation = eve_data.xpath(
                './td[4]/text()').extract_first()
            positionTime = eve_data.xpath('./td[5]/text()').extract_first()
            for field in Item.fields:
                Item[field] = eval(field)
            yield Item
