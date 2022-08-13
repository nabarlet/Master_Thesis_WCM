import pdb
import common.objects as obj
from common.utilities.string import join, escape_quotes, __UNK__

class Recording:
    def __init__(self, comp = None, oi = None, title = None, perf = None, dur = __UNK__, label = __UNK__):
        self.composer = comp
        self.title = title
        self.other_info = oi
        self.duration = dur
        self.label = label
        self.performance = perf

    def inspect(self):
        result = "Recording:\n\tcomposer:\t" + self.composer.inspect() + '\n'
        result += "\ttitle:\t\t" + self.title + '\n'
        result += "\tother_info:\t" + self.other_info + '\n'
        result += "\tduration:\t" + self.duration.inspect() + '\n'
        result += "\tperformance:\t" + self.performance.inspect() + '\n'
        result += "\tlabel:\t\t" + self.label + '\n'
        return result

    def to_csv(self):
        return "%s,\"%s\",\"%s\",%s,\"%s\",%s" % (self.composer.to_csv(), escape_quotes(self.title), escape_quotes(str(self.other_info)), self.duration, self.label, self.performance.to_csv())
