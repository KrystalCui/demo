# -*- coding: utf-8 -*-
import scrapy
from scrapy import cmdline
import re
from Gaia.logger import crawler
from Gaia.items import InformationAggregationItem
import time
import redis
import pymongo
from urllib.parse import quote_plus as pl
from Gaia.config import *
# import subprocess
# from collections import deque
import threading
from threading import Thread
import multiprocessing as mp
from multiprocessing import Process
from fake_useragent import UserAgent


class SinaFinanceNews(scrapy.Spider, Process):
    name="SinaFinanceNewsSpider"
    def __init__(self):
        #配置数据库
        redis_args = get_redis_args()
        mongodb_args = get_mongo_db_args()
        #redis
        pool = redis.ConnectionPool(
            host=redis_args.get('host'),
            port=redis_args.get('port'),
            db=redis_args.get('id_name'),
            password=redis_args.get('password')
        )
        self.server = redis.Redis(connection_pool=pool)

        #mongodb
        uri = 'mongodb://{}:{}@{}:{}/{}'.format(
            pl(mongodb_args.get('user')),
            pl(mongodb_args.get('password')),
            mongodb_args.get('host'),
            mongodb_args.get('port'),
            mongodb_args.get('db_name')
        )
        #写入日志
        crawler.info("uri: %s", uri)
        crawler.info("db: %s", mongodb_args.get('db_name'))

        connection = pymongo.MongoClient(uri)
        # connection = pymongo.MongoClient(user=pl(mongodb_args.get('user')),
        #                                  password=pl(mongodb_args.get('password')),
        #                                  host=mongodb_args.get('host'),
        #                                  port=mongodb_args.get('port'))
        self.db = connection[mongodb_args.get('db_name')]
        # self.listdict = deque([])

        # self.pool = mp.Pool(4)
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}
        self.url = 'http://finance.sina.com.cn/roll/index.d.html?cid=56995&page={}'

    def start_requests(self):
        for i in range(22,0,-1):
            url = self.url.format(i)
            yield scrapy.Request(url=url, callback=self.parse_fromlist, dont_filter = True, headers=self.header)

    def parse_fromlist(self, response):
        # crawler.info(response.read().decode('utf-8'))
        uls = response.xpath('.//ul[@class="list_009"]') #爬出来的数据是5个一组的
        for ul in uls:
            # print("aaa:" + a)
            # crawler.info(a.xpath('a/@href').extract())
            for j in range(1,6,1):
                #根据当前页面的显示创建字典,主要是为了将内容的url与标题信息等匹配存储在全部信息获取到后添加数据库
                dic = {}
                stra = str(j)
                strs = '[' + stra + ']'
                #信息列表页面标题,摘要,子标题与此相同
                title = ul.xpath('.//li' + strs + '/a/text()').extract_first()
                # dict['title'] = ul.xpath('.//li' + strs + '/a/text()').extract_first()
                try:
                    # 先与redis内容进行比较,避免浪费
                    hkey = "informationaggregation_filter"
                    if self.server.hget(hkey,title) is None:
                        dic['title'] = title
                        #信息列表页面时间
                        dic['newstime'] = ul.xpath('.//li' + strs + '/span/text()').extract_first()
                        #内容url
                        dic['contenurl'] = ul.xpath('.//li' + strs + '/a/@href').extract_first()
                        #将信息列表页面的信息存入
                        # self.listdict.append(dict)
                        # print(dict['contenurl'])
                        #
                        # 将信息列表页面的信息存入
                        # self.listdict.append(dict)
                        # print(dict['contenurl'])
                        yield scrapy.Request(url=dic['contenurl'], meta={'item': dic, 'itemB':1}, callback=self.parse_getcontent,
                                             dont_filter=True, headers=self.header)
                        # tup = (dict, dict['contenurl'],)

                        # Thread(target=self.gogetcontent, args=(tup,)).start()
                        # self.pool.apply_async(self.gogetcontent, args=(tup,))
                        # functionParse = self.parse_getcontent
                        # p = Process(target=self.gogetcontent, kwargs={'dict':dict, 'url':dict['contenurl'], 'func':functionParse, 'header':self.header}).start()#args=(dict, dict['contenurl'],)
                        # p.close()
                        # print(threading.currentThread().name)
                        # print('当前运行的线程:  ', threading.enumerate())
                        # print('当前运行的线程的数量:  ', threading.activeCount())
                except Exception as e:
                    print('当前错误信息: ',e)
                    continue


    # #线程函数,访问新闻内容页面
    # @staticmethod
    # def gogetcontent(dict, url, func, header):
    #     print(type(dict))
    #     print(dict)
    #     #print(url)
    #     # if len(tup) > 0:
    #     # dict = tup[0]
    #     # url = tup[1]
    #     yield scrapy.Request(url=url, meta={'item': dict}, callback=func,
    #                              dont_filter=True, headers=header)
    #         # print(type(tup))
            # print(tup)
            # print(url)

    #查询内容并存到数据库
    # @staticmethod
    def parse_getcontent(self,response):
        # time.sleep(1)
        dic = response.meta['item']
        div = response.xpath('.//div[@class="article"]')
        time.sleep(1)
        ps = div.xpath('.//p')
        if ps == [] :
            ps = div.xpath('.//div/p')
        # if ps == [] :
        #     time.sleep(1)
        #     ps = response.xpath('.//div[@id="artibody"]/p')
        # if ps == [] :
        #     time.sleep(1)
        #     ps = response.xpath('.//div[@id="artibody"]/div/p')

        #print(dict['title'])
        content = ''
        for p in ps:
            str = p.xpath('.//text()').extract_first()
            if str == None :
                continue
            else:
                try:
                    str = re.sub('\s', '', str)
                    str = str.strip('\t')
                    if str.find('责任编辑') > 0:
                        str = ''
                except:
                    a = 1
                if not str == '':
                    content += str + "\r\n"
                # else:
                #     content += str + "\r\n"
            # try:
            #     content += p.xpath('.//text()').extract_first()
            # except Exception as e:
            #     print(e)
        # print(content)
        if content == '':
            timesNum = response.meta['itemB']
            if timesNum < 3:
                timesNum += 1
                yield scrapy.Request(url=response.url, callback=self.parse_getcontent, meta={'item': dic, 'itemB': timesNum}, dont_filter=True, headers=self.header)
        else:
            item = InformationAggregationItem()
            item['content'] = content
            crawler.info("content:%s", content)

            #此处标题,摘要,子标题相同
            title = dic['title']
            item['title'] = title
            crawler.info("title:%s", title)
            item['abstract'] = title
            crawler.info("abstract:%s", title)
            item['subtitle'] = title
            crawler.info("subtitle:%s", title)
            item['state'] = 0
            crawler.info("state:%s", item['state'])
            item['newstime'] = dic['newstime']
            crawler.info("newstime:%s", item['newstime'])
            item['datasource'] = '新浪财经'
            crawler.info("datasource:%s", item['datasource'])

            hkey = "informationaggregation_filter"
            try:
                if self.server.hget(hkey, title) is None:
                    self.server.hset(hkey, title, title)
                    self.db['informationaggregation'].insert(dict(item))
            except Exception as e:
                crawler.into("本次新浪财经存入失败原因:%s", e)


if __name__ == '__main__':
    cmdline.execute("scrapy crawl SinaFinanceNewsSpider".split())