import pdb
import sys, os
import datetime as dt

mypath = os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, *(['..']*2)), os.path.join(mypath, *(['..']*3))])

import common.objects as obj
from common.utilities.date import date
from common.objects.provider import Providers
from common.utilities.composer_plot  import ComposerPlot
from common.utilities.string         import __UNK__
from common.utilities.bwlist         import BWList
from common.wikid.geoinfo            import get_lat_long_address
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
        query = "SELECT * FROM %s WHERE ((composer_1_id = ? AND composer_2_id = ?) OR (composer_1_id = ? AND composer_2_id = ?)) AND performance_id = ?" % (self.table_name)
        values = (c1id, c2id, c2id, c1id, pid)
        results = self.sql_execute(query, values, db = db)
        if len(results) > 0:
            (id, comp1id, comp2id, perf_id) = results[0]
            result = cls(comp1id, comp2id, perf_id)
        return result

    def insert(self):
        j_string = "INSERT INTO %s (composer_1_id, composer_2_id, performance_id) VALUES (?, ? , ?);" % (self.table_name)
        values = (self.composer_1_id, self.composer_2_id, self.performance_id)
        self.db_dev.sql_execute(j_string, values)

    @staticmethod
    def clear_composer_composer_of_provider(provider):
        result = None
        db = DbDev()
        prov = obj.Providers.query_by_name(provider)
        d_string = "DELETE FROM %s WHERE performance_id IN (SELECT performance.id FROM performance JOIN provider WHERE provider.name = ? AND performance.provider_id = provider.id)" % (self.table_name)
        values = (provider)
        db.sql_execute(d_string, values)
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
        query = "SELECT * FROM %s WHERE composer_id = ? AND performance_id = ?" % (self.table_name)
        values = (self.composer_id, self.performance_id)
        results = self.sql_execute(query, values, db = db)
        if len(results) > 0:
            (id, composer_id, performance_id) = results[0]
            result = ComposerPerformance(composer_id, performance_id)
        return result

    def insert(self):
        j_string = "INSERT INTO %s (composer_id, performance_id) VALUES (?, ?);" % (self.table_name)
        values = (self.composer_id, self.performance_id)
        self.db_dev.sql_execute(j_string, values)

    @staticmethod
    def clear_composer_performances_of_provider(provider):
        result = None
        db = DbDev()
        prov = obj.Providers.query_by_name(provider)
        d_string = "DELETE FROM %s WHERE performance_id IN (SELECT performance.id FROM performance,provider WHERE provider.name = '%s' AND performance.provider_id = provider.id)" % (self.table_name, provider)
        db.sql_execute(d_string)
        return prov.id

class NoSuchComposer(Exception):
    pass

class Composer(obj.ObjectBase):

    __DB_TABLE_NAME__ = 'composer'
    def __init__(self,name,birth=None,death=None,movement=__UNK__, nid=None, id=None, country=__UNK__, gender=__UNK__, lat=__UNK__, long=__UNK__):
        super(Composer, self).__init__(Composer.__DB_TABLE_NAME__)
        self.nid = nid
        self.name=name
        self.birth=birth
        self.death=death
        self.movement=movement
        self.id = id
        self.country = country
        self.gender = gender
        self.lat = lat
        self.long = long
        self.check_geolocation()
        
    def inspect(self):
        return "Composer: id: %s, nid: %s, name: %s, birth: %s, death: %s, movement: %s, country: %s, gender: %s, lat: %s, long: %s" %(str(self.id), self.nid, self.name,self.birth,self.death,self.movement, self.country, self.gender, self.lat, self.long)
        
    def to_csv(self):
        return "%s,\"%s\",%s,%s,\"%s\",%s,\"%s\",%s,%s" % (self.nid, self.name,self.birth,self.death,self.movement,self.gender,self.country,self.lat,self.long)

    def anydate(self, d):
        result = None
        if d and d != 'None':
            result = date(d)
        return result

    def birthdate(self):
        return self.anydate(self.birth)

    def deathdate(self):
        return self.anydate(self.death)

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
    def common_query(cls, qstring, values, db = DbPro()):
        result = None
        results = db.query(qstring, values)
        if results and len(results) > 0:
            (id, name, birth, death, nid, movement_id, country, gender, lat, long) = results[0]
            mov = obj.TimeLine.query_by_id(movement_id).key
            result = cls(name, birth=birth, death=death, movement=mov, nid=nid, country=country, gender=gender, lat=lat, long=long, id=id)
        return result

    @classmethod
    def query_by_nid(cls, nid, db = DbPro()):
        values = (nid,)
        return cls.common_query("SELECT * FROM %s WHERE nid = ?;" % (Composer.__DB_TABLE_NAME__), values, db=db)

    @classmethod
    def query_by_name(cls, name, db = DbPro()):
        values = (name,)
        return cls.common_query("SELECT * FROM %s WHERE name = ? COLLATE NOCASE;" % (Composer.__DB_TABLE_NAME__), values, db=db)

    @classmethod
    def query_by_id(cls, id, db = DbPro()):
        values = (id,)
        return cls.common_query("SELECT * FROM %s WHERE id = ?;" % (Composer.__DB_TABLE_NAME__), values, db=db)

    def insert(self, db = DbDev()):
        """
            insert()

            will insert a composer record in the database, checking:
            a) that the record does not exist yet
            b) that the composer object is not corrupted (has birthdate, etc.)

            After insertion, it will create a link to a specific performance
        """
        result = self.query_by_nid(self.nid, db=db)
        if not result:
            if self.birthdate():
                mov = obj.TimeLine.query_by_name(self.movement)
                i_string = "INSERT INTO %s (name, birth, death, nid, movement_id, country, gender, lat, long) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);" % (self.table_name)
                values   = (self.name, self.birthdate(), self.deathdate(), self.nid, mov.id, self.country, self.gender, self.lat, self.long)
                db.sql_execute(i_string, values)
                self.bump.bump('c')
                result = self.query_by_nid(self.nid, db=db)

        return result

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

    def check_geolocation(self):
        """
           check_geolocation():

           in case lat and long are not known yet, we chack again with
           translated names
        """
        if self.lat == __UNK__ or self.long == __UNK__:
            bwl = BWList()
            new_country = bwl.is_white(self.country)
            (self.lat, self.long, throw_away) = get_lat_long_address(new_country)
