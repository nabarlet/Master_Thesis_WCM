import pdb
import common.objects as obj
from common.utilities.string import join

class File:
    def __init__(self):
        self.date = None
        self.time_sections = []
        self.anniversaries = []

    def append_time_section(self, tsection):
        if type(tsection) is not obj.TimeSection:
            raise obj.ObjectError("expected TimeSection object got %s" % (type(tsection)))
        self.time_sections.append(tsection)

    def append_anniversary(self, ann):
        if type(ann) is not obj.Anniversary:
            raise obj.ObjectError("expected Anniversary object got %s" % (type(ann)))
        self.anniversaries.append(ann)

    def set_date(self, datestring):
        self.date = datestring

    def inspect(self):
        res = "%s:\t\tParsed palimpsest: %s\n\n" % ('class File', self.date)
        # res += (join([a.inspect() for a in self.anniversaries], '') + '\n\n')
        # res += (join([ts.inspect() for ts in self.time_sections], '') + '\n\n')
        return res.rstrip()
