import os
import json
from time import sleep
from lib.crawler import MinuteCrawler, DayCrawler, DayAppendCrawler, DataMissingException 

BASE_PATH = './data/taipower'

def format_usage_json(jfile):
    '''
    Format a total usage .csv file to csv tuple for recording
    Input:
        List of contents crawl from taipower read as .csv
    Output:
        List of a string and the first column must be the record time
    '''
    needed = [l.replace('"','').replace('\n','').replace(',','')
                for l in jfile[2:6]]
    seperate = needed[-1].split(':')
    hr = seperate[0][-2:]
    minute = seperate[1][:2]
    # print(hr, minute)
    del needed[-1]
    needed.insert(0,'{}:{}'.format(hr,minute))
    needed = [','.join(needed)+'\n']
    # print(needed)

    return needed

def format_genary_json(jfile):
    '''
    Format a genary .csv file to csv contents for recording
    Input:
        List of contents crawl from taipower read as .csv
    Output:
        List of csv tuple for recording and the first line must be the record time
    '''
    contents = json.loads(jfile[0])
    rtime = contents['']
    contents = [','.join(l[1:]).strip().replace('-','')
                 + '\n' for l in contents['aaData']]
    contents.insert(0, rtime+ '\n')
    return contents

if __name__ == '__main__':
    genaryCrawler = MinuteCrawler(
                        'https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/genary.txt',
                        os.path.join(BASE_PATH, 'genary/'))
    fuelTypeCrawler = DayCrawler(
                    'https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/loadfueltype.csv',
                    os.path.join(BASE_PATH, 'fueltype/'))
    areasCrawler = DayCrawler(
                    'https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/loadareas.csv',
                    os.path.join(BASE_PATH, 'day_usage/'))
    areasGenCrawler = DayAppendCrawler(
                        'https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/genloadareaperc.csv',
                        os.path.join(BASE_PATH, 'gen_usage/'))
    totalUsageCrawler = DayAppendCrawler(
                        'https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/loadpara.txt',
                        os.path.join(BASE_PATH, 'total/'))
    
    general_crawl_dict = {genaryCrawler:format_genary_json,
                         fuelTypeCrawler:None,
                         areasCrawler:None}
    append_crawl_dict = {areasGenCrawler:('areasGenCrawler',None),
                        totalUsageCrawler:('totalUsageCrawler',format_usage_json)}

    for c,f in general_crawl_dict.items():
        success_flag = False
        while not success_flag:
            try:
                if f is not None: 
                    c.crawl(convert=f)
                else:
                    c.crawl()
                success_flag = True
            except DataMissingException:
                print('Waiting 1 minutes for data upload ...')
                sleep(60)
                
    for c,t in append_crawl_dict.items():
        try:
            if t[1] is not None:
                c.crawl(convert=t[1])
            else:
                c.crawl()
        except DataMissingException as e:
            print(t[0], e)

