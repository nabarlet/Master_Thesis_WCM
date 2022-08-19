import sys, os
import re

mypath = os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, *(['..']*2)), os.path.join(mypath, *(['..']*3))])

try:
    from db.db import DbDev, DbPro
except ModuleNotFoundError:
    from db import DbDev, DbPro

from common.utilities.bump   import Bump

class ObjectBase:

    def __init__(self, tn = None):
        self.db_dev = DbDev()
        self.db_pro = DbPro()
        self.table_name = tn
        self.bump = Bump()

    @staticmethod
    def cleanse_string(string):
        """
            +cleanse_string():+
    
            needed to cleanup the title from commas, quotes, etc.
        """
        escape_meta_re = re.compile('([,"])')
        result = escape_meta_re.sub('\\\\\\1', string)
        return result

    def sql_execute(self, string, values = (), db = None):
        if not db:
            db = self.db_dev
        db.execute(string, values)

    def table_exists(self, db = None):
        result = None
        if self.table_name:
            sql_string = '.table %s' % (self.table_name)
            result = self.sql_execute(sql_string, db = db)
        return result

    def create_table(self, fields, properties = ()):
        self.db_dev.create_table(self.table_name, fields, properties)

    def table_size(self, db = None):
        if not db:
            db = self.db_dev
        return db.table_size(self.table_name)

    def select_all(self, db = None):
        sql_string = 'SELECT * FROM %s' % (self.table_name)
        return self.sql_execute(sql_string, db = db)

    def table_exists(self, db = None):
        result = None
        if self.table_name:
            sql_string = '.table %s' % (self.table_name)
            result = self.sql_execute(sql_string, db = db)
        return result

    @classmethod
    def create_from_db(cls):
        result = cls()
        result.load_records() 
        return result
