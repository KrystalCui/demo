import scrapy
from Gaia.items import NewsItem
from Gaia.logger import crawler
import urllib.request
import os
from Gaia.gaiaupslpy import *
import time
import json


class EastMoneyNewsSpider(scrapy.Spider):
    name = "EastMoneyNewsSpider"
    def __init__(self):
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
                item = NewsItem()
                item['localtime'] = time.strftime(self.ISOTIMEFORMAT, time.localtime())
                crawler.info('localtime : %s', item['localtime'])
                item['datasource'] = "东方财富网"
                item['titleurl'] = li.xpath('.//p[@class="title"]/a/@href').extract_first().strip()
                crawler.info('titleurl : %s',item['titleurl'])
                item['titletext'] = li.xpath('.//p[@class="title"]/a/text()').extract_first().strip()
                crawler.info('titletext : %s',item['titletext'])
                if li.xpath('.//p[@class="info"]/@title').extract_first() == None or li.xpath('.//p[@class="info"]/@title').extract_first() == '':
                    item['contenttitle'] = item['titletext']
                else:
                    item['contenttitle'] = li.xpath('.//p[@class="info"]/@title').extract_first().strip()
                crawler.info('contenttitle : %s',item['contenttitle'])
                if li.xpath('.//p[@class="info"]/text()').extract_first() == None or li.xpath('.//p[@class="info"]/text()').extract_first() == '':
                    item['contenttext'] = item['contenttitle']
                else :
                    item['contenttext'] = li.xpath('.//p[@class="info"]/text()').extract_first().strip()
                crawler.info('contenttext : %s',item['contenttext'])
                item['time'] = li.xpath('.//p[@class="time"]/text()').extract_first().strip()
                crawler.info('time : %s',item['time'])
                item['imageurl'] = li.xpath('.//div[@class="image"]/a/@href').extract_first().strip()
                crawler.info('imageurl : %s', item['imageurl'])
                imagescr = li.xpath('.//div[@class="image"]/a/img/@src').extract_first().strip()
                item['imagescr'] = imagescr#li.xpath('.//div[@class="image"]/a/img/@src').extract_first().strip()

                try:
                    self.strwd = os.getcwd() + '\\image'
                    if not os.path.isdir(self.strwd):
                        os.mkdir('image')
                    namenum = item['imagescr'].rfind('/') + 1
                    self.namescr = imagescr[namenum:]
                    self.namescr = item['imagescr'][namenum:]
                    urllib.request.urlretrieve(item['imagescr'], self.strwd + '\\' + self.namescr)
                    text = gaia_upload_u('http://gress.gaiafintech.com/upload', imagescr)
                    jsontext = json.loads(text)
                    dfilesjson = jsontext['dfiles']
                    if len(dfilesjson) > 0:
                        item['imagescr'] = jsontext['dfiles']
                    else:
                        crawler.info('%s的图片未上传成功', item['titletext'])
                        break
                    crawler.info('imagescr : %s', item['imagescr'])


                except Exception as e:
                    print(e)
                    crawler.info('%s的图片下载未成功',item['titletext'])
                    continue

                yield item

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













