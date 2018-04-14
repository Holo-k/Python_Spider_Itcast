# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from douban.items import DoubanItem


class Movietop250Spider(CrawlSpider):
    name = 'MovieTop250'
    allowed_domains = ['movie.douban.com']
    start_urls = ['http://movie.douban.com/']
    url = 'https://movie.douban.com/top250'
    rules = (Rule(
        LinkExtractor(allow=r'\?start=\d+?&'),
        callback='parse_item',
        follow=True), )

    def start_requests(self):
        yield scrapy.Request(self.url)

    def parse_item(self, response):
        info_list = response.xpath('//div[@class="info"]')
        for eve_info in info_list:
            Item = DoubanItem()
            title = eve_info.xpath(
                ".//span[@class='title'][1]/text()").extract()[0]
            bd = eve_info.xpath(".//div[@class='bd']/p/text()").extract()[0]
            star = eve_info.xpath(
                ".//div[@class='star']/span[@class='rating_num']/text()"
            ).extract()[0]
            quote = eve_info.xpath(
                ".//p[@class='quote']/span/text()").extract()
            if len(quote) != 0:
                quote = quote[0]
            for field in Item.fields:
                try:
                    Item[field] = eval(field)
                except NameError as e:
                    pass
            yield Item
