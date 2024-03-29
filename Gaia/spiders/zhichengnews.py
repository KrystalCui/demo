import scrapy
from Gaia.items import NewsItem
from Gaia.logger import crawler
import urllib.request
import os
import urllib3
import requests
from Gaia.gaiaupslpy import *
import subprocess
import time
from subprocess import Popen
import schedule
import json
from scrapy import cmdline

class ZhiChengNewsSpider(scrapy.Spider):
    name = "至诚财经"
    def __init__(self):
        self.url = 'http://www.zhicheng.com/index.php?m=seahot&c=index&a=get_more_list&page={}&pagesize=20'
        self.ISOTIMEFORMAT = '%Y-%m-%d %X'

    def start_requests(self):
        for i in range(536, 10000, 1):
            url = self.url.format(i)
            yield scrapy.Request(url=url, callback= self.parse_zhichengnews, dont_filter = True)

    def parse_zhichengnews(self, response):
        crawler.info('ZhiChengNewsSpider parse_zhichengnews:%s', response)
        try:
            content = response.body.decode("utf-8")
            strLength = len(content)
            jsoncotent = json.loads(content[1:strLength-1])
            for each in jsoncotent['data']:
                item = NewsItem()
                item['titleurl'] = each['url']
                item['datasource'] = "至诚财经"
                item['imagescr'] = each['thumb']
                item['imageurl'] = each['thumb']
                item['titletext'] = each['title']
                item['contenttitle'] = each['description']
                item['contenttext'] = each['description']
                item['time'] = each['updatetime']
                imagescr = item['imagescr']

                try:
                    self.strwd = os.getcwd() + '\\image'
                    if not os.path.isdir(self.strwd):
                        os.mkdir('image')
                    namenum = item['imagescr'].rfind('/') + 1
                    self.name = item['imagescr'][namenum:]
                    urllib.request.urlretrieve(item['imagescr'], self.strwd + '\\' + self.name)
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

                item['localtime'] = time.strftime(self.ISOTIMEFORMAT, time.localtime())
                crawler.info('ZhiChengNewsSpider localtime : %s', item['localtime'])

                crawler.info('ZhiChengNewsSpider url:%s', item['titleurl'])
                crawler.info('ZhiChengNewsSpider datasource:%s', item['datasource'])
                yield item

        except Exception as e:
            crawler.info('ZhiChengNewsSpider error %s:', e)

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

if __name__ == '__main__':
    cmdline.execute("scrapy crawl 至诚财经".split())
    # schedule.every(5).seconds.do(run)













