import pdb
import sys, os
import datetime as dt
import csv
import re

mypath = os.path.dirname(__file__)

class Program:
    def __init__(self, string):
        (self.start, self.end) = string.split('-')
        self.start = Program.convert_to_time(self.start)
        self.end = Program.convert_to_time(self.end)

    @staticmethod
    def convert_to_time(tstring):
        (hours, mins) = tstring.split(':')
        result = dt.time(int(hours), int(mins))
        return result

    def match(self, mydt):
        result = False
        myh = mydt.hour
        mym = mydt.minute
        if myh >= self.start.hour and mym >= self.start.minute:
            result = True
            if myh > self.end.hour:
                result = False
            elif myh == self.end.hour and mym > self.end.minute:
                result = False
        return result

    def isoformat(self, mydt):
        result = dt.datetime(mydt.year, mydt.month, mydt.day, self.start.hour, self.start.minute)
        return result

class BBC3Schedule:

    __BBC3_SCHEDULE__ = os.path.join(mypath, 'BBC3_sched.csv')
    def __init__(self, config = __BBC3_SCHEDULE__):
        self.config = config
        self.map = None
        self.setup()

    __RE_EMPTY_MATCH__ = re.compile('\A\s*\Z')
    def setup(self):
        cols = { 'Monday': 1, 'Tuesday': 3, 'Wednesday': 5, 'Thursday': 7, 'Friday': 9, 'Saturday': 11, 'Sunday': 13 }
        self.map = { k:[] for k in cols.keys() }
        with open(self.config, 'r') as fl:
             csvreader = csv.reader(fl, delimiter=',')
             for row in csvreader:
                 for key, col in cols.items():
                     timerange = row[col]
                     if not BBC3Schedule.__RE_EMPTY_MATCH__.match(timerange):
                         p = Program(timerange)
                         self.map[key].append(p)

    def quantize_date(self, mydt):
        result = None
        wdays = [ 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday' ]
        wday = wdays[mydt.weekday()]
        for prog in self.map[wday]:
            if prog.match(mydt):
                result = prog.isoformat(mydt)
                break
        return result
