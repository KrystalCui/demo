# -*- coding: utf-8 -*-

# Scrapy settings for GaiaSpider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'Gaia'

SPIDER_MODULES = ['Gaia.spiders']
NEWSPIDER_MODULE = 'Gaia.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
CONCURRENT_REQUESTS_PER_DOMAIN = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
   'Gaia.middlewares.RotateUserAgentMiddleware': 110,
}

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See http://scrapy.readthedocs.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'Gaia.pipelines.pipelines.MongoDBPipeline': 300,
    'scrapy_redis.pipelines.RedisPipeline': 300
}

MONGODB_SERVER = "47.100.3.16"
MONGODB_PORT = 27017
MONGODB_DB = "lordspider"
MONGODB_USER = "root"
MONGODB_PASSWORD = "root"

# If proxy mode is 2 uncomment this sentence :
#CUSTOM_PROXY = "http://host1:port"
# Enables scheduling storing requests queue in redis.
SCHEDULER = "Gaia.scrapy_redis.scheduler.Scheduler"
SCHEDULER_PERSIST = True
SCHEDULER_QUEUE_CLASS = 'Gaia.scrapy_redis.queue.SpiderSimpleQueue'

# DEPTH_LIMIT = 1

REDIS_URL = None
REDIS_HOST = '47.100.3.16'
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = ''

# 去重队列的信息
FILTER_URL = None
FILTER_HOST = '47.100.3.16'
FILTER_PORT = 6379
FILTER_DB = 0
FILTER_PASSWORD = ''

DOWNLOAD_DELAY = 10  # 间隔时间
# LOG_LEVEL = 'INFO'  # 日志级别
CONCURRENT_REQUESTS = 1  # 默认为16
# CONCURRENT_ITEMS = 1
# CONCURRENT_REQUESTS_PER_IP = 1
REDIRECT_ENABLED = False



