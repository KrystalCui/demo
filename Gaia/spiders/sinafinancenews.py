# -*- coding: utf-8 -*-
import scrapy
from scrapy import cmdline
from Gaia.logger import crawler
from Gaia.items import SinaFinanceNewsItem


class SinaFinanceNews(scrapy.Spider):
    name="SinaFinanceNewsSpider"
    def __init__(self):
        self.url = 'http://finance.sina.com.cn/roll/index.d.html?cid=56995&page={}'

    def start_requests(self):
        for i in range(1,22,1):
            url = self.url.format(i)
            yield scrapy.Request(url=url, callback=self.parse_sinafinance, dont_filter = True)

    def parse_sinafinance(self, response):
        # crawler.info(response.read().decode('utf-8'))
        uls = response.xpath('.//ul[@class="list_009"]') #爬出来的数据是5个一组的
        for ul in uls:
            # print("aaa:" + a)
            # crawler.info(a.xpath('a/@href').extract())
            for j in range(1,5,1):

                item = SinaFinanceNewsItem()
                stra = str(j)
                strs = '[' + stra + ']'
                item['title'] = ul.xpath('.//li' + strs + '/a/text()').extract_first()
                # crawler.info("title:%s", item['title'])
                crawler.info(item['title'])
                item['time'] = ul.xpath('.//li' + strs + '/span/text()').extract_first()
                # crawler.info("time:%s", item['time'])
                crawler.info(item['time'])
                item['url'] = ul.xpath('.//li' + strs + '/a/@href').extract_first()
                # crawler.info("url:%s",item['url']).extract()
                crawler.info(item['url'])
                yield item
                j +=1

