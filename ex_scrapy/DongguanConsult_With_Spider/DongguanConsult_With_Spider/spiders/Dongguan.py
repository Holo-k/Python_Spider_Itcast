# -*- coding: utf-8 -*-
import scrapy
import requests
from lxml import etree
import re
from DongguanConsult_With_Spider.items import DongguanconsultWithSpiderItem


class DongguanSpider(scrapy.Spider):
    name = 'Dongguan'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/']
    url = 'http://wz.sun0769.com/index.php/question/questionType?type=4&page={page}'

    def start_requests(self):
        page = 0
        max_page = int(
            re.search(
                'type=4&page=(\d+)',
                etree.HTML(
                    requests.get(
                        self.url
                    ).text).xpath(
                        '//div[@class="pagination"]//a[last()]/@href')[0])
            .group(1))
        while True:
            if page > max_page:
                break
            yield scrapy.Request(
                self.url.format(page=page), callback=self.parse_page)
            page += 30

    def parse_page(self, response):
        consult_urls = response.xpath('//a[@class="news14"]/@href').extract()
        for eve_url in consult_urls:
            yield scrapy.Request(eve_url, callback=self.parse_detail)

    def parse_detail(self, response):
        Item = DongguanconsultWithSpiderItem()
        temp_data = response.xpath(
            '//div[contains(@class, "pagecenter p3")]//strong/text()'
        ).extract_first().strip()
        title = temp_data.split(' ')[0].split('：')[-1]
        content = response.xpath(
            '(//div[@class="c1 text14_2"]/text() | //div[@class="contentext"]/text())'
        ).extract()  #//div[@class="c1 text14_2"]//text()更好
        content = ''.join(content).replace('\t',
                                           '').replace('\xa0', '').replace(
                                               '\n', '').strip()
        url = response.url
        number = temp_data.split(' ')[-1].split(':')[-1]

        for field in Item.fields:
            Item[field] = eval(field)
        yield Item
