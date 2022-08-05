import pdb

import sys,os

mypath = os.path.dirname(__file__)
sys.path.append(os.path.join(mypath, '..'))

from db.db import DbPro
from charts.barhplot import barhplot

db = DbPro()

#
# composer query
#
cquery = "SELECT C.id, C.name FROM composer AS C;"
composers = db.query(cquery)

#
# global chart
#
gquery = "SELECT C.id,C.name,count(*) FROM composer AS C JOIN composer_performance AS CP WHERE CP.composer_id = C.id AND C.id = %d ORDER BY count(*) DESC;" 
barhplot(composers, gquery, 'Top_%d_global_pop.png', 'Top %d global popularity', rootpath = mypath)

#
# single radio charts
#
SINGLE_PROV_XLIMIT = 600
rquery = "SELECT P.id,P.name FROM provider AS P JOIN provider_type AS PT WHERE P.type_id = PT.id AND PT.type = 'radio';"
radios = db.query(rquery)
for rid, rname in radios:
    lquery_tail = " AND P.provider_id = %d AND CP.performance_id = P.id;" % (rid)
    lquery = "SELECT C.id,C.name,count(*) FROM composer AS C JOIN composer_performance AS CP, performance AS P WHERE CP.composer_id = C.id AND C.id = %d" + lquery_tail 
    filename = 'Top_%d_' + ("%s_pop.png" % (rname))
    plot_title = 'Top %d ' + ("%s popularity" % (rname)) 
    barhplot(composers, lquery, filename, plot_title, xlimit = SINGLE_PROV_XLIMIT, rootpath = mypath)
