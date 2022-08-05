import pdb

import sys,os

mypath = os.path.dirname(__file__)
sys.path.append(os.path.join(mypath, '..'))

from db.db import DbPro
from charts.barhplot import barhplot

db = DbPro()

#
# era query
#
equery = "SELECT M.id, M.name FROM movement AS M WHERE M.parent_id IS NULL ORDER BY M.id;"
eras   = db.query(equery)

#
# global chart
#
egquery = "SELECT M.id,M.name,count(M.id) FROM movement AS M JOIN composer AS C, composer_performance AS CP, performance AS P WHERE M.id = %d AND C.movement_id = M.id AND CP.composer_id = C.id AND CP.performance_id = P.id;"
barhplot(eras, egquery, 'Top_global_eras.png', 'Eras global popularity', rootpath = mypath, limit = None)

#
# single radio charts
#
SINGLE_PROV_XLIMIT = 600
rquery = "SELECT P.id,P.name FROM provider AS P JOIN provider_type AS PT WHERE P.type_id = PT.id AND PT.type = 'radio';"
radios = db.query(rquery)
for rid, rname in radios:
    lquery_tail = " AND P.provider_id = %d;" % (rid)
    lquery = "SELECT M.id,M.name,count(M.id) FROM movement AS M JOIN composer AS C, composer_performance AS CP, performance AS P WHERE M.id = %d AND C.movement_id = M.id AND CP.composer_id = C.id AND CP.performance_id = P.id " + lquery_tail 
    filename = "Eras_%s_pop.png" % (rname)
    plot_title = "Eras %s popularity" % (rname) 
    barhplot(eras, lquery, filename, plot_title, xlimit = SINGLE_PROV_XLIMIT, rootpath = mypath, limit = None)
