import pdb
import re

class ObjectBase:

    @classmethod
    def cleanse_string(cls, string):
        """
            +cleanse_string():+
    
            needed to cleanup the title from commas, quotes, etc.
        """
        escape_meta_re = re.compile('([,"])')
        result = escape_meta_re.sub('\\\\\\1', string)
        return result

class Record(ObjectBase):
    def __init__(self,comp,perfs,title,date):
        self.composer=comp
        self.performers=perfs
        self.title=title
        self.date=date
        
    def inspect(self):
        return "composer: %s, performers: %s, title: \"%s\", date: %s" % (self.composer.inspect(), self.performers, self.title, self.date)
        
    def to_csv(self):
        return "%s,\"%s\",%s" % (self.composer.to_csv(),self.__class__.cleanse_string(self.title),self.date)
        
class Composer(ObjectBase):
    def __init__(self,name,birth=None,death=None,movement=None):
        self.name=name
        self.birth=birth
        self.death=death
        self.movement=movement
        
    def inspect(self):
        return "name: %s, birth: %s, death: %s, movement: %s" %(self.name,self.birth,self.death,self.movement)
        
    def to_csv(self):
        return "\"%s\",%s,%s,\"%s\"" % (self.name,self.birth,self.death,self.movement)
