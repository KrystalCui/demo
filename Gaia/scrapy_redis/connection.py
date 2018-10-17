import redis
from Gaia.logger import crawler

# Default values.
REDIS_URL = None
REDIS_HOST = 'localhost'
REDIS_PORT = 6379

FILTER_URL = None
FILTER_HOST = 'localhost'
FILTER_PORT = 6379
FILTER_DB = 0

def from_settings(settings):
    url = settings.get('REDIS_URL', REDIS_URL)
    host = settings.get('REDIS_HOST', REDIS_HOST)
    port = settings.get('REDIS_PORT', REDIS_PORT)

    crawler.info ("from_settings url:%s" , url)
    crawler.info("from_settings host:%s", host)
    crawler.info("from_settings port:%s", port)

    # REDIS_URL takes precedence over host/port specification.
    if url:
        return redis.from_url(url)
    else:
        return redis.Redis(host=host, port=port)


def from_settings_filter(settings):
    url = settings.get('FILTER_URL', FILTER_URL)
    host = settings.get('FILTER_HOST', FILTER_HOST)
    port = settings.get('FILTER_PORT', FILTER_PORT)
    db = settings.get('FILTER_DB', FILTER_DB)

    crawler.info ("from_settings_filter url:%s" , url)
    crawler.info("from_settings_filter host:%s", host)
    crawler.info("from_settings_filter port:%s", port)
    if url:
        return redis.from_url(url)
    else:
        return redis.Redis(host=host, port=port, db=db)
