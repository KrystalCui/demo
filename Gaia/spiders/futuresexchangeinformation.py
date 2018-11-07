import scrapy
import json
from Gaia.items import FuturesExchangeItem
from Gaia.items import ContractSpecificationsItem
from scrapy import cmdline
from Gaia.logger import crawler
import schedule
from queue import Queue
import threading

class futuresexchangeinformation(scrapy.Spider):
    name = 'FuturesExchangeSpider'
    def __init__(self):
        self.pre = 'https://www.cmegroup.com'
        self.list = ['https://www.cmegroup.com/cn-s/trading/agricultural.html', 'https://www.cmegroup.com/cn-s/trading/metals.html',
                     'https://www.cmegroup.com/cn-s/trading/interest-rates.html', 'https://www.cmegroup.com/cn-s/trading/fx.html',
                     'https://www.cmegroup.com/cn-s/trading/equity-index.html', 'https://www.cmegroup.com/cn-s/trading/energy.html']
        self.suf = '_contract_specifications.html'
        # self.jobqueue = Queue.Queue()
        # self.baseurl = '/CmeWS/mvc/Quotes/FrontMonths?productIds=300,34,19,22,320,310,312,323,&venue=G&type=OPEN_INTEREST'

    def start_requests(self):
        # url = self.pre + self.baseurl
        # yield scrapy.Request(url=url, callback=self.parse_futures, dont_filter = True)
        for url in self.list:
            # url = self.list
            yield scrapy.Request(url=url, callback=self.parse_getbaseurl, dont_filter=True)

    def parse_getbaseurl(self, response):
        scri = response.xpath('.//div[@class="cmeDelayedQuotes section"]/script[3]/text()').extract_first()
        if len(scri) > 0:
            scrilist = scri.split(';')
            for scrieach in scrilist:
                if 'component.baseUrl' in scrieach:
                    baseurl = scrieach.split('="')[1].strip('"')
                    break
                else:
                    continue
        url = self.pre + baseurl
        yield scrapy.Request(url=url, callback=self.parse_futures, dont_filter=True)


    def parse_futures(self, response):
        contentaAll = json.loads(response.text)
        for each in contentaAll:
            item = FuturesExchangeItem()
            item['productId'] = each['productId']
            crawler.info('productId:%s', item['productId'])
            item['productName'] = each['productName']
            crawler.info('productName:%s', item['productName'])
            item['productCode'] = each['productCode']
            crawler.info('productCode:%s', item['productCode'])
            item['uri'] = each['uri']
            crawler.info('uri:%s', item['uri'])
            item['exchangeCode'] = each['exchangeCode']
            crawler.info('exchangeCode:%s', item['exchangeCode'])
            item['datasource'] = '芝商所'
            crawler.info('datasource:%s', item['datasource'])
            self.eachuri = each['uri'][:each['uri'].rfind('.')]
            url = self.pre + self.eachuri + self.suf
            yield scrapy.Request(url=url, callback=self.parse_contract_specifications, dont_filter=True)
            yield item

    def parse_contract_specifications(self, response):
        trs = response.xpath('.//tr')
        list = {}
        for tr in trs:
            trtext = tr.xpath('.//td[1]/text()').extract_first().strip()
            list.get(trtext)# = tr.xpath('.//tr[2]')
            if tr.xpath('.//td[2]/text()').extract_first() == None:
                list[trtext] = tr.xpath('.//td[2]/a/text()').extract_first().strip()
            else:
                list[trtext] = tr.xpath('.//td[2]/text()').extract_first().strip()
        item = ContractSpecificationsItem()

        item['productName'] = response.xpath('.//head/title/text()').extract_first().strip()
        crawler.info('productName:%s', item['productName'])
        if list.get('Contract Unit') != None and list.get('Contract Unit') != '':
            item['ContractUnit'] = list['Contract Unit']
            crawler.info('ContractUnit:%s', item['ContractUnit'])
        if list.get('Price Quotation') != None and list.get('Price Quotation') != '':
            item['PriceQuotation'] = list['Price Quotation']
            crawler.info('PriceQuotation:%s', item['PriceQuotation'])
        if list.get('Trading Hours') != None and list.get('Trading Hours') != '':
            item['TradingHours'] = list['Trading Hours']
            crawler.info('TradingHours:%s', item['TradingHours'])
        if list.get('Minimum Price Fluctuation') != None and list.get('Minimum Price Fluctuation') != '':
            item['MinimumPriceFluctuation'] = list['Minimum Price Fluctuation']
            crawler.info('MinimumPriceFluctuation:%s', item['MinimumPriceFluctuation'])
        if list.get('Product Code') != None and list.get('Product Code') != '':
            item['ProductCode'] = list['Product Code']
            crawler.info('ProductCode:%s', item['ProductCode'])
        if list.get('Listed Contracts') != None and list.get('Listed Contracts') != '':
            item['ListedContracts'] = list['Listed Contracts']
            crawler.info('ListedContracts:%s', item['ListedContracts'])
        if list.get('Settlement Method') != None and list.get('Settlement Method') != '':
            item['SettlementMethod'] = list['Settlement Method']
            crawler.info('SettlementMethod:%s', item['SettlementMethod'])
        if list.get('Termination Of Trading') != None and list.get('Termination Of Trading') != '':
            item['TerminationOfTrading'] = list['Termination Of Trading']
            crawler.info('TerminationOfTrading:%s', item['TerminationOfTrading'])
        if list.get('Trade At Marker Or Trade At Settlement Rules') != None and list.get('Trade At Marker Or Trade At Settlement Rules') != '':
            item['TradeAtMarkerOrTradeAtSettlementRules'] = list['Trade At Marker Or Trade At Settlement Rules']
            crawler.info('TradeAtMarkerOrTradeAtSettlementRules:%s', item['TradeAtMarkerOrTradeAtSettlementRules'])
        if list.get('Settlement Procedures') != None and list.get('Settlement Procedures') != '':
            item['SettlementProcedures'] = list['Settlement Procedures']
            crawler.info('SettlementProcedures:%s', item['SettlementProcedures'])
        if list.get('Position Limits') != None and list.get('Position Limits') != '':
            item['PositionLimits'] = list['Position Limits']
            crawler.info('PositionLimits:%s', item['PositionLimits'])
        if list.get('Exchange Rulebook') != None and list.get('Exchange Rulebook') != '':
            item['ExchangeRulebook'] = list['Exchange Rulebook']
            crawler.info('ExchangeRulebook:%s', item['ExchangeRulebook'])
        if list.get('Block Minimum') != None and list.get('Block Minimum') != '':
            item['BlockMinimum'] = list['Block Minimum']
            crawler.info('BlockMinimum:%s', item['BlockMinimum'])
        if list.get('Price Limit Or Circuit') != None and list.get('Price Limit Or Circuit') != '':
            item['PriceLimitOrCircuit'] = list['Price Limit Or Circuit']
            crawler.info('PriceLimitOrCircuit:%s', item['PriceLimitOrCircuit'])
        if list.get('Vendor Codes') != None and list.get('Vendor Codes') != '':
            item['VendorCodes'] = list['Vendor Codes']
            crawler.info('VendorCodes:%s', item['VendorCodes'])
        yield item

    def worker_main(self):
        while 1:
            job_func = self.jobqueue.get()
            job_func()

if __name__ == '__main__':
    # fu = futuresexchangeinformation()
    # schedule.every(5).seconds.do(fu.jobqueue, fu.start_requests)

    cmdline.execute("scrapy crawl FuturesExchangeSpider".split())
