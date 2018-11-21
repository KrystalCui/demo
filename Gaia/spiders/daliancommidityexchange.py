# -*- encoding = utf-8 -*-
import scrapy
from scrapy import cmdline
import json
from Gaia.logger import crawler
from Gaia.items import DalianCommodityExchangeItem

class daliancommodityexchange(scrapy.Spider):
    name = "DaLianCommodityExchangeSpider"
    def __init__(self):
        self.url = 'http://www.dce.com.cn/dalianshangpin/dalianshangpin_PAGE_KEY/index.html'
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36'}
        self.urlpre = "http://www.dce.com.cn"

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse_daliancommodity, headers=self.headers, dont_filter=True)

    def parse_daliancommodity(self,response):
        # lis = response.xpath('.//div[@class="header"]').xpath('.//ul/li')
        divs = response.xpath('.//div[@class="pzzx_left"]/div')
        for diveach in divs:
            lis = diveach.xpath('.//ul/li')
            for li in lis:
                # print(lis)
                # for li in lis:
                ahref = li.xpath('.//a/@href').extract_first()
                url = self.urlpre + ahref
                # print('parse_daliancommodity  url :%s' % url)
                yield scrapy.Request(url=url, callback=self.parse_daliancode, headers=self.headers, dont_filter=True)

    def parse_daliancode(self,response):#.//div[@id="list_type"]/div/div[2]/ul/li[1]/a/@href
        try:
            ahref = response.xpath('.//div[@id="list_type"]/div/div[2]/ul/li[1]/a/@href').extract_first()
            url = self.urlpre + ahref
            # print('parse_daliancode  url :%s'%url)
            yield scrapy.Request(url=url, callback=self.parse_daliancodedetails, headers=self.headers, dont_filter=True)
        except Exception as e:
            print(e)

    def parse_daliancodedetails(self, response):
        divzoom = response.xpath('.//div[@id="zoom"]')
        tableout = divzoom.xpath('.//table')
        list = {}
        try:
            if tableout.xpath('.//table') == None or tableout.xpath('.//table') == []:
                trs = tableout.xpath('.//tr')
                for tr in trs:
                    textstr = ''
                    td1 = tr.xpath('.//td[1]')
                    if td1.xpath('.//text()') != None:
                        textstr = td1.xpath('.//text()').extract_first().strip()
                    list.get(textstr)
                    td2 = tr.xpath('.//td[2]')
                    if td2.xpath('.//text()') != None:
                        list[textstr] = td2.xpath('.//text()').extract_first().strip()
            else:
                tabelbody = tableout.xpath('.//table')
                trs = tabelbody.xpath('.//tr')
                for tr in trs:
                    textstr = ''
                    td1 = tr.xpath('.//td[1]')
                    if td1.xpath('.//text()') != None:
                        textstr = td1.xpath('.//text()').extract_first().strip()
                    list.get(textstr)
                    td2 = tr.xpath('.//td[2]')
                    if td2.xpath('.//text()') != None:
                        list[textstr] = td2.xpath('.//text()').extract_first().strip()
        except Exception as e:
            print(e)
        item = DalianCommodityExchangeItem()
        item['datasource'] = '大连商品交易所'
        try:
            if list.get('交易品种') != None and list.get('交易品种') != '':
                item['tradingvariety'] = list['交易品种']
                crawler.info('交易品种:%s', item['tradingvariety'])
            if list.get('交易单位') != None and list.get('交易单位') != '':
                item['tradingunit'] = list['交易单位']
                crawler.info('交易单位:%s', item['tradingunit'])
            if list.get('报价单位') != None and list.get('报价单位') != '':
                item['quotationunit'] = list['报价单位']
                crawler.info('报价单位:%s', item['quotationunit'])
            if list.get('最小变动价位') != None and list.get('最小变动价位') != '':
                item['minimumpricechange'] = list['最小变动价位']
                crawler.info('最小变动价位:%s', item['minimumpricechange'])
            if list.get('涨跌停板幅度') != None and list.get('涨跌停板幅度') != '':
                item['pricelimits'] = list['涨跌停板幅度']
                crawler.info('涨跌停板幅度:%s', item['pricelimits'])
            if list.get('合约月份') != None and list.get('合约月份') != '':
                item['contractmonth'] = list['合约月份']
                crawler.info('合约月份:%s', item['contractmonth'])
            if list.get('交易时间') != None and list.get('交易时间') != '':
                item['tradingtime'] = list['交易时间']
                crawler.info('交易时间:%s', item['tradingtime'])
            if list.get('最后交易日') != None and list.get('最后交易日') != '':
                item['lastNoticeDay'] = list['最后交易日']
                crawler.info('最后交易日:%s', item['lastNoticeDay'])
            if list.get('最后交割日') != None and list.get('最后交割日') != '':
                item['finaldeliverydate'] = list['最后交割日']
                crawler.info('最后交割日:%s', item['finaldeliverydate'])
            if list.get('交割等级') != None and list.get('交割等级') != '':
                item['deliveryGrade'] = list['交割等级']
                crawler.info('交割等级:%s', item['deliveryGrade'])
            if list.get('交割地点') != None and list.get('交割地点') != '':
                item['deliverypoints'] = list['交割地点']
                crawler.info('交割地点:%s', item['deliverypoints'])
            if list.get('最低交易保证金') != None and list.get('最低交易保证金') != '':
                item['minimumtransactionmargin'] = list['最低交易保证金']
                crawler.info('最低交易保证金:%s', item['minimumtransactionmargin'])
            if list.get('交割方式') != None and list.get('交割方式') != '':
                item['deliverymethods'] = list['交割方式']
                crawler.info('交割方式:%s', item['deliverymethods'])
            if list.get('交易代码') != None and list.get('交易代码') != '':
                item['transactioncode'] = list['交易代码']
                crawler.info('交易代码:%s', item['transactioncode'])
            if list.get('上市交易所') != None and list.get('上市交易所') != '':
                item['listingexchange'] = list['上市交易所']
                crawler.info('上市交易所:%s', item['listingexchange'])
            if list.get('容重') != None and list.get('容重') != '':
                item['bulkdensity'] = list['容重']
                crawler.info('容重:%s', item['bulkdensity'])
            if list.get('总量') != None and list.get('总量') != '':
                item['total'] = list['总量']
                crawler.info('总量:%s', item['total'])
            if list.get('项目') != None and list.get('项目') != '':
                item['project'] = list['项目']
                crawler.info('项目:%s', item['project'])

        except Exception as e:
            print(e)
        yield item



if __name__=="__main__":
    cmdline.execute("scrapy crawl DaLianCommodityExchangeSpider".split())
