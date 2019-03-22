from scrapy import cmdline
from Gaia.schedule.seventwentyfournewsschedule import SevenTwentyFourNewsSchedule
import os
import schedule
import subprocess
import time
from subprocess import Popen

#
# def run():
#     subprocess.Popen("scrapy crawl EastMoneyNewsSpider")

def runseventwentyfournewsschedule():
    p = SevenTwentyFourNewsSchedule()
    p.fetch()

def runsinafinacen():
    subprocess.Popen("scrapy crawl 新浪财经新闻")

def runeastmoney():
    subprocess.Popen("scrapy crawl 东方财富新闻")

if __name__ == '__main__':
    # cmdline.execute("scrapy crawl 新浪新闻".split())
    # spro = scrapypro()
    # schedule.every(2).seconds.do(spro.run())
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    # run()
    # runseventwentyfournewsschedule()
    subprocess.Popen("scrapy crawl 东方财富新闻")
    subprocess.Popen("scrapy crawl 新浪财经新闻")
    schedule.every(20).minutes.do(runsinafinacen)
    schedule.every(20).minutes.do(runeastmoney)
    schedule.every(5).seconds.do(runseventwentyfournewsschedule)

    # schedule.every(600).seconds.do(run)
    # schedule.every(5).seconds.do(run_stocknews)

    while True:
        schedule.run_pending()
        time.sleep(1)
