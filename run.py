from scrapy import cmdline
from Gaia.spiders.seventwentyfournews import InvestmentNewsSpider
import os
import subprocess
import time
from subprocess import Popen

def run():
    subprocess.Popen("scrapy crawl EastMoneyNewsSpider")


if __name__ == '__main__':
    # cmdline.execute("scrapy crawl SinaFinanceNewsSpider".split())
    # spro = scrapypro()
    # schedule.every(2).seconds.do(spro.run())
    # while True:
    #     schedule.run_pending()
    #     time.sleep(1)
    while True:
        run()
        time.sleep(600)  # 每隔10min
