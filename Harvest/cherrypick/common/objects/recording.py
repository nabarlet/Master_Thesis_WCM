import pdb
import common.objects as obj
from common.utilities.string import join

class Recording:
    def __init__(self, comp = None, perfs = None, title = None, whenp = None, dur = None, label = None):
        self.composer = comp
        self.title = title
        self.movements = ''
        self.performers = perfs
        self.duration = dur
        self.label = label
        self.perf_date = whenp

    def append_performers(self, performer):
        if not istype(obj.Performer):
            raise obj.ObjectError("expected Performer object got %s" % (type(performer)))
        self.performers.append(performer)

    def inspect(self):
        result = "Recording:\n\tcomposer:\t" + self.composer.inspect() + '\n'
        result += "\ttitle:\t\t" + self.title + '\n'
        # result += ("movements:\t" + self.movements)
        # result += "performers:\n" + join([p.inspect() for p in self.performers], '')
        result += "\tduration:\t" + self.duration.inspect() + '\n'
        result += "\tlabel:\t\t" + self.label + '\n'
        return result

    def to_csv(self):
        return self.composer.to_csv()
