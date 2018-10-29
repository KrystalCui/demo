# -*- coding: utf-8 -*-
import requests
import pymongo
from pymongo import MongoClient
import socket
import datetime
import time
import scrapy


class Futuredata30Spider(scrapy.Spider):
    name = 'futuredata30'
    allowed_domains = ['stock2.finance.sina.com.cn']
    start_urls = ['http://stock2.finance.sina.com.cn/futures/api/json.php/IndexService.getInnerFuturesMiniKLine30m?symbol=cu1812']

    def connection(self):
        # 获取本机电脑名
        myname = socket.getfqdn(socket.gethostname())
        # 获取本机ip
        myaddr = socket.gethostbyname(myname)
        # 建立MongoDB数据库连接
        client = MongoClient('ss.gaiafintech.com', 3307)
        # 连接所需数据库,test为数据库名
        db = client.gaiaspider
        # 连接所用集合，也就是我们通常所说的表，test为表名
        collection = db.futuresdata_30
        # 接下里就可以用collection来完成对数据库表的一些操作
        # 查找集合中所有数据
        # for item in collection.find():
        # print(item)
        # 查找集合中单条数据
        # print(collection.find_one())
        # 向集合中插入数据
        # collection.insert({name: 'Tom', age: 25, addr: 'Cleveland'})
        # 更新集合中的数据,第一个大括号里为更新条件，第二个大括号为更新之后的内容
        # collection.update({Name: 'Tom'}, {Name: 'Tom', age: 18})
        # 删除集合collection中的所有数据
        # collection.remove()
        # 删除集合collection
        # collection.drop()
        # con = pymongo.Connection(myaddr, 27017)
        # db = con.jykt
        return collection

    def parse(self, response):
        connection = self.connection()
        count = 0
        seconds = 10
        while True:
            result = response.content.decode('utf-8')
            result = result[1: len(result) - 2]
            result = result.replace("[", "").replace("\"", "")
            results = result.split("],")
            seconds += 10
            for data in results:
                datas = data.split(",")
                if count != 0:
                    dt = datetime.datetime.strptime(datas[0], "%Y-%m-%d %H:%M:%S")
                    now_dt = datetime.datetime.now()
                    delta = now_dt - dt
                    if delta > datetime.timedelta(minutes=30):
                        continue
                seconds = 10 if seconds <= 10 else seconds - 10
                print(datas)
                mydict = {"datetime": datas[0], "code": "cu1812", "open": datas[1], "high": datas[2], "low": datas[3],
                          "close": datas[4], "volume": datas[5]}
                updateRes = connection.update_one(filter={'datetime': datas[0]},
                                                  update={'$set': dict(mydict)},
                                                  upsert=True)
                # x = connection.insert_one(mydict)
            count += 1
            print(count)
            time.sleep(seconds)
            pass



