import pdb
import sys, os
import datetime as dt

mypath = os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, *(['..']*2)), os.path.join(mypath, *(['..']*3))])

import common.objects as obj
from common.utilities.date import date
from db.db import DbDev, DbPro

class ComposerPerformance(obj.ObjectBase):

    __DB_TABLE_NAME__ = 'composer_performance'
    def __init__(self,composer_id, performance_id):
        super(ComposerPerformance, self).__init__(ComposerPerformance.__DB_TABLE_NAME__)
        self.composer_id = composer_id
        self.performance_id = performance_id

    def query_by_composer_id_and_performance_id(self, db = None):
        result = None
        query = "SELECT * FROM %s WHERE composer_id = %d AND performance_id = %d" % (ComposerPerformance.__DB_TABLE_NAME__, self.composer_id, self.performance_id)
        results = self.sql_execute(query, db)
        if len(results) > 0:
            (id, composer_id, performance_id) = results[0]
            result = ComposerPerformance(composer_id, performance_id)
        return result

    def insert(self):
        args = (('composer_id', 'integer', 'non null'), ('performance_id', 'integer', 'non null'))
        properties = [('FOREIGN KEY(composer_id) REFERENCES composer(id)'), ('FOREIGN KEY(performance_id) REFERENCES performance(id)')]
        self.create_table(args, properties)
        j_string = "INSERT INTO %s (composer_id, performance_id) VALUES (%d, %d);" % (ComposerPerformance.__DB_TABLE_NAME__, self.composer_id, self.performance_id)
        self.db_dev.sql_execute(j_string)

    @staticmethod
    def clear_composer_performances_of_provider(provider):
        result = None
        db = DbDev()
        prov = obj.Providers.query_by_name(provider)
        d_string = "DELETE FROM %s WHERE performance_id IN (SELECT performance.id FROM performance,provider WHERE provider.name = '%s' AND performance.provider_id = provider.id)" % (ComposerPerformance.__DB_TABLE_NAME__, provider)
        db.sql_execute(d_string)
        return prov.id

class NoSuchComposer(Exception):
    pass

class Composer(obj.ObjectBase):

    __DB_TABLE_NAME__ = 'composer'
    def __init__(self,name,birth=None,death=None,movement=None, perf_date=None, nid=None, id=None):
        super(Composer, self).__init__(Composer.__DB_TABLE_NAME__)
        self.nid = nid
        self.name=name
        self.birth=birth
        self.death=death
        self.movement=movement
        self.perf_date = perf_date
        self.id = id
        
    def inspect(self):
        return "Composer: id: %s, name: %s, birth: %s, death: %s, movement: %s, performance date: %s" %(self.nid, self.name,self.birth,self.death,self.movement, self.perf_date)
        
    def to_csv(self):
        return "%s,\"%s\",%s,%s,\"%s\",%s" % (self.nid, self.name,self.birth,self.death,self.movement,self.perf_date)

    def birthdate(self):
        return date(self.birth)

    def deathdate(self):
        result = None
        if self.death:
            result = date(self.death)
        return result

    def end_date(self):
        result = dt.date.today()
        if self.death:
            result = self.deathdate()
        return result

    def age(self):
        end = self.end_date()
        start = self.birthdate()
        delta = end - start
        years = int(delta.days / float(365.25)) # crude way to keep track of bisextile years
        return years

    @classmethod
    def query(cls, nid, db = DbDev()):
        result = None
        q_string = "SELECT * FROM %s WHERE nid = '%s';" % (Composer.__DB_TABLE_NAME__, nid)
        results = db.query(q_string)
        if len(results) > 0:
            (id, name, birth, death, nid, movement_id) = results[0]
            mov = obj.TimeLine.query_by_id(movement_id).key
            result = cls(name, birth, death, mov, None, nid, id)
        return result

    @classmethod
    def query_by_name(cls, name, db = DbDev()):
        result = None
        q_string = "SELECT * FROM %s WHERE name = '%s' COLLATE NOCASE;" % (Composer.__DB_TABLE_NAME__, name)
        results = db.query(q_string)
        if results and len(results) > 0:
            (id, name, birth, death, nid, movement_id) = results[0]
            mov = obj.TimeLine.query_by_id(movement_id).key
            result = cls(name, birth, death, mov, None, nid, id)
        return result

    def insert(self, provider):
        """
            insert(provider)

            will insert a composer record in the database, checking:
            a) that the record does not exist yet
            b) that the composer object is not corrupted (has birthdate, etc.)

            After insertion, it will create a link to a specific performance
        """
        args = (('name', 'text', 'non_null'), ('birth', 'text', 'non null'), ('death', 'text'), ('nid', 'text', 'non null'), ('movement_id', 'integer', 'non null'))
        properties = [('FOREIGN KEY(movement_id) REFERENCES movement(id)')]
        self.create_table(args, properties)
        c_exists = self.query(self.nid)
        if not c_exists:
            if self.birthdate():
                mov = obj.TimeLine.query_by_name(self.movement)
                i_string = "INSERT INTO %s (name, birth, death, nid, movement_id) VALUES (\"%s\", '%s', '%s', '%s', %d);" % (Composer.__DB_TABLE_NAME__, self.name, self.birthdate(), self.deathdate(), self.nid, mov.id)
                self.db_dev.sql_execute(i_string)
                self.link_to_performance(provider)
        else:
            self.link_to_performance(provider)

    def link_to_performance(self, provider):
        perf = obj.Performance(self.perf_date, provider)
        perf.insert()
        perf = obj.Performance.query_by_datetime_and_provider(self.perf_date, provider, self.db_dev)
        cid = self.id
        if not cid:
             c = Composer.query(self.nid)
             if c:
                  cid = c.id
             else:
                  raise NoSuchComposer(self.name)
        join = ComposerPerformance(cid, perf.id)
        join.insert()
