from abc import ABC, abstractmethod
import os
import datetime
import pytz

TZ = pytz.timezone('Asia/Taipei')

def ensure_path(path):
    '''
    If input path is not exist, 
    function will create the path including all middle directory.
    '''
    if not os.path.isdir(path):
        os.makedirs(path)

class AbsCrawler(ABC):
    _url = ''
    _directory = ''
    _cmd = 'curl {url} > {path}'
    _filename = ''

    def __init__(self, url, directory):
        self._now = datetime.datetime.now(TZ)
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

    @property
    def now(self):
        return self._now

    @abstractmethod
    def _set_filename(self):
        '''
        Return file name string(e.g:'tmp.csv')
        '''
        pass
 
    def crawl(self):
        ensure_path(self.directory)
        status = os.system(self.cmd)
        if status != 0:
            raise CrawFailException('Craw Action Failed !')
        if not self.check():
            raise DataMissingException('Crawed data is missing !')
   
    @abstractmethod
    def check(self):
        '''
        Return Ture for crawled file valid, otherwise return False
        '''
        pass

class DayCrawler(AbsCrawler):
    def _set_filename(self):
        return self.now.strftime('%Y%m%d.csv')

    def get_verify(self, now):
        return int(now.hour*6+(now.minute/10) + 1)

    def check(self):
        contents = self.store()
        verify_len = self.get_verify(self.now)
        # print(verify_len, len(contents))
        if len(contents) == verify_len:
            return True
        else:
            return False

    def store(self):
        with open(self.path, 'r') as rf:
            return [l for l in rf.readlines() if l != ',\n']

class DayAppendCrawler(DayCrawler):
    def crawl(self, convert=None):
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
        return self.now.strftime('%Y.csv')
 
    def check(self):
        contents = self.store()
        verify_len = self.get_verify(self.now)
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
        minute = int(self.now.minute/10)
        return self.now.strftime('%Y%m%d-%H{:<02d}.csv'.format(minute))

    def crawl(self, convert=None):
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
        verify = self.get_verify(self.now)
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

class HourCrawler(AbsCrawler):
    def _set_filename(self):
        return self.now.strftime('%Y%m%d-%H.csv')

    def check(self):
        with open(self.path, 'r') as rf:
            header = rf.readline()
        if 'float32' in header:
            return True
        else:
            return False


class CrawFailException(Exception):
    pass

class DataMissingException(Exception):
    pass

