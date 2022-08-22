import pdb

import sys, os

mypath=os.path.join(os.path.dirname(__file__))
sys.path.extend([os.path.join(mypath, '..'), os.path.join(mypath, *['..']*2)])

from db.db import DbDev
from common.utilities.bump import Bump

b = Bump()
db = DbDev()
rquery = 'SELECT R.id,P.id,RP.id from record as R join performance as P, record_performance AS RP Where P.provider_id = 2 and P.id = RP.performance_id and R.id = RP.record_id;'
results = db.query(rquery)

bumps   = ['/', '-', '\\']
for rid, pid, rpid in results:
    rquery = "DELETE FROM record WHERE id = %d" % (rid)
    pquery = "DELETE FROM performance WHERE id = %d" % (pid)
    rpquery = "DELETE FROM record_performance WHERE id = %d" % (rpid)
    for idx, q in enumerate([rquery, pquery, rpquery]):
        db.sql_execute(q)
        b.bump(bumps[idx])
