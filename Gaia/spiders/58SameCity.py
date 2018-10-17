import json
import logging
import random
import uuid
from urllib.parse import urlparse

import scrapy
from scrapy import Spider
from scrapy.selector import HtmlXPathSelector
from Gaia.scrapy_redis.spiders import RedisSpider

from Gaia.items import *
from Gaia.logger import crawler

logger = logging.getLogger('58SameCity')

class SameCity58Spider(RedisSpider):
	name = "58SameCity"
	redis_key = "GaiaSpider_58SameCity:start_urls"
	rotete_user_agent = True
	start_urls = 'https://sh.58.com/zufang/0/j1/'

	def start_requests(self):
		crawler.info("start_requests:%s", 11111)
		yield scrapy.Request(url=self.start_urls, callback=self.parse)

	def parse(self, response):
		crawler.info("start_requests:%s", 22222)
		crawler.info("response:%s", response)
		item = CourseItem()
		for box in response.xpath('//ul[@class="listUl"]/li'):
			href = box.xpath('.//div[@class="des"]/h2/a[@class="strongbox"]/@href').extract()
			href = 'https:' + href[0];
			crawler.info("herf:%s", href)
			yield scrapy.Request(url=href, callback=self.parse_item)

		next_page = response.xpath(
				'.//[@id="bottom_ad_li"]/div[@class="pager"]/a/@href').extract_first()
		crawler.info("next_page:%s", next_page)
		if next_page:
			next_page = response.urljoin(str(next_page))
			yield scrapy.Request(next_page, callback=self.parse)
		else:
			print(None)

	def parse_item(self, response):
		crawler.info("parse_item response:%s", response)
		if not response.text or response.text == "":
			return