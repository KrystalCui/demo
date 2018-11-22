import scrapy
from scrapy import cmdline
from Gaia.logger import crawler
from Gaia.items import DomesticCommodityExchangeItem

class ineoil(scrapy.Spider):
    name = 'ineoilspider'

    def __init__(self):
        self.url = 'http://www.ine.cn/products/oil/standard/text'

    def start_requests(self):
        yield scrapy.Request(url=self.url, callback=self.parse_ine, dont_filter=True)

    def parse_ine(self, response):
        dls = response.xpath('.//div[@class="details"]/dl')
        list = {}
        for dl in dls:
            try:
                textfirst = dl.xpath('.//dt/text()').extract_first().strip()
            except:
                textfirst = dl.xpath('.//dt/text()').extract_first()
            list.get(textfirst)
            try:
                list[textfirst] = dl.xpath('.//dd/text()').extract_first().strip()
            except:
                list[textfirst] = dl.xpath('.//dd/text()').extract_first()
        item = DomesticCommodityExchangeItem()
        item['datasource'] = '上海国际能源交易中心'
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
            if list.get('合约交割月份') != None and list.get('合约交割月份') != '':
                item['contractmonth'] = list['合约交割月份']
                crawler.info('合约交割月份:%s', item['contractmonth'])
            if list.get('交易时间') != None and list.get('交易时间') != '':
                item['tradingtime'] = list['交易时间']
                crawler.info('交易时间:%s', item['tradingtime'])
            if list.get('最后交易日') != None and list.get('最后交易日') != '':
                item['lastNoticeDay'] = list['最后交易日']
                crawler.info('最后交易日:%s', item['lastNoticeDay'])
            if list.get('交割品质') != None and list.get('交割品质') != '':
                item['deliveryGrade'] = list['交割品质']
                crawler.info('交割品质:%s', item['deliveryGrade'])
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
            if list.get('上市机构') != None and list.get('上市机构') != '':
                item['listingexchange'] = list['上市机构']
                crawler.info('上市机构:%s', item['listingexchange'])
            if list.get('交割日期') != None and list.get('交割日期') != '':
                item['deliverydate'] = list['交割日期']
                crawler.info('交割日期:%s', item['deliverydate'])

        except Exception as e:
            print(e)
        yield item

if __name__=="__main__":
    cmdline.execute("scrapy crawl ineoilspider".split())
