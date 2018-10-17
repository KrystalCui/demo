# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import logging
import os
from urllib.parse import quote_plus
import pymongo
import redis
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from Gaia.logger.log import crawler
from Gaia.items import *
from scrapy.utils.serialize import ScrapyJSONEncoder
from twisted.internet.threads import deferToThread
from Gaia.scrapy_redis import connection

class MongoDBPipeline(object):
    def __init__(self):
        pool = redis.ConnectionPool(
            host = settings['REDIS_HOST']
            ,port = settings['REDIS_PORT']
            ,db = settings['REDIS_DB']
            ,password = quote_plus(settings['REDIS_PASSWORD']))
        self.server = redis.Redis(connection_pool=pool)

        uri = "mongodb://{}:{}@{}:{}".format (quote_plus(settings['MONGODB_USER']),
                                              quote_plus(settings['MONGODB_PASSWORD']),
                                                 settings['MONGODB_SERVER'],
                                                 settings['MONGODB_PORT'])

        crawler.info("uri: %s", uri)
        connection=pymongo.MongoClient(uri)
        crawler.info("db: %s", settings['MONGODB_DB'])
        self.db = connection[settings['MONGODB_DB']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing{0}!".format(data))
        if valid:
            try:
                'This returns the number of values added, zero id alread exists.'
                if type(item) == ParameterItem:
                    title = item['title']
                    key = "news_filter_{}".format(title)
                    if self.server.get(key) is None:
                        self.server.set(key, title)
                        self.db['futures_news'].insert(dict(item))
                        crawler.info('add futures_news: %s', dict(item))
                elif type(item) == F10Item:
                    title = item['title']
                    key = "news_filter_{}".format(title)
                    if self.server.get(key) is None:
                        self.server.set(key, title)
                        self.db['futures_news'].insert(dict(item))
                        crawler.info('add futures_news: %s', dict(item))
                elif type(item) == InvestmentAdviserItem:
                    title = item['title']
                    key = "investment_advisers_filter_{}".format(title)
                    if self.server.get(key) is None:
                        self.server.set(key, title)
                        self.db['investment_advisers'].insert(dict(item))
                        crawler.info('add investment_advisers: %s', dict(item))
            except(pymongo.errors.WriteError, KeyError) as err:
                crawler.info('add error: %s', err)
                raise DropItem("Duplicated Item: {}".format(item['title']))
        return item

class RedisPipeline(object):
    """Pushes serialized item into a redis list/queue"""

    def __init__(self, server):
        self.server = server
        self.encoder = ScrapyJSONEncoder()

    @classmethod
    def from_settings(cls, settings):
        server = connection.from_settings(settings)
        return cls(server)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def process_item(self, item, spider):
        return deferToThread(self._process_item, item, spider)

    def _process_item(self, item, spider):
        key = self.item_key(item, spider)
        data = self.encoder.encode(item)
        self.server.rpush(key, data)
        return item

    def item_key(self, item, spider):
        """Returns redis key based on given spider"""
        return "%s:items" % spider.name
