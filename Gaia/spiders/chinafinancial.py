import scrapy
from scrapy import cmdline
from Gaia.items import DomesticCommodityExchangeItem
from Gaia.logger import crawler

class chinafinancial(scrapy.Spider):
    name = '中国金融期货交易所F10资料(请勿多次爬取)'

    def __init__(self):
        self.urlpre = 'http://www.cffex.com.cn'

    def start_requests(self):
        yield scrapy.Request(url=self.urlpre, callback=self.parse_chinafinancial, dont_filter=True)

    def parse_chinafinancial(self, response):
        # 获取到产品左右两边的list
        divs = response.xpath('.//ul[@class="nav_ul"]/li[3]/div')  # /div[1]/a[1]/@href').extract_first()
        for div in divs:
            a_s = div.xpath('.//a')
            for a in a_s:
                href = a.xpath('@href').extract_first()
                url = self.urlpre + href
                yield scrapy.Request(url=url, callback=self.parse_chinafinancialF10, dont_filter=True)

    def parse_chinafinancialF10(self, response):
        trs = response.xpath('.//div[@class="table_introduction debt_table_introduction"]/table/tbody/tr')
        list = {}
        for tr in trs:
            #提取信息，提取后返回的类型由SelectorList转成list，list可以由len(list)获取其长度
            tds = tr.xpath('.//td')
            tdlen = len(tds.extract())
            #一般情况下一行四列，两组
            if tdlen == 4:
                try:
                    textfirst = tds[0].xpath('text()').extract_first().strip()
                except:
                    textfirst = tds[0].xpath('text()').extract_first()
                list.get(textfirst)
                try:
                    list[textfirst] = tds[1].xpath('text()').extract_first().strip()
                except:
                    list[textfirst] = tds[1].xpath('text()').extract_first()
                textfirst = tds[2].xpath('text()').extract_first()
                list.get(textfirst)
                list[textfirst] = tds[3].xpath('text()').extract_first()
            else:
                text = ''
                for td in tds:
                    text += td.xpath('text()').extract_first()
                crawler.info(text, '未存入数据库信息，请核对')
        item = DomesticCommodityExchangeItem()
        item['datasource'] = '中国金融期货交易所'
        try:
            if list.get('合约标的') != None and list.get('合约标的') != '':
                item['tradingvariety'] = list['合约标的']
                crawler.info('合约标的:%s', item['tradingvariety'])
            if list.get('报价单位') != None and list.get('报价单位') != '':
                item['quotationunit'] = list['报价单位']
                crawler.info('报价单位:%s', item['quotationunit'])
            if list.get('最小变动价位') != None and list.get('最小变动价位') != '':
                item['minimumpricechange'] = list['最小变动价位']
                crawler.info('最小变动价位:%s', item['minimumpricechange'])
            if list.get('每日价格最大波动限制') != None and list.get('每日价格最大波动限制') != '':
                item['pricelimits'] = list['每日价格最大波动限制']
                crawler.info('每日价格最大波动限制:%s', item['pricelimits'])
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
            if list.get('可交割国债') != None and list.get('可交割国债') != '':
                item['deliverablenationaldebt'] = list['可交割国债']
                crawler.info('可交割国债:%s', item['deliverablenationaldebt'])
            if list.get('报价方式') != None and list.get('报价方式') != '':
                item['quotationmethod'] = list['报价方式']
                crawler.info('报价方式:%s', item['quotationmethod'])
            if list.get('交割日期') != None and list.get('交割日期') != '':
                item['deliverydate'] = list['交割日期']
                crawler.info('交割日期:%s', item['deliverydate'])
            if list.get('合约乘数') != None and list.get('合约乘数') != '':
                item['tradingunit'] = list['合约乘数']
                crawler.info('合约乘数:%s', item['tradingunit'])
            if list.get('最后交易日交易时间') != None and list.get('最后交易日交易时间') != '':
                item['lasttradingdaytradingtime'] = list['最后交易日交易时间']
                crawler.info('最后交易日交易时间:%s', item['lasttradingdaytradingtime'])

        except Exception as e:
            print(e)
        yield item

if __name__ == "__main__":
    cmdline.execute("scrapy crawl 中国金融期货交易所F10资料(请勿多次爬取)".split())