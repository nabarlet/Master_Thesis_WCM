import pdb
from common.utilities.string import join
import common.objects as obj

class TimeSection:
    def __init__(self, title, time):
        self.time = time
        self.title_list = title
        self.recordings = []

    def append_recording(self, recording):
        if not istype(obj.Recording):
            raise obj.ObjectError("expected Recording object got %s" % (type(recording)))
        self.recordings.append(recording)

    def inspect(self):
        result = "class TimeSection:\t%s (%s)\n\n\n" % (self.title_list, self.time)
        # result += join([(r.inspect() + '\n\n') for r in self.recordings], '')
        return result.rstrip()
