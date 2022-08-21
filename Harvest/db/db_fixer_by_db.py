import pdb
import csv
import sys, os

mypath=os.path.dirname(__file__)
sys.path.append(mypath)

from db import DbDev
from db_fixer_by_csv import DbFixer

if len(sys.argv) < 2:
    print("Usage: %s <Provider name>" % (os.path.basename(sys.argv[0])), file=sys.stderr)
    sys.exit(-1)
dbf = DbFixer(sys.argv[1])
dbf.fix_by_db()
