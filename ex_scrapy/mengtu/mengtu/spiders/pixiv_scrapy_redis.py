# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Rule
from mengtu.items import PixivItem
from scrapy_redis.spiders import RedisCrawlSpider


class PixivSpider(RedisCrawlSpider):
    name = 'pixiv_distributed'
    redis_key = 'pixivspider:start_urls'

    def __init__(self, *args, **kwargs):
        # Dynamically define the allowed domains list.
        domain = kwargs.pop('domain', '')
        self.allowed_domains = filter(None, domain.split(','))
        super(PixivSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        yield scrapy.Request('http://moe.005.tv/moeimg/tb/')

    rules = (
        Rule(
            LinkExtractor(
                allow=r'moe.005.tv/\d+\.html',
                restrict_xpaths='//div[@class="zhuti_w_list"]'),
            callback='parse_item',
            follow=True),
        Rule(
            LinkExtractor(restrict_xpaths='//div[@class="content_nr"]//h1'),
            callback='parse_item',
            follow=True),
        Rule(
            LinkExtractor(
                allow=r'moe.005.tv/\d+?_\d\.html',
                restrict_xpaths='//ul[@class="pagelist"]'),
            callback='parse_item',
            follow=True),
        Rule(
            LinkExtractor(
                allow=r'/moeimg/tb/list_3_\d+?\.html',
                restrict_xpaths='//ul[@class="pagelist"]'),
            follow=True))

    def parse_item(self, response):
        content_nr = response.xpath('//div[@class="content_nr"]')
        for eve_item in content_nr:
            Item = PixivItem()
            p_id = eve_item.xpath(
                './div[1]//text()|./div[2]//text()|./div[3]//text()').re(
                    'id=(\d+)')
            p_imgs = eve_item.xpath(
                './div[1]/img/@src|.//div[2]/img/@src|./div[3]/img/@src'
            ).extract()
            p_title = response.xpath(
                '//div[@class="content_w_box"]/h1/text()').extract_first()
            try:
                for field in Item.fields:
                    Item[field] = eval(field)
            except NameError as e:
                print('Name Error')
            yield Item
