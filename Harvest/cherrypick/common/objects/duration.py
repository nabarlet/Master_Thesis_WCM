import pdb
import sys,os
import datetime as dt

mypath=os.path.dirname(__file__)
sys.path.append(os.path.join(mypath, *['..']*2))

from common.objects.object_base import ObjectBase
from common.utilities.string import __UNK__

class DurationValueError(ValueError):
    pass

class Duration(ObjectBase):
    def __init__(self, value):
        if value != __UNK__ and type(value) is not dt.timedelta:
            raise DurationValueError(value)
        self.__dur__ = value

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
        hours = mins = secs = 0
        if len(hms_list) == 3:
            (hours, mins, secs) = hms_list
        elif len(hms_list) == 2:
            (mins, secs) = hms_list
        else:
            secs = hms_list[0]
        return dt.timedelta(hours=hours, minutes=mins, seconds=secs)

    @staticmethod
    def colon_parser(raw_value):
        splitted = raw_value.split(':')
        splitted = [int(s) for s in splitted]
        return Duration.common_parser(splitted)

    @staticmethod
    def dot_parser(raw_value):
        splitted = raw_value.split('.')
        splitted = [int(s) for s in splitted]
        return Duration.common_parser(splitted)


    @staticmethod
    def h_dot_parser(raw_value):
        s1 = raw_value.split('h')
        s2 = s1[1].split('.')
        splitted = [s1[0]]
        splitted.extend(s2)
        splitted = [int(s) for s in splitted]
        return Duration.common_parser(splitted)

    @classmethod
    def create(cls, raw_value, parser=None):
        if not parser:
            parser = Duration.colon_parser
        result = cls(__UNK__)
        if raw_value != __UNK__:
            result = cls(parser(raw_value))
        return result
