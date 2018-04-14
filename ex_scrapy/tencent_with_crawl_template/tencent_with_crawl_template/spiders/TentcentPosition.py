# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from tencent_with_crawl_template.items import TencentWithCrawlTemplateItem


class TentcentpositionSpider(CrawlSpider):
    name = 'TentcentPosition'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['https://hr.tencent.com/position.php?&start=0#a']

    rules = (Rule(
        LinkExtractor(allow='position\.php\?&start=\d+#a'), callback='parse_item',
        follow=True), )

    def parse_item(self, response):
        eve_position_data = response.xpath(
            '//tr[@class="even"]|//tr[@class="odd"]')
        for eve_data in eve_position_data:
            Item = TencentWithCrawlTemplateItem()
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
