import scrapy
# import win32com
from Gaia.items import *
from Gaia.logger.log import *
import urllib.request
import codecs

class InvestmentNewsSpider(scrapy.Spider):
    name="SevenTwentyFourNewsSpider"
    def __init__(self):
        url = 'http://newsapi.eastmoney.com/kuaixun/v1/getlist_102_ajaxResult_500_1_.html'
        self.pre_investmentnews = url
        request = urllib.request.Request(url)
        response = urllib.request.urlopen(request)
        self.str = response.read().decode("utf-8")


    def start_requests(self):
        # print("好好111")
        for i in range(1,2,1):
           url = self.pre_investmentnews.format(i)
           # crawler.info("")  #打印日志
           yield scrapy.Request(url = url, callback = self.parse_investment)

    #
    # def splitjsonstrs(self, response):
    #     divIds = response.xpath('.//div[@class="media-content"]')
    #     # print("好好22221")
    #     for divId in divIds:
    #         # divId2 = divId.xpath('/div[@class="media-content"]')
    #         # print("divId2" + divId2)
    #         # for divid in divId2:
    #         item = InvestmentNewsItem()
    #         item['title'] = divId.xpath('.//a[@class="media-title"]/text()').extract_first()
    #         if item['title'] is None:
    #             item['title'] = divId.xpath('.//span[@class="media-title"]/text()').extract_first()
    #         crawler.info('title:%s',item['title'] )
    #         item['time'] = divId.xpath('.//span[@class="time"]/text()').extract_first()
    #         crawler.info('time:%s',item['time'] )
    #         item['url'] = divId.xpath('.//a[@class="media-title"]/@href').extract_first()
    #         crawler.info('url:%s',item['url'] )
    #         item['commentcount'] = divId.xpath('.//span[3]/text()').extract_first()
            # yield item
            # print("title:" + item.title + "\ntime:" + item.time + "\ncommentcount:" + item.commentcount)
            #print(item)
            # print(item['title'])

    def parse_investment(self, response):
        listeachone = self.str.split('{')
        sizeeach = int(len(listeachone) - 1)
        i = 1
        print('parse_investment')
        while (i < sizeeach):
            # print("好好22221 + i" + i)
            listattribute = listeachone[i + 1].split(',')
            j = 0
            while (j < (len(listattribute) - 1)):
                listkeyvalue = listattribute[j].split(':')
                if len(listkeyvalue) > 0:
                    item = SevenTwentyFourNewsItem()
                    if listkeyvalue[0] == '"title"':
                        item['title'] = listkeyvalue[1][0:].strip('"')
                        crawler.info('title:%s', item['title'])
                        # print('title:%s'%item['title'])
                    if listkeyvalue[0] == '"simtitle"':
                        item['simtitle'] = listkeyvalue[1][0:].strip('"')
                        crawler.info('simtitle:%s', item['simtitle'])
                        # print('simtitle:%s'%item['simtitle'])
                    if listkeyvalue[0] == '"showtime"':
                        item['showtime'] = listkeyvalue[1][0:] + ":" + listkeyvalue[2] + ":" + listkeyvalue[3].strip('"')
                        crawler.info('showtime:%s', item['showtime'])
                        # print('showtime:%s' % item['showtime'])
                    if listkeyvalue[0] == '"id"':
                        item['_id'] = listkeyvalue[1][0:].strip('"')
                        crawler.info('_id:%s', item['_id'])
                        # print('_id:%s' % item['_id'])
                    if listkeyvalue[0] == '"commentnum"':
                        item['commentnum'] = listkeyvalue[1][0:].strip('"')
                        crawler.info('commentnum:%s', item['commentnum'])
                        # print('commentnum:%s' % item['commentnum'])
                    if listkeyvalue[0] == '"digest"':
                        item['digest'] = listkeyvalue[1][0:].strip('"')
                        crawler.info('digest:%s', item['digest'])
                        # print('digest:%s' % item['digest'])
                    if listkeyvalue[0] == '"simdigest"':
                        item['simdigest'] = listkeyvalue[1][0:].strip('"')
                        crawler.info('simdigest:%s', item['simdigest'])
                        # print('simdigest:%s' % item['simdigest'])
                j = j + 1
            i = i + 1
        yield item

