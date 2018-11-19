#import scrapy
from Gaia.config import *
import pymongo
import redis
from urllib.parse import quote_plus
from Gaia.items import WorldFinanceItem
from Gaia.logger import crawler
import urllib.request
from bs4 import BeautifulSoup
import os
from Gaia.gaiaupslpy import *
import json
import re

class worldfinanceB:#(scrapy.Spider)
    #name = "worldfinancespider"

    def __init__(self):
        redis_args = get_redis_args()
        mongo_db_args = get_mongo_db_args()
        pool = redis.ConnectionPool(
            host=redis_args.get('host')
            , port=redis_args.get('port')
            , db=redis_args.get('id_name'))
        self.server = redis.Redis(connection_pool=pool)

        uri = "mongodb://{}:{}@{}:{}/{}".format(quote_plus(mongo_db_args.get('user')),
                                                quote_plus(mongo_db_args.get('password')),
                                                mongo_db_args.get('host'),
                                                mongo_db_args.get('port'), mongo_db_args.get('db_name'))

        crawler.info("uri: %s", uri)
        connection = pymongo.MongoClient(uri)
        crawler.info("db: %s", mongo_db_args.get('db_name'))
        self.db = connection[mongo_db_args.get('db_name')]

    # def start_requests(self):
    #     hearders = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
    #     yield scrapy.Request(url=self.url0, callback=self.parse_worldfinance, headers=hearders)
    #     for i in range(2, 10, 1):
    #         url = self.url.format(i)
    #         yield scrapy.Request(url = url, callback = self.parse_worldfinance, dont_filter = True, headers=hearders)

    def parse_worldfinance(self,response):#,response
        bf = BeautifulSoup(response, 'lxml')
        lis = bf.find_all('li', class_='item')
        for li in lis:
            if li.img != None:
                #continue
                item = WorldFinanceItem()
                item['datasource'] = "财经_环球网"
                crawler.info("item['datasource']: %s",item['datasource'])
                item['title'] = li.find_all('a')[0].get('title')
                crawler.info("item['title']: %s", item['title'])
                item['url'] = li.find_all('a')[0].get('href')
                crawler.info("item['url']: %s", item['url'])
                item['simdigest'] = li.h5.contents[0]
                crawler.info("item['simdigest']: %s", item['simdigest'])
                item['abouttime'] = li.h6.contents[1]
                crawler.info("item['abouttime']: %s", item['abouttime'])
                imagescr = li.img.get('src')
                try:
                    imgsrc = os.getcwd() + "\\img_wordfinance"
                    if not os.path.isdir(imgsrc):
                        os.mkdir("img_wordfinance")
                    latestnum = self.find_last(imagescr, '/') + 1#imagescr.rfind('/') + 1
                    imgname = imagescr[latestnum:]
                    urllib.request.urlretrieve(imagescr, imgsrc + '\\' + imgname)
                    text = gaia_upload_u('http://gress.gaiafintech.com/upload', imagescr)
                    jsontext = json.loads(text)
                    dfilesjson = jsontext['dfiles']
                    if len(dfilesjson) > 0:
                        item['imagescr'] = jsontext['dfiles']
                    else:
                        item['imagescr'] = imagescr
                        crawler.info('%s的图片未上传成功', item['titletext'])
                        break
                    crawler.info('imagescr : %s', item['imagescr'])
                    _id = item['title']
                    hkey = "worldfinance_filter"
                    if self.server.hget(hkey, _id) is None:
                        self.server.hset(hkey, _id, _id)
                        self.db['photonews'].insert_one(dict(item))

                except Exception as e:
                    crawler.info(e)

            else:
                continue

    def find_last(self, string, str):
        last_position = -1
        while True:
            position = string.find(str, last_position + 1)
            if position == -1:
                return last_position
            last_position = position

if __name__=="__main__":
    world = worldfinanceB()
    url0 = "http://finance.huanqiu.com/hqsl/"
    request = urllib.request.Request(url=url0)
    response = urllib.request.urlopen(request)
    world.parse_worldfinance(response)
    for i in range(2, 9, 1):
        url = url0 + str(i) + ".html"
        request = urllib.request.Request(url=url)
        response = urllib.request.urlopen(request)
        world.parse_worldfinance(response)
    # hearders = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}



