from time import sleep
from crawler import YearCrawler,DataMissingException
if __name__ == '__main__':
    reserveCrawler = YearCrawler(
                        'https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/reserve.csv',
                        '~/data/TaiPower/reserve')
    success_flag = False
    while not success_flag:
        try:
            reserveCrawler.craw()
            success_flag = True
        except DataMissingException:
            print('Waiting 1 hour for data upload ...')
            sleep(3600)

