import datetime
import pytz
from lib.crawler import HourCrawler

TZ = pytz.timezone('Asia/Taipei')

HR = ['00','06','12','18']

if __name__ == '__main__':
    now = datetime.datetime.now(TZ).strftime('%Y%m%d%H')
    # Should delete
    if now[-2:] not in HR:
        index = int(now[-2:]) // 6
        now = now[:-2] + HR[index]

    print(now)
    power_gen_url = 'http://greenmet.cwb.gov.tw/data/map_csv/Display/Range/Analysis/{time}/NOCWRF_03000_00_K01WEP_{time}_0000.csv'.format(time=now)
    density_url = 'http://greenmet.cwb.gov.tw/data/map_csv/Display/Range/Analysis/{time}/NOCWRF_03000_00_K01WED_{time}_0000.csv'.format(time=now)
    speed_url = 'http://greenmet.cwb.gov.tw/data/map_csv/Display/Range/Analysis/{time}/NOCWRF_03000_00_K01WSP_{time}_0000.csv'.format(time=now)

    crawl_dict = {power_gen_url: './data/greenmet/wind/power_gen/',
                  density_url: './data/greenmet/wind/density/',
                  speed_url: './data/greenmet/wind/speed/'}

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
