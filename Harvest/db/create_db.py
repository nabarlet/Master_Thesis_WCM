import sys
from db import Db

if len(sys.argv) < 2:
    print("Usage: python3 %s <file name>" % (sys.argv[0]), file=sys.stderr)
    sys.exit(-1)

DATABASE_NAME=sys.argv[1]

dbase = Db.connect(DATABASE_NAME)

dbase.create_table('composer', (('name', 'non_null'), ('nid', 'non_null'),  ('birth', 'datetime', 'non_null'), ('death', 'datetime'), ('movement_id', 'foreign_key', 'non_null')))
dbase.create_table('movement', ('name', ('start', 'year', 'non_null'), ('end', 'year')))
