import pdb
import sys, os
import datetime as dt

mypath = os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, *(['..']*2)), os.path.join(mypath, *(['..']*3))])

import common.objects as obj
from common.utilities.date import clean_datetime
from common.utilities.string import __UNK__
try:
    from db.db import DbDev, DbPro
except ModuleNotFoundError:
    from db import DbDev, DbPro

class Performance(obj.ObjectBase):

    __DB_TABLE_NAME__ = 'performance'
    def __init__(self, datetime, provider, title = __UNK__, id = None):
        super(Performance, self).__init__(Performance.__DB_TABLE_NAME__)
        self.datetime = datetime
        self.provider = provider
        self.title    = title
        self.id       = id
        self._records_= []

    def load_records(self, db = DbPro()):
        result = []
        if self.id:
            q_string = "SELECT record_id FROM %s AS RP WHERE RP.performance_id = ?;" % (obj.RecordPerformance.__DB_TABLE_NAME__)
            values = (self.id, )
            results = db.query(q_string, values)
            for rid in results:
                record = obj.Record.query_by_id(rid, perf=self, db=db)
                result.append(record)
        self._records_ = result
        return self._records_

    def records(self, db = DbPro()):
        if len(self._records_) == 0:
            self.load_records(db = db)
        return self._records_

    def to_csv(self):
        return "%s,%s,\"%s\",%s" % (self.provider,self.datetime,self.title,str(self.id))
        
    def inspect(self):
        return "Performance: id: %s, date and time: %s, provider: %s, title: %s" %(str(self.id), self.datetime, self.provider, self.title)
        
    @classmethod
    def query_by_datetime_and_provider(cls, datetime, provider, db = DbPro()):
        result = None
        prov = obj.Providers.query_by_name(provider)
        q_string = "SELECT * FROM %s WHERE datetime = ? AND provider_id = ?;" % (cls.__DB_TABLE_NAME__)
        values = (clean_datetime(datetime), prov.id)
        results = db.query(q_string, values)
        if len(results) > 0:
            (id, datetime, title, provider_id) = results[0]
            result = cls(datetime, prov.name, title=title, id=id)
            # result.load_records(db = db)
        return result

    @staticmethod
    def clear_performances_of_provider(provider):
        result = None
        db = DbDev()
        #
        # First clear binding links, then clear performance records
        #
        prov_id = obj.ComposerPerformance.clear_composer_performances_of_provider(provider)
        d_string = "DELETE FROM %s WHERE provider_id = %d" % (Performance.__DB_TABLE_NAME__, prov_id)
        db.sql_execute(d_string)
        return prov_id

    def insert(self, db=DbDev()):
        result = self.__class__.query_by_datetime_and_provider(self.datetime, self.provider, db=db)
        if not result:
            prov = obj.Providers.query_by_name(self.provider, db=db)
            i_string = "INSERT INTO %s (datetime, provider_id, title) VALUES (?, ?, ?);" % (Performance.__DB_TABLE_NAME__)
            values = (clean_datetime(self.datetime), prov.id, self.title)
            db.sql_execute(i_string, values)
            self.bump.bump('p')
            result = self.__class__.query_by_datetime_and_provider(self.datetime, self.provider, db=db)

        return result
