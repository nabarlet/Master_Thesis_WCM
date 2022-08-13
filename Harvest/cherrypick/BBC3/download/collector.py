import pdb

import sys,os

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, '.'), os.path.join(mypath, *['..']*2)])

import datetime as dt
from single_day import SingleDay

class Collector:

    __DEFAULT_INIT_DATE__ = dt.date(2013, 4, 1)
    def __init__(self, provider, init_date = __DEFAULT_INIT_DATE__): 
        self.provider  = provider
        self.init_date = init_date
        self.end_date  = dt.date.today()
        self.one_day   = dt.timedelta(1)

    def retrieve(self):
        cur_date = self.init_date
        while (cur_date < self.end_date):
            sd = SingleDay(cur_date, self.provider)
            cur_date += self.one_day
            yield sd

    @classmethod
    def collect(cls, provider, init_date = __DEFAULT_INIT_DATE__):
        c = Collector(provider, init_date)
        for sd in c.retrieve():
            yield sd.retrieve()

if __name__ == '__main__':
    c = Collector()
    c.collect()
