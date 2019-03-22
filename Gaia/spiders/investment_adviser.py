import json
import logging
import random
import uuid
from urllib.parse import urlparse
from scrapy.selector import HtmlXPathSelector

import scrapy
from scrapy import Spider

from Gaia.items import *
from Gaia.logger import crawler

logger = logging.getLogger('InvestmentAdviserSpider')

class InvestmentAdviserSpider(scrapy.Spider):
	name = "投资顾问(和讯网)"
	rotete_user_agent = True

	#在关闭爬虫之前,保存资源
	def __init__(self):
		self.pre_investment_adviser = 'http://futures.hexun.com/domestic/index-{}.html'

	def start_requests(self):
		for i in range(1, 2, 1):
			url = self.pre_investment_adviser.format(i)
			crawler.info("start_requests url: %s", url)
			yield scrapy.Request(url = url, callback=self.parse_investment_adviser)

	def parse_investment_adviser(self, response):
		crawler.info("parse_investment_adviser response:%s", response)
		links = response.xpath("//@href").extract()
		crawler.info("parse_investment_adviser links:%s", links)
		for link in links:
			crawler.info("Link: %s", link)
			url = urlparse(link)
			crawler.info("url: %s", url)
			if url.netloc: #是一个 URL 而不是 "javascript:void(0)"
				if not url.scheme:
					link = "http:" + link

			if url.netloc == 'futures.hexun.com':
				yield scrapy.Request (url=link , callback=self.parse_investment_adviser_item)

	def parse_investment_adviser_item(self, response):
		crawler.info("parse_investment_adviser_item response:%s", response)
		if not response.text or response.text == "":
			return
		parsed = urlparse(response.url)
		if '/201' in parsed.path:
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