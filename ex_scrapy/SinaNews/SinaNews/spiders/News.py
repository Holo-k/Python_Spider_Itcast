# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import os
from SinaNews.items import SinanewsItem
from scrapy_splash import SplashRequest


class NewsSpider(CrawlSpider):
    name = 'News'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://sina.com.cn/']

    rules = (Rule(
        LinkExtractor(restrict_xpaths='//ul[@class="list01"]//a/@href'),
        callback='parse_sub',
        follow=True),
             Rule(
                 LinkExtractor(restrict_xpaths='//a'),
                 callback='parse_son',
                 follow=False))

    def start_requests(self):
        url = 'http://news.sina.com.cn/guide/'
        yield scrapy.Request(url, callback=self.parse_guide)

    def parse_guide(self, response):
        items = []
        parentTitle = response.xpath('//h3/a/text()').extract()
        parentUrls = response.xpath('//h3/a/@href').extract()

        subTitle = response.xpath(
            '//ul[@class="list01"]/li/a/text()').extract()
        subUrls = response.xpath('//ul[@class="list01"]/li/a/@href').extract()

        for i in range(0, len(parentTitle)):
            parent_file_name = f'./Data/{parentTitle[i]}'

            if (not os.path.exists(parent_file_name)):
                os.makedirs(parent_file_name)

            for j in range(0, len(subTitle)):
                item = SinanewsItem()
                item['parentTitle'] = parentTitle[i]
                item['parentUrls'] = parentUrls[i]

                is_belong = subUrls[j].startswith(item['parentUrls'])
                if is_belong:
                    sub_file_name = f'{parent_file_name}/{subTitle[j]}'

                    if (not os.path.exists(sub_file_name)):
                        os.makedirs(sub_file_name)

                    item['subUrls'] = subUrls[j]
                    item['subTitle'] = subTitle[j]
                    item['subFilename'] = sub_file_name
                    items.append(item)
        for eve_item in items:
            yield scrapy.Request(
                eve_item['subUrls'],
                meta={'meta_1': eve_item},
                callback=self.parse_sub)

    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
