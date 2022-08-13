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
    def colon_parser(raw_value):
        hours = mins = secs = 0
        splitted = raw_value.split(':')
        splitted = [int(s) for s in splitted]
        if len(splitted) == 3:
            (hours, mins, secs) = splitted
        elif len(splitted) == 2:
            (mins, secs) = splitted
        else:
            secs = splitted[0]
        return dt.timedelta(hours=hours, minutes=mins, seconds=secs)

    @staticmethod
    def dot_parser(raw_value):

    @classmethod
    def create(cls, raw_value, parser=None):
        if not parser:
            parser = Duration.colon_parser
        result = cls(__UNK__)
        if raw_value != __UNK__:
            result = cls(parser(raw_value))
        return result
