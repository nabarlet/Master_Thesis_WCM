from common.objects.object_base import ObjectBase

class Duration(ObjectBase):
    def __init__(self, raw_value):
        self.raw_value = raw_value

    def __str__(self):
        # return "%02d:%02d:%02d" % (self.hours, self.minutes, self.seconds)
        return self.raw_value

    def to_seconds(self):
        pass
#       return (self.hours * 3600) + (self.minutes * 60) + self.seconds

    def inspect(self):
        return "Duration: %s" % (self.raw_value)
