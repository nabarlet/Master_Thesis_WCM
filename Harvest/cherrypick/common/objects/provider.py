import pdb
import sys, os
import csv

mypath = os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, *(['..']*2)), os.path.join(mypath, *(['..']*3), 'db', 'create')])
import common.utilities.path as p
import common.objects as obj
try:
    from db.db import DbDev, DbPro
except ModuleNotFoundError:
    from db import DbDev, DbPro

class Provider:

    def __init__(self, name, nation, type_id, id = None):
        self.name = name
        self.nation = nation
        self.type_id = type_id
        self.id   = id

    def inspect(self):
        nncombo = "%s (%s)" % (self.name, self.nation)
        result = "%-40s (%d)" % (nncombo, self.id)
        return result

    def save_record(self, db, tn):
        res = Providers.query_by_name(self.name)
        if len(res) <= 0:
            i_string = "INSERT INTO %s (name, nation, type_id) VALUES ('%s', '%s')" % (tn, self.name, self.nation, self.type_id)
            db.sql_execute(i_string)

class Providers(obj.ObjectBase):

    __DB_TABLE_NAME__ = 'provider'

    def __init__(self):
        super(Providers, self).__init__(Providers.__DB_TABLE_NAME__)
        self.providers = []

    __PROVIDERS_DEFAULT_SOURCE_FILE__ = os.path.join(p.repo_path, 'other_data', 'Providers.csv')
    @classmethod
    def create_from_csv(cls, csv_file = __PROVIDERS_DEFAULT_SOURCE_FILE__, delimiter = ','):
        result = cls()
        with open(csv_file, 'r') as fh:
            reader = csv.reader(fh, delimiter=delimiter)
            for row in reader:
                this_node = Provider(row[0], row[1], row[2])
                result.providers.append(this_node)
        return result

    def inspect(self):
        result = ''
        for p in self.providers:
            result += ('\n' + p.inspect())
        return result

    def save_records(self):
        for p in self.providers:
            p.save_record(self.db_dev, Providers.__DB_TABLE_NAME__)

    def load_records(self, db = None):
        if not db:
            db = self.db_dev
        self.providers = [] # clear just in case
        for r in db.select_all(Providers.__DB_TABLE_NAME__):
            (id, name, nation) = r
            p = Provider(name, nation, id, type_id)
            self.providers.append(p)

    @classmethod
    def create(cls):
        result = None
        db = DbDev()
        args = ('name', 'nation')
        db.create_table(cls.__DB_TABLE_NAME__, args)
        if db.table_size(cls.__DB_TABLE_NAME__) == 0:
            result = cls.create_from_csv()
            result.save_records()
        #
        # we need to recreate from db anyway to have the ids
        # 
        result = cls.create_from_db()
        return result

    @classmethod
    def query_by_name(cls, name, db = None):
        result = None
        if not db:
            db = DbDev()
        q_string = "SELECT * FROM %s WHERE name = '%s';" % (cls.__DB_TABLE_NAME__, name)
        results = db.query(q_string)
        if len(results) > 0:
            (id, name, nation, type_id) = results[0]
            result = Provider(name, nation, type_id, id)
        return result
