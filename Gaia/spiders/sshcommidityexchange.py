from selenium import webdriver
from Gaia.config import *
import pymongo
import redis
from urllib.parse import quote_plus
import time
import unittest
import urllib
from bs4 import BeautifulSoup
from Gaia.items import DomesticCommodityExchangeItem
from Gaia.logger import crawler

class sshcommidityexchange(unittest.TestCase):

    def setUp(self):
        redis_args = get_redis_args()
        mongo_db_args = get_mongo_db_args()
        pool = redis.ConnectionPool(
            host=redis_args.get('host')
            , port=redis_args.get('port')
            , db=redis_args.get('id_name'))
        self.server = redis.Redis(connection_pool=pool)

        uri = "mongodb://{}:{}@{}:{}/{}".format(quote_plus(mongo_db_args.get('user')),
                                                quote_plus(mongo_db_args.get('password')),
                                                mongo_db_args.get('host'),
                                                mongo_db_args.get('port'), mongo_db_args.get('db_name'))

        crawler.info("uri: %s", uri)
        connection = pymongo.MongoClient(uri)
        crawler.info("db: %s", mongo_db_args.get('db_name'))
        self.db = connection[mongo_db_args.get('db_name')]
        self.url = "http://www.shfe.com.cn"
        self.hreflist = []
        #创建驱动程序对象
        self.driver = webdriver.Firefox()

    def test_search_in_python_org(self):
        #创建驱动程序对象的本地引用
        driver = self.driver
        #打开对应网页
        driver.get(self.url)
        # 加载3秒，等待所有数据加载完毕
        time.sleep(2)
        #使用assert断言的方法判断在页面标题中是否包含 “Python”，assert 语句将会在之后的语句返回false后抛出异常
        #self.assertIn("ul", driver.title)
        #获取到id为subnav的ul，也就是最外层的ul
        elemul = driver.find_element_by_id('subnav')#.text
        #此处用的是elements！返回的是list，此层获取到的是金属，能源等的列表
        elemlis_first = elemul.find_elements_by_xpath('.//li[2]/ul/li')
        for elemli_first in elemlis_first:
            #将每一个li打开，里面还有一层ul，此处为铜铝等详细列表
            elemlis_second = elemli_first.find_elements_by_xpath('.//ul/li')
            for elemli_second in elemlis_second:
                #selenium获取a的href需要get_attribute方法
                href = elemli_second.find_element_by_tag_name('a').get_attribute('href')#.click()
                self.hreflist.append(href)
        self.parse_code()
        self.driver.quit()

    def parse_code(self):
        for href in self.hreflist:
            request = urllib.request.Request(url=href)
            response = urllib.request.urlopen(request)
            time.sleep(1)
            html = BeautifulSoup(response, 'lxml')
            #直接取出来的是[]列表，取第0个就是配置文件格式
            if html.find_all('div', class_='heyue_big') != []:
                div = html.find_all('div', class_='heyue_big')[0]
                a = div.find_all('a')[0]
                href = a.get('href')
                url = self.url + href
                request = urllib.request.Request(url=url)
                responses = urllib.request.urlopen(request)
                time.sleep(1)
                self.parse_variety(response=responses)

    def parse_variety(self, response):
        html = BeautifulSoup(response, 'lxml')
        if html.find_all('tr') != None:
            trs = html.find_all('tr')
            list = {}
            for tr in trs:
                tds = tr.find_all('td')
                tdlen = len(tds)
                if tdlen == 2:
                    spantext = tds[0].text
                    try:
                        textfirst = spantext.strip()
                    except:
                        textfirst = spantext
                    list.get(textfirst)
                    spantext_2 = tds[1].text
                    try:
                        list[textfirst] = spantext_2.strip()
                    except:
                        list[textfirst] = spantext_2
        else:
            print('图片')
        item = DomesticCommodityExchangeItem()
        item['datasource'] = '上海期货交易所'
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
            if list.get('交割日期') != None and list.get('交割日期') != '':
                item['deliverydate'] = list['交割日期']
                crawler.info('交割日期:%s', item['deliverydate'])
            if list.get('交割单位') != None and list.get('交割单位') != '':
                item['tradingunit'] = list['交割单位']
                crawler.info('交割单位:%s', item['tradingunit'])
            variety = item['tradingvariety']
            hkey = 'sshcommidityexchange_filter'
            if self.server.hget(hkey, variety) is None:
                self.server.hset(hkey, variety, variety)
                self.db['contractF10_domestic'].insert_one(dict(item))
        except Exception as e:
            print(e)



if __name__=="__main__":
    unittest.main()




