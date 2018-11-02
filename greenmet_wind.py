import os
import datetime
import pytz
from lib.crawler import HourCrawler, CrawlerCollector, DataMissingException

BASE_PATH = '~/data/Greenmet/wind/'

TZ = pytz.timezone('Asia/Taipei')

MAX_TIME = 168
WAITING_SEC = 3600

if __name__ == '__main__':
    now = datetime.datetime.now(TZ).strftime('%Y%m%d%H')

    power_gen_url = 'http://greenmet.cwb.gov.tw/data/map_csv/Display/Range/Analysis/{time}/NOCWRF_03000_00_K01WEP_{time}_0000.csv'.format(time=now)
    density_url = 'http://greenmet.cwb.gov.tw/data/map_csv/Display/Range/Analysis/{time}/NOCWRF_03000_00_K01WED_{time}_0000.csv'.format(time=now)
    speed_url = 'http://greenmet.cwb.gov.tw/data/map_csv/Display/Range/Analysis/{time}/NOCWRF_03000_00_K01WSP_{time}_0000.csv'.format(time=now)

    crawl_dict = {power_gen_url: os.path.join(BASE_PATH, 'power_gen/'),
                  density_url: os.path.join(BASE_PATH, 'density/'),
                  speed_url: os.path.join(BASE_PATH, 'speed/')}

    crawl_list = [HourCrawler(k,v) for k,v in crawl_dict.items()]

    cc = CrawlerCollector(MAX_TIME, WAITING_SEC)
    cc.add(crawl_list)
    cc.all_crawl()
