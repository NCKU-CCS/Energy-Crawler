from abc import ABC, abstractmethod
import os
import datetime
from time import sleep
import pytz
import json
TZ = pytz.timezone('Asia/Taipei')

def ensure_path(path):
    '''
    If input path is not exist, 
    function will create the path including all middle directory.
    '''
    if not os.path.isdir(path):
        os.makedirs(path)

def format_usage_json(jfile):
    '''
    Format a total usage .csv file to csv tuple for recording
    Input:
        List of contents craw from taipower read as .csv
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
        List of contents craw from taipower read as .csv
    Output:
        List of csv tuple for recording and the first line must be the record time
    '''
    contents = json.loads(jfile[0])
    rtime = contents['']
    contents = [','.join(l[1:]).strip().replace('-','')
                 + '\n' for l in contents['aaData']]
    contents.insert(0, rtime+ '\n')
    return contents

class AbsCrawler(ABC):
    _url = ''
    _directory = ''
    _cmd = 'curl {url} > {path}'
    _filename = ''

    def __init__(self, url, directory):
        self.url = url
        self.directory = directory
        self._filename = self._set_filename()

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, u):
        self._url = u

    @property
    def directory(self):
        return self._directory

    @directory.setter
    def directory(self, d):
        if '~' in d:
            self._directory = d.replace('~', os.path.expanduser('~'))
        else:
            self._directory = d

    @property
    def cmd(self):
        return self._cmd.format(url=self.url,
                                path=self.path)
    @property
    def filename(self):
        return self._filename

    @property
    def path(self):
        return os.path.join(self.directory, self._filename)

    @abstractmethod
    def _set_filename(self):
        '''
        Return file name string(e.g:'tmp.csv')
        '''
        pass
 
    def craw(self):
        ensure_path(self.directory)
        status = os.system(self.cmd)
        if status != 0:
            raise CrawFailException('Craw Action Failed !')
        if not self.check():
            raise DataMissingException('Crawed data is missing !')
   
    @abstractmethod
    def check(self):
        '''
        Return Ture for crawed file valid, otherwise return False
        '''
        pass

class DayCrawler(AbsCrawler):
    def _set_filename(self):
        return datetime.datetime.now(TZ).strftime('%Y%m%d.csv')

    def get_verify(self, now):
        return int(now.hour*6+(now.minute/10) + 1)

    def check(self):
        contents = self.store()
        now = datetime.datetime.now(TZ)
        verify_len = self.get_verify(now)
        # print(verify_len, len(contents))
        if len(contents) == verify_len:
            return True
        else:
            return False

    def store(self):
        with open(self.path, 'r') as rf:
            return [l for l in rf.readlines() if l != ',\n']

class DayAppendCrawler(DayCrawler):
    def craw(self, convert=None):
        exist_flag = False
        ensure_path(self.directory)
        if os.path.isfile(self.path):
            exist_flag = True
            old = self.store()

        status = os.system(self.cmd)
        if status != 0:
            raise CrawFailException('Craw Action Failed !')
        new = self.store() 
        if convert is not None: new = convert(new)
        if exist_flag: 
            self.append(old, new)
        else:
            with open(self.path, 'w') as wf:
                wf.writelines(new)

        if not self.check():
            raise DataMissingException('Crawed data is missing !')

    def append(self, old, new):
        # print(old, new)
        last_time = old[-1].split(',')[0]
        new_time = new[0].split(',')[0]
                
        if last_time == '23:50':
            combine = new
        elif last_time != new_time: 
            combine = old + new
        else:
            combine = old

        # print(combine)
        with open(self.path, 'w') as wf:
            wf.writelines(combine)

class YearCrawler(AbsCrawler):
    def _set_filename(self):
        return datetime.datetime.now(TZ).strftime('%Y.csv')
 
    def check(self):
        contents = self.store()
        now = datetime.datetime.now(TZ)
        verify_len = self.get_verify(now)
        # print(verify_len, len(contents))
        if len(contents) == verify_len:
            return True
        else:
            return False

    def get_verify(self, now):
        now = now.date()
        first = datetime.date(now.year, 1, 1)
        return (now - first).days

    def store(self):
        with open(self.path, 'r') as rf:
            return [l for l in rf.readlines() if ',,,' not in l]

class MinuteCrawler(AbsCrawler):
    def _set_filename(self):
        now = datetime.datetime.now(TZ)
        minute = int(now.minute/10)
        return now.strftime('%Y%m%d-%H{:<02d}.csv'.format(minute))

    def craw(self, convert=None):
        ensure_path(self.directory)
        status = os.system(self.cmd)
        if status != 0:
            raise CrawFailException('Craw Action Failed !')
        new = self.store()
        if convert is not None:
            new = convert(new)
            with open(self.path, 'w') as wf:
                wf.writelines(new)
        if not self.check():
            raise DataMissingException('Crawed data is missing !')
    
    def check(self):
        contents = self.store()
        rec_time = datetime.datetime.strptime(contents[0],'%Y-%m-%d %H:%M\n')
        rec_time = rec_time.strftime('%Y%m%d-%H%M')
        now = datetime.datetime.now(TZ)
        verify = self.get_verify(now)
        #  print(verify, rec_time)
        if  rec_time == verify:
            return True
        else:
            return False

    def get_verify(self, now):
        minute = int(now.minute/10)
        return now.strftime('%Y%m%d-%H{:<02d}'.format(minute))

    def store(self):
        with open(self.path, 'r') as rf:
            return rf.readlines()

class CrawFailException(Exception):
    pass

class DataMissingException(Exception):
    pass

if __name__ == '__main__':
    genaryCrawler = MinuteCrawler(
                        'https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/genary.txt',
                        './data/genary/')
    fuelTypeCrawler = DayCrawler(
                    'https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/loadfueltype.csv',
                    './data/fueltype/')
    areasCrawler = DayCrawler(
                    'https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/loadareas.csv',
                    './data/area/day_usage/')
    areasGenCrawler = DayAppendCrawler(
                        'https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/genloadareaperc.csv',
                        './data/area/gen_usage/')
    totalUsageCrawler = DayAppendCrawler(
                        'https://www.taipower.com.tw/d006/loadGraph/loadGraph/data/loadpara.txt',
                        './data/total/')
    
    general_craw_dict = {genaryCrawler:format_genary_json,
                         fuelTypeCrawler:None,
                         areasCrawler:None}
    append_craw_dict = {areasGenCrawler:('areasGenCrawler',None),
                        totalUsageCrawler:('totalUsageCrawler',format_usage_json)}

    for c,f in general_craw_dict.items():
        success_flag = False
        while not success_flag:
            try:
                if f is not None: 
                    c.craw(convert=f)
                else:
                    c.craw()
                success_flag = True
            except DataMissingException:
                print('Waiting 1 minutes for data upload ...')
                sleep(60)
                
    for c,t in append_craw_dict.items():
        try:
            if t[1] is not None:
                c.craw(convert=t[1])
            else:
                c.craw()
        except DataMissingException as e:
            print(t[0], e)

