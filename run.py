from scrapy import cmdline
from Gaia.schedule.seventwentyfournewsschedule import SevenTwentyFourNewsSchedule
import os
import schedule
import subprocess
import time
from subprocess import Popen


def run():
    subprocess.Popen("scrapy crawl EastMoneyNewsSpider")

def run_stocknews():
    # subprocess.Popen("scrapy crawl EastMoneyStockNewsSpider")
    subprocess.Popen("scrapy crawl SinaFinanceNewsSpider")


def runseventwentyfournewsschedule():
    p = SevenTwentyFourNewsSchedule()
    p.fetch()

def runsinafinacen():
    subprocess.Popen("scrapy crawl SinaFinanceNewsSpider")

if __name__ == '__main__':
    # cmdline.execute("scrapy crawl SinaFinanceNewsSpider".split())
    # spro = scrapypro()
    # schedule.every(2).seconds.do(spro.run())
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    # run()
    # runseventwentyfournewsschedule()
    subprocess.Popen("scrapy crawl EastMoneyNewsSpider")
    subprocess.Popen("scrapy crawl SinaFinanceNewsSpider")
    schedule.every(1).minutes.do(runsinafinacen)
    # schedule.every(5).seconds.do(runseventwentyfournewsschedule)
    schedule.every(600).seconds.do(run)
    # subprocess.Popen("scrapy crawl SinaFinanceNewsSpider")
    # schedule.every(5).seconds.do(run_stocknews)
    while True:
        schedule.run_pending()
        time.sleep(1)
