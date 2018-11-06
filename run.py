from scrapy import cmdline
from Gaia.schedule.seventwentyfournewsschedule import SevenTwentyFourNewsSchedule
import os
import schedule
import subprocess
import time
from subprocess import Popen


def run():
    subprocess.Popen("scrapy crawl EastMoneyNewsSpider")


def runseventwentyfournewsschedule():
    p = SevenTwentyFourNewsSchedule()
    p.fetch()


if __name__ == '__main__':
    # cmdline.execute("scrapy crawl SinaFinanceNewsSpider".split())
    # spro = scrapypro()
    # schedule.every(2).seconds.do(spro.run())
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    run()
    schedule.every(30).seconds.do(runseventwentyfournewsschedule)
    schedule.every(600).seconds.do(run)
    while True:
        schedule.run_pending()
        time.sleep(1)
