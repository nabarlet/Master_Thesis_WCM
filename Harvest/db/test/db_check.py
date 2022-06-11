
import sys,os

mypath = os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, '..'), os.path.join(mypath, *(['..']*2), 'cherrypick')])

from db import DbPro, DbDev

dbp = DbPro()
count = dbp.check_consistency()
print("%d inconsistent records found on DbPro" % (count), file=sys.stderr)

dbd = DbDev()
count = dbd.check_consistency()
print("%d inconsistent records found on DbDev" % (count), file=sys.stderr)
