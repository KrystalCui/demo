from apscheduler.schedulers.background import BackgroundScheduler as Sch
import urllib
from Gaia.items import SevenTwentyFourNewsItem
from Gaia.logger.log import crawler
import pymongo
import redis
from Gaia.config import *
from urllib.parse import quote_plus
import schedule
import time
import json

class SevenTwentyFourNewsSchedule:
    def __init__(self):
        redis_args = get_redis_args()
        mongo_db_args = get_mongo_db_args()
        pool = redis.ConnectionPool(
            host=redis_args.get('host')
            , port=redis_args.get('port')
            , db=redis_args.get('id_name')
            , password=redis_args.get('password'))
        self.server = redis.Redis(connection_pool=pool)

        uri = "mongodb://{}:{}@{}:{}/{}".format(quote_plus(mongo_db_args.get('user')),
                                                quote_plus(mongo_db_args.get('password')),
                                                mongo_db_args.get('host'),
                                                mongo_db_args.get('port'), mongo_db_args.get('db_name'))

        crawler.info("uri: %s", uri)
        connection = pymongo.MongoClient(uri)
        crawler.info("db: %s", mongo_db_args.get('db_name'))
        self.db = connection[mongo_db_args.get('db_name')]
        self.url = 'http://newsapi.eastmoney.com/kuaixun/v1/getlist_102_ajaxResult_50_1_.html'

    def fetch(self):
        crawler.info("start fetch")
        request = urllib.request.Request(self.url)
        response = urllib.request.urlopen(request)
        content = response.read().decode("utf-8")
        splitnum = content.rfind('=') + 1
        jsoncotent = json.loads(content[splitnum:])
        for each in jsoncotent['LivesList']:
            item = SevenTwentyFourNewsItem()
            item['title'] = each['title']
            crawler.info('title:%s', item['title'])
            item['simtitle'] = each['simtitle']
            crawler.info('simtitle:%s', item['simtitle'])
            item['showtime'] = each['showtime']
            crawler.info('showtime:%s', item['showtime'])
            item['ordertime'] = each['ordertime']
            crawler.info('ordertime:%s', item['ordertime'])
            item['_id'] = each['id']
            crawler.info('_id:%s', item['_id'])
            item['commentnum'] = each['commentnum']
            crawler.info('commentnum:%s', item['commentnum'])
            if each['digest'] == None or each['digest'] =='':
                item['digest'] = item['title']
            else:
                item['digest'] = each['digest']
            crawler.info('digest:%s', item['digest'])
            if each['simdigest'] == None or each['simdigest'] == '':
                item['simdigest'] = each['simtitle']
            else:
                item['simdigest'] = each['simdigest']
            crawler.info('simdigest:%s', item['simdigest'])
            hkey = "seventwentyfournews_filter"
            try:
                _id = item['_id']
                if self.server.hget(hkey, _id) is None:
                    self.server.hset(hkey, _id, _id)
                    self.db['seventwentyfournews'].insert_one(dict(item))
            except :
                continue
            # a = self.server.hget(hkey, _id)


def run():
    p = SevenTwentyFourNewsSchedule()
    p.fetch()
#     # sch = Sch()
#     # sch.add_job(p.fetch, 'interval', minutes=1)  # 每1分钟抓取一次
#     # sch.start()
#     schedule.every(1).seconds.do(p.fetch())

if __name__ == '__main__':
    crawler.info("start SevenTwentyFourNewsSchedule")
    p = SevenTwentyFourNewsSchedule()
    p.fetch()
    schedule.every(30).seconds.do(run)
    while True:
        schedule.run_pending()
        time.sleep(1)
#     p = SevenTwentyFourNewsSchedule()
#     p.fetch()
#
#     while True:
#         schedule.run_pending()
        # time.sleep(1)
    # run()
# p = SevenTwentyFourNewsSchedule()
# schedule.every(2).seconds.do(run)
# while True:
#     schedule.run_pending()
#     time.sleep(1)