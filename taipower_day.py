import os
from time import sleep
from lib.crawler import YearCrawler, DataMissingException

BASE_PATH = './data/taipower/'

if __name__ == '__main__':
    reserveCrawler = YearCrawler(
                        'https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/reserve.csv',
                        os.path.join(BASE_PATH, 'reserve/')

    success_flag = False
    while not success_flag:
        try:
            reserveCrawler.crawl()
            success_flag = True
        except DataMissingException:
            print('Waiting 1 hour for data upload ...')
            sleep(3600)

