# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SinanewsPipeline(object):
    def process_item(self, item, spider):
        filename = f'{item["head"]}.txt'
        with open(
                f'{item["subFilename"]}/ {filename}', mode='w',
                encoding='utf-8') as file:
            file.write(item['content'])
        return item
