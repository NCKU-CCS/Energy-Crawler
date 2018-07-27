import datetime
import pytz
from time import sleep
from lib.crawler import HourCrawler, DataMissingException

TZ = pytz.timezone('Asia/Taipei')

if __name__ == '__main__':
    now = datetime.datetime.now(TZ).strftime('%Y%m%d%H')

    power_gen_url = 'http://greenmet.cwb.gov.tw/data/map_csv/Display/Range/Analysis/{time}/HIMAW8_01000_00_B00SED_{time}_0000.csv'.format(time=now)
    radiation_url = 'http://greenmet.cwb.gov.tw/data/map_csv/Display/Range/Analysis/{time}/HIMAW8_01000_00_B00DIR_{time}_0000.csv'.format(time=now)

    crawl_dict = {power_gen_url: './data/greenmet/solar/power_gen/',
                  radiation_url: './data/greenmet/solar/radiation/'}

    crawl_list = [HourCrawler(k,v) for k,v in crawl_dict.items()]

    for c in crawl_list:
        success_flag = False
        while not success_flag:
            try:
                c.crawl()
                success_flag = True
            except DataMissingException:
                print('Waiting 1 hour for data upload ...')
                sleep(3600)
