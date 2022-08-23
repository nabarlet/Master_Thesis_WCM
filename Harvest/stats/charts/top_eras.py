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
        egquery = "SELECT M.name, count (C.id) from movement as M JOIN composer as C, record as R, record_performance as RP, performance as P, provider as PR WHERE C.movement_id = M.id AND RP.performance_id = P.id AND RP.record_id = R.id AND R.composer_id = C.id AND P.provider_id < 4 group by M.name order by count(P.id) DESC;"
        (y, ylabels) = self.make_top_common(egquery)
        barhplot(y, ylabels, 'Top_global_eras.png', 'Eras global popularity', plotdir = self.plotdir, limit = None, fontsize = 30)

    def make_top_radio_eras(self):
        radios = TopEras.load_providers()
        for rid, rname in radios:
            lquery = "SELECT M.name, count (C.id) from movement as M JOIN composer as C, record as R, record_performance as RP, performance as P, provider as PR WHERE C.movement_id = M.id AND RP.performance_id = P.id AND RP.record_id = R.id AND R.composer_id = C.id AND P.provider_id = %d group by M.name order by count(P.id) DESC;" %(rid) 
            filename = "Eras_%s_pop.png" % (rname)
            plot_title = "Eras %s popularity" % (rname) 
            (y, ylabels) = self.make_top_common(lquery)
            barhplot(y, ylabels, filename, plot_title, plotdir = self.plotdir, limit = None, fontsize=30)

    def make_top_common(self, query):
        results = self.db.query(query)
        ylabels = [item[0] for item in results]
        y       = [item[1] for item in results]
        return (y, ylabels)
