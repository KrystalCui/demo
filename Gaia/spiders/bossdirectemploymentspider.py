import logging

from Gaia.items import *
from Gaia.logger import crawler
import scrapy
from scrapy import Spider
from scrapy.selector import HtmlXPathSelector

logger = logging.getLogger('BossDirectEmploymentSpider')

class BossDirectEmploymentSpider(scrapy.Spider):
	name = "BossDirectEmploymentSpider"
	rotete_user_agent = True

	#在关闭爬虫之前,保存资源
	def __init__(self):
		self.start_url = 'https://www.zhipin.com/c101020100/?page=1&ka=page-1'

	def start_requests(self):
		crawler.info("start_url:%s", self.start_url)
		yield scrapy.Request(url=self.start_url, callback=self.parse)

	def parse(self, response):
		crawler.info("response:%s", response)
		job_list = response.css('div.job-list > ul > li')
		for job in job_list:
			crawler.info('parse:' + job)
			href = item.xpath('.//h3[@class="name"]/h2/a/@href').extract()
			href = 'https://www.zhipin.com' + href[0];
			crawler.info("herf:%s", href)
			yield scrapy.Request(url=href, callback=self.parse_item)

	def parse_item(self, response):
		crawler.info("parse_item response:%s", response)
		if not response.text or response.text == "":
			return