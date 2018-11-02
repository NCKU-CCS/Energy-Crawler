import os
from lib.crawler import YearCrawler, CrawlerCollector, DataMissingException

BASE_PATH = '~/data/TaiPower/'

MAX_TIME = 168
WAITING_TIME = 3600

if __name__ == '__main__':
    reserveCrawler = YearCrawler(
                        'https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/reserve.csv',
                        os.path.join(BASE_PATH, 'reserve/'))

    cc = CrawlerCollector(MAX_TIME, WAITING_TIME)
    cc.add(reserveCrawler)
    cc.all_crawl()
