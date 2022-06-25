import sys,os
from db import DbDev, DbPro

db = DbDev()

if len(sys.argv) > 1:
    dbname = sys.argv[1]
    db = eval(dbname)()

res = db.check_consistency()
print("%d composers have no performance in db %s!" % (res, os.path.basename(db.dbname)), file=sys.stderr)
