import pdb
from common.utilities.string import join
import common.objects as obj

class TimeSection:
    def __init__(self, title, time):
        self.time = time
        self.title_list = title

    def inspect(self):
        result = "class TimeSection:\t%s (%s)\n\n\n" % (self.title_list, self.time)
        return result.rstrip()
