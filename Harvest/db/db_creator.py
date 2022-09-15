import pdb
import sys, os
import csv

mypath = os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, '..'), os.path.join(mypath, '..', 'cherrypick')])

from db import DbDev, __DEFAULT_DEV_DB__
import common.objects as obj
from common.utilities.bump import Bump

class DbCreator:

    def __init__(self, db = DbDev()):
        self.db = db
        self.bump = Bump()
        
    def reset(self):
        os.remove(self.db.dbname)
        self.create_db_from_scratch()

    __SCHEMA_PATH__ = os.path.join(mypath, 'data', 'db_schema.txt')
    def create_db_from_scratch(self):
        with open(self.db.dbname, 'w') as dummy: # this is just to create an empty file :-(
            pass

        self.db.reopen()
        dblines = []
        with open(DbCreator.__SCHEMA_PATH__, 'r') as dbsfh:
            dblines = dbsfh.readlines()
            dblines = [l.rstrip() for l in dblines]

        for line in dblines:
            self.db.sql_execute(line)


    @classmethod
    def create(cls, db = DbDev()):
        dbc = cls(db)
        dbc.reset()
        for data in dbc.read_csvs(): 
            try:
	            record = obj.Record.from_csv(data)
	            if record:
	                record.insert(db=db)
            except Exception as e:
                print("Error --> %s" % (str(e)), file=sys.stderr)

    @classmethod
    def create_single(cls, provider, db = DbDev()):
        dbc = cls(db)
        csvfile = DbCreator.__CSVS__[provider]
        for data in dbc.read_csv(csvfile, db=db): 
            try:
	            record = obj.Record.from_csv(data)
	            if record:
	                record.insert(db=db)
            except Exception as e:
                print("Error --> %s" % (str(e)), file=sys.stderr)

    def read_csv(self, csvfile, db = DbDev()):
        with open(csvfile, 'r') as csvfh:
            csvreader = csv.reader(csvfh, delimiter=',', quotechar='"')
            for csvline in csvreader:
                yield csvline

    __DATA_PATH__ = os.path.join(mypath, '..', 'cherrypick')
    __CSVS__ = {
        'RAI_RadioClassica': os.path.join(__DATA_PATH__, 'RAI_RadioClassica', 'RRC_clean.csv'),
        'BBC3':              os.path.join(__DATA_PATH__, 'BBC3', 'BBC_clean.csv'),
        'RadioC':            os.path.join(__DATA_PATH__, 'RadioC', 'RC_clean.csv'),
    }
    def read_csvs(self):
        for csvfile in DbCreator.__CSVS__.values():
            for csvline in self.read_csv(csvfile, db = db):
                yield csvline

if __name__ == '__main__':
    if len(sys.argv) < 2:
        ans = 'n'
        print("Attempting to re-create full database from scratch. Are you sure? [y|n]")
        ans = input()
        if ans == 'y' or ans == 'Y':
            DbCreator.create()
        else:
            sys.exit(-1)
    else:
        DbCreator.create_single(sys.argv[1])
