# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PixivItem(scrapy.Item):
    # define the fields for your item here like:
    p_id = scrapy.Field()
    p_imgs = scrapy.Field()
    p_title = scrapy.Field()
