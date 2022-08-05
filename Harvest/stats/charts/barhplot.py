import os
import matplotlib.pyplot as plt
from db.db import DbPro
db = DbPro()

def barhplot(comps, query, filename_template, title, limit = 60, xlimit = None, rootpath = '.'):
    plotdir = os.path.join(rootpath, './plots')
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
    if limit:
        title = title % (limit)
        filename_template = filename_template % (limit)
    plt.title(title)
    if xlimit and limit:
        plt.axis([0, xlimit, -1, limit+1])
    filename = filename_template
    plt.savefig(os.path.join(plotdir, filename), bbox_inches='tight')

    return top
