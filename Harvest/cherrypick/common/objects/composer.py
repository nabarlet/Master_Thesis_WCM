import pdb
import sys, os
import datetime as dt

mypath = os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, *(['..']*2)), os.path.join(mypath, *(['..']*3))])

import common.objects as obj
from common.utilities.date import date
from common.objects.provider import Providers
from common.utilities.composer_plot  import ComposerPlot
from common.utilities.bump   import Bump
try:
    from db.db import DbDev, DbPro
except ModuleNotFoundError:
    from db import DbDev, DbPro

class ComposerComposer(obj.ObjectBase):

    __DB_TABLE_NAME__ = 'composer_composer'
    def __init__(self, composer_1_id, composer_2_id, performance_id):
        super().__init__(ComposerComposer.__DB_TABLE_NAME__)
        self.composer_1_id = composer_1_id
        self.composer_2_id = composer_2_id
        self.performance_id = performance_id

    def inspect(self):
        result = 'ComposerComposer(composer_1_id = %d, composer_2_id = %d, performance_id = %d)' % (self.composer_1_id, self.composer_2_id, self.performance_id)
        return result

    def __str__(self, db = DbPro()):
        pass
        # TO BE DONE
        # c1 = 


    @classmethod
    def query_by_composers_and_performance(cls, c1id, c2id, pid, db = None):
        result = None
        query = "SELECT * FROM %s WHERE ((composer_1_id = %d AND composer_2_id = %d) OR (composer_1_id = %d AND composer_2_id = %d)) AND performance_id = %d" % (ComposerComposer.__DB_TABLE_NAME__, c1id, c2id, c2id, c1id, pid)
        results = self.sql_execute(query, db)
        if len(results) > 0:
            (id, comp1id, comp2id, perf_id) = results[0]
            result = cls(comp1id, comp2id, perf_id)
        return result

    def insert(self):
        args = (('composer_1_id', 'integer', 'non null'), ('composer_2_id', 'integer', 'non null'), ('performance_id', 'integer', 'non null'))
        properties = [('FOREIGN KEY(composer_1_id) REFERENCES composer(id)'), ('FOREIGN KEY(composer_2_id) REFERENCES composer(id)'), ('FOREIGN KEY(performance_id) REFERENCES performance(id)')]
        self.create_table(args, properties)
        j_string = "INSERT INTO %s (composer_1_id, composer_2_id, performance_id) VALUES (%d, %d, %d);" % (ComposerComposer.__DB_TABLE_NAME__, self.composer_1_id, self.composer_2_id, self.performance_id)
        self.db_dev.sql_execute(j_string)

    @staticmethod
    def clear_composer_composer_of_provider(provider):
        result = None
        db = DbDev()
        prov = obj.Providers.query_by_name(provider)
        d_string = "DELETE FROM %s WHERE performance_id IN (SELECT performance.id FROM performance JOIN provider WHERE provider.name = '%s' AND performance.provider_id = provider.id)" % (ComposerComposer.__DB_TABLE_NAME__, provider)
        db.sql_execute(d_string)
        return prov.id

    @classmethod
    def create_composer_composer_table(cls):
        b = Bump()
        db = DbDev()
        drop_query = "DROP TABLE IF EXISTS composer_composer;"
        db.query(drop_query)
        pnames = [p[0] for p in db.select_all('provider AS P JOIN provider_type AS PT', 'P.name', "WHERE P.type_id = PT.id AND PT.type = 'radio'")]
        providers = [Providers.query_by_name(p) for p in pnames]
        for p in providers:
            perfs = db.select_all('performance AS P', 'P.id', "WHERE P.provider_id = %d" % (p.id))
            for r in perfs:
                (perf_id, ) = r
                comps = db.select_all('composer AS C JOIN composer_performance AS CP, performance AS P', 'C.id', "WHERE CP.composer_id = C.id AND CP.performance_id = P.id AND P.id = %d ORDER BY P.datetime" % (perf_id))
                comps = [c[0] for c in comps] # need to explicitely bypass the 'select_all' generator and have the list of composers per performance
                for row, col in ComposerPlot.static_matrix_fill(comps):
                    c1id = row
                    c2id = col
                    cc = cls(c1id, c2id, perf_id)
                    cc.insert()
                b.bump()

    @classmethod
    def list(cls, db = DbPro()):
        """
            TO BE DONE
            download performance
            downlad all cc with p.id 
            create objects
            list names and nids
        """
        pass

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
    UNK = 'unknown'
    def __init__(self,name,birth=None,death=None,movement=None, perf_date=None, nid=None, id=None, country=UNK, gender=UNK, lat=UNK, long=UNK):
        super(Composer, self).__init__(Composer.__DB_TABLE_NAME__)
        self.nid = nid
        self.name=name
        self.birth=birth
        self.death=death
        self.movement=movement
        self.perf_date = perf_date
        self.id = id
        self.country = country
        self.gender = gender
        self.lat = lat
        self.long = long
        
    def inspect(self):
        return "Composer: id: %s, name: %s, birth: %s, death: %s, movement: %s, performance date: %s, country: %s, gender: %s, lat: %s, long: %s" %(self.nid, self.name,self.birth,self.death,self.movement, self.perf_date, self.country, self.gender, self.lat, self.long)
        
    def to_csv(self):
        return "%s,\"%s\",%s,%s,\"%s\",%s,%s,%s,%s,%s" % (self.nid, self.name,self.birth,self.death,self.movement,self.perf_date,self.country,self.gender, self.lat, self.long)

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
    def common_query(cls, qstring, db = DbPro()):
        result = None
        results = db.query(qstring)
        if results and len(results) > 0:
            (id, name, birth, death, nid, movement_id) = results[0]
            mov = obj.TimeLine.query_by_id(movement_id).key
            result = cls(name, birth, death, mov, None, nid, id)
        return result

    @classmethod
    def query(cls, nid, db = DbPro()):
        return cls.common_query("SELECT * FROM %s WHERE nid = '%s';" % (Composer.__DB_TABLE_NAME__, nid), db)

    @classmethod
    def query_by_name(cls, name, db = DbPro()):
        return cls.common_query("SELECT * FROM %s WHERE name = '%s' COLLATE NOCASE;" % (Composer.__DB_TABLE_NAME__, name), db)

    @classmethod
    def query_by_id(cls, id, db = DbPro()):
        return cls.common_query("SELECT * FROM %s WHERE id = %d;" % (Composer.__DB_TABLE_NAME__, id), db)

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
