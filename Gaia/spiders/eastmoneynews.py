import scrapy
from Gaia.items import InformationAggregationItem
from Gaia.logger import crawler
import urllib.request
import os
from Gaia.gaiaupslpy import *
import time
import json
import re
import multiprocessing as mp
from multiprocessing import Process
from scrapy import cmdline
import time
import redis
import pymongo
from urllib.parse import quote_plus as pl
from Gaia.config import *


class EastMoneyNewsSpider(scrapy.Spider, Process):
    name = "EastMoneyNewsSpider"
    def __init__(self):
        # 配置数据库
        redis_args = get_redis_args()
        mongodb_args = get_mongo_db_args()
        # redis
        pool = redis.ConnectionPool(
            host=redis_args.get('host'),
            port=redis_args.get('port'),
            db=redis_args.get('id_name'),
            password=redis_args.get('password')
        )
        self.server = redis.Redis(connection_pool=pool)

        # mongodb
        uri = 'mongodb://{}:{}@{}:{}/{}'.format(
            pl(mongodb_args.get('user')),
            pl(mongodb_args.get('password')),
            mongodb_args.get('host'),
            mongodb_args.get('port'),
            mongodb_args.get('db_name')
        )
        # 写入日志
        crawler.info("uri: %s", uri)
        crawler.info("db: %s", mongodb_args.get('db_name'))

        connection = pymongo.MongoClient(uri)
        self.db = connection[mongodb_args.get('db_name')]
        # self.pool = mp.Pool(4)
        self.url = 'http://futures.eastmoney.com/a/cqhdd_{}.html'
        self.ISOTIMEFORMAT = '%Y-%m-%d %X'

    def start_requests(self):
        for i in range(25, 0, -1):
            url = self.url.format(i)
            yield scrapy.Request(url=url, callback= self.parse_easymoneyinvestment, dont_filter = True)

    def parse_easymoneyinvestment(self, response):
        uls = response.xpath('.//ul[@id="newsListContent"]')
        for ul in uls:
            lis = ul.xpath('.//li')
            for li in lis:
                title = li.xpath('.//p[@class="title"]/a/text()').extract_first().strip()
                try:
                    # 先与redis内容进行比较,避免浪费
                    hkey = "informationaggregation_filter"
                    if self.server.hget(hkey,title) is None:
                        dict = {}
                        dict['title'] = title
                        dict['abstract'] = li.xpath('.//p[@class="title"]/a/text()').extract_first().strip()
                        dict['newstime'] = li.xpath('.//p[@class="time"]/text()').extract_first().strip()
                        dict['contenturl'] = li.xpath('.//p[@class="title"]/a/@href').extract_first().strip()

                        imagescr = li.xpath('.//div[@class="image"]/a/img/@src').extract_first().strip()
                        try:
                            #截取新闻图片地址作为文件名
                            self.strwd = os.getcwd() + '\\image'
                            if not os.path.isdir(self.strwd):
                                os.mkdir('image')
                            namenum = imagescr.rfind('/') + 1
                            self.namescr = imagescr[namenum:]
                            # self.namescr = item['imagescr'][namenum:]
                            # urllib.request.urlretrieve(self.namescr, self.strwd + '\\' + self.namescr)
                            #上传文件,并获取上传至远程的本地地址
                            text = gaia_upload_u('http://gress.gaiafintech.com/upload', imagescr)
                            jsontext = json.loads(text)
                            dfilesjson = jsontext['dfiles']
                            if len(dfilesjson) > 0:
                                dict['imgURL'] = jsontext['dfiles']
                            else:
                                crawler.info('%s的图片未上传成功', imagescr)
                                break
                            crawler.info('imagescr : %s', dict['imgURL'])


                        except Exception as e:
                            print(e)
                            crawler.info('%s的图片下载未成功',imagescr)
                            continue

                        yield scrapy.Request(url=dict['contenturl'], callback=self.parse_getcontent, dont_filter=True,
                                             meta={'item': dict})
                except Exception as e:
                    crawler.info('当前位置错误: %s', e)
                # try:
                #     lock = mp.Lock()
                #     self.pool.apply_async(self.gogetcontent, (lock, dict,), callback=self.getcontent)#lock,
                # except Exception as e:
                #     crawler.info('当前错误信息: %s', e)
        # self.pool.close()
        # self.pool.join


                # pool.map(self.gogetcontent, dict)

    # @staticmethod
    # def gogetcontent(lock,dic):#
    #     # try:
    #     html = requests.get(url=dic['contenturl']).text
    #     lock.acquire()
    #     dic['html'] = BeautifulSoup(html)
    #     lock.release()
    #     return dic
        # finally:

    def parse_getcontent(self, response):
        dic = response.meta['item']
        item = InformationAggregationItem()
        div = response.xpath('.//div[@class="newsContent"]')
        ps = div.xpath('.//p')
        if ps == []:
            ps = div.xpath('.//div/p')
        if ps == []:
            ps = response.xpath('.//div[@id="artibody"]/p')
        content = ''
        for p in ps:
            str = p.xpath('string(.)').extract_first()
            if str == None:
                continue
            else:
                try:
                    str = re.sub('\s', '', str)
                    str = str.strip('\t')
                    if str.find('文章来源') > 0:
                        textnum = str.rfind('：') + 1
                        item['source'] = str[textnum:len(str) - 1]
                        str = ''
                    elif str.rfind('责任编辑') > 0:
                        textnum = str.rfind('：') + 1
                        item['newsauth'] = str[textnum:len(str) - 1]
                        str = ''
                except:
                    a = 1
                if not str == '':
                    content += str + "\r\n"
        item['imgURL'] = dic['imgURL']
        crawler.info("imgURL:%s", item['imgURL'])
        item['content'] = content
        crawler.info("content:%s", content)
        title = dic['title']
        item['title'] = title
        crawler.info("title:%s", dic['title'])
        item['abstract'] = dic['abstract']
        crawler.info("abstract:%s", dic['abstract'])
        item['subtitle'] = title
        crawler.info("subtitle:%s", title)
        item['state'] = 0
        crawler.info("state:%s", item['state'])
        item['newstime'] = dic['newstime']
        crawler.info("newstime:%s", item['newstime'])
        item['datasource'] = '东方财富'
        crawler.info("datasource:%s", item['datasource'])
        hkey = "informationaggregation_filter"
        try:
            if self.server.hget(hkey, title) is None:
                self.server.hset(hkey, title, title)
                self.db['informationaggregation'].insert_one(dic(item))
        except Exception as e:
            crawler.into("本次东方财富存入失败原因:%s", e)
        # item['titletext'] = li.xpath('.//p[@class="title"]/a/text()').extract_first().strip()
        # crawler.info('titletext : %s', item['titletext'])

        #
        # item['localtime'] = time.strftime(self.ISOTIMEFORMAT, time.localtime())
        # crawler.info('localtime : %s', item['localtime'])
        # # item['datasource'] = "东方财富网"
        # item['titleurl'] = li.xpath('.//p[@class="title"]/a/@href').extract_first().strip()
        # crawler.info('titleurl : %s',item['titleurl'])
        #
        # if li.xpath('.//p[@class="info"]/@title').extract_first() == None or li.xpath('.//p[@class="info"]/@title').extract_first() == '':
        #     item['contenttitle'] = item['titletext']
        # else:
        #     item['contenttitle'] = li.xpath('.//p[@class="info"]/@title').extract_first().strip()
        # crawler.info('contenttitle : %s',item['contenttitle'])
        # if li.xpath('.//p[@class="info"]/text()').extract_first() == None or li.xpath('.//p[@class="info"]/text()').extract_first() == '':
        #     item['contenttext'] = item['contenttitle']
        # else :
        #     item['contenttext'] = li.xpath('.//p[@class="info"]/text()').extract_first().strip()
        # crawler.info('contenttext : %s',item['contenttext'])
        # item['time'] = li.xpath('.//p[@class="time"]/text()').extract_first().strip()
        # crawler.info('time : %s',item['time'])
        # item['imageurl'] = li.xpath('.//div[@class="image"]/a/@href').extract_first().strip()
        # crawler.info('imageurl : %s', item['imageurl'])
        # imagescr = li.xpath('.//div[@class="image"]/a/img/@src').extract_first().strip()
        # item['imagescr'] = imagescr#li.xpath('.//div[@class="image"]/a/img/@src').extract_first().strip()
        #
        # try:
        #     self.strwd = os.getcwd() + '\\image'
        #     if not os.path.isdir(self.strwd):
        #         os.mkdir('image')
        #     namenum = item['imagescr'].rfind('/') + 1
        #     self.namescr = imagescr[namenum:]
        #     # self.namescr = item['imagescr'][namenum:]
        #     urllib.request.urlretrieve(self.namescr, self.strwd + '\\' + self.namescr)
        #     text = gaia_upload_u('http://gress.gaiafintech.com/upload', imagescr)
        #     jsontext = json.loads(text)
        #     dfilesjson = jsontext['dfiles']
        #     if len(dfilesjson) > 0:
        #         item['imagescr'] = jsontext['dfiles']
        #     else:
        #         crawler.info('%s的图片未上传成功', item['titletext'])
        #         break
        #     crawler.info('imagescr : %s', item['imagescr'])
        #
        #
        # except Exception as e:
        #     print(e)
        #     crawler.info('%s的图片下载未成功',item['titletext'])
        #     continue
        #
        # yield item


    # def topost(self):
        # 在 urllib2 上注册 http 流处理句柄
        # register_openers()

        # 开始对文件 "DSC0001.jpg" 的 multiart/form-data 编码
        # "image1" 是参数的名字，一般通过 HTML 中的  标签的 name 参数设置

        # headers 包含必须的 Content-Type 和 Content-Length
        # datagen 是一个生成器对象，返回编码过后的参数
        # datagen, headers = request.post.encode.multipart_encode({"image1": open("DSC0001.jpg", "rb")})

        # 创建请求对象
        # request = urllib3.Request("http://localhost:5000/upload_image", datagen, headers)
        # 实际执行请求并取得返回
        # print(urllib3.urlopen(request).read())
        # try:
        #     #data = {'enctype': 'multipart/form-data', 'name': '11'}
        #
        #     url = 'http://gress.gaiafintech.com/upload'
        #     headers = {'content-type': "application/x-www-form-urlencoded",
        #                'gress_checker': '__gaiafintech__',
        #                "name": "test.file"}
        #
        #     files = {'img':open(self.strwd + '\\' + self.name,'rb')}
        #     reponse = requests.post(url,headers=headers, files = files)
        #     text = reponse.text
        #     print(text)
        # except Exception as e:
        #     print(e)


    # schedule.every(5).seconds.do(run)

if __name__ == '__main__':
    cmdline.execute("scrapy crawl EastMoneyNewsSpider".split())











