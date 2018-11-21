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
        hearder = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
            'Connection': 'keep-alive'}
        for url in self.list:
            # url = self.list
            yield scrapy.Request(url=url, callback=self.parse_getbaseurl, dont_filter=True, headers=hearder)

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
        hearder = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36', 'Connection':'keep-alive'}
        yield scrapy.Request(url=url, callback=self.parse_futures, dont_filter=True, headers=hearder)


    def parse_futures(self, response):
        contentaAll = json.loads(response.text)
        for each in contentaAll:
            self.eachuri = each['uri'][:each['uri'].rfind('.')]
            url = self.pre + '/cn-s' + self.eachuri + self.suf
            hearder = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
                'Connection': 'keep-alive'}
            yield scrapy.Request(url=url, callback=self.parse_contract_specifications, dont_filter=True,headers=hearder)
            # yield item

    def parse_contract_specifications(self, response):
        trs = response.xpath('.//tr')
        list = {}
        for tr in trs:
            trtext = ''
            if tr.xpath('.//td[1]/p/text()').extract_first() != None:
                trtext = tr.xpath('.//td[1]/p/text()').extract_first().strip()
            else:
                trtext = tr.xpath('.//td[1]/text()').extract_first().strip()
            list.get(trtext)# = tr.xpath('.//tr[2]')
            if tr.xpath('.//td[2]/p/text()').extract_first() != None:
                ps = tr.xpath('.//p')
                pstr = ''
                for p in ps:
                    pstr += p.xpath('text()').extract_first().strip()
                list[trtext] = pstr
            elif tr.xpath('.//td[2]/a/text()').extract_first() != None:
                list[trtext] = tr.xpath('.//td[2]/a/text()').extract_first().strip()
            elif tr.xpath('.//td[2]').extract_first() != None:
                list[trtext] = tr.xpath('.//td[2]/text()').extract_first().strip()
            else:
                list[trtext] = tr.xpath('.//th/text()').extract_first().strip()
            if tr.xpath('.//td[3]/text()').extract_first() != None:
                list[trtext] += tr.xpath('.//td[3]/text()').extract_first().strip()
            if 'CME ClearPort' in trtext:#trtext.rfind('CME Globex') > 0 or
                if trtext != '交易时间':
                    list['交易时间'] += '\n' + trtext + list[trtext]

        item = ContractSpecificationsItem()

        item['datasource'] = '芝商所'
        crawler.info('来源:%s', item['datasource'])
        productName = response.xpath('.//head/title/text()').extract_first().strip()

        namenum = productName.rfind('合约规格——芝商所')
        if namenum > 0:
            item['productName'] = productName[:namenum]
        else:
            item['productName'] = productName
        crawler.info('productName:%s', item['productName'])
        try:
            if list.get('合约规模') != None and list.get('合约规模') != '':
                item['ContractUnit'] = list['合约规模']
                crawler.info('合约规模:%s', item['ContractUnit'])
            if list.get('报价') != None and list.get('报价') != '':
                item['PriceQuotation'] = list['报价']
                crawler.info('报价:%s', item['PriceQuotation'])
            elif list.get('定价单位') != None and list.get('定价单位') != '':
                item['PriceQuotation'] = list['定价单位']
                crawler.info('定价单位:%s', item['PriceQuotation'])
            if list.get('交易时间') != None and list.get('交易时间') != '':
                item['TradingHours'] = list['交易时间']
                crawler.info('交易时间:%s', item['TradingHours'])
            if list.get('最小变动价位') != None and list.get('最小变动价位') != '':
                item['MinimumPriceFluctuation'] = list['最小变动价位']
                crawler.info('最小变动价位:%s', item['MinimumPriceFluctuation'])
            elif list.get('最小价格波幅') != None and list.get('最小价格波幅') != '':
                item['MinimumPriceFluctuation'] = list['最小价格波幅']
                crawler.info('最小价格波幅:%s', item['MinimumPriceFluctuation'])
            if list.get('产品代码') != None and list.get('产品代码') != '':
                num = -1
                if list['产品代码'].rfind('：') > 0:
                    num = list['产品代码'].rfind('：') + 1
                elif list['产品代码'].rfind(':') > 0:
                    num = list['产品代码'].rfind(':') + 1
                item['ProductCode'] = list['产品代码'][num:].strip()
                crawler.info('产品代码:%s', item['ProductCode'])
            elif list.get('商品代码') != None and list.get('商品代码') != '':
                num = -1
                if list['商品代码'].rfind('：') > 0:
                    num = list['商品代码'].rfind('：') + 1
                elif list['商品代码'].rfind(':') > 0:
                    num = list['商品代码'].rfind(':') + 1
                elif list['商品代码'].rfind('： ') > 0:
                    num = list['商品代码'].rfind('： ') + 1
                item['ProductCode'] = list['商品代码'][num:]
                crawler.info('商品代码:%s', item['ProductCode'])
            if list.get('上市合约') != None and list.get('上市合约') != '':
                item['ListedContracts'] = list['上市合约']
                crawler.info('上市合约:%s', item['ListedContracts'])
            if list.get('结算方法') != None and list.get('结算方法') != '':
                item['SettlementMethod'] = list['结算方法']
                crawler.info('结算方法:%s', item['SettlementMethod'])
            if list.get('交易终止') != None and list.get('交易终止') != '':
                item['TerminationOfTrading'] = list['交易终止']
                crawler.info('交易终止:%s', item['TerminationOfTrading'])
            if list.get('以市价或以结算价交易规则交易') != None and list.get('以市价或以结算价交易规则交易') != '':
                item['TradeAtMarkerOrTradeAtSettlementRules'] = list['以市价或以结算价交易规则交易']
                crawler.info('以市价或以结算价交易规则交易:%s', item['TradeAtMarkerOrTradeAtSettlementRules'])
            if list.get('结算程序') != None and list.get('结算程序') != '':
                item['SettlementProcedures'] = list['结算程序']
                crawler.info('结算程序:%s', item['SettlementProcedures'])
            if list.get('头寸限制') != None and list.get('头寸限制') != '':
                item['PositionLimits'] = list['头寸限制']
                crawler.info('头寸限制:%s', item['PositionLimits'])
            if list.get('交易规则手册') != None and list.get('交易规则手册') != '':
                item['ExchangeRulebook'] = list['交易规则手册']
                crawler.info('交易规则手册:%s', item['ExchangeRulebook'])
            elif list.get('交易所规则手册') != None and list.get('交易所规则手册') != '':
                item['ExchangeRulebook'] = list['交易所规则手册']
                crawler.info('交易所规则手册:%s', item['ExchangeRulebook'])
            if list.get('整批委托最低额') != None and list.get('整批委托最低额') != '':
                item['BlockMinimum'] = list['整批委托最低额']
                crawler.info('整批委托最低额:%s', item['BlockMinimum'])
            if list.get('价格限制或熔断') != None and list.get('价格限制或熔断') != '':
                item['PriceLimitOrCircuit'] = list['价格限制或熔断']
                crawler.info('价格限制或熔断:%s', item['PriceLimitOrCircuit'])
            if list.get('供应商报价代码') != None and list.get('供应商报价代码') != '':
                item['VendorCodes'] = list['供应商报价代码']
                crawler.info('供应商报价代码:%s', item['VendorCodes'])

        except Exception as e:
            print(e)
        yield item

    def worker_main(self):
        while 1:
            job_func = self.jobqueue.get()
            job_func()

if __name__ == '__main__':
    cmdline.execute("scrapy crawl FuturesExchangeSpider".split())
