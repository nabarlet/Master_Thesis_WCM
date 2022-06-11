from common.utilities.string import join

class Performer:
    def __init__(self, name):
        self.name = name
        self.role = None

    def inspect(self):
        result = "\t\t%s" % (join(self.name))
        if self.role:
            result += ", role: %s" % (self.role)
        return result + "\n"
