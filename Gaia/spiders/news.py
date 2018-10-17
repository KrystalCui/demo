import json
import logging
import random
import uuid
from urllib.parse import urlparse
from scrapy.selector import HtmlXPathSelector
from Gaia.scrapy_redis.spiders import RedisSpider

import scrapy
from scrapy import Spider

from Gaia.items import *
from Gaia.logger import crawler

logger = logging.getLogger('News')

class SinaSpider(RedisSpider):
	name = "News"
	redis_key='GaiaSpider_News:start_urls'
	rotete_user_agent = True

	#在关闭爬虫之前,保存资源
	def __init__(self):
		self.pre_url = 'http://finance.sina.com.cn/roll/index.d.html?cid=56995&page={}'
		self.urls = ['http://futures.hexun.com/domestic/']
		self.pre_investment_adviser = 'http://futures.hexun.com/domestic/index-{}.html'

	def start_requests(self):

		for url in self.urls:
			yield scrapy.Request(url = url, callback=self.parse)

		for i in range(1, 272, 1):
			url = self.pre_investment_adviser.format(i)
			yield scrapy.Request(url = url, callback=self.parse)

		for i in range(1, 100, 1):
			url = self.pre_url.format(i)
			yield scrapy.Request(url = url, callback=self.parse)

	def parse(self, response):
		crawler.info("response:%s", response)
		links = response.xpath("//@href").extract()
		for link in links:
			crawler.info("Link: %s", link)
			url = urlparse(link)
			crawler.info("url: %s", url)
			if url.netloc: #是一个 URL 而不是 "javascript:void(0)"
				if not url.scheme:
					link = "http:" + link
			if url.netloc == 'finance.sina.com.cn' :
				yield scrapy.Request (url=link , callback=self.parse_item)

			if url.netloc == 'futures.hexun.com':
				yield scrapy.Request (url=link , callback=self.parse_item)

	def parse_item(self , response):
		crawler.debug("parse_item response:%s", response)
		if not response.text or response.text == "":
			return
		parsed = urlparse(response.url)
		crawler.info("parse_item netloc: %s", parsed.netloc)
		crawler.info("parse_item path: %s", parsed.path)
		if '/money/future/fmnews' in parsed.path:
			crawler.info("/money/future/fmnews exists ")
			item = ParameterItem()
			crawler.info("parse_item url: %s", response.url)
			item['url'] = response.url
			title = response.xpath ('/html/body/div[2]/h1/text()').extract ()
			item['title'] = title[0]
			crawler.info("title: %s", item['title'])
			datetime = response.xpath('/html/body/div[2]/div[3]/div[1]/div[1]/div[2]/span/text()').extract()
			item['datetime'] = datetime[0]
			content = response.xpath ('//*[@id="artibody"]/p/text()').extract ()
			item['content'] = content
			item['source'] = '新浪财经'
			if item['title'] == "":
				return
			yield item

		elif 'futures/quotes' in parsed.path:
			crawler.info("futures/quotes exists ")
			item = F10Item()
			crawler.info("parse_item url: %s", response.url)

			underlyingIssueName = response.xpath ('//*[@id="table-futures-basic-data"]/tbody/tr[1]/td[1]/text()').extract ()
			item['underlyingIssueName'] = underlyingIssueName[0]
			crawler.info("underlyingIssueName: %s", item['underlyingIssueName'])

			priceTick = response.xpath ('//*[@id="table-futures-basic-data"]/tbody/tr[2]/td[1]/text()').extract ()
			item['priceTick'] = priceTick[0]
			crawler.info("priceTick: %s", item['priceTick'])

			exchangeDate = response.xpath ('//*[@id="table-futures-basic-data"]/tbody/tr[3]/td[1]/text()').extract ()
			item['exchangeDate'] = exchangeDate[0]
			crawler.info("exchangeDate: %s", item['exchangeDate'])

			underlyingIssueCode = response.xpath ('//*[@id="table-futures-basic-data"]/tbody/tr[4]/td[1]/text()').extract ()
			item['underlyingIssueCode'] = underlyingIssueCode[0]
			crawler.info("underlyingIssueCode: %s", item['underlyingIssueCode'])

			exchangeUnit = response.xpath ('//*[@id="table-futures-basic-data"]/tbody/tr[1]/td[2]/text()').extract ()
			item['exchangeUnit'] = exchangeUnit[0]
			crawler.info("exchangeUnit: %s", item['exchangeUnit'])

			upDownLimit = response.xpath ('//*[@id="table-futures-basic-data"]/tbody/tr[2]/td[2]/text()').extract ()
			item['upDownLimit'] = upDownLimit[0]
			crawler.info("upDownLimit: %s", item['upDownLimit'])

			deliveryGrade = response.xpath ('//*[@id="table-futures-basic-data"]/tbody/tr[3]/td[2]/text()').extract ()
			item['deliveryGrade'] = deliveryGrade[0]
			crawler.info("deliveryGrade: %s", item['deliveryGrade'])

			tradeMarket = response.xpath ('//*[@id="table-futures-basic-data"]/tbody/tr[4]/td[2]/text()').extract ()
			item['tradeMarket'] = tradeMarket[0]
			crawler.info("tradeMarket: %s", item['tradeMarket'])

			tickUnit = response.xpath ('//*[@id="table-futures-basic-data"]/tbody/tr[1]/td[3]/text()').extract ()
			item['tickUnit'] = tickUnit[0]
			crawler.info("tickUnit: %s", item['tickUnit'])

			deliveryDate = response.xpath ('//*[@id="table-futures-basic-data"]/tbody/tr[2]/td[3]/text()').extract ()
			item['deliveryDate'] = deliveryDate[0]
			crawler.info("deliveryDate: %s", item['deliveryDate'])

			deliveryAddress = response.xpath ('//*[@id="table-futures-basic-data"]/tbody/tr[3]/td[3]/text()').extract ()
			item['deliveryAddress'] = deliveryAddress[0]
			crawler.info("deliveryAddress: %s", item['deliveryAddress'])

			additionalInfo = response.xpath ('//*[@id="table-futures-basic-data"]/tbody/tr[4]/td[3]/text()').extract ()
			item['additionalInfo'] = additionalInfo[0]
			crawler.info("additionalInfo: %s", item['additionalInfo'])
			if item['underlyingIssueName'] == "":
				return
			yield item

		elif '/201' in parsed.path:
			crawler.info("/201 exist ")
			crawler.info("parse_item url: %s", response.url)
			item = InvestmentAdviserItem()
			item['url'] = response.url
			title = response.xpath ('/html/body/div[6]/h1/text()').extract ()
			item['title'] = title[0]
			crawler.info("title: %s", item['title'])
			datetime = response.xpath('/html/body/div[6]/div/div[1]/span/text()').extract()
			item['datetime'] = datetime[0]
			crawler.info("datetime: %s", item['datetime'])
			content = response.xpath ('/html/body/div[7]/div[1]/div[1]/div[1]/p/text()').extract ()
			item['content'] = content
			crawler.info("content: %s", item['content'])
			item['source'] = '和讯网'
			if item['title'] == "":
				return
			yield item
			return