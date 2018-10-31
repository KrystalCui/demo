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

class SevenTwentyFourNewsSchedule:
    def __init__(self):
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
        self.url = 'http://newsapi.eastmoney.com/kuaixun/v1/getlist_102_ajaxResult_50_1_.html'

    def fetch(self):
        crawler.info("start fetch")
        request = urllib.request.Request(self.url)
        response = urllib.request.urlopen(request)
        content = response.read().decode("utf-8")
        # crawler.info(content)
        listeachone = content.split('{')
        sizeeach = int(len(listeachone) - 1)
        i = 1
        while (i < sizeeach):
            # print("好好22221 + i" + i)
            listattribute = listeachone[i + 1].split(',')
            j = 0
            item = SevenTwentyFourNewsItem()
            while (j < (len(listattribute) - 1)):
                listkeyvalue = listattribute[j].split(':')
                if len(listkeyvalue) > 0:
                    if listkeyvalue[0] == '"title"':
                        item['title'] = listkeyvalue[1][0:].strip('"')
                        crawler.info('title:%s', item['title'])
                        # print('title:%s'%item['title'])
                    if listkeyvalue[0] == '"simtitle"':
                        item['simtitle'] = listkeyvalue[1][0:].strip('"')
                        crawler.info('simtitle:%s', item['simtitle'])
                        # print('simtitle:%s'%item['simtitle'])
                    if listkeyvalue[0] == '"showtime"':
                        item['showtime'] = listkeyvalue[1].strip('"') + ":" + listkeyvalue[2] + ":" + listkeyvalue[3].strip(
                            '"')
                        crawler.info('showtime:%s', item['showtime'])
                        # print('showtime:%s' % item['showtime'])
                    if listkeyvalue[0] == '"ordertime"':
                        item['ordertime'] = listkeyvalue[1].strip('"') + ":" + listkeyvalue[2] + ":" + listkeyvalue[3].strip(
                            '"')
                        crawler.info('ordertime:%s', item['ordertime'])
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
    schedule.every(1).minutes.do(run)
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