import scrapy
from Gaia.items import StockNewsItem
from Gaia.logger import crawler
import time
import numpy as np
import json
from scrapy import cmdline
from Gaia.stocks import stockNames

class EastMoneyStockNewsSpider(scrapy.Spider):
    name = "EastMoneyStockNewsSpider"
    def __init__(self):
        self.url = 'http://api.so.eastmoney.com/bussiness/Web/GetSearchList?type=20&pageindex={1}&pagesize=20&keyword={0}'
        self.ISOTIMEFORMAT = '%Y-%m-%d %X'

    def start_requests(self):
        for stockName in stockNames:
            for index in range(1, 10, 1):
                url = self.url.format(stockName, index)
                time.sleep(np.random.rand() * 5)
                yield scrapy.Request(url=url, callback= self.parse_eastmoneystocknews, dont_filter = True)

    def parse_eastmoneystocknews(self, response):
        crawler.info('EastMoneyStockNewsSpider parse_eastmoneystocknews:%s', response)
        try:
            content = response.body.decode("utf-8")
            if '未查询到数据' in content:
                yield

            jsoncotent = json.loads(content)
            stockname = jsoncotent['Keyword']
            for each in jsoncotent['Data']:
                item = StockNewsItem()
                item['arttitle'] = each['Art_Title']
                item['datasource'] = "东方财富网"
                item['arturl'] = each['Art_Url']
                item['artcreateTime'] = each['Art_CreateTime']
                item['artcontent'] = each['Art_Content']
                item['stockname'] = stockname

                item['localtime'] = time.strftime(self.ISOTIMEFORMAT, time.localtime())
                crawler.info('EastMoneyStockNewsSpider localtime : %s', item['localtime'])

                crawler.info('EastMoneyStockNewsSpider url:%s', item['arttitle'])
                crawler.info('EastMoneyStockNewsSpider datasource:%s', item['datasource'])
                yield item

        except Exception as e:
            crawler.info('EastMoneyStockNewsSpider error %s:', e)

if __name__ == '__main__':
    cmdline.execute("scrapy crawl EastMoneyStockNewsSpider".split())
    # schedule.every(5).seconds.do(run)













