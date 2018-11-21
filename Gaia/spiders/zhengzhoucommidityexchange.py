import scrapy
from scrapy import cmdline
from Gaia.items import DomesticCommodityExchangeItem
from Gaia.logger import crawler

class zhengzhoucommidityexchange(scrapy.Spider):
    name = "zhengzhoucommidityexchangespider"

    def __init__(self):
        self.urlpre = "http://www.czce.com.cn"

    def start_requests(self):
        url = self.urlpre
        yield scrapy.Request(url=url, callback=self.parse_zhengzhoucommidity, dont_filter=True)

    def parse_zhengzhoucommidity(self, response):
        #农产品
        aes_top = response.xpath('.//div[@class="topnypz"]/ul/li/a')
        #非农产品
        aes_f = response.xpath('.//div[@class="fnypz"]/ul/li/a')
        #期权产品
        #aes_qq = response.xpath('.//div[@class="qqcp"]/ul/li/a')
        for a_top in aes_top:
            url = self.urlpre + a_top.xpath('@href').extract_first()
            yield scrapy.Request(url=url, callback=self.parse_code, dont_filter=True)
        for a_f in aes_f:
            url = self.urlpre + a_f.xpath('@href').extract_first()
            yield scrapy.Request(url=url, callback=self.parse_code, dont_filter=True)

        # for a_qq in aes_qq:
        #     url = self.urlpre + a_qq.xpath('@href').extract_first()
        #     yield scrapy.Request(url=url, callback=self.parse_code, dont_filter=True)

    def parse_code(self, response):
        #divtable = response.xpath('.//div[@id="BodyLabel"]')
        trs = response.xpath('.//table/tbody/tr')
        list = {}
        textfirst =''
        try:
            for tr in trs:
                #print(tr.xpath('.//td').extract_first())
                if tr.xpath('.//td[2]').extract_first() != None:
                    #print(tr.xpath('.//td[2]').extract_first())
                    if tr.xpath('.//td[1]/p/text()') != None and tr.xpath('.//td[1]/p/text()') != []:
                        #print(type(tr.xpath('.//td[1]/p/text()')))
                        try:
                            textfirst = tr.xpath('.//td[1]/p/text()').extract_first().strip()
                        except:
                            textfirst = tr.xpath('.//td[1]/p/text()').extract_first()

                    elif tr.xpath('.//td[1]/text()') != None and tr.xpath('.//td[1]/text()') != []:
                        try:
                            textfirst = tr.xpath('.//td[1]/text()').extract_first().strip()
                        except:
                            textfirst = tr.xpath('.//td[1]/text()').extract_first()
                    list.get(textfirst)
                    if tr.xpath('.//td[2]/p') != None and tr.xpath('.//td[2]/p') != []:
                        ps = tr.xpath('.//td[2]/p')
                        list[textfirst] = ''
                        for p in ps:
                            try:
                                list[textfirst] += p.xpath('text()').extract_first().strip()
                            except:
                                list[textfirst] += p.xpath('text()').extract_first()
                    elif tr.xpath('.//td[2]/text()') != None and tr.xpath('.//td[2]/text()') != []:
                        try:
                            list[textfirst] = tr.xpath('.//td[2]/text()').extract_first().strip()
                        except:
                            list[textfirst] = tr.xpath('.//td[2]/text()').extract_first()
                else:
                    continue
            item = DomesticCommodityExchangeItem()
            item['datasource'] = '郑州商品交易所'

            if list.get('交易品种') != None and list.get('交易品种') != '':
                item['tradingvariety'] = list['交易品种']
                crawler.info('交易品种:%s', item['tradingvariety'])
            if list.get('交易单位') != None and list.get('交易单位') != '':
                item['tradingunit'] = list['交易单位']
                crawler.info('交易单位:%s', item['tradingunit'])
            if list.get('交易') != None and list.get('交易') != '':
                item['tradingunit'] = list['交易']
                crawler.info('交易:%s', item['tradingunit'])
            if list.get('报价单位') != None and list.get('报价单位') != '':
                item['quotationunit'] = list['报价单位']
                crawler.info('报价单位:%s', item['quotationunit'])
            if list.get('最小变动价位') != None and list.get('最小变动价位') != '':
                item['minimumpricechange'] = list['最小变动价位']
                crawler.info('最小变动价位:%s', item['minimumpricechange'])
            if list.get('每日价格波动限制') != None and list.get('每日价格波动限制') != '':
                item['pricelimits'] = list['每日价格波动限制']
                crawler.info('每日价格波动限制:%s', item['pricelimits'])
            elif list.get('每日价格最大波动限制') != None and list.get('每日价格最大波动限制') != '':
                item['pricelimits'] = list['每日价格最大波动限制']
                crawler.info('每日价格最大波动限制:%s', item['pricelimits'])
            if list.get('合约交割月份') != None and list.get('合约交割月份') != '':
                item['contractmonth'] = list['合约交割月份']
                crawler.info('合约交割月份:%s', item['contractmonth'])
            if list.get('交易时间') != None and list.get('交易时间') != '':
                item['tradingtime'] = list['交易时间']
                crawler.info('交易时间:%s', item['tradingtime'])
            if list.get('最后交易日') != None and list.get('最后交易日') != '':
                item['lastNoticeDay'] = list['最后交易日']
                crawler.info('最后交易日:%s', item['lastNoticeDay'])
            if list.get('最后交割日') != None and list.get('最后交割日') != '':
                item['finaldeliverydate'] = list['最后交割日']
                crawler.info('最后交割日:%s', item['finaldeliverydate'])
            if list.get('交割品级') != None and list.get('交割品级') != '':
                item['deliveryGrade'] = list['交割品级']
                crawler.info('交割品级:%s', item['deliveryGrade'])
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
            yield item

        except Exception as e:
            crawler.info("当前错误信息: ", e)

if __name__ == '__main__':
    cmdline.execute("scrapy crawl zhengzhoucommidityexchangespider".split())


