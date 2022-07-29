import pdb

import sys,os
import matplotlib.pyplot as plt

mypath = os.path.dirname(__file__)
sys.path.append(os.path.join(mypath, '..'))

from db.db import DbPro
db = DbPro()

def barhplot(comps, query, filename_template, title, limit = 60):
    plotdir = os.path.join(mypath, './plots')
    results = []
    for cid, name in comps:
        comp = db.query(query % (cid))
        results.append(comp)
        
    results = sorted(results, key=lambda x:x[0][2], reverse=True)
    top     = results[0:limit]
    ylabels = [item[0][1] for item in top]
    y       = [item[0][2] for item in top]
    y.reverse()
    ylabels.reverse()
    x = range(len(y))
    fig, ax = plt.subplots()
    fig.set_figwidth(11.5)
    fig.set_figheight(15.3)
    plt.barh(x,y)
    plt.yticks(x, ylabels)
    plt.title(title % (limit))
    filename = filename_template % (limit)
    plt.savefig(os.path.join(plotdir, filename), bbox_inches='tight')

    return results

#
# composer query
#
cquery = "SELECT C.id, C.name FROM composer AS C;"
composers = db.query(cquery)

#
# global chart
#
gquery = "SELECT C.id,C.name,count(*) FROM composer AS C JOIN composer_performance AS CP WHERE CP.composer_id = C.id AND C.id = %d;" 
barhplot(composers, gquery, 'Top_%d_global_pop.png', 'Top %d global popularity')

#
# single radio charts
#
rquery = "SELECT P.id,P.name FROM provider AS P JOIN provider_type AS PT WHERE P.type_id = PT.id AND PT.type = 'radio';"
radios = db.query(rquery)
for rid, rname in radios:
    lquery_tail = " AND P.provider_id = %d;" % (rid)
    lquery = "SELECT C.id,C.name,count(*) FROM composer AS C JOIN composer_performance AS CP, performance AS P WHERE CP.composer_id = C.id AND C.id = %d" + lquery_tail 
    filename = 'Top_%d_' + ("%s_pop.png" % (rname))
    plot_title = 'Top %d' + ("%s popularity" % (rname)) 
    barhplot(composers, lquery, filename, plot_title)
