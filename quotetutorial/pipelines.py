# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
import pymongo

# class QuotetutorialPipeline(object):
#用于加工item数据
class TextPipeline(object):
    def __init__(self):
        #将item中的text长度设置在50
        self.limit = 50

    def process_item(self, item, spider):
        if item["text"]:
            if len(item["text"]) > self.limit:
                item["text"] = item["text"][:self.limit].rstrip()+"..."
            return item
        else:
            #删除此item
            return DropItem("Missing Text")
        return item

#将item数据保存到mongodb中
class MongoPipeline(object):

    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    #pipeline中的默认方法，用于在获取settings文件的配置参数
    @classmethod
    def from_crawler(cls,crawler):
        #返回 一个构造函数的调用，也就是返回一个对象
        return cls(
            mongo_uri= crawler.settings.get("MONGO_URI"),
            mongo_db= crawler.settings.get("MONGO_DB")
        )
    #此方法在爬虫刚要启动时运行
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    #此方法在quotes.py中有产生了yield item对象时调用
    def process_item(self,item,spider):
        #保存时需要将item对象转换成字典对象
        self.db["quotes"].insert(dict(item))
        return item

    #此方法在爬虫关闭时调用
    def colse_spider(self,spider):
        self.client.close()