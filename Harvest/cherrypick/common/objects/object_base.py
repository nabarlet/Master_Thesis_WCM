import sys, os
import re

mypath = os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, *(['..']*2)), os.path.join(mypath, *(['..']*3))])

from db.db import DbDev, DbPro

class ObjectBase:

    def __init__(self, tn = None):
        self.db_dev = DbDev()
        self.db_pro = DbPro()
        self.table_name = tn

    @staticmethod
    def cleanse_string(string):
        """
            +cleanse_string():+
    
            needed to cleanup the title from commas, quotes, etc.
        """
        escape_meta_re = re.compile('([,"])')
        result = escape_meta_re.sub('\\\\\\1', string)
        return result

    def sql_execute(self, string, db = None):
        if not db:
            db = DbDev()
        db.execute(string)

    def table_exists(self, db = None):
        result = None
        if self.table_name:
            sql_string = '.table %s' % (self.table_name)
            result = self.sql_execute(sql_string, db)
        return result

    def create_table(self, fields, properties = ()):
        self.db_dev.create_table(self.table_name, fields, properties)

    def table_size(self, db = None):
        if not db:
            db = DbDev()
        return db.table_size(self.table_name)

    def select_all(self, db = None):
        sql_string = 'SELECT * FROM %s' % (self.table_name)
        return self.sql_execute(sql_string, db)

    def table_exists(self, db = None):
        result = None
        if self.table_name:
            sql_string = '.table %s' % (self.table_name)
            result = self.sql_execute(sql_string, db)
        return result

    @classmethod
    def create_from_db(cls):
        result = cls()
        result.load_records() 
        return result
