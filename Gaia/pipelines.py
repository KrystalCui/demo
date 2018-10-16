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
from .logger.log import crawler
from Lord.items import *

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