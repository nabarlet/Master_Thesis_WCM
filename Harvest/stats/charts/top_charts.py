import pdb
import sys,os

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, '.'), os.path.join(mypath, *['..']*2)])

from charts.chart import Chart
from charts.barhplot import barhplot

class TopCharts(Chart):

    def __init__(self, ylimit = 60, xlimit = None, rootpath = '.'):
        super().__init__(ylimit = ylimit, xlimit = xlimit, rootpath = rootpath)
        self.composers = TopCharts.load_composers()

    @classmethod
    def create(cls, ylimit = 60, xlimit = None, rootpath = '.'):
        tc = cls(ylimit, xlimit, rootpath)
        tc.make_top_charts()

    def make_top_charts(self):
        self.make_top_global_chart()
        self.make_top_radio_charts()

    def make_top_global_chart(self):
        total = TopCharts.load_total_performances()[0][0]
        gquery = """SELECT C.id,C.name,count(*) FROM composer AS C JOIN record AS R, record_performance AS RP, performance AS P
                    WHERE R.composer_id = C.id AND C.id = %d AND RP.record_id = R.id AND RP.performance_id = P.id;"""
        (y, ylabels) = self.make_top_common(gquery)
        # y = [(yitem/float(total))*100 for yitem in y]
        barhplot(y, ylabels, 'Top_%d_global_pop.png', 'Top %d global popularity', plotdir = self.plotdir)

    # SINGLE_PROV_XLIMIT = 600
    SINGLE_PROV_XLIMIT = None
    def make_top_radio_charts(self):
        radios = TopCharts.load_providers()
        for rid, rname in radios:
            total = TopCharts.load_total_performances(rid)[0][0]
            lquery_tail = " AND P.provider_id = %d;" % (rid)
            lquery = "SELECT C.id,C.name,count(*) FROM composer AS C JOIN record AS R, record_performance AS RP, performance AS P WHERE R.composer_id = C.id AND C.id = %d AND RP.record_id = R.id AND RP.performance_id = P.id" + lquery_tail 
            filename = 'Top_%d_' + ("%s_pop.png" % (rname))
            plot_title = 'Top %d ' + ("%s popularity" % (rname)) 
            (y, ylabels) = self.make_top_common(lquery)
            # y = [(yitem/float(total))*100 for yitem in y]
            barhplot(y, ylabels, filename, plot_title, plotdir = self.plotdir, xlimit = TopCharts.SINGLE_PROV_XLIMIT)

    def make_top_common(self, query):
        results = []
        for cid, cname in self.composers:
            comp = self.db.query(query % (cid))
            results.append(comp)

        results = sorted(results, key=lambda x:x[0][2], reverse=True)
        top     = results[0:self.ylimit]
        ylabels = [item[0][1] for item in top]
        y       = [item[0][2] for item in top]
        return (y, ylabels)
