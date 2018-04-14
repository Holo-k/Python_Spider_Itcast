# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.pipelines.images import ImagesPipeline
import scrapy
from scrapy.exceptions import DropItem
import re


class MengtuPipeline(object):
    def __init__(self, file):
        self.file = file

    @classmethod
    def from_crawler(cls, crawler):
        return cls(file=open('./data.json', mode='w', encoding='utf-8'))

    def process_item(self, item, spider):
        self.file.write(json.dumps(dict(item), ensure_ascii=False, indent=1))
        return item

    def close_spider(self, spider):
        self.file.close()


class PixivPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None):
        folder = request.meta['title']
        folder_strip = strip(folder)
        # _id = request.meta['_id']
        # if _id:
        #     image_guid = str(
        #         _id + re.search("(.jpg|.png$)", response.url).group(1))
        # else:
        #     image_guid = request.url.split('/')[-1]
        image_guid = request.url.split('/')[-1]
        filename = u'full/{0}/{1}'.format(folder_strip, image_guid)
        return filename

    def get_media_requests(self, item, info):
        p_imgs = item['p_imgs']
        p_id = item['p_id']
        for img, _id in zip(p_imgs, p_id):
            yield scrapy.Request(
                img, meta={
                    '_id': _id,
                    'title': item['p_title']
                })

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item


def strip(path):
    """
    :param path: 需要清洗的文件夹名字
    :return: 清洗掉Windows系统非法文件夹名字的字符串
    """
    path = re.sub(r'[？\\*|“<>:/]', '', str(path))
    return path
