import pdb
import sys, os
import matplotlib.pyplot as plt
import datetime as dt

mypath=os.path.dirname(__file__)
sys.path.extend([os.path.join(mypath, '..'), os.path.join(mypath, '..', 'cherrypick')])

from common.utilities.bump import Bump

from playlist import Playlist, PlaylistStats
from movement_playlist import MovementPlaylist
from random_playlist import RandomPlaylist
from strict_path_playlist import StrictPathPlaylist 
from zone_playlist import ZonePlaylist
from movement_path_playlist import MovementPathPlaylist
from zone_path_playlist import ZonePathPlaylist
from path_playlist import PathPlaylist
from decorators import plotmethod, barmethod

class PlaylistGenerator:

    def __init__ (self, type_string, num=10):
        self.name = type_string
        self.type=eval(self.name)
        self.count=num
        self.stats=[]
        self.generated = False
        self.failed = 0
        self.action_time = dt.datetime.now().isoformat()[0:19]
        self.cache = Playlist.load_composers_from_cache()
      
    def generate(self):
        if not self.generated:
            b = Bump()
            for n in range(self.count):
                try:
                    pl = self.type.create_random_args(self.cache)
                    self.stats.append(pl.calc_stats())
                except Exception as e:
                    print("Playlist generation failed: %s" % (str(e)), file=sys.stderr)
                    self.failed += 1
                b.bump() 
            self.generated = True

    def header(self, stat):
        return "%s - %s (%s) (%d reiterations)" % (self.name, stat, self.action_time, self.count - self.failed)

    def filename(self, chart_type):
        return "%s_%s_%s_(%d_iterations).png" % (self.name, chart_type, self.action_time, self.count - self.failed)

    __DEFAULT_PLOT_DIR__ = os.path.join(mypath, 'plots')
    def create_plots(self, plotdir=__DEFAULT_PLOT_DIR__):
        self.generate()
        plots = [self.create_pop_average_plot, self.create_pop_median_plot, \
                 self.create_era_coverage_plot, self.create_composer_coverage_plot]
        for p in plots:
            p(plotdir)

    @plotmethod
    def create_pop_average_plot(self, plotdir):
        plot_name = 'pop_average'
        pavgs = [ps.pop_avg for ps in self.stats]
        return pavgs, self.header(plot_name), self.filename(plot_name), plotdir

    @plotmethod
    def create_pop_median_plot(self, plotdir):
        plot_name = 'pop_median'
        pmeds = [ps.pop_median for ps in self.stats]
        return pmeds, self.header(plot_name), self.filename(plot_name), plotdir

    @barmethod
    def create_era_coverage_plot(self, plotdir):
        plot_name = 'era_coverage'
        keys = ['Medieval', 'Renaissance', 'Baroque', 'Classical', 'Romantic', 'Modernism', 'Contemporary']
        result = {k:0.0 for k in keys}
        for s in self.stats:
            for key,val in s.eras_dist:
                result[key] += val
        statsz = len(self.stats)
        values = [result[k]/statsz for k in keys]
        return keys, values, self.header(plot_name), self.filename(plot_name), plotdir

    __MAX_COMPOSERS_PLOTTED__ = 60
    __MAX_COMPOSER_NAME_LEN__ = 50
    __NAME_DOTS__             = '...'
    @barmethod
    def create_composer_coverage_plot(self, plotdir):
        plot_name = 'composer_coverage'
        result = {}
        for s in self.stats:
            for key,val in s.composers_list:
                if key in result:
                    result[key] += val
                else:
                    result[key] = 1
        sorted_results = sorted(result.items(), key=lambda x:x[1], reverse=True)
        comp_limit = len(sorted_results)
        if comp_limit > PlaylistGenerator.__MAX_COMPOSERS_PLOTTED__:
            comp_limit = PlaylistGenerator.__MAX_COMPOSERS_PLOTTED__
        sorted_results = sorted_results[:comp_limit]
        statsz = float(len(self.stats))
        keys = []
        for k, v in sorted_results:
            maxname = len(k)
            name = k
            if len(k) > PlaylistGenerator.__MAX_COMPOSER_NAME_LEN__:
                maxname = PlaylistGenerator.__MAX_COMPOSER_NAME_LEN__ - len(PlaylistGenerator.__NAME_DOTS__)
                name = k[:maxname] + PlaylistGenerator.__NAME_DOTS__
            keys.append(name)
        values = [v/statsz for k,v in sorted_results]
        return keys, values, self.header(plot_name), self.filename(plot_name), plotdir

if __name__ == '__main__':
    ptype = 'RandomPlaylist'
    count = 10
    if len(sys.argv) > 1:
        ptype = sys.argv[1]
    if len(sys.argv) > 2:
        count = int(sys.argv[2])
    plg = PlaylistGenerator(ptype, count)
    plg.create_plots()
