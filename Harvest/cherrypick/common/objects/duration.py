import pdb
import sys,os
import datetime as dt
import re

mypath=os.path.dirname(__file__)
sys.path.append(os.path.join(mypath, *['..']*2))

from common.objects.object_base import ObjectBase
from common.utilities.string import __UNK__

class DurationValueError(ValueError):
    pass

class Duration(ObjectBase):
    def __init__(self, value, attrs = {}):
        if value != __UNK__ and type(value) is not dt.timedelta:
            raise DurationValueError(value)
        self.__dur__ = value
        self.attrs   = attrs

    def __str__(self):
        return str(self.__dur__)

    def to_seconds(self):
        result = self.__dur__
        if type(self.__dur__) is dt.timedelta:
            result = self.__dur__.seconds
        return result

    def inspect(self):
        return "Duration: %s" % (str(self.to_seconds()))

    @staticmethod
    def common_parser(hms_list):
        (hours, mins, secs) = hms_list
        return dt.timedelta(hours=hours, minutes=mins, seconds=secs)

    @staticmethod
    def single_split_parser(raw_value, attrs = {}):
        splitted = None
        s1 = raw_value.split(attrs['splitchar'])
        s1 = [int(v) for v in s1]
        if len(s1) == 2:
            splitted = [0]
            splitted.extend(s1)
        elif len(s1) == 1:
            splitted = [0, 0]
            splitted.extend(s1)
        else: # this must be len(s1) == 3
            splitted = s1
        return Duration.common_parser(splitted)

    @staticmethod
    def colon_parser(raw_value, attrs = {}):
        attrs['splitchar'] = ':'
        return Duration.single_split_parser(raw_value, attrs)

    @staticmethod
    def dot_parser(raw_value, attrs = {}):
        attrs['splitchar'] = '.'
        return Duration.single_split_parser(raw_value, attrs)

    @staticmethod
    def h_dot_parser(raw_value, attrs = {}):
        s1 = raw_value.split('h')
        s2 = s1[1].split('.')
        splitted = [s1[0]]
        splitted.extend(s2)
        splitted = [int(s) for s in splitted]
        return Duration.common_parser(splitted)

    @staticmethod
    def quote_parser(raw_value, attrs = {}):
        dsep = attrs['dsep']
        ssep = attrs['ssep']
        dsep_re = re.compile(dsep)
        ssep_re = re.compile(ssep)
        rv = dsep_re.sub('', raw_value)
        vals = ssep_re.split(rv)
        padded_zeroes = 3 - len(vals)
        splitted = [0]*padded_zeroes
        splitted.extend([int(v) for v in vals])
        return Duration.common_parser(splitted)

    @staticmethod
    def single_number_parser(raw_value, attrs = {}):
        """
            single_number_parser(value)

            parses objects like '(7)' or '(15)', assigning the number to the
            minute value.
        """
        v = int(raw_value)
        splitted = [0, v, 0]
        return Duration.common_parser(splitted)

    @classmethod
    def create(cls, raw_value, parser=None, attrs={}):
        if not parser:
            parser = Duration.colon_parser
        result = cls(__UNK__)
        if raw_value != __UNK__:
            cooked_value = parser(raw_value, attrs)
            result = cls(cooked_value)
        return result
