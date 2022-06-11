import pdb
import sys, os
import datetime as dt

mypath = os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, *(['..']*2)), os.path.join(mypath, *(['..']*3))])

import common.objects as obj
from common.utilities.date import clean_datetime
from db.db import DbDev, DbPro

class Performance(obj.ObjectBase):

    __DB_TABLE_NAME__ = 'performance'
    def __init__(self, datetime, provider, id = None):
        super(Performance, self).__init__(Performance.__DB_TABLE_NAME__)
        self.datetime = datetime
        self.provider = provider
        self.id = id
        
    def inspect(self):
        return "Performance: id: %d, date and time: %s, provider: %s" %(self.id, self.datetime, self.provider)
        
    @classmethod
    def query_by_datetime_and_provider(cls, datetime, provider, db = DbPro()):
        result = None
        prov = obj.Providers.query_by_name(provider)
        q_string = "SELECT * FROM %s WHERE datetime = '%s' AND provider_id = %d;" % (cls.__DB_TABLE_NAME__, clean_datetime(datetime), prov.id)
        results = db.query(q_string)
        if len(results) > 0:
            (id, datetime, provider_id) = results[0]
            result = cls(datetime, prov.name, id)
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

    def insert(self):
        args = (('datetime', 'text', 'non_null'), ('provider_id', 'integer', 'non null'))
        properties = [('FOREIGN KEY(provider_id) REFERENCES provider(id)'), ('UNIQUE(datetime, provider_id)')]
        self.create_table(args, properties)
        p_exists = Performance.query_by_datetime_and_provider(self.datetime, self.provider, db=self.db_dev)
        if not p_exists:
            prov = obj.Providers.query_by_name(self.provider)
            i_string = "INSERT INTO %s (datetime, provider_id) VALUES ('%s', %d);" % (Performance.__DB_TABLE_NAME__, clean_datetime(self.datetime), prov.id)
            self.db_dev.sql_execute(i_string)
