import scrapy
from Gaia.items import QQFinanceItem
from Gaia.logger import crawler
import os
import urllib.request
from scrapy import cmdline

class QQFinance(scrapy.Spider):
    name = "QQFinanceSpider"
    def __init__(self):
        self.url = 'https://new.qq.com/ch/finance/'

    def start_requests(self):
        yield scrapy.Request(url= self.url, callback= self.parse_qqfinance, dont_filter = True)

    def parse_qqfinance(self, response):
        lis = response.xpath('.//li[@class="item cf"]')
        for li in lis:
            item = QQFinanceItem()
            item['_id'] = li.xpath('@id').extract_first()#.strip()
            crawler.info('_id : %s',item['_id'])
            # item['titletext'] = li.xpath('.//a[@class="picture"]/img/@alt').extract_first()#.strip()
            # crawler.info('titletext : %s', item['titletext'])
            item['url'] = li.xpath('.//a[@class="picture"]/@href').extract_first()#.strip()
            crawler.info('url : %s', item['url'])
            item['abouttime'] = li.xpath('.//span[@class="time"]/text()').extract_first()#.strip()
            crawler.info('abouttime : %s', item['abouttime'])
            item['imgscr'] = li.xpath('.//a[@class="picture"]/img/@scr').extract_first()#.strip()
            # crawler.info('imgscr : %s', item['imgscr'])
            try:
                strwd = os.getcwd() + '\\img'
                if not os.path.isdir(strwd):
                    os.mkdir('img_qqfinance')
                lastestnum = item['imgscr'].rfind('/')
                strfilelong = item['imgscr'][:lastestnum]
                nextnum = strfilelong.rfind('/') + 1
                filename = strfilelong[nextnum:]
                #将图片保存至本地
                urllib.request.urlretrieve(item['imgscr'], filename)
            except Exception as e:
                print(e)
            yield item

if __name__ == '__main__':
    cmdline.execute("scrapy crawl QQFinanceSpider".split())





