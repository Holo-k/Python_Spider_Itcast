# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from DongguanConsult.items import DongguanconsultItem


class DongguanSpider(CrawlSpider):
    name = 'Dongguan'
    allowed_domains = ['wz.sun0769.com']
    start_urls = [
        'http://wz.sun0769.com/index.php/question/questionType?type=4&page=0'
    ]

    rules = (Rule(LinkExtractor(allow=r'type=4&page=\d+'), follow=True),
             Rule(
                 LinkExtractor(allow=r'question/\d+/\d+\.shtml'),
                 callback='parse_item',
                 follow=False))

    def parse_item(self, response):
        Item = DongguanconsultItem()
        temp_data = response.xpath(
            '//div[contains(@class, "pagecenter p3")]//strong/text()'
        ).extract_first().strip()
        title = temp_data.split(' ')[0].split('：')[-1]
        content = response.xpath(
            '(//div[@class="c1 text14_2"]/text() | //div[@class="contentext"]/text())').extract() #//div[@class="c1 text14_2"]//text()更好
        content = ''.join(content).replace('\t',
                                           '').replace('\xa0', '').replace(
                                               '\n', '').strip()
        url = response.url
        number = temp_data.split(' ')[-1].split(':')[-1]

        for field in Item.fields:
            Item[field] = eval(field)
        yield Item
