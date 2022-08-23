import pdb
import sys,os

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, '.'), os.path.join(mypath, *['..']*2)])

from charts.chart import Chart
from charts.barhplot import barhplot

class TopEras(Chart):

    def __init__(self, ylimit = 60, xlimit = None, rootpath = '.'):
        super().__init__(ylimit = ylimit, xlimit = xlimit, rootpath = rootpath)
        self.eras = TopEras.load_eras()

    @classmethod
    def create(cls, ylimit = 60, xlimit = None, rootpath = '.'):
        tc = cls(ylimit, xlimit, rootpath)
        tc.make_top_eras()

    def make_top_eras(self):
        self.make_top_global_era()
        self.make_top_radio_eras()

    def make_top_global_era(self):
        egquery = "SELECT M.id,M.name,count(M.id) FROM movement AS M JOIN composer AS C, record AS R, record_performance AS RP, performance AS P WHERE M.id = %d AND C.movement_id = M.id AND R.composer_id = R.id AND RP.performance_id = P.id AND RP.record_id = R.id;"
        (y, ylabels) = self.make_top_common(egquery)
        barhplot(y, ylabels, 'Top_global_eras.png', 'Eras global popularity', plotdir = self.plotdir, limit = None, fontsize = 30)

    def make_top_radio_eras(self):
        radios = TopEras.load_providers()
        for rid, rname in radios:
            lquery_tail = " AND P.provider_id = %d;" % (rid)
            lquery = "SELECT M.id,M.name,count(M.id) FROM movement AS M JOIN composer AS C, record AS R, record_performance AS RP, performance AS P WHERE M.id = %d AND C.movement_id = M.id AND RP.record_id = R.id AND R.composer_id = C.id AND RP.performance_id = P.id " + lquery_tail 
            filename = "Eras_%s_pop.png" % (rname)
            plot_title = "Eras %s popularity" % (rname) 
            (y, ylabels) = self.make_top_common(lquery)
            barhplot(y, ylabels, filename, plot_title, plotdir = self.plotdir, limit = None, fontsize = 30)

    def make_top_common(self, query):
        results = []
        for cid, cname in self.eras:
            era = self.db.query(query % (cid))
            results.append(era)

        results = sorted(results, key=lambda x:x[0][2], reverse=True)
        ylabels = [item[0][1] for item in results]
        y       = [item[0][2] for item in results]
        return (y, ylabels)
