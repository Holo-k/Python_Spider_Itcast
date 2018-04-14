# -*- coding: utf-8 -*-
import scrapy
import os
from SinaNews.items import SinanewsItem


class News2Spider(scrapy.Spider):
    name = 'News_2'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://sina.com.cn/']

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

    def parse_sub(self, response):
        meta_1 = response.meta['meta_1']
        sonUrls = response.xpath('//a/@href').extract()
        items = []
        for i in range(0, len(sonUrls)):
            is_belong = sonUrls[i].endswith(
                '.shtml') and sonUrls[i].startswith(meta_1['parentUrls'])

            if is_belong:
                item = SinanewsItem()
                item['parentTitle'] = meta_1['parentTitle']
                item['parentUrls'] = meta_1['parentUrls']
                item['subUrls'] = meta_1['subUrls']
                item['subTitle'] = meta_1['subTitle']
                item['subFilename'] = meta_1['subFilename']
                item['sonUrls'] = sonUrls[i]
                items.append(item)

        for item in items:
            yield scrapy.Request(
                url=item['sonUrls'],
                meta={'meta_2': item},
                callback=self.detail_parse)

    def detail_parse(self, response):
        item = response.meta['meta_2']
        content = ""
        head = response.xpath(
            '//h1[@class="main-title"]/text()|//h1[@id="main_title"]/text()|//h1[@id="artibodyTitle"]/text()'
        ).extract_first()
        content_list = response.xpath(
            '//div[@id="artibody"]/p/text()').extract()
        for eve_content in content_list:
            content += eve_content
        item['head'] = head
        item['content'] = content
        yield item